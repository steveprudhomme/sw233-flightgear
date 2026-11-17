"""Compare static cubemap reflections in a dedicated SW233 null-FDM session."""
import argparse
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageChops, ImageStat

from tools.flightgear import execute


def capture(output, port):
    base = f"http://127.0.0.1:{port}"

    def get(path):
        with urlopen(base + "/json" + path, timeout=10) as response:
            return json.load(response).get("value")

    def put(path, value):
        value = int(value) if isinstance(value, bool) else value
        execute(f"setprop({json.dumps(path)},{json.dumps(value)});", port)

    if get("/sim/aircraft") != "sw233" or get("/sim/flight-model") != "null":
        raise ValueError("Dedicated SW233 --fdm=null session required")
    output.mkdir(parents=True, exist_ok=False)
    view = "/sim/current-view/"
    visual = "/sim/sw233/visuals/"
    keys = [view+k for k in ("view-number", "heading-offset-deg", "pitch-offset-deg",
                             "field-of-view")]
    keys += [visual+"canopy-reflection", visual+"instrument-reflection",
             "/sim/menubar/visibility", "/sim/freeze/master"]
    saved = {p: get(p) for p in keys}
    report = {"version": get("/sim/version/flightgear"),
              "skydome_shader": get("/sim/rendering/shaders/skydome"),
              "scope": "Static fair-sky cubemap; not live scenery or flight validation",
              "comparisons": []}
    try:
        put("/sim/freeze/master", 1)
        put("/sim/menubar/visibility", 0)
        for name, camera in {"pilote": (0, 0, -18, 65),
                             "lateral": (0, 70, 0, 75),
                             "exterieur": (1, 140, 15, 25)}.items():
            for p, value in zip(keys[:4], camera):
                put(p, value)
            frames = []
            for state, strength in (("sans", 0), ("fort", 1), ("regle", None)):
                put(visual+"canopy-reflection", .25 if strength is None else strength)
                put(visual+"instrument-reflection", .12 if strength is None else strength)
                time.sleep(.6)
                start_frame = get("/sim/frame-number")
                started = time.monotonic()
                time.sleep(1)
                end_frame = get("/sim/frame-number")
                elapsed = time.monotonic() - started
                report.setdefault("frame_counter_rates", []).append({
                    "view": name, "state": state, "elapsed_seconds": elapsed,
                    "frames": end_frame - start_frame,
                    "fps": (end_frame - start_frame) / elapsed})
                with urlopen(base+"/screenshot?type=jpg", timeout=30) as response:
                    data = response.read()
                frame = Image.open(io.BytesIO(data)).convert("RGB")
                if frame.width < 1024 or frame.height < 600:
                    raise ValueError("Restore the simulator window before capture")
                (output/f"{name}-{state}.jpg").write_bytes(data)
                frames.append(frame)
            difference = ImageChops.difference(frames[0], frames[1])
            report["comparisons"].append({"view": name, "camera": camera,
                "mean_rgb_difference_0_to_1": ImageStat.Stat(difference).mean})
    finally:
        for p, value in saved.items():
            put(p, value)
    report["restoration"] = {p: get(p) == value for p, value in saved.items()}
    if not all(report["restoration"].values()):
        raise ValueError("Session settings were not restored")
    (output/"checks.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    capture(args.output, args.port)

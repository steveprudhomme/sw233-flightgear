"""Capture static radio geometry in a dedicated null-FDM SW233 session."""
import argparse
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from flightgear import execute
from PIL import Image


def capture(folder, port):
    base = f"http://127.0.0.1:{port}"

    def read(path):
        with urlopen(base + path, timeout=20) as r:
            return r.read()

    def get(path):
        return json.loads(read("/json" + path))["value"]

    def put(path, value):
        execute(f"setprop('{path}',{float(value)});", port)

    if (get("/sim/aircraft") != "sw233" or not get("/sim/initialized")
            or get("/sim/flight-model") != "null"):
        raise ValueError("Dedicated initialized SW233 null-FDM session required")
    folder.mkdir(parents=True, exist_ok=False)
    settings = {"/sim/current-view/" + k: v for k, v in {
        "view-number": 0, "heading-offset-deg": 0,
        "pitch-offset-deg": -18, "field-of-view": 20,
        "x-offset-m": -.141, "y-offset-m": .5, "z-offset-m": 1.7,
    }.items()}
    settings["/sim/menubar/visibility"] = 0
    settings["/orientation/heading-deg"] = 10
    saved = {p: get(p) for p in settings}
    frames = []
    try:
        for p, v in settings.items():
            put(p, v)
        for heading in (10, 100):
            put("/orientation/heading-deg", heading)
            for name, x, azimuth in (("face", -.141, 0), ("biais", -.221, -5)):
                put("/sim/current-view/x-offset-m", x)
                put("/sim/current-view/heading-offset-deg", azimuth)
                time.sleep(2)
                content = read("/screenshot?type=jpg")
                with Image.open(io.BytesIO(content)) as im:
                    if im.width < 1024 or im.height < 600:
                        raise RuntimeError("Capture vide : restaurer FlightGear")
                filename = f"{name}-{heading}.jpg"
                (folder / filename).write_bytes(content)
                frames.append({"image": filename, "heading": heading,
                               "x": x, "azimuth": azimuth})
    finally:
        for p, v in saved.items():
            put(p, v)
    (folder / "session.json").write_text(json.dumps({
        "aircraft_dir": get("/sim/aircraft-dir"),
        "version": get("/sim/version/flightgear"),
        "scope": "Static visual inspection only; radio is not functional",
        "settings": settings, "frames": frames, "saved": saved,
        "restored": {p: get(p) for p in saved},
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    capture(args.folder, args.port)

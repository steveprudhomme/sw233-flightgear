"""Capture a paused panel at two headings with unchanged camera settings."""
import argparse
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

from tools.flightgear import execute


def capture(output, port):
    base = f"http://127.0.0.1:{port}"
    def get(path):
        with urlopen(base + "/json" + path, timeout=15) as response:
            return json.load(response)["value"]
    if get("/sim/aircraft") != "sw233" or not get("/sim/freeze/master"):
        raise ValueError("A dedicated paused SW233 session is required")
    settings = {"/sim/current-view/view-number": 0,
                "/sim/current-view/heading-offset-deg": 0,
                "/sim/current-view/pitch-offset-deg": -18,
                "/sim/current-view/field-of-view": 65,
                "/sim/menubar/visibility": 0,
                "/orientation/heading-deg": 10}
    saved = {p: get(p) for p in settings}
    output.mkdir(parents=True, exist_ok=False)
    evidence = {"aircraft_dir": get("/sim/aircraft-dir"),
                "version": get("/sim/version/flightgear"), "camera": settings.copy(),
                "scope": "Paused visual comparison, not flight validation", "frames": []}
    try:
        for path, value in settings.items():
            execute(f'setprop("{path}",{value});', port)
        for heading in (10, 100):
            execute(f'setprop("/orientation/heading-deg",{heading});', port)
            time.sleep(2)
            with urlopen(base + "/screenshot?type=jpg", timeout=30) as response:
                content = response.read()
            with Image.open(io.BytesIO(content)) as frame:
                if frame.width < 1024 or frame.height < 600:
                    raise ValueError("Restore the FlightGear window before capturing")
            name = f"heading-{heading:03d}.jpg"
            (output / name).write_bytes(content)
            evidence["frames"].append({"file": name,
                "heading": get("/orientation/heading-deg"),
                "local_time": get("/sim/time/local-time-string")})
    finally:
        for path, value in saved.items():
            execute(f'setprop("{path}",{float(value)});', port)
    (output / "capture.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    capture(args.output, args.port)

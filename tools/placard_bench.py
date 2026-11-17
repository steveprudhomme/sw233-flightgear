"""Capture both placard languages from three repeatable static cockpit views."""

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

    if get("/sim/aircraft") != "sw233" or get("/sim/flight-model") != "null":
        raise ValueError("A dedicated SW233 session with --fdm=null is required")
    output.mkdir(parents=True, exist_ok=False)
    prefix = "/sim/current-view/"
    common = {"view-number": 0, "heading-offset-deg": 0, "y-offset-m": .5}
    views = {
        "compare": {"x-offset-m": 0, "z-offset-m": 1.7,
                    "pitch-offset-deg": -23, "field-of-view": 32},
        "pilote": {"x-offset-m": 0, "z-offset-m": 1.65,
                   "pitch-offset-deg": -18, "field-of-view": 80},
        "biais": {"x-offset-m": .13, "z-offset-m": 1.7,
                  "pitch-offset-deg": -23, "field-of-view": 32},
    }
    paths = [prefix + k for k in common | views["compare"]]
    paths.extend(["/sim/sw233/language", "/sim/menubar/visibility"])
    saved = {p: get(p) for p in paths}
    report = {"scope": "Static display test, not flight validation",
              "version": get("/sim/version/flightgear"),
              "aircraft_dir": get("/sim/aircraft-dir"), "frames": []}
    try:
        execute('setprop("/sim/menubar/visibility",0);', port)
        for language in ("fr", "en"):
            execute(f'sw233_language.choose("{language}");', port)
            for name, values in views.items():
                settings = common | values
                execute("".join(f'setprop("{prefix}{k}",{v});'
                                for k, v in settings.items()), port)
                time.sleep(1)
                with urlopen(base + "/screenshot?type=jpg", timeout=30) as response:
                    content = response.read()
                with Image.open(io.BytesIO(content)) as frame:
                    if frame.width < 1024 or frame.height < 600:
                        raise ValueError("Restore the FlightGear window before capturing")
                filename = f"{language}-{name}.jpg"
                (output / filename).write_bytes(content)
                report["frames"].append({"file": filename, "camera": settings,
                                         "language": get("/sim/sw233/language")})
    finally:
        execute("".join(f'setprop({json.dumps(p)},{json.dumps(v)});'
                        for p, v in saved.items()), port)
    (output / "capture.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    capture(args.output, args.port)

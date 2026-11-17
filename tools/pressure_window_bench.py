"""Check the live pressure window in a dedicated null-FDM FlightGear session."""
import argparse
import csv
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from flightgear import execute
from PIL import Image


def capture(folder, port, oblique=False):
    base = f"http://127.0.0.1:{port}"

    def read(path):
        with urlopen(base + path, timeout=20) as response:
            return response.read()

    def value(path):
        return json.loads(read("/json" + path))["value"]

    def put(path, val):
        execute(f"setprop('{path}',{float(val)});", port)

    if (value("/sim/aircraft") != "sw233" or not value("/sim/initialized")
            or value("/sim/flight-model") != "null"):
        raise ValueError("Charger une session SW233 dediee avec --fdm=null")
    folder.mkdir(parents=True, exist_ok=False)
    setting = "/instrumentation/altimeter/setting-inhg"
    service = "/instrumentation/altimeter/serviceable"
    settings = {"/sim/current-view/" + k: v for k, v in {
        "view-number": 0, "heading-offset-deg": -5 if oblique else 0,
        "pitch-offset-deg": -25, "field-of-view": 24,
        "x-offset-m": -.30 if oblique else -.22,
        "y-offset-m": .5, "z-offset-m": 1.7,
    }.items()}
    settings["/sim/menubar/visibility"] = 0
    settings[service] = 1
    saved = {p: value(p) for p in [*settings, setting]}
    try:
        for p, v in settings.items():
            put(p, v)
        with (folder / "pressions.csv").open("w", newline="") as f:
            log = csv.writer(f)
            log.writerow(["requested_inhg", "before", "after", "expected_text",
                          "indicated_altitude_ft", "image"])
            for pressure in (28, 28.92, 29.92, 29.99, 30, 30.01, 30.92, 31):
                put(setting, pressure)
                time.sleep(.8)
                before = value(setting)
                content = read("/screenshot?type=jpg")
                with Image.open(io.BytesIO(content)) as im:
                    if im.width < 1024 or im.height < 600:
                        raise RuntimeError("Capture vide : restaurer FlightGear")
                after = value(setting)
                if abs(before-pressure) > 1e-8 or abs(after-pressure) > 1e-8:
                    raise RuntimeError("Calage instable")
                name = f"pression-{pressure:.2f}.jpg"
                (folder / name).write_bytes(content)
                log.writerow([pressure, before, after, f"{pressure:.2f}",
                              value("/instrumentation/altimeter/indicated-altitude-ft"), name])
    finally:
        for p, v in saved.items():
            put(p, v)
    (folder / "session.json").write_text(json.dumps({
        "aircraft_dir": value("/sim/aircraft-dir"),
        "version": value("/sim/version/flightgear"),
        "scope": "Static display test; inspect the screenshots, not an OCR assertion",
        "test_settings": settings, "saved": saved,
        "restored": {p: value(p) for p in saved},
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--oblique", action="store_true")
    args = parser.parse_args()
    capture(args.folder, args.port, args.oblique)

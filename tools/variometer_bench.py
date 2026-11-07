"""Capture the variometer display at known instrument inputs in a dedicated SW233 session."""

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.request import urlopen

from flightgear import execute


def capture(folder, port):
    url = f"http://127.0.0.1:{port}"

    def read(path):
        with urlopen(url + path, timeout=10) as response:
            return response.read()

    def value(prop):
        return json.loads(read("/json" + prop))["value"]

    def put(prop, val):
        execute(f"setprop('{prop}',{float(val)});", port)

    if value("/sim/aircraft") != "sw233" or not value("/sim/initialized"):
        raise RuntimeError("Charger le SW233 dans une session de test")
    folder.mkdir(parents=True, exist_ok=False)
    node = "/instrumentation/vertical-speed-indicator/"
    view = "/sim/current-view/"
    camera = {
        "view-number": 0,
        "heading-offset-deg": 0,
        "pitch-offset-deg": -30,
        "field-of-view": 22,
        "x-offset-m": 0.295,
        "y-offset-m": 0.5,
        "z-offset-m": 1.7,
    }
    saved_view = {k: value(view + k) for k in camera}
    service = value(node + "serviceable")
    original = value(node + "indicated-speed-fpm")
    menu = value("/sim/menubar/visibility")
    try:
        for k, v in camera.items():
            put(view + k, v)
        put("/sim/menubar/visibility", 0)
        put(node + "serviceable", 0)
        with (folder / "vario.csv").open("w", newline="") as f:
            log = csv.writer(f)
            log.writerow(["entree_fpm", "avant_fpm", "apres_fpm", "lecture_centaines", "capture"])
            for kt in (-500, 0, 500, 1000):
                put(node + "indicated-speed-fpm", kt)
                time.sleep(0.6)
                before = value(node + "indicated-speed-fpm")
                name = f"vario-{kt}.jpg"
                (folder / name).write_bytes(read("/screenshot?type=jpg"))
                after = value(node + "indicated-speed-fpm")
                if before != kt or after != kt:
                    raise RuntimeError("Entrée instable : capture non validée")
                log.writerow([kt, before, after, kt / 100, name])
    finally:
        put(node + "indicated-speed-fpm", original)
        put(node + "serviceable", service)
        put("/sim/menubar/visibility", menu)
        for k, v in saved_view.items():
            put(view + k, v)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--port", type=int, default=18097)
    args = parser.parse_args()
    capture(args.folder, args.port)

"""Capture the altimeter display at known instrument inputs in a dedicated SW233 session."""

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.request import urlopen

from flightgear import execute


def capture(folder, port, pressure=False):
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
    if pressure and value("/sim/flight-model") != "null":
        raise RuntimeError("Le banc de pression exige --fdm=null")
    folder.mkdir(parents=True, exist_ok=False)
    node = "/instrumentation/altimeter/"
    view = "/sim/current-view/"
    camera = {
        "view-number": 0,
        "heading-offset-deg": 0,
        "pitch-offset-deg": -25,
        "field-of-view": 24,
        "x-offset-m": -0.22,
        "y-offset-m": 0.5,
        "z-offset-m": 1.7,
    }
    saved_view = {k: value(view + k) for k in camera}
    service = value(node + "serviceable")
    original = value(node + "indicated-altitude-ft")
    menu = value("/sim/menubar/visibility")
    try:
        for k, v in camera.items():
            put(view + k, v)
        put("/sim/menubar/visibility", 0)
        put(node + "serviceable", 0)
        with (folder / "altitudes.csv").open("w", newline="") as f:
            log = csv.writer(f)
            log.writerow(["entree_ft", "avant_ft", "apres_ft", "angle_centaines", "capture"])
            for kt in (0, 950, 1000, 1050, 2500):
                put(node + "indicated-altitude-ft", kt)
                time.sleep(0.6)
                before = value(node + "indicated-altitude-ft")
                name = f"alt-{kt}.jpg"
                (folder / name).write_bytes(read("/screenshot?type=jpg"))
                after = value(node + "indicated-altitude-ft")
                if before != kt or after != kt:
                    raise RuntimeError("Entrée instable : capture non validée")
                log.writerow([kt, before, after, (kt * 0.36) % 360, name])
        if pressure:
            setting = value(node + "setting-inhg")
            put(node + "serviceable", 1)
            try:
                with (folder / "pression.csv").open("w", newline="") as f:
                    log = csv.writer(f)
                    log.writerow(
                        [
                            "calage_inhg",
                            "altitude_ft",
                            "pression_statique_inhg",
                            "indication_ft",
                            "capture",
                        ]
                    )
                    height = value("/position/altitude-ft")
                    for qnh in (28.92, 29.92, 30.92):
                        put(node + "setting-inhg", qnh)
                        time.sleep(0.6)
                        altitude = value("/position/altitude-ft")
                        if abs(altitude - height) > 0.01:
                            raise RuntimeError("Altitude non constante")
                        name = f"pression-{qnh:.2f}.jpg"
                        (folder / name).write_bytes(read("/screenshot?type=jpg"))
                        log.writerow(
                            [
                                qnh,
                                altitude,
                                value("/systems/static/pressure-inhg"),
                                value(node + "indicated-altitude-ft"),
                                name,
                            ]
                        )
            finally:
                put(node + "setting-inhg", setting)
    finally:
        put(node + "indicated-altitude-ft", original)
        put(node + "serviceable", service)
        put("/sim/menubar/visibility", menu)
        for k, v in saved_view.items():
            put(view + k, v)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--port", type=int, default=18097)
    parser.add_argument("--pressure", action="store_true")
    args = parser.parse_args()
    capture(args.folder, args.port, args.pressure)

"""Capture imposed compass indications in a dedicated null-FDM session."""
import argparse
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from flightgear import execute
from PIL import Image


def capture(folder, port, seams=False):
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
        raise ValueError("Utiliser une session SW233 dediee --fdm=null")
    folder.mkdir(parents=True, exist_ok=False)
    service = "/instrumentation/magnetic-compass/serviceable"
    heading = "/instrumentation/magnetic-compass/indicated-heading-deg"
    settings = {"/sim/current-view/" + k: v for k, v in {
        "view-number": 0, "heading-offset-deg": 0, "pitch-offset-deg": -26,
        "field-of-view": 17, "x-offset-m": 0, "y-offset-m": .5,
        "z-offset-m": 1.7,
    }.items()}
    settings.update({"/sim/menubar/visibility": 0, service: 0})
    saved = {p: value(p) for p in [*settings, heading]}
    records = []
    try:
        for p, v in settings.items():
            put(p, v)
        for view, x, h in [("face", 0, 0), ("biais", -.08, -5)]:
            put("/sim/current-view/x-offset-m", x)
            put("/sim/current-view/heading-offset-deg", h)
            angles = (0, 45, 90, 135, 180, 225, 270, 359, 1)
            if seams:
                angles += (179, 181, 315)
            for deg in angles:
                put(heading, deg)
                time.sleep(.6)
                before = value(heading)
                data = read("/screenshot?type=jpg")
                with Image.open(io.BytesIO(data)) as im:
                    if im.width < 1024 or im.height < 600:
                        raise RuntimeError("Restaurer FlightGear : image vide")
                after = value(heading)
                if abs(before-deg) > 1e-6 or abs(after-deg) > 1e-6:
                    raise RuntimeError("Indication imposee instable")
                name = f"{view}-{deg:03d}.jpg"
                (folder/name).write_bytes(data)
                records.append(dict(view=view, requested=deg, before=before,
                                    after=after, image=name))
    finally:
        # Restore the imposed value before re-enabling the live instrument.
        for p, v in saved.items():
            if p != service:
                put(p, v)
        put(service, saved[service])
    (folder/"results.json").write_text(json.dumps({
        "version": value("/sim/version/flightgear"),
        "aircraft_dir": value("/sim/aircraft-dir"), "records": records,
        "scope": "Display checks only; inspect images to assess readability",
        "saved": saved, "restored_serviceable": value(service),
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--seams", action="store_true", help="Ajouter 179, 181 et 315 degres")
    args = parser.parse_args()
    capture(args.folder, args.port, args.seams)

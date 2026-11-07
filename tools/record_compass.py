"""Record paired cockpit frames and telemetry in a fresh folder (FlightGear HTTP)."""

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.request import urlopen

from flightgear import execute


def record(folder, port):
    folder.mkdir(parents=True, exist_ok=False)
    url = f"http://127.0.0.1:{port}"

    def read(path):
        with urlopen(url + path, timeout=8) as response:
            return response.read()

    def value(prop):
        return json.loads(read("/json" + prop))["value"]

    if not value("/sim/initialized") or value("/sim/aircraft") != "sw233":
        raise RuntimeError("Charger SW233 avant la capture")
    execute(Path(__file__).with_name("compass-turn.nas").read_text(encoding="utf-8-sig"), port)
    time.sleep(0.25)
    fields = ["time", "phase", "mag", "ind", "roll", "kt", "wind"]
    with (folder / "vol.csv").open("w", newline="") as stream:
        table = csv.writer(stream)
        table.writerow(["frame", *fields])
        deadline = time.monotonic() + 350
        for i in range(2600):
            frame_start = time.monotonic()
            state = json.loads(read("/json/sim/sw233/turn?d=1"))
            vals = {v["name"]: v.get("value") for v in state["children"]}
            frame = f"{i:04d}.jpg"
            (folder / frame).write_bytes(read("/screenshot?type=jpg"))
            table.writerow([frame, *(vals[k] for k in fields)])
            stream.flush()
            if vals["done"]:
                if vals["phase"] != 5:
                    raise RuntimeError("Virages incomplets : conserver la trace pour diagnostic")
                return
            if frame_start > deadline:
                break
            time.sleep(max(0, 0.14 - (time.monotonic() - frame_start)))
    raise RuntimeError("Durée de capture dépassée")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--port", type=int, default=18097)
    args = parser.parse_args()
    record(args.folder, args.port)

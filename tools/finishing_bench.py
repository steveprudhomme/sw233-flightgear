"""Native VIS-05b/c finishing views in a dedicated, restoring null-FDM session."""

import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.request import urlopen

from tools import airframe_bench as bench
from tools.flightgear import execute


def capture(output, port):
    fg = bench.Session(port)
    if fg.get("/sim/aircraft") != "sw233" or fg.get("/sim/flight-model") != "null":
        raise ValueError("Dedicated SW233 null session required")
    execute(
        "".join(
            f'setprop("{p}",{v});'
            for p, v in {
                bench.BRAKE: 0,
                bench.ELEVATOR: 0,
                bench.MASS: 180,
                bench.MASS + "[1]": 180,
            }.items()
        ),
        port,
    )
    target = "/sim/view[1]/config/target-z-offset-m"
    original = fg.get(target)
    frames = bench.FRAMES
    try:
        fg.put(target, 1.5)
        bench.FRAMES = (
            ("lumiere-a", 140, 15, 17, 25, {"/orientation/heading-deg": 10}),
            ("lumiere-b", 320, 15, 17, 25, {"/orientation/heading-deg": 190}),
            (
                "grille",
                140,
                35,
                18,
                25,
                {bench.VIS + "uv-grid": True, "/orientation/heading-deg": 10},
            ),
            (
                "coque-sans-livree",
                90,
                0,
                14,
                25,
                {bench.VIS + "livery": False, "/orientation/heading-deg": 10},
            ),
            ("cadres", 140, 25, 13, 25, {"/orientation/heading-deg": 10}),
        )
        bench.capture(output / "exterieur", port)
    finally:
        bench.FRAMES = frames
        fg.put(target, original)
    original_view = fg.get(bench.VIEW + "view-number")
    fg.put(bench.VIEW + "view-number", 0)
    keys = (*bench.ANGLE_KEYS, "/sim/menubar/visibility")
    saved = {p: fg.get(p) for p in keys}
    try:
        for p, v in zip(keys, (0, -18, 80, False)):
            fg.put(p, v)
        time.sleep(1)
        data = urlopen(fg.base + "/screenshot?type=png", timeout=30).read()
        (output / "cockpit.png").write_bytes(data)
        (output / "cockpit.json").write_text(
            json.dumps(
                {
                    "settings": {p: fg.get(p) for p in keys},
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "purpose": "Static instrument visibility, not flight validation",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    finally:
        for p, v in saved.items():
            fg.put(p, v)
        fg.put(bench.VIEW + "view-number", original_view)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    capture(args.output, args.port)

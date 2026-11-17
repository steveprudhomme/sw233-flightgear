"""Capture the unchanged aircraft for VIS-05a using the existing restoring bench."""

import argparse
from pathlib import Path

from tools import airframe_bench as bench
from tools.flightgear import execute

GENERAL = (
    ("arriere", 0, 0, 55, 25, {}),
    ("avant", 180, 0, 55, 25, {}),
    ("profil-a", 90, 0, 45, 25, {}),
    ("profil-b", 270, 0, 45, 25, {}),
    ("dessus", 0, 85, 55, 25, {}),
    ("dessous", 0, -85, 55, 25, {}),
)
CLOSE = (
    ("nez-profil", 90, 0, 14, 25, {}),
    ("nez-oblique", 140, 15, 17, 25, {}),
    ("verriere-dessus", 140, 50, 17, 25, {}),
)


def capture(output, port):
    fg = bench.Session(port)
    if fg.get("/sim/aircraft") != "sw233" or fg.get("/sim/flight-model") != "null":
        raise ValueError("Dedicated SW233 null session required")
    # The isolated null session does not initialize JSBSim visual properties.
    execute(
        "".join(f'setprop("{p}",0);' for p in (bench.BRAKE, bench.ELEVATOR))
        + f'setprop("{bench.MASS}",180);setprop("{bench.MASS}[1]",180);',
        port,
    )
    target = "/sim/view[1]/config/target-z-offset-m"
    original = fg.get(target)
    if original is None:
        raise ValueError("Expected configured exterior target")
    frames = bench.FRAMES
    try:
        bench.FRAMES = GENERAL
        bench.capture(output / "general", port)
        fg.put(target, 1.5)
        bench.FRAMES = CLOSE
        bench.capture(output / "details", port)
    finally:
        bench.FRAMES = frames
        fg.put(target, original)
        if fg.get(target) != original:
            raise RuntimeError("Exterior target restoration failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    capture(args.output, args.port)

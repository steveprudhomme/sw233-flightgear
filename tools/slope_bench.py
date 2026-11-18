"""Native planar ramp checks; frozen geometry test, not a landing simulation."""

import argparse
import json
import math
import time
from pathlib import Path

from tools.flightgear import execute
from tools.glass_bench import VIEW, Session
from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]
BASE = "/sim/sw233/gear/"


def mesh_lift(h, sx, sy):
    """Project every actual mesh vertex against z=h+sx*x+sy*y."""
    _, objects = read_mesh(ROOT / "src/SW233/Models/sw233.ac")
    return max(
        0,
        max(
            h + sx * (p[0] - 2.559214) + sy * p[1] - (p[2] + 0.845)
            for _, face in objects["roue"]
            for p in face
        ),
    )


def native_math(port):
    """Check Nasal against actual mesh vertices and reject unusable samples."""
    s = Session(port)
    cases = []
    for h in [0, 0.03, 0.10]:
        for ax, ay in [
            (0, 0),
            (25, 0),
            (-25, 0),
            (0, 25),
            (0, -25),
            (20, 20),
            (-20, -20),
            (20, -20),
            (-20, 20),
        ]:
            sx, sy = math.tan(math.radians(ax)), math.tan(math.radians(ay))
            cases.append((f"sw233_gear.terrain_offset([{h},{sx},{sy}],1)", mesh_lift(h, sx, sy)))
    cases += [
        ("sw233_gear.terrain_offset([.1,.4,.4],0)", 0),
        ("sw233_gear.terrain_offset(nil,1)", 0),
        ("sw233_gear.plane(0,nil,0,0,0)==nil", 1),
        ("sw233_gear.plane(0,.1,.1,0,0)==nil", 1),
        ("sw233_gear.plane(0,0,0,.1,.1)==nil", 1),
        ("sw233_gear.plane(0,.6,0,0,0)==nil", 1),
        ("sw233_gear.plane(0,.1,-.1,.1,-.1)!=nil", 1),
    ]
    rows = []
    for expr, expected in cases:
        execute(f'setprop("/sim/bench/result",{expr});', port)
        actual = s.get("/sim/bench/result")
        if abs(actual - expected) > 0.00002:
            raise AssertionError((expr, actual, expected))
        rows.append(dict(expression=expr, actual=actual, expected=expected))
    return rows


def run(port, scenery, output):
    s = Session(port)
    output.mkdir(parents=True, exist_ok=False)
    if s.get("/sim/flight-model") != "null":
        raise ValueError("Dedicated --fdm=null session required")
    (output / "math.json").write_text(
        json.dumps(native_math(port), indent=2) + "\n", encoding="utf-8"
    )
    ramps = json.loads((scenery / "ramps.json").read_text())
    results = []
    execute(
        'setprop("/sim/freeze/master",1);setprop("/sim/menubar/visibility",0);'
        'setprop("/sim/sw233/visuals/crew",0);setprop("/orientation/heading-deg",0);'
        'setprop("/orientation/pitch-deg",0);setprop("/orientation/roll-deg",0);'
        'setprop("/sim/current-view/view-number",1);',
        port,
    )
    for key, value in [
        ("target-z-offset-m", 2.559214),
        ("target-y-offset-m", -0.60),
        ("heading-offset-deg", 270),
        ("pitch-offset-deg", 0),
        ("field-of-view", 7),
    ]:
        s.put(("/sim/view[1]/config/" if key.startswith("target-") else VIEW) + key, value)
    execute("sw233_gear.bench_update=sw233_gear.update;sw233_gear.update=func {};", port)
    try:
        for r in ramps:
            s.put("/position/latitude-deg", r["latitude"])
            s.put("/position/longitude-deg", r["longitude"])
            s.put("/position/altitude-ft", 65 / 0.3048)
            time.sleep(2)
            # Force a view so nearby scenery is paged in before querying it.
            s.screenshot()
            execute(
                "var c=aircraftToCart({x:-2.559214,y:0,z:.845});"
                "var g=carttogeod(c.x,c.y,c.z);var h=geodinfo(g[0],g[1],1000);"
                'setprop("/sim/bench/ground",h[0]);',
                port,
            )
            ground = s.get("/sim/bench/ground")
            if not 57 < ground < 63:
                raise AssertionError(f"Ramp not loaded: {ground}")
            s.put("/position/altitude-ft", (ground + 0.845 - 0.03) / 0.3048)
            for _ in range(4):
                time.sleep(0.4)
                execute('setprop("/sim/bench/h",sw233_gear.ground_height(0,0));', port)
                measured = s.get("/sim/bench/h")
                if measured is None:
                    raise AssertionError("Terrain ray missed")
                s.put(
                    "/position/altitude-ft",
                    s.get("/position/altitude-ft") + (measured - 0.03) / 0.3048,
                )
            time.sleep(0.4)
            execute('setprop("/gear/gear/wow",1);sw233_gear.bench_update();', port)
            data = {
                key: s.get(BASE + key)
                for key in [
                    "terrain-valid",
                    "terrain-height-m",
                    "terrain-slope-x",
                    "terrain-slope-y",
                    "main-offset-m",
                    "mode",
                ]
            }
            if not data["terrain-valid"]:
                raise AssertionError(data)
            h, sx, sy = [
                data[k] for k in ["terrain-height-m", "terrain-slope-x", "terrain-slope-y"]
            ]
            if abs(h - 0.03) > 0.001:
                raise AssertionError(("height", h))
            expected = mesh_lift(h, sx, sy)
            error = data["main-offset-m"] - expected
            if abs(error) > 0.00002:
                raise AssertionError((r, data, expected))
            # Orientation mapping is checked separately from the mesh oracle.
            if abs(sx - r["slope_x"]) > 0.001 or abs(sy - r["slope_y"]) > 0.001:
                raise AssertionError(("slope mismatch", r, data))
            if r["index"] in [1, 3, 5]:
                # Freeze timer callbacks while recording an explicit before/after pose.
                execute('setprop("/sim/sw233/gear/main-offset-m",0);', port)
                time.sleep(0.4)
                (output / f"pente-{r['index']}-avant.jpg").write_bytes(s.screenshot())
                execute('setprop("/gear/gear/wow",1);sw233_gear.bench_update();', port)
                time.sleep(0.4)
                (output / f"pente-{r['index']}-apres.jpg").write_bytes(s.screenshot())
            results.append(dict(ramp=r, properties=data, expected_m=expected, error_m=error))
    finally:
        execute("sw233_gear.update=sw233_gear.bench_update;", port)
    (output / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", type=int, required=True)
    p.add_argument("--scenery", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(run(a.port, a.scenery, a.output), indent=2))

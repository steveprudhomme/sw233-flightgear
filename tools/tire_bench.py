"""Compare the native tyre animation to an independent mesh support calculation."""
import argparse
import json
import math
from pathlib import Path

from tools.flightgear import execute
from tools.glass_bench import Session
from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]


def mesh_offset(compression, pitch, roll, mesh=None):
    """Oracle: project actual vertices relative to the unloaded contact point."""
    _, objects = read_mesh(mesh or ROOT/'src/SW233/Models/sw233.ac')
    points = [p for _, face in objects['roue'] for p in face]
    center_x = (max(p[0] for p in points)+min(p[0] for p in points))/2
    bottom = min(p[2] for p in points)
    theta, phi = math.radians(pitch), math.radians(roll)
    normal = (-math.sin(theta), -math.sin(phi)*math.cos(theta),
              math.cos(phi)*math.cos(theta))
    minimum = min(sum(a*b for a, b in zip((p[0]-center_x, p[1], p[2]-bottom), normal))
                  for p in points)
    return compression*.3048 - minimum/normal[2]


def native_checks(port):
    s = Session(port)
    cases = [(c, p, r, 1) for c in [0, .04, .15]
             for p, r in [(0, 0), (-7, -13), (-7, 13), (10, -30), (10, 30)]]
    cases += [(None, 0, 0, 1), (.04, None, 0, 1), (.04, 0, None, 1),
              (.04, 0, 0, 0), (.04, 0, 0, None), (-1, 0, 0, 1),
              (1, 0, 0, 1), (.04, 0, 80, 1), (.04, 60, 0, 1)]
    code = []
    for i, args in enumerate(cases):
        literals = ','.join('nil' if x is None else str(x) for x in args)
        code.append(f'setprop("/sim/sw233/gear/tests/case-{i}",sw233_gear.offset({literals}));')
    execute('\n'.join(code), port)
    results = []
    for i, args in enumerate(cases):
        actual = s.get(f'/sim/sw233/gear/tests/case-{i}')
        expected = mesh_offset(*args[:3]) if i < 15 else 0
        error = actual-expected
        if abs(error) > .00002:
            raise AssertionError((args, actual, expected))
        results.append(dict(arguments=args, offset_m=actual, expected_m=expected, error_m=error))
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    results = native_checks(args.port)
    args.output.write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
    print(f'{len(results)} native tyre checks passed')

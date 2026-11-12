"""Verify elevator travel and native animation in a dedicated ground-test session."""

import argparse
import json
import math
import time
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute


def capture(folder, port, limit):
    base = f'http://127.0.0.1:{port}'
    def value(p):
        with urlopen(base + '/json' + p, timeout=10) as response:
            return json.load(response)['value']
    def put(p, v):
        execute(f"setprop('{p}',{float(v)});", port)
    if value('/sim/aircraft') != 'sw233' or value('/sim/flight-model') != 'jsb':
        raise RuntimeError('A dedicated SW233 JSBSim session is required')
    if not value('/sim/initialized'):
        raise RuntimeError('Wait for initialization')
    settings = {'/controls/flight/elevator-trim': 0,
                '/sim/current-view/view-number': 0,
                '/sim/current-view/x-offset-m': 0,
                '/sim/current-view/y-offset-m': 1.4,
                '/sim/current-view/z-offset-m': 10,
                '/sim/current-view/heading-offset-deg': 0,
                '/sim/current-view/pitch-offset-deg': -25,
                '/sim/current-view/field-of-view': 85,
                '/sim/menubar/visibility': 0}
    command = '/controls/flight/elevator'
    actual = '/fdm/jsbsim/fcs/elevator-pos-rad'
    saved = {p: value(p) for p in [*settings, command]}
    folder.mkdir(parents=True, exist_ok=False)
    rows = []
    try:
        for p, v in settings.items():
            put(p, v)
        for demand, name in ((0, 'neutre'), (-1, 'haut'), (1, 'bas')):
            put(command, demand)
            time.sleep(1)
            before = value(actual)
            if abs(math.degrees(before) - demand * limit) > 0.001:
                raise AssertionError('Effective travel does not match requested limit')
            with urlopen(base + '/screenshot?type=jpg', timeout=20) as response:
                (folder / f'{name}.jpg').write_bytes(response.read())
            after = value(actual)
            if abs(after - before) > 1e-6:
                raise AssertionError('Deflection changed during capture')
            rows.append(dict(command=demand, before_rad=before, after_rad=after,
                             degrees=math.degrees(before), image=f'{name}.jpg'))
    finally:
        for p, v in saved.items():
            put(p, v)
    (folder / 'native.json').write_text(json.dumps({'camera': settings, 'rows': rows}, indent=2),
                                      encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--port', type=int, default=18097)
    parser.add_argument('--limit-deg', type=float, default=23)
    args = parser.parse_args()
    capture(args.folder, args.port, args.limit_deg)


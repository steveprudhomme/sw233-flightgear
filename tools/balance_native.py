"""Capture native FlightGear mass readings in a dedicated ground-test session."""

import argparse
import json
import time
from pathlib import Path
from urllib.request import urlopen

from tools.balance import source_balance
from tools.flightgear import execute


def capture(folder, port):
    base = f'http://127.0.0.1:{port}'

    def value(path):
        with urlopen(base + '/json' + path, timeout=10) as response:
            return json.load(response)['value']

    def put(path, number):
        execute(f"setprop('{path}',{float(number)});", port)

    if value('/sim/aircraft') != 'sw233' or value('/sim/flight-model') != 'jsb':
        raise RuntimeError('Use SW233 with JSBSim in a dedicated ground-test session')
    if not value('/sim/initialized'):
        raise RuntimeError('Wait for FlightGear initialization')
    folder.mkdir(parents=True, exist_ok=False)
    prefix = '/fdm/jsbsim/inertia/'
    props = [prefix + 'pointmass-weight-lbs', prefix + 'pointmass-weight-lbs[1]']
    saved = [value(p) for p in props]
    rows = []
    execute('gui.showWeightDialog();', port)
    try:
        for front, rear in ((180, 180), (180, 0), (140, 220)):
            for p, w in zip(props, (front, rear)):
                put(p, w)
            expected_weight, expected_cg = source_balance(front, rear)
            for _ in range(100):
                weight = value(prefix + 'weight-lbs')
                cg = value(prefix + 'cg-x-in')
                if abs(weight - expected_weight) < 1e-5 and abs(cg - expected_cg[0]) < 1e-5:
                    break
                time.sleep(0.1)
            else:
                raise AssertionError('Native mass balance did not settle')
            time.sleep(0.5)
            name = f'chargement-{front}-{rear}.jpg'
            with urlopen(base + '/screenshot?type=jpg', timeout=20) as response:
                (folder / name).write_bytes(response.read())
            if abs(value(prefix + 'cg-x-in') - cg) > 1e-5:
                raise AssertionError('CG changed during capture')
            rows.append(dict(front_lbs=front, rear_lbs=rear, weight_lbs=weight,
                             cg_x_in=cg, expected_cg_x_in=expected_cg[0], capture=name))
    finally:
        for p, w in zip(props, saved):
            put(p, w)
    (folder / 'native.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--port', type=int, default=18097)
    args = parser.parse_args()
    capture(args.folder, args.port)

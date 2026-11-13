"""Exercise occupant actions in a dedicated, stationary FlightGear session."""
import argparse
import json
import time
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute


def bench(folder, port):
    base = f'http://127.0.0.1:{port}'
    def get(p):
        with urlopen(base + '/json' + p, timeout=10) as response:
            return json.load(response)['value']
    def run(script):
        execute(script, port)
    if get('/sim/aircraft') != 'sw233' or not get('/gear/gear/wow'):
        raise RuntimeError('Use a dedicated SW233 session on the ground')
    folder.mkdir(parents=True, exist_ok=False)
    paths = ['/fdm/jsbsim/inertia/' + p for p in
             ['pointmass-weight-lbs', 'pointmass-weight-lbs[1]', 'weight-lbs', 'cg-x-in']]
    run('setprop("/sim/sw233/test-guards", sw233_load.stationary(1,0) and '
        '!sw233_load.stationary(0,0) and !sw233_load.stationary(1,2) and '
        '!sw233_load.stationary(1,nil));')
    if not get('/sim/sw233/test-guards'):
        raise AssertionError('Ground/motion guard failed')
    original = [get(p) for p in paths[:2]]
    rows = []
    run('sw233_load.dialog.open();')
    try:
        cases = [('solo', 'sw233_load.preset(180,0);', 180, 0),
                 ('biplace', 'sw233_load.preset(180,180);', 180, 180),
                 ('avant-plus', 'sw233_load.step(0,5);', 185, 180),
                 ('arriere-moins', 'sw233_load.step(1,-5);', 185, 175),
                 ('personnalise', 'sw233_load.preset(220,140);', 220, 140),
                 ('refus', 'sw233_load.stage(-1,140); sw233_load.apply();', 220, 140),
                 ('texte', 'setprop(sw233_load.base~"front","abc"); sw233_load.apply();', 220, 140),
                 ('restaure', 'sw233_load.restore();', *original)]
        for name, script, front, rear in cases:
            run(script + 'fgcommand("dialog-update");')
            time.sleep(1)
            values = [get(p) for p in paths]
            expected = [front, rear, 610 + front + rear,
                        (610 * 103.2 + front * 43 + rear * 85) / (610 + front + rear)]
            if any(abs(a-b) > 0.0002 for a, b in zip(values, expected)):
                raise AssertionError((name, values, expected))
            data = urlopen(base + '/screenshot?type=jpg', timeout=20).read()
            if len(data) < 10000:
                raise RuntimeError('Restore FlightGear window before capturing')
            (folder / (name + '.jpg')).write_bytes(data)
            rows.append(dict(case=name, values=values, expected=expected,
                             message=get('/sim/sw233/occupants/message')))
    finally:
        run('sw233_load.restore();')
    (folder / 'native.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--port', type=int, default=18097)
    args = parser.parse_args()
    bench(args.folder, args.port)

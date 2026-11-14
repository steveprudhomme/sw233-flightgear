"""Capture an unretouched exterior preview from a dedicated paused FlightGear session."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute


def capture(folder, port):
    base = f'http://127.0.0.1:{port}'
    def get(path):
        with urlopen(base + '/json' + path, timeout=15) as response:
            return json.load(response)['value']
    if get('/sim/aircraft') != 'sw233' or not get('/sim/freeze/master'):
        raise ValueError('Pause SW233 after loading; verify /sim/freeze/master.')
    if get('/position/altitude-ft') < 1000:
        raise ValueError('Start in air at 5000 ft for this preview recipe.')
    settings = {'/sim/current-view/view-number': 1,
                '/sim/current-view/heading-offset-deg': 140,
                '/sim/current-view/pitch-offset-deg': 20,
                '/sim/current-view/field-of-view': 45,
                '/sim/menubar/visibility': 0}
    saved = {p: get(p) for p in settings}
    folder.mkdir(parents=True, exist_ok=False)
    try:
        for p, v in settings.items():
            execute(f'setprop("{p}",{v});', port)
        time.sleep(1)
        altitude = get('/position/altitude-ft')
        with urlopen(base + '/screenshot?type=jpg', timeout=20) as response:
            content = response.read()
        if len(content) < 10000 or abs(get('/position/altitude-ft')-altitude) > 0.1:
            raise ValueError('Empty or moving scene; inspect the paused session.')
        (folder / 'exterior.jpg').write_bytes(content)
        metadata = dict(camera=settings, altitude_ft=altitude,
                        scene='CYJN, paused presentation; not flight validation',
                        aircraft_dir=get('/sim/aircraft-dir'),
                        fg_version=get('/sim/version/flightgear'),
                        sha256=hashlib.sha256(content).hexdigest())
        (folder / 'capture.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    finally:
        for p, v in saved.items():
            execute(f'setprop("{p}",{float(v)});', port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--port', type=int, default=18101)
    args = parser.parse_args()
    capture(args.folder, args.port)

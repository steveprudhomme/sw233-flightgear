"""Capture repeatable cockpit enclosure views in a dedicated paused FG session."""
import argparse
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

from tools.flightgear import execute

VIEWS = {
    'profil-gauche': (1, 90, 0, 25),
    'profil-droit': (1, 270, 0, 25),
    'trois-quarts': (1, 140, 15, 25),
    'dessus': (1, 180, 80, 45),
    'cockpit': (0, 0, -18, 80),
}


def capture(output, port):
    base = f'http://127.0.0.1:{port}'
    def get(path):
        with urlopen(base + '/json' + path, timeout=15) as response:
            return json.load(response)['value']
    if get('/sim/aircraft') != 'sw233':
        raise ValueError('Dedicated SW233 session required')
    output.mkdir(parents=True, exist_ok=False)
    execute('setprop("/sim/freeze/master",1);', port)
    paths = ['/sim/current-view/view-number', '/sim/current-view/heading-offset-deg',
             '/sim/current-view/pitch-offset-deg', '/sim/current-view/field-of-view']
    original = {p: get(p) for p in paths}
    menu = get('/sim/menubar/visibility')
    evidence = dict(aircraft_dir=get('/sim/aircraft-dir'),
                    version=get('/sim/version/flightgear'),
                    altitude_ft=get('/position/altitude-ft'), views=VIEWS)
    try:
        execute('setprop("/sim/menubar/visibility",0);', port)
        for name, values in VIEWS.items():
            # Switching the view can reset its configuration, so set it first.
            execute(f'setprop("{paths[0]}",{values[0]});', port)
            execute(''.join(f'setprop("{p}",{v});' for p, v in
                            zip(paths[1:], values[1:])), port)
            time.sleep(0.8)
            with urlopen(base + '/screenshot?type=jpg', timeout=20) as response:
                content = response.read()
            with Image.open(io.BytesIO(content)) as frame:
                if frame.width < 1024 or frame.height < 600:
                    raise ValueError('Restore the FlightGear window: empty/minimized capture')
            (output / (name + '.jpg')).write_bytes(content)
    finally:
        execute(''.join(f'setprop("{p}",{float(v)});' for p, v in original.items()) +
                f'setprop("/sim/menubar/visibility",{float(menu)});', port)
    (output / 'capture.json').write_text(json.dumps(evidence, indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--port', type=int, default=18102)
    args = parser.parse_args()
    capture(args.output, args.port)

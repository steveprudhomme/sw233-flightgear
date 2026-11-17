"""Capture canopy fixtures in an explicitly dedicated SW233 session."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute
from tools.glass_bench import CAMERA_KEYS, VIEW, Session


def capture(output, port):
    fg = Session(port)
    if fg.get('/sim/aircraft') != 'sw233':
        raise ValueError('Dedicated SW233 session required')
    output.mkdir(parents=True, exist_ok=False)
    keys = ('/sim/freeze/master', '/sim/menubar/visibility',
            '/sim/sw233/visuals/crew', '/sim/view[1]/config/target-z-offset-m')
    saved = {k: fg.get(k) for k in keys}
    original = fg.get(VIEW+'view-number')
    cameras = {}
    report = {'version': fg.get('/sim/version/flightgear'),
              'aircraft': fg.get('/sim/aircraft-dir'),
              'method': 'Static position fixtures, not timed animation measurements', 'frames': []}
    execute(Path(__file__).with_name('canopy-tests.nas').read_text(), port)
    report['native_assertions'] = fg.get('/sim/sw233/canopy/tests-passed')
    assert report['native_assertions'] == 14
    try:
        fg.put(keys[0], 1)
        fg.put(keys[1], 0)
        fg.put(keys[3], 1.5)
        for view, label, angles in ((1, 'exterieur', (220, 20, 22)),
                                    (0, 'cockpit', (-55, 0, 90)),
                                    (1, 'dessus', (180, 75, 20))):
            fg.put(VIEW+'view-number', view)
            if view not in cameras:
                cameras[view] = {k: fg.get(k) for k in CAMERA_KEYS}
            for k, v in zip(CAMERA_KEYS, angles):
                fg.put(k, v)
            for crew in (0, 1):
                fg.put(keys[2], crew)
                for pct in (0, 25, 50, 75, 100):
                    execute(f'sw233_canopy.position={pct/100};sw233_canopy.target={pct/100};'
                            'sw233_canopy.refused=0;sw233_canopy.publish();', port)
                    time.sleep(.5)
                    name = f'{label}-equipage-{crew}-{pct:03d}.png'
                    data = urlopen(fg.base+'/screenshot?type=png', timeout=30).read()
                    (output/name).write_bytes(data)
                    report['frames'].append({
                        'image': name, 'position': fg.get('/sim/sw233/canopy/position'),
                        'crew': crew, 'sha256': hashlib.sha256(data).hexdigest()})
    finally:
        execute('sw233_canopy.reset();', port)
        for view, values in cameras.items():
            fg.put(VIEW+'view-number', view)
            for k, v in values.items():
                fg.put(k, v)
        fg.put(VIEW+'view-number', original)
        for k, v in saved.items():
            fg.put(k, v)
        (output/'canopy-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--port', required=True, type=int)
    args = parser.parse_args()
    capture(args.output, args.port)

"""Compare central root junction in dedicated native SW233 sessions."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute
from tools.glass_bench import VIEW, Session


def capture(output, port):
    fg = Session(port)
    if fg.get('/sim/aircraft') != 'sw233':
        raise ValueError('Dedicated SW233 required')
    output.mkdir(parents=True, exist_ok=False)
    keys = ('/sim/freeze/master', '/sim/menubar/visibility', '/sim/sw233/visuals/crew',
            '/sim/view[1]/config/target-z-offset-m', '/sim/view[0]/config/limits/enabled',
            '/orientation/heading-deg')
    saved = {k: fg.get(k) for k in keys}
    original = fg.get(VIEW+'view-number')
    angles = ['heading-offset-deg', 'pitch-offset-deg', 'field-of-view',
              'x-offset-m', 'y-offset-m', 'z-offset-m']
    cameras = {}
    report = {'aircraft': fg.get('/sim/aircraft-dir'), 'version': fg.get('/sim/version/flightgear'),
              'method': 'Static native comparisons; no photographic dimensions claimed',
              'frames': []}
    frames = [('dessus', 1, 180, 75, 13, None), ('oblique', 1, 140, 25, 13, None),
              ('dossier', 0, 180, -15, 85, (0, .50, 1.65)),
              ('racine-gauche', 0, 65, 22, 60, (0, .58, 2.39)),
              ('racine-droite', 0, -65, 22, 60, (0, .58, 2.39))]
    try:
        fg.put(keys[5], 190)
        fg.put(keys[4], 0)
        fg.put(keys[0], 1)
        fg.put(keys[1], 0)
        fg.put(keys[3], 2.3)
        for label, view, heading, pitch, fov, position in frames:
            fg.put(VIEW+'view-number', view)
            if view not in cameras:
                cameras[view] = {k: fg.get(VIEW+k) for k in angles}
            values = dict(zip(angles[:3], (heading, pitch, fov)))
            if position:
                values.update(zip(angles[3:], position))
            for k, v in values.items():
                fg.put(VIEW+k, v)
            for crew in (0, 1):
                fg.put(keys[2], crew)
                for opened in (0, 1):
                    execute(f'sw233_canopy.position={opened};sw233_canopy.target={opened};'
                            'sw233_canopy.publish();', port)
                    time.sleep(.5)
                    name = f'{label}-equipage-{crew}-ouvert-{opened}.png'
                    data = urlopen(fg.base+'/screenshot?type=png', timeout=30).read()
                    (output/name).write_bytes(data)
                    report['frames'].append({'image': name, 'view': values, 'crew': crew,
                                             'opened': opened,
                                             'sha256': hashlib.sha256(data).hexdigest()})
    finally:
        execute('sw233_canopy.reset();', port)
        for view, values in cameras.items():
            fg.put(VIEW+'view-number', view)
            for k, v in values.items():
                fg.put(VIEW+k, v)
        fg.put(VIEW+'view-number', original)
        for k, v in saved.items():
            fg.put(k, v)
        (output/'rapport.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path)
    p.add_argument('--port', required=True, type=int)
    args = p.parse_args()
    capture(args.output, args.port)

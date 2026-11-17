"""Capture UV, moving surfaces and near/far crew in an isolated SW233 null session."""
import argparse
import hashlib
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

from tools.glass_bench import CAMERA_KEYS as ANGLE_KEYS
from tools.glass_bench import VIEW, Session

VIS = '/sim/sw233/visuals/'
MASS = '/fdm/jsbsim/inertia/pointmass-weight-lbs'
BRAKE = '/fdm/jsbsim/fcs/speedbrake-pos-norm'
ELEVATOR = '/fdm/jsbsim/fcs/elevator-pos-rad'
DISTANCE = VIEW+'z-offset-m'
CAMERA_KEYS = (*ANGLE_KEYS, DISTANCE)
BASE = {VIS+'livery': True, VIS+'uv-grid': False, VIS+'crew': True,
        VIS+'wings': False, MASS: 180, MASS+'[1]': 180, BRAKE: 0, ELEVATOR: 0}
# name, heading offset, pitch offset, field of view, chase distance, overrides
FRAMES = (
    ('grid-top', 140, 80, 40, 25, {VIS+'uv-grid': True}),
    ('grid-bottom', 140, -65, 40, 25, {VIS+'uv-grid': True}),
    ('paint-top', 140, 80, 40, 25, {}),
    ('paint-bottom', 140, -65, 40, 25, {}),
    ('spoilers-out', 140, 65, 40, 25, {BRAKE: 1}),
    ('spoilers-in', 140, 65, 40, 25, {BRAKE: 0}),
    ('crew-near', 120, 15, 40, 25, {}),
    ('crew-far', 120, 15, 10, 100, {}),
    ('elevator-up', 90, 5, 40, 25, {ELEVATOR: -.35}),
    ('elevator-down', 90, 5, 40, 25, {ELEVATOR: .35}),
)


def capture(output, port):
    fg = Session(port)

    def read(paths):
        values = {p: fg.get(p) for p in paths}
        if any(v is None for v in values.values()):
            raise ValueError(f'Initialize required properties before capture: {values}')
        return values

    def put(values):
        for path, value in values.items():
            fg.put(path, value)

    if fg.get('/sim/aircraft') != 'sw233' or fg.get('/sim/flight-model') != 'null':
        raise ValueError('Dedicated SW233 null-FDM session required')
    saved = read((*BASE, '/sim/menubar/visibility', '/sim/freeze/master',
                  '/orientation/heading-deg'))
    original_view = read((VIEW+'view-number',))[VIEW+'view-number']
    cameras = {original_view: read(CAMERA_KEYS)}
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    report = dict(version=fg.get('/sim/version/flightgear'),
                  aircraft_dir=fg.get('/sim/aircraft-dir'),
                  purpose='Native geometry and texture inspection; no automatic LOD visibility '
                          'or aerodynamic validation',
                  distance_note='Negative current-view z offset is a camera setting, not distance '
                                'to each drawable bounding sphere. LOD threshold is 60 m.',
                  original_view=original_view, initial_properties=saved, frames=[])
    errors = []
    try:
        put({'/sim/freeze/master': True, '/sim/menubar/visibility': False})
        fg.put(VIEW+'view-number', 1)
        if 1 not in cameras:
            cameras[1] = read(CAMERA_KEYS)
        for name, heading, pitch, fov, distance, changes in FRAMES:
            values = {**BASE, **changes, DISTANCE: -distance}
            values.update(zip(ANGLE_KEYS, (heading, pitch, fov)))
            put(values)
            time.sleep(1)
            actual = read(values)
            if actual != values:
                raise RuntimeError(f'Frame settings not applied for {name}: {actual}')
            with urlopen(fg.base+'/screenshot?type=png', timeout=30) as response:
                data = response.read()
            with Image.open(io.BytesIO(data)) as image:
                if image.format != 'PNG' or image.width < 1024 or image.height < 600:
                    raise ValueError('Native PNG of at least 1024 x 600 required')
                size = list(image.size)
                image.verify()
            filename = name+'.png'
            (output/filename).write_bytes(data)
            report['frames'].append(dict(
                image=filename, dimensions=size, sha256=hashlib.sha256(data).hexdigest(),
                settings=actual, runtime={p: fg.get(p) for p in (
                    VIEW+'view-number', VIEW+'x-offset-m', VIEW+'y-offset-m', VIEW+'z-offset-m',
                    '/orientation/heading-deg', '/position/altitude-ft', '/sim/frame-number')}))
    except Exception as exc:
        report['error'] = str(exc)
        raise
    finally:
        def restore(path, value):
            try:
                fg.put(path, value)
                if fg.get(path) != value:
                    errors.append(f'Not restored: {path}')
            except Exception as exc:
                errors.append(f'{path}: {exc}')

        for number, values in cameras.items():
            restore(VIEW+'view-number', number)
            for path, value in values.items():
                restore(path, value)
        for path, value in saved.items():
            restore(path, value)
        restore(VIEW+'view-number', original_view)
        for path, value in cameras[original_view].items():
            restore(path, value)
        report.update(saved_cameras=cameras, restored=not errors, restoration_errors=errors)
        (output/'checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        if errors:
            raise RuntimeError('Restoration incomplete: '+'; '.join(errors))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    capture(args.output, args.port)

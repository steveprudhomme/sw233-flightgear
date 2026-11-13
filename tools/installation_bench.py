"""Capture and verify a relocated package in a dedicated FlightGear ground session."""
import argparse
import json
import math
import time
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute
from tools.launch import verify


def check(package, output, port):
    verify(package)
    base = f'http://127.0.0.1:{port}'
    def get(p):
        with urlopen(base + '/json' + p, timeout=15) as response:
            return json.load(response)['value']
    def run(script):
        execute(script, port)
    loaded = Path(get('/sim/aircraft-dir')).resolve()
    if loaded != (package / 'Aircraft/SW233').resolve() or not get('/gear/gear/wow'):
        raise AssertionError('Wrong package or not on ground')
    output.mkdir(parents=True, exist_ok=False)
    paths = ['/controls/flight/elevator', '/controls/flight/elevator-trim',
             '/controls/flight/speedbrake']
    saved = {p: get(p) for p in paths}
    data = dict(loaded=str(loaded), controls=[], instruments={})
    def capture(name):
        with urlopen(base + '/screenshot?type=jpg', timeout=20) as response:
            content = response.read()
        if len(content) < 10000:
            raise AssertionError('FlightGear must have a visible rendered window')
        (output / name).write_bytes(content)
    try:
        run('sw233_load.dialog.close();')
        for p in paths:
            run(f'setprop("{p}",0);')
        time.sleep(1)
        capture('cockpit.jpg')
        for elevator, spoilers in [(1, 1), (-1, 0), (0, 0)]:
            run(f'setprop("{paths[0]}",{elevator});setprop("{paths[2]}",{spoilers});')
            time.sleep(0.5)
            angle = get('/fdm/jsbsim/fcs/elevator-pos-rad')
            brake = get('/fdm/jsbsim/fcs/speedbrake-pos-norm')
            if abs(angle-math.radians(23)*elevator) > 1e-5 or abs(brake-spoilers) > 1e-5:
                raise AssertionError((angle, brake))
            data['controls'].append(dict(command=elevator, radians=angle, speedbrake=brake))
        for prop in ['airspeed-indicator/indicated-speed-kt',
                     'altimeter/indicated-altitude-ft',
                     'vertical-speed-indicator/indicated-speed-fpm']:
            value = get('/instrumentation/' + prop)
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise AssertionError((prop, value))
            data['instruments'][prop] = value
        run('sw233_load.dialog.open();')
        time.sleep(0.5)
        capture('occupants.jpg')
        data['weight_lbs'] = get('/fdm/jsbsim/inertia/weight-lbs')
    finally:
        for p, value in saved.items():
            run(f'setprop("{p}",{float(value)});')
        run('sw233_load.dialog.close();')
    (output / 'installation.json').write_text(json.dumps(data, indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--port', type=int, default=18099)
    args = parser.parse_args()
    check(args.package.resolve(), args.output, args.port)

"""Exercise generic COM1 tuning in a dedicated SW233 null-FDM session."""
import argparse
import io
import json
import time
from pathlib import Path
from urllib.request import urlopen

from flightgear import execute
from PIL import Image


def capture(folder, port):
    base = f"http://127.0.0.1:{port}"

    def read(path):
        with urlopen(base + path, timeout=20) as r:
            return r.read()

    def get(p):
        return json.loads(read('/json' + p))['value']

    def put(p, v):
        execute(f"setprop('{p}',{json.dumps(v)});", port)

    if (get('/sim/aircraft') != 'sw233' or not get('/sim/initialized')
            or get('/sim/flight-model') != 'null'):
        raise ValueError('Dedicated initialized SW233 null-FDM session required')
    folder.mkdir(parents=True, exist_ok=False)
    freq = '/instrumentation/comm/frequencies/selected-mhz'
    protected = ['/instrumentation/comm/frequencies/standby-mhz',
                 '/instrumentation/comm[1]/frequencies/selected-mhz']
    settings = {'/sim/current-view/' + k: v for k, v in {
        'view-number': 0, 'heading-offset-deg': 0, 'pitch-offset-deg': -18,
        'field-of-view': 20, 'x-offset-m': -.141, 'y-offset-m': .5, 'z-offset-m': 1.7,
    }.items()}
    settings['/sim/menubar/visibility'] = 0
    saved = {p: get(p) for p in [*settings, freq, *protected]}
    rows = []
    try:
        for p, v in settings.items():
            put(p, v)
        cases = [
            ('fine-plus', 118.300, 1, 118.325),
            ('fine-minus', 118.325, -1, 118.300),
            ('carry', 118.975, 1, 119.000),
            ('borrow', 119.000, -1, 118.975),
            ('coarse-plus', 123.450, 40, 124.450),
            ('coarse-minus', 124.450, -40, 123.450),
            ('lower-stop', 118.000, -1, 118.000),
            ('upper-stop', 136.975, 1, 136.975),
            ('lower-coarse', 118.025, -40, 118.000),
            ('upper-coarse', 136.950, 40, 136.975),
            ('external-25', 125.125, 0, 125.125),
            ('external-833', 118.005, 1, 118.005),
            ('invalid', 117.000, 1, 117.000),
        ]
        for name, initial, delta, expected in cases:
            put(freq, initial)
            execute(f'sw233_radio.tune({delta});', port)
            time.sleep(.4)
            actual = get(freq)
            if abs(actual-expected) > 1e-7:
                raise AssertionError((name, actual, expected))
            for p in protected:
                if get(p) != saved[p]:
                    raise AssertionError(f'Unexpected modification: {p}')
            content = read('/screenshot?type=jpg')
            with Image.open(io.BytesIO(content)) as im:
                if im.width < 1024 or im.height < 600:
                    raise RuntimeError('Capture vide : restaurer FlightGear')
            (folder / (name+'.jpg')).write_bytes(content)
            rows.append(dict(case=name, initial=initial, channels=delta,
                             expected=expected, actual=actual,
                             message=get('/sim/sw233/radio/message')))
    finally:
        for p, v in saved.items():
            put(p, v)
    restored = {p: get(p) for p in saved}
    if restored != saved:
        raise AssertionError('Restoration failed')
    (folder / 'results.json').write_text(json.dumps(dict(
        version=get('/sim/version/flightgear'), aircraft_dir=get('/sim/aircraft-dir'),
        scope='Tuning/display only; no audio or network validation',
        cases=rows, saved=saved, restored=restored), indent=2), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    capture(args.folder, args.port)

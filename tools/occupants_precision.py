"""Run real Nasal functions against isolated properties without changing the aircraft."""
import argparse
import json
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute

ROOT = Path(__file__).resolve().parents[1]


def check(port):
    source = (ROOT / 'src/SW233/Nasal/occupants.nas').read_text(encoding='utf-8')
    source = source[:source.index('var dialog =')]
    source = source.replace('/sim/sw233/occupants/', '/sim/sw233/precision-test/')
    source = source.replace('/fdm/jsbsim/inertia/pointmass-weight-lbs[1]',
                            '/sim/sw233/precision-test/effective-rear')
    source = source.replace('/fdm/jsbsim/inertia/pointmass-weight-lbs',
                            '/sim/sw233/precision-test/effective-front')
    results = []
    for variant in ('before', 'after'):
        script = source.replace('%.17g', '%.2f') if variant == 'before' else source
        script += ('\nsetprop(front,200.125); setprop(rear,139.875); begin();'
                   'preset(180,180); restore();'
                   'setprop(base~"result-front",getprop(front));'
                   'setprop(base~"result-rear",getprop(rear));')
        execute(script, port)
        values = []
        for field in ('front', 'rear'):
            with urlopen(f'http://127.0.0.1:{port}/json/sim/sw233/precision-test/result-{field}',
                         timeout=10) as response:
                values.append(json.load(response)['value'])
        results.append(dict(variant=variant, values=values))
    if results[0]['values'] == [200.125, 139.875]:
        raise AssertionError('Rounding regression was not reproduced')
    if results[1]['values'] != [200.125, 139.875]:
        raise AssertionError('Exact decimal restoration failed')
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=18097)
    args = parser.parse_args()
    print(json.dumps(check(args.port), indent=2))

"""Reference-frame experiments on temporary FDM copies, never the distributed aircraft."""

import argparse
import hashlib
import json
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import jsbsim

from tools.glide import ROOT, trim_glide


def experiment(shift_in=0, arp_shift_in=0, correct_moment=False):
    tree = ET.parse(ROOT / 'src/SW233/sw233.xml')
    locations = tree.findall('.//location')
    for location in locations:
        if location.get('unit') != 'IN':
            raise ValueError('This experiment requires inch locations')
        x = location.find('x')
        x.text = str(float(x.text) + shift_in)
    arp = tree.find("metrics/location[@name='AERORP']/x")
    arp.text = str(float(arp.text) + arp_shift_in)
    if correct_moment:
        # For structural shift dx of AERORP, add -dx/12 * Fz(body)
        # to its own pitch moment, preserving the total moment at the CG.
        pitch = tree.find("aerodynamics/axis[@name='PITCH']/function")
        old = list(pitch)
        for child in old:
            pitch.remove(child)
        total = ET.SubElement(pitch, 'sum')
        total.extend(old)
        term = ET.SubElement(total, 'product')
        ET.SubElement(term, 'value').text = str(-arp_shift_in / 12)
        # Body Fz = -L*cos(alpha)-D*sin(alpha), beta=0 for these tests.
        force = ET.SubElement(term, 'sum')
        for load, trig in (('load-lift', 'cos'), ('load-drag', 'sin')):
            product = ET.SubElement(force, 'product')
            ET.SubElement(product, 'value').text = '-1'
            ET.SubElement(product, 'property').text = 'aero/sw233/' + load
            angle = ET.SubElement(product, trig)
            ET.SubElement(angle, 'property').text = 'aero/alpha-rad'
    with tempfile.TemporaryDirectory(prefix='sw233-frames-') as temporary:
        tree.write(Path(temporary) / 'sw233.xml', encoding='utf-8')
        fdm = jsbsim.FGFDMExec(None)
        fdm.set_debug_level(0)
        fdm.set_aircraft_path(temporary)
        if not fdm.load_model('sw233', False):
            raise RuntimeError('Temporary model did not load')
        fdm.set_dt(1 / 120)
        result = trim_glide(fdm)
        result.update(shift_in=shift_in, arp_shift_in=arp_shift_in,
                      corrected_moment=correct_moment, translated_locations=len(locations))
        for key in ('inertia/cg-x-in', 'metrics/aero-rp-x-in', 'metrics/visualrefpoint-x-in',
                    'moments/m-aero-lbsft', 'aero/sw233/load-pitch'):
            result[key] = fdm[key]
        result['arm_in'] = fdm['metrics/aero-rp-x-in'] - fdm['inertia/cg-x-in']
        for _ in range(7200):
            if not fdm.run():
                raise RuntimeError('Simulation stopped')
        result['final_speed_kts'] = fdm['velocities/vc-kts']
        result['final_altitude_ft'] = fdm['position/h-sl-ft']
    return result


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    args.folder.mkdir(parents=True, exist_ok=False)
    results = [experiment(), experiment(shift_in=10), experiment(arp_shift_in=-1),
               experiment(arp_shift_in=-1, correct_moment=True)]
    data = {'jsbsim_version': jsbsim.__version__,
            'fdm_sha256': hashlib.sha256((ROOT/'src/SW233/sw233.xml').read_bytes()).hexdigest(),
            'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': '50 kt CAS; 5000 ft; beta=0; no wind; temporary XML only',
            'results': results}
    (args.folder/'frames.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    for r in results:
        print(r['shift_in'], r['arp_shift_in'], r['corrected_moment'],
              r['elevator_norm'], r['arm_in'], r['final_altitude_ft'])


if __name__ == '__main__':
    run()

"""Ground-development bench; no claim of manufacturer handling fidelity."""
import argparse
import json
import math
from pathlib import Path

import jsbsim

from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('position/h-agl-ft', 'attitude/theta-deg', 'attitude/phi-deg',
          'velocities/vg-fps', 'velocities/p-rad_sec', 'velocities/q-rad_sec',
          'velocities/r-rad_sec', 'inertia/cg-x-in', 'inertia/cg-y-in',
          'inertia/cg-z-in', 'gear/unit/compression-ft')


def load(directory):
    fdm = jsbsim.FGFDMExec(None)
    fdm.set_debug_level(0)
    fdm.set_aircraft_path(str(directory))
    if not fdm.load_model('sw233', False):
        raise RuntimeError('Cannot load ground-test aircraft')
    fdm.set_dt(1/120)
    return fdm


def sample(fdm):
    values = {p: fdm[p] for p in FIELDS}
    if not all(math.isfinite(v) for v in values.values()):
        raise RuntimeError('Non-finite ground state')
    return values


def run_case(directory, roll=1.0, speed=0.0, seconds=60):
    fdm = load(directory)
    fdm['ic/h-agl-ft'] = 4.2
    fdm['ic/phi-deg'] = roll
    fdm['ic/vc-kts'] = 0
    if not fdm.run_ic():
        raise RuntimeError('Initial ground state rejected')
    for _ in range(7200):
        if not fdm.run():
            raise RuntimeError('Settling failed')
    settled = sample(fdm)
    if speed:
        fdm['ic/h-agl-ft'] = settled['position/h-agl-ft']
        fdm['ic/theta-deg'] = settled['attitude/theta-deg']
        fdm['ic/phi-deg'] = settled['attitude/phi-deg']
        fdm['ic/vc-kts'] = speed
        fdm['ic/gamma-deg'] = 0
        if not fdm.run_ic():
            raise RuntimeError('Rolling state rejected')
    history = [sample(fdm)]
    distance = 0.0
    for i in range(round(seconds*120)):
        if not fdm.run():
            raise RuntimeError('Ground run stopped')
        distance += fdm['velocities/vg-fps']/120*.3048
        if i % 120 == 119:
            history.append(sample(fdm))
    return dict(initial_roll_deg=roll, initial_speed_kts=speed, duration_s=seconds,
                distance_m=distance, settled=settled, samples=history,
                final=history[-1])


def mesh_clearance(state, mesh):
    """Flat ground, origin at VRP=0; JSBSim AGL is at CG, all lengths metres."""
    _, objects = read_mesh(mesh)
    cg = [state[f'inertia/cg-{axis}-in']*.0254 for axis in 'xyz']
    theta, phi = [math.radians(state[p]) for p in
                  ('attitude/theta-deg', 'attitude/phi-deg')]
    def height(p):
        x, y, z = [p[i]-cg[i] for i in range(3)]
        return (state['position/h-agl-ft']*.3048-x*math.sin(theta)
                -y*math.sin(phi)*math.cos(theta)+z*math.cos(phi)*math.cos(theta))
    return {name: min(height(p) for _, face in faces for p in face)
            for name, faces in objects.items() if faces}


def audit(directory, mesh):
    cases = [run_case(directory, roll, speed) for roll, speed in
             ((-1, 0), (1, 0), (-1, 5), (1, 5))]
    for case in cases:
        case['mesh_clearance_m'] = mesh_clearance(case['final'], mesh)
    return dict(jsbsim_version=jsbsim.__version__, dt_s=1/120,
                scope='Flat ground, still air, 970 lb; no tow force or pilot input',
                cases=cases)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--aircraft', type=Path, default=ROOT/'src/SW233')
    parser.add_argument('--mesh', type=Path, default=ROOT/'src/SW233/Models/sw233.ac')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(audit(args.aircraft, args.mesh), indent=2)+'\n',
                           encoding='utf-8')

"""Audit visual dimensions against identified maintenance manual references."""
import argparse
import json
import xml.etree.ElementTree as ET
from math import cos, radians, sin
from pathlib import Path

from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]
INCH = 0.0254
STATIONS = {"wing_le": 66.34, "main": 88.75, "tail": 285.0}


def vertical_envelope(points, pitch=0.0, roll=0.0):
    """Rotated point envelope, not ground clearance or a contact simulation.

    Construction axes: aft, right, up. Positive pitch raises the nose;
    positive roll lowers the right wing. Translation cancels in the extent.
    """
    pitch, roll = radians(pitch), radians(roll)
    values = [-x*sin(pitch)-y*sin(roll)*cos(pitch)+z*cos(roll)*cos(pitch)
              for x, y, z in points]
    return max(values)-min(values)


def audit(mesh, pitch=0.0, roll=0.0):
    _, objects = read_mesh(mesh)

    def points(names):
        return [p for name in names for _, face in objects[name] for p in face]

    wing_le = min(p[0] for p in points(('aile-1', 'aile1')))
    wheels = {}
    for label, name in (("main", "roue"), ("tail", "roulette")):
        vertices = points((name,))
        center = (min(p[0] for p in vertices)+max(p[0] for p in vertices))/2
        expected = (STATIONS[label]-STATIONS['wing_le'])*INCH
        wheels[label] = dict(x=center, distance_from_wing_le=center-wing_le,
                             manual_distance=expected, residual=center-wing_le-expected)
    config = ET.parse(ROOT/'src/SW233/sw233.xml')
    contacts = {}
    for name in ('main-wheel', 'tail'):
        node = config.find(f"ground_reactions/contact[@name='{name}']/location")
        if node.attrib.get('unit') != 'IN':
            raise ValueError('Expected inch contact coordinates')
        contacts[name] = float(node.findtext('x'))*INCH
    vertices = points(objects.keys())
    manual_spacing = (STATIONS['tail']-STATIONS['main'])*INCH
    return dict(manual_pdf_pages=[9, 20, 149, 150, 222],
                scope='A12 example serial 369; model wing leading edge retained',
                wing_le=wing_le, wheels=wheels,
                manual_wheel_spacing=manual_spacing,
                visual_wheel_spacing=wheels['tail']['x']-wheels['main']['x'],
                fdm_contact_spacing=contacts['tail']-contacts['main-wheel'],
                level_visual_height=vertical_envelope(vertices),
                attitude=dict(pitch=pitch, roll=roll),
                rotated_visual_height=vertical_envelope(vertices, pitch, roll),
                manual_height=(9*12+3.5)*INCH,
                height_status='Unresolved: attitude and measurement endpoints unspecified')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh', type=Path, default=ROOT/'src/SW233/Models/sw233.ac')
    parser.add_argument('--pitch', type=float, default=0)
    parser.add_argument('--roll', type=float, default=0)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    text = json.dumps(audit(args.mesh, args.pitch, args.roll), indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text)

"""Crew visibility follows existing mass properties; generated faces remain valid."""
import math
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.crew import finish_crew


def condition(node, properties):
    if node.tag in {'condition', 'and'}:
        return all(condition(child, properties) for child in node)
    if node.tag == 'not':
        return not condition(node[0], properties)
    if node.tag == 'property':
        return bool(properties[node.text])
    if node.tag == 'greater-than':
        return properties[node.findtext('property')] > float(node.findtext('value'))
    if node.tag == 'equals':
        return properties[node.findtext('property')] == float(node.findtext('value'))
    raise AssertionError(f'Unexpected condition {node.tag}')


class CrewVisualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix='SW233 crew test ')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.models = Path(cls.temp.name)
        finish_crew(cls.models)
        cls.tree = ET.parse(cls.models / 'crew.xml')
        cls.mesh = (cls.models / 'crew.ac').read_text(encoding='utf-8')

    def visible(self, front=180, rear=180, enabled=True, wings=False, view=1):
        properties = {
            '/fdm/jsbsim/inertia/pointmass-weight-lbs': front,
            '/fdm/jsbsim/inertia/pointmass-weight-lbs[1]': rear,
            '/sim/sw233/visuals/crew': enabled,
            '/sim/sw233/visuals/wings': wings,
            '/sim/current-view/view-number': view,
        }
        return {obj.text for anim in self.tree.findall('animation')
                if condition(anim.find('condition'), properties)
                for obj in anim.findall('object-name')}

    def test_zero_mass_hides_only_corresponding_occupant(self):
        for front, rear in ((0, 0), (180, 0), (0, 180), (180, 180)):
            with self.subTest(front=front, rear=rear):
                visible = self.visible(front, rear)
                self.assertEqual(any(n.startswith('front-') for n in visible), front > 0)
                self.assertEqual(any(n.startswith('rear-') for n in visible), rear > 0)
        self.assertFalse(self.visible(enabled=False, wings=True))

    def test_front_head_hidden_in_cockpit_and_wings_opt_in(self):
        outside = self.visible()
        cockpit = self.visible(view=0)
        hidden = outside - cockpit
        self.assertTrue(hidden)
        self.assertTrue(all(name.startswith('front-') for name in hidden))
        self.assertTrue(any('head' in name for name in hidden))
        self.assertTrue(any('neck' in name for name in hidden))
        self.assertTrue(any(name.startswith('front-') for name in cockpit))
        wings = self.visible(wings=True) - outside
        self.assertEqual(len(wings), 2)
        self.assertTrue(all('optional-fictional-wings' in name for name in wings))

    def test_all_objects_selected_once_without_physical_writes(self):
        names = re.findall(r'^name "([^"]+)"', self.mesh, re.M)
        selected = [n.text for n in self.tree.findall('animation/object-name')]
        self.assertEqual(len(selected), len(set(selected)))
        self.assertEqual(set(selected), set(names))
        self.assertTrue(all(a.findtext('type') == 'select'
                            for a in self.tree.findall('animation')))
        self.assertFalse(self.tree.findall('.//nasal'))
        self.assertFalse(self.tree.findall('.//binding'))
        self.assertFalse(self.tree.findall('.//script'))
        # The only physical property references are read-only selection predicates.
        mass_refs = [n for n in self.tree.findall('.//property')
                     if 'pointmass' in (n.text or '')]
        predicates = self.tree.findall('.//greater-than/property')
        self.assertTrue(mass_refs)
        self.assertTrue(all(n in predicates for n in mass_refs))

    def test_serialized_geometry_has_finite_non_degenerate_triangles(self):
        count = 0
        for part in self.mesh.split('OBJECT poly')[1:]:
            name = re.search(r'name "([^"]+)"', part).group(1)
            rows = part.split('numvert ')[1].splitlines()
            vertices = [tuple(map(float, row.split())) for row in rows[1:1 + int(rows[0])]]
            self.assertTrue(all(math.isfinite(v) for point in vertices for v in point), name)
            for surface in part.split('SURF ')[1:]:
                rows = surface.split('refs ')[1].splitlines()
                self.assertEqual(int(rows[0]), 3, name)
                indices = [int(row.split()[0]) for row in rows[1:4]]
                self.assertTrue(all(0 <= i < len(vertices) for i in indices), name)
                a, b, c = [vertices[i] for i in indices]
                u = [b[i] - a[i] for i in range(3)]
                v = [c[i] - a[i] for i in range(3)]
                cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2],
                         u[0]*v[1]-u[1]*v[0])
                self.assertGreater(sum(x*x for x in cross), 1e-22, name)
                count += 1
        self.assertGreater(count, 1000)


if __name__ == '__main__':
    unittest.main()

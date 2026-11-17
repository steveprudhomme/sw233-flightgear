"""Validate enclosure seams and animation geometry."""
import unittest
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]


class EnclosureTests(unittest.TestCase):
    def test_outer_shell_has_no_unpaired_edges(self):
        _, objects = read_mesh(ROOT/'src/SW233/Models/sw233.ac')
        edges = Counter()
        for name in ('fuselage', 'verriere', 'raccord-arriere',
                     'pare-brise', 'vitrage-droit', 'vitrage-gauche'):
            for _, polygon in objects[name]:
                for a, b in zip(polygon, polygon[1:]+polygon[:1]):
                    edges[tuple(sorted((a, b)))] += 1
        self.assertTrue(edges)
        self.assertEqual(Counter(edges.values()), {2: len(edges)})

    def test_animation_parts_exist_and_cabin_has_no_deck(self):
        _, objects = read_mesh(ROOT/'src/SW233/Models/sw233.ac')
        config = ET.parse(ROOT/'src/SW233/Models/sw233-model.xml')
        names = set(objects) | {node.findtext('name') for node in config.findall('text')}
        for node in config.findall('.//object-name'):
            self.assertIn(node.text, names)
        for _, polygon in objects['fuselage']:
            x = sum(p[0] for p in polygon)/len(polygon)
            if .50 < x < 3.16:
                high = [p for p in polygon if p[2] >= .05]
                self.assertFalse(any(p[1] < -.2 for p in high) and
                                 any(p[1] > .2 for p in high))

    def test_panels_have_area_and_leaning_boundary(self):
        _, objects = read_mesh(ROOT/'src/SW233/Models/sw233.ac')
        for name in ('pare-brise', 'vitrage-gauche', 'vitrage-droit'):
            self.assertTrue(objects[name])
            for _, v in objects[name]:
                a = [v[1][i]-v[0][i] for i in range(3)]
                b = [v[2][i]-v[0][i] for i in range(3)]
                cross = [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
                         a[0]*b[1]-a[1]*b[0]]
                self.assertGreater(sum(c*c for c in cross), 1e-12)
        points = [p for _, v in objects['pare-brise'] for p in v]
        self.assertAlmostEqual(max(p[0] for p in points), 1.69)
        self.assertIn('contour-porte-1', objects)
        self.assertIn('contour-porte1', objects)

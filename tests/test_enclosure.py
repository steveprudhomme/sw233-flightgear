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
        for name in ('fuselage', 'verriere', 'raccord-arriere'):
            for _, polygon in objects[name]:
                for a, b in zip(polygon, polygon[1:]+polygon[:1]):
                    edges[tuple(sorted((a, b)))] += 1
        self.assertTrue(edges)
        self.assertEqual(Counter(edges.values()), {2: len(edges)})

    def test_animation_parts_exist_and_cabin_has_no_deck(self):
        _, objects = read_mesh(ROOT/'src/SW233/Models/sw233.ac')
        config = ET.parse(ROOT/'src/SW233/Models/sw233-model.xml')
        for node in config.findall('.//object-name'):
            self.assertIn(node.text, objects)
        for _, polygon in objects['fuselage']:
            x = sum(p[0] for p in polygon)/len(polygon)
            if .50 < x < 3.16:
                high = [p for p in polygon if p[2] >= .05]
                self.assertFalse(any(p[1] < -.2 for p in high) and
                                 any(p[1] > .2 for p in high))

"""Check the animation binding and its geometry assumptions without FlightGear."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from tools.tire_bench import mesh_offset

ROOT = Path(__file__).resolve().parents[1]


class TireTests(unittest.TestCase):
    def test_level_wheel_follows_compression(self):
        self.assertAlmostEqual(mesh_offset(.04, 0, 0), .04*.3048, places=9)
        self.assertAlmostEqual(mesh_offset(0, 0, 0), 0, places=9)

    def test_both_roll_directions_raise_the_lower_edge(self):
        for pitch in [-15, 0, 15]:
            left = mesh_offset(.04, pitch, -13)
            right = mesh_offset(.04, pitch, 13)
            self.assertAlmostEqual(left, right, places=9)
            self.assertGreater(left, .04*.3048)

    def test_only_main_wheel_translates_up(self):
        root = ET.parse(ROOT/'src/SW233/Models/sw233-model.xml')
        nodes = [n for n in root.findall('animation')
                 if n.findtext('property') == '/sim/sw233/gear/main-offset-m']
        self.assertEqual(len(nodes), 1)
        node = nodes[0]
        self.assertEqual(node.findtext('type'), 'translate')
        self.assertEqual([n.text for n in node.findall('object-name')], ['roue'])
        self.assertEqual([float(node.findtext('axis/'+a)) for a in 'xyz'], [0, 0, 1])
        config = ET.parse(ROOT/'src/SW233/sw233-set.xml')
        self.assertEqual(config.findtext('nasal/sw233_gear/file'), 'Nasal/gear.nas')

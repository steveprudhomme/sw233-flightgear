"""Contact geometry and settled/rolling behaviour on flat ground."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from tools.ground_bench import mesh_clearance, run_case
from tools.parts_atlas import bounds, read_mesh

ROOT = Path(__file__).resolve().parents[1]


class GroundContactTests(unittest.TestCase):
    def test_wheel_contacts_match_unloaded_mesh_bottoms(self):
        _, objects = read_mesh(ROOT/'src/SW233/Models/sw233.ac')
        xml = ET.parse(ROOT/'src/SW233/sw233.xml')
        for contact, name in [('main-wheel', 'roue'), ('tail', 'roulette')]:
            point = xml.find(f"ground_reactions/contact[@name='{contact}']/location")
            box = bounds(objects[name])
            self.assertAlmostEqual(float(point.findtext('x'))*.0254,
                                   sum(box[0])/2, places=5)
            self.assertAlmostEqual(float(point.findtext('z'))*.0254, box[2][0], places=5)

    def test_settles_on_either_wing_without_floating_or_large_penetration(self):
        for roll in [-1, 1]:
            with self.subTest(roll=roll):
                result = run_case(ROOT/'src/SW233', roll, seconds=15)
                final = result['final']
                self.assertLess(final['velocities/vg-fps'], .01)
                self.assertLess(abs(final['velocities/p-rad_sec']), .001)
                self.assertLess(abs(final['velocities/q-rad_sec']), .001)
                self.assertTrue(-9 < final['attitude/theta-deg'] < -5)
                self.assertTrue(10 < abs(final['attitude/phi-deg']) < 15)
                clearances = mesh_clearance(final, ROOT/'src/SW233/Models/sw233.ac')
                self.assertGreater(min(clearances.values()), -.04)
                self.assertLess(abs(clearances['roue']), .04)
                self.assertGreater(clearances['fuselage'], -.005)

    def test_five_knot_impulse_stops_and_remains_stable(self):
        result = run_case(ROOT/'src/SW233', -1, 5, seconds=30)
        self.assertGreater(result['distance_m'], .5)
        self.assertLess(result['distance_m'], 10)
        self.assertLess(result['final']['velocities/vg-fps'], .01)
        for state in result['samples']:
            self.assertLess(abs(state['attitude/phi-deg']), 20)
            self.assertTrue(0 < state['position/h-agl-ft'] < 5)

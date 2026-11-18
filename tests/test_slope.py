import math
import unittest

from tools.slope_bench import mesh_lift


class SlopeTests(unittest.TestCase):
    def test_level(self):
        self.assertAlmostEqual(mesh_lift(0.03, 0, 0), 0.03, places=6)

    def test_lateral_width(self):
        for angle in [-25, 25]:
            slope = math.tan(math.radians(angle))
            self.assertAlmostEqual(mesh_lift(0.03, 0, slope), 0.03 + 0.075 * abs(slope), places=6)

    def test_symmetry(self):
        for sx, sy in [(0.4663, 0), (0, 0.4663), (0.364, 0.364)]:
            self.assertAlmostEqual(mesh_lift(0.03, sx, sy), mesh_lift(0.03, -sx, -sy), delta=1e-5)

    def test_no_downward_extension(self):
        self.assertEqual(mesh_lift(-0.4, 0.364, 0.364), 0)

    def test_longitudinal_polygon(self):
        slope = math.tan(math.radians(25))
        # 20-sided wheel: the supporting vertex is at 288 degrees.
        expected = (
            0.03
            + 0.245 * (slope * math.cos(math.radians(288)) - math.sin(math.radians(288)))
            - 0.245
        )
        self.assertAlmostEqual(mesh_lift(0.03, slope, 0), expected, places=5)

import unittest

from tools.dimension_audit import ROOT, audit, vertical_envelope


class DimensionTests(unittest.TestCase):
    def test_wheels_match_manual_distances_from_wing(self):
        result = audit(ROOT/'src/SW233/Models/sw233.ac')
        for wheel in result['wheels'].values():
            self.assertLess(abs(wheel['residual']), 0.00001)
        self.assertAlmostEqual(result['visual_wheel_spacing'], 4.98475, places=5)

    def test_height_uses_attitude_and_ignores_translation(self):
        points = [(0, -2, 0), (0, 2, 0), (0, 0, 1)]
        self.assertEqual(vertical_envelope(points), 1)
        self.assertAlmostEqual(vertical_envelope(points, roll=90), 4)
        shifted = [(x+11, y-5, z+3) for x, y, z in points]
        self.assertAlmostEqual(vertical_envelope(points, 12, -23),
                               vertical_envelope(shifted, 12, -23))

    def test_unresolved_height_is_not_reported_as_conformant(self):
        result = audit(ROOT/'src/SW233/Models/sw233.ac')
        self.assertAlmostEqual(result['manual_height'], 2.8321)
        self.assertIn('Unresolved', result['height_status'])

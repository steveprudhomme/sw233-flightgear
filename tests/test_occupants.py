"""Changing both occupant masses must propagate into the physical CG."""
import unittest

from tools.glide import aircraft


class OccupantTests(unittest.TestCase):
    def test_independent_masses_and_restoration(self):
        fdm = aircraft()
        for front, rear in [(180, 180), (180, 0), (220, 140), (100, 200), (0, 0), (180, 180)]:
            with self.subTest(front=front, rear=rear):
                fdm['inertia/pointmass-weight-lbs'] = front
                fdm['inertia/pointmass-weight-lbs[1]'] = rear
                self.assertTrue(fdm.run_ic())
                total = 610 + front + rear
                self.assertAlmostEqual(fdm['inertia/weight-lbs'], total, places=6)
                self.assertAlmostEqual(fdm['inertia/cg-x-in'],
                                       (610 * 103.2 + front * 43 + rear * 85) / total, places=6)
                self.assertAlmostEqual(fdm['inertia/cg-z-in'],
                                       (-610 * 6.4 + (front + rear) * 4) / total, places=6)

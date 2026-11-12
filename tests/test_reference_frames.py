"""Coordinate invariance and aerodynamic reference transport regression tests."""

import unittest

from tools.reference_frames import experiment


class ReferenceFrameTests(unittest.TestCase):
    def test_common_translation_preserves_dynamics(self):
        base, translated = experiment(), experiment(shift_in=10)
        self.assertAlmostEqual(translated['inertia/cg-x-in'] - base['inertia/cg-x-in'], 10)
        for key in ('arm_in', 'elevator_norm', 'gamma_deg', 'final_altitude_ft'):
            self.assertAlmostEqual(base[key], translated[key], places=8)

    def test_arp_change_requires_moment_transport(self):
        base = experiment()
        moved = experiment(arp_shift_in=-1)
        corrected = experiment(arp_shift_in=-1, correct_moment=True)
        self.assertGreater(abs(moved['elevator_norm'] - base['elevator_norm']), 0.01)
        self.assertAlmostEqual(corrected['elevator_norm'], base['elevator_norm'], places=8)
        self.assertAlmostEqual(corrected['gamma_deg'], base['gamma_deg'], places=8)
        self.assertLess(abs(corrected['final_altitude_ft'] - base['final_altitude_ft']), 0.001)

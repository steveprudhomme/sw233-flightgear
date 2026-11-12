"""Check independent moments and sensitivity, not real-aircraft certification."""

import unittest

from tools.balance import pitch_terms, prepare, source_balance
from tools.glide import trim_glide


class BalanceTests(unittest.TestCase):
    def test_seat_transfer_preserves_weight_and_moves_cg(self):
        w1, c1 = source_balance(220, 140)
        w2, c2 = source_balance(140, 220)
        self.assertEqual(w1, w2)
        self.assertAlmostEqual(c2[0] - c1[0], 80 * (85 - 43) / 970)
        for front, rear in ((180, 0), (220, 140), (140, 220)):
            fdm = prepare(front, rear)
            weight, cg = source_balance(front, rear)
            self.assertAlmostEqual(fdm['inertia/weight-lbs'], weight)
            self.assertAlmostEqual(fdm['inertia/cg-x-in'], cg[0])

    def test_pitch_transport_closes_at_two_loadings(self):
        for front, rear in ((180, 180), (140, 220)):
            fdm = prepare(front, rear)
            trim_glide(fdm)
            terms = pitch_terms(fdm)
            self.assertLess(terms['transport_pitch_lbsft'], 0)
            self.assertGreater(terms['intrinsic_pitch_lbsft'], 0)
            self.assertLess(abs(terms['total_aero_pitch_lbsft']), 1e-5)

    def test_invalid_weights_are_rejected(self):
        for weight in (-1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                source_balance(weight, 180)

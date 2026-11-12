"""Elevator limits, trim saturation and unchanged aerodynamic equilibrium."""

import math
import unittest
import xml.etree.ElementTree as ET

from tools.glide import ROOT, aircraft, trim_glide


class ElevatorTests(unittest.TestCase):
    def test_effective_travel_and_trim_saturation(self):
        for stick, trim, expected in ((-1, 0, -23), (0, 0, 0), (1, 0, 23),
                                      (-5, 0, -23), (5, 0, 23), (0.8, 0.8, 23),
                                      (-0.8, -0.8, -23), (0.5, -0.5, 0)):
            with self.subTest(stick=stick, trim=trim):
                fdm = aircraft()
                fdm['ic/h-sl-ft'] = 5000
                fdm['ic/vc-kts'] = 50
                fdm['fcs/elevator-cmd-norm'] = stick
                fdm['fcs/pitch-trim-cmd-norm'] = trim
                self.assertTrue(fdm.run_ic())
                self.assertAlmostEqual(
                    math.degrees(fdm['fcs/elevator-pos-rad']), expected, places=8)

    def test_same_physical_trim_and_animation_conversion(self):
        fdm = aircraft()
        result = trim_glide(fdm)
        self.assertAlmostEqual(math.degrees(fdm['fcs/elevator-pos-rad']), -16.4181768145, places=6)
        self.assertAlmostEqual(result['gamma_deg'], -4.685139003, places=6)
        wrapper = ET.parse(ROOT / 'src/SW233/Models/sw233-model.xml')
        for side in (-1, 1):
            node = next(a for a in wrapper.findall('animation')
                        if a.findtext('object-name') == f'profondeur{side}')
            self.assertEqual(node.findtext('property'), 'fdm/jsbsim/fcs/elevator-pos-rad')
            self.assertAlmostEqual(float(node.findtext('factor')) * math.radians(23), 23)
            self.assertEqual(node.findtext('axis/y'), '1')

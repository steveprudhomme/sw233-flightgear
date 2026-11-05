"""Verify the yarn follows airflow and the pitot does not move with it."""

import math
import unittest
import xml.etree.ElementTree as ET

from tools.glide import ROOT, aircraft


class YarnTests(unittest.TestCase):
    def test_yarn_streams_downwind(self):
        animations = ET.parse(ROOT / "src/SW233/Models/sw233-model.xml").findall("animation")
        self.assertFalse(any(a.findtext("object-name") == "tube-pitot" for a in animations))
        yarn = next(a for a in animations if a.findtext("object-name") == "fil-de-laine")
        self.assertEqual([float(yarn.findtext(f"axis/{k}")) for k in "xyz"], [0, 0, 1])
        fdm = aircraft()
        prop = yarn.findtext("property").removeprefix("fdm/jsbsim/")
        self.assertTrue(any(p.split()[0] == prop for p in fdm.get_property_catalog()))
        fdm["ic/vc-kts"] = 50
        fdm["ic/h-sl-ft"] = 5000
        for beta in (-8, 0, 8):
            fdm["ic/beta-deg"] = beta
            self.assertTrue(fdm.run_ic())
            angle = math.radians(fdm[prop] * float(yarn.findtext("factor")))
            self.assertAlmostEqual(math.sin(angle), -math.sin(math.radians(beta)))

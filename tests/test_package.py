"""Verify packaging cannot overwrite an existing installation."""

import shutil
import unittest
import xml.etree.ElementTree as ET
from uuid import uuid4

from tools.package import ROOT, package


class PackageTests(unittest.TestCase):
    def test_animated_panel_and_checklists_resolve(self):
        aircraft = ROOT / "src" / "SW233"
        config = ET.parse(aircraft / "sw233-set.xml")
        wrapper = ROOT / "src" / config.findtext("sim/model/path").removeprefix("Aircraft/")
        model = ET.parse(wrapper)
        mesh = (wrapper.parent / model.findtext("path")).read_text()
        animations = model.findall("animation")
        self.assertEqual({a.findtext("object-name") for a in animations}, {
            "alt-centaines", "alt-milliers", "vitesse-mph", "vario", "fil-de-laine",
            "aerofrein-1", "aerofrein1", "poignee-frein", "compas-rose",
        })
        for animation in animations:
            self.assertIn(f'name "{animation.findtext("object-name")}"', mesh)
            self.assertIsNotNone(animation.findtext("property"))
        lists = ET.parse(aircraft / config.find("sim/checklists").attrib["include"])
        self.assertEqual(len(lists.findall("checklist")), 4)
        for item in lists.findall("checklist/item"):
            self.assertTrue(item.findtext("name") and item.findtext("value"))

    def test_package_contains_resolvable_model_and_rejects_overwrite(self):
        scratch = ROOT / "build" / "test-scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        output = scratch / uuid4().hex
        output.mkdir()
        try:
            aircraft = package(output)
            config = ET.parse(aircraft / "sw233-set.xml").getroot()
            self.assertTrue((output / config.findtext("sim/model/path")).is_file())
            self.assertTrue((aircraft / (config.findtext("sim/aero") + ".xml")).is_file())
            with self.assertRaises(FileExistsError):
                package(output)
        finally:
            if output.resolve().parent == scratch.resolve():
                shutil.rmtree(output)

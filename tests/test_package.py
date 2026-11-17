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
            "aerofrein-1", "aerofrein1", "poignee-frein", "compas-rose", "alt-calage",
            "profondeur-1", "profondeur1", "alt-pression", "radio-frequence",
            "radio-bouton-gauche", "radio-bouton-droit",
        })
        texts = {node.findtext("name"): node for node in model.findall("text")}
        self.assertEqual(set(texts), {"alt-pression", "alt-unite", "radio-frequence"})
        for node in texts.values():
            if node.findtext("type") == "number-value":
                self.assertTrue(node.findtext("property"))
                self.assertTrue(node.findtext("format"))
            else:
                self.assertTrue(node.findtext("text"))
        for animation in animations:
            for node in animation.findall("object-name"):
                if node.text not in texts:
                    self.assertIn(f'name "{node.text}"', mesh)
            kind = animation.findtext("type")
            self.assertIn(kind, {"rotate", "knob", "material", "pick"})
            if kind in {"rotate", "knob"}:
                self.assertTrue(animation.findtext("property"))
            elif kind == "pick":
                actions = animation.findall("action")
                self.assertTrue(actions)
                for action in actions:
                    self.assertEqual(action.findtext("binding/command"), "nasal")
                    self.assertTrue(action.findtext("binding/script"))
            else:
                self.assertIsNotNone(animation.find("diffuse"))
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

"""Verify packaging cannot overwrite an existing installation."""

import json
import shutil
import unittest
import xml.etree.ElementTree as ET
from uuid import uuid4

from tools.package import ROOT, package
from tools.versioning import project_version, validate


class PackageTests(unittest.TestCase):
    def test_semver_rejects_ambiguous_versions(self):
        for value in ("0.1.0-alpha.1", "1.2.3", "1.2.3+001", "1.2.3-0"):
            self.assertEqual(validate(value), value)
        for value in ("v1.2.3", "01.2.3", "1.2", "1.2.3-alpha.01", "1.2.3-"):
            with self.assertRaises(ValueError):
                validate(value)
        self.assertEqual(project_version(), (ROOT / "VERSION").read_text().strip())

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
            "radio-bouton-gauche", "radio-bouton-droit", "plaquettes-fr", "plaquettes-en",
            "fuselage",
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
            self.assertIn(kind, {"rotate", "knob", "material", "pick", "select"})
            if kind in {"rotate", "knob"}:
                self.assertTrue(animation.findtext("property"))
            elif kind == "pick":
                actions = animation.findall("action")
                self.assertTrue(actions)
                for action in actions:
                    self.assertEqual(action.findtext("binding/command"), "nasal")
                    self.assertTrue(action.findtext("binding/script"))
            elif kind == "select" and animation.findtext("object-name") == "fuselage":
                self.assertEqual({p.text for p in animation.findall("condition/and/not/property")},
                                 {"/sim/sw233/visuals/livery", "/sim/sw233/visuals/uv-grid"})
                self.assertEqual({n.text for n in animation.findall("object-name")}, {
                    "fuselage", "aile-1", "aile1", "aerofrein-1", "aerofrein1",
                    "empennage-1", "empennage1", "profondeur-1", "profondeur1", "derive"})
            elif kind == "select":
                self.assertEqual(animation.findtext("condition/equals/property"),
                                 "sim/sw233/language")
                self.assertIn(animation.findtext("condition/equals/value"), {"fr", "en"})
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
            self.assertEqual((output / "VERSION").read_text().strip(), project_version())
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["project_version"], project_version())
            config = ET.parse(aircraft / "sw233-set.xml").getroot()
            self.assertTrue((output / config.findtext("sim/model/path")).is_file())
            self.assertTrue((aircraft / (config.findtext("sim/aero") + ".xml")).is_file())
            with self.assertRaises(FileExistsError):
                package(output)
        finally:
            if output.resolve().parent == scratch.resolve():
                shutil.rmtree(output)

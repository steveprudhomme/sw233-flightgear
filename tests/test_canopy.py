"""Canopy grouping, pivot, rear roof and public controls."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]


class CanopyTests(unittest.TestCase):
    def test_only_front_canopy_moves(self):
        _, objects = read_mesh(ROOT / "src/SW233/Models/sw233.ac")
        model = ET.parse(ROOT / "src/SW233/Models/sw233-model.xml")
        animations = [a for a in model.findall("animation")
                      if a.findtext("property") == "/sim/sw233/canopy/position"]
        self.assertEqual(len(animations), 1)
        animation = animations[0]
        names = {n.text for n in animation.findall("object-name")}
        self.assertEqual(names, {"pare-brise", "cadre-mobile", "joint-mobile",
                                 "vis-mobiles", "poignee-verriere"})
        for name in names:
            points = [p for _, face in objects[name] for p in face]
            self.assertLess(max(p[0] for p in points), 1.72)
        self.assertLess(float(animation.findtext("center/y-m")), 0)
        handle = [p for _, face in objects["poignee-verriere"] for p in face]
        self.assertGreater(min(p[1] for p in handle), 0.4)

    def test_rear_glazing_is_between_wings(self):
        _, objects = read_mesh(ROOT / "src/SW233/Models/sw233.ac")
        roof = [p for _, face in objects["verriere"] for p in face if p[0] > 2.13]
        self.assertTrue(roof)
        for name in ("aile-1", "aile1"):
            points = [p for _, face in objects[name] for p in face]
            self.assertGreaterEqual(min(abs(p[1]) for p in points), 0.43999)
        self.assertLess(max(abs(p[1]) for p in roof), 0.44)

    def test_menu_and_handle_share_controller(self):
        model = ET.parse(ROOT / "src/SW233/Models/sw233-model.xml")
        handle = [a for a in model.findall("animation") if a.findtext("type") == "pick"
                  and a.findtext("object-name") == "poignee-verriere"]
        self.assertEqual(handle[0].findtext("action/binding/script"), "sw233_canopy.toggle();")
        dialog = ET.parse(ROOT / "src/SW233/gui/dialogs/canopy.xml")
        scripts = {n.text for n in dialog.findall(".//binding/script")}
        self.assertEqual(scripts, {"sw233_canopy.request(1);", "sw233_canopy.request(0);"})

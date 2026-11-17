"""Preserve source-attested mnemonic order across translated UI resources."""

import re
import unittest
import xml.etree.ElementTree as ET

from tools.package import ROOT


class ChecklistLanguagesTests(unittest.TestCase):
    def test_mnemonic_order_and_placard_parity(self):
        for filename in ("sw233.xml", "sw233-en.xml"):
            root = ET.parse(ROOT / "src/SW233/Checklists" / filename)
            lists = root.findall("checklist")
            cards = root.findall("placards/card")
            self.assertEqual(len(lists), 4)
            self.assertEqual(len(cards), 4)
            for index, mnemonic in enumerate(("BCISTRSC", "AAAT", "SWARTSC", "ASCOT")):
                with self.subTest(language=filename, checklist=index):
                    names = [i.findtext("name") for i in lists[index].findall("item")]
                    lines = [i.text for i in cards[index].findall("line")][1:]
                    self.assertEqual("".join(n[0] for n in names), mnemonic)
                    self.assertEqual("".join(n[0] for n in lines), mnemonic)
                    self.assertEqual(len(names), len(lines))
                    self.assertFalse(lists[index].findall(".//binding"))


    def test_legacy_display_map_covers_current_french_without_changing_placards(self):
        aircraft = ROOT / "src/SW233"
        nasal = (aircraft / "Nasal/language.nas").read_text(encoding="utf-8")
        pairs = re.findall(r'\["([^"\n]+)","([^"\n]*)"\]', nasal)
        root = ET.parse(aircraft / "Checklists/sw233.xml")
        for checklist in root.findall("checklist"):
            for field in checklist.iter():
                if field.tag not in ("title", "name", "value"):
                    continue
                text = field.text
                for old, new in pairs:
                    text = text.replace(old, new)
                self.assertTrue(text.isascii(), field.text)
        self.assertIn("DÉPORTEURS", [n.text for n in root.findall("placards/card/line")
                                    if "DÉPORTEURS" in n.text][0])

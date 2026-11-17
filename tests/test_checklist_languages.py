"""Preserve source-attested mnemonic order across translated UI resources."""

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

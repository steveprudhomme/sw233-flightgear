"""Verify packaging cannot overwrite an existing installation."""

import shutil
import unittest
import xml.etree.ElementTree as ET
from uuid import uuid4

from tools.package import ROOT, package


class PackageTests(unittest.TestCase):
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

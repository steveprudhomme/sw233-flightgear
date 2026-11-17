"""Reject broken visual dependencies, including nested models and effects."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.launch import validate_model_resources


class VisualResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='SW233 visuals ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.air = self.root / 'Aircraft/SW233'
        self.write('Models/main.xml', '''<PropertyList>
          <path>body.ac</path>
          <model><path>crew/crew.xml</path></model>
          <effect><inherits-from>Aircraft/SW233/Effects/glass</inherits-from></effect>
        </PropertyList>''')
        self.write('Models/body.ac', 'AC3Db\ntexture "paint.png"\n')
        self.write('Models/paint.png', 'texture fixture')
        self.write('Models/crew/crew.xml', '<PropertyList><path>crew.ac</path></PropertyList>')
        self.write('Models/crew/crew.ac', 'AC3Db\ntexture "../paint.png"\n')
        self.write('Effects/glass.eff', '''<PropertyList>
          <inherits-from>Effects/glass</inherits-from>
          <parameters><texture><image>Aircraft/SW233/Models/paint.png</image></texture></parameters>
        </PropertyList>''')
        self.model = self.air / 'Models/main.xml'

    def write(self, name, content):
        path = self.air / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    def test_nested_dependencies_and_builtin_effect(self):
        validate_model_resources(self.root, self.model)

    def test_missing_nested_dependencies_rejected(self):
        for name in ('Models/crew/crew.xml', 'Models/crew/crew.ac',
                     'Models/paint.png', 'Effects/glass.eff'):
            with self.subTest(resource=name):
                path = self.air / name
                original = path.read_bytes()
                path.unlink()
                try:
                    with self.assertRaisesRegex(ValueError, 'absent'):
                        validate_model_resources(self.root, self.model)
                finally:
                    path.write_bytes(original)

    def test_effect_inheritance_and_texture_are_recursive(self):
        self.write('Effects/glass.eff', '''<PropertyList>
          <inherits-from>base</inherits-from></PropertyList>''')
        self.write('Effects/base.eff', '''<PropertyList>
          <inherits-from>Effects/glass</inherits-from>
          <parameters><texture><images><positive-x>missing.png</positive-x>
          </images></texture></parameters></PropertyList>''')
        with self.assertRaisesRegex(ValueError, 'missing.png'):
            validate_model_resources(self.root, self.model)

    def test_escape_from_aircraft_rejected_even_if_file_exists(self):
        outside = self.root / 'outside.ac'
        outside.write_text('AC3Db', encoding='utf-8')
        self.write('Models/crew/crew.xml',
                   '<PropertyList><path>../../../../outside.ac</path></PropertyList>')
        with self.assertRaisesRegex(ValueError, 'invalide'):
            validate_model_resources(self.root, self.model)

    def test_shared_and_cyclic_models_terminate(self):
        self.write('Models/crew/crew.xml', '''<PropertyList><path>crew.ac</path>
          <model><path>../main.xml</path></model></PropertyList>''')
        validate_model_resources(self.root, self.model)

    def test_malformed_effect_rejected(self):
        self.write('Effects/glass.eff', '<PropertyList>')
        with self.assertRaises(ET.ParseError):
            validate_model_resources(self.root, self.model)


if __name__ == '__main__':
    unittest.main()

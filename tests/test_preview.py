"""Check optional catalog media and source metadata without network access."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from tools.launch import verify
from tools.package import ROOT, package


class PreviewTests(unittest.TestCase):
    def test_optional_media_and_manifest(self):
        with TemporaryDirectory(prefix='SW233 preview ') as tmp:
            root = Path(tmp)
            plain = root / 'plain'
            package(plain)
            self.assertIsNone(ET.parse(plain / 'Aircraft/SW233/sw233-set.xml').find('sim/previews'))
            source = root / 'fixture.jpg'
            Image.new('RGB', (1280, 720), 'white').save(source)
            illustrated = root / 'illustrated'
            air = package(illustrated, source)
            self.assertEqual((air / 'Previews/sw233-exterior.jpg').read_bytes(),
                             source.read_bytes())
            with Image.open(air / 'thumbnail.jpg') as thumb:
                self.assertEqual(thumb.size, (171, 128))
                self.assertEqual(thumb.format, 'JPEG')
            manifest = verify(illustrated)
            self.assertIn('Aircraft/SW233/thumbnail.jpg', manifest['files'])
            config = ET.parse(air / 'sw233-set.xml')
            self.assertEqual(config.findtext('sim/previews/preview/type'), 'exterior')
            (air / 'thumbnail.jpg').unlink()
            with self.assertRaises(ValueError):
                verify(illustrated)

    def test_source_metadata_and_reject_small_image(self):
        config = ET.parse(ROOT / 'src/SW233/sw233-set.xml')
        self.assertEqual(config.findtext('sim/minimum-fg-version'), '2024.1.7')
        self.assertIn('GPL-3.0-only', config.findtext('sim/long-description'))
        self.assertIn('prototype', config.findtext('sim/description'))
        with TemporaryDirectory() as tmp:
            image = Path(tmp) / 'tiny.jpg'
            Image.new('RGB', (171, 128)).save(image)
            output = Path(tmp) / 'rejected'
            with self.assertRaises(ValueError):
                package(output, image)
            self.assertFalse(output.exists())

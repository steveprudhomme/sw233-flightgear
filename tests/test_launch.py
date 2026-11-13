"""Relocation, integrity and argument boundaries without starting a simulator."""
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.launch import command, verify
from tools.package import package


class LaunchTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='SW233 launch ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = self.root / 'original package'
        package(self.original)
        self.moved = self.root / 'relocated package'
        shutil.copytree(self.original, self.moved)
        self.exe = self.root / 'Flight Gear' / 'fgfs.exe'
        self.exe.parent.mkdir()
        self.exe.touch()
        self.data = self.root / 'fg data'
        self.data.mkdir()
        (self.data / 'defaults.xml').write_text('<PropertyList/>')
        (self.data / 'version').write_text('2024.1.7')
        self.scene = self.root / 'scene data'
        airport = self.scene / 'Airports/C/Y/J'
        airport.mkdir(parents=True)
        (airport / 'CYJN.threshold.xml').write_text('<PropertyList/>')
        terrain = self.scene / 'Terrain/w080n40/w074n45'
        terrain.mkdir(parents=True)
        (terrain / 'sample.btg.gz').touch()

    def test_relocated_package_and_argument_boundaries(self):
        verify(self.moved)
        args = command(self.moved, self.exe, self.data, self.scene)
        self.assertIn('--fg-aircraft=' + str(self.moved / 'Aircraft'), args)
        self.assertIn('--on-ground', args)
        self.assertNotIn('--in-air', args)
        self.assertFalse(any(a.startswith('--httpd') for a in args))
        air = command(self.moved, self.exe, self.data, self.scene, 'air', 18099)
        self.assertIn('--altitude=5000', air)
        self.assertIn('--httpd=18099', air)
        self.assertFalse(any(str(self.original) in a for a in args))

    def test_missing_or_modified_texture_rejected(self):
        texture = self.moved / 'Aircraft/SW233/Models/panel.png'
        original = texture.read_bytes()
        texture.write_bytes(b'broken')
        with self.assertRaisesRegex(ValueError, 'modifie'):
            verify(self.moved)
        texture.write_bytes(original)
        texture.unlink()
        with self.assertRaisesRegex(ValueError, 'absent'):
            verify(self.moved)

    def test_wrong_paths_and_package_collision(self):
        with self.assertRaisesRegex(ValueError, 'Programme'):
            command(self.moved, self.root / 'absent.exe', self.data, self.scene)
        with self.assertRaisesRegex(ValueError, 'absent'):
            command(self.moved, self.exe, self.data, self.root / 'missing scenery')
        occupied = self.root / 'user files'
        occupied.mkdir()
        sentinel = occupied / 'launch.py'
        sentinel.write_text('user content')
        with self.assertRaises(FileExistsError):
            package(occupied)
        self.assertEqual(sentinel.read_text(), 'user content')

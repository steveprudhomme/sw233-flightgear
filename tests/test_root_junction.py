"""Regressions for the central glazing junction and rear trim."""
import unittest
from pathlib import Path

from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]


class RootJunctionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.palette, cls.objects = read_mesh(ROOT / 'src/SW233/Models/sw233.ac')

    def points(self, name):
        return [p for _, face in self.objects[name] for p in face]

    def test_glass_touches_actual_wing_root_profile(self):
        # Extract upper root segments from the exported wing, independent of its generator.
        vertices = set(p for p in self.points('aile1') if abs(p[1] - .44) < 1e-5)
        top = sorted((x, z) for x, y, z in vertices if z >= .74)
        edge = [p for p in self.points('verriere') if abs(p[1] - .44) < 1e-5
                and 1.99 <= p[0] <= 3.16]
        self.assertGreater(len(edge), 20)
        for x, y, z in edge:
            for (a, za), (b, zb) in zip(top, top[1:]):
                if a - 1e-5 <= x <= b + 1e-5:
                    self.assertAlmostEqual(z, za + (zb - za) * (x - a) / (b - a), places=4)
                    break
            else:
                self.fail('Glazing edge outside actual root segments')

    def test_grey_caps_and_left_only_filter(self):
        for side in (-1, 1):
            faces = self.objects['habillage-racine' + str(side)]
            self.assertEqual({m for m, _ in faces}, {15})
        self.assertGreater(min(self.palette[15]), 100)
        self.assertLess(max(p[1] for p in self.points('grille-racine-gauche')), 0)
        self.assertNotIn('grille-racine-droite', self.objects)
        for side in (-1, 1):
            self.assertEqual({m for m, _ in self.objects['jonction-bleue' + str(side)]}, {14})

    def test_recessed_backrest_and_belt_aperture(self):
        points = self.points('dossier-arriere-moule')
        self.assertGreater(max(p[0] for p in points) - min(p[0] for p in points), .06)
        self.assertGreater(min(p[0] for p in points), 2.41)
        opening = self.points('passage-sangle-demi-lune')
        self.assertAlmostEqual(min(p[2] for p in opening), .20)
        self.assertAlmostEqual(max(p[2] for p in opening), .265)
        self.assertAlmostEqual(max(p[1] for p in opening), .065)
        self.assertAlmostEqual(min(p[1] for p in opening), -.065)

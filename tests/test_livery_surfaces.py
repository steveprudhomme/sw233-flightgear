"""UV, surface clearance and moving-skin regression checks for provisional paint."""

import copy
import math
import shutil
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from tools.livery import (
    CHARTS,
    MOVING,
    SURFACES,
    audit_coverage,
    build_surfaces,
    chart_uv,
    finish_livery,
    normal,
    read_object,
)

ROOT = Path(__file__).resolve().parents[1]


class LiverySurfacesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="SW233 livery ")
        cls.models = Path(cls.temp.name)
        for filename in ("sw233.ac", "sw233-model.xml"):
            shutil.copyfile(ROOT / "src/SW233/Models" / filename, cls.models / filename)
        cls.before = (cls.models / "sw233.ac").read_bytes()
        cls.report = finish_livery(cls.models)
        cls.surfaces = build_surfaces(cls.models / "sw233.ac")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_requested_surfaces_and_layers_exist(self):
        self.assertEqual({s["source"] for s in self.surfaces}, set(SURFACES))
        self.assertEqual(self.report["objects"], 46)
        text = (self.models / "livery.ac").read_text()
        names = [line[6:-1] for line in text.splitlines() if line.startswith('name "')]
        self.assertEqual(len(names), len(set(names)))
        for s in self.surfaces:
            for prefix in ("livery-", "uv-"):
                self.assertIn(prefix + s["name"], names)
        self.assertEqual((self.models / "sw233.ac").read_bytes(), self.before)

    def test_every_output_reference_is_valid_and_uv_bounded(self):
        lines = (self.models / "livery.ac").read_text().splitlines()
        count = 0
        for i, line in enumerate(lines):
            if line.startswith("numvert "):
                count = int(line.split()[1])
                for row in lines[i + 1 : i + 1 + count]:
                    self.assertTrue(all(math.isfinite(float(v)) for v in row.split()))
            elif line.startswith("refs "):
                for row in lines[i + 1 : i + 1 + int(line.split()[1])]:
                    index, u, v = row.split()
                    self.assertTrue(0 <= int(index) < count)
                    self.assertTrue(0 <= float(u) <= 1)
                    self.assertTrue(0 <= float(v) <= 1)

    def test_new_charts_do_not_collapse_and_have_expected_orientation(self):
        for surface in self.surfaces:
            if surface["source"] == "fuselage":
                continue  # Legacy seam/cap chart is intentionally unchanged.
            for face in surface["polygons"]:
                points = [chart_uv(p, surface["chart"]) for p in face]
                area = sum(
                    a[0] * b[1] - b[0] * a[1] for a, b in zip(points, points[1:] + points[:1])
                )
                self.assertGreater(abs(area), 1e-7, surface["name"])
        # Looking down: right wing is screen-right, aft is screen-down.
        self.assertGreater(
            chart_uv((2.5, 0.8, -2), "wing-top")[0], chart_uv((2.5, 0.8, 2), "wing-top")[0]
        )
        self.assertLess(chart_uv((3, 0.8, 2), "wing-top")[1], chart_uv((2, 0.8, 2), "wing-top")[1])
        # Looking from below reverses horizontal orientation, not the letters.
        self.assertLess(
            chart_uv((2.5, 0.8, -2), "wing-bottom")[0], chart_uv((2.5, 0.8, 2), "wing-bottom")[0]
        )
        self.assertGreater(chart_uv((7, 1, 0), "fin-left")[0], chart_uv((6.8, 1, 0), "fin-left")[0])
        self.assertLess(chart_uv((7, 1, 0), "fin-right")[0], chart_uv((6.8, 1, 0), "fin-right")[0])

    def test_mirrored_pairs_match_geometry_and_uv(self):
        objects = {s["name"]: s for s in self.surfaces}
        for family in ("aile", "aerofrein", "empennage", "profondeur"):
            for side in ("top", "bottom"):
                left, right = objects[family + "-1-" + side], objects[family + "1-" + side]
                lv = {p for f in left["polygons"] for p in f}
                rv = {p for f in right["polygons"] for p in f}
                self.assertEqual({(p[0], p[1], -p[2]) for p in lv}, rv)
                for p in lv:
                    mirror = (p[0], p[1], -p[2])
                    u, v = chart_uv(p, left["chart"])
                    other_u, other_v = chart_uv(mirror, right["chart"])
                    self.assertAlmostEqual(u + other_u, 1)
                    self.assertAlmostEqual(v, other_v)
                    moved, other = left["shifted"][p], right["shifted"][mirror]
                    for axis, sign in ((0, 1), (1, 1), (2, -1)):
                        self.assertAlmostEqual(moved[axis] * sign, other[axis], places=7)

    def test_normals_outward_and_positions_exactly_replace_originals(self):
        for s in self.surfaces:
            for face in s["polygons"]:
                n = normal(face)
                if s["name"].endswith("-top"):
                    self.assertGreater(n[1], 0)
                elif s["name"].endswith("-bottom"):
                    self.assertLess(n[1], 0)
                elif s["source"] == "derive":
                    self.assertGreater(n[2] if s["name"].endswith("-left") else -n[2], 0)
                for p in face:
                    delta = [s["shifted"][p][i] - p[i] for i in range(3)]
                    self.assertEqual(delta, [0.0, 0.0, 0.0])

    def test_every_original_face_and_vertex_is_covered_exactly(self):
        coverage = audit_coverage(self.models / "sw233.ac", self.surfaces)
        self.assertEqual(set(coverage), set(SURFACES))
        self.assertEqual(
            sum(c["source_faces"] for c in coverage.values()),
            sum(len(read_object(self.models / "sw233.ac", n)) for n in SURFACES),
        )
        self.assertEqual(
            sum(c["replacement_faces"] for c in coverage.values()),
            sum(c["source_faces"] for c in coverage.values()) + 7,
        )
        for source in SURFACES:
            original = read_object(self.models / "sw233.ac", source)
            selected = [s for s in self.surfaces if s["source"] == source]
            self.assertEqual(
                {p for f in original for p in f},
                {p for s in selected for f in s["polygons"] for p in f},
            )
        # A missing single face must fail; testing only total vertices misses this.
        broken = copy.deepcopy(self.surfaces)
        broken[0]["polygons"].pop()
        with self.assertRaisesRegex(ValueError, "Incomplete replacement coverage"):
            audit_coverage(self.models / "sw233.ac", broken)

    def test_closed_replacements_preserve_source_two_sided_visibility(self):
        lines = (self.models / "livery.ac").read_text().splitlines()
        name = ""
        for line in lines:
            if line.startswith('name "'):
                name = line[6:-1]
            elif line.startswith("SURF "):
                closed = "-fuselage-" in name or "-aile" in name
                self.assertEqual(line, "SURF 0x30" if closed else "SURF 0x10", name)
        # Single-sheet pieces have two exact coplanar opposite faces. Only one
        # can face a given camera, because each uses single-sided rendering.
        for source in SURFACES:
            if source == "fuselage" or source.startswith("aile"):
                continue
            pair = [s for s in self.surfaces if s["source"] == source]
            for a, b in zip(pair[0]["polygons"], pair[1]["polygons"]):
                self.assertEqual(set(a), set(b))
                self.assertAlmostEqual(sum(x * y for x, y in zip(normal(a), normal(b))), -1)

    @staticmethod
    def rotation_payload(animation):
        node = copy.deepcopy(animation)
        for name in node.findall("object-name"):
            node.remove(name)
        return [
            (child.tag, (child.text or "").strip(), dict(child.attrib)) for child in node.iter()
        ]

    def test_mobile_skins_copy_authoritative_rotations_exactly(self):
        source = ET.parse(self.models / "sw233-model.xml").getroot()
        painted = ET.parse(self.models / "livery.xml").getroot()
        rotations = [a for a in painted.findall("animation") if a.findtext("type") == "rotate"]
        self.assertEqual(len(rotations), len(MOVING))
        for name in MOVING:
            original = next(
                a
                for a in source.findall("animation")
                if name in [v.text for v in a.findall("object-name")]
                and a.findtext("type") == "rotate"
            )
            actual = next(
                a
                for a in rotations
                if "uv-" + name + "-top" in [v.text for v in a.findall("object-name")]
            )
            self.assertEqual(self.rotation_payload(original), self.rotation_payload(actual))
            self.assertEqual(
                {v.text for v in actual.findall("object-name")},
                {
                    mode + "-" + name + "-" + side
                    for mode in ("uv", "livery")
                    for side in ("top", "bottom")
                },
            )

    def test_diagnostic_layer_overrides_paint_without_requiring_it(self):
        root = ET.parse(self.models / "livery.xml").getroot()
        selects = [a for a in root.findall("animation") if a.findtext("type") == "select"]

        def evaluate(node, properties):
            if node.tag == "property":
                return properties.get(node.text, False)
            if node.tag in ("and", "condition"):
                return all(evaluate(child, properties) for child in node)
            if node.tag == "not":
                return not evaluate(node[0], properties)
            raise AssertionError(node.tag)

        for paint in (False, True):
            for grid in (False, True):
                properties = {
                    "/sim/sw233/visuals/livery": paint,
                    "/sim/sw233/visuals/uv-grid": grid,
                }
                active = [
                    a.findtext("object-name").split("-")[0]
                    for a in selects
                    if evaluate(a.find("condition"), properties)
                ]
                self.assertEqual(active, ["uv"] if grid else ["livery"] if paint else [])

    def test_textures_exist_are_original_and_grid_is_asymmetric(self):
        for chart in self.report["charts"]:
            with Image.open(self.models / f"livery-grid-{chart}.png") as im:
                self.assertEqual(im.getpixel((0, 0)), (38, 255, 83))  # U=0 green edge.
                self.assertEqual(im.getpixel((im.width // 2, im.height - 1)), (255, 48, 48))
            with Image.open(self.models / f"livery-{chart}.png") as im:
                if chart in CHARTS:
                    self.assertEqual(im.getextrema(), ((237, 237), (179, 179), (41, 41)))

    def test_missing_rotation_fails_instead_of_freezing_a_control_skin(self):
        with TemporaryDirectory(prefix="SW233 missing rotation ") as temp:
            target = Path(temp)
            shutil.copyfile(self.models / "sw233.ac", target / "sw233.ac")
            root = ET.parse(self.models / "sw233-model.xml").getroot()
            for a in list(root.findall("animation")):
                if a.findtext("object-name") == "aerofrein-1":
                    root.remove(a)
            ET.ElementTree(root).write(target / "sw233-model.xml")
            with self.assertRaisesRegex(ValueError, "authoritative rotation"):
                finish_livery(target)

    def test_negative_vertex_index_is_rejected(self):
        with TemporaryDirectory(prefix="SW233 bad UV source ") as temp:
            p = Path(temp) / "bad.ac"
            p.write_text(
                'name "fuselage"\nnumvert 3\n0 0 0\n1 0 0\n0 1 0\n'
                "refs 3\n-1 0 0\n1 0 0\n2 0 0\nkids 0"
            )
            with self.assertRaisesRegex(ValueError, "Invalid vertex"):
                read_object(p, "fuselage")


if __name__ == "__main__":
    unittest.main()

"""Check real crew geometry, clothing placement and complementary native LOD ranges."""

import math
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.crew import (
    LOD_DISTANCE_M,
    build_crew_mesh,
    crew_lods,
    export_atlas_source,
    finish_crew,
)
from tools.parts_atlas import bounds, read_mesh

ROOT = Path(__file__).resolve().parents[1]


def condition(node, properties):
    if node.tag in {"condition", "and"}:
        return all(condition(child, properties) for child in node)
    if node.tag == "not":
        return not condition(node[0], properties)
    if node.tag == "property":
        return bool(properties[node.text])
    if node.tag == "greater-than":
        return properties[node.findtext("property")] > float(node.findtext("value"))
    if node.tag == "equals":
        return properties[node.findtext("property")] == float(node.findtext("value"))
    raise AssertionError(f"Unexpected condition {node.tag}")


def surface_heights(x, y, faces):
    """Intersect a vertical line with actual aircraft triangles, in construction axes."""
    for _, polygon in faces:
        for i in range(1, len(polygon) - 1):
            a, b, c = polygon[0], polygon[i], polygon[i + 1]
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(den) < 1e-12:
                continue
            u = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / den
            v = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / den
            if min(u, v, 1 - u - v) >= -1e-7:
                yield u * a[2] + v * b[2] + (1 - u - v) * c[2]


def surface_margin(parts, faces, above=False):
    # Vertices and triangle centres are independent samples of the real surfaces.
    # This is a sampled clearance check, not an exhaustive collision certification.
    points = set()
    for _, _, vertices, triangles, _, _ in parts:
        points.update(vertices)
        points.update(
            tuple(sum(vertices[j][k] for j in f) / 3 for k in range(3)) for f in triangles
        )
    margins = []
    for x, y, z in points:
        heights = list(surface_heights(x, y, faces))
        if not heights:
            raise AssertionError(f"No aircraft surface under/above sample {(x, y, z)}")
        surface = min(heights)
        margins.append(z - surface if above else surface - z)
    return min(margins), len(points)


def clearance_data():
    """Read the current aircraft; return reproducible, conservative geometric margins."""
    _, objects = read_mesh(ROOT / "src/SW233/Models/sw233.ac")
    mesh = build_crew_mesh()
    roof = sum((objects[n] for n in ("pare-brise", "verriere", "raccord-arriere")), [])
    result = {}
    for person in ("front", "rear"):
        parts = [p for p in mesh.parts if p[0].startswith(person + "-")]
        head = [p for p in parts if p[-1] == "head"]
        feet = [p for p in parts if "-boot" in p[0] or "-sole" in p[0]]
        hands = [p for p in parts if any(k in p[0] for k in ("-hand", "-finger", "-thumb"))]
        head_margin, head_samples = surface_margin(head, roof)
        feet_margin, feet_samples = surface_margin(feet, objects["fuselage"], above=True)
        hand_points = [v for p in hands for v in p[2]]
        hand_box = [
            (min(v[k] for v in hand_points), max(v[k] for v in hand_points)) for k in range(3)
        ]
        stick_box = bounds(objects["manche"])
        stick_gap = math.sqrt(
            sum(max(0, a[0] - b[1], b[0] - a[1]) ** 2 for a, b in zip(hand_box, stick_box))
        )
        brake_box = bounds(objects["poignee-frein"])
        # The existing brake lever rotates about Y, so its lateral extent is
        # invariant for every deflection, not just the two end positions.
        brake_gap = hand_box[1][0] - brake_box[1][1]
        result[person] = {
            "roof_vertical_margin_m": head_margin,
            "lower_shell_vertical_margin_m": feet_margin,
            "stick_aabb_separation_m": stick_gap,
            "brake_all_deflections_lateral_gap_m": brake_gap,
            "head_samples": head_samples,
            "feet_samples": feet_samples,
        }
    return result


class CrewVisualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = TemporaryDirectory(prefix="SW233 crew test ")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.models = Path(cls.temp.name)
        cls.report = finish_crew(cls.models)
        cls.tree = ET.parse(cls.models / "crew.xml")
        cls.mesh = (cls.models / "crew.ac").read_text(encoding="utf-8")
        cls.clearances = clearance_data()

    def visible(self, front=180, rear=180, enabled=True, wings=False, view=1, distance=1):
        properties = {
            "/fdm/jsbsim/inertia/pointmass-weight-lbs": front,
            "/fdm/jsbsim/inertia/pointmass-weight-lbs[1]": rear,
            "/sim/sw233/visuals/crew": enabled,
            "/sim/sw233/visuals/wings": wings,
            "/sim/current-view/view-number": view,
        }
        selected = {
            obj.text
            for anim in self.tree.findall("animation")
            if anim.findtext("type") == "select" and condition(anim.find("condition"), properties)
            for obj in anim.findall("object-name")
        }
        ranged = {
            obj.text
            for anim in self.tree.findall("animation")
            if anim.findtext("type") == "range"
            and float(anim.findtext("min-m", "0"))
            <= distance
            < float(anim.findtext("max-m", "inf"))
            for obj in anim.findall("object-name")
        }
        return selected & ranged

    def test_zero_mass_hides_only_corresponding_occupant_in_both_lods(self):
        for distance in (1, 100):
            for front, rear in ((0, 0), (180, 0), (0, 180), (180, 180)):
                with self.subTest(front=front, rear=rear, distance=distance):
                    visible = self.visible(front, rear, distance=distance)
                    self.assertEqual(any(n.startswith("front-") for n in visible), front > 0)
                    self.assertEqual(any(n.startswith("rear-") for n in visible), rear > 0)
            self.assertFalse(self.visible(enabled=False, wings=True, distance=distance))

    def test_front_head_and_neck_hidden_in_cockpit_and_wings_opt_in(self):
        for distance in (1, 100):
            outside = self.visible(distance=distance)
            cockpit = self.visible(view=0, distance=distance)
            self.assertEqual(len(outside - cockpit), 1)
            self.assertTrue(all(n.startswith("front-head-") for n in outside - cockpit))
            self.assertTrue(any(n.startswith("front-body-") for n in cockpit))
            wings = self.visible(wings=True, distance=distance) - outside
            self.assertEqual(len(wings), 2)
            self.assertTrue(all("optional-fictional-wings" in n for n in wings))
        necks = [p for p in build_crew_mesh().parts if p[0].endswith("-neck")]
        self.assertEqual(len(necks), 2)
        self.assertTrue(all(p[-1] == "head" for p in necks))

    def test_complementary_ranges_have_equal_centres_without_duplicate_transition(self):
        fine, coarse = crew_lods()
        for high, low in zip(fine.parts, coarse.parts):
            for axis in range(3):
                high_bound = (min(v[axis] for v in high[2]), max(v[axis] for v in high[2]))
                low_bound = (min(v[axis] for v in low[2]), max(v[axis] for v in low[2]))
                for a, b in zip(high_bound, low_bound):
                    self.assertAlmostEqual(a, b, places=12)
        for distance in (0, 25, LOD_DISTANCE_M - 1e-6, LOD_DISTANCE_M, LOD_DISTANCE_M + 1e-6, 100):
            names = self.visible(wings=True, distance=distance)
            self.assertEqual(len(names), 6)
            suffix = "-fine" if distance < LOD_DISTANCE_M else "-coarse"
            self.assertTrue(all(n.endswith(suffix) for n in names))
        self.assertLess(self.report["coarse_triangles"], self.report["fine_triangles"] * 0.15)

    def test_all_objects_selected_and_ranged_once_without_physical_writes(self):
        names = set(re.findall(r'^name "([^"]+)"', self.mesh, re.M))
        for kind in ("select", "range"):
            selected = [
                n.text
                for a in self.tree.findall("animation")
                if a.findtext("type") == kind
                for n in a.findall("object-name")
            ]
            self.assertEqual(len(selected), len(set(selected)))
            self.assertEqual(set(selected), names)
        for tag in ("nasal", "binding", "script"):
            self.assertFalse(self.tree.findall(".//" + tag))
        mass_refs = [n for n in self.tree.findall(".//property") if "pointmass" in (n.text or "")]
        predicates = self.tree.findall(".//greater-than/property")
        self.assertTrue(mass_refs)
        self.assertTrue(all(n in predicates for n in mass_refs))

    def test_head_feet_and_fixed_hands_clear_current_aircraft(self):
        for person, result in self.clearances.items():
            with self.subTest(person=person):
                self.assertGreater(result["roof_vertical_margin_m"], 0.015)
                self.assertGreater(result["lower_shell_vertical_margin_m"], 0.09)
                self.assertGreater(result["stick_aabb_separation_m"], 0.05)
                self.assertGreater(result["brake_all_deflections_lateral_gap_m"], 0.15)
                self.assertGreater(result["head_samples"], 1000)
                self.assertGreater(result["feet_samples"], 1000)
        aircraft = ET.parse(ROOT / "src/SW233/Models/sw233-model.xml")
        stick = [
            a
            for a in aircraft.findall("animation")
            if "manche" in [n.text for n in a.findall("object-name")]
        ]
        self.assertFalse(stick, "Reassess fixed hand clearance if the stick gains an animation")
        brake = next(
            a
            for a in aircraft.findall("animation")
            if "poignee-frein" in [n.text for n in a.findall("object-name")]
        )
        self.assertEqual(brake.findtext("type"), "rotate")
        self.assertEqual([float(brake.findtext("axis/" + k)) for k in "xyz"], [0, -1, 0])

    def test_name_tape_has_clear_chest_space_outside_harness(self):
        mesh = build_crew_mesh()
        for person in ("front", "rear"):
            tag = next(p for p in mesh.parts if p[0] == person + "-nametape")
            points = tag[2]
            self.assertAlmostEqual(max(p[1] for p in points) - min(p[1] for p in points), 0.082)
            self.assertAlmostEqual(max(p[2] for p in points) - min(p[2] for p in points), 0.025)
            straps = [p for p in mesh.parts if p[0].startswith(person + "-right-shoulder-harness")]
            for z in (0.179, 0.1915, 0.204):
                inner = []
                for strap in straps:
                    corners = strap[2]
                    for a, b in zip(corners, corners[1:] + corners[:1]):
                        if min(a[2], b[2]) <= z <= max(a[2], b[2]) and a[2] != b[2]:
                            inner.append(a[1] + (b[1] - a[1]) * (z - a[2]) / (b[2] - a[2]))
                self.assertTrue(inner)
                self.assertGreater(min(inner) - max(p[1] for p in points), 0.01)

    def test_text_u_runs_left_to_right_from_each_exterior_view(self):
        # Chest is seen looking aft (+X): screen right is -Y. On the right
        # shoulder one looks -Y (screen right -X), and the left shoulder is opposite.
        # This geometric camera test detects mirror images without relying on OCR.
        raw = build_crew_mesh()
        fine, _ = crew_lods()
        checked = 0
        for part in raw.parts:
            name, _, vertices, _, uv, category = part
            if name.endswith("nametape") or "optional-fictional-wings" in name:
                right = (0, -1, 0)
            elif name.endswith("right-shoulder-patch"):
                right = (-1, 0, 0)
            elif name.endswith("left-shoulder-patch"):
                right = (1, 0, 0)
            else:
                continue
            screen = [sum(point[k] * right[k] for k in range(3)) for point in vertices]
            horizontal = sum(
                (screen[i] - screen[j]) * (uv[i][0] - uv[j][0]) for i in range(4) for j in range(4)
            )
            vertical = sum(
                (vertices[i][2] - vertices[j][2]) * (uv[i][1] - uv[j][1])
                for i in range(4)
                for j in range(4)
            )
            self.assertGreater(horizontal, 0, name + " mirrored outside")
            self.assertGreater(vertical, 0, name + " upside down")
            # Fusion must retain that orientation in the runtime atlas UVs.
            group = next(
                p
                for p in fine.parts
                if p[0].startswith(name.split("-")[0] + "-") and p[-1] == category
            )
            runtime_uv = [group[4][group[2].index(point)] for point in vertices]
            self.assertGreater(
                sum(
                    (screen[i] - screen[j]) * (runtime_uv[i][0] - runtime_uv[j][0])
                    for i in range(4)
                    for j in range(4)
                ),
                0,
                name,
            )
            checked += 1
        self.assertEqual(checked, 8)

    def test_individual_parts_remain_available_for_teaching_atlas(self):
        path = self.models / "crew-parts.ac"
        count = export_atlas_source(path)
        _, parts = read_mesh(path)
        self.assertEqual(count, len(parts))
        for name in ("front-neck", "rear-nametape", "front-left-sleeve"):
            self.assertIn(name, parts)

    def test_serialized_geometry_has_finite_non_degenerate_triangles_and_uvs(self):
        count = 0
        for part in self.mesh.split("OBJECT poly")[1:]:
            name = re.search(r'name "([^"]+)"', part).group(1)
            rows = part.split("numvert ")[1].splitlines()
            vertices = [tuple(map(float, row.split())) for row in rows[1 : 1 + int(rows[0])]]
            self.assertTrue(all(math.isfinite(v) for point in vertices for v in point), name)
            for surface in part.split("SURF ")[1:]:
                rows = surface.split("refs ")[1].splitlines()
                self.assertEqual(int(rows[0]), 3, name)
                refs = [row.split() for row in rows[1:4]]
                self.assertTrue(all(0 <= float(v) <= 1 for ref in refs for v in ref[1:]), name)
                indices = [int(ref[0]) for ref in refs]
                self.assertTrue(all(0 <= i < len(vertices) for i in indices), name)
                a, b, c = [vertices[i] for i in indices]
                u = [b[i] - a[i] for i in range(3)]
                v = [c[i] - a[i] for i in range(3)]
                cross = (
                    u[1] * v[2] - u[2] * v[1],
                    u[2] * v[0] - u[0] * v[2],
                    u[0] * v[1] - u[1] * v[0],
                )
                self.assertGreater(sum(x * x for x in cross), 1e-22, name)
                count += 1
        self.assertEqual(count, self.report["triangles"])


if __name__ == "__main__":
    unittest.main()

"""Original SW233 crew: deterministic anatomical lofts and painted cloth atlas.

Construction coordinates are metres (x aft, y right, z up). No downloaded mesh,
portrait or photo texture is used. finish_crew is the package-builder entry point.
"""

import json
import math
import random
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TILES = {
    "blue": (0, (44, 68, 93)),
    "green": (1, (79, 86, 62)),
    "skin": (2, (177, 132, 104)),
    "hair": (3, (64, 49, 39)),
    "boot": (4, (29, 30, 29)),
    "strap": (5, (102, 102, 84)),
    "metal": (6, (151, 155, 149)),
    "dark": (7, (34, 39, 39)),
    "name_front": (8, (25, 38, 51)),
    "name_rear": (9, (44, 49, 37)),
    "project": (10, (31, 43, 53)),
    "aircraft": (11, (37, 46, 48)),
    "wings": (12, (37, 46, 48)),
    "seam_blue": (13, (65, 86, 106)),
    "seam_green": (14, (104, 109, 83)),
    "lips": (15, (137, 89, 77)),
}


def _label_font():
    """Use an accented Unicode font on common hosts, with Pillow fallback."""
    for candidate in (
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ):
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, 32)
    return ImageFont.load_default(size=32)


def _atlas(path):
    """4x4 original 256 px tiles, including isolated embroidered label tiles."""
    im = Image.new("RGB", (1024, 1024))
    rng = random.Random(233)
    for key, (index, color) in TILES.items():
        tile = Image.new("RGB", (256, 256))
        pix = tile.load()
        for v in range(256):
            for u in range(256):
                grain = rng.randrange(-3, 4)
                weave = (2 if (u % 4 == 0) else 0) - (2 if v % 4 == 0 else 0)
                pix[u, v] = tuple(max(0, min(255, c + grain + weave)) for c in color)
        draw = ImageDraw.Draw(tile)
        if key in ("blue", "green"):
            # Subtle folds; detailed garment seams are geometry, not baked shadows.
            for row in (30, 97, 165, 230):
                draw.arc(
                    (8, row - 12, 245, row + 19),
                    185,
                    350,
                    fill=tuple(max(0, c - 7) for c in color),
                    width=2,
                )
        if key.startswith("name_"):
            label = "R. PAG\u00c9" if key == "name_front" else "R. VACHON"
            # Paint at the physical tape aspect ratio, then fit the square atlas
            # tile: avoids tiny, vertically squashed letters on the 82 x 25 mm tag.
            tape = Image.new("RGB", (256, 80), color)
            lettering = ImageDraw.Draw(tape)
            lettering.rectangle((3, 3, 252, 76), outline="#b8b7a2", width=2)
            lettering.text((128, 40), label, anchor="mm", font=_label_font(), fill="#e0dfc4")
            tile = tape.resize((256, 256), Image.Resampling.LANCZOS)
        if key in ("project", "aircraft", "wings"):
            draw.rounded_rectangle((8, 10, 247, 245), radius=32, outline="#bebda3", width=4)
            font = ImageFont.load_default(size=25)
            if key == "project":
                draw.text((128, 65), "PROJET", anchor="mm", font=font, fill="#e0dfc4")
                draw.text((128, 124), "CEC", anchor="mm", font=font, fill="#e0dfc4")
                draw.text((128, 180), "ST-JEAN", anchor="mm", font=font, fill="#e0dfc4")
            else:
                draw.line((30, 107, 226, 107), fill="#e0dfc4", width=8)
                draw.line((128, 55, 128, 163), fill="#e0dfc4", width=7)
                draw.line((94, 150, 162, 150), fill="#e0dfc4", width=6)
                draw.text(
                    (128, 207),
                    "SW233" if key == "aircraft" else "FICTIF",
                    anchor="mm",
                    font=font,
                    fill="#e0dfc4",
                )
        im.paste(tile, ((index % 4) * 256, (index // 4) * 256))
    im.save(path)


class CrewMesh:
    def __init__(self, low_detail=False):
        self.parts = []
        self.low_detail = low_detail

    def add(self, name, material, vertices, faces, uvs=None, category="body"):
        if self.low_detail:
            keep = (
                "torso",
                "pelvis",
                "neck",
                "head",
                "hair",
                "nose",
                "ear",
                "thigh",
                "knee",
                "calf",
                "boot-top",
                "boot",
                "sole",
                "shoulder",
                "sleeve",
                "hand",
                "shoulder-harness",
                "lap-harness",
                "belt-buckle",
                "optional-fictional-wings",
            )
            if (
                not any(name.endswith("-" + suffix) for suffix in keep)
                and "-shoulder-harness-" not in name
            ):
                return
        assert all(len(f) == 3 for f in faces)
        assert all(0 <= i < len(vertices) for f in faces for i in f)
        if uvs is None:
            uvs = [(0.5, 0.5)] * len(vertices)
        assert all(0 <= u <= 1 and 0 <= v <= 1 for u, v in uvs)
        self.parts.append((name, material, vertices, faces, uvs, category))

    def loft(self, name, material, rings, category="body", segments=24):
        """Horizontal elliptical rings: (x, y, z, radius_x, radius_y)."""
        segments = min(segments, 8) if self.low_detail else segments
        vs, uv, fs = [], [], []
        for row, (x, y, z, rx, ry) in enumerate(rings):
            for i in range(segments + 1):
                a = 2 * math.pi * i / segments
                vs.append((x + rx * math.cos(a), y + ry * math.sin(a), z))
                uv.append((i / segments, row / (len(rings) - 1)))
        for row in range(len(rings) - 1):
            for i in range(segments):
                a = row * (segments + 1) + i
                b = a + segments + 1
                fs.extend([(a, a + 1, b + 1), (a, b + 1, b)])
        # End caps avoid open cuffs and soles. Winding is outward.
        for row, reverse in ((0, True), (len(rings) - 1, False)):
            x, y, z, _, _ = rings[row]
            mid = len(vs)
            vs.append((x, y, z))
            uv.append((0.5, 0.5))
            for i in range(segments):
                a = row * (segments + 1) + i
                fs.append((mid, a + 1, a) if reverse else (mid, a, a + 1))
        self.add(name, material, vs, fs, uv, category)

    def ellipsoid(self, name, material, center, radii, category="body", n=16):
        rings = []
        for j in range(0, 13, 3) if self.low_detail else range(13):
            a = -math.pi / 2 + math.pi * (j + 0.015) / (12 + 0.03)
            rings.append(
                (
                    center[0],
                    center[1],
                    center[2] + radii[2] * math.sin(a),
                    radii[0] * math.cos(a),
                    radii[1] * math.cos(a),
                )
            )
        self.loft(name, material, rings, category, n)

    def limb(self, name, material, a, b, radius_a, radius_b, category="body"):
        """Rounded, gently bulged sleeve/trouser/hand section along any 3D axis."""
        axis = [b[i] - a[i] for i in range(3)]
        length = math.sqrt(sum(x * x for x in axis))
        axis = [x / length for x in axis]
        helper = (0, 0, 1) if abs(axis[2]) < 0.9 else (0, 1, 0)

        def cross(u, v):
            return (
                u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0],
            )

        e = cross(axis, helper)
        size = math.sqrt(sum(x * x for x in e))
        e = [x / size for x in e]
        f = cross(axis, e)
        vs = []
        uv = []
        fs = []
        n = 8 if self.low_detail else 16
        for row, t in enumerate((0, 0.07, 0.25, 0.55, 0.83, 0.96, 1)):
            radius = ((1 - t) * radius_a + t * radius_b) * (
                0.72 + 0.28 * math.sin(math.pi * t) ** 0.4
            )
            for j in range(n + 1):
                ang = j * 2 * math.pi / n
                vs.append(
                    tuple(
                        a[k]
                        + (b[k] - a[k]) * t
                        + radius * (e[k] * math.cos(ang) + f[k] * math.sin(ang))
                        for k in range(3)
                    )
                )
                uv.append((j / n, t))
        for row in range(6):
            for j in range(n):
                q = row * (n + 1) + j
                r = q + n + 1
                fs.extend(((q, q + 1, r + 1), (q, r + 1, r)))
        for row, point in ((0, a), (6, b)):
            c = len(vs)
            vs.append(point)
            uv.append((0.5, 0.5))
            for j in range(n):
                q = row * (n + 1) + j
                fs.append((c, q + 1, q) if row == 0 else (c, q, q + 1))
        self.add(name, material, vs, fs, uv, category)

    def sleeve(self, name, material, sections):
        """One continuous bent sleeve, with shared rings through the elbow."""
        vertices, faces, uv = [], [], []
        count = 8 if self.low_detail else 24
        for row, (center, radius) in enumerate(sections):
            before = sections[max(0, row - 1)][0]
            after = sections[min(len(sections) - 1, row + 1)][0]
            tangent = [after[k] - before[k] for k in range(3)]
            length = math.sqrt(sum(t * t for t in tangent))
            tangent = [t / length for t in tangent]
            # Every sleeve travels downward and forward. A fixed lateral reference
            # avoids an abrupt basis flip at its elbow.
            u = (-tangent[2], 0, tangent[0])
            length = math.sqrt(sum(t * t for t in u))
            u = [t / length for t in u]
            v = (tangent[1] * u[2], tangent[2] * u[0] - tangent[0] * u[2], -tangent[1] * u[0])
            for j in range(count + 1):
                angle = 2 * math.pi * j / count
                vertices.append(
                    tuple(
                        center[k] + radius * (u[k] * math.cos(angle) + v[k] * math.sin(angle))
                        for k in range(3)
                    )
                )
                uv.append((j / count, row / (len(sections) - 1)))
        for row in range(len(sections) - 1):
            for j in range(count):
                a = row * (count + 1) + j
                b = a + count + 1
                faces.extend(((a, a + 1, b + 1), (a, b + 1, b)))
        for row in (0, len(sections) - 1):
            middle = len(vertices)
            vertices.append(sections[row][0])
            uv.append((0.5, 0.5))
            for j in range(count):
                a = row * (count + 1) + j
                faces.append((middle, a + 1, a) if row == 0 else (middle, a, a + 1))
        self.add(name, material, vertices, faces, uv)

    def patch(self, name, material, corners, category="body", flip_u=False):
        # Corner order follows construction coordinates. Textured labels explicitly
        # reverse U when increasing coordinate runs left in the exterior view.
        self.add(
            name,
            material,
            corners,
            [(0, 1, 2), (0, 2, 3)],
            [(1, 0), (0, 0), (0, 1), (1, 1)] if flip_u else [(0, 0), (1, 0), (1, 1), (0, 1)],
            category,
        )

    def save(self, path):
        lines = [
            "AC3Db",
            'MATERIAL "crew" rgb 1 1 1 amb 0.45 0.45 0.45 emis 0 0 0 '
            "spec 0.08 0.08 0.08 shi 12 trans 0",
            "OBJECT world",
            f"kids {len(self.parts)}",
        ]
        for name, mat, vertices, faces, uv, category in self.parts:
            lines += [
                "OBJECT poly",
                f'name "{name}"',
                'texture "crew-atlas.png"',
                "crease 70",
                f"numvert {len(vertices)}",
            ]
            lines += [f"{x:.6f} {z:.6f} {-y:.6f}" for x, y, z in vertices]
            lines.append(f"numsurf {len(faces)}")
            tile = TILES[mat][0] if mat != "atlas" else 0
            tx = tile % 4
            ty = tile // 4
            for face in faces:
                lines += ["SURF 0x30", "mat 0", "refs 3"]
                for vertex in face:
                    u, v = uv[vertex]
                    # Four-pixel gutter, AC uses bottom-left texture origin.
                    if mat != "atlas":
                        u = (tx * 256 + 4 + u * 248) / 1024
                        v = 1 - (ty * 256 + 252 - v * 248) / 1024
                    lines.append(f"{vertex} {u:.7f} {v:.7f}")
            lines.append("kids 0")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _chest_front(y, z):
    rings = (
        (-0.10, 0.035, 0.103, 0.138),
        (0.015, 0.045, 0.097, 0.137),
        (0.12, 0.050, 0.105, 0.158),
        (0.235, 0.045, 0.092, 0.174),
        (0.285, 0.035, 0.070, 0.135),
    )
    for a, b in zip(rings, rings[1:]):
        if a[0] <= z <= b[0]:
            t = (z - a[0]) / (b[0] - a[0])
            x, rx, ry = ((1 - t) * a[i] + t * b[i] for i in (1, 2, 3))
            return x - rx * math.sqrt(max(0, 1 - (y / ry) ** 2)) - 0.0025
    raise ValueError("Chest detail outside torso interpolation")


def _person(mesh, prefix, seat, cloth, head_z):
    """Seated proportions chosen for the cockpit, not anthropometric certification."""
    seam = "seam_" + cloth

    def e(label, mat, c, r, cat="body"):
        mesh.ellipsoid(prefix + "-" + label, mat, (c[0] + seat, c[1], c[2]), r, cat)

    def limb(label, mat, a, b, ra, rb=None, cat="body"):
        mesh.limb(
            prefix + "-" + label,
            mat,
            (seat + a[0], a[1], a[2]),
            (seat + b[0], b[1], b[2]),
            ra,
            rb or ra,
            cat,
        )

    def patch(label, mat, points, cat="body", flip_u=False):
        mesh.patch(
            prefix + "-" + label, mat, [(seat + x, y, z) for x, y, z in points], cat, flip_u=flip_u
        )

    mesh.loft(
        prefix + "-torso",
        cloth,
        [
            (seat + 0.015, 0, -0.18, 0.095, 0.115),
            (seat + 0.035, 0, -0.10, 0.103, 0.138),
            (seat + 0.045, 0, 0.015, 0.097, 0.137),
            (seat + 0.050, 0, 0.12, 0.105, 0.158),
            (seat + 0.045, 0, 0.235, 0.092, 0.174),
            (seat + 0.035, 0, 0.285, 0.070, 0.135),
            (seat + 0.025, 0, 0.302, 0.052, 0.067),
        ],
    )
    e("pelvis", cloth, (0.01, 0, -0.16), (0.115, 0.156, 0.105))
    # The neck belongs to the head selection too: the pilot camera must not
    # look down onto a detached skin sphere when the front head is hidden.
    e("neck", "skin", (0.024, 0, 0.316), (0.041, 0.043, 0.053), "head")
    # Chin, jaw, cheeks and skull share one surface, avoiding the visible dark
    # intersection formerly produced by two overlapping ellipsoids.
    mesh.loft(
        prefix + "-head",
        "skin",
        [
            (seat + 0.018, 0, head_z - 0.116, 0.025, 0.027),
            (seat - 0.003, 0, head_z - 0.095, 0.050, 0.044),
            (seat - 0.008, 0, head_z - 0.067, 0.067, 0.056),
            (seat + 0.010, 0, head_z - 0.030, 0.076, 0.066),
            (seat + 0.020, 0, head_z + 0.020, 0.083, 0.069),
            (seat + 0.026, 0, head_z + 0.065, 0.075, 0.063),
            (seat + 0.028, 0, head_z + 0.103, 0.045, 0.041),
            (seat + 0.028, 0, head_z + 0.116, 0.002, 0.002),
        ],
        "head",
        segments=32,
    )
    e("hair", "hair", (0.031, 0, head_z + 0.068), (0.077, 0.068, 0.052), "head")
    e("nose", "skin", (-0.065, 0, head_z - 0.005), (0.027, 0.016, 0.025), "head")
    for sign in (-1, 1):
        s = "left" if sign < 0 else "right"
        e(s + "-ear", "skin", (0.017, sign * 0.070, head_z - 0.012), (0.020, 0.010, 0.031), "head")
        e(s + "-eye", "dark", (-0.056, sign * 0.030, head_z + 0.016), (0.005, 0.012, 0.004), "head")
        limb(
            s + "-brow",
            "hair",
            (-0.054, sign * 0.020, head_z + 0.033),
            (-0.054, sign * 0.043, head_z + 0.030),
            0.003,
            cat="head",
        )
        # Broad upper legs, bent knees, tapering calves and rounded boot uppers.
        limb(
            s + "-thigh",
            cloth,
            (-0.015, sign * 0.089, -0.16),
            (-0.28, sign * 0.120, -0.20),
            0.081,
            0.069,
        )
        e(s + "-knee", cloth, (-0.28, sign * 0.120, -0.20), (0.074, 0.070, 0.071))
        limb(
            s + "-calf",
            cloth,
            (-0.29, sign * 0.12, -0.21),
            (-0.47, sign * 0.12, -0.36),
            0.061,
            0.039,
        )
        limb(
            s + "-boot-top",
            "boot",
            (-0.45, sign * 0.12, -0.345),
            (-0.49, sign * 0.12, -0.41),
            0.043,
            0.046,
        )
        e(s + "-boot", "boot", (-0.535, sign * 0.12, -0.420), (0.097, 0.047, 0.044))
        e(s + "-sole", "dark", (-0.54, sign * 0.12, -0.449), (0.099, 0.048, 0.014))
        # Shoulder cap penetrates the torso; the sleeve is one connected mesh
        # all the way to its cuff, rather than three barely touching solids.
        e(s + "-shoulder", cloth, (0.035, sign * 0.150, 0.232), (0.070, 0.066, 0.064))
        mesh.sleeve(
            prefix + "-" + s + "-sleeve",
            cloth,
            [
                ((seat + 0.035, sign * 0.137, 0.242), 0.059),
                ((seat + 0.027, sign * 0.163, 0.218), 0.061),
                ((seat + 0.006, sign * 0.181, 0.151), 0.057),
                ((seat - 0.022, sign * 0.195, 0.079), 0.052),
                ((seat - 0.046, sign * 0.195, 0.045), 0.049),
                ((seat - 0.079, sign * 0.183, 0.029), 0.046),
                ((seat - 0.147, sign * 0.156, 0.008), 0.041),
                ((seat - 0.211, sign * 0.132, -0.015), 0.035),
                ((seat - 0.250, sign * 0.118, -0.029), 0.030),
            ],
        )
        limb(
            s + "-cuff",
            seam,
            (-0.221, sign * 0.129, -0.019),
            (-0.249, sign * 0.119, -0.028),
            0.034,
            0.032,
        )
        limb(
            s + "-hand",
            "skin",
            (-0.243, sign * 0.118, -0.029),
            (-0.313, sign * 0.101, -0.047),
            0.030,
            0.025,
        )
        e(s + "-thumb", "skin", (-0.280, sign * 0.089, -0.032), (0.026, 0.012, 0.014))
        for finger in range(4):
            limb(
                s + f"-finger-{finger}",
                "skin",
                (-0.300, sign * (0.085 + finger * 0.011), -0.052),
                (-0.328, sign * (0.085 + finger * 0.011), -0.062),
                0.006,
                0.005,
            )
        # Stitching follows outer sleeves and trousers; three cloth fold ridges each.
        limb(
            s + "-sleeve-seam",
            seam,
            (0.006, sign * 0.218, 0.20),
            (-0.026, sign * 0.243, 0.065),
            0.0018,
        )
        limb(
            s + "-leg-seam",
            seam,
            (-0.04, sign * 0.163, -0.17),
            (-0.29, sign * 0.184, -0.20),
            0.0017,
        )
        for j in range(3):
            limb(
                s + f"-elbow-fold-{j}",
                seam,
                (-0.075 - j * 0.012, sign * 0.177, 0.076 - j * 0.009),
                (-0.075 - j * 0.012, sign * 0.222, 0.057 - j * 0.009),
                0.002,
            )
            limb(
                s + f"-knee-fold-{j}",
                seam,
                (-0.292 - j * 0.010, sign * 0.085, -0.156 - j * 0.013),
                (-0.292 - j * 0.010, sign * 0.151, -0.156 - j * 0.013),
                0.002,
            )
        # Breast pocket flaps and zip, right nametape is above pocket.
        yc = sign * 0.095
        patch(
            s + "-pocket",
            cloth,
            [
                (-0.060, yc - 0.034, 0.073),
                (-0.060, yc + 0.034, 0.073),
                (-0.057, yc + 0.034, 0.159),
                (-0.057, yc - 0.034, 0.159),
            ],
        )
        limb(
            s + "-pocket-zip",
            "metal",
            (-0.062, yc - 0.030, 0.155),
            (-0.062, yc + 0.030, 0.155),
            0.0017,
        )
        limb(
            s + "-pocket-edge",
            seam,
            (-0.063, yc - 0.033, 0.074),
            (-0.063, yc + 0.033, 0.074),
            0.0015,
        )
        # Seat belt lap and shoulder webbing, broad strips over garment.
        strap_path = ((0.040, -0.068), (0.142, 0.182), (0.116, 0.272))
        for index, (a, b) in enumerate(zip(strap_path, strap_path[1:])):
            corners = []
            for y, z in (
                (a[0] - 0.015, a[1]),
                (a[0] + 0.015, a[1]),
                (b[0] + 0.015, b[1]),
                (b[0] - 0.015, b[1]),
            ):
                corners.append((_chest_front(sign * y, z) - 0.002, sign * y, z))
            patch(s + f"-shoulder-harness-{index}", "strap", corners)
        patch(
            s + "-lap-harness",
            "strap",
            [
                (-0.108, sign * 0.012, -0.126),
                (-0.079, sign * 0.142, -0.150),
                (-0.085, sign * 0.144, -0.115),
                (-0.112, sign * 0.012, -0.090),
            ],
        )
        e(
            s + "-harness-adjuster",
            "metal",
            (_chest_front(sign * 0.113, 0.110) - 0.008, sign * 0.113, 0.110),
            (0.008, 0.020, 0.023),
        )
        # Shoulder project labels are original and are not official insignia.
        outer = sign * 0.218
        patch(
            s + "-shoulder-patch",
            "project" if sign > 0 else "aircraft",
            [
                (-0.025, outer, 0.132),
                (0.032, outer, 0.132),
                (0.032, outer, 0.213),
                (-0.025, outer, 0.213),
            ],
            flip_u=sign > 0,
        )
        for j in range(4):
            limb(
                s + f"-boot-lace-{j}",
                "seam_green",
                (-0.515 - j * 0.014, sign * 0.096, -0.387),
                (-0.515 - j * 0.014, sign * 0.144, -0.387),
                0.0016,
            )
    limb(
        "mouth",
        "lips",
        (-0.074, -0.019, head_z - 0.045),
        (-0.074, 0.019, head_z - 0.045),
        0.002,
        cat="head",
    )
    # Collar rolls, front opening and fine zipper pull.
    for sign in (-1, 1):
        limb(
            f"collar-{sign}",
            cloth,
            (-0.020, sign * 0.052, 0.302),
            (-0.060, sign * 0.028, 0.247),
            0.016,
            0.010,
        )
    limb("central-zip", "metal", (-0.060, 0, 0.251), (-0.060, 0, -0.045), 0.0017)
    e("zip-pull", "metal", (-0.065, 0, 0.238), (0.004, 0.006, 0.011))
    e("belt-buckle", "metal", (-0.117, 0, -0.108), (0.012, 0.027, 0.026))
    e("buckle-inset", "dark", (-0.128, 0, -0.108), (0.003, 0.017, 0.016))
    patch(
        "nametape",
        "name_" + prefix,
        [
            (_chest_front(y, z) - 0.001, y, z)
            for y, z in ((0.027, 0.179), (0.109, 0.179), (0.109, 0.204), (0.027, 0.204))
        ],
        flip_u=True,
    )
    patch(
        "optional-fictional-wings",
        "wings",
        [
            (-0.061, -0.140, 0.179),
            (-0.061, -0.058, 0.179),
            (-0.061, -0.058, 0.215),
            (-0.061, -0.140, 0.215),
        ],
        "wings",
        flip_u=True,
    )


# Artistic crossover: detail at cockpit distances, simplified bodies outside 60 m.
LOD_DISTANCE_M = 60.0


def build_crew_mesh(low_detail=False):
    mesh = CrewMesh(low_detail=low_detail)
    # The previous 0.438 m head intersected the sloping windscreen by 0.19 mm.
    _person(mesh, "front", 1.52, "blue", 0.418)
    _person(mesh, "rear", 2.39, "green", 0.438)
    return mesh


def export_atlas_source(path: Path):
    """Write individual fine parts for teaching diagrams, never loaded by FG."""
    mesh = build_crew_mesh()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh.save(path)
    return len(mesh.parts)


def _bounds(vertices):
    return [(min(v[i] for v in vertices), max(v[i] for v in vertices)) for i in range(3)]


def _coalesce(mesh, detail, reference=None):
    """One drawable per visibility category gives both LODs the same bound centre.

    Original part names remain in the editable mesh. UVs are resolved before
    merging so distinct cloth/skin/name tiles still use the same atlas material.
    Coarse extrema are aligned to fine extrema (sub-mm changes) for identical
    bounding boxes, hence the same eye-distance origin at the range boundary.
    """
    result = CrewMesh()
    for person in ("front", "rear"):
        for category in ("body", "head", "wings"):
            vs, faces, uv = [], [], []
            for name, material, points, triangles, coords, cat in mesh.parts:
                if not name.startswith(person + "-") or cat != category:
                    continue
                offset = len(vs)
                vs.extend(points)
                faces.extend(tuple(offset + i for i in face) for face in triangles)
                tile = TILES[material][0]
                uv.extend(
                    (
                        (tile % 4 * 256 + 4 + u * 248) / 1024,
                        1 - (tile // 4 * 256 + 252 - v * 248) / 1024,
                    )
                    for u, v in coords
                )
            label = "optional-fictional-wings" if category == "wings" else category
            if reference is not None:
                target = next(
                    p[2] for p in reference.parts if p[0] == person + "-" + label + "-fine"
                )
                old, new = _bounds(vs), _bounds(target)
                vs = [
                    tuple(
                        new[i][0]
                        + (v[i] - old[i][0]) * (new[i][1] - new[i][0]) / (old[i][1] - old[i][0])
                        if old[i][1] != old[i][0]
                        else new[i][0]
                        for i in range(3)
                    )
                    for v in vs
                ]
            result.add(person + "-" + label + "-" + detail, "atlas", vs, faces, uv, category)
    return result


def crew_lods():
    fine = _coalesce(build_crew_mesh(), "fine")
    coarse = _coalesce(build_crew_mesh(True), "coarse", fine)
    return fine, coarse


def _visibility(root, mesh, person, category):
    animation = ET.SubElement(root, "animation")
    ET.SubElement(animation, "type").text = "select"
    for name, _, _, _, _, cat in mesh.parts:
        if name.startswith(person + "-") and cat == category:
            ET.SubElement(animation, "object-name").text = name
    condition = ET.SubElement(ET.SubElement(animation, "condition"), "and")
    ET.SubElement(condition, "property").text = "/sim/sw233/visuals/crew"
    greater = ET.SubElement(condition, "greater-than")
    suffix = "" if person == "front" else "[1]"
    ET.SubElement(greater, "property").text = "/fdm/jsbsim/inertia/pointmass-weight-lbs" + suffix
    ET.SubElement(greater, "value").text = "0"
    if person == "front" and category == "head":
        different = ET.SubElement(ET.SubElement(condition, "not"), "equals")
        ET.SubElement(different, "property").text = "/sim/current-view/view-number"
        ET.SubElement(different, "value").text = "0"
    if category == "wings":
        ET.SubElement(condition, "property").text = "/sim/sw233/visuals/wings"


def finish_crew(models: Path):
    """Write two real LODs in crew.ac, range/visibility XML and original atlas."""
    models = Path(models)
    models.mkdir(parents=True, exist_ok=True)
    fine, coarse = crew_lods()
    mesh = CrewMesh()
    mesh.parts = fine.parts + coarse.parts
    _atlas(models / "crew-atlas.png")
    mesh.save(models / "crew.ac")
    root = ET.Element("PropertyList")
    ET.SubElement(root, "path").text = "crew.ac"
    for person in ("front", "rear"):
        for category in ("body", "head", "wings"):
            _visibility(root, mesh, person, category)
    # Each range wraps one merged object, so coarse and fine use equal bounding
    # spheres, independent of the visibility state of other people or heads.
    for name, _, _, _, _, _ in mesh.parts:
        animation = ET.SubElement(root, "animation")
        ET.SubElement(animation, "type").text = "range"
        ET.SubElement(animation, "object-name").text = name
        if name.endswith("-fine"):
            ET.SubElement(animation, "min-m").text = "0"
            ET.SubElement(animation, "max-m").text = str(LOD_DISTANCE_M)
        else:
            ET.SubElement(animation, "min-m").text = str(LOD_DISTANCE_M)
            # No arbitrary far cut-off: FlightGear's default maximum is unbounded.
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(models / "crew.xml", encoding="utf-8", xml_declaration=True)
    vertices = [v for p in mesh.parts for v in p[2]]
    report = {
        "objects": len(mesh.parts),
        "vertices": len(vertices),
        "triangles": sum(len(p[3]) for p in mesh.parts),
        "fine_triangles": sum(len(p[3]) for p in fine.parts),
        "coarse_triangles": sum(len(p[3]) for p in coarse.parts),
        "lod_distance_m": LOD_DISTANCE_M,
        "construction_bounds": dict(zip("xyz", _bounds(vertices))),
        "texture": [1024, 1024],
        "uv_checked": True,
    }
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("models", type=Path)
    parser.add_argument("--parts-atlas", type=Path)
    args = parser.parse_args()
    if args.parts_atlas:
        export_atlas_source(args.parts_atlas)
    print(json.dumps(finish_crew(args.models), indent=2))

"""Original provisional C-FYLP paint; no third-party photographs are embedded."""

import copy
import json
import math
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

YELLOW = "#edb329"
BLUE = "#183c72"
OFFSET = 0.0  # Complete replacement skin: the main model hides the covered originals.
SIZE = (4096, 1024)
X_RANGE = (0.0, 7.61)
Y_RANGE = (-0.63, 0.80)  # AC3D vertical coordinate, not construction y.


def read_object(path, name):
    """Read a flat AC3D object; refuse transforms and invalid vertex references."""
    text = path.read_text(encoding="utf-8")
    start = text.index('name "' + name + '"')
    lines = text[start : text.index("kids 0", start)].splitlines()
    if any(line.startswith(("loc ", "rot ")) for line in lines):
        raise ValueError("Transforms must be baked before painting: " + name)
    i = next(i for i, line in enumerate(lines) if line.startswith("numvert "))
    count = int(lines[i].split()[1])
    vertices = [tuple(map(float, line.split())) for line in lines[i + 1 : i + 1 + count]]
    faces = []
    for i, line in enumerate(lines):
        if line.startswith("refs "):
            ids = [int(row.split()[0]) for row in lines[i + 1 : i + 1 + int(line.split()[1])]]
            if any(j < 0 or j >= len(vertices) for j in ids):
                raise ValueError("Invalid vertex index: " + name)
            faces.append([vertices[j] for j in ids])
    return faces


def read_fuselage(path):
    return read_object(path, "fuselage")


def normal(face):
    """Newell's normal handles both quads and the two many-sided end caps."""
    n = [0.0, 0.0, 0.0]
    for a, b in zip(face, face[1:] + face[:1]):
        n[0] += (a[1] - b[1]) * (a[2] + b[2])
        n[1] += (a[2] - b[2]) * (a[0] + b[0])
        n[2] += (a[0] - b[0]) * (a[1] + b[1])
    length = math.sqrt(sum(v * v for v in n))
    if length < 1e-10:
        raise ValueError("Degenerate face")
    return tuple(v / length for v in n)


def uv(point, side):
    x, height, _ = point
    u = (x - X_RANGE[0]) / (X_RANGE[1] - X_RANGE[0])
    if side == "right":
        u = 1 - u
    return u, (height - Y_RANGE[0]) / (Y_RANGE[1] - Y_RANGE[0])


def paint(side):
    """Physical-position stripe, but ordinary left-to-right text on BOTH images."""
    width, height = SIZE
    im = Image.new("RGB", SIZE, YELLOW)
    draw = ImageDraw.Draw(im)

    def pixel(x, y):
        u, v = uv((x, y, 0), side)
        return round(u * (width - 1)), round((1 - v) * (height - 1))

    # Artistic boundaries, not measured from a current photograph of C-FYLP.
    contour = [(0.0, -0.32), (1.0, -0.27), (3.25, -0.23), (5.0, -0.21), (7.61, -0.12)]
    draw.polygon([pixel(x, y) for x, y in contour + [(7.61, -0.63), (0.0, -0.63)]], fill=BLUE)
    draw.line([pixel(x, y + 0.035) for x, y in contour], fill=BLUE, width=5)
    # Draw fresh letters, never mirror an image containing letters.
    a, b = pixel(3.65, -0.015), pixel(5.35, -0.17)
    box = (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))
    font = ImageFont.load_default(size=150)
    ink = Image.new("RGBA", (1000, 220), (0, 0, 0, 0))
    pen = ImageDraw.Draw(ink)
    bounds = pen.textbbox((0, 0), "C-FYLP", font=font)
    pen.text((-bounds[0], -bounds[1]), "C-FYLP", font=font, fill=BLUE)
    ink = ink.crop((0, 0, bounds[2] - bounds[0], bounds[3] - bounds[1]))
    ink = ink.resize((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    im.paste(ink, (box[0], box[1]), ink)
    return im


# All dimensions below belong to THIS MODEL, not a measurement of real C-FYLP.
SURFACES = (
    "fuselage",
    "aile-1",
    "aile1",
    "aerofrein-1",
    "aerofrein1",
    "empennage-1",
    "empennage1",
    "profondeur-1",
    "profondeur1",
    "derive",
)
MOVING = ("aerofrein-1", "aerofrein1", "profondeur-1", "profondeur1")
# Chart axes are expressed in AC3D coordinates (aft, up, left).
CHARTS = {
    "wing-top": ((2, -1, -7.7724, 7.7724), (0, -1, -3.56, -1.99), (4096, 512)),
    "wing-bottom": ((2, 1, -7.7724, 7.7724), (0, -1, -3.56, -1.99), (4096, 512)),
    "wing-tip": ((0, 1, 1.99, 3.56), (1, 1, 0.68034, 0.99472), (1024, 256)),
    "tail-top": ((2, -1, -1.93, 1.93), (0, -1, -7.79, -6.85), (2048, 512)),
    "tail-bottom": ((2, 1, -1.93, 1.93), (0, -1, -7.79, -6.85), (2048, 512)),
    "fin-left": ((0, 1, 6.5, 7.8486), (1, 1, 0.04, 1.42), (1024, 1024)),
    "fin-right": ((0, -1, -7.8486, -6.5), (1, 1, 0.04, 1.42), (1024, 1024)),
}


def chart_uv(point, chart):
    if chart in ("left", "right"):
        return uv(point, chart)

    def coordinate(axis):
        index, sign, low, high = axis
        return (point[index] * sign - low) / (high - low)

    return tuple(coordinate(axis) for axis in CHARTS[chart][:2])


def outward_wing(faces):
    """Orient the generated skin outward, including the mirrored source wing."""
    stations = defaultdict(set)
    for face in faces:
        for p in face:
            stations[p[2]].add(p)
    centers = {
        z: tuple(sum(p[i] for p in points) / len(points) for i in range(3))
        for z, points in stations.items()
    }
    result = []
    for face in faces:
        n = normal(face)
        center = tuple(sum(p[i] for p in face) / len(face) for i in range(3))
        if len({p[2] for p in face}) == 1:
            # The source wing has a tip cap; its outward direction is spanwise.
            direction = (0.0, 0.0, center[2])
        else:
            inside = tuple(sum(centers[p[2]][i] for p in face) / len(face) for i in range(3))
            direction = tuple(center[i] - inside[i] for i in range(3))
        result.append(
            face if sum(n[i] * direction[i] for i in range(3)) > 0 else list(reversed(face))
        )
    return result


def shifted_vertices(faces):
    """Keep the exact source positions; mutually exclusive layers need no offset."""
    return {point: point for face in faces for point in face}


def canonical_face(face):
    """Face identity ignores cyclic starting corner and winding, not topology."""
    cycle = tuple(face)
    reverse = tuple(reversed(cycle))
    return min(c[i:] + c[:i] for c in (cycle, reverse) for i in range(len(c)))


def audit_coverage(path, surfaces):
    """Prove every original face is replaced before it may be hidden by the parent."""
    report = {}
    for source in SURFACES:
        original = read_object(path, source)
        generated = [
            face
            for surface in surfaces
            if surface["source"] == source
            for face in surface["polygons"]
        ]
        multiplier = 1 if source == "fuselage" or source.startswith("aile") else 2
        expected = Counter(canonical_face(face) for face in original)
        expected = Counter({face: count * multiplier for face, count in expected.items()})
        if Counter(canonical_face(face) for face in generated) != expected:
            raise ValueError("Incomplete replacement coverage: " + source)
        for surface in surfaces:
            if surface["source"] == source:
                if any(surface["shifted"][p] != p for face in surface["polygons"] for p in face):
                    raise ValueError("Replacement vertices must match the original: " + source)
        report[source] = dict(
            source_faces=len(original),
            replacement_faces=len(generated),
            source_vertices=len({p for face in original for p in face}),
            coverage="complete",
            face_multiplicity=multiplier,
        )
    return report


def build_surfaces(path):
    """Complete replacement charts; thin faces get two opposing single-sided skins."""
    result = []

    def add(source, suffix, polygons, chart, shifted):
        if polygons:
            result.append(
                dict(
                    name=source + "-" + suffix,
                    source=source,
                    polygons=polygons,
                    chart=chart,
                    shifted=shifted,
                )
            )

    for source in SURFACES:
        faces = read_object(path, source)
        if source == "fuselage":
            shifted = shifted_vertices(faces)
            groups = {"left": [], "right": [], "seam": []}
            for face in faces:
                lateral = sum(p[2] for p in face) / len(face)
                side = "left" if lateral > 1e-7 else "right" if lateral < -1e-7 else "seam"
                groups[side].append(face)
            for side, polygons in groups.items():
                add(source, side, polygons, "right" if side == "right" else "left", shifted)
        elif source.startswith("aile"):
            faces = outward_wing(faces)
            shifted = shifted_vertices(faces)
            groups = {"top": [], "bottom": [], "tip": []}
            for face in faces:
                n = normal(face)
                side = "tip" if abs(n[2]) > 0.9 else "top" if n[1] > 0 else "bottom"
                groups[side].append(face)
            for side, polygons in groups.items():
                add(source, side, polygons, "wing-" + side, shifted)
        else:
            vertical = source == "derive"
            axis = 2 if vertical else 1
            chart_family = (
                "fin" if vertical else "wing" if source.startswith("aerofrein") else "tail"
            )
            for sign, side in [
                (1, "left" if vertical else "top"),
                (-1, "right" if vertical else "bottom"),
            ]:
                oriented = [
                    face if normal(face)[axis] * sign > 0 else list(reversed(face))
                    for face in faces
                ]
                add(source, side, oriented, chart_family + "-" + side, shifted_vertices(oriented))
    return result


def grid(chart):
    """Original numbered UV checker; U right/V up shows flipped chart orientation."""
    size = SIZE if chart in ("left", "right") else CHARTS[chart][2]
    im = Image.new("RGB", size)
    draw = ImageDraw.Draw(im)
    columns, rows = (16, 4) if size[0] > size[1] * 3 else (8, 8)
    font = ImageFont.load_default(size=max(12, min(size) // 28))
    for row in range(rows):
        for col in range(columns):
            x, y = col * size[0] / columns, row * size[1] / rows
            color = "#e5dd91" if (row + col) % 2 else "#365f83"
            draw.rectangle(
                (x, y, (col + 1) * size[0] / columns, (row + 1) * size[1] / rows), fill=color
            )
            draw.text(
                (x + 5, y + 5),
                f"{col + 1}:{rows - row}",
                font=font,
                fill="#141b22",
                stroke_width=1,
                stroke_fill="#ffffff",
            )
    draw.rectangle((0, size[1] - 5, size[0] - 1, size[1] - 1), fill="#ff3030")
    draw.rectangle((0, 0, 4, size[1] - 1), fill="#26ff53")
    draw.text(
        (size[0] // 2, size[1] // 2),
        chart + "  U >  V ^",
        anchor="mm",
        font=font,
        fill="white",
        stroke_width=2,
        stroke_fill="black",
    )
    return im


def model_text(surfaces):
    lines = [
        "AC3Db",
        'MATERIAL "provisional-paint" rgb 1 1 1 amb .5 .5 .5 '
        "emis 0 0 0 spec .10 .10 .10 shi 16 trans 0",
        "OBJECT world",
        f"kids {len(surfaces) * 2}",
    ]
    for mode in ("livery", "uv"):
        for surface in surfaces:
            polygons, chart = surface["polygons"], surface["chart"]
            name = mode + "-" + surface["name"]
            vertices = list(dict.fromkeys(p for face in polygons for p in face))
            indices = {p: i for i, p in enumerate(vertices)}
            texture = f"livery-{chart}.png" if mode == "livery" else f"livery-grid-{chart}.png"
            lines += [
                "OBJECT poly",
                f'name "{name}"',
                f'texture "{texture}"',
                "crease 15",
                f"numvert {len(vertices)}",
            ]
            lines += [" ".join(f"{v:.7f}" for v in surface["shifted"][p]) for p in vertices]
            lines.append(f"numsurf {len(polygons)}")
            for face in polygons:
                flags = (
                    "0x30"
                    if surface["source"] == "fuselage" or surface["source"].startswith("aile")
                    else "0x10"
                )
                lines += [f"SURF {flags}", "mat 0", f"refs {len(face)}"]
                for j, p in enumerate(face):
                    u, v = chart_uv(p, chart)
                    if not (-1e-6 <= u <= 1.000001 and -1e-6 <= v <= 1.000001):
                        raise ValueError("Surface exceeds its UV chart: " + name)
                    lines.append(f"{indices[p]} {u:.8f} {v:.8f}")
            lines.append("kids 0")
    return "\n".join(lines) + "\n"


def write_selection(root, names, grid_mode):
    animation = ET.SubElement(root, "animation")
    ET.SubElement(animation, "type").text = "select"
    for name in names:
        ET.SubElement(animation, "object-name").text = name
    condition = ET.SubElement(animation, "condition")
    if grid_mode:
        ET.SubElement(condition, "property").text = "/sim/sw233/visuals/uv-grid"
    else:
        both = ET.SubElement(condition, "and")
        ET.SubElement(both, "property").text = "/sim/sw233/visuals/livery"
        ET.SubElement(ET.SubElement(both, "not"), "property").text = "/sim/sw233/visuals/uv-grid"


def finish_livery(models: Path):
    """Generate original paint and diagnostic UV layers after finish_panel(models)."""
    models = Path(models)
    surfaces = build_surfaces(models / "sw233.ac")
    coverage = audit_coverage(models / "sw233.ac", surfaces)
    (models / "livery.ac").write_text(model_text(surfaces), encoding="utf-8")
    charts = sorted({s["chart"] for s in surfaces})
    for chart in charts:
        image = (
            paint(chart)
            if chart in ("left", "right")
            else Image.new("RGB", CHARTS[chart][2], YELLOW)
        )
        image.save(models / f"livery-{chart}.png")
        grid(chart).save(models / f"livery-grid-{chart}.png")
    root = ET.Element("PropertyList")
    ET.SubElement(root, "path").text = "livery.ac"
    # Clone the authoritative animation, rather than maintaining duplicate numbers.
    source_model = ET.parse(models / "sw233-model.xml").getroot()
    for source in MOVING:
        matches = [
            a
            for a in source_model.findall("animation")
            if a.findtext("type") == "rotate"
            and source in [n.text for n in a.findall("object-name")]
        ]
        if len(matches) != 1:
            raise ValueError("Expected one authoritative rotation for " + source)
        animation = copy.deepcopy(matches[0])
        for node in animation.findall("object-name"):
            animation.remove(node)
        for mode in ("livery", "uv"):
            for surface in surfaces:
                if surface["source"] == source:
                    ET.SubElement(animation, "object-name").text = mode + "-" + surface["name"]
        root.append(animation)
    for mode in ("livery", "uv"):
        write_selection(root, [mode + "-" + s["name"] for s in surfaces], mode == "uv")
    ET.indent(root)
    ET.ElementTree(root).write(models / "livery.xml", encoding="utf-8", xml_declaration=True)
    report = dict(
        surfaces=len(surfaces),
        objects=len(surfaces) * 2,
        charts=charts,
        original_objects=list(SURFACES),
        moving_objects=list(MOVING),
        nominal_offset_m=OFFSET,
        fully_covered_objects=list(coverage),
        coverage=coverage,
        source_visibility_rule="hide originals when livery OR uv-grid is true",
        minimum_face_clearance_m=min(
            sum((s["shifted"][p][i] - p[i]) * normal(face)[i] for i in range(3))
            for s in surfaces
            for face in s["polygons"]
            for p in face
        ),
        maximum_vertex_displacement_m=max(
            math.dist(p, moved) for s in surfaces for p, moved in s["shifted"].items()
        ),
        status="original provisional paint, not current-aircraft certification",
    )
    (models / "livery-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("models", type=Path, help="Generated package Models directory")
    print(json.dumps(finish_livery(parser.parse_args().models), indent=2))

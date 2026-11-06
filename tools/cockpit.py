"""Read the editable exterior mesh and draw a telemetry-driven front-seat view."""

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

MODEL = Path(__file__).resolve().parents[1] / "src/SW233/Models/sw233.ac"


def exterior():
    """AC coordinates (aft, up, left) to replay body (nose, right, up)."""
    lines = MODEL.read_text(encoding="utf-8").splitlines()
    materials, faces = [], []
    for i, line in enumerate(lines):
        if line.startswith("MATERIAL "):
            rgb = line.split(" rgb ")[1].split()[:3]
            materials.append(tuple(round(float(c)*255) for c in rgb))
        if line.startswith('name "'):
            name = line[6:-1]
        if line.startswith("numvert "):
            count = int(line.split()[1])
            vertices = np.array([list(map(float, s.split())) for s in lines[i+1:i+1+count]])
            vertices = np.column_stack((2.4-vertices[:, 0], -vertices[:, 2], vertices[:, 1]))
        if line.startswith("mat "):
            material = int(line.split()[1])
        if line.startswith("refs "):
            if name in {"chiffres", "traits", "tableau", "alt-fond", "vsi-fond", "ias-fond",
                        "alt-centaines", "alt-milliers", "vitesse-mph", "vario", "sieges",
                        "manche", "poignee-frein"}:
                continue
            count = int(line.split()[1])
            indices = [int(s.split()[0]) for s in lines[i+1:i+1+count]]
            faces.append((vertices[indices], materials[material]))
    return faces


def _font(size):
    for face in ("DejaVuSans.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(face, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


F = {s: _font(s) for s in (11, 13, 15, 17, 20, 24)}


def _needle(d, cx, cy, angle, length, color, width=3):
    a = math.radians(angle)
    d.line((cx, cy, cx+length*math.sin(a), cy-length*math.cos(a)), fill=color, width=width)


def dial(d, center, radius, caption, units, ticks, needles):
    cx, cy = center
    for r, color in [(radius+5, "#121e20"), (radius+3, "#88948a"),
                     (radius, "#35423f"), (radius-3, "#132026")]:
        d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=color)
    for value, angle in ticks:
        a = math.radians(angle)
        sn, cs = math.sin(a), math.cos(a)
        d.line((cx+(radius-7)*sn, cy-(radius-7)*cs, cx+(radius-12)*sn, cy-(radius-12)*cs),
               fill="#f4ead2", width=2)
        d.text((cx+(radius-21)*sn, cy-(radius-21)*cs), str(value),
               font=F[13], anchor="mm", fill="#f4ead2")
    d.text((cx, cy+15), units, fill="#b9ccc2", font=F[11], anchor="mm")
    for angle, length, color in needles:
        _needle(d, cx, cy, angle, length*radius, color)
    d.ellipse((cx-4, cy-4, cx+4, cy+4), fill="#dcbd85")
    d.text((cx, cy+radius+14), caption, font=F[13], anchor="mm", fill="#f2e9cf")


def front_view(row, vertical_fps, land, colors, rotation):
    t, north, east, height, roll, pitch, yaw, speed, altitude = row[:9]
    w, h = 890, 458
    im = Image.new("RGB", (w, h), "#c3d9df")
    d = ImageDraw.Draw(im)
    for y in range(175):
        f = y / 175
        d.line((0, y, w, y), fill=(int(116+82*f), int(171+45*f), int(196+26*f)))
    orientation = rotation(roll, pitch, yaw)
    world = (land-np.array([north, east, height])) @ orientation.T
    depth = world[:, :, 0]
    uv = world[:, :, 1:] / np.maximum(depth[:, :, None], 0.01)
    pix = uv * [590, -590] + [445, 144]
    visible = ((depth.min(1) > 30) & (pix[:, :, 0].min(1) < w)
               & (pix[:, :, 0].max(1) > 0) & (pix[:, :, 1].min(1) < 290))
    for k in np.argsort(-depth.mean(1)):
        if visible[k]:
            d.polygon([tuple(p) for p in pix[k]], fill=colors[k])
    # The tuft follows measured sideslip, not the control command.
    beta = row[9] if len(row) > 9 else 0
    spoilers = row[10] if len(row) > 10 else 0
    eye = np.array([1.50, 0, .39])
    pivot = np.array([-.055, 0, .237])
    angle = math.radians(-beta)
    rot = np.array([[math.cos(angle), -math.sin(angle), 0],
                    [math.sin(angle), math.cos(angle), 0], [0, 0, 1]])

    def sight(points):
        points = np.asarray(points)-eye
        return [(445+590*y/-x, 144-590*z/-x) for x, y, z in points]

    d.line(sight([(.222, 0, -.073), (-.055, 0, .237), (-.212, 0, .239)]),
           fill="#46595c", width=4)
    tuft = np.array([pivot, (.018, 0, .253), (.10, 0, .275),
                     (.17, 0, .306), (.235, 0, .325)])
    tuft = (tuft-pivot) @ rot.T + pivot
    # A neutral reference makes small, real deflections legible.
    d.line((445, 168, 445, 220), fill="#f4f1e7", width=1)
    d.line(sight(tuft), fill="#c83222", width=4)
    # Wing schematic: the opening displayed is the measured FCS position.
    d.rounded_rectangle((655, 26, 867, 112), 6, fill="#183239")
    d.text((667, 34), "AILE · AÉROFREINS", font=F[13], fill="#c4dfd4")
    d.line((675, 92, 845, 92), fill="#e9bd51", width=7)
    a = math.radians(85*spoilers)
    d.line((746, 88, 746+49*math.cos(a), 88-49*math.sin(a)), fill="#ec744c", width=6)
    d.text((680, 63), f"{100*spoilers:.0f} %", font=F[15], fill="#f7edd8")
    # Windscreen sill and front-seat panel inspired by C-FYLP, with original artwork.
    d.line([(0, 4), (45, 122), (80, 223)], fill="#dac486", width=8)
    d.line([(890, 4), (845, 122), (810, 223)], fill="#dac486", width=8)
    arch = [(x, 207+int(75*((x-445)/445)**2)) for x in range(0, 891, 5)]
    d.polygon([*arch, (890, h), (0, h)], fill="#263537")
    d.line(arch, fill="#ddb569", width=6)
    # Animated left cockpit lever, driven by the same measured spoiler position.
    d.line((42, 412, 42+53*spoilers, 350+30*spoilers), fill="#c4b77d", width=6)
    hx, hy = 42+53*spoilers, 350+30*spoilers
    d.ellipse((hx-9, hy-9, hx+9, hy+9), fill="#d94c24")
    d.text((445, 230), "SW233   /   PLACE AVANT", font=F[15], anchor="mm", fill="#ebdba8")
    dial(d, (184, 333), 66, "ALTIMÈTRE", "ft",
         [(v, 36*v) for v in range(10)],
         [(altitude*.036, .46, "#e2ab61"), (altitude*.36, .79, "#fff0cb")])
    mph = speed*1.150779448
    dial(d, (580, 304), 66, "ANÉMOMÈTRE", "mph",
         [(v, v*1.75-140) for v in range(0, 161, 20)],
         [(mph*1.75-140, .81, "#fff0cb")])
    dial(d, (762, 365), 55, "VARIOMÈTRE", "×1000 ft/min",
         [(v, v*65) for v in range(-2, 3)],
         [(np.clip(vertical_fps*60/1000, -2, 2)*65, .80, "#fff0cb")])
    d.ellipse((391, 284, 454, 347), fill="#101a1a", outline="#667671", width=3)
    for k in range(4):
        d.line((397, 302+k*7, 448, 298+k*7), fill="#455451", width=2)
    d.rounded_rectangle((323, 367, 492, 426), 5, fill="#efe7ce")
    d.text((407, 380), "AVANT ATTERRISSAGE", font=F[13], anchor="mm", fill="#293735")
    d.text((407, 406), "Harnais · verrière", font=F[15], anchor="mm", fill="#293735")
    return im

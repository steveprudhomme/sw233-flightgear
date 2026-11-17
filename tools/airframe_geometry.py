"""VIS-05b/c estimated curved enclosure; no changes to aerodynamic geometry."""

from bisect import bisect_right
from math import cos, pi, sin

# x, lower half-width, lower centre, lower height, rim half-width, sill.
# Model estimates. A smaller sampling interval is not increased measurement accuracy.
HULL = [
    (0, 0.024, -0.24, 0.025, 0.012, -0.215),
    (0.04, 0.105, -0.25, 0.11, 0.075, -0.15),
    (0.10, 0.165, -0.26, 0.15, 0.13, -0.105),
    (0.22, 0.23, -0.27, 0.19, 0.16, -0.08),
    (0.50, 0.35, -0.27, 0.28, 0.24, 0.05),
    (0.91, 0.425, -0.27, 0.32, 0.397, 0.07),
    (1.55, 0.465, -0.27, 0.35, 0.43, 0.09),
    (2.13, 0.47, -0.27, 0.36, 0.44, 0.10),
    (2.78, 0.43, -0.24, 0.34, 0.39, 0.10),
    (3.16, 0.39, -0.21, 0.32, 0.34, 0.10),
    (3.25, 0.38, -0.20, 0.32, 0.33, 0.12),
    (5, 0.21, -0.12, 0.22, 0.18, 0.10),
    (7.61, 0.065, -0.03, 0.105, 0.05, 0.075),
]
# x, canopy height above rim, aft lean of crown.
CANOPY = [
    (0.50, 0.03, 0),
    (0.65, 0.23, 0.02),
    (0.91, 0.43, 0.05),
    (1.25, 0.53, 0.10),
    (1.55, 0.56, 0.14),
    (2.13, 0.60, 0),
    (2.78, 0.47, 0),
    (3.16, 0.14, 0),
]
DIVISIONS = 32


def interpolate(rows, x, column):
    """Monotone cubic Hermite interpolation, with zero slopes at extrema."""
    xs = [r[0] for r in rows]
    ys = [r[column] for r in rows]
    slopes = [(b - a) / (v - u) for a, b, u, v in zip(ys, ys[1:], xs, xs[1:])]
    tangents = [slopes[0]]
    for a, b in zip(slopes, slopes[1:]):
        tangents.append(0 if a * b <= 0 else 2 * a * b / (a + b))
    tangents.append(slopes[-1])
    i = min(max(bisect_right(xs, x) - 1, 0), len(xs) - 2)
    h = xs[i + 1] - xs[i]
    t = (x - xs[i]) / h
    return (
        (2 * t**3 - 3 * t * t + 1) * ys[i]
        + (t**3 - 2 * t * t + t) * h * tangents[i]
        + (-2 * t**3 + 3 * t * t) * ys[i + 1]
        + (t**3 - t * t) * h * tangents[i + 1]
    )


def build_enclosure(poly, rod):
    knots = sorted({r[0] for r in HULL} | {r[0] for r in CANOPY})
    xs = []
    for a, b in zip(knots, knots[1:]):
        count = max(1, round((b - a) / 0.065)) if a < 3.16 else 1
        xs.extend(a + (b - a) * i / count for i in range(count))
    xs.append(knots[-1])
    lower, upper = [], []
    for x in xs:
        r, z, h, rim, sill = [interpolate(HULL, x, j) for j in range(1, 6)]
        ring = [(x, -rim, sill)]
        # Keep the six original belly facets aft of the nose. Subdivision alone
        # must not erase the real lower-shell chines seen in the photographs.
        for i in range(25):
            t = i / 4
            j = min(int(t), 5)
            f = t - j
            a, b = pi + j * pi / 6, pi + (j + 1) * pi / 6
            fac_y = (1 - f) * cos(a) + f * cos(b)
            fac_z = (1 - f) * sin(a) + f * sin(b)
            blend = max(0, 1 - x / 0.5)
            angle = pi + i * pi / 24
            ring.append(
                (
                    x,
                    r * ((1 - blend) * fac_y + blend * cos(angle)),
                    z + h * ((1 - blend) * fac_z + blend * sin(angle)),
                )
            )
        ring.append((x, rim, sill))
        lower.append(ring)
        if x <= 0.5:
            height, lean = 0.01 + 0.02 * x / 0.5, 0
        elif x <= 3.16:
            height, lean = interpolate(CANOPY, x, 1), interpolate(CANOPY, x, 2)
        else:
            height, lean = 0, 0
        upper.append(
            [
                (
                    x + lean * sin(i * pi / DIVISIONS),
                    rim * cos(i * pi / DIVISIONS),
                    sill + height * sin(i * pi / DIVISIONS),
                )
                for i in range(DIVISIONS + 1)
            ]
        )
    for k, (a, b) in enumerate(zip(lower, lower[1:])):
        for j in range(len(a) - 1):
            poly("fuselage", 0, a[j], a[j + 1], b[j + 1], b[j])
        front = xs[k + 1] <= 0.5
        cabin = xs[k] >= 0.5 and xs[k + 1] <= 3.16
        if front or cabin:
            a, b = upper[k], upper[k + 1]
            for j in range(DIVISIONS):
                fairing = cabin and xs[k] >= 2.13 and 8 <= j < 24
                if front:
                    name = "fuselage"
                elif fairing:
                    name = "raccord-arriere"
                elif xs[k] < 1.55:
                    name = "pare-brise"
                elif j < 8:
                    name = "vitrage-droit"
                elif j >= 24:
                    name = "vitrage-gauche"
                else:
                    name = "verriere"
                m = 0 if front or fairing else 4
                poly(name, m, a[j], a[j + 1], b[j + 1])
                poly(name, m, a[j], b[j + 1], b[j])
        else:
            poly("fuselage", 0, a[-1], a[0], b[0], b[-1])
    # Nose cap uses exactly the subdivided upper boundary; tail stays faceted.
    poly("fuselage", 0, *reversed(lower[0] + upper[0][1:-1]))
    poly("fuselage", 0, *lower[-1])
    rear = min(range(len(xs)), key=lambda i: abs(xs[i] - 3.16))
    poly("raccord-arriere", 0, *upper[rear])
    cabin_ids = [i for i, x in enumerate(xs) if 0.5 <= x <= 3.16]
    for k in cabin_ids[:-1]:
        for j in (0, DIVISIONS):
            rod("bordures-cockpit", 0, upper[k][j], upper[k + 1][j], 0.018)
    # No extra transverse bar halfway across the forward windscreen.
    for x in (0.5, 1.55, 2.13, 3.16):
        k = min(range(len(xs)), key=lambda i: abs(xs[i] - x))
        for a, b in zip(upper[k], upper[k][1:]):
            rod("arceaux", 0, a, b, 0.016)
    for k in cabin_ids[:-1]:
        if xs[k] >= 1.55:
            for j in (8, 24):
                rod("longerons-verriere", 0, upper[k][j], upper[k + 1][j], 0.010)
    for side in (-1, 1):
        selected = [row for row in HULL if 1.55 <= row[0] <= 2.78]
        line = [
            (x, side * (r * (1 + cos(pi / 6)) / 2 + 0.002), z - h * 0.25)
            for x, r, z, h, rim, sill in selected
        ]
        first, last = selected[0], selected[-1]
        contour = [(first[0], side * (first[4] + 0.002), first[5])] + line
        contour += [(last[0], side * (last[4] + 0.002), last[5])]
        for a, b in zip(contour, contour[1:]):
            rod("contour-porte" + str(side), 3, a, b, 0.0025)
    return HULL

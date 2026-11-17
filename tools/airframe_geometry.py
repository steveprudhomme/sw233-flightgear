"""VIS-05b/c estimated curved enclosure; no changes to aerodynamic geometry."""

from bisect import bisect_right
from math import cos, pi, sin

# x, lower half-width, lower centre, lower height, rim half-width, sill.
# Model estimates. A smaller sampling interval is not increased measurement accuracy.
HULL = [
    (0, 0.008, -0.12, 0.008, 0.008, -0.12),
    (0.04, 0.105, -0.15, 0.11, 0.08, -0.03),
    (0.10, 0.165, -0.20, 0.15, 0.13, 0.035),
    (0.22, 0.25, -0.22, 0.20, 0.20, 0.09),
    (0.50, 0.35, -0.25, 0.28, 0.30, 0.12),
    (0.70, 0.40, -0.26, 0.30, 0.36, 0.12),
    (0.91, 0.425, -0.27, 0.32, 0.397, 0.12),
    (1.55, 0.465, -0.27, 0.35, 0.43, 0.12),
    (2.13, 0.47, -0.27, 0.36, 0.44, 0.13),
    (2.78, 0.43, -0.24, 0.34, 0.39, 0.13),
    (3.16, 0.39, -0.21, 0.32, 0.34, 0.13),
    (3.25, 0.38, -0.20, 0.32, 0.33, 0.12),
    (5, 0.21, -0.12, 0.22, 0.18, 0.10),
    (7.61, 0.065, -0.03, 0.105, 0.05, 0.075),
]
# x, height above rim, aft lean of crown. Estimated silhouette, not surveyed dimensions.
NOSE = [
    (0, 0.008, 0),
    (0.04, 0.04, 0),
    (0.10, 0.07, 0),
    (0.22, 0.13, 0),
    (0.50, 0.16, 0),
    (0.70, 0.14, 0),
]
CANOPY = [
    (0.70, 0.14, 0),
    (0.91, 0.37, 0.05),
    (1.25, 0.52, 0.10),
    (1.55, 0.56, 0.14),
    (2.13, 0.58, 0),
    (2.78, 0.57, 0),
    (3.16, 0.54, 0),
]
FAIRING = [(3.16, 0.54, 0), (3.56, 0.50, 0), (4.20, 0.25, 0), (5, 0, 0)]
CABIN_START = 0.70
CABIN_END = 3.16
FRAME_MATERIAL = 14
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
    knots = sorted({r[0] for rows in (HULL, NOSE, CANOPY, FAIRING) for r in rows})
    xs = []
    for a, b in zip(knots, knots[1:]):
        count = max(1, round((b - a) / 0.065)) if a < 5 else 1
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
        if x <= CABIN_START:
            height, lean = interpolate(NOSE, x, 1), 0
        elif x <= CABIN_END:
            height, lean = interpolate(CANOPY, x, 1), interpolate(CANOPY, x, 2)
        elif x <= 5:
            height, lean = interpolate(FAIRING, x, 1), 0
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
        front = xs[k + 1] <= CABIN_START
        cabin = xs[k] >= CABIN_START and xs[k + 1] <= CABIN_END
        a, b = upper[k], upper[k + 1]
        for j in range(DIVISIONS):
            fairing = CABIN_END <= xs[k] < 5
            if fairing:
                name = "raccord-arriere"
            elif front or not cabin:
                name = "fuselage"
            elif xs[k] < 1.55:
                name = "pare-brise"
            elif j < 8:
                name = "vitrage-droit"
            elif j >= 24:
                name = "vitrage-gauche"
            else:
                name = "verriere"
            m = 0 if name in ("fuselage", "raccord-arriere") else 4
            poly(name, m, a[j], a[j + 1], b[j + 1])
            poly(name, m, a[j], b[j + 1], b[j])
    # Upper and lower boundaries share every cap edge, including the flat tail deck.
    poly("fuselage", 0, *reversed(lower[0] + upper[0][1:-1]))
    poly("fuselage", 0, *(lower[-1] + upper[-1][1:-1]))
    cabin_ids = [i for i, x in enumerate(xs) if CABIN_START <= x <= CABIN_END]

    def trim(name, a, b, radius, moving=False):
        # Rubber bead behind the blue metal frame; offsets are model estimates.
        def back(p):
            return (p[0] - 0.016, p[1], p[2])
        rod("joint-mobile" if moving else "joints-verriere",
            3, back(a), back(b), radius + 0.004)
        rod("cadre-mobile" if moving else name, FRAME_MATERIAL, a, b, radius)

    for k in cabin_ids[:-1]:
        for j in (0, DIVISIONS):
            trim("bordures-cockpit", upper[k][j], upper[k + 1][j], 0.014, xs[k] < 1.55)
    for x in (CABIN_START, 1.55, 2.13, CABIN_END):
        k = min(range(len(xs)), key=lambda i: abs(xs[i] - x))
        for a, b in zip(upper[k], upper[k][1:]):
            trim("arceaux", a, b, 0.014, x <= 1.55)
        for p in upper[k][::4]:
            rod(
                "vis-mobiles" if x <= 1.55 else "fixations-cadres",
                9,
                (p[0] + 0.012, p[1], p[2]),
                (p[0] + 0.019, p[1], p[2]),
                0.0035,
            )
    for k in cabin_ids[:-1]:
        if xs[k] >= 1.55:
            for j in (8, 24):
                rod("longerons-verriere", FRAME_MATERIAL, upper[k][j], upper[k + 1][j], 0.010)
    # Right-hand latch; the moving group carries it with the front canopy.
    latch = [
        (1.44, 0.445, 0.145),
        (1.46, 0.472, 0.17),
        (1.54, 0.472, 0.17),
        (1.56, 0.445, 0.145),
    ]
    for a, b in zip(latch, latch[1:]):
        rod("poignee-verriere", 11, a, b, 0.006)
    # Two estimated hinge barrels on the left rim, aligned with the animation axis.
    for x in (0.83, 1.43):
        y = -0.36 - (x - 0.70) * 0.07 / 0.85
        rod("charnieres-fixes", 9, (x - 0.025, y, 0.12),
            (x + 0.025, y - 0.05 * 0.07 / 0.85, 0.12), 0.012)
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

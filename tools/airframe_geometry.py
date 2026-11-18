"""VIS-05b/c estimated curved enclosure; no changes to aerodynamic geometry."""

from bisect import bisect_right
from math import cos, exp, pi, sin

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
FAIRING = [(2.49, 0.57, 0), (3.514, 0.50, 0), (4.20, 0.25, 0), (5, 0, 0)]
CABIN_START = 0.70
CABIN_END = 2.49
FRAME_MATERIAL = 14
DIVISIONS = 32
ROOT_Y, ROOT_X, ROOT_CHORD, ROOT_Z = 0.44, 1.99, 1.524, 0.74
WING_PROFILE = ((0, 0), (0.09, 0.054), (0.3, 0.072), (0.72, 0.040),
                (1, 0.002), (0.68, -0.028), (0.19, -0.038))


def wing_roof(x):
    """Same piecewise-linear top contour as the current wing root, not an airfoil claim."""
    f = max(0, min(1, (x - ROOT_X) / ROOT_CHORD))
    for (a, za), (b, zb) in zip(WING_PROFILE[:4], WING_PROFILE[1:5]):
        if f <= b:
            return ROOT_Z + ROOT_CHORD * (za + (zb - za) * (f - a) / (b - a))
    return ROOT_Z + ROOT_CHORD * 0.002


def root_fit(x, ring, rim, sill):
    """Blend the front fixed panes into a roof touching both wing-root upper edges."""
    blend = min(1, max(0, (x - 1.55) / (ROOT_X - 1.55)),
                max(0, (4.20 - x) / (4.20 - (ROOT_X + ROOT_CHORD))))
    blend = blend * blend * (3 - 2 * blend)
    result = []
    for i, (px, y, z) in enumerate(ring):
        if 8 <= i <= 24:
            ny = ROOT_Y * cos(i * pi / DIVISIONS) / cos(pi / 4)
            nz = wing_roof(x) + 0.018 * (1 - (ny / ROOT_Y) ** 2)
        else:
            t = min(i, DIVISIONS - i) / 8
            ny = (rim * (1 - t) + ROOT_Y * t) * (1 if i < 8 else -1)
            nz = sill * (1 - t) + wing_roof(x) * t
        result.append((px * (1 - blend) + x * blend,
                       y * (1 - blend) + ny * blend, z * (1 - blend) + nz * blend))
    return result


def rear_back_x(y, z):
    # Recesses for the torso, shoulders and head; estimated from DET-02/06.
    return (2.42 + 0.045 * exp(-(y / 0.22) ** 4 - ((z - 0.10) / 0.30) ** 4)
            + 0.065 * exp(-(y / 0.13) ** 4 - ((z - 0.57) / 0.18) ** 4))


def build_root_details(poly, rod):
    stations = sorted({ROOT_X + ROOT_CHORD * i / 48 for i in range(49)}
                      | {ROOT_X + ROOT_CHORD * f for f, _ in WING_PROFILE[:5]})
    for side in (-1, 1):
        # Grey root end cap, visible from inside the cabin, never a yellow open cut.
        ring = [(ROOT_X + ROOT_CHORD * f, side * ROOT_Y, ROOT_Z + ROOT_CHORD * h)
                for f, h in WING_PROFILE]
        center = (ROOT_X + ROOT_CHORD * 0.40, side * ROOT_Y, ROOT_Z)
        for a, b in zip(ring, ring[1:] + ring[:1]):
            poly('habillage-racine' + str(side), 15, center,
                 *( (b, a) if side < 0 else (a, b) ))
        # A narrow blue cover follows the exact upper-root contour.
        for a, b in zip(stations, stations[1:]):
            def edge(x, y):
                return (x, side * y, wing_roof(x) + 0.018 * (1 - (y / ROOT_Y) ** 2) + 0.001)
            poly('jonction-bleue' + str(side), FRAME_MATERIAL,
                 edge(a, ROOT_Y), edge(b, ROOT_Y), edge(b, ROOT_Y - 0.026),
                 edge(a, ROOT_Y - 0.026))
    ys = sorted({-0.33 + 0.66 * i / 32 for i in range(33)} | {-0.065, 0.065})
    zs = sorted({-0.19 + 1.01 * i / 48 for i in range(49)} | {0.20, 0.265})
    def point(y, z):
        x = rear_back_x(y, z)
        if z > 0.70:
            roof = wing_roof(x) + 0.018 * (1 - (y / ROOT_Y) ** 2) - 0.004
            z += (z - 0.70) / 0.12 * (roof - 0.82)
        return (x, y, z)
    for a, b in zip(ys, ys[1:]):
        for c, d in zip(zs, zs[1:]):
            if a >= -0.065 and b <= 0.065 and c >= 0.20 and d <= 0.265:
                continue  # Actual opening for the belt; no invented grille.
            p, q, r, t = point(a, c), point(b, c), point(b, d), point(a, d)
            poly('dossier-arriere-moule', 15, p, r, q)
            poly('dossier-arriere-moule', 15, p, t, r)
    arc = [(0.065 * cos(i * pi / 32), 0.20 + 0.065 * sin(i * pi / 32))
           for i in range(33)]
    for (a, b), (c, d) in zip(arc, arc[1:]):
        poly('dossier-arriere-moule', 15,
             point(a, 0.265), point(c, 0.265), point(c, d), point(a, b))
    # Dark recess, not a claimed reproduction of the hidden belt anchor.
    poly('passage-sangle-demi-lune', 3,
         *[(rear_back_x(y, z) + 0.008, y, z) for y, z in arc])
    strap = [(2.46, 0.215), (2.43, 0.16), (2.38, 0.06), (2.33, -0.10)]
    for (x, z), (nx, nz) in zip(strap, strap[1:]):
        poly('sangle-dossier-arriere', 8,
             (x, -0.023, z), (x, 0.023, z), (nx, 0.023, nz), (nx, -0.023, nz))
    # Left root opening described by the maintainer. Function and size unconfirmed.
    cx, cz, radius = 2.23, 0.755, 0.032
    circle = [(cx + radius * cos(i * pi / 20), -ROOT_Y + 0.002,
               cz + radius * sin(i * pi / 20)) for i in range(40)]
    poly('ouverture-racine-gauche', 3, *circle)
    for a, b in zip(circle, circle[1:] + circle[:1]):
        rod('bord-ouverture-gauche', 15, a, b, 0.003)
    for i in range(-3, 4):
        v = i * 0.007
        reach = (radius * radius - v * v) ** 0.5
        rod('grille-racine-gauche', 2, (cx - reach, -ROOT_Y + 0.004, cz + v),
            (cx + reach, -ROOT_Y + 0.004, cz + v), 0.001)
        rod('grille-racine-gauche', 2, (cx + v, -ROOT_Y + 0.004, cz - reach),
            (cx + v, -ROOT_Y + 0.004, cz + reach), 0.001)
    for y in (-0.29, 0.29):
        for z in (-0.14, 0.77):
            x = rear_back_x(y, z)
            rod('vis-dossier-arriere', 9, (x - 0.006, y, z), (x, y, z), 0.006)



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
    knots = sorted({r[0] for rows in (HULL, NOSE, CANOPY, FAIRING) for r in rows}
                   | {ROOT_X + ROOT_CHORD * f for f, _ in WING_PROFILE[:5]})
    knots = sorted({round(x, 8) for x in knots})
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
        if x > 1.55:
            upper[-1] = root_fit(x, upper[-1], rim, sill)
        if CABIN_START < x < ROOT_X:
            # One continuous crown curve, with a gentle peak before the wing junction.
            t = (x - CABIN_START) / (ROOT_X - CABIN_START)
            end = wing_roof(ROOT_X) + 0.018
            crown = 0.26 + (end - 0.26) * (2 * t - t * t) + 0.55 * t * t * (1 - t)
            delta = crown - upper[-1][DIVISIONS // 2][2]
            upper[-1] = [(px, y, z + delta * sin(i * pi / DIVISIONS))
                         for i, (px, y, z) in enumerate(upper[-1])]
        if x >= ROOT_X + ROOT_CHORD - 1e-8:
            # Straight aft silhouette; retain the section shape and its sill edges.
            start = ROOT_X + ROOT_CHORD
            start_z = wing_roof(start) + 0.018
            end_x, end_z = HULL[-1][0], HULL[-1][5]
            crown = start_z + (end_z - start_z) * (x - start) / (end_x - start)
            old_height = upper[-1][DIVISIONS // 2][2] - sill
            upper[-1] = [
                (px, y, sill + (crown - sill) *
                 ((pz - sill) / old_height if old_height > 1e-8
                  else sin(i * pi / DIVISIONS)))
                for i, (px, y, pz) in enumerate(upper[-1])]
        # Inclined rear rim: the sill is forward of the roof junction.
        if CABIN_START < x < CABIN_END:
            span = ROOT_X - CABIN_START if x <= ROOT_X else CABIN_END - ROOT_X
            t = (x - CABIN_START) / span if x <= ROOT_X else (CABIN_END - x) / span
            shift = 0.15 * (t * t * (3 - 2 * t))
            lower[-1] = [(px - shift, y, z) for px, y, z in lower[-1]]
            upper[-1] = [(px - shift * max(0, 1 - min(i, DIVISIONS - i) / 8), y, z)
                         for i, (px, y, z) in enumerate(upper[-1])]
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
            elif xs[k] < ROOT_X:
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
            trim("bordures-cockpit", upper[k][j], upper[k + 1][j], 0.014, xs[k] < ROOT_X)
    for x in (CABIN_START, ROOT_X, CABIN_END):
        k = min(range(len(xs)), key=lambda i: abs(xs[i] - x))
        for a, b in zip(upper[k], upper[k][1:]):
            trim("arceaux", a, b, 0.014, x <= ROOT_X)
        for p in upper[k][::4]:
            rod(
                "vis-mobiles" if x <= ROOT_X else "fixations-cadres",
                9,
                (p[0] + 0.012, p[1], p[2]),
                (p[0] + 0.019, p[1], p[2]),
                0.0035,
            )
    for k in cabin_ids[:-1]:
        if xs[k] >= ROOT_X:
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
    for x in (0.83, 1.87):
        y = -0.36 - (x - 0.70) * 0.08 / 1.29
        rod("charnieres-fixes", 9, (x - 0.025, y, 0.12),
            (x + 0.025, y - 0.05 * 0.08 / 1.29, 0.12), 0.012)
    for side in (-1, 1):
        selected = [(x, *[interpolate(HULL, x, i) for i in range(1, 6)])
                    for x in (ROOT_X - 0.15, 2.13, CABIN_END)]
        line = [
            (x, side * (r * (1 + cos(pi / 6)) / 2 + 0.002), z - h * 0.25)
            for x, r, z, h, rim, sill in selected
        ]
        first, last = selected[0], selected[-1]
        contour = [(first[0], side * (first[4] + 0.002), first[5])] + line
        contour += [(last[0], side * (last[4] + 0.002), last[5])]
        for a, b in zip(contour, contour[1:]):
            rod("contour-porte" + str(side), 3, a, b, 0.0025)
    build_root_details(poly, rod)
    return HULL

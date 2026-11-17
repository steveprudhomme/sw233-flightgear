# 21 — Deux personnages dans le cockpit

Le projet possède deux personnages originaux : **Rodolphe Pagé**, combinaison bleue au siège avant, et **Roméo Vachon**, combinaison verte au siège arrière. Le second rôle est celui d’un officier dans la fiction du projet. Ces personnages ne sont pas des portraits. Aucun grade, qualification réelle ou statut militaire individuel n’est affirmé.

## Retrouver et reconstruire le travail

**Repère de reconstruction : `tools/crew.py`, fonction `finish_crew(models: Path)`.** Ce fichier contient les dimensions, la construction des volumes, les couleurs, le dessin des étiquettes et les conditions d’affichage. Les fichiers AC3D, XML et PNG sont des résultats générés, pas les sources à retoucher.

Depuis la racine du dépôt :

```powershell
python tools/crew.py build/personnages-essai/Models
```

L’environnement Python doit disposer de Pillow. Le constructeur du paquet appelle `finish_crew` avec son répertoire `Models`; le modèle principal charge `crew.xml` à l’origine commune de l’avion. Aucun décalage supplémentaire n’est requis. Le générateur ne lit ni ne modifie les masses du modèle de vol.

Trois fichiers sont produits : `crew.ac` (géométrie), `crew-atlas.png` (atlas original 1024 × 1024) et `crew.xml` (affichage conditionnel). La graine de tissu est fixe, 233. Tous les indices et les coordonnées UV sont contrôlés pendant la construction. La fonction retourne le nombre de sommets, triangles et objets et les bornes en coordonnées de construction.

## Comment les corps sont construits

Un personnage n’est pas une collection de cylindres droits. Le torse utilise sept anneaux elliptiques : bassin, taille, poitrine, épaules et col ont des largeurs distinctes. Chaque manche forme un seul tube courbé à neuf anneaux partagés, depuis une épaule qui pénètre dans le torse jusqu’au poignet. Il n’y a plus de coupure au coude. Les jambes sont des sections orientées à sept anneaux, renflées et amincies aux extrémités; les genoux raccordent les segments. Les mollets descendent vers des bottes avec semelles, dessus et lacets. Les mains ont un volume de paume, un pouce et quatre doigts séparés. Le visage possède mâchoire, nez, oreilles, yeux, sourcils, bouche et cheveux discrets. Le menton, la mâchoire, les joues et le crâne appartiennent à une seule surface à huit anneaux, pour éviter une coupure visuelle entre la bouche et le visage.

Les combinaisons ont des poches de poitrine et leur fermeture, une fermeture centrale et sa tirette, un col, des poignets, des coutures, des plis aux coudes et genoux. Le tissu est peint procéduralement avec un grain et une trame très fins. Un harnais d’épaules et une ceinture ventrale avec boucle et réglages se superposent à chaque combinaison. Leur cheminement est une représentation artistique, pas une preuve d’installation ou de certification.

Les noms `R. PAGÉ` et `R. VACHON` sont placés sur le devant droit au-dessus de la poche. Le patch droit porte explicitement **PROJET / CEC / ST-JEAN**; le patch gauche est un dessin original d’aéronef avec **SW233**. Aucun de ces dessins ne reproduit un écusson officiel. Des ailes fictives peuvent apparaître à gauche de la poitrine uniquement avec l’option spécifique; elles portent le mot **FICTIF**. Il n’y a pas d’insigne de grade.

## Dimensions et repères

Les coordonnées de construction sont en mètres : **x vers l’arrière, y vers la droite, z vers le haut**. L’export AC3D transforme chaque point `(x, y, z)` en `(x, z, -y)`. Les positions des sièges sont x = 1,52 et 2,39. La tête avant culmine à environ z = 0,558, sous le plafond fourni. La demi-largeur maximale des personnages est 0,247 m.

Ces dimensions sont des estimations artistiques adaptées au cockpit disponible. Elles ne résultent pas d’une campagne de mesures humaines ou d’un relevé du harnais. Pour changer la posture, modifier `_person`; pour changer la résolution, modifier `loft`, `ellipsoid`, `limb` ou `sleeve`. La tête avec son cou, le corps et les ailes ont des groupes de noms distincts. Les coutures ne doivent pas être agrandies comme de gros cordages.

## Affichage dans FlightGear

Chaque groupe demande `/sim/sw233/visuals/crew = true` et la masse correspondante strictement positive :

- Avant : `/fdm/jsbsim/inertia/pointmass-weight-lbs`.
- Arrière : `/fdm/jsbsim/inertia/pointmass-weight-lbs[1]`.

La tête et le cou avant demandent aussi `/sim/current-view/view-number != 0`. Le corps reste visible en vue pilote; la tête arrière reste visible. Cela évite que les yeux de la caméra se retrouvent à l’intérieur du visage avant. Les ailes demandent en plus `/sim/sw233/visuals/wings = true`; cette option est désactivée par défaut dans la configuration du projet.

En essai `fdm=null`, fournir explicitement des masses positives aux propriétés de test pour voir les personnes. En l’absence de ces propriétés, les personnages restent cachés. Le générateur ne crée pas de valeurs de remplacement et ne change aucune masse.

## Vérification locale

Génération isolée réussie : **178 objets, 24 716 sommets et 45 896 triangles**, un atlas 1024 × 1024. Bornes communes : x = 0,881 à 2,545; y = −0,247 à +0,247; z = −0,464 à +0,558 m. Les UV restent dans chaque tuile, avec une marge de quatre pixels pour limiter les bavures entre couleurs. Les surfaces sont lissées et à double face, notamment pour les petites pièces de tissu.

Ces vérifications portent sur les fichiers et la construction; les captures FlightGear et le contrôle final des intersections cockpit relèvent de l’essai du paquet complet. Les modèles n’animent pas encore la respiration, les doigts ou le suivi des commandes. Il faut distinguer cette limite des détails déjà présents dans la géométrie.

Voir [les références et limites de conception](../references/equipage-conception.md).

## Essais dans le simulateur

Les premières captures natives ont révélé deux défauts précis : le cou restait visible comme une boule lorsqu’on regardait vers le bas en vue pilote, et les raccords du visage et des bras semblaient coupés en regardant le siège arrière. La recette corrigée classe le cou avec la tête, construit chaque manche d’un seul tenant et utilise une seule surface pour les joues et la mâchoire. Les épaules pénètrent dans le torse, au lieu de seulement toucher son bord.

Les images de la séance **visuals-39** permettent de refaire le contrôle. En vue pilote, regarde vers le bas : le corps reste présent, mais le cou et la tête avant doivent disparaître. Regarde ensuite le personnage arrière : le contour de ses épaules, coudes et joues doit rester continu. La tête arrière reste visible. Ce contrôle vérifie le rendu dans FlightGear, pas des mensurations réelles.

![Vue pilote vers le bas : corps conservé, tête et cou avant masqués](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/crew-pilot.jpg)

![Vue du personnage arrière : contrôle des raccords du visage, des épaules et des manches](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/crew-rear.jpg)

## Ton atelier, une petite étape à la fois

1. **Prépare un dossier vide.** La commande ci-dessus fabrique les trois fichiers dans
   `build/personnages-essai/Models`. Tu peux recommencer après avoir changé la recette :
   ce dossier sert aux résultats, pas à tes sources.
2. **Dessine un personnage de face et de profil.** Marque le siège, les genoux,
   les épaules et le sommet de la tête. Ici on utilise les sièges déjà construits :
   2,39 − 1,52 = 0,87 m séparent leurs repères. Ce ne sont pas deux mesures nouvelles
   prises sur le vrai planeur.
3. **Fais le torse avec des anneaux.** Imagine des cerceaux empilés. Un anneau large
   fait les épaules, un plus étroit fait la taille. Relier leurs bords produit une peau.
   Dans `_person`, les nombres de `mesh.loft` décrivent ces anneaux. Change une seule
   largeur, reconstruis et regarde le dessin de profil et celui de face dans l'atlas.
4. **Ajoute les membres.** Chaque manche suit un trajet épaule–coude–poignet.
   Un seul tube continu évite un trou au coude. Le bout de l'épaule entre un peu
   dans le torse. C'est comme emboîter deux pièces : des pièces seulement posées
   bord contre bord peuvent laisser apparaître une fente.
5. **Habille le corps.** Une poche est une petite surface devant le tissu. Une couture
   est un tube très fin. Notre couture de 0,0018 m fait 1,8 mm de rayon.
   C'est un choix pour la voir dans le simulateur, pas une couture mesurée.
6. **Peins les noms.** `_atlas` remplit une image divisée en petites cases.
   Les coordonnées UV disent quelle case habille chaque pièce. Vérifie le É de PAGÉ
   et ne retourne pas la case comme dans un miroir.
7. **Pose le harnais par-dessus.** Regarde les bretelles et la boucle de face,
   puis de côté. Les mains sont posées, elles ne suivent pas encore le manche.
8. **Essaie dans FlightGear.** Au sol, ouvre le menu Occupants et centrage.
   Une masse nulle cache la personne de cette place. Le menu Équipage cache les deux
   personnes sans enlever leur masse. Cette différence permet de comparer l'image
   sans changer le chargement du planeur. En vue pilote, regarde vers le bas :
   tu dois voir le corps, mais pas un cou flottant devant toi.

![Torse construit avec des anneaux, dessin de contrôle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/front-torso.png)

[Atlas de toutes les pièces](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/atlas.zip) :
ouvre `index.html` après décompression. Cherche les noms qui commencent par `front-`
pour le cadet, puis `rear-` pour l'officier. Chaque ligne mène au dessin d'une pièce.
Ces dessins montrent la géométrie ; les captures suivantes montrent son rendu réel.

## Recopie la recette complète

Crée le dossier `tools` s’il n’existe pas encore, puis crée le fichier `crew.py` dedans. Copie tout le bloc suivant dans ce fichier, en gardant les espaces au début des lignes. C’est la recette complète utilisée par le paquet, pas un extrait. Ne la colle pas à la fin d’une ancienne version : remplace le contenu du fichier.

Après avoir enregistré, lance la commande indiquée au début de cette fiche avec le chemin d’un dossier de travail. Tu obtiens les trois fichiers du personnage. Les valeurs affichées te permettent de vérifier les nombres d’objets et de triangles. Pour faire un essai de couleur, cherche la table `TILES` au début de la recette; change une seule couleur, reconstruis, puis compare. Les trois nombres d’une couleur représentent le rouge, le vert et le bleu, chacun entre 0 et 255.

<!-- atelier-fichier: tools/crew.py -->
```python
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
            draw.rectangle((8, 65, 247, 190), outline="#b8b7a2", width=3)
            font = _label_font()
            draw.text((128, 128), label, anchor="mm", font=font, fill="#e0dfc4")
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
    def __init__(self):
        self.parts = []

    def add(self, name, material, vertices, faces, uvs=None, category="body"):
        assert all(len(f) == 3 for f in faces)
        assert all(0 <= i < len(vertices) for f in faces for i in f)
        if uvs is None:
            uvs = [(0.5, 0.5)] * len(vertices)
        assert all(0 <= u <= 1 and 0 <= v <= 1 for u, v in uvs)
        self.parts.append((name, material, vertices, faces, uvs, category))

    def loft(self, name, material, rings, category="body", segments=24):
        """Horizontal elliptical rings: (x, y, z, radius_x, radius_y)."""
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
        for j in range(13):
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
        n = 16
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
        count = 24
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

    def patch(self, name, material, corners, category="body"):
        # Corners: bottom left, bottom right, top right, top left as viewed outside.
        self.add(
            name,
            material,
            corners,
            [(0, 1, 2), (0, 2, 3)],
            [(0, 0), (1, 0), (1, 1), (0, 1)],
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
            tile = TILES[mat][0]
            tx = tile % 4
            ty = tile // 4
            for face in faces:
                lines += ["SURF 0x30", "mat 0", "refs 3"]
                for vertex in face:
                    u, v = uv[vertex]
                    # Four-pixel gutter, AC uses bottom-left texture origin.
                    u = (tx * 256 + 4 + u * 248) / 1024
                    v = 1 - (ty * 256 + 252 - v * 248) / 1024
                    lines.append(f"{vertex} {u:.7f} {v:.7f}")
            lines.append("kids 0")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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

    def patch(label, mat, points, cat="body"):
        mesh.patch(prefix + "-" + label, mat, [(seat + x, y, z) for x, y, z in points], cat)

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
        patch(
            s + "-shoulder-harness",
            "strap",
            [
                (-0.084, sign * 0.025, -0.068),
                (-0.084, sign * 0.055, -0.068),
                (-0.060, sign * 0.133, 0.265),
                (-0.060, sign * 0.103, 0.265),
            ],
        )
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
        e(s + "-harness-adjuster", "metal", (-0.079, sign * 0.085, 0.110), (0.008, 0.021, 0.023))
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
            (-0.060, 0.057, 0.177),
            (-0.060, 0.139, 0.177),
            (-0.060, 0.139, 0.207),
            (-0.060, 0.057, 0.207),
        ],
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
    )


def finish_crew(models: Path):
    """Write crew.ac, crew.xml, crew-atlas.png; return geometry verification data."""
    models = Path(models)
    models.mkdir(parents=True, exist_ok=True)
    mesh = CrewMesh()
    _person(mesh, "front", 1.52, "blue", 0.438)
    _person(mesh, "rear", 2.39, "green", 0.438)
    _atlas(models / "crew-atlas.png")
    mesh.save(models / "crew.ac")
    root = ET.Element("PropertyList")
    ET.SubElement(root, "path").text = "crew.ac"
    for person in ("front", "rear"):
        suffix = "" if person == "front" else "[1]"
        for category in ("body", "head", "wings"):
            animation = ET.SubElement(root, "animation")
            ET.SubElement(animation, "type").text = "select"
            for name, _, _, _, _, cat in mesh.parts:
                if name.startswith(person + "-") and cat == category:
                    ET.SubElement(animation, "object-name").text = name
            condition = ET.SubElement(ET.SubElement(animation, "condition"), "and")
            ET.SubElement(condition, "property").text = "/sim/sw233/visuals/crew"
            greater = ET.SubElement(condition, "greater-than")
            ET.SubElement(greater, "property").text = (
                "/fdm/jsbsim/inertia/pointmass-weight-lbs" + suffix
            )
            ET.SubElement(greater, "value").text = "0"
            if person == "front" and category == "head":
                different = ET.SubElement(ET.SubElement(condition, "not"), "equals")
                ET.SubElement(different, "property").text = "/sim/current-view/view-number"
                ET.SubElement(different, "value").text = "0"
            if category == "wings":
                ET.SubElement(condition, "property").text = "/sim/sw233/visuals/wings"
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(models / "crew.xml", encoding="utf-8", xml_declaration=True)
    vertices = [v for p in mesh.parts for v in p[2]]
    report = {
        "objects": len(mesh.parts),
        "vertices": len(vertices),
        "triangles": sum(len(p[3]) for p in mesh.parts),
        "construction_bounds": {
            axis: [min(v[i] for v in vertices), max(v[i] for v in vertices)]
            for i, axis in enumerate("xyz")
        },
        "texture": [1024, 1024],
        "uv_checked": True,
    }
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("models", type=Path)
    print(json.dumps(finish_crew(parser.parse_args().models), indent=2))
```

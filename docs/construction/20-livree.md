# 20 — Peindre le planeur et vérifier les UV

## 1. Ce que l'on sait, ce que l'on dessine

Notre livrée **C-FYLP reste provisoire**. Les couleurs, les bandes et la position des lettres sont des choix de dessin. Le lot 40 ajoute la peinture jaune unie sur les ailes, les spoilers et les empennages ; il n'invente ni logo ni inscription sous les ailes. Le [registre des références](../references/livree-recherche.md) sépare les éléments confirmés, estimés et inconnus. La photographie légendée C-FYLP du site 155 est une vue depuis le cockpit : elle ne prouve pas la peinture extérieure actuelle.

Imagine deux autocollants possibles pour chaque pièce : un autocollant de peinture, et un autocollant à carreaux pour vérifier le dessin. On ne les affiche jamais en même temps. Quand on les cache tous les deux, les matériaux de base réapparaissent.

## 2. Les pièces et les axes

Le générateur lit la copie de `sw233.ac` dans le paquet. Le fichier source reste intact. Il traite 10 objets de base : le fuselage, les deux ailes, les deux spoilers, les deux stabilisateurs, les deux profondeurs et la dérive. Une plaque très fine doit être peinte des deux côtés : nous créons une face extérieure dessus et une face extérieure dessous. Les ailes possèdent déjà une épaisseur ; leurs faces sont classées dessus, dessous et bout.

Le résultat contient **23 surfaces de peinture et 23 surfaces de grille**, soit 46 objets dans `livery.ac`. Les cartes utilisent neuf dispositions UV et produisent 18 images PNG. `livery-report.json` résume le résultat. Toutes les images sont originales, dessinées par Python et Pillow.

Les axes AC3D sont `(x vers la queue, y vers le haut, z vers la gauche)`. Nos dessins de construction utilisent `(x vers la queue, y vers la droite, z vers le haut)`. Pour passer d'un point du dessin au fichier, transforme `(x,y,z)` en `(x,z,-y)`.

## 3. Mettre une règle sur la texture

Une texture est un rectangle. `u` indique la position horizontale de 0 à 1 ; `v` indique la position verticale de 0 à 1. Le coin inférieur gauche est `(0,0)`. Pour transformer une longueur en proportion, on soustrait son début et on divise par sa largeur : `u=(position-début)/(fin-début)`.

Voici les limites **mesurées dans notre maillage numérique**, et non sur l'appareil réel :

| Famille | Étendue dans les axes AC3D | Carte |
| --- | --- | --- |
| Fuselage | x de 0 à 7,61 m ; y de -0,63 à 0,12 m | 4096 × 512 px par flanc |
| Deux ailes | x de 1,99 à 3,56 m ; z de -7,7724 à 7,7724 m | 4096 × 512 px pour le dessus ; autre carte pour le dessous |
| Bouts des ailes | x de 1,99 à 3,56 m ; y de 0,68034 à 0,99472 m | 1024 × 256 px |
| Stabilisateurs et profondeurs | x de 6,85 à 7,79 m ; z de -1,93 à 1,93 m | 2048 × 512 px par côté |
| Dérive | x de 6,5 à 7,8486 m ; y de 0,04 à 1,42 m | 1024 × 1024 px par flanc |
| Spoilers | Ils réutilisent la carte complète des ailes | Même repère que l'aile, même quand ils tournent |

Sur le fuselage gauche, `u=x/7,61` et `v=(y+0,63)/0,75`. Au milieu de la longueur, x=3,805 donne u=0,5. Pillow compte ses lignes depuis le haut, donc la ligne de l'image vaut `(1-v)×511`. Le dernier pixel d'une ligne large de 4096 pixels porte le numéro 4095 : le premier est zéro.

Pour les ailes vues du dessus, la droite du planeur apparaît à droite de l'image : `u=(-z+7,7724)/15,5448`. Le nez est vers le haut : `v=(3,56-x)/1,57`. Vues du dessous, on inverse l'axe horizontal, donc `u=(z+7,7724)/15,5448`. Les profondeurs et stabilisateurs partagent leur propre règle ; leur séparation à x=7,35 m ne coupe pas la continuité du dessin.

## 4. Des lettres dans le bon sens

Quand on passe à droite du fuselage, le nez change de côté. On utilise `u_droit=1-u_gauche`. Mais il ne faut pas retourner une image portant déjà du texte : les lettres deviendraient des lettres de miroir. Le programme dessine C-FYLP à nouveau, normalement, dans chaque feuille. La dérive possède aussi deux cartes orientées indépendamment, même si sa peinture est unie pour le moment.

La grille porte des numéros de cases et les indications U et V. Sa bordure gauche est verte ; sa bordure basse est rouge. Ces repères asymétriques permettent de voir un retournement que de simples carreaux noirs et blancs pourraient cacher. Les carreaux sont réguliers **dans la texture**, pas nécessairement carrés en mètres sur une surface courbe. Le vieux raccord central du fuselage garde sa projection d'origine ; les nouvelles cartes sont contrôlées pour éviter les faces UV aplaties sur une ligne.

## 5. Remplacer une surface au lieu de superposer deux peaux

Deux surfaces presque au même endroit peuvent scintiller, surtout quand le planeur est loin. Un essai à 100 m a montré ce défaut sous le fuselage. Éloigner arbitrairement la peinture ne résout pas proprement ce problème : cela grossirait la maquette.

La solution est de ne montrer qu'une seule version de chaque surface. Quand la livrée **ou** la grille est active, le modèle principal masque les dix objets sources entièrement remplacés. Lorsque les deux options sont éteintes, il les montre à nouveau. Les nouvelles surfaces utilisent les coordonnées originales exactes : leur déplacement vaut **zéro**.

Avant de les masquer, le programme vérifie la couverture complète. Chaque face originale doit être retrouvée, avec tous ses sommets dans le même ordre circulaire, éventuellement parcouru à l'envers. Il y a 138 faces sources : 87 sur le fuselage, 22 par aile, et une sur chacun des sept objets très fins. Les surfaces fines sont dessinées une fois de chaque côté, ce qui donne 145 faces dans les 23 objets de peinture. Une face manquante provoque une erreur ; compter seulement les sommets ne suffirait pas à détecter un trou.

La coque et les ailes conservent une visibilité à deux faces, comme dans le modèle original. Cela préserve aussi leur apparence depuis l'intérieur. Les plaques très fines utilisent deux faces opposées et chacune n'est visible que de son propre côté : elles peuvent partager exactement les mêmes coordonnées sans être affichées ensemble depuis le même côté.

Le sens des sommets définit la direction de la normale, une flèche perpendiculaire à une face. L'aile gauche d'origine a un ordre inversé par rapport à l'autre aile. Le générateur le remet dans le bon sens uniquement dans la version peinte. Il ne modifie pas le fichier source. Les tests vérifient les normales, la symétrie et l'absence de déplacement.

### Voir le défaut avant et après

Ces deux captures FlightGear utilisent les mêmes réglages de caméra : distance 100 m, champ de vision 10°, orientation de vue 120°, inclinaison 0° et cap du planeur 10°. Le menu visible dans la première image n'intervient pas dans la comparaison du fuselage.

![Avant : motif de concurrence entre deux surfaces sous le fuselage à 100 m](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/surface-before.jpg)

Regarde le ventre bleu du planeur, particulièrement sous le cockpit. Le motif irrégulier de petits traits vient de deux surfaces presque confondues : la carte graphique alterne entre elles. Ce phénomène s'appelle le *z-fighting*. Une capture fixe montre le motif ; elle ne montre pas son clignotement pendant le déplacement de la vue.

![Après : même vue avec une seule version visible de chaque surface](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/surface-after.jpg)

Dans cette vue après correction, le motif dense n'est plus visible et le dessous paraît continu. La correction consiste à masquer l'original entièrement remplacé, sans gonfler le planeur ni déplacer la peinture. L'image reste sombre sous le fuselage et les contours sont encore anguleux : ce contrôle démontre la disparition du défaut observé dans cette vue, pas un rendu parfait sous tous les angles. Il faut aussi vérifier les commandes mobiles et les autres distances.

## 6. Faire tourner la peinture avec les commandes

Une peinture de spoiler ne doit pas rester sur l'aile lorsque le spoiler se lève ! Le programme lit les quatre animations de rotation dans `sw233-model.xml` : deux spoilers et deux profondeurs. Il copie leur propriété, leur axe, leur centre et leur facteur **exactement**, puis remplace seulement les noms d'objets par ceux des peaux.

Ainsi une modification future de l'axe original est reprise à la prochaine génération. Si l'une des quatre rotations manque ou apparaît deux fois, le programme s'arrête au lieu de produire une peau immobile. Les peaux de grille suivent les mêmes rotations que la peinture.

## 7. Construire et choisir la vue

Le constructeur du paquet appelle `finish_livery(models)` après `finish_panel(models)`. Le dossier `models` doit contenir `sw233.ac` **et** `sw233-model.xml`. Le modèle principal garde `<model><path>livery.xml</path></model>`. Aucune deuxième inclusion n'est nécessaire. Le modèle principal doit aussi sélectionner les objets d'origine uniquement lorsque **les deux propriétés sont fausses** : `not (livery or uv-grid)`. Les objets concernés sont `fuselage`, `aile-1`, `aile1`, `aerofrein-1`, `aerofrein1`, `empennage-1`, `empennage1`, `profondeur-1`, `profondeur1` et `derive`. Ce masque est indispensable : garder les originaux visibles recréerait les deux surfaces concurrentes. Les autres pièces, notamment le cockpit, le train et les haubans, restent gérées par leurs règles habituelles.

Pour un essai isolé, crée un nouveau dossier `Models`, copie ces deux fichiers dedans, puis lance `python tools/livery.py CHEMIN_DU_DOSSIER_MODELS`. Modifie `YELLOW`, `BLUE`, les points de `contour` ou les règles `CHARTS`, puis reconstruis le paquet. Ne retouche pas seulement un PNG généré : il serait remplacé à la prochaine construction.

| `/sim/sw233/visuals/livery` | `/sim/sw233/visuals/uv-grid` | Résultat |
| --- | --- | --- |
| false | false | Matériaux de base |
| true | false | Livrée originale provisoire |
| false | true | Grille de contrôle |
| true | true | Grille de contrôle, prioritaire |

La grille est un outil de développement. Elle ne représente aucune décoration de l'appareil réel. Les valeurs par défaut et les commandes de menu appartiennent à la configuration principale.

## 8. Observer dans FlightGear

Les liens suivants sont réservés aux captures du lot 40. Une capture de simulateur prouve l'aspect du modèle à cet instant ; elle ne confirme pas la livrée de l'avion réel.

![Flanc gauche, peinture provisoire](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/livery-left.jpg)

![Flanc droit, peinture provisoire](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/livery-right.jpg)

Lis C-FYLP normalement des deux côtés. Le dessous bleu et le filet doivent rester attachés à la coque. Observe à courte puis à longue distance : aucune zone ne devrait clignoter entre la couleur de base et la nouvelle peinture.

![Ailes et empennages, vue du dessus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/livery-top.png)

![Ailes et empennages, vue du dessous](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/livery-bottom.png)

Regarde les deux faces des ailes et des empennages. Les surfaces unies sont volontaires : nous n'ajoutons pas de faux marquage là où les photographies manquent.

![Grille de contrôle, dessus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/uv-top.png)

![Grille de contrôle, dessous](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/uv-bottom.png)

Les numéros et les bords colorés servent de règle. Vérifie les deux côtés, puis le dessous : une inversion doit correspondre au changement de point de vue, pas à une lettre retournée. La forme des ailes peut étirer les carreaux ; une face devenue entièrement un trait serait une erreur.

![Spoilers déployés avec leur peinture](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/spoilers-open.jpg)

![Dérive, stabilisateurs et profondeurs](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/tail.jpg)

Déploie les spoilers puis rentre-les. Déplace la profondeur dans les deux sens. Observe le dessus, le dessous et la charnière : la peau doit suivre la pièce mobile sans rester suspendue dans l'air. Répète avec la grille, de près puis de loin.

Les contrôles automatiques se lancent avec `python -m unittest discover -s tests -p test_livery_surfaces.py -v`. Ils examinent les indices, les textures, la symétrie, les normales, la couverture complète, les positions exactes, les conditions et les animations. Ils ne remplacent pas ces observations dans FlightGear.

Les vues du [lot 39](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/visuals-39) restent l'archive de la première peau de fuselage. Les captures du lot 40 servent à vérifier l'extension aux nouvelles surfaces.

## 9. Examiner chaque pièce séparément

Télécharge [l'atlas complet du lot 40](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/atlas.zip), décompresse-le et ouvre `index.html`. Chaque image présente trois projections du maillage : profil, dessus et face. Ce sont des **schémas**, pas des photographies ni des captures du simulateur. Les textures, la transparence et les animations n'y apparaissent pas ; les dimensions sont celles du modèle.

L'index donne accès aux 23 surfaces de peinture, aux 182 pièces individuelles des occupants et aux trois vitres des instruments, soit **208 images individuelles**. Les couches de grille UV ne sont pas répétées : elles utilisent les mêmes surfaces. Deux sections optionnelles montrent aussi six groupes LOD détaillés et six groupes LOD simplifiés. Ces 12 images représentent des regroupements des occupants déjà montrés, pas 12 pièces supplémentaires de l'avion. L'atlas contient donc **220 images** au total, avec un inventaire et un rapport JSON.

![Schéma de la surface supérieure de l'aile gauche : profil, dessus et face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/livery-aile-top.png)

Sur ce dessin de `livery-aile-1-top`, retrouve l'étendue de l'aile puis compare-la aux limites de sa carte UV dans le tableau de l'étape 3. Le schéma utilise la couleur du matériau de base, sans charger sa texture jaune ou sa grille. Pour juger les lettres, les bandes ou les carreaux, utilise les captures de l'étape 8 et les essais dans FlightGear.

## Code complet à reconstruire

Le code ci-dessous est celui de `tools/livery.py`. Python et Pillow sont déjà utilisés pour les instruments.

<!-- atelier-fichier: tools/livery.py -->
```python
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
SIZE = (4096, 512)
X_RANGE = (0.0, 7.61)
Y_RANGE = (-0.63, 0.32)  # AC3D vertical coordinate, not construction y.


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
```

# 24 — Reconstruire le nez, la coque et la verrière

**But :** remplacer les grands morceaux droits de l'avant par des courbes plus fines,
puis vérifier que toutes les pièces se touchent encore. Imagine une coque de bateau :
on dessine plusieurs tranches, puis on tend une peau entre elles.

Ce lot42 est une **interprétation de maquette**. Les photographies montrent des formes,
mais ne donnent pas de nouvelles dimensions constructeur. Nous gardons les repères
et les incertitudes de la [fiche23](23-releves-avant.md). La peinture C-FYLP reste provisoire.
Le mécanisme d'ouverture de la verrière sera construit dans un autre atelier.

> **Lecture historique :** les explications et captures ci-dessous racontent le lot42.
> Le bloc de recette complet est maintenu à jour pour reconstruire la version actuelle.
> Les paramètres modifiés, cadres bleus, joints, fixations et nouveau raccord arrière
> sont expliqués dans la [fiche25](25-finitions-avant.md), à lire avant de lancer la recette.

## 1. Préparer et comprendre les références

Relis EXT-02 (profil oblique), EXT-03 (verrière fermée) et DET-03/05 (verrière ouverte)
dans les analyses [extérieur](../references/analyse-exterieur-lot-01.md) et
[détails](../references/analyse-details-lot-02.md). Les originaux restent dans les
références locales ; leurs droits de publication ne sont pas établis.

Sur une feuille, sépare trois observations :

- le nez est arrondi ; une pointe faite de quelques triangles ne suffit pas ;
- le pare-brise est bombé ; son sommet ne doit pas former une longue pente droite ;
- le bas du fuselage possède aussi de vraies cassures : tout arrondir serait une erreur.

Nous n'avons pas mesuré le nez avec les visages, les mains ou les roues de la photo.
La perspective peut les agrandir. Le rapport photographique de la fiche23 aide à
poser une question ; il ne devient pas automatiquement une dimension en mètres.

Avant les modifications, les sous-étapes ont été enregistrées dans le ROADMAP au
commit `14db098`. Le modèle du lot41 sert de témoin. Voici son profil dans FlightGear :

![Profil avant reconstruction](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/avant-nez-profil.png)

## 2. Lire les tranches de la coque

Les axes de notre cahier sont : **x** du nez vers la queue, **y** vers le côté droit,
**z** vers le haut. L'exporteur change ensuite ces axes pour AC3D ; ne les change pas
deux fois ! Une ligne de `HULL` contient six nombres :

| Colonne | Ce qu'elle décrit | Exemple à x = 0,91 m |
|---|---|---|
| x | position de la tranche | 0,91 |
| r | demi-largeur de la partie basse | 0,425 |
| z | hauteur du centre de cette partie basse | −0,27 |
| h | profondeur sous ce centre | 0,32 |
| rim | demi-largeur au bord du cockpit | 0,397 |
| sill | hauteur de ce bord | 0,07 |

À cet endroit, la largeur au bord vaut `2 × 0,397 = 0,794 m` et le point le plus bas
vaut `−0,27 − 0,32 = −0,59 m`. Ces calculs décrivent **notre fichier**, pas une mesure
prise sur un véritable SGS 2-33.

Les grandes tranches à 0,50 ; 0,91 ; 1,55 ; 2,13 ; 2,78 ; 3,16 ; 3,25 ; 5 et
7,61 m conservent leurs valeurs de coque. Deux petites tranches à 0,04 et 0,10 m
et une extrémité moins pincée remplacent le départ trop anguleux. Les valeurs de ces
nouvelles tranches sont des choix artistiques, révisables avec de vraies cotes.

![Coque seule, trois projections du maillage](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-fuselage.png)

## 3. Relier les tranches sans bosses accidentelles

Une règle relie deux points avec un trait droit. Une courbe d'interpolation les relie
plus doucement. `interpolate` utilise une courbe d'Hermite : elle connaît les deux
extrémités et la direction de la courbe à chacune. Lorsque les valeurs changent de
sens, la pente devient nulle. Cela évite d'inventer une bosse au-delà des valeurs choisies.

`build_enclosure` insère des tranches espacées d'environ 6,5 cm dans la zone avant.
Les repères d'origine restent présents. Une tranche du dessous contient les deux
bords du cockpit et 25 points le long du ventre. Après x = 0,50 m, ces points restent
sur les six pans d'origine : ajouter des points ne transforme pas ces pans en ballon.
Près du nez, une transition les rapproche progressivement d'une ellipse.

**Petit essai :** regarde le nez dans le plan de côté, puis dans le plan de face.
Une belle courbe de côté peut encore être trop étroite de face. Il faut toujours
examiner les deux vues avant de déclarer la forme correcte.

## 4. Construire le bombé du pare-brise

`CANOPY` contient la position, la hauteur au-dessus du bord et un décalage vers
l'arrière. Par exemple, à x = 0,91 m, le sommet monte maintenant de **0,43 m** au-dessus
du bord, contre 0,28 m auparavant. À x = 1,55 m, la hauteur passe de 0,52 à **0,56 m**.
Ce sont des hypothèses de forme issues de la comparaison visuelle, pas des relevés physiques.

Chaque arceau suit une demi-ellipse : 32 intervalles donnent 33 points. Sur les bords,
la hauteur ajoutée vaut zéro ; au milieu, elle atteint la hauteur choisie. Le décalage
vers l'arrière suit la même progression. Le bord de coque et le bord de verre réemploient
**exactement les mêmes points**, comme deux pièces de puzzle dessinées avec le même trait.

![Pare-brise seul](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-pare-brise.png)

![Partie supérieure de verrière](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-verriere.png)

![Vitrage droit](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-vitrage-droit.png)

![Vitrage gauche](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-vitrage-gauche.png)

Les petites surfaces sont triangulées pour ne pas demander à quatre points d'une courbe
de former un seul panneau plat. Le raccord arrière reste opaque sous l'aile.

![Raccord arrière opaque](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-raccord-arriere.png)

## 5. Poser les cadres et fermer les raccords

Les arceaux sont placés à 0,50 ; 1,55 ; 2,13 et 3,16 m. L'ancienne barre intermédiaire
à 0,91 m, qui traversait le pare-brise avant, est retirée. Les longerons latéraux
commencent à 1,55 m. Leur disposition reste à comparer aux pièces exactes de C-FYLP.
Les cadres restent jaunes dans ce lot de forme ; leur bleu et leur quincaillerie
appartiennent à la reprise de livrée et au mécanisme d'ouverture.

![Arceaux](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-arceaux.png)

![Bordures du cockpit](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-bordures-cockpit.png)

![Longerons du vitrage](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-longerons-verriere.png)

Les contours des portes sont conservés comme repères. Ils ne sont pas encore des
portes séparées capables de pivoter. Les deux illustrations permettent de les reconnaître :

![Contour de porte gauche](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-contour-porte-1.png)

![Contour de porte droite](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/piece-contour-porte1.png)

## 6. Lisser la lumière sans effacer les vrais plis

Un contour peut être courbe et pourtant montrer des bandes d'ombre. Lors du premier
essai, chaque face possédait sa propre copie des sommets. Les faces voisines ne
partageaient donc pas leurs points pour calculer une lumière continue.

L'exporteur de la [fiche02](02-maillage.md) partage maintenant les sommets des six
pièces de l'enveloppe. L'exporteur de peinture de la [fiche20](20-livree.md) fait de même.
Le seuil `crease 15` garde une séparation d'éclairage aux angles de plus de 15 degrés.
La position des faces reste la même. Le partage des sommets ne doit pas changer
l'immatriculation, les coordonnées de texture ou le contour d'une aile.

**Trois choses différentes :** davantage de tranches améliore la silhouette ; le
partage des sommets améliore la lumière ; l'anticrénelage adoucit les petits escaliers
des pixels à l'écran. Activer le troisième ne répare pas les deux premiers.

## 7. Écrire la recette complète

Dans ton dossier *Mon-Schweizer*, crée `tools/airframe_geometry.py` avec le Bloc-notes,
en UTF-8, sans ajouter `.txt`. Copie le bloc ci-dessous. Il construit uniquement
l'enveloppe et ses cadres. La fiche02 l'appelle avec `build_enclosure(poly, rod)`.
Il faut donc créer ce fichier **avant** de lancer `fabrique.py`.

<!-- atelier-fichier: tools/airframe_geometry.py -->
```python
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
            fairing = (cabin and xs[k] >= 2.13 and 8 <= j < 24) or (CABIN_END <= xs[k] < 5)
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

    def trim(name, a, b, radius):
        # Rubber bead behind the blue metal frame; offsets are model estimates.
        def back(p):
            return (p[0] - 0.016, p[1], p[2])
        rod("joints-verriere", 3, back(a), back(b), radius + 0.004)
        rod(name, FRAME_MATERIAL, a, b, radius)

    for k in cabin_ids[:-1]:
        for j in (0, DIVISIONS):
            trim("bordures-cockpit", upper[k][j], upper[k + 1][j], 0.014)
    for x in (CABIN_START, 1.55, 2.13, CABIN_END):
        k = min(range(len(xs)), key=lambda i: abs(xs[i] - x))
        for a, b in zip(upper[k], upper[k][1:]):
            trim("arceaux", a, b, 0.014)
        for p in upper[k][::4]:
            rod(
                "fixations-cadres",
                9,
                (p[0] + 0.012, p[1], p[2]),
                (p[0] + 0.019, p[1], p[2]),
                0.0035,
            )
    for k in cabin_ids[:-1]:
        if xs[k] >= 1.55:
            for j in (8, 24):
                rod("longerons-verriere", FRAME_MATERIAL, upper[k][j], upper[k + 1][j], 0.010)
    # Visible latch representation only: it does not unlock or move the canopy.
    latch = [
        (1.44, -0.445, 0.145),
        (1.46, -0.472, 0.17),
        (1.54, -0.472, 0.17),
        (1.56, -0.445, 0.145),
    ]
    for a, b in zip(latch, latch[1:]):
        rod("poignee-verriere", 11, a, b, 0.006)
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
```

## 8. Reconstruire et essayer

Dans *Mon-Schweizer*, avec les autres fiches déjà copiées, lance :

```powershell
.\.venv\Scripts\python.exe fabrique.py
.\.venv\Scripts\python.exe dynamique.py
```

Dans une copie du dépôt complet, la commande suivante reconstruit les fichiers
à partir du livre dans un **nouveau dossier vide**, puis les compare aux sources :

```powershell
python -m tools.check_workbook build/verification-formes-42
```

Si ce dossier existe déjà, choisis un autre nom. Ne supprime pas un dossier contenant
un travail que tu souhaites garder. Pour installer le paquet publié, suis la
[fiche12](12-installation.md), avec l'archive `sw233-formes-42.zip` du
[lot42](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/formes-42).

Dans FlightGear, sélectionne une vue extérieure, observe le profil puis l'avant.
Ouvre **SW233**, active la grille UV et regarde le nez. Remets ensuite la peinture.
Reviens à la vue pilote et vérifie les instruments. Les carreaux sont un papier
quadrillé temporaire : ils aident à repérer un trou, un chevauchement ou un étirement.

![Profil reconstruit dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/apres-nez-profil.png)

![Avant, vue oblique témoin](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/avant-nez-oblique.png)

![Après, même caméra oblique](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/apres-nez-oblique.png)

![Contrôle de la grille sur le nez](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/grid-close.png)

![Vue depuis le siège avant](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/cockpit.png)

## 9. Ce que les vérifications disent vraiment

Le banc utilise FlightGear 2024.1.7, une position au-dessus de CYJN, un ciel et une
heure fixes, une image de 1280 × 720 pixels et un modèle de vol nul. L'appareil est
immobilisé pour comparer ses formes ; ce n'est pas un essai de pilotage.
`tools.reference_bench` reprend les neuf caméras du lot41 et restaure les vues après
les captures. Les vues de détail ciblent x = 1,50 m, avec une distance de caméra de
25 m et un champ de 14° pour le profil, 17° pour les obliques. Le profil sombre est
conservé pour rester comparable au témoin, pas présenté comme une vue de livrée finale.

Les contrôles automatiques vérifient :

- que chaque bord de l'enveloppe appartient exactement à deux faces ;
- que le verre a une surface réelle, que les points sont finis et symétriques
  à la précision d'écriture de 0,00001 m ;
- que l'interpolation ne dépasse pas les valeurs des tranches aux points testés ;
- que la peinture couvre les faces nouvelles et que les UV restent dans leurs images ;
- que les occupants ne traversent pas le toit ou le dessous aux points échantillonnés ;
- que les recettes du livre reproduisent les sources et les outils.

Les plus petits dégagements verticaux échantillonnés tête/toit valent **9,8 cm à
l'avant et 10,8 cm à l'arrière** ; pieds/coque : **10,3 et 13,6 cm**. Ce sont des
résultats du modèle numérique, pas une certification de sécurité ni un relevé réel.
Les mains restent fixes et ne touchent pas nécessairement les commandes.

La comparaison des polygones avec le commit préalable trouve **neuf objets modifiés** :
coque, cinq parties vitrées/opaque de l'enveloppe, arceaux, bordures et longerons.
Les contours de porte, ailes, gouvernes, train, Pitot et instruments gardent leurs
coordonnées. Le FDM reste inchangé. Le partage des sommets de peinture change le
calcul d'éclairage, pas ces coordonnées.

## 10. Ce qui reste à corriger

Le résultat est une première reconstruction plus fine, pas une ressemblance finale
validée. La terminaison du nez, le raccord sous aile, les cadres exacts et les proportions
devront être revus avec tes retours et des cotes réelles. Les ailes, le patin, les sièges,
les harnais, la livrée éclair bleue et les emblèmes ont leurs propres tâches VIS-05.
La verrière est encore fixe. Ne confonds pas une belle image avec un mécanisme qui fonctionne.

Les [preuves et les 77 planches de pièces](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/formes-42)
permettent de revenir sur chaque comparaison. Les planches de pièces sont des projections
du maillage, sans texture ; seules les images portant la mention FlightGear sont des
captures du simulateur.

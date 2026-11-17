# 20 — Peindre une livrée provisoire, sans écrire à l'envers

## Notre objectif

Imagine un autocollant très fin posé sur la coque du planeur. On peut le retirer pour revoir la couleur d'origine. Cet autocollant est le fichier `livery.ac`. Ses deux feuilles de peinture sont `livery-left.png` et `livery-right.png`. Le petit fichier `livery.xml` décide si l'autocollant est visible.

**Cette peinture est provisoire.** Elle porte l'immatriculation demandée C-FYLP, mais les bandes et les nuances ne sont pas mesurées sur une photographie récente. Lis [la recherche et ses limites](../references/livree-recherche.md). On ne dessine pas un emblème officiel que l'on ne connaît pas.

## 1. Choisir les surfaces

Le fichier source `src/SW233/Models/sw233.ac` contient déjà une coque appelée `fuselage`. Le programme lit seulement cette coque dans la copie du paquet. Il ne change ni le cockpit, ni les ailes, ni les commandes. Le modèle original reste disponible lorsque l'option de livrée est désactivée.

Le générateur travaille avec les axes AC3D : x va vers la queue, y monte, z va à gauche. Dans nos dessins de construction, x va vers la queue, y va à droite et z monte. Pour passer du dessin au fichier : `(x, y, z)` devient `(x, z, -y)`. Ne confonds donc pas le y du fichier avec la largeur du planeur !

## 2. Placer la peinture sur l'image

Une texture est une image rectangle. Le point `(u=0, v=0)` est son coin inférieur gauche ; `(1,1)` son coin supérieur droit. Notre coque va de x=0 à x=7,61 m et de y=-0,63 à y=0,12 m. Sa hauteur utile est donc `0,12 - (-0,63) = 0,75 m`.

Sur le flanc gauche :

- `u = x / 7,61` ; à x=3,805 m, u vaut 0,5.
- `v = (y + 0,63) / 0,75` ; à y=-0,255 m, v vaut 0,5.
- Dans une image de 4096 × 512 pixels, le milieu est environ `(2048,256)`.

Pillow compte les lignes depuis le haut de l'image. On dessine donc à la ligne `(1-v) × 511`. Pour la colonne, on utilise `u × 4095`. Le dernier pixel porte le numéro 4095, car le premier porte le numéro zéro.

## 3. Lire C-FYLP des deux côtés

Quand on contourne le planeur, le nez change de côté dans notre vue. À droite, on utilise `u_droit = 1 - u_gauche`. Mais on ne retourne **jamais** une image qui porte déjà les lettres : elles seraient écrites comme dans un miroir. On redessine C-FYLP normalement dans chaque image et on place les bandes selon leurs coordonnées physiques. À x=5 m, u gauche vaut environ 0,657 et u droit environ 0,343.

Les objets `livery-fuselage-left` et `livery-fuselage-right` utilisent chacun leur feuille. L'objet `livery-fuselage-seam` ferme les zones centrales et les extrémités. Il utilise la feuille gauche, dans des régions sans lettres.

## 4. Éviter deux peaux au même endroit

Si deux feuilles occupent exactement la même place, la carte graphique hésite : l'image peut scintiller. Nous déplaçons donc la nouvelle peau de 1,2 mm vers l'extérieur. Une normale est simplement une petite flèche perpendiculaire à une surface. Au bord de plusieurs faces, on additionne leurs flèches puis on ramène la flèche obtenue à une longueur de 1. Chaque copie d'un même point reçoit exactement le même déplacement ; les raccords restent fermés.

La formule est `nouveau_point = ancien_point + 0,0012 × normale_moyenne`. Cette épaisseur est un choix pratique de dessin, pas une mesure de la peinture réelle. Les essais donnent au moins 0,591 mm de séparation perpendiculaire avec les faces voisines. Une vérification dans FlightGear reste nécessaire pour les vues lointaines et rasantes.

## 5. Intégrer et reconstruire

Le constructeur du paquet appelle `finish_livery(models)` après `finish_panel(models)`, où `models` désigne le dossier `Models` du paquet généré. Il ajoute aussi `<model><path>livery.xml</path></model>` dans le modèle principal. Le sous-modèle sélectionne ses trois objets lorsque `/sim/sw233/visuals/livery` vaut le booléen `true`. La valeur par défaut est gérée par la configuration principale, pas par le générateur.

Pour un essai isolé, copie `sw233.ac` dans un nouveau dossier `Models`, puis lance `python tools/livery.py CHEMIN_DU_DOSSIER_MODELS`. Les quatre sorties sont régénérables ; les conserver dans les sources n'est pas nécessaire. Modifier `YELLOW`, `BLUE` ou les points de `contour` change la peinture sans toucher au maillage de base.

## 6. Contrôler son travail

Vérifie que les deux textures affichent C-FYLP normalement, puis regarde chaque côté dans le simulateur. Active et désactive la livrée : la coque d'origine doit réapparaître. Regarde le nez, le dessous et la queue de près pour repérer les trous ; recule pour chercher un scintillement. Les essais géométriques ont trouvé 87 faces, 358 coins, 99 positions distinctes, des UV compris entre 0 et 1 et aucune normale latérale retournée. Les deux projections UV ont été examinées ; elles ne remplacent pas le contrôle final dans FlightGear.

## Code complet à reconstruire

Ce programme ne nécessite que Python et Pillow, déjà utilisés pour les instruments.

<!-- atelier-fichier: tools/livery.py -->
```python
"""Original provisional C-FYLP paint; no third-party photographs are embedded."""

import math
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

YELLOW = '#edb329'
BLUE = '#183c72'
OFFSET = .0012  # 1.2 mm: separate paint from the source skin.
SIZE = (4096, 512)
X_RANGE = (0., 7.61)
Y_RANGE = (-.63, .12)  # AC3D vertical coordinate, not construction y.


def read_fuselage(path):
    """Read the flat, untransformed fuselage object from our editable AC3D file."""
    text = path.read_text(encoding='utf-8')
    start = text.index('name "fuselage"')
    lines = text[start:text.index('kids 0', start)].splitlines()
    if any(line.startswith(('loc ', 'rot ')) for line in lines):
        raise ValueError('Fuselage transforms must be baked before painting')
    i = next(i for i, line in enumerate(lines) if line.startswith('numvert '))
    count = int(lines[i].split()[1])
    vertices = [tuple(map(float, line.split())) for line in lines[i+1:i+1+count]]
    faces = []
    for i, line in enumerate(lines):
        if line.startswith('refs '):
            count = int(line.split()[1])
            faces.append([vertices[int(row.split()[0])] for row in lines[i+1:i+1+count]])
    return faces


def normal(face):
    """Newell's normal handles both quads and the two many-sided end caps."""
    n = [0., 0., 0.]
    for a, b in zip(face, face[1:]+face[:1]):
        n[0] += (a[1]-b[1])*(a[2]+b[2])
        n[1] += (a[2]-b[2])*(a[0]+b[0])
        n[2] += (a[0]-b[0])*(a[1]+b[1])
    length = math.sqrt(sum(v*v for v in n))
    if length < 1e-10:
        raise ValueError('Degenerate fuselage face')
    return tuple(v/length for v in n)


def uv(point, side):
    x, height, _ = point
    u = (x-X_RANGE[0])/(X_RANGE[1]-X_RANGE[0])
    if side == 'right':
        u = 1-u
    return u, (height-Y_RANGE[0])/(Y_RANGE[1]-Y_RANGE[0])


def paint(side):
    """Physical-position stripe, but ordinary left-to-right text on BOTH images."""
    width, height = SIZE
    im = Image.new('RGB', SIZE, YELLOW)
    draw = ImageDraw.Draw(im)
    def pixel(x, y):
        u, v = uv((x, y, 0), side)
        return round(u*(width-1)), round((1-v)*(height-1))
    # Artistic boundaries, not measured from a current photograph of C-FYLP.
    contour = [(0., -.32), (1., -.27), (3.25, -.23), (5., -.21), (7.61, -.12)]
    draw.polygon([pixel(x,y) for x,y in contour+[(7.61,-.63),(0.,-.63)]],fill=BLUE)
    draw.line([pixel(x,y+.035) for x,y in contour],fill=BLUE,width=5)
    # Draw fresh letters, never mirror an image containing letters.
    a, b = pixel(3.65, -.015), pixel(5.35, -.17)
    box = (min(a[0],b[0]), min(a[1],b[1]), max(a[0],b[0]), max(a[1],b[1]))
    font = ImageFont.load_default(size=150)
    ink = Image.new('RGBA',(1000,220),(0,0,0,0))
    pen = ImageDraw.Draw(ink)
    bounds = pen.textbbox((0,0),'C-FYLP',font=font)
    pen.text((-bounds[0],-bounds[1]),'C-FYLP',font=font,fill=BLUE)
    ink = ink.crop((0,0,bounds[2]-bounds[0],bounds[3]-bounds[1]))
    ink = ink.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    im.paste(ink,(box[0],box[1]),ink)
    return im


def finish_livery(models: Path):
    """Generate a removable overlay after finish_panel(models); source stays intact."""
    models = Path(models)
    faces = read_fuselage(models/'sw233.ac')
    normals = defaultdict(lambda: [0.,0.,0.])
    for face in faces:
        n = normal(face)
        for point in face:
            for axis in range(3):
                normals[point][axis] += n[axis]
    shifted = {}
    for point,n in normals.items():
        length = math.sqrt(sum(v*v for v in n))
        if length < 1e-10:
            raise ValueError('Opposing skin normals at a vertex')
        shifted[point] = tuple(point[i]+OFFSET*n[i]/length for i in range(3))
    groups = {'left':[], 'right':[], 'seam':[]}
    for face in faces:
        lateral = sum(p[2] for p in face)/len(face)
        side = 'left' if lateral > 1e-7 else 'right' if lateral < -1e-7 else 'seam'
        groups[side].append(face)
    lines = ['AC3Db', 'MATERIAL "provisional-paint" rgb 1 1 1 amb .5 .5 .5 '
             'emis 0 0 0 spec .10 .10 .10 shi 16 trans 0', 'OBJECT world', 'kids 3']
    for side, polygons in groups.items():
        name = 'livery-fuselage-'+side
        texture = 'right' if side == 'right' else 'left'
        vertices = [p for face in polygons for p in face]
        lines += ['OBJECT poly',f'name "{name}"',f'texture "livery-{texture}.png"',
                  'crease 40',f'numvert {len(vertices)}']
        lines += [' '.join(f'{v:.7f}' for v in shifted[p]) for p in vertices]
        lines.append(f'numsurf {len(polygons)}')
        offset = 0
        for face in polygons:
            # Smooth, single-sided polygons, same winding as the source skin.
            lines += ['SURF 0x10','mat 0',f'refs {len(face)}']
            for j,p in enumerate(face):
                u,v = uv(p,texture)
                if not (-1e-6 <= u <= 1.000001 and -1e-6 <= v <= 1.000001):
                    raise ValueError('Fuselage exceeds the documented UV bounds')
                lines.append(f'{offset+j} {u:.8f} {v:.8f}')
            offset += len(face)
        lines.append('kids 0')
    (models/'livery.ac').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for side in ('left','right'):
        paint(side).save(models/f'livery-{side}.png')
    root = ET.Element('PropertyList')
    ET.SubElement(root,'path').text = 'livery.ac'
    animation = ET.SubElement(root,'animation')
    ET.SubElement(animation,'type').text = 'select'
    for side in groups:
        ET.SubElement(animation,'object-name').text = 'livery-fuselage-'+side
    equals = ET.SubElement(ET.SubElement(animation,'condition'),'equals')
    ET.SubElement(equals,'property').text = '/sim/sw233/visuals/livery'
    ET.SubElement(equals,'value',{'type':'bool'}).text = 'true'
    ET.indent(root)
    ET.ElementTree(root).write(models/'livery.xml',encoding='utf-8',xml_declaration=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('models',type=Path,help='Generated package Models directory')
    finish_livery(parser.parse_args().models)
```
## 7. Observer la livrée dans FlightGear

Les deux images ci-dessous sont destinées aux captures réelles du simulateur, prises à gauche puis à droite. Elles montrent la maquette avec sa **livrée provisoire**, et non une photographie de C-FYLP réel. Le jaune, le bleu et les bandes restent des choix de dessin tant que leur disposition exacte n'a pas été confirmée par des photographies datées.

![Vue gauche de la livrée provisoire dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/livery-left.jpg)

Sur le flanc gauche, repère le dessous bleu et le filet au-dessus de lui. Les lettres C-FYLP doivent se lire normalement sur la partie jaune. Observe aussi le passage de la bande vers la queue : le dessin doit suivre la coque sans flotter devant elle.

![Vue droite de la livrée provisoire dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/livery-right.jpg)

À droite, le nez apparaît de l'autre côté de l'image, mais les lettres doivent toujours se lire de gauche à droite. Compare la hauteur de la bande avec celle du flanc gauche. Si les lettres deviennent inversées, c'est le placement de la texture qu'il faut corriger : retourner toute l'image retournerait aussi l'écriture.

Pour examiner séparément les trois morceaux de cette peau, télécharge [l'atlas complet des nouvelles pièces](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/atlas.zip), décompresse-le, puis ouvre `index.html`. Il contient aussi les 178 pièces des occupants et les trois vitres des cadrans. Chaque dessin montre le profil, le dessus et la face ; il explique la géométrie sans représenter la transparence ou la texture.

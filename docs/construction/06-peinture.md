# 6 · Peindre sans figer les instruments

Une texture est comme une feuille autocollante. Nous allons la dessiner nous-mêmes, sans reprendre une photo protégée. Crée tools/panel.py. Les diamètres et positions sont ceux de la maquette, la disposition est inspirée de C-FYLP. Le module peint lors de l’assemblage : il ne modifie pas ton original.

**Fichier à écrire :** `tools/panel.py`. Colle les blocs de ce fichier dans l’ordre, sans retirer les espaces du début des lignes.

## A · Fais une feuille de métal virtuelle

Crée une image de 1536 × 768 pixels. Le grain est une suite de petits gris ; la graine 233 assure le même motif à chaque essai. Le gabarit couvre 0,80 × 0,40 m : les deux sens ont donc 1920 px par mètre. Le fond dépasse un peu de la planche ; les faces 3D en découpent le contour. Python doit garder quatre espaces devant le corps de finish_panel.

<!-- atelier-fichier: tools/panel.py -->
```python
"""Paint an original instrument panel from editable dimensions, without photographs."""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def finish_panel(models: Path):
    """Decorate the packaged mesh; its three animated instruments stay independent."""
    w, h = 1536, 768
    rng = random.Random(233)
    noise = bytes(rng.randrange(35, 53) for _ in range(w*h))
    im = Image.frombytes("L", (w, h), noise).convert("RGB")
    pen = ImageDraw.Draw(im)
```

## B · Construis une règle et trois tampons

La règle xy convertit des mètres en pixels : droite = plus de colonnes, haut = moins de lignes. À y = 0 et z = 0,10, retrouve (768,384). Le tampon disc dessine un disque ; screw superpose deux disques décalés et une fente ; label centre un texte. Un rayon de 0,0042 m donne environ 8 px. Taille et teinte des vis sont des choix graphiques, pas un relevé de visserie.

<!-- atelier-fichier: tools/panel.py -->
```python
    def xy(y, z):
        return ((y+.4)*w/.8, (.30-z)*h/.4)

    def disc(y, z, radius, color):
        x, v = xy(y, z)
        r = radius*w/.8
        pen.ellipse((x-r, v-r, x+r, v+r), fill=color)

    def screw(y, z):
        disc(y, z, .0042, "#121414")
        disc(y-.0005, z+.0006, .0032, "#8f9189")
        pen.line([xy(y-.002, z-.001), xy(y+.002, z+.001)], fill="#252629", width=2)

    def label(y, z, text, size):
        pen.text(xy(y, z), text, fill="#e0ded0", anchor="mm",
                 font=ImageFont.load_default(size=size))
```

## C · Aligne les trous sur les aiguilles

Reprends les mêmes centres et rayons qu’à la fiche 2 : un cercle autour d’une aiguille doit avoir le même centre qu’elle. Pour la vitesse, (0,17 ; 0,14) donne environ (1094 ; 307) px. Trois disques concentriques donnent au bord une zone sombre, une arête éclairée et un retour sombre. Quatre vis sont réparties à 90° : elles restent attachées au panneau.

<!-- atelier-fichier: tools/panel.py -->
```python
    for y, z, r, title in [(-.22,.087,.083,"ALT  /  FT"), (.17,.14,.075,"AIR SPEED  /  MPH"),
                            (.295,.022,.063,"VERTICAL SPEED")]:
        for extra, color in [(.009,"#141719"),(.007,"#777b78"),(.005,"#393c39")]:
            disc(y,z,r+extra,color)
        for i in range(4):
            a = (i+.5)*math.pi/2
            screw(y+(r+.008)*math.cos(a), z+(r+.008)*math.sin(a))
        label(y,z-r-.018,title,17)
```

## D · Installe l’aérateur et les repères fixes

La photo C-FYLP montre une bouche ronde au-dessus du centre. Les disques et traits qui suivent en donnent une interprétation originale. Les textes et couleurs de cette planche sont nos choix, pas une photo scannée. La peinture s’arrête avant les aiguilles mobiles.

<!-- atelier-fichier: tools/panel.py -->
```python
    # Central vent and grille observed on the supplied C-FYLP cockpit photograph.
    for r, color in [(.046,"#141414"),(.044,"#6e706b"),(.042,"#34373a"),
                     (.037,"#505457"),(.034,"#141719")]:
        disc(0,.197,r,color)
    for j in range(-2,3):
        pen.line([xy(-.026,.197+j*.009+.003),xy(.026,.197+j*.009-.003)],
                 fill="#55585a", width=4)
    for y, z in [(-.30,.15),(-.36,.04),(.33,.11),(-.085,.24),(.082,.24)]:
        screw(y,z)
```

## D bis · Refaire les quatre plaquettes et la façade radio

Sur l’image C-FYLP, pointe le milieu des cartes vers (282,176), (413,181), (282,254) et (408,259). Chacune mesure environ 40 × 65 px dans la photo. Avec la largeur supposée de la planche, cela donne environ 0,051 × 0,083 m. Sur la feuille de peinture à 1920 px/m, notre carte de 97 × 140 px représente 0,051 × 0,073 m : nous raccourcissons volontairement le texte pour le garder lisible. Écris le titre en haut, trace une ligne, puis place les rappels ; les listes complètes restent dans le menu. La radio de la photo est à gauche de la bouche, son centre vers (210,222). Vérifie avant de dessiner qu’elle ne recouvre pas l’altimètre. Un écran gris sans chiffres évite de faire croire à une fréquence active. La boule de largage, elle, n’est pas imprimée sur la feuille : elle a été fabriquée en 3D à la fiche 2.

<!-- atelier-fichier: tools/panel.py -->
```python
    # Les cartes sont des rappels du simulateur, pas des consignes de vol réel.
    def card(y, z, title, words):
        x, v = xy(y, z)
        width, height = 97, 140
        box = (x-width/2, v-height/2, x+width/2, v+height/2)
        pen.rounded_rectangle(box, radius=6, fill="#ddd7bf", outline="#908d83", width=3)
        pen.line((x-41, v-39, x+41, v-39), fill="#4c4a44", width=2)
        for i, line in enumerate([title, *words]):
            pen.text((x-41, v-58+i*22), line, fill="#25272a",
                     font=ImageFont.load_default(size=12 if i == 0 else 14))

    card(-.079, .197, "PRE TAKE-OFF", ["BALLAST", "CONTROLS", "SPOILERS", "CANOPY"])
    card(.078, .190, "PRE-LANDING", ["SPOILERS", "WIND", "AIRSPEED", "TRAFFIC"])
    card(-.079, .077, "PRE RELEASE", ["AREA", "ALTITUDE", "POSITION", "TRAFFIC"])
    card(.078, .070, "PRE STALL", ["ALTITUDE", "STRAPS", "CANOPY", "TRAFFIC"])
    # Face radio et deux boutons. Aucun chiffre de fréquence fictif.
    ry, rz = -.145, .169
    for rr, tone in [(.039,"#171717"),(.037,"#686866"),(.035,"#323536")]:
        disc(ry,rz,rr,tone)
    x, v = xy(ry,rz)
    pen.rounded_rectangle((x-35,v-20,x+35,v-3), radius=3, fill="#71766a")
    label(ry,rz-.009,"COM",12)
    for dy in (-.017,.017):
        disc(ry+dy,rz-.021,.008,"#101214")
        disc(ry+dy-.001,rz-.019,.005,"#414441")
    label(-.143,.114,"RADIO",11)
    label(0,.014,"LARGAGE",14)
```

## E · Colle la peau sans coller les aiguilles

Écris le PNG dans la copie à installer. Dans le maillage, ajoute une matière claire : une matière noire multiplierait et assombrirait la peinture. Parcours seulement les références de la face tableau. U va de gauche à droite, V va du bas vers le haut, contrairement aux lignes de l’image. Au centre du gabarit, U = V = 0,5. Les trois derniers nombres lus par Python sont les coordonnées AC3D : la variable left est l’opposé de y. N’applique cette fonction qu’une fois à une copie fraîche.

<!-- atelier-fichier: tools/panel.py -->
```python
    im.save(models/"panel.png")
    mesh = models/"sw233.ac"
    s = mesh.read_text()
    tag = 'OBJECT world'
    material = s[:s.index(tag)].count('MATERIAL ')
    s = s.replace(tag, 'MATERIAL "panel-finish" rgb 1 1 1 amb .6 .6 .6 emis .2 .2 .2 '
                  'spec .12 .12 .12 shi 12 trans 0\n'+tag, 1)
    start = s.index('name "tableau"')
    end = s.index("kids 0",start)
    lines = s[start:end].splitlines()
    n = int(lines[1].split()[1])
    verts = [list(map(float, line.split())) for line in lines[2:2+n]]
    ri = next(i for i,v in enumerate(lines) if v.startswith("refs "))
    lines[ri-1] = f"mat {material}"
    for i in range(ri+1,len(lines)):
        idx = int(lines[i].split()[0])
        _,z,left = verts[idx]
        lines[i] = f"{idx} {(-left+.4)/.8:.6f} {(z+.1)/.4:.6f}"
    lines.insert(1,'texture "panel.png"')
    mesh.write_text(s[:start]+"\n".join(lines)+"\n"+s[end:])
```

**Contrôle :** la fiche 7 appelle `finish_panel` sur le paquet. Dans la copie peinte, ouvre *Models/panel.png* avec Photos : la bouche d’air doit être en haut et les lettres doivent être à l’endroit. Puis cherche `texture "panel.png"` dans la copie de *sw233.ac*. Si le tableau est beau mais l’aiguille immobile, c’est l’animation de la fiche 4 qu’il faut contrôler, pas cette peinture.

**Compare ton résultat.** [Ouvre la capture du siège avant dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/cockpit-construction-01/SW233-cockpit-CFYLP.jpg). Repère la boule bordeaux sous la bouche d’air et compte les quatre cartes crème. Regarde aussi ce qui reste à améliorer : la radio est trop proche du cerclage gauche et il manque le compas entre les cartes du bas.

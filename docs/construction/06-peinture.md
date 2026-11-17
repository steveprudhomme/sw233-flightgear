# 6 · Peindre sans figer les instruments

![Le tableau peint dans l’enveloppe corrigée](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-cockpit.jpg)

Rendu natif actualisé : les cadrans restent des textures originales avec des aiguilles séparées. Voir la [fiche 14](14-enveloppe.md) pour les parois et les cadres jaunes.

Une texture est comme une feuille autocollante. Nous allons la dessiner nous-mêmes, sans reprendre une photo protégée. Crée tools/panel.py. Les diamètres et positions sont ceux de la maquette, la disposition est inspirée de C-FYLP. Le module peint lors de l’assemblage : il ne modifie pas ton original.

**Fichier à écrire :** `tools/panel.py`. Colle les blocs de ce fichier dans l’ordre, sans retirer les espaces du début des lignes.

## A · Fais une feuille de métal virtuelle

Crée une image de 1536 × 768 pixels. Le grain est une suite de petits gris entre 25 et 32 (auparavant 35 à 52) ; la graine 233 assure le même motif à chaque essai. Le gabarit couvre 0,80 × 0,40 m : les deux sens ont donc 1920 px par mètre. Le fond dépasse un peu de la planche ; les faces 3D en découpent le contour. Python doit garder quatre espaces devant le corps de finish_panel.

<!-- atelier-fichier: tools/panel.py -->
```python
"""Paint an original instrument panel from editable dimensions, without photographs."""

import math
import random
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def finish_panel(models: Path):
    """Decorate the packaged mesh; its three animated instruments stay independent."""
    w, h = 1536, 768
    rng = random.Random(233)
    # Fine, low-contrast paint grain; artistic values, not measured reflectance.
    noise = bytes(rng.randrange(25, 33) for _ in range(w*h))
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
        # Painted shadow, washer and a slotted metal head (no added geometry).
        disc(y+.0006, z-.0006, .0048, "#111315")
        disc(y, z, .0043, "#35383a")
        disc(y, z, .0033, "#898c87")
        x, v = xy(y, z)
        r = .0031*w/.8
        pen.arc((x-r, v-r, x+r, v+r), 195, 300, fill="#d4d3c7", width=2)
        pen.arc((x-r, v-r, x+r, v+r), 15, 120, fill="#4a4d4b", width=2)
        pen.line([xy(y-.002, z-.001), xy(y+.002, z+.001)], fill="#26282a", width=3)
        pen.line([xy(y-.0018, z-.0005), xy(y+.0017, z+.0012)],
                 fill="#b8b9ae", width=1)

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
        # All three instrument rims and their fasteners are separate 3D objects.
        label(y,z-r-.018,title,17)
```

## D · Installe l’aérateur et les repères fixes

La photo C-FYLP montre une bouche ronde au-dessus du centre. Les disques et traits qui suivent en donnent une interprétation originale. Les textes et couleurs de cette planche sont nos choix, pas une photo scannée. La peinture s’arrête avant les aiguilles mobiles.

<!-- atelier-fichier: tools/panel.py -->
```python
    # The central vent is now separate 3D geometry; leave the paint beneath it plain.
    for y, z in [(-.30,.15),(-.36,.04),(.33,.11),(-.085,.24),(.082,.24)]:
        screw(y,z)
```

## D bis · Refaire les quatre plaquettes et la façade radio

Sur l’image C-FYLP, pointe le milieu des cartes vers (282,176), (413,181), (282,254) et (408,259). Chacune mesure environ 40 × 65 px dans la photo. Avec la largeur supposée de la planche, cela donne environ 0,051 × 0,083 m. Sur la feuille de peinture à 1920 px/m, notre carte de 97 × 140 px représente 0,051 × 0,073 m : nous raccourcissons volontairement le texte pour le garder lisible. Écris le titre en haut, trace une ligne, puis place les rappels ; les listes complètes restent dans le menu. La radio de la photo est à gauche de la bouche, son centre vers (210,222). Vérifie avant de dessiner qu’elle ne recouvre pas l’altimètre. Un écran gris sans chiffres évite de faire croire à une fréquence active. La boule de largage, elle, n’est pas imprimée sur la feuille : elle a été fabriquée en 3D à la fiche 2.

<!-- atelier-fichier: tools/panel.py -->
```python
    # Les cartes sont des rappels du simulateur, pas des consignes de vol réel.
    def card(y, z):
        x, v = xy(y, z)
        width, height = 97, 140
        box = (x-width/2, v-height/2, x+width/2, v+height/2)
        # Dark holder and warm-white card, inspired by the reference photograph.
        pen.rounded_rectangle((box[0]-4, box[1]-3, box[2]+4, box[3]+5),
                              radius=8, fill="#111416", outline="#565b59", width=2)
        pen.rounded_rectangle(box, radius=5, fill="#e3e1d5", outline="#b1b3a9", width=1)
        pen.line((x-41, v-39, x+41, v-39), fill="#4c4a44", width=1)
    for y,z in [(-.079,.197),(-.079,.077),(.078,.190),(.078,.070)]:
        card(y,z)
    # Both atlases come from the same XML files as the native checklist data.
    for language, filename in [("fr","sw233.xml"),("en","sw233-en.xml")]:
        data = ET.parse(models.parent/"Checklists"/filename)
        atlas = Image.new("RGB",(1024,1536),"#e3e1d5")
        draw = ImageDraw.Draw(atlas)
        for index, entry in enumerate(data.findall("placards/card")):
            x,y = (index%2)*512,(index//2)*768
            rows = entry.findall("line")
            spacing = min(130, 510/max(1, len(rows)-1))
            for row, node in enumerate(rows):
                # Pillow's bundled font lacks these accented capitals. Keep UTF-8
                # in the data and add the acute/grave strokes to their base glyphs.
                letters = []
                accents = []
                for char in unicodedata.normalize("NFD",node.text):
                    if unicodedata.combining(char):
                        if char not in ("\u0301","\u0300") or not letters:
                            raise ValueError("Unsupported placard accent: " + node.text)
                        accents.append((len(letters)-1,char))
                    else:
                        letters.append(char)
                text = "".join(letters)
                size = 42 if row == 0 else min(62, int(spacing*.72))
                while True:
                    font = ImageFont.load_default(size=size)
                    box = draw.textbbox((0,0),text,font=font)
                    if box[2]-box[0] <= 480 or size <= 20:
                        break
                    size -= 1
                left = x+256-draw.textlength(text,font=font)/2
                top = y+65 if row == 0 else y+185+(row-1)*spacing
                draw.text((left,top),text,anchor="lt",font=font,fill="#25272a")
                # Highlight the mnemonic initial only, never the title.
                if row > 0:
                    draw.text((left,top),text[0],anchor="lt",font=font,fill="#a01820")
                for position,accent in accents:
                    center = left+draw.textlength(text[:position],font=font)
                    center += draw.textlength(text[position],font=font)/2
                    dx = size*.10
                    a,b = (center-dx,top-size*.10),(center+dx,top-size*.24)
                    if accent == "\u0300":
                        a,b = (a[0],b[1]),(b[0],a[1])
                    draw.line((a,b),fill="#a01820" if row > 0 and position == 0 else "#25272a",
                              width=max(2,round(size*.05)))
            draw.line((x+20,y+155,x+492,y+155),fill="#4c4a44",width=3)
            draw.text((x+256,y+718),"SIMULATION",anchor="mt",
                      font=ImageFont.load_default(size=26),fill="#4c4a44")
        atlas.save(models/("placards-"+language+".png"))
    # The radio now has its own textured face and fixed 3D controls.
    label(-.131,.151,"RADIO",11)
    radio = Image.new("RGB",(512,512),"#292e2d")
    rp = ImageDraw.Draw(radio)
    # Original artwork: blank display, only clearly readable COM inscription.
    rp.rounded_rectangle((112,128,400,214),radius=9,fill="#0e1313",
                         outline="#717971",width=3)
    rp.text((256,268),"COM1 MHz",anchor="mm",fill="#e0ded0",
            font=ImageFont.load_default(size=32))
    radio.save(models/"radio.png")
    # Le compas en relief est dans le maillage : ne pas le repeindre ici.
    label(0,.014,"LARGAGE",14)
```

## E · Colle la peau sans coller les aiguilles

Écris le PNG dans la copie à installer. Dans le maillage, ajoute une matière claire : une matière noire multiplierait et assombrirait la peinture. Traite séparément les faces du tableau et de l’anémomètre. U va de gauche à droite, V va du bas vers le haut, contrairement aux lignes de l’image. Au centre du gabarit, U = V = 0,5. Les trois derniers nombres lus par Python sont les coordonnées AC3D : la variable left est l’opposé de y. N’applique cette fonction qu’une fois à une copie fraîche.

<a name="peinture-ias"></a>

**Peins la face de l’anémomètre.** Prépare un carré de 512 × 512 pixels et place le pivot en (256,256). Lis la table de la fiche 4. Pour chaque vitesse, trouve les deux lignes qui l’encadrent et partage le trajet en proportion. Dessine un trait tous les 5 mph de 20 à 160, un trait long tous les 10 et un nombre tous les 20. Les lettres MPH restent fixes. Le moyeu et l’aiguille ivoire, eux, ont été construits dans la fiche 2 : ne les peins pas.

**Choisis les couleurs sur la bonne ligne du manuel.** Ouvre le *FAA Approved Flight Manual* du [fonds local](../references/inventaire.md), §2.3, page imprimée 10 (page 6 du PDF). Pour la configuration **1 040 lb** reproduite ici : arc vert **38–65 mph**, jaune **65–98 mph**, trait rouge **98 mph**. La colonne 1 080 lb contient d’autres valeurs : il s’agit d’une autre configuration, pas de couleurs à changer selon le poids instantané du planeur. La photo donne l’allure, le manuel donne les bornes. Nos couleurs sont dessinées, pas prélevées sur une peinture d’usine.

Colle la nouvelle texture *ias.png* uniquement sur *ias-fond*. Son diamètre dans notre maquette est de 0,15 m : le bord gauche est à 0,17 − 0,075 = 0,095 m. Le bas est à 0,14 − 0,075 = 0,065 m. Ces deux nombres expliquent les coordonnées de la deuxième ligne de la boucle finale. Vérifie que les valeurs augmentent dans le sens horaire, puis [essaie les quatre entrées](07-essais.md#banc-anemometre).

<!-- atelier-fichier: tools/panel.py -->
```python
    # Read the needle's actual knot/degree table. Never maintain two scales.
    anims = ET.parse(models/"sw233-model.xml").getroot()
    table = anims.find("animation[object-name='vitesse-mph']/interpolation")
    scale = [(float(e.findtext("ind")),float(e.findtext("dep"))) for e in table]
    def angle(mph):
        kt = mph * 1609.344 / 1852
        for (a,lo),(b,hi) in zip(scale,scale[1:]):
            if kt <= b:
                return lo+(hi-lo)*(kt-a)/(b-a)
        return scale[-1][1]

    dial = Image.new("RGB",(512,512),"#23262a")
    brush = ImageDraw.Draw(dial)
    def polar(mph, radius):
        a = math.radians(angle(mph))
        return (256+radius*math.sin(a),256-radius*math.cos(a))

    # Manual §2.3, 1040 lb configuration, all markings in mph.
    for low,high,ink in [(38,65,"#318563"),(65,98,"#e8bd43")]:
        brush.arc((10,10,502,502),angle(low)-90,angle(high)-90,fill=ink,width=12)
    for v in range(20,161,5):
        brush.line([polar(v,235),polar(v,202 if v%10==0 else 219)],
                   fill="#f5efde",width=5 if v%10==0 else 3)
    brush.line([polar(98,247),polar(98,207)],fill="#e54d43",width=9)
    for v in range(20,161,20):
        brush.text(polar(v,171),str(v),anchor="mm",fill="#f5efde",
                   font=ImageFont.load_default(size=35))
    brush.text((256,313),"MPH",anchor="mm",fill="#eee9d9",font=ImageFont.load_default(size=26))
    dial.save(models/"ias.png")
```

### Le petit cadran de montée et descente

Continue dans le même fichier. Peins le disque en 512 × 512 pixels. Relis la table de l’animation *vario*, puis dessine un trait tous les 100 ft/min et un grand trait tous les 500. Divise le nombre par 100 pour écrire le chiffre du cadran ; omets le signe, remplacé par les indications UP et DOWN. Pour placer le disque dans la maquette, prends le centre (0,295 ; 0,022) et le rayon 0,063 m : le coin inférieur gauche vaut (0,232 ; −0,041). L’aiguille reste une pièce 3D ivoire. [Vérifie ses quatre positions dans FlightGear](07-essais.md#banc-variometre).

<!-- atelier-fichier: tools/panel.py -->
```python
    # VSI graduations and needle share the measured angle table.
    entries = anims.find("animation[object-name='vario']/interpolation")
    vsi_scale = [(float(e.findtext("ind")),float(e.findtext("dep"))) for e in entries]
    def vsi_point(rate, radius):
        for (a,lo),(b,hi) in zip(vsi_scale,vsi_scale[1:]):
            if rate <= b:
                ang = math.radians(lo+(hi-lo)*(rate-a)/(b-a))
                return (256+radius*math.sin(ang),256-radius*math.cos(ang))
        raise ValueError(rate)
    vsi = Image.new("RGB",(512,512),"#25282b")
    draw = ImageDraw.Draw(vsi)
    ivory = "#eeeadd"
    for rate in range(-2000,2001,100):
        major = rate%500 == 0
        draw.line([vsi_point(rate,242),vsi_point(rate,204 if major else 222)],
                  fill=ivory,width=7 if major else 4)
        if major and abs(rate)!=2000:
            draw.text(vsi_point(rate,170),str(abs(rate)//100),anchor="mm",fill=ivory,
                      font=ImageFont.load_default(size=35))
    for where,txt,size in [((425,256),"20",36),((152,202),"UP",18),((152,310),"DOWN",18),
                           ((265,181),"VERTICAL SPEED",21),((265,207),"100 FEET PER MIN",16)]:
        draw.text(where,txt,anchor="mm",fill=ivory,font=ImageFont.load_default(size=size))
    vsi.save(models/"vsi.png")
```

### Altimètre : échelle régulière et aiguilles en relief

Prépare un carré 512 × 512, centre (256,256). Cinquante divisions donnent 7,2° par petit trait ; cinq petits traits font un secteur de 36°. Écris 0 à 9, puis ALT et FEET. Garde la fenêtre de pression vide : une valeur peinte serait fausse après réglage. Le centre dans la maquette est (−0,22 ; 0,087) et le rayon 0,083 m ; le coin inférieur gauche vaut donc (−0,303 ; 0,004). [Contrôle les cinq lectures](07-essais.md#banc-altimetre).

<!-- atelier-fichier: tools/panel.py -->
```python
    # Altimeter: ten equal sectors, two independent 3D hands.
    alt = Image.new("RGB",(512,512),"#24272a")
    draw = ImageDraw.Draw(alt)
    def alt_point(angle, radius):
        a = math.radians(angle)
        return (256+radius*math.sin(a),256-radius*math.cos(a))
    for i in range(50):
        draw.line([alt_point(i*7.2,241),alt_point(i*7.2,205 if i%5==0 else 223)],
                  fill="#f1eddf",width=6 if i%5==0 else 3)
    for i in range(10):
        draw.text(alt_point(i*36,172),str(i),anchor="mm",fill="#f1eddf",
                  font=ImageFont.load_default(size=39))
    draw.text((256,208),"ALT",anchor="mm",fill="#eeeadd",font=ImageFont.load_default(size=29))
    draw.text((256,304),"FEET",anchor="mm",fill="#eeeadd",font=ImageFont.load_default(size=19))
    # Estimated window for the live XML pressure readout, behind the hands.
    draw.rounded_rectangle((336,220,448,292),radius=4,fill="#111519",outline="#737975",width=2)
    alt.save(models/"alt.png")
    im.save(models/"panel.png")
    # Original compass strip: north at the middle, south split at both ends.
    # Draw at twice the final resolution, then filter the edges for smooth text.
    scale = 2
    width, height = 4096, 256
    strip = Image.new("RGB", (width*scale,height*scale), "#111819")
    ink = ImageDraw.Draw(strip)
    ivory = "#eeeadd"
    def row(h):
        return (.011-h)/.022*height*scale
    for deg in range(0,360,5):
        x = ((.5-deg/360)%1)*width*scale
        for shift in (-width*scale,0,width*scale):
            ink.rectangle((x+shift-4*scale,row(.010 if deg%10==0 else .007),
                           x+shift+4*scale,row(.004)), fill=ivory)
    font = ImageFont.load_default(size=140*scale)
    for deg, word in enumerate(["N","3","6","E","12","15","S","21","24","W","30","33"]):
        x = ((.5-deg/12)%1)*width*scale
        for shift in (-width*scale,0,width*scale):
            ink.text((x+shift,row(.001)),word,font=font,anchor="mt",fill=ivory)
    strip.resize((width,height),Image.Resampling.LANCZOS).save(models/"compass.png")
    mesh = models/"sw233.ac"
    s = mesh.read_text()
    tag = 'OBJECT world'
    material = s[:s.index(tag)].count('MATERIAL ')
    s = s.replace(tag, 'MATERIAL "panel-finish" rgb 1 1 1 amb .6 .6 .6 emis .2 .2 .2 '
                  'spec .12 .12 .12 shi 12 trans 0\n'+tag, 1)
    for name,texture,ymin,zmin,span_y,span_z in [
        ("tableau","panel.png",-.4,-.1,.8,.4),("ias-fond","ias.png",.095,.065,.15,.15),
        ("vsi-fond","vsi.png",.232,-.041,.126,.126),
        ("alt-fond","alt.png",-.303,.004,.166,.166),
        ("radio-face","radio.png",-.172,.158,.062,.062),
    ]:
        start = s.index(f'name "{name}"')
        end = s.index("kids 0",start)
        lines = s[start:end].splitlines()
        n = int(lines[1].split()[1])
        verts = [list(map(float, line.split())) for line in lines[2:2+n]]
        ri = next(i for i,v in enumerate(lines) if v.startswith("refs "))
        lines[ri-1] = f"mat {material}"
        for i in range(ri+1,len(lines)):
            idx = int(lines[i].split()[0])
            _,z,left = verts[idx]
            lines[i] = f"{idx} {(-left-ymin)/span_y:.6f} {(z-zmin)/span_z:.6f}"
        lines.insert(1,f'texture "{texture}"')
        s = s[:start]+"\n".join(lines)+"\n"+s[end:]
    # Keep the other panel materials unchanged; this card needs a brighter base.
    compass_material = s[:s.index(tag)].count('MATERIAL ')
    s = s.replace(tag, 'MATERIAL "compass-finish" rgb 1 1 1 amb .6 .6 .6 '
                  'emis .45 .45 .45 spec .05 .05 .05 shi 8 trans 0\n'+tag, 1)
    # Each face has four private vertices, ordered bottom-left to top-left.
    start = s.index('name "compas-rose"')
    end = s.index("kids 0",start)
    lines = s[start:end].splitlines()
    for i,line in enumerate(lines):
        if line.startswith("mat "):
            lines[i] = f"mat {compass_material}"
        elif line.startswith("refs "):
            for j in range(1,5):
                idx = int(lines[i+j].split()[0])
                face,corner = divmod(idx,4)
                u = (face+(1 if corner in (1,2) else 0))/72
                v = 1 if corner in (2,3) else 0
                lines[i+j] = f"{idx} {u:.8f} {v}"
    lines.insert(1,'texture "compass.png"')
    s = s[:start]+"\n".join(lines)+"\n"+s[end:]
    # One atlas quarter per placard; the XML selects only one language object.
    for language in ("fr","en"):
        start = s.index('name "plaquettes-'+language+'"')
        end = s.index("kids 0",start)
        lines = s[start:end].splitlines()
        for i,line in enumerate(lines):
            if line.startswith("mat "):
                lines[i] = f"mat {material}"
            elif line.startswith("refs "):
                for j in range(1,5):
                    idx = int(lines[i+j].split()[0])
                    face,corner = divmod(idx,4)
                    u = (face%2+(1 if corner in (1,2) else 0))/2
                    v = 1-(face//2+(0 if corner in (2,3) else 1))/2
                    lines[i+j] = f"{idx} {u} {v}"
        lines.insert(1,'texture "placards-'+language+'.png"')
        s = s[:start]+"\n".join(lines)+"\n"+s[end:]
    mesh.write_text(s)
```

**Contrôle :** la fiche 7 appelle `finish_panel` sur le paquet. Dans la copie peinte, ouvre *Models/panel.png* avec Photos : la bouche d’air doit être en haut et les lettres doivent être à l’endroit. Puis cherche `texture "panel.png"` dans la copie de *sw233.ac*. Si le tableau est beau mais l’aiguille immobile, c’est l’animation de la fiche 4 qu’il faut contrôler, pas cette peinture.


<a name="comparaison-cockpit"></a>

## F · Le jeu des deux tableaux : la radio et le compas

**1. Trouve le problème.** Sur la première image, pars du grand cadran de gauche (l’altimètre). Suis son bord vers deux heures, comme sur une horloge. Le petit rond de la radio mord sur ce bord. Puis regarde entre les deux cartes crème du bas : cet espace est vide.

![Avant : la radio touche le bord supérieur droit de l’altimètre ; rien entre les deux cartes du bas.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/cockpit-comparaison-02/SW233-compas-avant.jpg)

**2. Prends deux repères sur la photo.** Ouvre la photo originale C-FYLP de 690 × 517 pixels citée dans la [fiche de mesures](01-mesures.md). Le centre de la bouche d’air est vers (346,177), celui de la radio vers (210,222) et celui du compas vers (344,253). Sur une photo, les lignes augmentent vers le bas ; sur notre planche, la hauteur augmente vers le haut. Avec 610 pixels pour une largeur supposée de 0,78 m, la radio serait à environ 0,174 m à gauche et 0,058 m sous la bouche. Le compas serait presque sur son axe et 0,097 m plus bas. Ces longueurs dépendent de la perspective et de la largeur supposée.

**3. Place les pièces.** Dans le bloc D bis, la bouche est en (0 ; 0,197). Pour le compas, choisis (0 ; 0,098) : dans la première version illustrée ici, le cadre et le trait étaient peints. Aujourd’hui, construis-les en relief à la fiche 2 (I ter) et laisse la peinture nue à cet endroit. Le trait est fixe : il ne donne pas le cap. Pour la radio, la place de l’altimètre actuel oblige à adapter le dessin : passe le centre de (−0,145 ; 0,169) à (−0,141 ; 0,189) et le rayon extérieur de 0,039 à 0,031 m. Elle reste donc plus haute que sur la photo. Tu peux vérifier le jeu avec deux disques en papier : à l’échelle 1:1, les nouveaux rayons sont 92 et 31 mm, leurs centres sont distants d’environ 129 mm. Il reste **6 mm** entre les bords, contre environ **20 mm de chevauchement** auparavant. Ce sont les dimensions de notre maquette.

**4. Compare dans FlightGear.** Refais le paquet comme à la [fiche 7](07-essais.md), sélectionne SW233 et place-toi au siège avant. Les deux images ont été prises dans FlightGear 2024.1.7, à CYJN, en 1280 × 720, en lancement en vol à 4 000 ft, cap initial 010°, le 21 juin à 16 h 45 UTC. Pour retrouver notre cadrage de comparaison, ouvre le navigateur de propriétés dans le menu Débogage et, sous `/sim/current-view`, règle `view-number` à 0, les décalages `x-offset-m`, `y-offset-m`, `z-offset-m` à 0, 0.50 et 1.70, `heading-offset-deg` à 0, `pitch-offset-deg` à −23 et `field-of-view` à 70. Saisis un point dans les décimales. Ce cadrage sert à comparer les images ; la hauteur réelle de l’œil du pilote reste à mesurer.

![Après : un espace noir sépare les cerclages ; le boîtier du compas apparaît sous la bouche d’air.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/cockpit-comparaison-02/SW233-compas-apres.jpg)

**À toi.** Cache cette légende. Montre l’espace entre la radio et l’altimètre, puis le compas et la boule de largage. Si le compas manque, vérifie d’abord que FlightGear a chargé **la copie reconstruite** de l’avion. Si tout le tableau paraît plus grand ou plus petit, vérifie le champ de vision avant de changer tes mesures.


<a name="compas-relief"></a>

## G · Comment savoir si le compas dépasse vraiment ?

**1. Avant de comparer.** Le compas de la séance F était imprimé sur la même feuille que les cartes. Pour cette séance, fabrique le boîtier avec la [recette et le dessin en coupe, fiche 2, I ter](02-maillage.md). Dans la fiche 6, ne dessine plus le compas sur la texture : deux traits, l’un imprimé et l’autre en relief, donneraient une double image de côté. Reconstruis ton paquet. Aucun réglage d’animation n’est nécessaire.

**2. De face, cherche des repères communs.** Ouvre les images en grand et passe de l’une à l’autre. Partant de la bouche ronde, descends jusqu’au petit trait blanc. Vérifie que le compas reste entre les deux cartes crème et que tu vois leurs bords. La vue de face sert à contrôler la position ; elle seule ne prouve pas la profondeur.

![Avant, de face : la fenêtre peinte entre les deux cartes.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-relief-03/compas-plat-face.jpg)

![Après, de face : même caméra, cadre en relief et trait derrière la vitre.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-relief-03/compas-relief-jour-face.jpg)

**3. Penche la tête.** Reprends le cadrage de la séance F, mais déplace maintenant l’œil sur le côté. Dans les propriétés de la vue, mets *x-offset-m* à **0.23**, *heading-offset-deg* à **16** et *field-of-view* à **48**. Garde la hauteur, le recul et l’inclinaison de F. Tourner la caméra sans déplacer l’œil ne ferait pas apparaître la même paroi. Sur l’image plate, le bord reste collé au tableau. Sur la nouvelle image, trouve la paroi entre la planche et la lèvre du cadre. Suis ensuite le bord de la fenêtre jusqu’au trait clair plus profond.

![Avant, de biais : ancien compas peint, sans flanc entre le cadre et la planche.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-relief-03/compas-plat-biais.jpg)

![Après, de biais : le boîtier sort de la planche ; le trait est à l’intérieur.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-relief-03/compas-relief-jour-biais.jpg)

**4. Change la lumière, pas la caméra.** Ces captures natives utilisent FlightGear 2024.1.7 à CYJN, le 21 juin 2026. Les deux premières paires sont prises avec le départ à 16 h 45 UTC ; relance le même scénario à **22 h 00 UTC** pour le deuxième éclairage. Garde la résolution 1280 × 720 et les mêmes valeurs de caméra. Compare les objets du tableau : le paysage et les aiguilles peuvent varier entre deux lancements.

![Le soir, de face : retrouve le repère clair au centre du compas.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-relief-03/compas-relief-soir-face.jpg)

![Le soir, de biais : compare la paroi et la fenêtre avec la même vue de jour.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-relief-03/compas-relief-soir-biais.jpg)

**Si ça ne marche pas.** Si tout est plat, vérifie que le maillage installé contient *compas-cadre* et que FlightGear utilise ton nouveau paquet. Si le trait est caché, vérifie d’abord que l’ouverture du cadre est vide, puis que la vitre utilise le matériau transparent. Le trait reste toujours fixe. Dans la [séance suivante](04-configuration.md#rose-magnetique), les graduations défilent derrière lui.

**Pour aller plus loin :** sur la photo verticale en vol, retrouve les chiffres derrière le trait fixe. Sur notre maquette, seul le trait est présent. Le [guide des cinq vues et du compas FSX](../references/cockpits-et-fsx.md) explique pourquoi le prochain élément à fabriquer est une bande graduée mobile.

## H · Finition du tableau — VIS-01f

Travail préparé par le commit `0b2a97a`, vérifications documentées le 16 novembre 2026. La photo C-FYLP du fonds local guide les couleurs et l'aspect ; elle ne fournit pas les dimensions des vis ni la réflectance de la peinture. Les choix suivants sont artistiques et restent estimés.

1. Dans la partie A, réduis le grain : `randrange(25, 33)` produit les entiers 25 à 32. La graine 233 garde le même dessin à chaque fabrication. Cela assombrit et adoucit la peinture.
2. Dans `screw`, dessine successivement l'ombre décalée, la rondelle, la tête et la fente. Les deux arcs opposés donnent une impression de relief. Ce relief est peint : il ne change pas avec le soleil comme une vraie vis en 3D.
3. Dans la boucle des cadrans, utilise trois anneaux sombres et deux arcs fins. Ne touche pas aux graduations ou aux aiguilles : ce sont des éléments séparés.
4. Dans `card`, dessine un support noir légèrement plus grand, puis la carte blanc cassé. Les textes restent des rappels simplifiés de simulation, pas une transcription complète des procédures réelles.
5. Reconstruis le paquet avec `python tools/package.py --output build/tableau-test`. Choisis un dossier neuf. Les textures générées restent hors des sources Git.

![Texture originale du tableau, sans aiguilles mobiles](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-21/panel.png)

Cette image montre les vis, bordures et supports produits par les blocs ci-dessus. Les valeurs en mètres sont celles de notre maquette ; aucun relevé physique supplémentaire n'a été obtenu.

### Comparaison native, cadrage identique

FlightGear 2024.1.7, CYJN, simulation figée, vue pilote, azimut caméra 0°, inclinaison −18°, champ 55°. Deux orientations du planeur, 010° et 100°, modifient l'éclairage relatif ; ce ne sont pas deux heures de la journée. Le cadrage rapproché coupe le bas du variomètre. Les heures locales enregistrées des deux sessions diffèrent de quelques secondes.

Avant, orientation 010° :

![Avant 010](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-21/avant-010.jpg)

Après, orientation 010° :

![Après 010](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-21/apres-010.jpg)

Avant, orientation 100° :

![Avant 100](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-21/avant-100.jpg)

Après, orientation 100° :

![Après 100](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-21/apres-100.jpg)

Pour reproduire, charger un paquet dans une session dédiée avec interface HTTP, mettre explicitement la simulation en pause, puis lancer `python -m tools.panel_bench build/captures --port 18107` depuis le dépôt. Le programme refuse une session non figée ou une image trop petite ; il restaure les paramètres de caméra après capture. Le port doit correspondre à la session réellement ouverte.

### Résultat et limites

La peinture est moins granuleuse, les bordures plus sombres et les supports de cartes mieux séparés. Le tableau reste schématique : éclairage peint, radio décorative, plaques simplifiées, dimensions estimées. Il ne s'agit pas encore d'un cockpit photographique.

Les textures des trois cadrans et le XML des animations sont identiques octet par octet avant/après. La reconstruction depuis le tutoriel passe. Le nouvel essai visuel de l'aiguille d'anémomètre a produit des images 1 × 1 après minimisation : elles sont rejetées. La reprise du 16 novembre a trouvé la session HTTP indisponible. Ce nouvel essai et l'actualisation de l'aperçu général restent à refaire ; aucune validation dynamique nouvelle n'est revendiquée.

## I · Validation finale du tableau — 16 novembre 2026

Plan préalable `ac91e15`. Une session neuve FlightGear 2024.1.7 charge le paquet à CYJN. On fige explicitement la simulation et son horloge avant de lancer le banc. Les anciennes images 1 × 1 sont rejetées ; le banc vérifie désormais au moins 1024 × 600 pixels avant d'enregistrer une capture comme résultat.

### Refaire les quatre lectures

Depuis la racine du dépôt, avec une session dédiée figée et son interface HTTP au port 18108 :

```powershell
python tools/airspeed_bench.py build/lecture-tableau --port 18108
python -m tools.enclosure_bench build/vues-tableau --port 18108
```

Choisis des dossiers neufs. Le premier programme désactive temporairement le calcul de l'anémomètre, injecte l'indication, vérifie sa stabilité avant/après capture puis restaure l'indication et l'état de fonctionnement précédents. Le second photographie l'appareil et la vue pilote. Garde la fenêtre restaurée pendant les captures.

| Entrée imposée (kt) | Lecture attendue (mph) |
|---|---:|
| 40 | 46,031 |
| 60 | 69,047 |
| 85 | 97,816 |
| 120 | 138,094 |

Ces valeurs vérifient seulement l'affichage et l'animation. Elles ne sont pas des vitesses recommandées ou un essai de l'enveloppe réelle. Conversion : kt × 1852 / 1609,344.

![Lecture injectée 40 kt dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-22/ias-40.jpg)

![Lecture injectée 60 kt dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-22/ias-60.jpg)

![Lecture injectée 85 kt dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-22/ias-85.jpg)

![Lecture injectée 120 kt dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-22/ias-120.jpg)

### Cockpit complet et paquet

![Cockpit complet, capture native](https://github.com/steveprudhomme/sw233-flightgear/releases/download/tableau-22/cockpit.jpg)

Les quatre images ont été examinées : la position de l'aiguille correspond aux valeurs attendues. Le CSV conserve les entrées avant et après chaque capture. La vue complète montre les instruments sans la coupe du cadrage rapproché précédent. Cette image sert au nouvel aperçu du paquet ; la description mentionne les finitions du tableau. La présentation dans le sélecteur n'a pas fait l'objet d'un nouvel essai d'interface.

VIS-01f est clos pour la finition et sa validation visuelle. Cela ne valide ni la polaire ni une fidélité photographique complète. Les ombres des vis restent peintes ; l'aérateur et les bordures pourront faire l'objet d'un prochain lot de relief 3D.

## Aérateur en relief

La grille peinte est retirée : la [recette et les quatre pièces 3D](02-maillage.md#aérateur--pièces-et-vérification-native) la remplacent. Le fond de peinture reste uni à cet emplacement.

## Bordure 3D de l'anémomètre

À cette étape historique, la condition `title != "AIR SPEED  /  MPH"` réservait les anneaux et vis peints aux deux autres instruments. Depuis VIS-01j, les trois instruments ont des bordures 3D. L'inscription sous le cadran est conservée. La [bague et ses fixations](02-maillage.md#anémomètre--pièces-et-essais-du-relief) remplacent le dessin ; aucune modification des arcs colorés, nombres ou aiguilles.

## Bordure de l’altimètre en relief

À l’étape VIS-01i, la boucle ne peignait plus les anneaux et fixations que pour VERTICAL SPEED. Depuis VIS-01j, ces derniers doublons peints sont retirés aussi. Altimètre et anémomètre utilisent leur géométrie ; inscriptions et cadrans restent inchangés. Voir les [pièces et essais](02-maillage.md#altimètre--pièces-et-vérification-du-relief).

## J · Régler l'altimètre à la souris

Essai VIS-01i du 16 novembre 2026 ; plan préalable `aff6ff6`. Paquet alt-bague-25 inchangé, FlightGear 2024.1.7, CYJN, FDM null. Le calage a été lu par l'interface de propriétés, mais **aucune valeur de calage n'a été écrite par le banc pendant ces gestes** : les changements proviennent de glissements de souris injectés dans la fenêtre native.

### Le geste à apprendre

1. Repère le bouton rond en bas à gauche du cadran.
2. Place le pointeur sur sa face, maintiens le bouton gauche et fais glisser horizontalement vers la droite, puis relâche : le calage augmente.
3. Repars du bouton et glisse vers la gauche pour diminuer.
4. Vérifie le repère du bouton et les aiguilles. Ne confonds pas la petite rotation avec une absence d'effet : le pas relevé dans cet essai est de 0,01 inHg.

L'essai de molette vers le haut n'a produit aucun changement. Un clic simple sans déplacement n'a pas été validé comme geste de réglage. Il faut documenter le geste efficace, pas promettre toutes les interactions possibles.

| Vue et geste | Calage avant → après (inHg) | Indication après (ft) |
|---|---|---:|
| Face, molette vers le haut | 29,92 → 29,92 | 0 |
| Face, glissement à droite | 29,92 → 29,93 | 9,084933 |
| Face, glissement à gauche | 29,93 → 29,92 | 0 |
| Biais, glissement à droite | 29,92 → 29,93 | 9,084933 |
| Biais, glissement à gauche | 29,93 → 29,92 | 0 |

Cette variation indique que la commande est reçue. La pression statique du banc null reste 29,92 inHg ; ce résultat ne valide pas une précision en vol. Le calage initial est restauré par le dernier glissement.

### Images de contrôle

![Face : augmentation](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-26/drag-plus.jpg)

![Face : diminution](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-26/drag-moins.jpg)

![Biais : augmentation](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-26/biais-plus.jpg)

![Biais : retour au calage initial](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-26/biais-moins.jpg)

### Reproduire les cadrages et comprendre les limites

Vue rapprochée : inclinaison −25°, champ 24°, x caméra −0,22 m, y 0,5 m, z 1,7 m, azimut 0°. Pour le biais, x devient −0,30 m et azimut −5°. Les glissements testés parcouraient environ 63 pixels ; ce nombre décrit l'essai, pas une garantie de pas par pixel. Les coordonnées changent si la fenêtre ou la caméra change : viser la face visible du bouton.

Les images proviennent de FlightGear ; les petits fichiers JSON joints à la publication consignent les valeurs après chaque geste. Le lot VIS-01i est clos pour la géométrie et cette interaction. Aucun code d'aéronef n'a changé : conserver le paquet alt-bague-25 et son aperçu. La fenêtre de pression non chiffrée reste une amélioration future ; toutes les positions possibles de caméra n'ont pas été testées.

## K · Variomètre en relief — vérifier et comparer

Le lot VIS-01j commence par le commit de plan `a0da1e0`. La photo C-FYLP fournie sert de référence de disposition ; le relief de 8 mm est estimé, et n'est pas mesuré sur cette photo. Voir les [choix de dimensions et la recette complète](02-maillage.md#bague-du-variomètre--vis-01j) et le [registre des références](../references/cockpits-et-fsx.md). Le résultat reste une représentation simplifiée, pas une reproduction photographique achevée.

### 1. Comprendre ce qui change

Avant, la bordure et les vis étaient dessinées sur une surface plate. Maintenant, elles possèdent des côtés. Les trois nouveaux objets sont `vsi-bague`, `vsi-vis` et `vsi-fentes`. Le centre du cadran et les 59 objets précédents ne changent pas. Une comparaison des faces du maillage l'a vérifié. Les textures `vsi.png`, `ias.png` et `alt.png` sont identiques à celles du paquet alt-bague-25 ; seule la peinture du tableau perd les doublons de la bordure et des vis.

Imagine une rondelle posée sur une feuille : tu dois toujours pouvoir lire les nombres écrits dans son trou. C'est le principe de notre contrôle.

### 2. Reconstruire puis lancer une session de contrôle

Travaille depuis la racine du dépôt, là où se trouve README.md. Il faut Python avec Pillow, FlightGear et le terrain CYJN déjà installés, comme expliqué dans la [fiche d'installation](12-installation.md). Choisis des dossiers de sortie qui n'existent pas encore. Construis le paquet, puis ouvre une session séparée du vol habituel. Sous Windows, remplace les trois chemins d'installation par les tiens ; garde les guillemets.

```powershell
# Vérifier que les blocs du tutoriel reconstruisent les sources.
python tools/check_workbook.py build/atelier-vario
# Préparer un paquet neuf.
python tools/package.py --output build/vario-relief
# Session statique dédiée : aucune dynamique de vol n'est calculée ici.
& "C:/Program Files/FlightGear 2024.1/bin/fgfs.exe" --fg-root="C:/Users/steve/FlightGear/Downloads/fgdata_2024_1" --fg-aircraft="$PWD/build/vario-relief/Aircraft" --fg-scenery="C:/Users/steve/FlightGear/Downloads/TerraSync" --aircraft=sw233 --airport=CYJN --in-air --altitude=5000 --heading=10 --fdm=null --httpd=18113 --read-only --ignore-autosave --enable-clock-freeze --start-date-gmt=2026:06:21:16:45:00 --geometry=1280x720 --disable-real-weather-fetch --disable-terrasync
```

Attends de voir le cockpit. Laisse la fenêtre ouverte, sans la minimiser. Lance les commandes suivantes dans un second terminal, également à la racine du dépôt. Le port doit être identique dans les deux commandes et dans FlightGear ; ne réutilise pas celui d'une autre session.

```powershell
# Sept indications de face, puis sept de biais.
python tools/variometer_bench.py build/vario-face --port 18113
python tools/variometer_bench.py build/vario-biais --port 18113 --oblique
```

### 3. Comprendre ce que fait le banc

Le banc mémorise la caméra, la visibilité du menu, l'indication et l'état de fonctionnement de l'instrument. Il désactive temporairement le calcul de cet instrument avec `serviceable=0`, puis écrit une indication connue. Il lit la propriété avant et après la capture pour vérifier qu'elle n'a pas changé. Il rejette les images de moins de 1 024 × 600 pixels et restaure les valeurs mémorisées à la fin, même en cas d'erreur de capture.

La caméra de face utilise x = 0,295 m, y = 0,5 m, z = 1,7 m, une inclinaison de −30° et un champ de 22°. De biais, x devient 0,375 m et l'azimut vaut +5°. Ces réglages sont un cadrage d'essai, pas une position d'œil mesurée sur un pilote.

### 4. Lire les résultats

Essais natifs FlightGear 2024.1.7, session FDM null à CYJN. Dans les deux séries, chaque valeur lue avant et après l'image correspond à l'entrée demandée. Le cadran exprime des centaines de pieds par minute : « 5 » signifie 500 ft/min. UP est la branche positive ; DOWN la branche négative.

| Entrée imposée (ft/min) | Lecture à chercher | Face | Biais |
|---:|---|---|---|
| −2 000 | 20, côté DOWN | vérifiée | vérifiée |
| −1 000 | 10, côté DOWN | vérifiée | vérifiée |
| −500 | 5, côté DOWN | vérifiée | vérifiée |
| 0 | zéro à gauche | vérifiée | vérifiée |
| +500 | 5, côté UP | vérifiée | vérifiée |
| +1 000 | 10, côté UP | vérifiée | vérifiée |
| +2 000 | 20, côté UP | vérifiée | vérifiée |

Ces essais contrôlent le passage de l'aiguille devant le nouveau relief. Ils ne prouvent ni le taux réel de montée, ni le retard pneumatique de l'instrument. Les essais de vol antérieurs sont décrits dans la [fiche 7](07-essais.md#banc-variometre) ; ils ne constituent pas un nouveau vol avec ce relief.

### 5. Comparer les images

Avant et après à indication nulle : même caméra et même cap. Observe le côté de la bague et les vis, sans confondre un changement d'ombre avec un changement de cadran.

![Avant : bordure peinte](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/avant.jpg)

![Après : bague et vis en relief](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/face-vario-0.jpg)

![Face : entrée imposée -2000 ft/min](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/face-vario--2000.jpg)

![Face : entrée imposée -1000 ft/min](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/face-vario--1000.jpg)

![Face : entrée imposée -500 ft/min](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/face-vario--500.jpg)

![Face : entrée imposée 500 ft/min](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/face-vario-500.jpg)

![Face : entrée imposée 1000 ft/min](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/face-vario-1000.jpg)

![Face : entrée imposée 2000 ft/min](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/face-vario-2000.jpg)

Sept vues de biais, réunies en planche pour comparer la course. Les JPEG natifs individuels sont joints à la publication.

![Série de biais](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/serie-biais.jpg)

![Tableau complet dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/cockpit.jpg)

### 6. Vérifier ton propre travail

Cherche une graduation cachée, une tête de vis qui passe devant l'aiguille ou une bordure peinte restée derrière la pièce. Si l'image est vide, restaure la fenêtre puis recommence dans un nouveau dossier. Compare les CSV avec les captures : une jolie image seule ne suffit pas à montrer la bonne valeur. Les fentes et vis de ce lot sont fixes, sans interaction.

La reconstruction du tutoriel, le contrôle des sources, le contrôle de style et la vérification du manifeste du paquet ont réussi. La description FlightGear mentionne maintenant les trois bagues ; son aperçu est renouvelé. Les limites restent les dimensions estimées, les deux cadrages testés et l'absence de nouvelle validation dynamique.

[Paquet et preuves de ce lot](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/vario-bague-27) · [CSV et contrôles de non-régression](https://github.com/steveprudhomme/sw233-flightgear/releases/download/vario-bague-27/releves.zip).

## L · Fenêtre de calage de l'altimètre

### 1. Examiner la référence sans deviner

La photo C-FYLP fournie montre l'altimètre à gauche, mais ne permet pas de lire avec certitude l'unité de sa petite fenêtre ni d'identifier son mécanisme. Une zone floue n'est pas une mesure. Notre bouton utilise déjà les pouces de mercure, nommés inHg dans FlightGear. L'affichage reprend cette unité, explicitement inscrite sous le nombre.

Il s'agit d'une fenêtre numérique horizontale simplifiée, pas d'une reproduction attestée d'un tambour de C-FYLP. Ce choix favorise la lisibilité ; sa fidélité photographique reste à améliorer avec une meilleure référence. Le plan a été commité avant les travaux (`21e793e`). Le [registre des photos](../references/cockpits-et-fsx.md) distingue les appareils réels des vues d'autres simulateurs.

### 2. Calculer les dimensions du dessin

Le cadran est une image de 512 × 512 pixels représentant 166 × 166 mm. Chaque pixel représente donc 166 ÷ 512 = 0,3242 mm dans le modèle.

1. Dans la recette de cette fiche, trouve la fenêtre dessinée juste avant `alt.save`. L'ancienne allait de (381, 222) à (423, 290) : seulement 42 pixels de large.
2. Le nouveau rectangle va de (336, 220) à (448, 292). Garde les coins arrondis, le fond sombre et la bordure grise. La ligne est déjà corrigée dans le bloc à recopier.
3. Calcule sa largeur : 112 × 166 ÷ 512 = 36,31 mm. Sa hauteur : 72 × 166 ÷ 512 = 23,34 mm. Ce sont des dimensions choisies pour notre dessin, pas relevées sur l'appareil.
4. Pour convertir un pixel horizontal u en position, utilise y = −0,303 + u × 0,166 ÷ 512. Verticalement, z = 0,170 − v × 0,166 ÷ 512 : on descend dans l'image quand v augmente.
5. Le centre est proche de y = −0,176 m, z = 0,087 m. Place le nombre au-dessus et l'unité au-dessous, avec les coordonnées XML expliquées dans la [fiche 4](04-configuration.md#fenêtre-de-calage--vis-01k).
6. Ne peins pas « 29.92 » dans la texture : le texte XML lit le véritable réglage et change quand on déplace le bouton.

Les aiguilles restent devant la fenêtre et peuvent la recouvrir brièvement à certaines altitudes. Le texte n'est pas un élément flottant toujours visible au-dessus de l'instrument. Le maillage AC3D est inchangé.

### 3. Reconstruire et préparer une session dédiée

Travaille depuis la racine du dépôt, où se trouve README.md. Utilise des dossiers de sortie neufs. La section K ci-dessus donne la commande complète pour lancer FlightGear ; adapte le paquet et utilise le port 18115, avec `--fdm=null --httpd=18115`. Laisse la fenêtre visible. Le banc refuse une session qui ne correspond pas au SW233 avec FDM null.

```powershell
# Vérifier les blocs du tutoriel dans un dossier neuf.
python tools/check_workbook.py build/atelier-calage
# Construire le paquet à charger dans FlightGear.
python tools/package.py --output build/calage-fenetre
# Après chargement de ce paquet en session FDM null, port 18115 :
python tools/pressure_window_bench.py build/calage-face --port 18115
python tools/pressure_window_bench.py build/calage-biais --port 18115 --oblique
```

### 4. Vérifier huit valeurs sous deux angles

Le banc impose 28.00, 28.92, 29.92, 29.99, 30.00, 30.01, 30.92 et 31.00 inHg. Il lit la propriété avant et après chaque capture, enregistre aussi l'altitude indiquée et refuse les images vides. Il restaure ensuite le calage, le fonctionnement de l'instrument, le menu et la caméra. Les fichiers `session.json` confirment cette restauration.

Dans le CSV, `expected_text` est une attente, pas une reconnaissance automatique des chiffres. Il faut ouvrir les images pour comparer. Les seize affichages ont été examinés dans FlightGear 2024.1.7 : valeurs correctes, passage 29.99 → 30.00 → 30.01 correct et zéros finaux conservés.

Caméra : inclinaison −25°, champ 24°, y = 0,5 m et z = 1,7 m. De face : x = −0,22 m et azimut 0°. De biais : x = −0,30 m et azimut −5°. Ce sont des cadrages d'essai, pas une position d'œil mesurée.

Les deux planches suivantes réunissent des recadrages des captures natives. Les JPEG complets sont joints à la publication.

![Contrôle face-lectures](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/face-lectures.jpg)

![Contrôle biais-lectures](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/biais-lectures.jpg)

![Contrôle face-pression-29.92](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/face-pression-29.92.jpg)

### 5. Manipuler le bouton et regarder le nombre

Place le pointeur sur le bouton rond en bas à gauche, maintiens le bouton gauche, glisse vers la droite et relâche. Repars de sa face, puis glisse vers la gauche. Recommence avec la vue de biais. Vise le bouton visible : ses coordonnées en pixels changent avec la caméra.

| Vue | Geste | Propriété après le geste (inHg) | Fenêtre lue |
|---|---|---:|---|
| Face | Droite | 29,93 | 29.93 |
| Face | Gauche | 29,92 | 29.92 |
| Biais | Droite | 29,93 | 29.93 |
| Biais | Gauche | 29,92 | 29.92 |

Pendant ces quatre gestes, aucune pression n'a été écrite par l'interface de test. Les JSON joints sont des lectures après manipulation. Le dernier geste restaure le calage initial. La molette n'a pas été retestée dans ce lot ; son ancien essai est décrit en section J.

![Essai souris : face-plus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/souris-face-plus.jpg)

![Essai souris : face-moins](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/souris-face-moins.jpg)

![Essai souris : biais-plus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/souris-biais-plus.jpg)

![Essai souris : biais-moins](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/souris-biais-moins.jpg)

### 6. Interpréter correctement les preuves

Ces essais valident l'affichage et sa liaison au bouton. Le FDM null ne calcule pas un vol réel : ils ne prouvent pas la précision barométrique. Les extrêmes 28.00 et 31.00 sont vérifiés comme valeurs affichées ; aucun nouvel essai de butée à la souris n'est revendiqué. Les deux vues ne couvrent pas toutes les positions possibles de caméra.

Le maillage et les douze animations antérieures sont inchangés. La police est fournie par FlightGear et n'est pas copiée dans le dépôt. Le contrôle des sources, le style Python, la reconstruction depuis le tutoriel et le manifeste du paquet sont vérifiés avant publication. La description et l'aperçu FlightGear sont actualisés.

![Cockpit avec calage chiffré](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/cockpit.jpg)

[Paquet et captures complètes](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/calage-fenetre-28) · [CSV et relevés JSON](https://github.com/steveprudhomme/sw233-flightgear/releases/download/calage-fenetre-28/releves.zip).

## M · Façade de radio en relief

### 1. Regarder la référence et définir le périmètre

Le plan préalable est le commit `5990da5`. La photo C-FYLP (fichier commençant par `5d81c6bf`, décrit dans le [registre des références](../references/cockpits-et-fsx.md)) guide la disposition : façade ronde à gauche de la carte avant décollage, écran en haut, boutons de tailles différentes. Le centre et le diamètre de notre modèle sont conservés. La photo ne donne pas une profondeur ni un diamètre constructeur fiable.

Le but de ce lot est une façade en relief. Les boutons restent fixes, l'écran reste sans fréquence et la pastille rouge est décorative. Nous n'attribuons pas un modèle commercial précis à cette radio et nous n'inventons pas les inscriptions illisibles. Le texte COM reste le seul libellé sur sa face. La texture est un dessin original, pas une photo collée sur le modèle.

### 2. Choisir les dimensions sans les présenter comme mesurées

| Élément | Dimension de maquette | Pourquoi |
|---|---|---|
| Centre | y = −0,141 m, z = 0,189 m | Conserver la disposition déjà utilisée |
| Rayon extérieur | 31 mm | Conserver l'encombrement de l'ancien dessin |
| Rayon de face | 29 mm | Réserver une bande de 2 mm au contour incliné |
| Avant de la façade | 6 mm devant le tableau | Faire apparaître le relief ; estimation |
| Écran | 33 × 8,5 mm | Loger une ouverture au-dessus du centre ; estimation |
| Boutons gauche/droit | diamètres 9 / 12 mm | Représenter leur différence de taille |
| Face avant des boutons | 13 mm devant le tableau | Leur donner 7 mm de saillie au-dessus de la façade |

Pour contrôler le voisinage, soustrais les centres de l'altimètre et de la radio : 79 mm horizontalement et 102 mm verticalement. Avec Pythagore, leur distance vaut environ 129,02 mm. Soustrais les rayons 93 et 31 mm : il reste environ **5,02 mm** entre les contours circulaires dans le plan du tableau. C'est une vérification géométrique de notre maquette, pas un écart mesuré sur C-FYLP. Les vues natives contrôlent ensuite les effets de perspective.

La [fiche 2](02-maillage.md#façade-de-radio--vis-01l) fournit la recette complète des huit objets et les images de chaque pièce.

### 3. Peindre la façade et poser la texture

1. Dans la recette de cette fiche, repère l'ancien dessin radio entre les cartes et le compas. Retire ses disques et ses boutons peints. Garde l'inscription RADIO sous l'appareil ; sa position reste la même.
2. Crée une image originale de 512 × 512 pixels, nommée `radio.png`. Elle représente un carré de 62 × 62 mm, donc un pixel vaut environ 0,1211 mm.
3. Dessine un rectangle arrondi sombre entre (112, 128) et (400, 214), avec un fin contour. Il encadre la pièce d'écran ; il n'affiche aucune fréquence fictive.
4. Inscris COM au point (256, 268), avec une taille de 32 pixels. Le point central simplifie l'alignement ; ce texte ne change pas avec le simulateur.
5. Dans la liste qui associe les textures aux pièces, ajoute `radio-face`, `radio.png`, −0,172, 0,158, 0,062, 0,062. Les deux premières coordonnées situent le coin inférieur gauche dans le plan (y, z) ; les deux dernières donnent la largeur et la hauteur.
6. Pour chaque sommet, le programme calcule u = (y + 0,172) / 0,062 et v = (z − 0,158) / 0,062. Ces nombres indiquent où prendre la couleur dans l'image. La texture est carrée mais la pièce est ronde : les coins de l'image ne sont pas utilisés.

La recette complète plus haut et `tools/panel.py` sont identiques après reconstruction. Les boutons et les vis sont de vraies pièces indépendantes : on ne les repeint pas une deuxième fois sur cette texture.

![Texture originale de façade ; les coins sont hors de la pièce ronde](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/texture-radio.png)

### 4. Refaire les captures dans FlightGear

Depuis la racine du dépôt, où se trouve README.md, choisis des dossiers de sortie neufs. Il faut Python avec Pillow, FlightGear et le terrain CYJN, comme expliqué dans la fiche d'installation.

```powershell
# Reconstruire les sources depuis les blocs du tutoriel.
python tools/check_workbook.py build/atelier-radio
# Préparer un paquet neuf.
python tools/package.py --output build/radio-relief
# Ouvrir une session dédiée à l'examen visuel ; adapter les chemins d'installation.
& "C:/Program Files/FlightGear 2024.1/bin/fgfs.exe" --fg-root="C:/Users/steve/FlightGear/Downloads/fgdata_2024_1" --fg-aircraft="$PWD/build/radio-relief/Aircraft" --fg-scenery="C:/Users/steve/FlightGear/Downloads/TerraSync" --aircraft=sw233 --airport=CYJN --in-air --altitude=5000 --heading=10 --fdm=null --httpd=18116 --read-only --ignore-autosave --enable-clock-freeze --start-date-gmt=2026:06:21:16:45:00 --geometry=1280x720 --disable-real-weather-fetch --disable-terrasync
```

Attends que le cockpit soit chargé et laisse la fenêtre visible. Dans un deuxième terminal placé à la racine du dépôt, lance le banc :

```powershell
# Le port doit correspondre à celui de la session précédente.
python tools/radio_bench.py build/radio-captures --port 18116
```

Le banc impose un cadrage rapproché et prend quatre vues : face et biais, aux caps 010° et 100°. L'heure est identique ; changer le cap change l'éclairage relatif au tableau. Le FDM null garde une scène statique, sans validation du vol. Le banc sauvegarde et restaure la caméra, le cap et le menu ; il refuse les images vides. Son `session.json` décrit les réglages et les valeurs restaurées.

Caméra de face : x = −0,141 m, y = 0,5 m, z = 1,7 m, inclinaison −18°, azimut 0°, champ 20°. De biais : x = −0,221 m, azimut −5°. Ces cadrages ne représentent pas une position d'œil mesurée.

### 5. Comparer avant et après

Les captures suivantes viennent de FlightGear 2024.1.7. L'avant utilise le paquet calage-fenetre-28 ; l'après utilise la nouvelle façade. Les réglages de caméra et d'éclairage sont les mêmes pour chaque paire.

Avant, de face : dessin plat et boutons peints.

![Avant, de face : dessin plat et boutons peints.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/avant-face-10.jpg)

Après, de face : contour incliné, écran séparé et deux boutons en relief.

![Après, de face : contour incliné, écran séparé et deux boutons en relief.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/apres-face-10.jpg)

Avant, de biais : les boutons suivent la surface plane.

![Avant, de biais : les boutons suivent la surface plane.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/avant-biais-10.jpg)

Après, de biais : les boutons dépassent de la façade.

![Après, de biais : les boutons dépassent de la façade.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/apres-biais-10.jpg)

Second cap : vérifier les contours dans un autre éclairage.

![Second cap : vérifier les contours dans un autre éclairage.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/apres-face-100.jpg)

Second cap, de biais : le relief demeure distinct de la carte voisine.

![Second cap, de biais : le relief demeure distinct de la carte voisine.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/apres-biais-100.jpg)

### 6. Vérifier et reconnaître les limites

Dans les quatre vues contrôlées, le contour reste séparé de l'altimètre et de la carte ; les boutons ne masquent aucun instrument voisin. Le contrôle du maillage confirme que les 62 objets précédents sont inchangés. Les textures des trois cadrans et le fichier de leurs animations sont identiques à ceux du paquet précédent. Le modèle contient maintenant 70 objets de maillage.

Le style Python, le contrôle des sources, la reconstruction depuis le tutoriel et le manifeste du paquet sont vérifiés. La description FlightGear indique explicitement que la radio est fixe et son écran sans fréquence ; l'aperçu est actualisé.

Le résultat reste stylisé : profondeurs, teintes et emplacement exact des petites fixations sont estimés. Le choix de préserver l'encombrement actuel facilite l'intégration, mais ne garantit pas l'échelle réelle de l'instrument. Les fonctions de communication, les canaux et les actions des boutons restent un lot futur, à préparer avec une référence identifiable. La pastille rouge ne prouve pas que la radio est alimentée.

![Ensemble du cockpit](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/cockpit.jpg)

[Paquet et images complètes](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/radio-relief-29) · [Réglages et contrôles de non-régression](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-relief-29/releves.zip).

## N · Régler la fréquence COM1

### 1. Définir ce qui est reproduit

Le plan a été commité avant les travaux (`7508264`). Les références ne permettent pas d'identifier avec certitude toute la radio de C-FYLP. Nous réalisons donc une commande générique de simulation : affichage actif et réglages grossier/fin. Les [sources et limites](../references/radio-com.md) distinguent les exemples FlightGear des hypothèses sur la radio réelle.

Le nombre visible doit être celui de COM1 active dans FlightGear. Un clic doit modifier cette même propriété, pas une copie réservée à l'affichage. La section M décrit l'ancien lot visuel avec écran vide ; ce lot le rend réglable.

### 2. Assembler le fonctionnement

1. Recopie le fichier `src/SW233/Nasal/radio.nas` fourni dans la fiche 4. Sa fonction `tune` reçoit un nombre de crans et calcule la nouvelle fréquence.
2. Ajoute son chargement sous `<nasal>` dans `sw233-set.xml`. Le bloc complet de la fiche 4 est déjà synchronisé. Sans ce chargement, le clic ne trouverait pas `sw233_radio.tune`.
3. Dans `sw233-model.xml`, ajoute le texte `radio-frequence`, lié à `instrumentation/comm[0]/frequencies/selected-mhz`. Utilise trois décimales pour distinguer 118.300 de 118.325. Le bloc complet est également dans la fiche 4.
4. Relie les pièces par deux animations `pick`. Celle de gauche appelle ±40 crans, celle de droite ±1 cran. Un cran vaut 0,025 MHz. Les quatre actions sont dans le XML à recopier.
5. Dans la recette de texture de cette fiche, le libellé devient COM1 MHz. Cette inscription est une aide de notre simulation, pas un marquage attesté de l'appareil réel.
6. Reconstruis le paquet. Le maillage est inchangé : ses boutons deviennent manipulables grâce au XML et au module Nasal.

### 3. Utiliser les boutons

| Pièce de la radio | Clic gauche de la souris | Clic milieu de la souris |
|---|---|---|
| Petit bouton de gauche | +1 MHz | −1 MHz |
| Gros bouton de droite | +25 kHz | −25 kHz |

Le clic milieu est généralement l'appui sur la roulette, pas sa rotation. Le clic droit, le glissement et la rotation de molette ne sont pas les gestes de ce lot. Sans clic milieu disponible, utiliser le dialogue radio de FlightGear pour diminuer la fréquence. Les infobulles rappellent le pas et les gestes. Les boutons ne tournent pas encore ; l'affichage confirme la modification.

La commande accepte 118.000 à 136.975 MHz sur grille 25 kHz. Une action trop grande s'arrête à la limite. Une valeur extérieure sur une autre grille reste visible, mais nos boutons la laissent intacte. Pour reprendre le réglage, choisir une valeur de la grille 25 kHz dans le dialogue radio de FlightGear. Le diagnostic de développement se trouve dans `/sim/sw233/radio/message`.

### 4. Reproduire le banc

Place-toi à la racine du dépôt, où se trouve README.md. Utilise des dossiers de sortie neufs. Les prérequis Python/Pillow, FlightGear et terrain CYJN sont décrits dans la fiche d'installation.

```powershell
# Vérifier la reconstruction et fabriquer un paquet.
python tools/check_workbook.py build/atelier-com1
python tools/package.py --output build/radio-com1
# Adapter les chemins locaux ; garder une session de test FDM null.
& "C:/Program Files/FlightGear 2024.1/bin/fgfs.exe" --fg-root="C:/Users/steve/FlightGear/Downloads/fgdata_2024_1" --fg-aircraft="$PWD/build/radio-com1/Aircraft" --fg-scenery="C:/Users/steve/FlightGear/Downloads/TerraSync" --aircraft=sw233 --airport=CYJN --in-air --altitude=5000 --heading=10 --fdm=null --httpd=18117 --read-only --ignore-autosave --enable-clock-freeze --start-date-gmt=2026:06:21:16:45:00 --geometry=1280x720 --disable-real-weather-fetch --disable-terrasync
```

Attends le chargement du cockpit et laisse la fenêtre visible. Dans un deuxième terminal à la racine du dépôt :

```powershell
# Ce banc impose des entrées, appelle la fonction Nasal et relève les résultats.
python tools/radio_tuning_bench.py build/com1-essais --port 18117
```

Le banc vérifie la session SW233/FDM null, sauvegarde les fréquences et la caméra, puis exécute les cas ci-dessous. Il contrôle que COM1 en attente et COM2 active ne changent pas, puis restaure les valeurs mémorisées. `results.json` conserve les attentes et les lectures. Il n'y a pas de reconnaissance automatique des caractères : ouvre les images pour vérifier aussi ce qui est affiché.

### 5. Lire les résultats natifs

Les treize cas suivants ont réussi dans FlightGear 2024.1.7 ; leurs affichages ont été examinés.

| Départ MHz | Action | Résultat MHz |
|---:|---|---:|
| 118.300 | +25 kHz | 118.325 |
| 118.325 | −25 kHz | 118.300 |
| 118.975 | +25 kHz | 119.000 |
| 119.000 | −25 kHz | 118.975 |
| 123.450 | +1 MHz | 124.450 |
| 124.450 | −1 MHz | 123.450 |
| 118.000 | −25 kHz | 118.000, butée |
| 136.975 | +25 kHz | 136.975, butée |
| 118.025 | −1 MHz | 118.000, limite atteinte |
| 136.950 | +1 MHz | 136.975, limite atteinte |
| 125.125 | Valeur externe, zéro cran | 125.125 |
| 118.005 | +25 kHz demandé | Refus, valeur conservée |
| 117.000 | +25 kHz demandé | Refus, valeur conservée |

Les deux dernières valeurs sont imposées volontairement pour vérifier le refus. Elles ne prouvent pas la prise en charge d'une autre grille ou d'une fréquence hors plage. L'écran montre la propriété telle quelle, même en cas de refus.

![Treize lectures — recadrages des captures natives](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/lectures.jpg)

![Affichage natif à 118.325 MHz](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/fine-plus.jpg)

### 6. Vérifier les vrais clics

Appeler une fonction ne prouve pas que le clic atteint la bonne pièce. Huit clics ont donc été testés dans la fenêtre native, sans écrire la fréquence par le banc pendant ces gestes.

Dans chacune des deux vues, partir de 118.300 : bouton droit → 118.325 → 118.300 ; bouton gauche → 119.300 → 118.300. Les quatre cycles ont réussi. Le dernier clic restaure la fréquence initiale. Les fichiers JSON joints sont des lectures après geste.

Caméra de face : x = −0,141 m, y = 0,5 m, z = 1,7 m, inclinaison −18°, azimut 0°, champ 20°. De biais : x = −0,221 m, azimut −5°. Vise toujours la pièce visible ; les coordonnées de pixels changent avec la caméra.

![Souris : face-fin-plus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-face-fin-plus.jpg)

![Souris : face-fin-moins](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-face-fin-moins.jpg)

![Souris : face-gros-plus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-face-gros-plus.jpg)

![Souris : face-gros-moins](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-face-gros-moins.jpg)

![Souris : biais-fin-plus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-biais-fin-plus.jpg)

![Souris : biais-fin-moins](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-biais-fin-moins.jpg)

![Souris : biais-gros-plus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-biais-gros-plus.jpg)

![Souris : biais-gros-moins](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/souris-biais-gros-moins.jpg)

### 7. Reconnaître les limites

COM1 active est réglable. La façade n'ajoute ni mémoire ni bouton d'échange avec la fréquence en attente. La grille 8,33 kHz, le volume, la mise sous tension, l'écoute ATIS, FGCom et les communications réseau restent non validés. La pastille rouge est décorative, pas un témoin d'émission. Le réglage est fonctionnel ; ce n'est pas encore une radio complète.

La reconstruction du tutoriel, le contrôle des sources, le style Python et le manifeste du paquet sont vérifiés avant publication. Le maillage et les treize animations précédentes sont préservés. La commande générique facilite le prototype mais sa fidélité au modèle réel n'est pas démontrée ; ce compromis reste explicite.

![Cockpit avec COM1](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/cockpit.jpg)

[Paquet et captures](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/radio-com-30) · [Résultats et relevés](https://github.com/steveprudhomme/sw233-flightgear/releases/download/radio-com-30/releves.zip).

## O · Finition du compas

### 1. Comprendre le changement

La [fiche 2, section O](02-maillage.md#o--comprendre-la-finition-du-compas-pièce-par-pièce) donne les observations, les calculs et les images des huit objets. Le compas était déjà animé : nous améliorons son boîtier, pas sa logique. Le noir du cadre est homogénéisé ; un filet plus clair reste autour de la fenêtre. Le joint et les vis sont de vraies faces 3D, sans nouvelle photo collée sur le tableau. Le rendu reste une interprétation simplifiée, pas une reproduction photographique certifiée.

### 2. Comparer à cadrage identique

Ces quatre captures natives FlightGear 2024.1.7 utilisent une indication imposée de 090°. La lettre E doit rester sous le repère. La comparaison garde position, champ de vision, cap de l’avion et heure simulée identiques.

![Avant : cadre à coins coupés, vis plates](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/avant-face.jpg)

![Après : coins arrondis, joint et vis en relief](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/face-090.jpg)

![Avant de biais](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/avant-biais.jpg)

![Après de biais : têtes et rebord visibles](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/biais-090.jpg)

### 3. Refaire le banc de lecture

Un banc impose un chiffre connu pour vérifier le dessin. Il ne prouve pas que le compas réel réagit correctement en vol. Dans une session dédiée, utilise le paquet construit avec `tools/package.py`, comme à la fiche 12. Pour cet exemple, le paquet est dans `build/compas`. Depuis la racine du dépôt, avec Python et les dépendances installés :

```powershell
# 1. Construire dans un dossier neuf. Adapter les trois chemins FlightGear.
python tools/package.py --output build/compas
& "C:/Program Files/FlightGear 2024.1/bin/fgfs.exe" `
  "--fg-root=C:/Users/steve/FlightGear/Downloads/fgdata_2024_1" `
  "--fg-aircraft=$PWD/build/compas/Aircraft" `
  "--fg-scenery=C:/Users/steve/FlightGear/Downloads/TerraSync" `
  --aircraft=sw233 --airport=CYJN --in-air --altitude=5000 --vc=60 `
  --heading=010 --fdm=null --httpd=18119 --geometry=1280x720 `
  --start-date-gmt=2026:06:21:16:45:00 --enable-clock-freeze `
  --wind=0@0 --disable-real-weather-fetch --disable-terrasync `
  --read-only --ignore-autosave
# 2. Attendre que la scène soit visible. Dans un second terminal à la racine :
python tools/compass_bench.py build/essais-compas --port 18119
```

Le dossier de résultats doit être neuf. Le script vérifie SW233 et le mode `null`, sauvegarde la caméra et les propriétés, puis désactive temporairement le calcul de l’instrument avec `serviceable = 0`. Il impose neuf indications, prend les images et relit chaque valeur avant et après. Enfin il restaure les réglages et l’état de service initial, même si une erreur survient pendant les essais. Avec un instrument réactivé, l’indication évolue à nouveau normalement.

| Entrée | Ce qu’il faut regarder sous le repère |
|---|---|
| 000° | N |
| 045° | À mi-chemin entre 3 (030°) et 6 (060°) |
| 090° | E |
| 135° | Entre 12 et 15 |
| 180° | S |
| 225° | Entre 21 et 24 |
| 270° | W |
| 359°, 000°, 001° | N se déplace légèrement, sans rupture de la rose |

La vue de face utilise x = 0, y = 0,5, z = 1,7 m, inclinaison −26° et champ 17°. La vue de biais change x à −0,08 m et l’orientation horizontale à −5°. Ce sont des réglages de caméra du prototype, pas une mesure de la position de l’œil réel.

![Neuf indications de face : recadrages des captures natives](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/lectures-face.jpg)

![Les mêmes indications de biais](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/lectures-biais.jpg)

Les 18 valeurs sont restées stables pendant leurs captures. Les lettres cardinales et les positions intermédiaires ont été examinées sur ces images. Le programme vérifie les valeurs ; il ne reconnaît pas automatiquement les lettres. Les chiffres voisins sont partiellement cachés par les côtés de la fenêtre, comme auparavant : la lecture se fait au repère central. Les caractères restent dessinés par petits polygones et peuvent paraître anguleux en gros plan.

### 4. Vérifier le défilement pendant un vrai vol simulé

Ferme la session statique de cet atelier. Pour le vol, utilise JSBSim, le moteur de dynamique du paquet FlightGear, et laisse l’horloge active. N’ajoute ni `--fdm=null` ni `--enable-clock-freeze`. Depuis la racine du dépôt :

```powershell
# Ouvrir le paquet déjà construit, en vol au-dessus de CYJN.
python build/compas/launch.py `
  --fgfs "C:/Program Files/FlightGear 2024.1/bin/fgfs.exe" `
  --fg-root "C:/Users/steve/FlightGear/Downloads/fgdata_2024_1" `
  --scenery "C:/Users/steve/FlightGear/Downloads/TerraSync" `
  --mode air --http-port 18122
# Attendre la scène, garder la fenêtre visible, puis enregistrer.
python tools/record_compass.py build/vol-compas-visible --port 18122
# Produire le graphe, les images annotées et un film de 30 secondes.
# Matplotlib et FFmpeg sont nécessaires, comme à la fiche 7.
python tools/compass_report.py build/vol-compas-visible build/rapport-compas-visible
```

Le scénario initialise une fois l’avion, puis agit sur les commandes pour faire un virage à droite et un à gauche. Il lit le cap magnétique et l’indication du compas ; il n’impose pas la valeur de la rose. Le film rassemble cinq extraits à vitesse normale : les sauts d’heure indiquent les coupes. Le petit encadré agrandit le compas de la même capture.

**Deux pièges rencontrés et corrigés.** Une horloge figée empêchait le premier vol d’avancer. Ensuite une fenêtre non visible renvoyait des JPEG de 1 × 1 pixel : les valeurs étaient enregistrées, mais ces images ne montraient aucun avion. Ces essais n’ont pas servi de preuves visuelles. L’outil refuse maintenant une horloge figée et vérifie la taille de chaque capture, y compris avant le départ. Restaurer une fenêtre visible et refaire le vol dans un dossier neuf est indispensable. Ne jamais agrandir une image vide pour la présenter comme une capture valable.

Le vol retenu contient **880 relevés sur 145,1 s**, avec 880 images natives de 1280 × 720 pixels. Le scénario passe le nord à droite puis à gauche. Au premier passage (47,4 s), le cap magnétique vaut environ 000,5° et le compas 314,0° : on lit entre 30 et 33, pas N. C’est cohérent avec l’indication enregistrée ; cela ne prouve pas que cet écart reproduit l’instrument réel. À la fin, les indications sont de nouveau proches de 330°.

![Premier passage du nord, avec agrandissement du compas](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/vol-nord.jpg)

![Retour ailes à plat](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/vol-retour.jpg)

![Caps enregistrés pendant les deux virages](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/courbes.png)

[Voir les 30 secondes d’extraits du vol](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/compas-en-virage.mp4) · [Télécharger les relevés](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/releves.zip). Les données du vol précèdent légèrement chaque capture (lecture puis requête d’image) : le bandeau n’est pas une mesure synchronisée à la trame près.

### 5. Vérifier le projet et connaître les limites

La reconstruction complète depuis les blocs du tutoriel est vérifiée. Les 24 tests passent après mise à jour de deux anciens contrôles : les textes créés par le XML ne sont pas dans le maillage, et une action de clic n’a pas nécessairement une propriété directe. Les tests vérifient désormais les noms du maillage **et** les textes déclarés, ainsi que les commandes des actions. Les animations de l’appareil restent inchangées.

Le contrôle visuel confirme le dessin et son sens de défilement dans les vues essayées. Il ne certifie ni les dimensions, ni la compensation, ni les erreurs d’accélération et de virage du véritable instrument. La vue de biais sert à vérifier les dégagements ; la lecture précise se fait de face, au repère. Les caractères anguleux et le matériau de vitre simplifié restent des limites pour une future finition photographique. Voir les [sources et choix de conception](../references/compas-finition.md).

![Vue d’ensemble avec le compas fini](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/cockpit.jpg)

[Paquet et captures originales](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/compas-finition-31).

## P · Des lettres plus nettes pour le compas

### 1. Le but de cette étape

Les lettres du compas étaient faites de petits carrés. En gros plan, leurs bords ressemblaient à un escalier. Nous allons dessiner une étiquette, puis l’enrouler sur le tambour de la [fiche 2, section P](02-maillage.md#p--un-tambour-lisse-pour-recevoir-les-nouvelles-lettres). Le cadre, les vis, la vitre et le repère ne changent pas.

Ouvre la photo C-FYLP et les références du [dossier compas](../references/compas-finition.md). Elles servent à regarder les inscriptions claires sur fond sombre et leur disposition. Elles ne permettent pas d’identifier précisément la police de caractères. Nous utilisons donc celle fournie par Pillow, la bibliothèque de dessin déjà utilisée dans ce projet. Ce n’est pas une photographie découpée ni une police déclarée identique à celle du véritable instrument.

### 2. Préparer la feuille autocollante

Reprends les blocs `tools/panel.py` de cette fiche, dans leur ordre. Ils contiennent la recette complète mise à jour. Ne colle pas une deuxième copie du programme à la fin.

Notre image finale mesure **4 096 × 256 pixels**. Un pixel est un petit point de couleur sur l’écran. La largeur correspond au tour complet du tambour, la hauteur à ses 22 mm. Pour comprendre la longueur du tour : 2 × 3,1416 × 49 ≈ **308 mm**. La texture offre donc environ 13,3 pixels par millimètre dans le sens du tour. Ces nombres servent au dessin du modèle ; ce ne sont pas des mesures du compas réel.

Nous dessinons d’abord deux fois plus grand, à **8 192 × 512 pixels**, puis nous réduisons l’image avec le filtre `LANCZOS`. Imagine une grande lettre soigneusement dessinée, puis une photocopie plus petite : le contour paraît moins en escalier. Cela s’appelle le **lissage**.

![La bande complète avant de l’enrouler](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/compass.png)

Ouvre l’image seule pour voir les traits en grand. Le S est coupé aux deux bords : ce n’est pas une erreur. Ces bords vont se rejoindre.

### 3. Placer les lettres et les traits

| Repère | Place sur la largeur finale | Explication |
|---|---|---|
| E | 1 024 pixels | Un quart de 4 096 |
| N | 2 048 pixels | Le milieu |
| W | 3 072 pixels | Trois quarts |
| S | 0 et 4 096 pixels | Les deux bouts de la même lettre |

Il y a une inscription tous les 30° : **4 096 ÷ 12 ≈ 341,33 pixels** entre leurs centres. Il y a un trait tous les 5° : **4 096 ÷ 72 ≈ 56,89 pixels** entre les traits. Un trait sur deux est plus long. Les lettres sont centrées par `anchor="mt"` : cela signifie « milieu, en haut ».

Dans l’image, les lignes se comptent du haut vers le bas. La fonction `row` traduit la hauteur du modèle en ligne de pixels. Exemple : la ligne du haut, à +11 mm, devient 0 ; celle du bas, à −11 mm, devient 256. Le haut des lettres est placé à +1 mm, soit environ la ligne 116. Les grands traits vont de +10 à +4 mm ; les petits de +7 à +4 mm.

Pourquoi dessiner trois copies décalées ? Une copie reste sur la feuille, les deux autres débordent à gauche et à droite. Cela permet au S et au trait du sud de se retrouver correctement sur les deux bords. Les parties qui dépassent l’image sont simplement coupées.

### 4. Coller la bonne partie sur chaque face

Les lettres **u** et **v** servent d’adresses sur la feuille. `u` va de 0 à 1, de gauche à droite ; `v` va de 0 à 1, du bas vers le haut. Ce ne sont pas des mètres. Une face du tambour reçoit une tranche de 1/72 de la largeur de l’image.

Exemple : la première face utilise u = 0 à 1/72 ; la deuxième, 1/72 à 2/72. La dernière se termine à 1. Le bas utilise v = 0, le haut v = 1. Chaque face possède quatre sommets indépendants : `divmod(idx, 4)` retrouve son numéro de face et le coin demandé. Le programme ajoute `texture "compass.png"` à l’objet du paquet et écrit ces adresses après chaque numéro de sommet.

Les anciennes lettres en petits polygones sont retirées ; les conserver provoquerait une superposition. La peinture est créée dans le paquet, jamais ajoutée au fichier source de maillage. Les fichiers PNG générés restent hors du suivi Git ; leur recette est conservée et peut les refaire.

### 5. Garder les lettres lisibles dans l’ombre

Le premier essai avait des lettres trop sombres sous le deuxième éclairage. Nous avons ajouté un matériau réservé à la rose : `compass-finish`. Sa composante `emis .45 .45 .45` maintient une base de luminosité. C’est une aide de lisibilité du prototype, **pas la simulation d’un éclairage électrique réel**. Les autres matériaux du tableau ne changent pas.

![Avant : caractères en petits polygones](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/avant-face.jpg)

![Après : caractères lissés, même cadrage et indication E](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/10-face-090.jpg)

![Essai intermédiaire trop sombre, avant correction du matériau](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/contraste-initial.jpg)

![Après sous le deuxième éclairage](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/100-face-090.jpg)

### 6. Refaire les essais sans confondre les deux caps

Il y a ici deux nombres différents : **le cap de l’avion** choisit son orientation face au soleil ; **l’indication du compas** est le nombre imposé au banc pour vérifier le dessin. Le banc statique ne reproduit pas un vol.

Construis un paquet neuf avec `tools/package.py`, puis lance la session `--fdm=null` décrite en section O. Choisis le port 18124 à la place de 18119. Garde la fenêtre visible. Depuis la racine du dépôt, lance :

```powershell
# Premier éclairage : garder --heading=010 au lancement.
python tools/compass_bench.py build/compas-texture-10 --port 18124 --seams
```

Pour le deuxième éclairage, ferme cette session de test et relance-la avec `--heading=100`, toutes les autres options identiques. Puis lance :

```powershell
# Le dossier de résultats doit être neuf.
python tools/compass_bench.py build/compas-texture-100 --port 18124 --seams
```

Chaque série vérifie douze indications de face et de biais : 000, 045, 090, 135, 180, 225, 270, 359, 001, 179, 181 et 315°. Le mode `--seams` ajoute les trois dernières valeurs au banc précédent. **12 indications × 2 vues × 2 éclairages = 48 captures.** Le script relit chaque valeur avant et après la photo et refuse les images vides. Il restaure ensuite les réglages sauvegardés.

Regarde N/E/S/W au centre. À 045°, le trait doit être entre 3 et 6 ; à 315°, entre 30 et 33. Compare 359/000/001 : N se déplace un peu. Compare 179/180/181 : S se déplace sans se casser au raccord. Les chiffres coupés aux côtés du guichet ne sont pas le chiffre à lire : utilise le repère central.

![Douze indications, cap avion 10°, vue face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/lectures-10-face.jpg)

![Douze indications, cap avion 10°, vue biais](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/lectures-10-biais.jpg)

![Douze indications, cap avion 100°, vue face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/lectures-100-face.jpg)

![Douze indications, cap avion 100°, vue biais](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/lectures-100-biais.jpg)

### 7. Regarder depuis la place du pilote

Un beau gros plan ne suffit pas. Nous reculons la caméra pour revoir le tableau entier. Les deux images suivantes montrent le même compas réglé à E, sous les deux orientations de lumière. L’appareil reste au banc statique ; les autres cadrans ne décrivent pas ici un vol réel. La lettre est visible, mais le guichet demeure petit dans cette vue : l’amélioration ne remplace pas le besoin de rapprocher la vue pour lire précisément.

![Vue pilote, cap avion 010°](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/cockpit-10.jpg)

![Vue pilote, cap avion 100°](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/cockpit-100.jpg)

### 8. Savoir quand ton travail est terminé

- Les 48 valeurs restent stables pendant leur capture. Les quatre planches ont été examinées : les points cardinaux, les valeurs intermédiaires et les deux raccords sont lisibles au repère. Le script ne reconnaît pas les lettres à ta place : tu dois regarder les images.
- Les 71 autres objets et les cinq textures antérieures sont identiques. Le XML d’animation n’a pas changé.
- Les 24 tests du dépôt passent ; le contrôle de style et la reconstruction depuis les blocs du tutoriel passent aussi.
- Le paquet contient `compass.png` et le maillage qui la référence ; sa vérification de ressources contrôle ce lien.

**Ta petite vérification personnelle :** montre les planches à quelqu’un. Demande-lui de trouver E, S et la position entre 30 et 33. S’il doit deviner, rapproche la vue et vérifie le contraste avant de changer la taille de toutes les lettres.

Les profondeurs, la police et la luminosité restent des choix de maquette. L’animation est conservée, mais ce lot ne refait pas les essais dynamiques en vol du lot précédent et ne certifie pas un compas réel. Le tutoriel est écrit pour un débutant ; il reste à le faire relire et reconstruire sans aide par un enfant pour vérifier que les explications suffisent.

[Paquet et captures](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/compas-texture-32) · [Relevés des contrôles](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/releves.zip).

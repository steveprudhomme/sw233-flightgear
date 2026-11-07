"""Paint an original instrument panel from editable dimensions, without photographs."""

import math
import random
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def finish_panel(models: Path):
    """Decorate the packaged mesh; its three animated instruments stay independent."""
    w, h = 1536, 768
    rng = random.Random(233)
    noise = bytes(rng.randrange(35, 53) for _ in range(w*h))
    im = Image.frombytes("L", (w, h), noise).convert("RGB")
    pen = ImageDraw.Draw(im)

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

    for y, z, r, title in [(-.22,.087,.083,"ALT  /  FT"), (.17,.14,.075,"AIR SPEED  /  MPH"),
                            (.295,.022,.063,"VERTICAL SPEED")]:
        for extra, color in [(.009,"#141719"),(.007,"#777b78"),(.005,"#393c39")]:
            disc(y,z,r+extra,color)
        for i in range(4):
            a = (i+.5)*math.pi/2
            screw(y+(r+.008)*math.cos(a), z+(r+.008)*math.sin(a))
        label(y,z-r-.018,title,17)
    # Central vent and grille observed on the supplied C-FYLP cockpit photograph.
    for r, color in [(.046,"#141414"),(.044,"#6e706b"),(.042,"#34373a"),
                     (.037,"#505457"),(.034,"#141719")]:
        disc(0,.197,r,color)
    for j in range(-2,3):
        pen.line([xy(-.026,.197+j*.009+.003),xy(.026,.197+j*.009-.003)],
                 fill="#55585a", width=4)
    for y, z in [(-.30,.15),(-.36,.04),(.33,.11),(-.085,.24),(.082,.24)]:
        screw(y,z)
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
    ry, rz = -.141, .189
    for rr, tone in [(.031,"#171717"),(.029,"#686866"),(.027,"#323536")]:
        disc(ry,rz,rr,tone)
    x, v = xy(ry,rz)
    pen.rounded_rectangle((x-29,v-18,x+29,v-3), radius=3, fill="#71766a")
    label(ry,rz-.009,"COM",12)
    for dy in (-.014,.014):
        disc(ry+dy,rz-.018,.006,"#101214")
        disc(ry+dy-.001,rz-.017,.004,"#414441")
    label(ry+.010,rz-.038,"RADIO",11)
    # Le compas en relief est dans le maillage : ne pas le repeindre ici.
    label(0,.014,"LARGAGE",14)
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
    im.save(models/"panel.png")
    mesh = models/"sw233.ac"
    s = mesh.read_text()
    tag = 'OBJECT world'
    material = s[:s.index(tag)].count('MATERIAL ')
    s = s.replace(tag, 'MATERIAL "panel-finish" rgb 1 1 1 amb .6 .6 .6 emis .2 .2 .2 '
                  'spec .12 .12 .12 shi 12 trans 0\n'+tag, 1)
    for name,texture,ymin,zmin,span_y,span_z in [
        ("tableau","panel.png",-.4,-.1,.8,.4),("ias-fond","ias.png",.095,.065,.15,.15),
        ("vsi-fond","vsi.png",.232,-.041,.126,.126),
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
    mesh.write_text(s)

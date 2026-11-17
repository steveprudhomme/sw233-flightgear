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

    for y, z, r, title in [(-.22,.087,.083,"ALT  /  FT"), (.17,.14,.075,"AIR SPEED  /  MPH"),
                            (.295,.022,.063,"VERTICAL SPEED")]:
        # All three instrument rims and their fasteners are separate 3D objects.
        label(y,z-r-.018,title,17)
    # Original identification plaque below the altimeter: artistic placement,
    # not a measured feature of the current C-FYLP cockpit. No new geometry.
    x, v = xy(-.22, -.05)
    half_width, half_height = .0575*w/.8, .012*h/.4
    pen.rounded_rectangle((x-half_width, v-half_height, x+half_width, v+half_height),
                          radius=3, fill="#101518", outline="#707772", width=2)
    label(-.22, -.05, "C-FYLP", 27)
    # The central vent is now separate 3D geometry; leave the paint beneath it plain.
    for y, z in [(-.30,.15),(-.36,.04),(.33,.11),(-.085,.24),(.082,.24)]:
        screw(y,z)
    # Les cartes sont des rappels du simulateur, pas des consignes de vol réel.
    def card(y, z):
        x, v = xy(y, z)
        width, height = (89, 128) if y > 0 else (97, 140)
        box = (x-width/2, v-height/2, x+width/2, v+height/2)
        # Dark holder and warm-white card, inspired by the reference photograph.
        pen.rounded_rectangle((box[0]-4, box[1]-3, box[2]+4, box[3]+5),
                              radius=8, fill="#111416", outline="#565b59", width=2)
        pen.rounded_rectangle(box, radius=5, fill="#e3e1d5", outline="#b1b3a9", width=1)
        pen.line((x-41, v-39, x+41, v-39), fill="#4c4a44", width=1)
    for y,z in [(-.079,.197),(-.079,.077),(.073,.229),(.073,.035)]:
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
    # Opaque paint has its own response; retain the established dial material.
    paint_material = s[:s.index(tag)].count('MATERIAL ')
    s = s.replace(tag, 'MATERIAL "cockpit-paint" rgb 1 1 1 amb .6 .6 .6 '
                  'emis .14 .14 .14 spec .025 .025 .025 shi 6 trans 0\n'+tag, 1)
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
        selected_material = paint_material if name in {"tableau", "radio-face"} else material
        lines[ri-1] = f"mat {selected_material}"
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

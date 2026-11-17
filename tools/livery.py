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

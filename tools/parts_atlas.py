"""Draw an exhaustive orthographic atlas from editable AC3D geometry, not FG screenshots."""
import argparse
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def read_mesh(path):
    lines = path.read_text(encoding='utf-8').splitlines()
    materials, objects = [], {}
    name, vertices, material = None, [], 0
    for i, line in enumerate(lines):
        if line.startswith('MATERIAL '):
            rgb = tuple(round(float(c)*255) for c in line.split(' rgb ')[1].split()[:3])
            materials.append(rgb)
        elif line.startswith('name "'):
            name = line[6:-1]
            objects[name] = []
        elif line.startswith('numvert '):
            count = int(line.split()[1])
            # AC3D (aft, up, left) -> construction (aft, right, up).
            vertices = [(v[0], -v[2], v[1]) for v in
                        [tuple(map(float, s.split())) for s in lines[i+1:i+1+count]]]
        elif line.startswith('mat '):
            material = int(line.split()[1])
        elif line.startswith('refs '):
            count = int(line.split()[1])
            ids = [int(s.split()[0]) for s in lines[i+1:i+1+count]]
            objects[name].append((material, [vertices[j] for j in ids]))
    return materials, objects


def font(size):
    try:
        return ImageFont.truetype('arial.ttf', size)
    except OSError:
        return ImageFont.load_default(size=size)


def bounds(faces):
    points = [p for _, polygon in faces for p in polygon]
    return [[min(p[i] for p in points), max(p[i] for p in points)] for i in range(3)]


def draw_part(path, title, faces, palette):
    image = Image.new('RGB', (1440, 650), '#f5f6f8')
    pen = ImageDraw.Draw(image)
    pen.text((28, 20), title, font=font(26), fill='#142638')
    extent = bounds(faces)
    dimensions = ' / '.join(f'{b-a:.4f} m' for a, b in extent)
    pen.text((28, 57), 'Etendue x / y / z : ' + dimensions, font=font(19), fill='#334b60')
    projections = [('Profil (x, z)', lambda p: (p[0], -p[2], p[1])),
                   ('Dessus (x, y)', lambda p: (p[0], p[1], p[2])),
                   ('Face (y, z)', lambda p: (p[1], -p[2], -p[0]))]
    for index, (label, project) in enumerate(projections):
        left = index*480 + 20
        pen.rounded_rectangle((left, 105, left+460, 565), radius=10, fill='white',
                              outline='#b5c4d2', width=2)
        pen.text((left+15, 120), label, font=font(21), fill='#142638')
        polygons = [(mat, [project(p) for p in v]) for mat, v in faces]
        points = [p for _, v in polygons for p in v]
        xmin, xmax = min(p[0] for p in points), max(p[0] for p in points)
        ymin, ymax = min(p[1] for p in points), max(p[1] for p in points)
        scale = min(420/max(xmax-xmin, .0001), 365/max(ymax-ymin, .0001))
        for mat, v in sorted(polygons, key=lambda item: sum(p[2] for p in item[1])/len(item[1])):
            xy = [(left+230+(p[0]-(xmin+xmax)/2)*scale,
                   355+(p[1]-(ymin+ymax)/2)*scale) for p in v]
            color = palette[mat]
            pen.polygon(xy, fill=color, outline='#56616b')
    pen.text((28, 595), 'Schema du maillage, sans perspective ni textures ; '
             'pas une capture FlightGear.',
             font=font(21), fill='#334b60')
    pen.text((28, 625), 'Chaque vue est ajustee au cadre. Les dimensions sont celles du modele, '
             'pas du constructeur.',
             font=font(17), fill='#334b60')
    image.save(path)


def atlas(mesh, output):
    output.mkdir(parents=True, exist_ok=False)
    palette, objects = read_mesh(mesh)
    record, cards = [], []
    for index, (name, faces) in enumerate(objects.items(), 1):
        filename = f'piece-{index:02d}.png'
        draw_part(output/filename, name, faces, palette)
        record.append(dict(name=name, image=filename, faces=len(faces), bounds_m=bounds(faces)))
        cards.append(f'<h2>{index}. {html.escape(name)}</h2><img src="{filename}" '
                     f'alt="Trois projections de {html.escape(name)}" width="100%">')
    groups = {
        'ensemble': list(objects),
        'coque': ['fuselage'],
        'verriere': ['verriere', 'pare-brise', 'vitrage-droit', 'vitrage-gauche',
                     'arceaux', 'bordures-cockpit', 'raccord-arriere', 'longerons-verriere'],
        'portes': ['fuselage', 'contour-porte-1', 'contour-porte1'],
        'ailes': ['aile-1', 'aile1', 'hauban-1', 'hauban1', 'aerofrein-1', 'aerofrein1'],
        'queue': ['derive', 'empennage-1', 'empennage1', 'profondeur-1', 'profondeur1'],
        'train': ['roue', 'roulette', 'patin'],
        'commandes': ['sieges', 'manche', 'poignee-frein', 'tige-largage', 'boule-largage'],
        'tableau': [n for n in objects if n.startswith(('alt', 'ias', 'vsi', 'compas')) or
                    n in ('tableau', 'vitesse-mph', 'vario')],
        'pitot': ['embase-pitot', 'tube-pitot', 'attache-laine', 'fil-de-laine'],
    }
    for name, selected in groups.items():
        draw_part(output/f'groupe-{name}.png', name,
                  [face for n in selected for face in objects.get(n, [])], palette)
    (output/'inventaire.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    (output/'index.html').write_text('<!doctype html><html lang="fr"><meta charset="utf-8">'
        '<title>Atlas des pieces SW233</title><body style="max-width:1440px;margin:auto">'
        '<h1>Chaque objet du maillage SW233</h1>'
        '<p>Projections originales generees depuis sw233.ac. '
        'Les textures et les animations ne sont pas representees.</p>' + ''.join(cards) +
        '</body></html>', encoding='utf-8')
    print(f'{len(record)} pieces illustrees dans {output}')
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mesh', type=Path, default=ROOT/'src/SW233/Models/sw233.ac')
    args = parser.parse_args()
    atlas(args.mesh, args.output)

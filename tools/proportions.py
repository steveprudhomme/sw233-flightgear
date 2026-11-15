"""Compare explicitly uncertain drawing landmarks with mesh coordinates."""
import argparse
import json
from pathlib import Path

from tools.parts_atlas import read_mesh

ROOT = Path(__file__).resolve().parents[1]


def compare():
    _, objects = read_mesh(ROOT/'src/SW233/Models/sw233.ac')
    windscreen = [p for _, face in objects['pare-brise'] for p in face]
    length = max(p[0] for _, face in objects['derive'] for p in face)
    foot = max(p[0] for p in windscreen if p[2] <= .10)
    landmarks = [('Debut du vitrage', 263, min(p[0] for p in windscreen)),
                 ('Pied du montant', 332, foot),
                 ('Sommet du montant', 339, max(p[0] for p in windscreen))]
    rows = []
    for label, pixel, model in landmarks:
        # Each endpoint and landmark has a conservative +/-3 px picking allowance.
        # This does NOT bound the unknown geometric error of the illustration itself.
        low = ((pixel-3)-(214+3))/((697+3)-(214+3))
        high = ((pixel+3)-(214-3))/((697-3)-(214-3))
        nominal = (pixel-214)/(697-214)
        rows.append(dict(label=label, pixel=pixel, drawing_ratio=nominal,
                         picking_interval=[low, high], model_m=model,
                         model_ratio=model/length, illustrative_m=nominal*length,
                         delta_m=model-nominal*length))
    return dict(reference='960x743 colour three-view, profile only; not dimensioned',
                nose_pixel=214, aft_pixel=697, allowance_px=3, model_length_m=length,
                interpretation='Drawing comparison only, not aircraft tolerance', rows=rows)


def report(output):
    output.mkdir(parents=True, exist_ok=False)
    data = compare()
    (output/'proportions.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="540" '
           'viewBox="0 0 1100 540"><rect width="1100" height="540" fill="#f4f7fa"/>',
           '<g font-family="sans-serif" fill="#193348">',
           '<text x="30" y="38" font-size="25">RepÃ¨res longitudinaux du pare-brise</text>',
           '<text x="30" y="72" font-size="18">Bleu : dessin ; orange : modÃ¨le (ratios).</text>']
    def x(ratio):
        return 300+ratio*2400
    for i, row in enumerate(data['rows']):
        y = 145+i*105
        svg += [f'<text x="25" y="{y}" font-size="20">{row["label"]}</text>',
                f'<line x1="300" x2="1020" y1="{y}" y2="{y}" stroke="#bbc9d4"/>']
        lo, hi = row['picking_interval']
        svg.append(f'<rect x="{x(lo)}" y="{y-8}" width="{x(hi)-x(lo)}" '
                   'height="16" fill="#afd9ef"/>')
        for value, offset, color in [(row['drawing_ratio'], 0, '#1673ac'),
                                      (row['model_ratio'], 24, '#b85f00')]:
            svg.append(f'<circle cx="{x(value)}" cy="{y+offset}" r="6" fill="{color}"/>')
            svg.append(f'<text x="{x(value)+10}" y="{y+offset+5}" '
                       f'font-size="17">{value:.3f}</text>')
    svg += ['<text x="30" y="465" font-size="18">Bande bleue : pointage Â±3 px.</text>',
            '<text x="30" y="497" font-size="18">Erreur du dessin inconnue.</text>',
            '</g></svg>']
    (output/'comparaison.svg').write_text(''.join(svg)+'\n', encoding='utf-8')
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('RGB', (1100, 540), '#f4f7fa')
    draw = ImageDraw.Draw(image)
    def font(size):
        try:
            return ImageFont.truetype('arial.ttf', size)
        except OSError:
            return ImageFont.load_default(size=size)
    draw.text((30, 20), 'RepÃ¨res longitudinaux du pare-brise', font=font(26), fill='#193348')
    draw.text((30, 65), 'Bleu : dessin ; orange : maillage. Nez = 0 ; longueur = 1.',
              font=font(20), fill='#193348')
    for i, row in enumerate(data['rows']):
        y = 145+i*105
        draw.text((25, y-14), row['label'], font=font(20), fill='#193348')
        draw.line((300, y, 1020, y), fill='#bbc9d4', width=2)
        lo, hi = row['picking_interval']
        draw.rectangle((x(lo), y-8, x(hi), y+8), fill='#afd9ef')
        for val, dy, color in [(row['drawing_ratio'], 0, '#1673ac'),
                               (row['model_ratio'], 24, '#b85f00')]:
            draw.ellipse((x(val)-6, y+dy-6, x(val)+6, y+dy+6), fill=color)
            draw.text((x(val)+12, y+dy-10), f'{val:.3f}', font=font(18), fill=color)
    draw.text((30, 453), 'Bande bleue : pointage Â±3 pixels seulement.',
              font=font(20), fill='#193348')
    draw.text((30, 489), 'Lâ€™erreur du dessin par rapport au vrai appareil reste inconnue.',
              font=font(20), fill='#193348')
    image.save(output/'comparaison.png')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    print(json.dumps(report(args.output), indent=2))

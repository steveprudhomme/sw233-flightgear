"""Generate a reproducible survey sheet and local photo overlay from explicit picks."""

import argparse
import hashlib
import html
import json
from pathlib import Path

from tools.parts_atlas import bounds, read_mesh

ROOT = Path(__file__).resolve().parents[1]
PARTS = (
    "fuselage",
    "pare-brise",
    "verriere",
    "vitrage-droit",
    "vitrage-gauche",
    "arceaux",
    "bordures-cockpit",
    "raccord-arriere",
    "longerons-verriere",
    "contour-porte-1",
    "contour-porte1",
)


def generate(output):
    data = json.loads((ROOT / "docs/references/releves-avant-41.json").read_text(encoding="utf-8"))
    photo = ROOT / "docs/references/originaux/exterieur-lot-01" / data["file"]
    if hashlib.sha256(photo.read_bytes()).hexdigest() != data["sha256"]:
        raise ValueError("Reference photo changed")
    output.mkdir(parents=True, exist_ok=False)
    points = data["points"]
    # Deliberately report image-space spans, not dimensions of the real aircraft.
    a, b, c, d = [points[k]["uv"] for k in "ABCD"]
    numerator, denominator = b[1] - c[1], b[0] - d[0]
    uncertainty_n = points["B"]["uncertainty_px"] + points["C"]["uncertainty_px"]
    uncertainty_d = points["B"]["uncertainty_px"] + points["D"]["uncertainty_px"]
    ratios = dict(
        height_projected_px=numerator,
        base_projected_px=denominator,
        ratio=numerator / denominator,
        conservative_reading_interval=[
            (numerator - uncertainty_n) / (denominator + uncertainty_d),
            (numerator + uncertainty_n) / (denominator - uncertainty_d),
        ],
        nose_horizontal_span_px=a[0] - b[0],
        note="Reading uncertainty only; unknown perspective error is not included",
    )
    _, objects = read_mesh(ROOT / "src/SW233/Models/sw233.ac")
    report = dict(
        reference=data,
        projected_ratios=ratios,
        model_axes="x aft, y right, z up; metres of model, not aircraft measurements",
        model_bounds={n: bounds(objects[n]) for n in PARTS},
    )
    (output / "releves.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    shapes = []
    for ids in data["contours"].values():
        coords = " ".join(",".join(map(str, points[k]["uv"])) for k in ids)
        shapes.append(
            f'<polyline points="{coords}" fill="none" stroke="#1674ae" stroke-width="4"/>'
        )
    for key, item in points.items():
        u, v = item["uv"]
        radius = item["uncertainty_px"]
        shapes.append(
            f'<circle cx="{u}" cy="{v}" r="{radius}" fill="none" '
            'stroke="#c32525" stroke-width="3"/>'
        )
        shapes.append(f'<text x="{u + 18}" y="{v - 15}" font-size="30" fill="#c32525">{key}</text>')
    content = "".join(shapes)
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="850 480 850 700">'
    (output / "points.svg").write_text(
        svg + '<rect x="850" y="480" width="850" height="700" fill="white"/>' + content + "</svg>",
        encoding="utf-8",
    )
    # Browser overlay: original bytes stay unchanged. It is an inspection sheet,
    # not a retouched photograph or a simulated FlightGear capture.
    image = html.escape(photo.resolve().as_uri(), quote=True)
    rows = "".join(
        f"<tr><td>{k}</td><td>{html.escape(v['label'])}</td><td>{v['uv']}</td>"
        f"<td>±{v['uncertainty_px']} px</td></tr>"
        for k, v in points.items()
    )
    page = f"""<!doctype html><html lang="fr"><meta charset="utf-8"><title>Relevés VIS-05a</title>
    <h1>Repères approximatifs sur EXT-02</h1><p>Coordonnées originales 2048 × 1364.
    Cercles = incertitude de lecture. Traits = guides, pas contours définitifs.</p>
    <svg viewBox="0 0 2048 1364" style="width:100%;max-width:1400px">
    <image href="{image}" width="2048" height="1364"/>{content}</svg>
    <table border="1"><tr><th>Point</th><th>Repère</th><th>u,v</th><th>Lecture</th></tr>
    {rows}</table>
    <p>Photo locale inchangée ; auteurs et date non établis.
    Les chiffres ne sont pas des mètres.</p>"""
    (output / "index.html").write_text(page, encoding="utf-8")
    print(json.dumps(ratios, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    generate(parser.parse_args().output)

"""Make a local photo/native comparison without copying or altering the photographs."""

import argparse
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    (
        "EXT-02 : volume du nez et flancs",
        "exterieur-lot-01",
        "841099659_18115421924518465_3488248020240132807_n.jpg",
        "apres-nez-profil.png",
        "Le nez doit rester plein et arrondi ; les cassures du ventre restent visibles.",
    ),
    (
        "EXT-03 : pare-brise ferme et raccord sous aile",
        "exterieur-lot-01",
        "843324439_18115421933518465_1258995022678257876_n.jpg",
        "apres-nez-oblique.png",
        "Comparer le bombe, les bords bleus et la continuite du raccord arriere.",
    ),
    (
        "DET-03 : cadres, joints et fixations",
        "details-lot-02",
        "576493756_851877043862334_4759751965595203080_n.jpg",
        "cadres.png",
        "La photo ouverte revele le cadre ; notre capture reste fermee et fixe.",
    ),
)


def generate(output, captures):
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for title, folder, photo, shot, note in PAIRS:
        original = ROOT / "docs/references/originaux" / folder / photo
        native = captures / shot
        if not original.is_file() or not native.is_file():
            raise FileNotFoundError((original, native))
        images = "".join(
            f'<a href="{p.as_uri()}"><img src="{p.as_uri()}" alt="{html.escape(label)}"></a>'
            for p, label in (
                (original.resolve(), "Photo de reference locale"),
                (native.resolve(), "Capture native FlightGear"),
            )
        )
        rows.append(
            f"<h2>{html.escape(title)}</h2><p>{html.escape(note)}</p>"
            f'<div class="pair">{images}</div>'
        )
    (output / "index.html").write_text(
        '<!doctype html><html lang="fr"><meta charset="utf-8">'
        "<title>Comparaison locale VIS-05b/c</title><style>"
        "body{font:18px system-ui;max-width:1600px;margin:30px auto;background:#eee;"
        "color:#172333}.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}"
        "img{width:100%;height:550px;object-fit:contain;background:white}</style>"
        "<h1>Photos et captures du lot43</h1><p>Originaux non retouches, conserves "
        "localement. Angles et perspectives differents : comparaison qualitative, "
        "pas une superposition calibree ni une mesure en metres. Cliquer pour ouvrir "
        "l'image complete.</p>" + "".join(rows) + "</html>",
        encoding="utf-8",
    )
    return output / "index.html"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--captures", type=Path, required=True)
    args = parser.parse_args()
    print(generate(args.output.resolve(), args.captures.resolve()))

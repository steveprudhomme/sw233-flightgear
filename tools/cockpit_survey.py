"""Export model-only cockpit measurements to prepare a real-aircraft survey."""
import argparse
import hashlib
import json
from pathlib import Path

from tools.parts_atlas import ROOT, bounds, draw_part, read_mesh

PARTS = (
    "fuselage", "pare-brise", "vitrage-gauche", "vitrage-droit", "arceaux",
    "bordures-cockpit", "raccord-arriere", "longerons-verriere",
    "contour-porte-1", "contour-porte1",
)


def export(mesh, output):
    palette, objects = read_mesh(mesh)
    # Fail before creating a partial dossier when a required object is absent.
    records = [{"object": name, "bounds_xyz_m": bounds(objects[name]),
                "image": f"piece-{i:02d}.png"} for i, name in enumerate(PARTS, 1)]
    output.mkdir(parents=True, exist_ok=False)
    data = {"classification": "MODEL ONLY; not measured on a real aircraft",
            "source": mesh.name, "sha256": hashlib.sha256(mesh.read_bytes()).hexdigest(),
            "axes": "x aft, y right, z up; construction frame, not mass datum",
            "records": records}
    (output / "model-measurements.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8")
    lines = ["# Relevé du modèle uniquement", "",
             "Ces limites ne sont pas des mesures de l'appareil réel.", "",
             f"Source SHA-256 : {data['sha256']}", "",
             "Axes : x arrière, y droite, z haut ; repère de construction.", "",
             "Les boîtes englobantes ne donnent pas la largeur à une section donnée.", "",
             "| Objet | x min / max (m) | y min / max (m) | z min / max (m) |",
             "|---|---|---|---|"]
    for row in records:
        limits = " | ".join(f"{lo:.4f} / {hi:.4f}" for lo, hi in row["bounds_xyz_m"])
        lines.append(f"| {row['object']} | {limits} |")
        draw_part(output / row["image"], row["object"], objects[row["object"]], palette)
    for row in records:
        lines += ["", f"## {row['object']}", "", f"![{row['object']}]({row['image']})"]
    (output / "mesures-modele.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = export(ROOT / "src/SW233/Models/sw233.ac", args.output)
    print(f"{len(result['records'])} model parts exported to {args.output}")

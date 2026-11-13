"""Rebuild the aircraft from the learner's fenced blocks in an empty practice folder."""

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(
    r"<!-- atelier-fichier: ([^\n]+?) -->\n```(?:python|xml|nasal)\n(.*?)\n```", re.S)


def rebuild(destination):
    destination.mkdir(parents=True, exist_ok=False)
    outputs = {}
    for page in sorted((ROOT / "docs/construction").glob("*.md")):
        for name, fragment in BLOCK.findall(page.read_text(encoding="utf-8")):
            outputs.setdefault(name, []).append(fragment)
    for name, fragments in outputs.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(fragments) + "\n", encoding="utf-8")
    for recipe in ("fabrique.py", "dynamique.py"):
        subprocess.run([sys.executable, recipe], cwd=destination, check=True)
    for src in sorted((ROOT/"src/SW233").rglob("*")):
        if src.is_file():
            name = src.relative_to(ROOT)
            if (destination/name).read_text(encoding="utf-8") != src.read_text(encoding="utf-8"):
                raise ValueError(f"Reconstruction différente : {name}")
    panel = Path("tools/panel.py")
    if ast.dump(ast.parse((destination/panel).read_text(encoding="utf-8"))) != ast.dump(
        ast.parse((ROOT/panel).read_text(encoding="utf-8-sig"))
    ):
        raise ValueError("La recette du tableau ne correspond pas à la leçon")
    print(f"Reconstruction vérifiée : {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("nouveau_dossier", type=Path)
    rebuild(parser.parse_args().nouveau_dossier.resolve())

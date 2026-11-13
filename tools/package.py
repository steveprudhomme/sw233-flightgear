"""Copy editable aircraft sources to an untracked FlightGear package."""

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

if __package__:
    from .launch import validate_resources
    from .panel import finish_panel
else:
    from launch import validate_resources
    from panel import finish_panel

ROOT = Path(__file__).resolve().parents[1]


def package(output: Path) -> Path:
    """Never overwrite a package or delete an existing user's directory."""
    destination = output / "Aircraft" / "SW233"
    extras = [output / name for name in
              ("launch.py", "start-sw233.cmd", "LICENSE.md", "LIRE-MOI.txt", "manifest.json")]
    if destination.exists() or any(path.exists() for path in extras):
        raise FileExistsError(f"Destination already exists: {destination}")
    shutil.copytree(ROOT / "src" / "SW233", destination)
    finish_panel(destination / "Models")
    validate_resources(output)
    shutil.copyfile(ROOT / "tools/launch.py", output / "launch.py")
    shutil.copyfile(ROOT / "LICENSE.md", output / "LICENSE.md")
    (output / "start-sw233.cmd").write_text(
        '@echo off\npython "%~dp0launch.py" %*\nexit /b %errorlevel%\n', encoding='ascii')
    (output / "LIRE-MOI.txt").write_text(
        "SW233 - GPL-3.0-only. Python 3.11+ requis pour le lanceur.\n"
        "Depuis un terminal : python launch.py --fgfs CHEMIN_EXE --fg-root DOSSIER_FGDATA "
        "--scenery DOSSIER_TERRASYNC --check\n"
        "Mettre les chemins entre guillemets. Retirer --check pour partir au sol a CYJN.\n"
        "--mode air : depart a 5000 ft / 60 kt, aucun pilote automatique.\n"
        "Manifeste : detection des modifications, pas signature d'authenticite.\n"
        "Les scenes et FlightGear ne sont pas inclus. La couverture terrain reste a verifier.\n"
        "Tutoriel : https://github.com/steveprudhomme/sw233-flightgear/"
        "blob/main/docs/construction/12-installation.md\n", encoding='utf-8')
    try:
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                           text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = 'unknown'
    files = sorted([p for p in destination.rglob('*') if p.is_file()] + extras[:-1])
    manifest = dict(format=1, source_revision=revision, files={
        p.relative_to(output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in files})
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build")
    print(package(parser.parse_args().output).resolve())

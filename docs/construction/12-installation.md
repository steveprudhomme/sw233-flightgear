# 12. Emporter son planeur et le lancer sans se tromper de dossier

Séance AUD-02a, 13 novembre 2026. Le plan a été commité avant le travail (`27a8fa6`). Nous validons Windows ici ; Linux, miniature et intégration au catalogue restent AUD-02b.

## 1. Distinguer l’atelier et la boîte à emporter

Le dépôt est l’atelier : il contient les recettes, les tests et les explications. Le paquet est la boîte que FlightGear ouvre. La recette de peinture crée des images que tu ne dois pas fabriquer à la main. Si tu copies seulement le maillage AC, il peut manquer le tableau peint, les cadrans ou le menu.

Prépare un dossier neuf. Le constructeur copie toutes les sources Aircraft/SW233, fabrique les textures puis vérifie les liens entre le fichier set, le modèle, le maillage, les images, les listes et le module Nasal. Il ajoute aussi la licence GPL, un petit mode d’emploi et le lanceur.

```text
SW233 pret a voler/
├── Aircraft/SW233/       # Avion et textures fabriquées
├── launch.py            # Vérifie puis démarre FlightGear
├── start-sw233.cmd      # Entrée Windows qui appelle launch.py
├── manifest.json        # Empreintes des fichiers du paquet
├── LICENSE.md
└── LIRE-MOI.txt
```

## 2. Préparer les chemins

Tu as besoin de trois adresses : le programme **fgfs.exe**, le dossier de données **fgdata** contenant defaults.xml/version et le dossier de scène **TerraSync** contenant Terrain et Airports. Il s’agit de trois choses différentes. Les chemins avec espaces doivent être entre guillemets dans le terminal.

Suis les commandes complètes de [INSTALL](../../INSTALL.md). Commence par `--check` : ce mode annonce ce qu’il lancerait sans ouvrir FlightGear. Corrige les erreurs avant d’enlever cette option. Le paquet déjà fabriqué ne dépend que de Python pour son lanceur ; Pillow reste nécessaire pour fabriquer les textures.

## 3. Lire le contrôle de ressources

`required` vérifie qu’un fichier existe et que son chemin reste dans le dossier prévu. `validate_resources` lit les références XML, puis cherche les lignes `texture` dans le fichier AC. `verify` calcule pour chaque fichier une empreinte SHA-256 : imagine une étiquette calculée à partir de son contenu. Une image changée ou manquante donne une erreur. Le manifeste ne prouve pas qui a créé le paquet : ce n’est pas une signature.

`command` prépare une **liste d’arguments**, pas une longue phrase exécutée par un shell. Ainsi, un chemin avec espaces reste un seul argument. Le mode au sol est choisi par défaut ; le mode air doit être demandé. Le programme ne télécharge pas de scène, ne change pas les commandes du joystick et n’ouvre pas de serveur HTTP sauf demande explicite pour les essais.

Sous Windows, `STARTUPINFO` demande une fenêtre interactive visible. Notre premier lancement hérita d’un état de fenêtre non rendu et la capture ne contenait qu’un pixel ; ce réglage a corrigé le lancement du paquet testé. Nous avons également vérifié le vrai fichier racine fgdata : dans 2024.1.7, c’est defaults.xml, et non preferences.xml.

## 4. Écrire le lanceur

Crée `tools/launch.py` dans ton atelier. Il sera copié à la racine du paquet. Les fonctions sont séparées pour pouvoir les tester sans ouvrir un simulateur à chaque essai.

<!-- atelier-fichier: tools/launch.py -->
```python
"""Validate a relocatable SW233 package and launch a visible FlightGear session."""
import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def required(root, relative):
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f"Fichier absent ou chemin invalide : {relative}")
    return target


def validate_resources(root):
    air = root / 'Aircraft/SW233'
    config = ET.parse(required(air, 'sw233-set.xml'))
    required(air, config.findtext('sim/aero') + '.xml')
    model = required(root, config.findtext('sim/model/path'))
    mesh = required(model.parent, ET.parse(model).findtext('path'))
    for texture in re.findall(r'^texture "([^"\n]+)"', mesh.read_text(), re.M):
        required(mesh.parent, texture)
    required(air, config.find('sim/checklists').attrib['include'])
    for node in config.findall('nasal/*/file'):
        required(air, node.text)
    required(air, 'gui/dialogs/occupants.xml')
    return air


def verify(root):
    manifest = json.loads(required(root, 'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('format') != 1 or not manifest.get('files'):
        raise ValueError('Manifeste absent ou incompatible ; reconstruire le paquet.')
    for relative, expected in manifest['files'].items():
        actual = hashlib.sha256(required(root, relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Fichier modifie : {relative}. Reconstruire un paquet neuf.')
    air = validate_resources(root)
    for path in air.rglob('*'):
        if path.is_file() and path.relative_to(root).as_posix() not in manifest['files']:
            raise ValueError(f'Fichier non repertorie : {path.name}')
    return manifest


def command(root, fgfs, fgroot, scenery, mode='ground', http_port=None):
    verify(root)
    if not fgfs.is_file():
        raise ValueError(f'Programme FlightGear introuvable : {fgfs}')
    required(fgroot, 'defaults.xml')
    required(fgroot, 'version')
    required(scenery, 'Airports/C/Y/J/CYJN.threshold.xml')
    terrain = scenery / 'Terrain/w080n40/w074n45'
    if not terrain.is_dir() or not any(terrain.glob('*.btg*')):
        raise ValueError('Terrain CYJN absent : installer la zone dans le dossier scenery indique.')
    args = [str(fgfs.resolve()), f'--fg-root={fgroot.resolve()}',
            f'--fg-aircraft={(root / "Aircraft").resolve()}',
            f'--fg-scenery={scenery.resolve()}', '--aircraft=sw233', '--airport=CYJN',
            '--heading=010', '--start-date-gmt=2026:06:21:16:45:00', '--wind=0@0',
            '--disable-real-weather-fetch', '--disable-terrasync', '--geometry=1280x720']
    args += ['--on-ground', '--vc=0'] if mode == 'ground' else [
        '--in-air', '--altitude=5000', '--vc=60']
    if http_port is not None:
        if not 1024 <= http_port <= 65535:
            raise ValueError('Port de test attendu entre 1024 et 65535.')
        args.append(f'--httpd={http_port}')
    return args


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--fgfs', type=Path, required=True)
    parser.add_argument('--fg-root', type=Path, required=True)
    parser.add_argument('--scenery', type=Path, required=True)
    parser.add_argument('--mode', choices=['ground', 'air'], default='ground')
    parser.add_argument('--check', action='store_true', help='Verifier sans lancer FlightGear')
    parser.add_argument('--http-port', type=int, help='Interface de test ; desactivee par defaut')
    args = parser.parse_args()
    try:
        root = args.package.resolve()
        argv = command(root, args.fgfs, args.fg_root, args.scenery, args.mode, args.http_port)
        revision = verify(root).get('source_revision', 'inconnue')
        print(f'Paquet verifie : {root}\nRevision source : {revision}')
        print('Scene CYJN detectee ; couverture visuelle a verifier dans FlightGear.')
        print(subprocess.list2cmdline(argv) if sys.platform == 'win32' else shlex.join(argv))
        if not args.check:
            options = {}
            if sys.platform == 'win32':
                startup = subprocess.STARTUPINFO()
                startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startup.wShowWindow = 1  # Visible interactive session.
                options['startupinfo'] = startup
            process = subprocess.Popen(argv, cwd=root, **options)
            print(f'FlightGear lance, PID {process.pid}. Mode : {args.mode}.')
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError, ET.ParseError) as exc:
        print(f'Erreur : {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
```

## 5. Compléter le constructeur

Remplace `tools/package.py` par cette version. Elle garde le refus d’écrasement, puis ajoute les fichiers de lancement et le manifeste. Elle ne parcourt pas tous tes fichiers personnels : les empreintes concernent uniquement les fichiers qu’elle vient de produire. Les fichiers generated restent dans build ou un dossier de distribution, jamais dans les sources Git.

<!-- atelier-fichier: tools/package.py -->
```python
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
```

## 6. Déplacer le paquet et lancer

Fabrique dans un premier dossier, puis copie **tout** le dossier obtenu dans un deuxième dossier contenant des espaces. Garde le premier pour comparer ; il n’est pas nécessaire au fonctionnement de la copie. Le lanceur de la copie retrouve Aircraft à côté de lui et construit un chemin absolu. N’ajoute pas Aircraft/SW233 comme racine de recherche : le paramètre fg-aircraft vise le dossier **Aircraft** qui le contient.

Dans notre essai, FlightGear a confirmé par `/sim/aircraft-dir` le dossier **Installation neuve SW233 14c/Aircraft/SW233**. L’entrée start-sw233.cmd a également été appelée depuis un autre répertoire, avec `--check`, et a retrouvé la même copie. Les noms 14b/14c sont les dossiers d’essais successifs ; tu peux choisir un autre nom neuf.

![Cockpit du paquet déplacé, rendu natif FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/installation-14/cockpit.jpg)

La piste et les champs sont visibles : ce n’est pas un vol au-dessus d’un océan sans scène. Le tableau peint et les cadrans sont chargés. L’horizon penché vient du planeur posé sur son train ; ce cliché n’est pas une preuve de vol équilibré.

![Menu des occupants chargé depuis le nouveau paquet](https://github.com/steveprudhomme/sw233-flightgear/releases/download/installation-14/occupants.jpg)

Le module des occupants affiche 970 lb avec 180 lb par siège. Les nombres de saisie n’ajoutent plus artificiellement deux décimales : le correctif de précision de la fiche 11 est inclus.

## 7. Vérifier les commandes et les erreurs

Le banc lit le chemin du paquet réellement chargé avant d’actionner quoi que ce soit. Dans cette session dédiée au sol, il vérifie trois états : profondeur +1 / aérofreins sortis, profondeur −1 / aérofreins rentrés, puis neutre. Il remet ensuite les commandes initiales. Les angles reçus sont ±0,401426 rad (environ ±23°), et les aérofreins donnent bien 1 puis 0.

Attention au nom de propriété : notre modèle utilise **/controls/flight/speedbrake**, comme les démonstrations précédentes. La propriété spoilers ne pilote pas cette chaîne FDM. Un premier banc a détecté cette mauvaise adresse et a été corrigé avant les preuves finales.

Les trois instruments interrogés renvoient des nombres finis. Cela vérifie leurs connexions dans ce paquet, pas leur étalonnage sur toute la plage. Les valeurs et le chemin effectif figurent dans installation.json joint à la publication.

```powershell
# Session dédiée au sol lancée avec --http-port 18099.
# Adapter le premier chemin au paquet à contrôler, et choisir une sortie neuve.
python -m tools.installation_bench "../Installation neuve SW233 14c" build/preuves-installation
```

Les tests Python fabriquent un paquet temporaire et le copient dans un chemin avec espaces. Ils vérifient les frontières des arguments, le départ au sol par défaut et l’absence de serveur HTTP implicite. Ils modifient puis retirent une texture dans **leur copie temporaire**, et exigent un refus. Ils vérifient enfin un programme absent, un scenery absent et la conservation d’un fichier préexistant lors d’un refus de fabrication.

```powershell
python -m unittest discover -s tests
python -m ruff check .
python tools/check_workbook.py build/livre-installation
```

## 8. Ce qui est prouvé, et ce qui reste à faire

19 tests passent ; le livre reconstruit les fichiers de l’avion. Le contrôle visuel natif est réalisé sous Windows avec FlightGear 2024.1.7. Les fichiers defaults.xml/version et une tuile de la région sont des indices de présence, pas une preuve que chaque fichier fgdata ou chaque kilomètre de terrain est complet. La capture confirme le décor à cet endroit précis.

Le manifeste du paquet de test mentionne le commit de préparation : les fichiers étaient encore en cours de travail. Les empreintes jointes identifient les contenus testés. Le paquet distribué après commit sera construit depuis la révision publiée. Les images et ZIP restent des pièces jointes de publication, tandis que les recettes éditables restent dans Git.

Sources de cette séance : fichiers locaux de FlightGear 2024.1.7, recette de peinture existante, propriétés effectivement relevées dans le simulateur et tests du dépôt. Aucune dimension ni donnée aérodynamique n’a été ajoutée. Biais de validation : une seule installation Windows a été essayée ; nous ne présentons pas cela comme une validation Linux. Les prochains contrôles de portabilité et de catalogue restent explicitement dans ROADMAP.

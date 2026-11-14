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
    for preview in config.findall('sim/previews/preview/path'):
        required(air, preview.text)
    if config.find('sim/previews') is not None:
        required(air, 'thumbnail.jpg')
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

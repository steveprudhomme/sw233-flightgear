# Installation et validation

## FlightGear

1. Installer FlightGear avec JSBSim et les scènes de la zone d'essai.
2. Cloner le dépôt, installer Pillow avec `python -m pip install Pillow==12.0.0`, puis exécuter `python tools/package.py` à sa racine.
3. Ajouter le chemin absolu de `build/Aircraft` aux dossiers d'aéronefs
   supplémentaires du lanceur FlightGear.
4. Sélectionner **Schweizer SGS 2-33 — Cadets de l’aviation royale du Canada (prototype)** (identifiant `sw233`).
5. Initialiser en vol au-dessus de CYJN à 5 000 ft MSL et 60 kt.
   Prévoir la marge terrain si une autre zone est choisie.

Le script copie les sources dans build/Aircraft/SW233 ; il crée la texture du tableau à partir de sa recette éditable et
refuse d'écraser une destination existante. Pour un nouveau paquet, choisir un
autre dossier avec `python tools/package.py --output build/essai-2` ; ajouter
alors build/essai-2/Aircraft au lanceur.

Sur Windows, utiliser le chemin complet de fgfs.exe si nécessaire. En ligne de
commande, le chemin de --fg-aircraft doit être absolu si l'on change de dossier.
Le planeur ne décolle pas seul : le prototype utilise un démarrage en vol.
Utiliser les commandes FlightGear de profondeur, ailerons, direction et spoilers.
Le fichier principal ne modifie pas les affectations du joystick.

## Environnement de développement

Python 3.11 ou 3.13 est utilisé en CI ; Python 3.11+ est recommandé.

```sh
python -m venv .venv
```

Activer `.venv` avec `.venv\Scripts\Activate.ps1` sur PowerShell ou
`source .venv/bin/activate` sur Linux/macOS, puis :

```sh
python -m pip install -r requirements-dev.txt
python tools/check.py
python -m ruff check .
python -m unittest discover -s tests -v
python tools/package.py
```

Les tests utilisent JSBSim autonome, version verrouillée dans les dépendances.
La version embarquée dans FlightGear peut différer. Consulter docs/validation.md
avant d'interpréter un test vert comme une validation de l'aéronef complet.

## Essai manuel sur Windows

Dans PowerShell, place-toi dans le dossier du projet (celui qui contient README.md et tools). Sur l’installation utilisée pour ce tutoriel, ce dossier est :

```powershell
Set-Location "C:\Users\steve\Documents\Codex\2026-11-01\j-aimerais-que-tu-cr-un-3\outputs\sw233-flightgear"
$essai = Join-Path (Get-Location) ("build\vol-manuel-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
python tools/package.py --output $essai
& "C:\Program Files\FlightGear 2024.1\bin\fgfs.exe" `
  "--fg-root=C:\Users\steve\FlightGear\Downloads\fgdata_2024_1" `
  "--fg-aircraft=$essai\Aircraft" `
  "--fg-scenery=C:\Users\steve\FlightGear\Downloads\TerraSync" `
  --aircraft=sw233 --airport=CYJN --in-air `
  --altitude=5000 --vc=60 --heading=010 `
  --start-date-gmt=2026:06:21:16:45:00 `
  --disable-real-weather-fetch --disable-terrasync `
  --prop:/controls/flight/elevator=-0.6244
```

Le dossier neuf protège les précédents essais. Cette commande lance un vol manuel, sans scénario qui actionne les commandes. Pour utiliser cette recette sur un autre ordinateur, adapte les chemins vers le projet, le programme, les données et TerraSync. Si Python ne trouve pas PIL, installe Pillow comme indiqué à l’étape 2.

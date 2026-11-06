# Installation et validation

## FlightGear

1. Installer FlightGear avec JSBSim et les scènes de la zone d'essai.
2. Cloner le dépôt, installer Pillow avec `python -m pip install Pillow==12.0.0`, puis exécuter `python tools/package.py` à sa racine.
3. Ajouter le chemin absolu de `build/Aircraft` aux dossiers d'aéronefs
   supplémentaires du lanceur FlightGear.
4. Sélectionner **Schweizer SGS 2-33 — Cadets de l’aviation royale du Canada (prototype)** (identifiant `sw233`).
5. Initialiser en vol au-dessus de KSFO à 5 000 ft MSL et 50 kt.
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

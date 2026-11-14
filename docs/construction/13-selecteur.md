# 13. Reconnaître son planeur dans le lanceur

Séance AUD-02b. Le plan a été enregistré dans Git avant la réalisation : `453705e`. Cette fiche explique comment fabriquer la carte de notre avion : son nom, sa description, sa petite image et son grand aperçu. Elle ne modifie pas le calcul du vol.

## 1. Préparer son établi

Termine la [fiche 12](12-installation.md) et garde son paquet de travail. Ouvre un terminal à la racine du dépôt, là où se trouvent README.md, src et tools. Dans les exemples suivants, Python et Pillow sont déjà installés. Les commandes utilisent des dossiers neufs : si un nom existe, choisis un nouveau nom au lieu d’effacer ton travail.

Nous séparons trois objets :

| Objet | Adresse | Rôle |
|---|---|---|
| Source éditable | src/SW233/sw233-set.xml | Texte que tu peux corriger |
| Capture native | notes/selecteur/exterior.jpg | Ce que FlightGear a réellement dessiné |
| Paquet fabriqué | build/avec-apercu/Aircraft/SW233 | Copie complète que FlightGear charge |

La miniature et les textures sont des résultats fabriqués. Elles sont distribuées avec le paquet et dans les pièces jointes de la publication ; elles ne sont pas ajoutées aux sources Git.

## 2. Écrire une carte honnête

Reprends le fichier complet de la [fiche 4](04-configuration.md). Dans son élément `sim`, les champs suivants répondent à des questions précises :

| Champ | Valeur / décision | Pourquoi ? |
|---|---|---|
| description | Schweizer SGS 2-33 — Cadets de l’aviation royale du Canada (prototype) | Identifier le projet et son stade actuel |
| author | Steve Prud'Homme et contributeurs SW233 | Créditer le projet |
| long-description | Prototype libre, GPL-3.0-only, commandes et masses configurables, FDM expérimental, livrée finale à réaliser | Éviter de promettre un modèle terminé |
| aircraft-version | 0.1.0-dev | Version du prototype, distincte de celle du simulateur |
| minimum-fg-version | 2024.1.7 | Plancher conservateur : version réellement utilisée pour cet essai |

Ce minimum ne prouve pas qu’une ancienne version échoue : nous ne l’avons pas essayée. Nous n’ajoutons aucun score de qualité. La licence complète reste dans LICENSE.md ; sa mention dans la description sert à informer le lecteur, sans inventer une balise XML de licence.

Le titre peut être raccourci par le lanceur lorsque la fenêtre est étroite. Le texte long reste lisible dans la fiche détaillée.

## 3. Choisir une vraie image

Une image publicitaire pourrait montrer un avion plus beau que celui installé. Ici, l’image doit montrer le prototype actuel, avec ses formes encore simples. Nous choisissons une vue extérieure, les deux ailes entièrement dans le cadre et un éclairage qui permet de lire le dessus jaune.

![Capture native du prototype, ailes dans le cadre](https://github.com/steveprudhomme/sw233-flightgear/releases/download/selecteur-15/exterior.jpg)

Cette image vient de FlightGear 2024.1.7. La séance démarre à CYJN à 5 000 ft, cap 010°, le 21 juin 2026 à 16:45 UTC dans le simulateur, sans vent. Le temps de la scène est un réglage de lumière, pas la date de publication. Le relevé indique 5 000,238062 ft au moment de la capture : une courte évolution a précédé la pause. Ce n’est pas un essai de stabilité en vol.

Dans ton paquet de travail, utilise la commande de lancement de la fiche 12, avec `--mode air --http-port 18101`. Dès que la scène est chargée, mets le simulateur en pause. Vérifie le terrain et la position de l’avion. Pour confirmer la pause dans ce banc local, ouvre un second terminal à la racine du dépôt et exécute :

```powershell
@'
from tools.flightgear import execute
execute('setprop("/sim/freeze/master",1);',18101)
'@ | python -
```

Le script ci-dessous refuse de photographier une autre machine ou une scène dont la propriété de pause est fausse. L’option de démarrage `--enable-freeze` seule n’a pas suffi lors de notre essai : il faut vérifier la pause après le chargement. Le serveur HTTP est destiné à cette séance locale et n’est pas activé par le lanceur ordinaire.

```powershell
python -m tools.capture_preview notes/selecteur --port 18101
```

Le dossier doit être neuf. Ouvre exterior.jpg pour vérifier l’image : les ailes doivent être entières, l’avion visible et le terrain présent. Une commande réussie ne remplace pas cette observation.

## 4. Comprendre les réglages de caméra

Le script sauvegarde les réglages avant de les changer. Il choisit la vue extérieure 1, un décalage de cap de 140°, un décalage de tangage de 20° et un champ de vision de 45°. Ces nombres sont un choix de cadrage, pas des mesures du véritable planeur. Il masque la barre de menus, attend une seconde, demande le JPEG natif et vérifie que l’altitude n’a pas changé de plus de 0,1 ft pendant la capture. Enfin, il remet les réglages de caméra sauvegardés, même si une erreur survient. La pause reste active.

Le fichier capture.json garde les réglages, l’altitude, la version FlightGear, le chemin de l’avion chargé et l’empreinte SHA-256 de l’image. Cette empreinte permet de retrouver le même fichier ; elle ne certifie pas à elle seule l’origine de la photographie.

Pour reconstruire cet outil, crée tools/capture_preview.py et copie le bloc suivant. Il réutilise l’outil HTTP `execute` du projet, présenté dans la fiche 7 ; ce petit script n’est donc pas indépendant de tools/flightgear.py.

<!-- atelier-fichier: tools/capture_preview.py -->
```python
"""Capture an unretouched exterior preview from a dedicated paused FlightGear session."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.request import urlopen

from tools.flightgear import execute


def capture(folder, port):
    base = f'http://127.0.0.1:{port}'
    def get(path):
        with urlopen(base + '/json' + path, timeout=15) as response:
            return json.load(response)['value']
    if get('/sim/aircraft') != 'sw233' or not get('/sim/freeze/master'):
        raise ValueError('Pause SW233 after loading; verify /sim/freeze/master.')
    if get('/position/altitude-ft') < 1000:
        raise ValueError('Start in air at 5000 ft for this preview recipe.')
    settings = {'/sim/current-view/view-number': 1,
                '/sim/current-view/heading-offset-deg': 140,
                '/sim/current-view/pitch-offset-deg': 20,
                '/sim/current-view/field-of-view': 45,
                '/sim/menubar/visibility': 0}
    saved = {p: get(p) for p in settings}
    folder.mkdir(parents=True, exist_ok=False)
    try:
        for p, v in settings.items():
            execute(f'setprop("{p}",{v});', port)
        time.sleep(1)
        altitude = get('/position/altitude-ft')
        with urlopen(base + '/screenshot?type=jpg', timeout=20) as response:
            content = response.read()
        if len(content) < 10000 or abs(get('/position/altitude-ft')-altitude) > 0.1:
            raise ValueError('Empty or moving scene; inspect the paused session.')
        (folder / 'exterior.jpg').write_bytes(content)
        metadata = dict(camera=settings, altitude_ft=altitude,
                        scene='CYJN, paused presentation; not flight validation',
                        aircraft_dir=get('/sim/aircraft-dir'),
                        fg_version=get('/sim/version/flightgear'),
                        sha256=hashlib.sha256(content).hexdigest())
        (folder / 'capture.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    finally:
        for p, v in saved.items():
            execute(f'setprop("{p}",{float(v)});', port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--port', type=int, default=18101)
    args = parser.parse_args()
    capture(args.folder, args.port)
```

## 5. Mesurer l’image en pixels

Un pixel est un petit carré de couleur. Notre capture mesure 1 280 pixels de large et 720 de haut. FlightGear attend une miniature JPEG de **171 × 128 pixels**, appelée thumbnail.jpg, à la racine de l’appareil.

Si nous écrasons directement le grand rectangle dans le petit, l’avion devient trop haut. Nous gardons donc les proportions : 171 ÷ 1 280 = 0,13359375. La hauteur réduite vaut 720 × 0,13359375 = 96,1875, arrondie à 96 pixels. Il reste 128 − 96 = 32 pixels, soit 16 pixels noirs au-dessus et 16 au-dessous. Aucun morceau d’aile n’est coupé.

![Miniature de 171 par 128 pixels](https://github.com/steveprudhomme/sw233-flightgear/releases/download/selecteur-15/thumbnail.jpg)

Dans tools/package.py, `ImageOps.pad` réalise ce travail avec le filtre LANCZOS. La qualité JPEG est réglée à 95. La grande image est copiée octet pour octet ; seule la miniature est réduite. Aucun détail du planeur n’est ajouté ou retouché.

## 6. Fabriquer le paquet avec son aperçu

La recette complète du constructeur se trouve dans la [fiche 12](12-installation.md), actualisée pour cette option. Depuis la racine du dépôt :

```powershell
python tools/package.py --output build/avec-apercu --preview notes/selecteur/exterior.jpg
```

Le constructeur exige un JPEG d’au moins 1 024 × 600 pixels. Il refuse une miniature utilisée par erreur comme grande image. Cette limite est notre contrôle de projet, pas une dimension imposée par FlightGear.

Il crée thumbnail.jpg et Previews/sw233-exterior.jpg dans Aircraft/SW233. Il ajoute, uniquement dans le fichier set du paquet, un élément sim/previews/preview : type vaut exterior, path vaut Previews/sw233-exterior.jpg et splash vaut true avec le type bool. Ce dernier réglage permet l’utilisation au chargement ; notre contrôle visuel porte ici sur le sélecteur.

Le manifeste inclut les deux JPEG et le XML du paquet. Le lanceur vérifie leurs empreintes avant de démarrer. Si tu changes la photo, reconstruis un paquet neuf ; ne corrige pas les empreintes à la main pour cacher une différence.

Sans l’option `--preview`, la fabrication reste possible hors réseau et n’ajoute aucun lien vers une image absente. Elle ne télécharge jamais de photographie automatiquement. Pour reproduire exactement notre paquet, télécharge exterior.jpg depuis la publication liée au-dessus au lieu de refaire la capture.

## 7. Vérifier dans le vrai lanceur

Ferme tes autres sessions FlightGear après avoir sauvegardé ton travail. Ouvre le lanceur en lui donnant le dossier Aircraft du nouveau paquet. Dans PowerShell, depuis la racine du dépôt, adapte le chemin du programme et celui de fgdata :

```powershell
$avions = (Resolve-Path 'build/avec-apercu/Aircraft').Path
& 'C:/Program Files/FlightGear 2024.1/bin/fgfs.exe' --launcher `
  '--fg-root=C:/Users/steve/FlightGear/Downloads/fgdata_2024_1' `
  "--fg-aircraft=$avions"
```

Clique Aircraft, puis Installed Aircraft. Cherche Schweizer. La petite image doit apparaître dans la liste. Double-clique la ligne : tu dois voir l’aperçu plus grand, la description, la licence et les auteurs.

![La miniature dans la liste des appareils installés](https://github.com/steveprudhomme/sw233-flightgear/releases/download/selecteur-15/selector-list.png)

![La fiche détaillée vérifiée dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/selecteur-15/selector-detail.png)

Notre essai utilise un paquet dans un dossier avec espaces, « Selecteur SW233 15 ». Le chemin en bas de la fiche prouve quelle copie le lanceur a trouvée. Les pastilles Ratings sont l’interface du lanceur ; nous n’avons pas renseigné de notes de qualité.

Difficulté rencontrée : plusieurs instances FlightGear étaient déjà ouvertes. Le lanceur de contrôle a utilisé un profil isolé et `--read-only`, avec une copie cohérente du cache de navigation existant. Un profil vide dans ce mode affichait « Missing navigation cache ». Ce détour de test n’est pas nécessaire pour ton utilisation ordinaire : préfère une seule session et ton profil habituel. Ne supprime pas ton cache pour reproduire ce problème.

## 8. Contrôler et expliquer ce qui est terminé

Depuis le dépôt avec les dépendances de développement de la fiche 12 :

```powershell
python -m unittest discover -s tests
python -m ruff check --no-cache tools tests
python tools/check.py
python tools/check_workbook.py build/livre-selecteur
```

Les 21 tests passent. Deux nouveaux tests vérifient notamment les deux modes avec/sans aperçu, le format de miniature, la copie exacte du JPEG, sa présence au manifeste, le refus d’une image trop petite et la détection d’une miniature supprimée. La reconstruction du tutoriel vérifie les sources de l’avion. Les captures ci-dessus apportent le contrôle visuel que les tests seuls ne peuvent pas fournir.

**Sur quoi nous appuyons-nous ?** Sur les conventions [Splash screen](https://wiki.flightgear.org/Splash_screen), la [structure standard des appareils](https://wiki.flightgear.org/Standard_aircraft_structure), l’exemple c172p-set.xml installé et les [options FlightGear 2024.1](https://flightgear.gitlab.io/getstart/release-2024.1/en/HTML/getstart-ench4.html), puis sur le contrôle natif illustré ici.

**Biais et limites :** le cadrage est choisi pour rendre l’avion lisible, pas pour mesurer sa fidélité géométrique. Un seul environnement Windows a été contrôlé ; Linux reste AUD-02c. La présence dans notre sélecteur local n’est pas une admission au catalogue officiel. Le cockpit photographique, la livrée finale et la validation aérodynamique restent des tâches distinctes dans ROADMAP.md.

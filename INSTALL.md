# Installer et lancer SW233

## Préparer

Installer FlightGear et ses données, Python 3.11 ou plus récent, puis les scènes de CYJN (Saint-Jean-sur-Richelieu). Le paquet n’inclut ni FlightGear ni le décor. Windows et FlightGear 2024.1.7 ont été vérifiés ; l’essai natif Linux reste à faire.

Ouvrir PowerShell **dans la racine du dépôt**, là où se trouvent README.md et tools. Dans l’Explorateur, ouvrir ce dossier, écrire `powershell` dans sa barre d’adresse et appuyer sur Entrée. Les chemins de l’exemple correspondent à l’installation de Steve : les adapter sur un autre ordinateur.

## Fabriquer un paquet neuf

```powershell
python -m pip install Pillow==12.0.0
python tools/package.py --output "build/SW233 pret a voler"
```

Le dossier contient Aircraft/SW233, les textures produites par la recette, la licence, un manifeste et les deux entrées du lanceur. Une destination déjà utilisée est refusée : choisir un nouveau nom pour chaque version. Après fabrication, **tout le dossier peut être déplacé** ; le lanceur doit rester à côté de Aircraft et manifest.json.

## Vérifier les chemins sans démarrer

```powershell
python "build/SW233 pret a voler/launch.py" `
  --fgfs "C:/Program Files/FlightGear 2024.1/bin/fgfs.exe" `
  --fg-root "C:/Users/steve/FlightGear/Downloads/fgdata_2024_1" `
  --scenery "C:/Users/steve/FlightGear/Downloads/TerraSync" `
  --check
```

Le contrôle vérifie les empreintes du paquet, les ressources nécessaires, le programme, les fichiers defaults.xml/version de fgdata, les seuils de CYJN et la présence d’un terrain dans la zone. Il ne prouve pas que toute la scène est complète : vérifier le paysage au lancement. Il n’effectue aucun téléchargement et ne corrige pas automatiquement les fichiers.

## Démarrer

Retirer **--check** de la commande précédente. Le départ se fait **au sol**, à CYJN, vent nul et date de démonstration fixe pour conserver un éclairage comparable. Aucune commande de vol automatique n’est activée. Le lanceur affiche le chemin exact du paquet et la commande passée à FlightGear.

Pour vérifier le vol, ajouter **--mode air** : départ à 5 000 ft et 60 kt, sans trim imposé ni pilote automatique. Le planeur ne décolle pas seul depuis le sol.

L’entrée Windows **start-sw233.cmd** accepte les mêmes arguments et requiert aussi Python dans PATH. Exemple depuis un autre répertoire après déplacement :

```powershell
& "C:/Mon dossier/SW233/start-sw233.cmd" `
  --fgfs "C:/Program Files/FlightGear 2024.1/bin/fgfs.exe" `
  --fg-root "C:/Mon dossier/fgdata" `
  --scenery "C:/Mon dossier/TerraSync" --check
```

Ces trois derniers dossiers sont des exemples : les remplacer par les vrais chemins. Un double-clic sans arguments ne configure pas l’installation ; utiliser le terminal pour lire les erreurs. Le [tutoriel illustré, fiche 12](docs/construction/12-installation.md) explique chaque étape.

## Contrôles dans FlightGear

- Vérifier la présence de la piste et du terrain de CYJN, puis des textures du tableau.
- Ouvrir **SW233 → Occupants et centrage**, avion arrêté au sol.
- Essayer solo/biplace et Restaurer ; les chiffres du haut du clavier sont validés, avec un point décimal. Le pavé numérique reste suivi sous AUD-01d.
- Vérifier les commandes FlightGear habituelles de profondeur, ailerons, direction et aérofreins. Le lanceur ne remplace pas les affectations du joystick.

## Dépannage

| Message ou symptôme | Action |
|---|---|
| Python/PIL introuvable | Vérifier Python, puis installer Pillow pour fabriquer le paquet. Le paquet déjà fabriqué ne nécessite pas Pillow pour démarrer. |
| Destination déjà existante | Choisir un dossier de sortie neuf ; aucun écrasement automatique. |
| Fichier absent ou modifié | Reconstruire depuis les sources ; ne pas modifier les empreintes pour masquer le problème. |
| Programme introuvable | Donner le chemin complet de fgfs.exe, pas celui du raccourci. |
| defaults.xml/version absent | Choisir la racine des données FlightGear, pas le répertoire Aircraft. |
| Terrain CYJN absent | Installer la zone dans le dossier scenery indiqué, puis relancer --check. |
| Océan malgré le contrôle | Vérifier le chemin de scène réellement chargé et compléter le terrain ; la présence d’une tuile ne certifie pas toute la zone. |
| Ancienne version affichée | Relire « Paquet vérifié » et fermer l’ancienne session pour éviter la confusion. |

## Développement et bancs

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m ruff check .
python tools/check_workbook.py build/livre-verifie
```

Sur Linux, utiliser `.venv/bin/python` ; cette instruction n’est pas une affirmation d’essai natif FlightGear Linux. JSBSim autonome est verrouillé dans requirements-dev.txt ; sa version peut différer du moteur embarqué. Voir [validation](docs/validation.md).

Le serveur HTTP reste désactivé par défaut. Pour un banc local dédié, ajouter **--http-port 18099**, puis suivre la fiche 12. Les empreintes du manifeste détectent des changements ; elles ne constituent pas une signature d’authenticité. Le champ source_revision indique le commit de base lors de la fabrication ; un paquet préparé depuis des fichiers modifiés doit être identifié par ses empreintes, pas seulement par ce commit.

## Ajouter la miniature et l’aperçu

Depuis la racine du dépôt, fabriquer un dossier neuf avec une capture JPEG native :

```powershell
python tools/package.py --output build/avec-apercu --preview notes/selecteur/exterior.jpg
```

Le fichier doit exister et mesurer au moins 1024 × 600 pixels. Le constructeur ne télécharge aucune image. Sans --preview, il produit un paquet utilisable sans références d’aperçus. La [fiche 13](docs/construction/13-selecteur.md) explique la capture, le téléchargement facultatif de la référence publiée et la vérification dans le lanceur. Le paquet avec images est disponible dans [selecteur-15](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/selecteur-15). Le minimum déclaré est 2024.1.7, version testée ; aucune compatibilité antérieure n’est affirmée.

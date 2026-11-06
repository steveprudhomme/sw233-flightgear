# Ton atelier : construis et filme un planeur

**Pour fabriquer les fichiers toi-même depuis un dossier vide, commence par le [livre de construction en sept séances](construction/README.md).** Cette page est le parcours rapide pour assembler et filmer une copie du projet.


**Ta mission :** partir d’un dossier de pièces, assembler un planeur dans FlightGear, passer au-dessus d’un vrai lieu et rapporter un film. Le vol est piloté par le scénario. Tu peux réussir cet atelier sans joystick ni compte GitHub. Cette édition utilise Windows.

## 1. Prépare ton établi

Il te faut un ordinateur qui fait déjà tourner FlightGear, une connexion pour le premier téléchargement et de la place pour les données et la vidéo. Si Windows demande le mot de passe de l’administrateur pour installer un programme, demande à la personne qui gère l’ordinateur. Tu n’en auras pas besoin pour modifier ta copie du planeur.

- Installe [FlightGear](https://www.flightgear.org/download/) avec ses **données de base**. Notre prise utilise la version 2024.1.4. Ouvre-le une première fois, fais apparaître un avion, puis ferme-le.
- Installe [Python](https://www.python.org/downloads/windows/) 3.11 ou 3.13 avec son lanceur Windows **py**. C’est l’outil qui assemble les pièces.
- Installe [FFmpeg](https://ffmpeg.org/download.html), l’outil qui met les images en vidéo. Sa commande doit être accessible depuis le terminal. Si les outils sont déjà installés, passe à la vérification.
- Sur la [page du projet](https://github.com/steveprudhomme/sw233-flightgear), clique **Code → Download ZIP**. Dans Téléchargements, clique droit sur le ZIP, puis **Extraire tout**. Entre dans le dossier qui contient **atelier.py** et **README.md**. Dans la barre d’adresse de ce dossier, écris **powershell**, puis appuie sur Entrée. C’est ici que tu copieras les commandes, une ligne à la fois.

```powershell
py --version
ffmpeg -version
```

**Tu dois voir :** deux numéros de version. Si une commande est inconnue, ferme et rouvre le terminal après l’installation. Pour FFmpeg, si tu as téléchargé une archive Windows, le fichier recherché est **ffmpeg.exe** dans le dossier **bin**. Tu peux le copier dans le dossier du projet, puis taper la ligne suivante dans ce terminal pour l’y trouver :

```powershell
$env:Path = "$((Get-Location).Path);" + $env:Path
```

## 2. Assemble le planeur et le terrain

Crée une boîte à outils réservée à ce projet. La première commande crée le dossier **.venv**. La deuxième y installe la peinture numérique et le moteur de test. La troisième télécharge environ 20 Mo de décor pour Saint-Jean-sur-Richelieu, au Québec.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools\scenery.py
```

**Tu dois voir :** « Décor prêt ». Imagine une tuile de jeu de société : celle-ci contient le sol et les pistes de **CYJN**. Sans la tuile, tu pourrais voir de l’eau. En cas de coupure, relance la troisième ligne ; elle vérifie aussi les fichiers déjà présents.

## 3. Fais ton premier film

Ferme FlightGear, puis lance :

```powershell
.\.venv\Scripts\python.exe atelier.py
```

Le programme te montre trois chemins : le simulateur, ses données et le décor. Appuie sur **Entrée** si le chemin est bon. Sinon colle le tien : le premier se termine par **fgfs.exe**, le deuxième contient **defaults.xml**, et le troisième contient **Terrain**. Le décor de l’étape 2 est choisi automatiquement.

Garde la fenêtre à sa taille de départ. Attends le chargement, les 83 secondes de vol et le montage. **Tu dois voir :** « Ton film est prêt ». Ouvre le dossier **build**, puis le nouveau dossier **atelier-…**. Double-clique sur **Mon-vol-CYJN.mp4**. Chaque essai obtient son propre dossier.

| Temps | Défi d’observation |
| --- | --- |
| 8 à 28 s | Repère la poignée orange en bas à gauche. Elle bouge quand les aérofreins sortent et rentrent. |
| 29 à 43 s | Regarde le dessus des ailes. Le pilote répète la manœuvre : vois-tu les deux panneaux se lever, puis disparaître ? |
| 46 à 61 s | Regarde la petite ficelle rouge. En glissade, l’air arrive aussi de côté ; le fil quitte le milieu. Le cadre agrandi vient de la même image. |
| 61 à 73 s | Retrouve le même virage vu du dehors. Regarde l’aile inclinée pendant que le vol continue. |
| Après 76 s | Retour dans le cockpit : le planeur se redresse et le fil revient vers le milieu. |

## 4. Ouvre le capot : comment l’a-t-on construit ?

Ces fichiers sont du texte. Ouvre-les avec le Bloc-notes. Travaille dans ta copie extraite. Le dossier **src** est ton original ; **build** est ce que tu as assemblé.

1. **Choisir les formes.** Lis [l’inventaire](references/inventaire.md) et [les décisions de conception](references/conception.md). Un dessin de dessus aide à placer les ailes ; une photo de face aide à placer les cadrans. Les plans de maquette ne donnent pas toutes les mesures du vrai planeur. Repère **tube-pitot**, **fil-de-laine** et **tableau** dans **src/SW233/Models/sw233.ac** : ce sont trois pièces différentes. Ce fichier contient les points et les faces de la maquette.
2. **Brancher les pièces.** Dans **src/SW233/sw233-set.xml**, trouve **sw233-model.xml**. C’est la fiche qui dit à FlightGear où trouver la maquette. Ouvre ce second fichier dans **Models** et cherche **fil-de-laine** : tu trouveras son axe de rotation et la valeur qui le fait tourner. Dans **src/SW233/Checklists/sw233.xml**, retrouve une liste du pilote.
3. **Faire voler la maquette.** Dans **src/SW233/sw233.xml**, cherche **wingarea**, la surface des ailes, puis **LIFT**, la force qui porte le planeur. JSBSim fait les calculs. FlightGear dessine le résultat. Les nombres de notre prototype sont des hypothèses de simulation : on les compare à des essais avant de les croire.
4. **Peindre ton propre tableau.** Dans **tools/panel.py**, repère le texte **RADIO** entre guillemets. Remplace seulement les lettres par **VHF**. Garde les guillemets. Enregistre puis refais l’étape 3. Recharge ton avion dans FlightGear et regarde sous le petit écran de la radio. Si le changement ne te plaît pas, remets le texte initial. Les trois aiguilles continuent de bouger : elles sont séparées de la peinture.
5. **Vérifier le vol.** Lance ces deux commandes. La première vérifie, entre autres, que les aérofreins augmentent la traînée. La seconde fait une minute de vol calculé sans ouvrir une fenêtre de FlightGear. Lis la vitesse et l’altitude finales. Un résultat différent d’un vrai planeur est une invitation à chercher pourquoi.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tools\glide.py --speed 50 --seconds 60
```

6. **Comprendre le film.** Ouvre **tools/native-demo.nas**. Cherche **video-start** puis **video-stop** : entre les deux, FlightGear enregistre. Cherche **view-number** : 0 place tes yeux dans le cockpit, 1 les place dehors. Dans **tools/annotate.py**, les légendes sont ajoutées après le vol à partir des valeurs enregistrées. Le fichier **vol.log** de ton essai contient ces valeurs, aux lignes **SW233_SAMPLE**.
7. **Garder tes versions.** Tu peux garder deux dossiers datés sans publier quoi que ce soit. Si tu utilises déjà Git, [le guide de contribution](../CONTRIBUTING.md) explique comment enregistrer un petit changement et le signer. La [feuille de route](../ROADMAP.md) montre ce qu’il reste à réaliser, dont la vraie peinture des Cadets.

**Si quelque chose coince :** « aucun fichier atelier.py » veut dire que le terminal n’est pas ouvert dans le bon dossier. « Programme ou données introuvables » veut dire qu’il faut corriger un des chemins de l’étape 3. Si tu vois du bleu sans aucune piste, vérifie que le dossier de décor choisi contient **Terrain/w080n40/w074n45/CYJN.btg.gz**. Si un film est incomplet, garde **vol.log**, ferme le simulateur et recommence dans un nouvel essai.

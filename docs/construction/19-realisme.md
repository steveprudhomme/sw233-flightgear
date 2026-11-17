# 19 — Verre, peinture extérieure et équipage

## A. Deux sortes de reflet

Un éclat de soleil est un point brillant. Une réflexion d’environnement montre
une image autour de l’objet. Ici FlightGear utilise son ciel fair-sky fourni :
cette image ne connaît pas les bâtiments sous ton planeur. L’effet dépend du
rendu compatible ; le matériau transparent sert de repli.

## B. Créer les effets

Crée le dossier src/SW233/Effects, puis ces deux fichiers UTF-8. La force 0,25
concerne la verrière ; 0,12 concerne les cadrans. Ce sont des réglages
artistiques. Le givre et la buée sont désactivés dans cet effet local.

<!-- atelier-fichier: src/SW233/Effects/canopy-glass.eff -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- SPDX-License-Identifier: GPL-3.0-only -->
<PropertyList>
  <name>Aircraft/SW233/Effects/canopy-glass</name>
  <inherits-from>Effects/glass</inherits-from>
  <parameters>
    <!-- Built-in fair-sky cubemap: a static environment, not the live scenery. -->
    <use-reflection type="int">1</use-reflection>
    <reflection-strength><use>/sim/sw233/visuals/canopy-reflection</use></reflection-strength>
    <frost-level type="float">0</frost-level>
    <fog-level type="float">0</fog-level>
    <rnorm type="float">0</rnorm><gsnorm type="float">0</gsnorm>
  </parameters>
</PropertyList>
```

<!-- atelier-fichier: src/SW233/Effects/instrument-glass.eff -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- SPDX-License-Identifier: GPL-3.0-only -->
<PropertyList>
  <name>Aircraft/SW233/Effects/instrument-glass</name>
  <inherits-from>Effects/glass</inherits-from>
  <parameters>
    <!-- Built-in fair-sky cubemap: a static environment, not the live scenery. -->
    <use-reflection type="int">1</use-reflection>
    <reflection-strength><use>/sim/sw233/visuals/instrument-reflection</use></reflection-strength>
    <frost-level type="float">0</frost-level>
    <fog-level type="float">0</fog-level>
    <rnorm type="float">0</rnorm><gsnorm type="float">0</gsnorm>
  </parameters>
</PropertyList>
```


## C. Ajouter une feuille transparente devant les aiguilles

Imagine le verre d'une montre : le verre doit être devant l'aiguille, sans la toucher.
Les nouveaux disques s'appellent `ias-vitre`, `alt-vitre` et `vsi-vitre`.
Leur recette se trouve dans [le maillage, section I sexies](02-maillage.md).

1. Repère `px = 0.87`, la position du tableau dans notre repère de construction.
2. Place chaque disque à `px + 0.019 = 0.889 m`. L'aiguille est à 0.882 m :
   il reste donc 7 mm. Ce jeu est un choix de modèle, pas une mesure sur l'appareil réel.
3. Prends les centres et rayons déjà utilisés par les trois instruments.
   Les rayons sont 67, 75 et 55 mm. Ne mesure pas une autre fois sur une photo inclinée :
   tu risquerais de fabriquer un verre qui ne recouvre pas notre cadran.
4. Coupe le cercle en 64 parts, comme une tarte. Chaque triangle va du centre
   à deux points du bord. Un tour vaut `2 × pi` radians.
5. Le matériau a une transparence de 0,96 : il est presque invisible.
   Le shader ajoute une image de ciel à sa couleur. Il ne change pas cette transparence.

Les pièces restent séparées des aiguilles. Dans [la configuration](04-configuration.md),
les deux blocs `effect` nomment exactement les quatre panneaux et les trois disques.
Une lettre manquante dans un nom suffit à laisser une pièce sans effet.

## D. Construire et ouvrir la bonne copie

Depuis le dossier du dépôt, fabrique un **nouveau** paquet avec la commande suivante.
Le nom `build/verre-essai` ne doit pas déjà exister. Le programme s'arrête au lieu
d'écraser ton ancien travail.

```powershell
python tools/package.py --output build/verre-essai
```

Ouvre cette copie dans FlightGear selon [la fiche d'installation](12-installation.md).
Pour reproduire le rendu testé, ajoute `--prop:/sim/rendering/shaders/skydome=true`
aux options **de FlightGear**, pas aux options du script Python. Cela active la
condition ALS utilisée par l'effet `Effects/glass` de FlightGear 2024.1.7.
Sans cette condition, le verre reste transparent mais le reflet peut être absent.
Ne modifie pas le fichier global `Effects/glass.eff` de ton installation.

## E. Comparer sans se tromper — premières preuves du lot 39

Un changement de caméra ou de soleil peut donner l'impression qu'un matériau
s'est amélioré. Pour une comparaison utile, garde le même angle et la même lumière.
Notre banc `tools/glass_bench.py` utilise une séance de développement `--fdm=null` :
le planeur est immobile et ces essais ne prouvent rien sur ses qualités de vol.

1. Prends une image avec les deux forces de reflet à 0.
2. Sans bouger la caméra, mets les forces à 1 et prends une deuxième image.
3. Remets 0,25 pour la verrière et 0,12 pour les cadrans.
4. Recommence du siège pilote, en regardant de côté et depuis l'extérieur.
5. Vérifie la ficelle, le terrain, les graduations et les aiguilles.
6. Clique sur le bouton de calage et celui de la radio. Un beau verre qui empêche
   de tourner un bouton serait une régression.

![Même vue sans reflet](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/pilote-sans.jpg)

![Même vue avec reflet volontairement fort](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/pilote-fort.jpg)

![Réglage retenu, reflet discret](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/pilote-regle.jpg)

Les clics natifs ont fait passer le calage de 29,92 à 29,93 inHg ; la commande
fine COM1 a produit une fréquence de 118,325 MHz. Les commandes restent accessibles.
Le reflet des cadrans est volontairement faible ; ce résultat n'est pas du verre
photographiquement réaliste. Le ciel réfléchi est fixe, et les panneaux restent facettés.

![Contrôle des commandes dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/cockpit-clicks.jpg)

## F. Voir chaque pièce et comprendre les limites

Télécharge [l'atlas](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/atlas.zip),
décompresse-le et ouvre `index.html`. Chaque pièce possède une vue de profil,
de dessus et de face. Ce sont des dessins de construction ; les images ci-dessus
sont des captures du simulateur. Ne confonds pas ces deux sortes de preuve.

La peinture extérieure se construit dans [la fiche 20](20-livree.md), puis les
personnages dans [la fiche 21](21-equipage.md). Les tests de ressources suivent
les liens de fichiers : modèle → sous-modèle → texture et effet. Une texture oubliée
fait maintenant échouer la construction du paquet avec un message explicite.

**Sur quoi repose cette étape ?** Sur les fichiers `Effects/glass.eff` et
`Shaders/glass-ALS.frag` installés avec FlightGear 2024.1.7, la géométrie du projet
et les comparaisons natives. Les forces, teintes et épaisseurs sont des choix artistiques.
Notre biais est de préférer la lisibilité à un reflet spectaculaire. Les captures ne
prouvent pas l'exactitude optique du vrai plexiglas ; les autres moteurs de rendu,
le tri des transparences à tous les angles et les performances sur un autre ordinateur
restent à contrôler.

## G. Lot 40 : regarder le verre sous deux orientations

Imagine une fenêtre que tu regardes depuis trois places. Pour comparer les reflets,
tu changes une seule chose à la fois. Notre banc fait tourner le planeur vers le
cap **010°**, puis vers le cap **190°**. Le soleil et l'heure ne changent pas : la
lumière arrive donc de l'autre côté du planeur. Ces nombres sont les caps de l'avion,
**pas une mesure de la direction du soleil**. Ne les appelle pas « soleil devant »
et « soleil derrière » sans avoir mesuré cette direction.

Voici les trois places utilisées à chaque cap. Les angles de caméra sont des
réglages du simulateur, pas des dimensions du véritable planeur.

| Place | Vue FlightGear | Direction de caméra | Inclinaison | Champ visible |
|---|---:|---:|---:|---:|
| Pilote | 0 | 0° | −18° | 65° |
| Oblique | 0 | 70° | 0° | 75° |
| Extérieur | 1 | 140° | 15° | 25° |

À chaque place, le banc prend trois images : `sans` (forces 0/0), `fort` (1/1)
et `regle` (0,25 pour la verrière, 0,12 pour les cadrans). Cela donne **18 images**.
Le nom `h190-oblique-regle.jpg` signifie : cap 190°, vue oblique, réglage retenu.
Le programme conserve les JPEG reçus de FlightGear sans retoucher leurs pixels.

Dans une séance réservée aux essais, ouvre le paquet du lot 40 avec `--fdm=null`
et une interface HTTP locale, comme pour les bancs précédents. Le numéro indiqué
après `--port` doit être celui de cette séance. Depuis le dépôt, par exemple :

```powershell
python -m tools.glass_bench D:/SW233-work/visuals-40/glass-matrix --port 18144
```

Le dossier de sortie doit être nouveau. Ne lance pas deux bancs sur la même séance.
Le programme refuse un autre avion et une séance JSBSim : il doit pouvoir changer
le cap sans faire voler l'avion. Il remet ensuite chaque vue visitée, le cap, les
forces de reflet, le menu et la pause à leurs valeurs enregistrées. Si une capture
échoue, il tente quand même cette remise en place et écrit le résultat dans
`checks.json`. Si `restored` vaut `false`, arrête les essais et lis
`restoration_errors` avant de continuer.

Les liens suivants désignent les fichiers de preuve du lot 40. Une comparaison
doit toujours utiliser les trois images de **la même ligne**. Les captures et leur
inspection doivent être terminées avant de déclarer V40-02 réussi.

| Cap et place | Force nulle | Force forte | Réglage retenu |
|---|---|---|---|
| 010°, pilote | [sans](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-pilote-sans.jpg) | [fort](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-pilote-fort.jpg) | [réglé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-pilote-regle.jpg) |
| 010°, oblique | [sans](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-oblique-sans.jpg) | [fort](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-oblique-fort.jpg) | [réglé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-oblique-regle.jpg) |
| 010°, extérieur | [sans](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-exterieur-sans.jpg) | [fort](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-exterieur-fort.jpg) | [réglé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h010-exterieur-regle.jpg) |
| 190°, pilote | [sans](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-pilote-sans.jpg) | [fort](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-pilote-fort.jpg) | [réglé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-pilote-regle.jpg) |
| 190°, oblique | [sans](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-oblique-sans.jpg) | [fort](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-oblique-fort.jpg) | [réglé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-oblique-regle.jpg) |
| 190°, extérieur | [sans](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-exterieur-sans.jpg) | [fort](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-exterieur-fort.jpg) | [réglé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/h190-exterieur-regle.jpg) |

Pour chaque ligne, cherche les aiguilles, les chiffres, la ficelle et le terrain
là où le cadrage les montre. Un panneau devient-il opaque ou disparaît-il ?
L'image fixe ne prouve pas l'absence de scintillement : regarde aussi le simulateur
pendant une petite rotation, puis reviens au cadrage pour les comparaisons.
Recommence les clics de calage et de radio séparément. Un changement de couleur
mesuré sur les images ne prouve ni la beauté du reflet ni sa fidélité au vrai verre.

## H. Compter les images sans annoncer une fausse victoire

Une limite de 60 images par seconde ressemble à un robinet fermé à moitié : un
ordinateur plus rapide ne peut pas dépasser cette limite. Deux résultats proches
de 60 ne prouvent donc pas que le nouveau verre ne coûte rien.

Pour une séance d'essai séparée, on peut transmettre cette option à **FlightGear** :

```text
--prop:/sim/rendering/vsync-enable=false
```

Ce nom de propriété est présent dans le programme FlightGear 2024.1 installé.
Le banc enregistre sa valeur dans `checks.json`, mais ne la change pas. Utilise
un dossier de préférences propre à la séance d'essai ; ne modifie pas les réglages
globaux de l'utilisateur. Même avec cette option, le pilote de la carte graphique
ou l'affichage peut imposer une autre limite. Il faut regarder les mesures avant
de dire que la cadence est libérée.

Le banc lit le compteur `/sim/frame-number`, attend une seconde, puis le relit.
Il divise les nouvelles images par le temps réellement écoulé. Par exemple,
120 nouvelles images en deux secondes donnent 60 images par seconde. La propriété
`/sim/frame-rate`, parfois nulle en pause, est conservée dans le rapport mais ne
sert pas au calcul.

Par défaut, chaque groupe de trois forces est mesuré **trois fois**, soit 54
mesures pour les six cadrages. L'ordre est inversé une fois sur deux pour ne pas
toujours favoriser le premier réglage. On compare les forces d'une même répétition,
puis on prend l'écart du milieu : la **médiane**. `--repeats 5 --interval 2`
permet des essais plus longs. Les images ne sont prises que lors de la première
répétition, après la mesure, pour ne pas inclure l'enregistrement JPEG dans le temps.

Ce compteur mesure la cadence globale du simulateur, pas le temps de calcul du
verre sur la carte graphique. La scène et l'ordinateur comptent aussi. Un plafond,
une faible différence ou quelques mesures instables laissent la mesure du coût
GPU ouverte. Publie ces limites avec les chiffres ; ne promets pas les mêmes
résultats sur une autre machine.

## I. Vérifier le repli sans ALS dans une autre séance

Ferme la séance d'essai, puis lance une autre copie dédiée avec
`--prop:/sim/rendering/shaders/skydome=false`. Le banc ne change pas cette propriété.
Enregistre ses images dans un **autre dossier** pour conserver celles d'ALS.
Dans ce mode, on attend surtout un verre transparent et des instruments lisibles,
pas le même reflet de ciel. La valeur `skydome_shader` dans le rapport permet de
distinguer les deux essais. L'absence de différence entre les forces 0 et 1 peut
être normale dans ce repli ; elle ne suffit pas à prouver que les panneaux sont
visibles. Il faut regarder les images et vérifier les commandes.


### Résultat de la matrice du 17 novembre 2026

Le banc a produit 18 captures et 54 mesures appariées, sous FlightGear 2024.1.7,
avec les vitrages du paquet visuals-39 (géométrie et effets conservés dans le lot40).
Les deux vues mémorisées et les propriétés ont été restaurées sans erreur.
Les cadrans, la ficelle et le paysage restent visibles dans les vues inspectées.

La désactivation de VSync a été demandée au lancement ; les valeurs mesurées restent
entre 59,84 et 60,98 images/s, médiane 60,00. Cela reste compatible avec un plafond
d'affichage. On ne peut donc pas annoncer un coût GPU isolé. Le paramètre de lancement
n'est pas une preuve que le pilote graphique a désactivé toute synchronisation.
La [documentation de profilage FlightGear](https://wiki.flightgear.org/Profiling_performance)
signale aussi la dépendance aux réglages du pilote. Nous n'avons pas changé ces
préférences globales. Le repli sans ALS est contrôlé séparément dans le paquet intégré.

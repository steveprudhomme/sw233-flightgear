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

## E. Comparer sans se tromper

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

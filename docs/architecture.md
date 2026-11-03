# Architecture

Le paquet installé est Aircraft/SW233. Le set FlightGear sélectionne `jsb` et
le fichier `sw233.xml`. JSBSim charge métriques, masses, contacts, commandes,
puis aérodynamique. Le modèle AC3D est exclusivement visuel.

Les fichiers XML et AC3D dans src/ sont les sources canoniques éditables.
tools/package.py en fait une copie d'installation ignorée par Git. Aucun outil
de génération n'est requis pour éditer les coefficients ou la géométrie.

Les positions du FDM suivent le repère structural : X arrière, Y droite, Z haut,
en pouces. Forces et moments suivent les conventions JSBSim. Les fonctions de
coefficient sont sans dimension, puis multipliées par qS, qSb ou qSc selon l'axe.
Les termes p et r utilisent b/(2V) ; q et αdot utilisent c/(2V).

Les propriétés `aero/sw233/*` sont privées au modèle et calculées avant les axes.
Les commandes entrent par `fcs/*-cmd-norm` ; la profondeur et le trim sont sommés
et bornés. La sortie normalisée des aérofreins est bornée entre 0 et 1.

La géométrie visuelle sert à vérifier l'installation. Cockpit, animations,
remorquage et instruments seront des incréments séparés et testés.

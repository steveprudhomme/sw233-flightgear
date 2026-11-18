# DIM-53c · Pneu sur terrain incliné — lot54

**Public :** contributeur qui connaît le modèle et les commandes Python.
**Date :** 18 novembre 2026. **FlightGear :** 2024.1.7.
**Version :** 0.1.0-alpha.4 en préparation, sans publication.
Le plan a été enregistré avant la correction dans le commit `2b9307e`.

## Résultat

Les cinq sondes mesurent la surface sous la roue dans les axes du modèle.
La roue remonte selon cette surface, sa largeur et ses vingt côtés.
Le contrôle indépendant lit les sommets du fichier AC3D.
Il ne recopie pas la formule trigonométrique du programme Nasal.

| Surface construite | Sens testés | Déplacement avec 3 cm de pénétration au centre |
|---|---|---|
| Horizontale | Sans pente | 3,00 cm |
| Longitudinale, 25° | Positif et négatif | 5,33 cm |
| Latérale, 25° | Positif et négatif | 6,50 cm |
| Combinée, 20° sur chaque axe | Deux signes identiques | 7,29 cm |

Les sept rampes sont chargées comme objets solides dans le décor natif.
Le banc contrôle leur pente mesurée, avec une tolérance de 0,001 sur chaque coefficient.
L’écart maximal entre déplacement natif et calcul sur les sommets est inférieur à 0,01 mm.
Cette valeur mesure l’accord numérique du dessin. Elle ne décrit pas la précision d’un pneu réel.

Les captures avant montrent une animation neutralisée, pas un ancien paquet.
Les captures après utilisent la correction, sans changer la pose ni la caméra.
Voir les [comparaisons illustrées de l’atelier 33](../construction/33-pneu-pentes.md).

## Contrôles natifs

- Sept surfaces mesurées par les sondes réelles de FlightGear.
- 34 contrôles du nouveau calcul : signes de pente, hauteurs, absence de contact et échantillons inutilisables.
- 24 contrôles conservés du calcul précédent, utilisé en secours.
- Terrain absent simulé : mode `fallback-flat`, déplacement de 0,012192 m pour une compression de 0,04 pied.
- En vol : mode `airborne`, déplacement nul et aucune sonde appelée.
- À CYJN : impulsion physique de roulage ; vitesse maximale relevée de 4,54 nœuds, puis arrêt.
- Quatorze contrôles de verrière réussis ; ouverture réelle au repos jusqu’à la position 1.

Les rampes utilisent `--fdm=null` et une pose imposée.
Le roulage à CYJN utilise JSBSim, le calcul des forces du vol.
Aucun atterrissage ni roulage dynamique sur les rampes fortes n’est validé par ce lot.

Les [données détaillées](pneu-pentes-lot54.json) contiennent les résultats et les empreintes des captures.
Les vues rapprochées utilisent la vue 1, un champ de 7° et une cible placée sur la roue.
Les images proviennent du simulateur ; elles ne sont pas retouchées.

## Choix et limites

Les sondes suivent la verticale du modèle. Elles partent 2 m au-dessus du contact nominal.
Leurs positions couvrent le centre et quatre points distants de 0,25 m.
Le programme refuse une hauteur relative dépassant 0,50 m.
Il refuse aussi une différence de plus de 1 cm entre le centre et la moyenne des points opposés.
Cette règle repère certaines ruptures ; cinq points ne détectent pas tous les trous ou bosses.
Une surface non plane peut donc demander une méthode plus détaillée.

Le mode de secours conserve le calcul précédent pour sol presque horizontal.
Il ne garantit pas le contact sur une forte pente.
Le mode et le drapeau `terrain-valid` permettent de reconnaître cette limite.
Les dernières valeurs de pente restent visibles ; les ignorer lorsque ce drapeau vaut zéro.

La mise à jour est demandée toutes les 0,05 seconde, avec cinq sondes seulement au contact.
La fréquence réelle dépend du simulateur ; aucun gain de performance n’est annoncé.
Le programme déplace uniquement la roue vers le haut.
Il ne modifie ni les forces, ni les masses, ni la forme du caoutchouc.
Les falaises, les grands trous, les rebonds et les atterrissages restent hors de cette validation.
Les roues d’aile et la hauteur constructeur restent ouvertes au ROADMAP.

## Sources techniques

La mesure utilise les fonctions natives de FlightGear 2024.1.
`aircraftToCart` convertit les coordonnées avant/droite/bas vers le repère terrestre.
`get_cart_ground_intersection` renvoie le point rencontré dans le décor.
Consulter les fonctions correspondantes dans le [code officiel NasalPositioned.cxx, branche 2024.1](https://github.com/FlightGear/flightgear/blob/release/2024.1/src/Scripting/NasalPositioned.cxx).

Le chargement des objets suit le [format officiel des scènes STG](https://github.com/FGDATA/fgdata/blob/master/Docs/README.scenery), section `OBJECT_STATIC`.
Les rampes et leurs dimensions sont des données d’essai du projet.
Le manuel constructeur n’impose ni ces pentes ni une course de suspension visuelle.

## Documentation

La relecture vérifie le public, le but, les prérequis, les actions et les résultats attendus.
Les images ont un texte alternatif et une légende ; les limites restent proches des résultats.
La recette Nasal est synchronisée avec l’atelier 32 ; l’atelier 33 donne les commandes du banc.
L’essai avec un lecteur débutant et l’audit de la page publiée restent non testés.
Aucune conformité globale WCAG ou CAN-ASC n’est déclarée.

## Contrôles du dépôt

Les 86 tests locaux passent. Le contrôle de style ne signale aucune erreur.
La reconstruction depuis les blocs du tutoriel reproduit les fichiers de l’appareil.

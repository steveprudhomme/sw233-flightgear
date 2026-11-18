# Stations du manuel — exemple 369

Pour les personnes qui vérifient les dimensions du modèle.
Source initiale : image de la page « SCHWEIZER 2-33 & 2-33A PARTS AND MAINTENANCE », fournie par le mainteneur.
Le formulaire illustré porte la date du 27 février 1975. Retrouvé dans le manuel complet : page PDF 20, page imprimée A12.
Original local : `docs/references/originaux/details-lot-02/manuel-masse-centrage-exemple-369.png`.

Une **station** est une distance depuis un repère commun. Ce n’est pas forcément une distance depuis le bout du nez.

| Repère lisible | Station, en pouces |
|---|---:|
| Bord d’attaque de l’aile à la racine | 66,34 |
| Centre de gravité du pilote avant | 43,80 |
| Centre de gravité du pilote arrière | 74,70 |
| Roue principale | 88,75 |
| Roue arrière | 285,0 |

Les deux pilotes sont séparés de 30,90 pouces entre leurs repères de centre de gravité, soit 0,78486 m.
Le repère avant est à 0,572516 m devant le bord d’attaque ; celui de l’arrière à 0,212344 m derrière.
Ces repères ne donnent pas directement la position des dossiers ni leurs dimensions.
Confirmer la position de Sta.0 avant de les reporter dans le modèle, dont l’origine est au nez.

Les masses 612, 170 et 150 livres appartiennent à un calcul d’exemple. Elles ne décrivent pas automatiquement C-FYLP.
Le dessin montre un dos arrière droit. Il permet de confirmer la forme générale, mais pas de mesurer une hauteur exacte sur cette petite image.
Cette page ne suffit pas à identifier le tableau plastifié photographié dans le cockpit : VIS-50c reste ouvert.

Empreinte SHA-256 : 1b911b8318ae18f75438ff8c19f9d2c97a9be936e1e73b23f1b0924828629058


## Manuel complet et dimensions de construction

Le manuel fourni compte 392 pages numérisées. Son titre est *Schweizer SGS 2-33 and 2-33A Parts & Maintenance Manual*, formulaire F-122.
La copie contient des pages révisées à plusieurs dates. Ne pas lui attribuer une seule date d’édition non vérifiée.
Fichier local : `originaux/SGS_233_Parts_and_Maintenance_Manua_A16CC38DA4B67.pdf`.
SHA-256 : `74161efcfebc3b5d744f3e0503677f157382a51141d3d7c63096ac6d18835b14`.

La page PDF 9, imprimée A2, donne les dimensions suivantes.
Un pouce vaut 0,0254 m. Un pied vaut 0,3048 m.

| Dimension | Valeur du manuel | Conversion | Modèle après correction | Décision |
|---|---:|---:|---:|---|
| Envergure principale | 51 pieds | 15,5448 m | 15,5448 m | Conserver |
| Longueur totale | 25 pieds et 9 pouces | 7,8486 m | 7,8486 m, nez à dérive | Conserver |
| Envergure du stabilisateur horizontal | 93 pouces | 2,3622 m | 2,3622 m | Réduire la largeur précédente de 3,86 m |
| Corde maximale | 60 pouces | 1,524 m | 1,524 m | Remplacer 1,57 m ; ajuster le raccord central |
| Hauteur totale | 9 pieds et 3,5 pouces | 2,8321 m | Non recalée | Vérifier l’assiette, le sol et les points extrêmes avant modification |

La **corde** est la distance entre les bords avant et arrière d’une aile.
Les contours et épaisseurs de l’empennage restent estimés : sa largeur vérifiée ne valide pas toute sa forme.
Le bord avant du modèle reste à x = 1,99 m. Sa position depuis le nez n’est pas confirmée par ces cotes.
Le nouveau bord arrière à la racine est donc x = 3,514 m, valeur calculée dans ce repère de maquette.

Les stations de centrage sont confirmées aux pages PDF 19 et 20, imprimées A11 et A12.
Elles recoupent les références déjà recensées dans [le dossier dimensionnel](dimensions-cockpit.md).
Aucune nouvelle position de dossier ou de verrière n’en est déduite.
La hauteur totale, les stations du train et les cotes détaillées de verrière restent à rapprocher d’un repère géométrique établi.
Les pages consultées ne suffisent toujours pas à identifier le tableau plastifié du cockpit.


Suite : [DIM-51 — distances du train, assiette et hauteur](dimensions-lot51.md). Les roues visuelles sont recalées sur les différences de stations de cet exemple ; l’origine absolue reste non confirmée.

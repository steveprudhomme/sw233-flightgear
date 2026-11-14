# 14. Fermer correctement les flancs du cockpit

Lot VIS-01a, commencé le 13 novembre et vérifié le 14 novembre 2026. Le plan a été commité avant les modifications : `1647ac1`. Notre but est de réparer l’enveloppe visible, puis de montrer chaque pièce construite. Ce n’est pas encore un cockpit photographique ni une reconstruction cotée par le constructeur.

## 1. Voir le défaut avant de le réparer

Imagine une boîte dont on retire le couvercle pour voir dedans. Si on coupe aussi les côtés, la boîte devient un plateau. C’est ce qui arrivait à notre fuselage : l’exporteur supprimait des faces dont le centre se trouvait entre x=0,66 et 2,48 m, au-dessus de z=−0,13 m. Cette condition supprimait des côtés autant que le dessus. Le verre transparent rendait le trou encore plus visible.

Le fichier AC utilisait déjà SURF 0x30 sur les faces. Nous n’avons donc pas simplement activé une option pour voir l’autre côté d’une face : il fallait reconstruire les faces absentes. La comparaison suivante montre le même réglage de caméra avant et après.

![Avant : les sièges et les commandes dépassent du flanc trop bas](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/avant-profil-gauche.jpg)

![Après : flanc continu jusqu’au bas des vitres](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-profil-gauche.jpg)

L’éclairage est conservé pour comparer les silhouettes ; ce côté et le dessous de l’aile restent sombres. Les photos sont des captures natives, sans repeindre la carlingue après coup.

## 2. Lire les références sans leur demander une précision inexistante

Ouvre les fichiers du [registre des références](../references/inventaire.md), conservés localement dans docs/references/originaux. Les photos et les plans tiers ne sont pas replacés sous GPL ni intégrés aux textures.

| Référence examinée | Observation utilisable | Limite |
|---|---|---|
| Short Kit Fuselage Plans, 800 × 608 | Le contour de profil présente une paroi sous les fenêtres, une séparation inclinée du pare-brise et une partie arrière sous l’aile | Plan de maquette photographié en perspective : pas de cote constructeur du cockpit |
| Trois-vues couleur, 960 × 743 | Le flanc jaune monte jusqu’au bord inférieur du vitrage ; les encadrements et le raccord arrière sont opaques | Dessin illustratif : épaisseurs et positions exactes inconnues |
| Photo C-FYLP, 690 × 517 | Bordure jaune autour du pare-brise, flancs enveloppants, planche devant le pilote | Perspective et dimension physique de référence inconnue |
| Photo N2930H | Porte et paroi latérale identifiables | Autre appareil : ne pas reprendre son tableau pour remplacer celui de C-FYLP |

**Exercice de pointage.** Sur la vue de profil du trois-vues couleur, repère approximativement le nez vers la colonne 214 et l’extrémité arrière vers 697 : environ 483 pixels. En utilisant la longueur publiée 7,8486 m de la fiche 1, l’échelle indicative serait 7,8486 / 483 ≈ 0,01625 m/pixel. Repère le bas du vitrage vers la ligne 219 et le ventre vers 274 : environ 55 pixels, soit 0,894 m. Ce calcul est un contrôle grossier du dessin, pas une cote à recopier dans la géométrie : les points ne sont pas tous à la même station et le trait a une épaisseur.

Nous n’avons pas recalé tout le fuselage avec ce seul rapport. Nous conservons les positions existantes du cockpit pour éviter de déplacer les instruments sans référence suffisante, et supprimons d’abord l’erreur certaine : l’absence des faces latérales. La finesse de la silhouette et les dimensions exactes restent à améliorer par des mesures supplémentaires.

## 3. Construire la coque en U

Dans la [fiche 2, partie C](02-maillage.md#c--construis-une-coque-ouverte-seulement-vers-le-haut), remplace l’ancienne coque et la règle de suppression par la nouvelle recette complète. Ne colle pas une deuxième coque par-dessus la première.

Chaque section comporte neuf points : un bord supérieur gauche, sept points autour du ventre, puis le bord supérieur droit. Relie seulement les voisins successifs de deux sections. Ne relie pas automatiquement le dernier au premier : cette bande serait le couvercle qui cacherait le cockpit.

À la station x=1,55 m :

- Le ventre a une demi-largeur de 0,465 m, soit 0,93 m de largeur.
- Son centre est à z=−0,27 m ; sa profondeur inférieure vaut 0,35 m : le bas est donc à −0,62 m.
- Les bords de l’ouverture sont à y=±0,43 m et z=0,09 m.
- La hauteur du bord au-dessus du ventre vaut 0,09 − (−0,62) = 0,71 m.

Ces nombres sont des **hypothèses de construction H**, pas des mesures d’un SGS 2-33 réel. Les calculs expliquent exactement ce que la recette dessine.

![Coque isolée, trois projections](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/groupe-coque.png)

Le pont supérieur existe seulement avant x=0,50 et après x=3,16 m. Le nez et la queue sont fermés aux extrémités. Le cockpit reste creux, ses côtés restent présents. L’exporteur écrit désormais toutes les faces préparées ; il ne décide plus lesquelles enlever d’après leur centre.

## 4. Faire coïncider les bords de verre et de métal

Dans la partie D, les six stations du vitrage reprennent les mêmes positions de bord :

| x, depuis le nez (m) | Demi-largeur au bord (m) | Hauteur du bord z (m) | Hauteur du demi-anneau vitré (m) |
|---|---|---|---|
| 0,50 | 0,240 | 0,05 | 0,03 |
| 0,91 | 0,397 | 0,07 | 0,28 |
| 1,55 | 0,430 | 0,09 | 0,52 |
| 2,13 | 0,440 | 0,10 | 0,60 |
| 2,78 | 0,390 | 0,10 | 0,47 |
| 3,16 | 0,340 | 0,10 | 0,14 |

Par exemple, au premier bord droit de la station 1,55 m, la coque et le verre possèdent tous deux le point (1,55 ; 0,43 ; 0,09). Ils se touchent exactement dans le fichier, sans cacher un vide avec une baguette.

Les baguettes jaunes longitudinales ont un rayon choisi de 18 mm. Les arceaux ont un rayon de 16 mm. Leur épaisseur est une approximation visuelle ; elle n’est pas une cote de tube structurel. Le raccord arrière opaque occupe les facettes supérieures entre les stations 2,13 et 3,16 m. Une fermeture termine le vitrage à l’avant et l’arrière.

![Verrière, bordures et raccord arrière séparés de la coque](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/groupe-verriere.png)

Une première variante avait retiré l’arceau à x=0,91 m. L’examen du cockpit a montré qu’il fallait garder le contour devant la planche ; il a été rétabli en jaune. C’est la variante finale illustrée ci-dessous. Les cadres sont encore polygonaux, et porte/verrière restent fixes.

## 5. Vérifier de l’intérieur et de l’autre côté

![Avant : cadre sombre et côtés manquants](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/avant-cockpit.jpg)

![Après : cadre jaune et parois latérales, instruments visibles](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-cockpit.jpg)

![Autre flanc après correction](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-profil-droit.jpg)

![Vue de trois quarts après correction](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-trois-quarts.jpg)

![Vue du dessus après correction](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-dessus.jpg)

Les aiguilles, la poignée et le Pitot ne sont pas déplacés pour dissimuler une obstruction. L’aile cache naturellement une partie du raccord arrière dans certaines vues. Les montants de la verrière se voient mieux lorsque la caméra change de côté. Ce contrôle ne prouve pas que l’ergonomie ou le champ visuel sont conformes au véritable planeur.

## 6. Refaire les captures

Fabrique deux paquets distincts si tu veux comparer deux versions. La version précédente publiée est selecteur-15 ; garde-la dans un dossier séparé. Lance chaque paquet avec les réglages de la fiche 12 : CYJN, cap 010°, 5 000 ft, scène du 21 juin 2026 à 16:45 UTC, fenêtre 1280 × 720. Donne un port HTTP distinct à chaque session de test.

Depuis la racine du dépôt, le script suivant choisit les cinq vues, photographie puis rétablit les réglages de caméra :

```powershell
python -m tools.enclosure_bench notes/apres --port 18104
```

Le dossier de sortie doit être neuf. La fenêtre FlightGear doit être visible : une fenêtre minimisée nous a renvoyé un JPEG minuscule. Le script refuse désormais ces images au lieu de les publier. Il laisse la simulation en pause pour éviter que l’avion poursuive son vol sans pilote pendant la comparaison.

Les réglages sont dans VIEWS du script : profils 90°/270°, tangage 0°, champ 25° ; trois quarts 140°/15°/25° ; dessus 180°/80°/45° ; cockpit 0°/−18°/80°. La vue externe est la vue 1, la place avant la vue 0. Le fichier capture.json note la copie chargée et les réglages. Il s’agit d’un cadrage du cockpit, donc la queue ou les bouts d’ailes sont parfois hors champ.

## 7. Vérifier ce que l’œil ne suffit pas à prouver

Deux tests sont ajoutés dans tests/test_enclosure.py :

1. Compter les arêtes de l’ensemble fuselage + vitres + raccord arrière. Chaque arête doit appartenir à deux faces : une seule signalerait une ouverture accidentelle. Cette propriété ne prouve pas à elle seule l’absence de toutes les intersections ni la conformité à l’avion réel.
2. Vérifier que les noms des pièces animées existent toujours et qu’aucune face opaque de coque ne traverse les deux bords supérieurs de la cabine.

Les **23 tests** passent, ainsi que le contrôle des sources, le contrôle de style et la reconstruction des fichiers de l’avion depuis les blocs du tutoriel. Le fichier du FDM et les animations restent inchangés.

Dans FlightGear, un premier essai des aérofreins renvoyait 0 puis 0 : l’horloge de la séance photo était encore gelée. Après reprise de l’horloge et de la simulation, la valeur effective a suivi 1 puis 0. Nous avons ensuite rétabli la pause et la commande rentrée. Le relevé commandes.json conserve les deux tentatives. Ce court essai confirme la réponse de commande ; ce n’est pas une nouvelle validation de la polaire.

## 8. Utiliser les images pour apprendre chaque pièce

Les premières fiches ont maintenant des images près des explications : ensemble pour les mesures, coque, vitrage, ailes, queue, train, commandes, instruments et Pitot. Les fiches 3 et 4 expliquent visuellement les rôles et les liens des fichiers. La fiche 5 illustre le contenu des listes.

L’[atlas des pièces](atlas-pieces.md) complète ces assemblages : **43 objets × 3 projections = 129 vues**. Chaque pièce a son nom exact et ses dimensions, y compris aiguilles, boutons, cadre et rose du compas. Un objet peut contenir plusieurs faces, comme les deux sièges ou les marques du tambour. L’atlas ne prétend pas représenter toutes les pièces mécaniques du véritable appareil, seulement toutes celles actuellement construites dans le maillage.

```powershell
python -m tools.parts_atlas build/atlas-personnel
```

Ouvre index.html dans le dossier produit pour parcourir toutes les pièces hors connexion. Les dessins sont produits à partir des coordonnées, sans IA générative ni modification des captures du simulateur. Ils ne montrent pas les textures du tableau ; la capture cockpit montre leur rendu réel.

## 9. Actualiser la carte de l’avion

La description FlightGear annonce maintenant l’enveloppe raccordée et les cadres jaunes. Le nouvel aperçu montre la géométrie corrigée. Pour fabriquer le paquet illustré :

```powershell
python tools/package.py --output build/planeur-enveloppe --preview notes/apercu/exterior.jpg
```

La [fiche 13](13-selecteur.md) explique comment obtenir ce JPEG natif et la miniature. La publication enveloppe-16 contient le nouveau paquet, les captures, l’atlas hors connexion et les empreintes. Les images de publications précédentes restent des preuves historiques de leur version ; elles ne sont pas remplacées silencieusement.

## 10. Ce qui reste à améliorer

La réparation ferme une lacune certaine, mais elle ne transforme pas les dimensions H en données constructeur. Restent à relever les sections précises du fuselage, les contours anguleux du vitrage, les montants et la porte d’un appareil identifié. Les formes encore facettées, l’intérieur et les matériaux restent schématiques. La livrée actuelle des Cadets n’est pas encore réalisée.

Notre biais principal est de conserver les positions existantes pour isoler la réparation. Cela réduit les régressions, mais peut conserver des proportions anciennes incorrectes. Les prochaines mesures devront pouvoir remettre ces choix en question. Les références et les captures justifient ici les raccords et la fermeture, pas une affirmation de fidélité photographique.

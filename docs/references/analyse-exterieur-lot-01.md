# Analyse extérieure — dix références, lot 01

Reçues le 17 novembre 2026. **Analyse et planification seulement : aucun maillage, matériau ou FDM modifié.**

## Diagnostic et base de comparaison

Le retour utilisateur est retenu : le lot40 fonctionne techniquement, mais son rendu ne satisfait pas l'objectif de fidélité visuelle. Les tests de chargement, les UV corrects et la disparition du scintillement ne constituent pas une validation artistique. Comparaison avec les captures natives publiées au lot40, notamment `livery-left.jpg`, `spoilers-open.jpg` et `release-cockpit.jpg`, et les dix images fournies dans ce message.

![État du modèle avant la reprise](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/spoilers-open.jpg)

Trois problèmes distincts doivent être traités :

1. **Forme :** silhouette anguleuse, nez et verrière trop facettés, ailes et détails simplifiés. Ajouter un effet de verre ne change pas le contour d'une verrière.
2. **Éclairage de la surface :** les normales et les ruptures de lissage peuvent faire apparaître des pans plats. Lisser les normales adoucit l'éclairage mais ne corrige pas une silhouette polygonale.
3. **Image affichée :** crénelage des arêtes et scintillement à mesurer séparément. L'anticrénelage adoucit les marches de pixels ; il ne rend pas un nez géométriquement rond et ne corrige pas une peinture incorrecte.

Le diagnostic précis des normales et du mode d'anticrénelage reste à mesurer. Aucune option FlightGear non vérifiée ni niveau de performance n'est promis ici.

## Conservation et traçabilité

Dix copies intégrales et non retouchées sont conservées dans `docs/references/originaux/exterieur-lot-01/`. Ouvrir son `index.html` pour consulter la galerie locale, dans l'ordre EXT-01 à EXT-10. Le [manifeste](exterieur-lot-01.json) enregistre noms originaux, dimensions et SHA-256 ; les dix copies ont été comparées aux fichiers reçus.

Conformément à la structure documentaire existante, `originaux/` reste local et exclu de Git. Le manifeste et cette analyse sont versionnés. Les auteurs, dates de prise de vue, URL d'origine et autorisations de redistribution ne sont pas établis par les seuls noms de fichiers ; les images ne sont pas placées sous GPL. La galerie locale n'est pas annoncée comme disponible sur GitHub. Le dessin trois-vues est gardé dans ce nouveau lot sans écraser l'exemplaire antérieur, dont la résolution peut différer.

## Lecture image par image

| ID | Nature et ce qui est visible | Utilité pour la reprise | Limite |
|---|---|---|---|
| EXT-01 | Photo arrière, ailes inclinées au sol, haubans, empennages vus en perspective et extrémités d'ailes | Implantation des haubans, allure de l'aile, volumes arrière et équipements d'extrémité | Inclinaison et perspective empêchent de déduire directement le dièdre ; immatriculation non lisible |
| EXT-02 | Photo latérale rapprochée, nez arrondi, ventre à pans, porte, patin, roue, cadres bleus, bande et texte AIR CADETS de L’AIR, MANITOBA et emblème | Référence forte pour transitions courbes/arêtes, découpe de porte et décoration visible | Appareil partiellement cadré, immatriculation incomplète ; aucune attribution à C-FYLP |
| EXT-03 | Photo oblique rapprochée, courbure du pare-brise, bandeaux bleus et fixations, raccord aile/verrière, petites poignées rouges, mât avant à branches et ficelle | Sections de verrière, épaisseur des cadres, détails et reflets ; localisation des petites pièces | Même aspect qu'EXT-02 mais identité/date commune non prouvée ; fonction de chaque branche du mât à confirmer |
| EXT-04 | Photo latérale : C-GCLX lisible, numéro 8 et drapeau sur la dérive, motif bleu en éclair, texte bilingue, roulette sous l'extrémité d'aile | Référence de livrée pour cet appareil, silhouette latérale, aile et train | Ne pas copier le 8 ou C-GCLX sur C-FYLP ; partie avant masquée et perspective |
| EXT-05 | Photo en vol rapprochée, nez/verrière, bande bleue, emblème, roue sortie, patin et câble | Comparer forme avant, implantation roue/patin et fermeture du cockpit | 640 × 357 pixels, identité/date non établies ; détails fins non mesurables |
| EXT-06 | Petite photo en vol, inscription latérale anglophone et bandes d'aile | Documenter une variante de peinture et l'allure générale | 350 × 280 pixels ; ne pas lui attribuer une date ni relever des dimensions précises |
| EXT-07 | Illustration artistique de deux planeurs, immatriculations et inscriptions dessinées | Ambiance et piste pour chercher des photos de ces décorations | Ce n'est pas une photo ; ni géométrie, ni transparence, ni couleur exacte à étalonner dessus |
| EXT-08 | Photo d'un appareil suspendu en intérieur, numéro 95, motif d'oiseau rouge, haubans et ventre visibles | Formes et construction visibles depuis le dessous | Autre décoration ; éclairage intérieur coloré, configuration de présentation différente |
| EXT-09 | Photo d'une aile levée : intrados, bande bleue, grandes lettres, aileron, roulette et reliefs visibles ; flanc marqué MANITOBA et texte anglophone | Découpage aileron, implantation roulette et marquages d'intrados | Ne pas transcrire une immatriculation partiellement masquée ; pas une preuve de la livrée actuelle de C-FYLP |
| EXT-10 | Dessin trois-vues, aile effilée, empennage arrondi, haubans et spoilers représentés | Guide de proportions et liste des pièces à contrôler par plusieurs vues | Illustration sans chaîne de cotes vérifiée ; pas un plan constructeur ni une source de profil aérodynamique |

## Écarts à corriger, par partie

### Fuselage, nez et fermeture du cockpit

Le nez réel montre une courbure continue au sommet et à l'avant (EXT-02/03/05), alors que le modèle expose de grands pans. Le ventre réel présente aussi des arêtes longitudinales : **ne pas arrondir toute la coque par une subdivision uniforme**. Relever séparément la ligne supérieure, le contour du nez, la cassure des flancs et la ligne du patin. Raccorder la porte, le seuil, le nez et la zone arrière sous l'aile. Comparer les deux côtés, pas seulement le côté le mieux photographié.

### Verrière et cadres

Reconstituer des sections courbes cohérentes, particulièrement le bombé du pare-brise et le raccord supérieur. Distinguer vitrage, cadre, joints, charnières et fixation. Les cadres bleus visibles sur EXT-02/03 ne sont pas le contour jaune générique actuel. La transparence doit conserver les visages et les instruments visibles. Les reflets observés sont un objectif d'aspect ; une texture de ciel statique ne reproduit pas le paysage réel.

### Ailes, gouvernes, haubans et empennages

Revoir le volume du bord d'attaque, l'épaisseur du profil visuel, le raccord d'emplanture, l'effilement et le saumon. Les photos ne déterminent pas à elles seules le profil aérodynamique : toute forme approchée doit être signalée. Séparer les ailerons, leurs jeux, charnières et limites ; vérifier les spoilers en volume, leurs découpes et leur logement. Préserver les axes et signes des animations. Arrondir les contours d'empennage visibles dans plusieurs références, garder les ruptures de gouvernes. Détailler les haubans, attaches et transitions, sans en inventer les cotes.

### Train, petits équipements et cockpit

Revoir pneu, jante, dégagement de roue, patin et supports, roulette arrière et roulettes d'extrémité d'aile. Inventorier séparément crochets/câbles de remorquage, poignées et mât avant ; confirmer Pitot, prises et support de ficelle par les références techniques avant de fusionner leurs fonctions. Le cockpit sera revu depuis l'extérieur : ouverture réelle, sièges, profondeur du tableau, silhouettes et visibilité à travers la verrière. Ces images ne suffisent pas à redessiner tous les instruments ou les badges des personnages.

### Livrée et matériaux

Notre bande inférieure sombre et la décoration uniforme des ailes ne reproduisent pas le motif visible sur EXT-02/04. Préparer une carte par surface : jaune dominant, bande fine au nez, éclair latéral, inscriptions, emblème, numéro/drapeau de dérive, bandes et immatriculations d'ailes lorsque attestés. Garder une variante par appareil et époque documentés. Ne pas réunir numéro 8, nom MANITOBA, inscription anglophone et C-FYLP en une livrée prétendument exacte.

Distinguer peinture brillante, vitrage, métal, caoutchouc et revêtement de surface. Les reflets et reliefs visibles peuvent être liés à la construction, à l'usure et à l'éclairage. Les traces d'EXT-02 ne doivent pas devenir une salissure systématique sur tous les avions. Les couleurs des JPEG ne donnent pas des références de peinture calibrées.

## Méthode de relevé et biais

- Identifier la photo et la pièce avant chaque relevé. Reporter les coordonnées en pixels, les extrémités choisies et la résolution originale ; conserver le raisonnement et l'incertitude.
- Commencer par des rapports sans unité, par exemple hauteur de verrière / longueur de nez dans une même vue. Une conversion en mètres exige une dimension fiable et une prise en compte de la perspective.
- Ne pas utiliser une aile inclinée pour déduire directement le dièdre ; ne pas utiliser une illustration pour certifier une épaisseur ou une teinte.
- Les gros plans avant dominent ce lot. L'arrière, le poste arrière, les logements de spoilers et certaines faces d'ailes restent insuffisamment documentés.
- La forme réelle comporte des parties facettées : le biais inverse serait de fabriquer un planeur entièrement lisse et moderne. Le biais de sélection serait de qualifier toutes ces livrées d'actuelles ou d'identiques.

## Acceptation du prochain travail

La priorité devient **formes avant et verrière**, après constitution des vues comparables. Pour chaque famille : référence identifiée, relevé explicite, modification de géométrie, capture native avant/après avec caméra et lumière identiques, retour visuel utilisateur, recette du tutoriel et contrôle des animations. Les tests techniques restent nécessaires mais la ligne « fidélité visuelle acceptée » reste ouverte tant que cette comparaison n'est pas satisfaisante. Aucun nouveau résultat visuel n'est revendiqué par ce dossier de planification.

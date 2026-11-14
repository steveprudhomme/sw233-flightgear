# 15. Donner des contours lisibles aux panneaux de la verrière

Lot VIS-01b, 14 novembre 2026. Le plan a été commité avant modification : `8896e56`. La coque de la fiche 14 est conservée. Cette séance change les surfaces vitrées au-dessus, ajoute des longerons et dessine des contours de porte fixes. Elle ne change ni le calcul du vol ni les instruments.

## 1. Observer avant de dessiner

Reprends le trois-vues couleur 960 × 743 et le plan Short Kit du [registre des références](../references/inventaire.md). Sur le profil du trois-vues, le montant derrière le pare-brise monte en reculant vers la queue. La fenêtre latérale possède des côtés plus droits que notre succession d’anneaux semi-elliptiques. Le plan de maquette montre lui aussi une séparation inclinée et une porte sous le vitrage.

![Avant : sections arrondies et montants verticaux](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-profil-gauche.jpg)

![Après : séparation inclinée et longeron au-dessus du vitrage latéral](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-profil-gauche.jpg)

Les vues gardent les mêmes réglages de caméra. Le côté ombragé aide à lire la silhouette mais ne convient pas à une comparaison de peinture. Le nouveau contour de porte est un trait très fin : l’atlas permet de l’examiner séparément.

## 2. Noter un pointage, puis son incertitude

Dans l’image originale du trois-vues, origine en haut à gauche, relève approximativement le pied du montant vers (332,219) et son sommet vers (339,187). La différence donne environ 7 pixels vers l’arrière pour 32 pixels vers le haut : 7/32 ≈ 0,22. Ce rapport est sans unité. Les traits épais et le dessin illustratif empêchent de le traiter comme une mesure constructeur.

Dans notre maquette, le montant était placé à x=1,55 m et sa hauteur était 0,52 m. Nous gardons ces positions de travail et faisons reculer son sommet de **0,14 m** : rapport 0,14/0,52 ≈ 0,27. Ce choix H suit le sens observé, mais n’est pas égal au rapport pointé. Un ajustement strict du dessin donnerait environ 0,114 m ; nous ne prétendons donc pas avoir ajusté exactement le modèle à ce dessin. Les deux valeurs sont conservées ici pour permettre une future révision fondée sur une photographie mieux mesurable.

| Information | Classe | Utilisation |
|---|---|---|
| Montant incliné vers l’arrière, panneaux latéraux identifiables | V, observation des dessins | Choix de construction |
| Rapport indicatif 7/32 | C à partir d’un pointage V | Contrôle de direction et ordre de grandeur |
| Recul choisi de 0,14 m, largeur et hauteur existantes | H | Géométrie actuelle, à réviser avec des cotes fiables |
| Sections symétriques et contours de porte des deux côtés | H provisoire | Aucun équipement ou accès symétrique réel affirmé |

Les références ne nous donnent pas une cinématique de porte ni des épaisseurs structurelles exactes. Rien de cela n’est inventé dans cette étape.

## 3. Remplacer le demi-cercle par un profil à coins repérés

Ouvre la [fiche 2, partie D](02-maillage.md#d--raccorde-les-vitres-et-les-cadres-jaunes). Le bloc complet y remplace l’ancien : ne garde pas deux verrières superposées.

Chaque station possède toujours neuf points. Le tableau profile donne pour chacun une fraction de la demi-largeur u et une fraction de la hauteur v. Les points extrêmes (1,0) et (−1,0) restent les bords inférieurs. Les autres sont (0,97 ; 0,25), (0,82 ; 0,82), (0,48 ; 0,97) et (0 ; 1), puis leur reflet. Ce sont des choix de forme H : ils distinguent les côtés relativement droits et le toit au lieu de suivre un sinus uniforme.

Pour un point, calcule : y=r×u et z=seuil+h×v. Au montant incliné seulement, calcule x=x_station+0,14×v. Ainsi le pied ne bouge pas et le sommet recule davantage que le milieu. Exemple au sommet : x=1,55+0,14=1,69 m ; z=0,09+0,52=0,61 m. Le bord inférieur reste exactement au point de coque x=1,55 m, y=±0,43 m, z=0,09 m.

![Les panneaux, montants et longerons assemblés](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/groupe-verriere.png)

## 4. Séparer les pièces sans créer de trous

Les surfaces prennent désormais des noms distincts : pare-brise, vitrage-gauche, vitrage-droit, verriere pour la partie supérieure et raccord-arriere pour la partie opaque. Leurs limites utilisent les mêmes sommets. Une séparation d’objets ne signifie pas laisser un espace entre eux.

Chaque quadrilatère est découpé en deux triangles avec une diagonale commune. Cela évite de laisser au lecteur AC3D le choix de dessiner une face dont les quatre coins ne seraient pas dans un seul plan. Le matériau reste transparent pour le verre, jaune opaque pour le raccord arrière.

Les longerons relient les points numérotés 2 et 6 des stations arrière : ils matérialisent la transition entre flanc et toit. Leur rayon choisi vaut 10 mm. Les autres cadres gardent les valeurs de la fiche 14. Ces baguettes n’attestent pas les dimensions d’une structure réelle.

## 5. Dessiner les contours de porte fixes

La coque reste entière. On trace deux lignes latérales entre les stations x=1,55 et 2,78 m, en passant par 2,13 m. Leur bord supérieur rejoint les bordures existantes. Le bas suit le milieu de la première facette inférieure de coque : y=r×(1+cos(30°))/2, z=z_centre−h/4. Nous décalons le trait de 2 mm vers l’extérieur pour limiter le scintillement entre surfaces superposées. Son rayon de dessin est 2,5 mm.

![Les contours sur la coque](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/groupe-portes.png)

Ces objets sont des repères visuels fixes, pas des portes fonctionnelles. Ils ne possèdent ni charnière, ni poignée ajoutée, ni animation. Leur symétrie est une approximation à vérifier sur les deux flancs d’un appareil identifié. L’atlas montre chaque contour isolément ; il ne faut pas confondre ce trait avec une pièce de structure.

## 6. Vérifier la vue pilote

![Avant : cadre arrondi](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-cockpit.jpg)

![Après : contour plus anguleux, cadrans visibles](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-cockpit.jpg)

![Autre côté du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-profil-droit.jpg)

![Vue de trois quarts](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-trois-quarts.jpg)

![Vue du dessus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-dessus.jpg)

La planche, les aiguilles et la caméra pilote sont inchangées. Vérifie les bords des cadrans et la vue vers le Pitot : une face jaune ne doit pas se trouver devant eux. Les captures montrent une géométrie encore facettée ; la comparaison ne démontre pas un champ visuel certifié.

Pour refaire ces vues, suis le lancement de la fiche 12, puis utilise un dossier neuf :

```powershell
python -m tools.enclosure_bench notes/panneaux --port 18105
```

Cette commande suppose une session SW233 de test déjà ouverte avec le serveur HTTP sur le même port. Elle prend les cinq cadrages de la fiche 14. La fenêtre doit rester visible. Elle remet les réglages de caméra puis laisse l’avion en pause.

## 7. Observer chacune des 49 pièces

L’[atlas actualisé](atlas-pieces.md) couvre **49 objets et 147 projections**. Les six objets supplémentaires sont pare-brise, vitrage-gauche, vitrage-droit, longerons-verriere, contour-porte-1 et contour-porte1. La partie supérieure conserve le nom verriere. Chaque objet possède son image et ses dimensions calculées dans le modèle.

Les premières fiches ont reçu les images actualisées des assemblages. Les illustrations historiques des fiches 14 et 13 restent attachées à leurs publications d’origine : elles permettent de comprendre les étapes précédentes au lieu de réécrire leur résultat.

```powershell
python -m tools.parts_atlas build/atlas-panneaux
```

Pour consulter les images sans outil Python, télécharge atlas-pieces.zip dans la publication panneaux-17, extrais-le et ouvre index.html. Les schémas de l’atlas viennent des sommets ; ce ne sont pas des captures FlightGear. Les dimensions sont celles du modèle, pas des cotes constructeur.

## 8. Contrôles et livraison

Les **24 tests** passent. Le contrôle d’enveloppe compte désormais les trois nouveaux objets vitrés : toutes les arêtes rejoignent deux faces. Le test supplémentaire vérifie que les panneaux ont une aire non nulle et que la limite inclinée atteint la position attendue. Il vérifie une construction, pas la fidélité aéronautique de cette position. La reconstruction depuis les blocs du tutoriel et le contrôle de style passent aussi.

Les images et la description du nouveau paquet FlightGear sont actualisées. La miniature utilise le nouvel aperçu natif. Le FDM et le fichier d’animations ne sont pas modifiés ; les commandes n’acquièrent pas de nouvelles fonctions.

Difficulté pratique rencontrée : le disque C: était presque plein. Les fichiers générés du lot ont été écrits sur D:/SW233-work/panneaux-17 sans déplacer ni supprimer les documents du projet. Tu peux choisir un autre disque avec de la place pour les options output des outils ; ce chemin n’est pas obligatoire.

## 9. Ce qui reste incertain

Nous nous appuyons sur les plans et photos fournis, sur les raccords calculés et sur les captures natives. Le principal biais est de garder les stations existantes : cela facilite la comparaison, mais ne corrige pas toutes les proportions. Les contours de porte, l’implantation exacte des montants, la largeur réelle et la courbure du pare-brise demandent encore des références dimensionnées. Une finition photographique ne doit pas être présentée comme réalisée à ce stade.

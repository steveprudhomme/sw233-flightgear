# 17. Trouver une cote fiable avant de reconstruire le cockpit

VIS-01d, 15 novembre 2026. Plan commité avant recherche : `06125ce`. But de cette séance : préparer un dossier qu'une autre personne peut vérifier, même sans IA. Tu n'as pas besoin d'accéder à un vrai planeur pour suivre les premières étapes.

## 1. Préparer ta feuille

Ouvre le [registre des sources](../references/dimensions-cockpit.md) et copie le [formulaire vierge](../references/releve-cockpit.md) dans tes notes. Écris la date. Laisse vide toute mesure inconnue. Un blanc signifie « je ne sais pas » ; zéro signifierait une vraie mesure.

## 2. Vérifier l'édition et l'appareil

Ouvre le manuel fourni dans un lecteur PDF. Va à la page PDF 4 : elle contient deux pages imprimées. Lis la date de révision, 15 février 2022, puis la description des variantes. Note « 2-33A », pas simplement « un Schweizer ». Le 2-33B est allongé : ses dimensions ne peuvent pas compléter les blancs de notre 2-33A.

Pour C-FYLP, ouvre le lien R4 du registre et cherche l'immatriculation à la page PDF 4. Cette source ancienne associe l'appareil au 2-33A. Elle ne donne pas sa configuration actuelle. Écris donc « variante historiquement attestée ; configuration photographiée à confirmer ». Consulte ensuite R5 : la pièce de verrière dépend du numéro de série ou d'une conversion. L'immatriculation seule ne suffit plus.

## 3. Lire et convertir une vraie cote

Dans la description, relève séparément 25 pieds et 9 pouces. Fais les deux multiplications : 25 × 0,3048 = 7,62 m ; 9 × 0,0254 = 0,2286 m. Additionne : **7,8486 m**. Garde aussi la valeur d'origine dans ta feuille pour permettre la vérification.

Ne recopie pas cette longueur dans la case « longueur de verrière » : elle concerne le fuselage entier. Une bonne mesure dans la mauvaise case devient une erreur.

## 4. Ne pas confondre les règles

Va à la page PDF 14, pages imprimées 26–27. Repère le datum, situé 66,34 pouces devant le bord d'attaque à l'emplanture. C'est le zéro de la règle de masse. Notre dessin utilise le nez comme zéro. Sans distance connue entre ces deux zéros, on ne peut pas les superposer.

Les stations 43,80 et 74,70 pouces concernent les bras de masse des occupants. Elles ne disent pas où placer les yeux du pilote ou le centre d'un siège. Classe-les « centrage », pas « forme du cockpit ».

## 5. Donner un nom à chaque point

![Schéma original des points à relever et de la largeur de section](https://github.com/steveprudhomme/sw233-flightgear/releases/download/references-19/releve-cockpit.png)

[Version SVG éditable](../illustrations/releve-cockpit.svg). Le dessin explique la méthode ; il n'est pas une nouvelle référence géométrique. N est le nez sans Pitot. A marque le début inférieur du vitrage ; B et C identifient les deux extrémités de la zone de pare-brise choisie ; D marque la fin de l'ouverture étudiée. Si la photographie ne montre pas ces limites, note « non visible ».

Reporte les lettres sur une copie de ta photo, jamais sur l'original. Mesure une distance projetée sur l'axe annoncé, pas le trajet d'un ruban suivant la courbure. Pour la largeur W, écris d'abord où se trouve la section S : une largeur sans position n'identifie pas la section à construire.

## 6. Comparer avec ce que nous avons réellement construit

![Modèle actuel dans FlightGear, profil gauche, capture panneaux-17 réutilisée](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-profil-gauche.jpg)

![Vue pilote actuelle, capture panneaux-17 réutilisée](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-cockpit.jpg)

Ces images sont les témoins du lot précédent, pas de nouveaux essais. Ouvre aussi l'[atlas de chaque pièce](atlas-pieces.md). Cherche le vitrage, les cadres et les contours de porte. Compare leur fonction au registre : une limite entre deux objets 3D ne prouve pas un joint sur le vrai vitrage. Le manuel décrit une verrière d'une pièce. Les cadres visibles restent donc à vérifier individuellement.

## 7. Préparer les mesures manquantes

Dans le formulaire, demande deux vues de profil, une de chaque côté, de la même configuration. Pour chaque mesure, conserve photo, unité, origine, instrument et marge d'incertitude. Demande au minimum deux dimensions indépendantes dans le même plan pour contrôler l'échelle. Une seule longueur peut masquer une perspective fausse ; deux cotes ne suppriment pas automatiquement cette perspective.

Un adulte autorisé recueillera les mesures sur l'appareil. Tu peux préparer les lettres et compléter les documents toi-même. Aucun contact n'a été envoyé pendant cette séance.

## 8. Décider et s'arrêter au bon endroit

Le dossier apporte une identification historique et des règles pour éviter de mélanger les variantes. Il ne donne toujours pas les cotes réelles du pare-brise et des sections de C-FYLP. **Nous ne déplaçons donc aucune pièce dans cette séance.** La fiche 16 conserve ses résultats ; ils ne deviennent pas des dimensions constructeur.

Point d'arrêt : tu dois pouvoir expliquer d'où vient chaque nombre et ce qu'il mesure. Le prochain lot VIS-01e sera accepté quand les relevés permettront une décision pièce par pièce. Ensuite seulement, modifier la recette de maillage, reconstruire, comparer les captures natives au même cadrage, puis actualiser les aperçus FlightGear.

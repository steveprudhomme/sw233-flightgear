# Feuille de route

Objectif : reconnaître en vue extérieure un Schweizer SGS 2-33A des Cadets et, en place avant, retrouver les instruments du même appareil. La variante, l’immatriculation et la date comptent : deux photos de 2-33 ne prouvent pas que leurs tableaux de bord sont identiques.

| Étape | État | Comment saurons-nous qu’elle est terminée ? |
| --- | --- | --- |
| Voler à CYJN | Démontré | Capture native de FlightGear avec le terrain chargé, les deux cycles d’aérofreins et un virage en glissade vu de deux points de vue. |
| Habiller le tableau avant | Deuxième passe réalisée | Le film montre le grain de la tôle, les cerclages, les vis et la bouche d’aération inspirés de la photo C-FYLP. Les trois cadrans restent animés. Les quatre plaquettes, la façade radio et la boule de largage complètent maintenant la place avant ; la radio et le largage ne sont pas opérationnels. |
| Livrée actuelle des Cadets de l’aviation royale du Canada | À documenter, puis à peindre | Comparaison avec des vues datées des deux flancs, du dessus et du dessous **d’un même planeur identifié** ; immatriculation, motifs, inscriptions et orientation lisibles aux bons endroits. |
| Cockpit photographique | Priorité suivante | Comparaison côte à côte dans le même cadrage : contours de la planche, typographie, unités, reflets du verre et profondeur des instruments. Aucun reflet ne doit cacher une aiguille, de face ou en vue oblique. |
| Valider le comportement | À mesurer | Polaire à plusieurs vitesses et masses, effets des aérofreins, contrôle du signe de la ficelle en glissade gauche et droite ; publier les écarts aux références. |
| Atelier pour débutants | Première édition | Un débutant sur une installation neuve arrive au film final et sait où retrouver son projet ; consigner les étapes où il a eu besoin d’aide. |

## Lot livrée : de la photo au planeur

1. Choisir avec un contributeur un exemplaire en service et une date de référence. La [documentation officielle de l’ARC](https://www.canada.ca/fr/force-aerienne/programmes/securite-vols/enquete.html) aide à identifier les appareils ; elle ne fixe pas à elle seule une livrée actuelle.
2. Dans l’inventaire, noter auteur, date, côté visible, provenance et permission pour chaque image. Demander des vues manquantes plutôt que reproduire un logo ou un motif par symétrie supposée.
3. Déplier le fuselage, les ailes et la dérive sur un patron à plat. Garder séparés peinture de fond, bandes, immatriculation et marques. Préférer un dessin original éditable ; n’incorporer des emblèmes tiers que si les droits sont établis.
4. Vérifier le sens des lettres sur les deux côtés, les raccords et la texture des panneaux d’aérofreins dans les deux positions. Photographier dans le simulateur sous deux éclairages, puis faire relire le résultat. La livrée jaune du film reste une livrée de développement.

## Lot cockpit : priorité au poste avant

Prendre la disposition C-FYLP comme référence de travail, pas le poste différent de N2930H. Relever les diamètres et la position de l’œil avant de changer l’échelle. Reconstruire d’abord les cadrans et leurs unités, puis le compas, la radio et les plaquettes selon l’exemplaire choisi. Une image fixe d’aiguille ne doit jamais remplacer une mesure de FlightGear. Pour une texture tirée d’une photographie, obtenir une image frontale nette et une autorisation de diffusion compatible. Le poste arrière viendra après validation du poste avant.

## Reconstruire depuis une page blanche, puis améliorer le cockpit

[Sept fiches publiées](docs/construction/README.md) ; reconstruction automatique en CI. Prochaine validation pédagogique : observer un premier lecteur refaire une mesure et assembler son avion sans assistance.

1. Écrire une aide à la tâche pour un lecteur de 10 ans : préparer un dossier vide, mesurer les références, noter page, unité, calcul et incertitude ; séparer les choix de maquette des mesures publiées.
2. Enseigner la fabrication complète du maillage AC3D, de la fiche FlightGear, des animations, des check-lists et de la peinture Python. Pour chaque opération : action, raison, résultat attendu et dépannage. Relier le modèle de vol, le décor, les essais, la vidéo et la publication à ces cinq fichiers.
3. Vérifier la reconstruction indépendamment des fichiers finaux ; ensuite poursuivre le poste C-FYLP avec un détail identifiable sur la photo et contrôler le résultat dans le cockpit.

## Ce que trois autres constructions nous apprennent

Notre atelier sait reproduire les fichiers. Cela répond à « deux personnes construisent-elles la même maquette ? ». Il reste deux questions : « le pilote voit-il ce qu’il verrait dans C-FYLP ? » et « à masse et vitesse connues, le modèle descend-il comme un 2-33 ? ». Voici les comparaisons qui motivent les prochains essais.

| Construction consultée | Observation | Décision pour le Schweizer |
| --- | --- | --- |
| [SGS233 historique de JSBSim](https://github.com/JSBSim-Team/jsbsim/blob/master/aircraft/sgs233/sgs233.xml), également étudié dans [l’inventaire FlightGear](docs/sources.md) | C’est le même type de planeur ; les auteurs signalent pourtant des estimations dans le modèle. | S’en servir comme témoin pour repérer un écart de comportement. Pour trancher, revenir à une donnée publiée du 2-33 avec sa variante, sa masse et ses unités. Un accord entre deux simulateurs n’est pas un essai en vol. |
| [ASK 21, développement de MrChillStorm](https://github.com/MrChillStorm/ASK21) | L’auteur distingue les comportements appuyés par le manuel ou des essais de ceux encore estimés, notamment en forte glissade. La ficelle a sa propre animation. | Tester séparément le mouvement visible de notre ficelle et la réponse aérodynamique du planeur. Aucun coefficient ni angle limite de l’ASK 21 ne devient une donnée du Schweizer. |
| [ASK 13, révision 4921 de FGAddon](https://sourceforge.net/p/flightgear/fgaddon/4921/) | Les sources éditables d’instruments sont conservées séparément, dont le fichier de travail de la radio. | Garder nos dessins et leur recette de génération modifiables. Isoler les éléments du tableau au fur et à mesure : déplacer la radio doit être possible sans repeindre l’altimètre ; vérifier ensuite le paquet reconstruit. |

### Dans quel ordre améliorer la maquette ?

- [ ] **1 · Fixer un point de comparaison avant de retoucher la peinture.** Reprendre la [capture actuelle du siège avant](https://github.com/steveprudhomme/sw233-flightgear/releases/download/cockpit-construction-01/SW233-cockpit-CFYLP.jpg). Noter position de l’œil, angle de vue et résolution ; relever sur la photo C-FYLP les centres, diamètres apparents et espaces entre cadrans. Si une largeur réelle manque, conserver les rapports et leur incertitude. Livrable : une feuille de mesures et un cadrage que deux contributeurs peuvent refaire.
- [ ] **2 · Corriger la disposition, puis l’aspect.** Dégager la radio du cerclage de l’altimètre et placer le compas entre les plaquettes inférieures. Comparer deux vues identiques avant/après, puis une vue oblique pour contrôler la profondeur. Ensuite seulement travailler le verre, la typographie et la tôle. Réussite : cadrans sans chevauchement, aiguilles lisibles sous deux éclairages, compas marqué décoratif tant que son indication n’a pas été testée.
- [ ] **3 · Vérifier la silhouette avant la livrée.** Comparer aile, hauban, roue et patin de face, de profil et du dessus. Consigner les différences avec le trois-vues ; une capture en perspective permet de détecter une forme étrange mais pas de certifier une cote. Corriger les écarts confirmés, puis reprendre le lot livrée ci-dessus avec un appareil daté et identifié.
- [ ] **4 · Mesurer le vol indépendamment du rendu.** À CYJN, en air calme, fixer masse, centrage et configuration. Relever à plusieurs vitesses stabilisées la vitesse indiquée et le taux de chute, puis recommencer à une deuxième masse. Refaire un point aérofreins rentrés puis sortis à la même vitesse. Publier conditions, unités, résultats et écarts aux seuls points documentés pour le Schweizer ; garder les autres comme mesures du simulateur.
- [ ] **5 · Distinguer une animation convaincante d’un système vérifié.** Filmer vol symétrique, glissade à gauche, puis à droite : noter commandes croisées, côté de l’aile basse, angle de vent relatif et sens de la ficelle. Vérifier séparément le levier et les deux panneaux d’aérofreins en butée. Pour la poignée de largage, attendre un essai avec câble attaché puis effectivement libéré avant de la déclarer fonctionnelle.
- [ ] **6 · Faire refaire les essais.** Un second contributeur repart du paquet publié, retrouve les cadrages et les états des commandes. Un lecteur débutant suit le tutoriel sans indication orale ; consigner la première étape où il hésite et corriger sa légende avant de clore le lot.

## Illustrer les sept fiches avec des captures natives de FlightGear

But : à chaque point d’arrêt, l’enfant peut répondre à « où dois-je regarder, et qu’est-ce qui me dit que j’ai réussi ? ». La [capture C-FYLP](https://github.com/steveprudhomme/sw233-flightgear/releases/download/cockpit-construction-01/SW233-cockpit-CFYLP.jpg) et le [film à CYJN](https://steveprudhomme.github.io/sw233-flightgear/#film) sont des points de départ ; le parcours illustré reste à produire. Pour les premières fiches, montrer le résultat attendu après assemblage, sans demander un lancement avant que l’avion soit prêt.

| Fiche de l’atelier | Capture à placer juste après l’action | Ce que le lecteur doit retrouver |
| --- | --- | --- |
| 1 · Mesurer | Vue extérieure du dessus, ailes entières, à côté du schéma de mesure | Pointer le changement de pente sur chaque aile ; prendre la cote sur le plan, pas sur la capture. |
| 2 · Maillage | Profil au sol et détail du nez sur fond contrasté | Distinguer la roue du patin, le tube Pitot de la ficelle. |
| 3 · Vol | Planeur stabilisé et valeurs du simulateur au même instant | Lire vitesse, unité et taux de chute ; retrouver la ligne correspondante du relevé d’essai. |
| 4 · Configuration et animations | Poste avant centré ; deux captures du même cadran à deux valeurs connues | Identifier le bon siège et constater que l’aiguille change dans le sens attendu. |
| 5 · Listes | Menu des listes ouvert puis une liste affichée | Retrouver le même titre et le premier item, sans rien actionner sur le planeur. |
| 6 · Peinture | Réutiliser la capture existante, puis ajouter le même cadrage après correction et un gros plan natif | Repérer les quatre cartes, la radio, les aiguilles et le bouton de largage ; distinguer ce qui est peint de ce qui dépasse du tableau. |
| 7 · Vol à CYJN | Terrain reconnaissable ; paires rentré/sorti depuis le siège et au-dessus des ailes ; glissade depuis le siège et de dehors | Suivre le mouvement des deux panneaux, puis associer ficelle et aile basse au même instant du vol. |

**Règle de publication.** Capturer dans FlightGear avec le terrain chargé et la lumière de côté ou de dos. Conserver l’original lisible parmi les pièces de la version ; versionner les légendes et, si utile, une annotation éditable. Indiquer version de FlightGear, révision de l’avion, vue, conditions et, pour un extrait du film, minutage. Donner un texte alternatif et une légende courte (« Regarde… Tu dois voir… ») ; ne pas couvrir le détail par une flèche. La fiche est prête quand le lecteur retrouve ce détail dans son propre simulateur et que l’image s’ouvre depuis le tutoriel publié.

### Séance radio et compas : contrôles avant publication

1. Figer le cadrage témoin : version du paquet, résolution, siège, décalages de caméra, inclinaison et champ de vision. Garder le même scénario à CYJN pour les deux captures natives.
2. Reporter les centres de la photo par rapport à la bouche d’air ; calculer aussi le jeu entre les bords des instruments. Conserver les hypothèses si la perspective ou la largeur inconnue empêche une mesure réelle.
3. Modifier la peinture originale, garder les aiguilles indépendantes et représenter le compas comme décoratif. Comparer deux images au même cadrage : cerclage dégagé, fenêtre du compas visible, textes libres.
4. Insérer les deux images dans la fiche de peinture avec une action que l’enfant peut refaire ; vérifier la reconstruction depuis le livre, puis actualiser README, historique et état de la feuille de route.

**Séance réalisée :** [mesures, recette et captures natives avant/après](docs/construction/06-peinture.md#comparaison-cockpit). Le cadrage de comparaison est fixé, la radio dégagée et le compas décoratif en place. Restent la mesure réelle de la position de l’œil, le contrôle en vue oblique, le verre sous deux éclairages et une indication de cap vérifiée.

### Séance réalisée : du compas peint au boîtier en relief

- Avant de toucher au maillage, assembler la version témoin et la photographier de face et de biais ; déplacer aussi l’œil pour révéler le flanc.
- Conserver le centre et la silhouette de façade. Distinguer ce que montre la photo de C-FYLP des épaisseurs choisies ; dessiner une coupe cotée, un cadre ouvert, une fenêtre en retrait et un trait fixe derrière la vitre. Éviter les surfaces superposées.
- Reprendre les deux vues avec les mêmes réglages puis changer uniquement l’éclairage. Vérifier contour, retrait, lisibilité du trait et dégagement des cartes, sans brancher d’indication de cap.
- Intégrer recette et captures légendées au livre, reconstruire le modèle à partir des fiches et actualiser les liens du projet.

[Recette et six captures natives](docs/construction/06-peinture.md#compas-relief) : de biais on distingue le flanc, les cartes restent dégagées et le trait reste visible de jour et le soir. La profondeur demeure estimée. Prochain essai distinct : indication de cap sur plusieurs orientations connues, puis contrôle au passage du nord.

Pour préparer la bande graduée mobile, voir [l’examen du compas FSX et les photos de cockpits identifiés](docs/references/cockpits-et-fsx.md). Le témoin FSX est une comparaison de fonctionnement, pas une source de cotes du Schweizer.

### Séance indication magnétique

1. Identifier la propriété réellement alimentée dans FlightGear ; distinguer l’orientation vraie, le cap magnétique et la lecture de l’instrument.
2. Construire une rose graduée originale derrière le trait fixe. Contrôler le sens, le centrage et l’occultation des graduations hors fenêtre.
3. Faire un essai visuel à entrée connue aux quatre points cardinaux et à 359°, 000°, 001° ; distinguer cet essai d’affichage de la validation en vol. Conserver des captures, la méthode et les limites dans le tutoriel.

**Affichage réalisé et vérifié dans FlightGear 2024.1.7 :** [essais illustrés et méthode](docs/construction/04-configuration.md#rose-magnetique). La rose suit l’indication magnétique du simulateur. Restent des essais en virage et après stabilisation pour évaluer sa réponse dynamique.

### Essai dynamique du compas à CYJN : protocole avant tournage

- Départ en vol stabilisé vers 330° magnétiques, vent demandé nul, compas en service. Commander les gouvernes, jamais la valeur indiquée. Enregistrer ensemble temps, cap magnétique, indication, roulis et vitesse.
- Virer vers 030° puis revenir vers 330° avec des inclinaisons cibles opposées de même amplitude. Garder un palier ailes à plat entre les virages. Repérer les passages de nord sur les mesures.
- Calculer l’écart signé dans [−180°, 180°[. Pour chaque retour à plat (|roulis| ≤ 3°), chercher le premier intervalle continu de 3 s avec |écart| ≤ 2°. Donner les seuils, le maximum par virage et signaler un critère non atteint.
- Publier film natif, courbes, trois images légendées et données de cette exécution. Séparer les observations du simulateur de toute affirmation sur l’appareil réel.

**Essai réalisé :** [126 s de vol à CYJN, film et relevés](docs/construction/07-essais.md#compas-en-virage). Écart extrême de −43,6° à droite et +43,6° à gauche. Une deuxième inclinaison et des mesures indépendantes seraient nécessaires avant de généraliser.

### Anémomètre C-FYLP : protocole avant modification

1. Garder le cadran initial et une capture témoin à vitesse connue. Identifier sur la photo le pivot, l’axe vertical et les graduations lisibles ; relever les points en pixels, les angles et leur incertitude.
2. Comparer les arcs visibles avec les limites explicitement documentées pour la variante et l’unité. Distinguer limite d’utilisation, marquage photographié et borne non vérifiée ; ne pas compléter un arc par supposition.
3. Tester la conversion nœuds → mph indépendamment de la position des graduations. Si l’échelle photographiée est irrégulière, utiliser la même correspondance par intervalles pour la peinture et la rotation de l’aiguille.
4. Essayer au moins trois vitesses réparties sur le cadran dans FlightGear ; comparer avant/après au même cadrage et à la même vitesse. Publier captures, table de mesures et procédure dans le tutoriel.

**Séance réalisée :** [relevé des angles de C-FYLP](docs/construction/04-configuration.md#anemometre), marquages du manuel §2.3 pour 1 040 lb et [quatre entrées vérifiées dans FlightGear](docs/construction/07-essais.md#banc-anemometre). Restent les erreurs de pression et la comparaison à une photographie parfaitement frontale.

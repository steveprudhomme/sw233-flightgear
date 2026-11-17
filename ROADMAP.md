# Feuille de route — Schweizer SGS 2-33

Mise à jour : **17 novembre 2026**. Les lots définissent du contenu, pas des dates promises.

## Vision et périmètre

Reproduire dans FlightGear un Schweizer SGS 2-33 crédible aux couleurs des Cadets de l’aviation royale du Canada, avec une construction expliquée pas à pas. Les détails attestés, les choix artistiques et les essais doivent rester identifiables.

Prototype de simulation sous GPL-3.0-only, non certifié pour l’instruction réelle. Les ressources tierces gardent leurs droits ; aucune fidélité exacte de géométrie, d’uniforme ou de performances n’est annoncée sans référence.

## État actuel

| Domaine | Réalisé | Limite restante |
|---|---|---|
| Cockpit | Enveloppe, cadres, relief des instruments, calage, COM1 et compas | Reflets de ciel statique sous ALS ; profondeurs estimées ; audio radio non validé |
| Checklists | FR/EN, accents, initiales rouges, souris et format 1024 × 600 | Ctrl+L physiquement confirmé ouvert ; essai fermé encore à préciser |
| Extérieur | Livrée jaune/bleu C-FYLP provisoire, spoilers et ficelle animés | Formes et peinture à reprendre (VIS-05) ; identité/date des nouvelles photos à compléter |
| Occupants | Deux personnages détaillés bleu/vert, noms, harnais et visibilité liée aux masses | Proportions artistiques ; insignes officiels et animations non validés |
| Validation | Essais natifs Windows à CYJN, 59 tests dans le lot visuel, reconstruction du tutoriel | Polaire réelle, Linux et relecture autonome du tutoriel non validés |

Statuts : **en cours** = lot commencé ; **prévu** = travail accepté à réaliser ; **attend une référence** = détail non confirmé ; **terminé** = preuve publiée. Les anciens protocoles sont dans l’[archive du 17 novembre](docs/planification/archive-roadmap-2026-11-17.md), et ne constituent plus une deuxième liste active.

## Priorité actuelle — VIS-05 : reprise de la fidélité visuelle

**Statut : prévu, rendu du lot40 non accepté visuellement par l’utilisateur.** Le lot40 reste une livraison technique ; il ne clôt pas l’objectif de ressemblance. Les dix nouvelles références sont conservées localement et analysées dans le [dossier extérieur lot01](docs/references/analyse-exterieur-lot-01.md), avec [manifeste des originaux](docs/references/exterieur-lot-01.json).

Responsable : mainteneur, avec revue visuelle utilisateur. Ordre : références et comparaison → nez/coque/verrière → ailes et queue → équipements → livrée/matériaux → intégration. Pas de date ferme. Chaque lot doit comporter un plan commité avant modification, un tutoriel illustré et des preuves FlightGear.

| Étape | Sous-étapes et références | Critère de fin |
|---|---|---|
| [x] **VIS-05a — vues de référence** | Classer photos/illustrations, séparer appareils/époques ; identifier les inscriptions ; relever contours et rapports de dimensions, noter perspective et inconnues ; préparer vues natives comparables au lot40 | Fiche de relevé traçable pour chaque pièce, six vues générales et gros plans avant ; aucune cote en mètres inventée |
| [ ] **VIS-05b — nez et coque** | Reconstruire les courbes avant, sections, flancs et ventre ; conserver les arêtes structurelles observées ; corriger raccords de porte et dessous (EXT-02/03/05) | Silhouettes avant/profil/oblique comparées ; courbes continues dans les zones rondes, arêtes conservées où attestées ; aucun trou ni superposition |
| [ ] **VIS-05c — verrière et porte** | Bombé du pare-brise, sections latérales, raccord sous aile, cadres/joints, charnières/poignées et limites de porte (EXT-02/03/05) | Comparaison intérieur/extérieur ; coque et verrière raccordées ; pas d’occultation des instruments ou de traversée des personnages |
| [ ] **VIS-05d — ailes et haubans** | Bord d’attaque, épaisseur visuelle documentée, emplanture, effilement, saumons, section des haubans et attaches (EXT-01/03/04/09/10) | Comparaisons dessus/dessous/face ; profils estimés signalés ; aucune prétention de recalibrage du FDM |
| [ ] **VIS-05e — gouvernes et spoilers** | Délimiter ailerons, profondeur, direction ; ajouter jeux/charnières ; revoir volumes et logements des spoilers avec références complémentaires | Débattements vérifiés dans FlightGear, vues cockpit et extérieures ; axes préservés, pas d’interpénétration ni peau désolidarisée |
| [ ] **VIS-05f — empennages** | Revoir contours arrondis, épaisseur, raccords, attaches et parties mobiles (EXT-01/04/10, photos complémentaires à obtenir) | Silhouettes de queue comparées dans trois vues ; inconnues de dimensions conservées |
| [ ] **VIS-05g — train et accessoires** | Pneu/jante, patin/supports, roulette arrière et roulettes d’ailes ; crochets, mât avant, Pitot et ficelle, poignées et fixations (EXT-02/03/04/05/09) | Inventaire pièce par pièce illustré, fonctions confirmées ; positions et dégagements comparés, aucune cote déduite sans échelle |
| [ ] **VIS-05h — livrée par appareil** | Corriger tracé bleu/éclair, cadres, inscriptions bilingues, emblème, drapeau/numéro, bandes et lettres d’ailes ; établir variantes identifiées ; conserver C-FYLP provisoire tant que sa couverture manque | Carte de placement par surface avec source ; textes dans le bon sens ; aucune combinaison C-GCLX/MANITOBA/C-FYLP non attestée |
| [ ] **VIS-05i — matériaux et détails** | Peinture, métal, revêtement, vitrage, caoutchouc ; reliefs de construction et usure mesurée ; reflets équilibrés, UV et densité de texture homogènes | Captures sous deux éclairages ; détails à l’échelle, instruments lisibles ; provenance des textures et compromis documentés |
| [ ] **VIS-05j — lissage et anticrénelage** | Séparer silhouette, normales et marches de pixels ; vérifier réglages réellement disponibles dans FlightGear ; comparer rendu identique à résolution fixe, puis mouvement ; mesurer coût | Avant/après géométrie et anticrénelage séparés ; arêtes voulues préservées, pas de scintillement observé dans le parcours testé ; limites de cadence explicites |
| [ ] **VIS-05k — cockpit et occupants** | Revoir volumes vus à travers la nouvelle verrière, sièges, tableau, posture, mains, formes du visage et plis des tenues ; compléter références intérieures | Captures avant/arrière/extérieures ; pas de traversées, noms lisibles ; personnages et badges artistiques identifiés |
| [ ] **VIS-05l — validation et tutoriel** | Pour chaque pièce : image de référence locale, relevé expliqué dès 10 ans, recette exacte, planche de pièce et capture native avant/après ; vérifier LOD, animations, performances et paquet ; mettre à jour aperçu, vidéo, MD et GitHub | Tests et reconstruction réussis **et** revue de ressemblance avec l’utilisateur ; résultat visuel accepté explicitement avant clôture |

### VIS-05a — séance de relevés avant toute reconstruction

Plan préalable `5e717b9`. [Preuves publiées : releves-41](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/releves-41), 13 fichiers vérifiés par SHA-256.

- [x] **A41-01** Choisir EXT-02 comme profil oblique de travail, EXT-03 pour le bombé et DET-03/05 pour la séparation mobile ; garder identités et limites photographiques.
- [x] **A41-02** Enregistrer points et contours en pixels sur les originaux, incertitude de pointage et rapports sans unité ; produire une fiche reproductible nez/coque/verrière sans conversion arbitraire en mètres.
- [x] **A41-03** Extraire les limites des pièces du modèle actuel et identifier fixe/mobile/candidat à découper ; ne pas fixer la charnière sans preuve.
- [x] **A41-04** Capturer six vues générales et des gros plans natifs dans une séance FlightGear isolée ; enregistrer caméra, éclairage et version, comparer qualitativement aux références sans prétendre à une calibration photogrammétrique.
- [x] **A41-05** Écrire un atelier pour débutant avec images, calculs simples, écarts observés et données manquantes ; vérifier liens, rapports et intégrité des originaux.
- [x] **A41-06** Publier les relevés, captures et documentation ; actualiser MD et GitHub. Aucun changement de forme ni du FDM dans cette séance.

### Complément lot02 — détails et ouverture au sol

[Analyse détaillée](docs/references/analyse-details-lot-02.md) · [Manifeste des onze fichiers](docs/references/details-lot-02.json). Six images nouvelles, quatre reprises du lot01 et une copie du presse-papiers, vérifiées par empreintes. Les originaux sont conservés localement. Ces sous-tâches précisent les étapes ci-dessus, sans les déclarer réalisées.

- [ ] **VIS-05c.1 — mécanisme réel :** identifier ensembles fixe/mobile, côté et axe de charnière, poignée, verrou et butée ; comparer ouvert/fermé ; faire confirmer la course, sans angle arbitraire présenté comme mesuré.
- [ ] **VIS-05c.2 — ouverture au sol :** commande de menu FR/EN et poignée cliquable reliées au même état ; animation progressive, fermeture/verrouillage, ouverture autorisée au sol immobilisé ; définir détection sol/vitesse, pause et réinitialisation. Raccourci après contrôle des conflits.
- [ ] **VIS-05c.3 — recette d'ouverture :** captures 0/25/50/75/100 %, intérieur/extérieur, occupants présents/absents ; absence de collision avec aile/nez/tableau ; refus en vol, commande répétée et cohérence de la checklist. Aucun largage de verrière ou effet aérodynamique inventé.
- [ ] **VIS-05k.1 — panneau arrière gris :** panneau principal, relief supérieur, raccord sous aile, ouverture de sangle, vis, plaque et habillages latéraux ; comparer cockpit vide/occupé (DET-02/06).
- [ ] **VIS-05k.2 — coussins bleus :** volumes séparés, épaisseur, coins adoucis et texture textile ; sièges toujours présents sans personnages ; mesures réelles ou estimations explicitement identifiées.
- [ ] **VIS-05k.3 — harnais olive :** cheminement, largeur/épaisseur, boucles et retours, ancrages à confirmer ; états porté/reposant sur siège, pas de traversée du corps ; ne pas inventer de point d'ancrage caché (DET-01/02/05/06).
- [ ] **VIS-05g.1 — mât/Pitot/ficelle :** embase, branches coudées, diamètre, espacement, extrémités et attaches ; confirmer fonctions par référence technique ; relevés en pixels puis échelle documentée, conserver animation et visibilité de ficelle.
- [ ] **VIS-05g.2 — largage arrière :** identifier boule, support et course par schéma et gros plan concordants ; prévoir action commune avec largage avant ; ne pas attribuer cette fonction à l'objet rouge/blanc masqué de DET-06 sans confirmation.
- [ ] **VIS-05g.3 — patin courbe :** profil remontant, semelle, largeur/épaisseur, supports et intervalle sous coque ; captures profil/dessous ; validation des contacts FDM séparée (DET-08).
- [ ] **VIS-05f.1 — détail de queue :** partie fixe jaune, direction bleue, charnières, commandes, raccords et roulette ; confirmer couleur et surfaces de profondeur sur vues complémentaires (DET-04).
- [ ] **VIS-05h.1 — marquages précis :** drapeau canadien sur la pièce correcte, emblème avant, chiffre de nez, éclair bleu et textes ; relevés par variante, contours éditables et aucune lettre en miroir (DET-03/04/05/08/10).
- [ ] **VIS-05l.1 — preuve par détail :** fiche de chaque pièce avec ID photo, observation/estimation/inconnue, dimensions traçables, explication dès 10 ans, vue native avant/après et essai de la commande si interactive ; revue utilisateur avant clôture.

**VIS-05a : relevé préparatoire réalisé** ([atelier23](docs/construction/23-releves-avant.md)) : sept points avec incertitude, onze objets inventoriés, neuf captures natives. Les cotes réelles et la cinématique de charnière restent à confirmer. **Prochain petit lot : VIS-05b/c.** Les autres lignes restent planifiées. Les nouvelles images enrichissent L40-R mais n’établissent pas encore la livrée actuelle exacte de C-FYLP ; L40-R/R2 et les références d’insignes restent ouverts.

## Lots techniques précédents : base fonctionnelle du réalisme

### VIS-01u — matériaux du tableau (terminé : premier réglage)

Preuves : [tutoriel illustré, section Q](docs/construction/06-peinture.md#q--donner-une-matière-différente-à-la-peinture-du-tableau).

Responsable : mainteneur. Référence de disposition : photo C-FYLP ; valeurs optiques artistiques.

- [x] Inventorier les matériaux et distinguer peinture, caoutchouc, métal, verre et surfaces d’instruments.
- [x] Capturer l’état initial dans FlightGear avec cadrage fixe et deux orientations d’éclairage.
- [x] Séparer la peinture mate des matériaux des cadrans ; réduire son aspect auto-éclairé sans changer les aiguilles, textes, géométrie ou commandes.
- [x] Comparer avant/après ; vérifier la lecture des instruments, cartes et radio.
- [x] Synchroniser la recette, expliquer les réglages au débutant avec images, vérifier reconstruction et paquet.
- [x] Publier les preuves et actualiser les MD et GitHub.

**Critère :** peinture visuellement distincte des instruments sous deux éclairages ; aucune variation des indications ou des sources aérodynamiques. Ce premier lot n’est pas une promesse de cockpit déjà photoréaliste.

### Incrément 40 — compléments techniques VIS-01v/w à VIS-04b

Plan autorisé et commité avant l’implémentation (`91daadc`).
Lot technique publié : **45 fichiers vérifiés par SHA-256**, contrôles GitHub Python 3.11/3.13 et site réussis.
Preuves : [atelier 22](docs/construction/22-verifications-visuelles.md), [publication visuals-40](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/visuals-40).
Chaque ligne correspond à un résultat vérifiable. Les réalisations du lot 39 sont
séparées des compléments ; les références absentes ne sont pas des travaux terminés.

Répartition : agent vitrages (banc et protocole), agent livrée (références, UV et
surfaces), agent équipage (références, posture et niveaux de détail). Le mainteneur
intègre, vérifie dans FlightGear, complète les captures, contrôle les recettes et publie.

### VIS-01v/w — verre de la verrière et des instruments

**Déjà livré, lot 39 :** quatre panneaux transparents, trois vitres indépendantes,
effets locaux de ciel statique sous ALS, réglages discrets, clics du calage et de COM1
vérifiés, atlas et tutoriel. Aucune réflexion dynamique du terrain annoncée.

- [x] **V40-01** Étendre le banc : soleil relatif devant/derrière, vue pilote et oblique, vue extérieure, forces 0/1/réglées. Enregistrer les réglages et restaurer toutes les vues visitées.
- [x] **V40-02** Inspecter les captures : aiguilles, ficelle et terrain visibles ; aucun panneau disparu ni scintillement observé dans cette matrice. Consigner les angles testés.
- [x] **V40-03** Essayer le repli sans ALS dans une séance séparée ; ne pas modifier les préférences globales de l'utilisateur.
- [x] **V40-04** Tenter une mesure sans limitation de cadence, avec paramètres documentés. Si le pilote graphique impose encore un plafond, publier cette limite et laisser la mesure du coût GPU ouverte.
- [x] **V40-05** Documenter pour le débutant le protocole, les comparaisons illustrées et les limites ; mettre à jour les preuves du paquet.

**Réussite :** la matrice d'angles et de lumière est illustrée, les commandes restent
utilisables, les erreurs observées sont corrigées ; aucune promesse de performance
universelle à partir d'une machine.

### VIS-02a — références de l'appareil C-FYLP

**Déjà livré :** choix C-FYLP confirmé, registre des recherches, distinction entre
photos historiques et peinture actuelle non attestée.

- [x] **L40-01** Compléter la recherche de vues identifiées et datées : flancs, ailes, dérive, dessus/dessous. Vérifier directement les sources accessibles et consigner les droits.
- [x] **L40-02** Dresser la matrice « confirmé / estimé / inconnu » des couleurs, emplacements, inscriptions et dimensions. Séparer les références de la livrée de celles du cockpit.
- [ ] **L40-R** Obtenir une couverture photographique récente suffisante pour certifier la livrée actuelle ; reste en attente si la recherche ne l'établit pas.

### VIS-02b — surfaces et peinture

**Déjà livré :** fuselage jaune/bleu provisoire, C-FYLP lisible des deux côtés,
plaque du cockpit, affichage réversible et sources éditables originales.

- [x] **L40-03** Étendre les UV aux surfaces pertinentes (ailes, empennages et spoilers), avec grille de contrôle sélectionnable et vérification des symétries et inversions.
- [x] **L40-04** Intégrer une peinture originale cohérente, sans logo ou marquage non sourcé ; conserver distinctement peinture de développement et variante provisoire.
- [x] **L40-05** Vérifier les raccords et l'animation des spoilers rentrés/sortis, vues dessus/dessous et deux distances. Corriger toute séparation entre peau et pièce mobile.
- [x] **L40-06** Illustrer chaque famille de pièces dans le tutoriel, actualiser aperçu et démonstration vidéo.
- [ ] **L40-R2** Reproduire les marquages exacts et leur placement à partir de L40-R, sans présenter les estimations comme des mesures.

### VIS-04a — références des tenues

**Déjà livré :** choix bleu devant / vert derrière, Rodolphe Pagé et Roméo Vachon,
CEC St-Jean, référence officielle C5B, écussons de projet et ailes fictives désactivées.

- [x] **E40-01** Vérifier séparément les références de la tenue de cadet et de celle d'officier ; produire une fiche comparative coupe/poches/insignes/harnais avec provenance et incertitudes.
- [ ] **E40-R** Confirmer les grades, qualifications et écussons exacts avant toute attribution ; aucune déduction à partir des seuls noms.

### VIS-04b — posture, lisibilité et performance des occupants

**Déjà livré :** deux corps détaillés, vêtements et harnais, noms, cou/visage et
manches raccordés ; tête et cou avant masqués dans la vue pilote ; visibilité
indépendante liée aux masses existantes, sans double comptage dans le FDM.

- [x] **E40-02** Contrôler les dégagements tête/verrière, pieds/plancher et mains/commandes à partir des coordonnées du modèle ; corriger les traversées constatées et expliquer les mesures.
- [x] **E40-03** Vérifier en gros plan les étiquettes et pièces de harnais ; adapter la posture et consigner les gestes non animés plutôt que promettre un contact permanent avec les commandes.
- [x] **E40-04** Construire un niveau de détail simplifié pour les vues éloignées, conserver les mêmes conditions de masse et de visibilité ; tester la transition sans duplication.
- [x] **E40-05** Vérifier intérieur/extérieur, occupants absents/présents, commandes aux butées et performances ; produire les captures et l'atlas des pièces modifiées.
- [x] **E40-06** Synchroniser la recette complète du tutoriel et ses explications simples ; conserver les inconnues réglementaires dans le registre de références.

### Intégration et publication de l'incrément 40

- [ ] **I40-01** Reconstruire depuis le tutoriel ; contrôler les dépendances, les UV, les niveaux de détail et les éléments mobiles avec des tests adaptés.
- [x] **I40-02** Corriger le centrage des vues extérieures sur un repère du modèle (sans déplacer le modèle ni le centre de gravité), puis vérifier le paquet final dans FlightGear ; actualiser description, aperçu, tutoriels, README, CHANGELOG et validation.
- [x] **I40-03** Publier commits, paquet, images, vidéo et atlas sur GitHub ; vérifier intégrité des fichiers et contrôles automatiques.

**Mesure encore ouverte :** isoler le coût GPU hors du plafond proche de 60 Hz (V40-04). Les mains restent fixes ; aucun contact animé permanent avec les commandes n’est validé.

Les références exactes manquantes restent ouvertes même si le lot technique est
livré. Aucun critère n'est coché sur la seule base d'une génération de fichiers.

## Autres travaux ouverts

| Priorité | Lot | Prochaine action / dépendance |
|---|---|---|
| P1 | VIS-01t | Confirmer Ctrl+L au clavier physique lorsque la checklist est fermée ; petits formats supplémentaires et autres versions |
| P1 | VIS-01e | Obtenir les relevés physiques de verrière, porte et sections avant de déplacer les stations |
| P2 | AUD-01d | Diagnostiquer le pavé numérique par comparaison avec un champ standard |
| P2 | AUD-02c | Tester installation et lancement sur Linux natif |
| P2 | AUD-13/14 | Consolider construction et validation automatiques des paquets publiés sur tag |
| P2 | AUD-01a/03/09 | Identifier pesée et repères ; comparer polaire, masses et vitesses aux références |
| P2 | AUD-05/06 | Contacts, frein, treuil, remorquage et largage avec essais séparés |
| P2 | AUD-10 | Sourcer urgences GASP/VEST et GPAS/PTES et inspections ; ne pas automatiser une procédure non disponible |
| P2 | AUD-07/08/12 | Maintenabilité, pause, reinitialisation et restauration des bancs |
| P2 | AUD-16 | Faire reconstruire le projet par un débutant sans aide orale |
| Futur | AUD-04 | Vol lent, décrochage et autorotation après validation des données de base |
| Futur | VIS-03 | Poste arrière interactif et variantes après le poste avant ; distinct des personnages VIS-04 |
| Futur | AUD-17/15 | Documentation anglaise maintenue et éventuelle candidature au hangar officiel |

## Travaux terminés et preuves

- Enveloppe et contrôle des proportions VIS-01a à d : [fiches de construction](docs/construction/14-enveloppe.md). Relevés VIS-01e toujours attendus.
- Finition et relief des instruments VIS-01f à o : [atelier de peinture](docs/construction/06-peinture.md). Les anciens titres « en cours » sont historiques.
- Bilinguisme VIS-01p, cartes VIS-01q et recettes VIS-01r/s : [atelier des listes](docs/construction/05-listes.md). Formulation française officielle et urgences restent distinctes.
- VIS-01t : souris, correction 1024 × 600, tutoriel et paquet [checklists-usage-37](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/checklists-usage-37) ; complément clavier indiqué plus haut.
- Profondeur AUD-01b, occupants AUD-01c, paquet AUD-02a et sélecteur AUD-02b : [archive et preuves](docs/planification/archive-roadmap-2026-11-17.md).
- Vol filmé à CYJN : [validation](docs/validation.md). Les essais d’affichage ne valident pas la physique du vol.

## Suivi et contributions

[Issues GitHub](https://github.com/steveprudhomme/sw233-flightgear/issues) · [Jalons](https://github.com/steveprudhomme/sw233-flightgear/milestones) · [Backlog des audits](docs/planification/backlog-audits.md) · [CONTRIBUTING](CONTRIBUTING.md).

Les codes AUD/VIS sont des identifiants documentaires, pas des numéros de tickets. Responsables recherchés : références Cadets, artistes 3D, texture, testeurs Linux et lecteurs débutants. À chaque lot : plan et commit préalables, réalisation, preuves natives, tutoriel illustré, tests adaptés, MD et publication. Ne cocher que les résultats vérifiés ; ne pas ajouter une copie du journal de travail à la fin de cette synthèse.

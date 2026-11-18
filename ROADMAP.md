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
| Validation | Essais natifs Windows à CYJN, 66 tests pour la préversion 0.1.0-alpha.2, reconstruction du tutoriel | Polaire réelle, Linux et relecture autonome du tutoriel non validés |

Statuts : **en cours** = lot commencé ; **prévu** = travail accepté à réaliser ; **attend une référence** = détail non confirmé ; **terminé** = preuve publiée. Les anciens protocoles sont dans l’[archive du 17 novembre](docs/planification/archive-roadmap-2026-11-17.md), et ne constituent plus une deuxième liste active.

## Priorité actuelle — VIS-05 : reprise de la fidélité visuelle

**Statut : en cours, rendu du lot40 non accepté visuellement par l’utilisateur.** Le lot40 reste une livraison technique ; il ne clôt pas l’objectif de ressemblance. Les dix nouvelles références sont conservées localement et analysées dans le [dossier extérieur lot01](docs/references/analyse-exterieur-lot-01.md), avec [manifeste des originaux](docs/references/exterieur-lot-01.json).

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

### Lot42 — reconstruction VIS-05b/c

- [x] **BC42-01** Reconstruire la recette de base ; inventorier coutures coque/vitrage, matériaux, objets animés, UV et dégagements occupants. Conserver les valeurs estimées comme telles.
- [x] **BC42-02** Ajouter des sections longitudinales courbes au nez et à la coque avant ; affiner les sections transversales sans effacer les cassures réelles du ventre. Vérifier fermeture, symétrie et absence de faces dégénérées.
- [x] **BC42-03** Refaire le bombé du pare-brise, les sections de verrière et les cadres ; partager exactement les bords avec la coque. Maintenir le raccord sous aile et les instruments dégagés ; ouverture au sol distincte de ce lot de forme.
- [x] **BC42-04** Adapter les dépendances strictement nécessaires : peau UV, attaches éventuelles, tests de couverture et dégagements ; garder les gouvernes et le FDM inchangés. Vérifier la reconstruction exacte du tutoriel.
- [x] **BC42-05** Comparer mêmes caméras/éclairage au lot41 dans FlightGear, intérieur/extérieur et grille UV ; produire images avant/après et planches des pièces reprises, corriger les défauts observés.
- [x] **BC42-06** Documenter chaque choix de forme et hypothèse dès 10 ans, actualiser aperçu/description si pertinent, publier sources, paquet et preuves sur GitHub. La ressemblance finale reste soumise à revue utilisateur.

**Livraison technique lot42 :** [formes-42](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/formes-42), source `6e0822f`, 25 fichiers publiés et empreintes vérifiées. La revue de ressemblance et les détails restant dans VIS-05b/c ne sont pas clos par cette livraison.


### Lot44 — ouvrir la verrière au sol

Priorité confirmée avant VIS-05d. Préversion visée : `0.1.0-alpha.2`.

- [x] **C44-01** Comparer DET-01/03/05/09 et le manuel ; identifier la verrière avant mobile, les vitrages arrière fixes, le côté des charnières et le verrou. Consigner les dimensions et la course estimées.
- [x] **C44-02a** Appliquer la précision du 17 novembre : occupant arrière sous l’aile, vitrage fixe central entre les ailes. Retirer le recouvrement des ailes sur ce vitrage ; vérifier dessus et place arrière.
- [x] **C44-02** Séparer vitrage, cadres, joints et fixations mobiles ; placer les charnières et la poignée du bon côté. Conserver le raccord sous aile et la porte arrière fixes.
- [x] **C44-03** Ajouter un état commun : fermé verrouillé, en mouvement, ouvert ; commande par poignée et menu FR/EN. Refuser l'ouverture en vol ou en déplacement. Permettre la fermeture, gérer pause et réinitialisation, sans effet aérodynamique inventé.
- [x] **C44-04** Afficher l'état réel dans les checklists FR/EN ; conserver les acronymes et distinguer la porte arrière fixe.
- [ ] **C44-05** Tester refus, commande répétée, fermeture, pause, réinitialisation et changement de langue dans FlightGear ; capturer 0/25/50/75/100 % depuis le cockpit et l'extérieur, avec et sans occupants.
- [x] **C44-06** Examiner les dégagements avec le nez, les ailes, le tableau et les personnages ; vérifier les pièces mobiles et la recette complète du tutoriel.
- [x] **C44-07** Publier le tutoriel illustré selon le guide de rédaction, les limites, le paquet SemVer, les MD et les preuves sur GitHub. L'essai par un enfant et l'acceptation de ressemblance restent distincts.

### Lot43 — finition des formes VIS-05b/c

Objectif : corriger les écarts visibles du lot42 avant de passer aux ailes. La clôture
technique de ce lot ne vaut pas acceptation utilisateur de la ressemblance ;
l'ouverture animée reste dans VIS-05c.1 à c.3.

- [x] **BC43-01** Revoir EXT-02/03/05 et DET-03/05 ; confronter nez, hauteur des flancs, cadre avant et raccord sous aile au lot42 ; consigner observations, estimations et inconnues.
- [x] **BC43-02** Corriger le volume du nez et son raccord aux flancs ; adoucir la pointe sans supprimer les cassures du ventre ; adapter les attaches avant uniquement si le nouveau capot l'exige.
- [x] **BC43-03** Corriger le raccord haut arrière et les vitrages latéraux ; détailler cadres, joints, contours et fixations visibles avec dimensions estimées explicites ; conserver tableau, occupants et enveloppe fermée.
- [x] **BC43-04** Comparer aux photos dans une galerie locale et dans FlightGear : profil, face, obliques, cockpit, deux orientations d'éclairage et grille UV ; examiner chaque pièce et corriger les écarts constatés.
- [x] **BC43-05** Vérifier coutures, surfaces, symétrie, UV, dégagements et animations affectées ; reconstruire exactement depuis le tutoriel ; conserver le FDM inchangé.
- [x] **BC43-07** Adopter SemVer : première préversion `0.1.0-alpha.1`, fichier VERSION unique, concordance avec FlightGear et le manifeste ; documenter la compatibilité et conserver les anciennes publications.
- [x] **BC43-08** Tester cette concordance, publier sous `v0.1.0-alpha.1` et vérifier les fichiers GitHub.
- [x] **BC43-06** Illustrer la démarche dès 10 ans avec les pièces et captures avant/après ; actualiser MD, aperçu, paquet et GitHub ; distinguer finition réalisée, mécanisme restant et revue utilisateur.

**État après finition :** formes statiques du nez, des flancs et de la verrière reprises,
cadres/joints/fixations et poignée de représentation ajoutés ([atelier25](docs/construction/25-finitions-avant.md)).
Les cases globales VIS-05b/c restent ouvertes pour la revue de ressemblance et les
charnières non confirmées ; elles ne signifient pas que le lot technique est à refaire.
**Lot44 : ouverture avant réalisée et vérifiée, avec réserves explicites.**
Voir [le tutoriel26](docs/construction/26-ouverture-verriere.md) et [le bilan](docs/validation/verriere-lot44.md).
Le vitrage arrière est fixe entre les ailes ; le passager arrière reste sous l’aile.
La course réelle et l’acceptation de ressemblance restent attendues.
La réinitialisation complète ferme FlightGear sur cette machine, y compris avec alpha.1.
La reprise des ailes ne clôt pas ces réserves.

### Complément lot02 — détails et ouverture au sol

[Analyse détaillée](docs/references/analyse-details-lot-02.md) · [Manifeste des onze fichiers](docs/references/details-lot-02.json). Six images nouvelles, quatre reprises du lot01 et une copie du presse-papiers, vérifiées par empreintes. Les originaux sont conservés localement. Ces sous-tâches précisent les étapes ci-dessus, sans les déclarer réalisées.

- [ ] **VIS-05c.1 — mécanisme réel :** identifier ensembles fixe/mobile, côté et axe de charnière, poignée, verrou et butée ; comparer ouvert/fermé ; faire confirmer la course, sans angle arbitraire présenté comme mesuré.
- [x] **VIS-05c.2 — ouverture au sol :** commande de menu FR/EN et poignée cliquable reliées au même état ; animation progressive, fermeture/verrouillage, ouverture autorisée au sol immobilisé ; définir détection sol/vitesse, pause et réinitialisation. Menu et poignée livrés ; aucun nouveau raccourci. Réinitialisation complète limitée par FG-44-01.
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

**VIS-05a : relevé préparatoire réalisé** ([atelier23](docs/construction/23-releves-avant.md)) : sept points avec incertitude, onze objets inventoriés, neuf captures natives. Les cotes réelles et la cinématique de charnière restent à confirmer. **Lot42 : première reconstruction VIS-05b/c réalisée**, [atelier24](docs/construction/24-formes-avant.md). Neuf objets repris, contrôle natif et recette vérifiée ; revue de ressemblance, quincaillerie et ouverture restent ouvertes. Les autres lignes restent planifiées. Les nouvelles images enrichissent L40-R mais n’établissent pas encore la livrée actuelle exacte de C-FYLP ; L40-R/R2 et les références d’insignes restent ouverts.

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

## DOC-01 — Règles de rédaction accessibles

Cette règle s'applique à toute nouvelle documentation et aux passages révisés. Consulter le [guide de rédaction](docs/guide-redaction.md).

- [x] **DOC-01a** Conserver le kit, vérifier ses liens et télécharger les 14 ressources ; relever leur version, leur statut et leur empreinte.
- [x] **DOC-01b** Écrire le guide de rédaction : WCAG 2.2 et 3.1.5, CAN-ASC-3.1:2025, repères scolaires du Québec et Simple French ; distinguer exigences et choix du projet.
- [x] **DOC-01c** Relier le guide aux consignes des contributeurs et des agents ; fournir une grille de relecture et un exemple de tâche.
- [ ] **DOC-01d** Faire essayer un prochain tutoriel à un lecteur débutant ; noter les obstacles et les corrections. Ne pas déclarer une conformité globale sans audit.

## Suivi et contributions

[Issues GitHub](https://github.com/steveprudhomme/sw233-flightgear/issues) · [Jalons](https://github.com/steveprudhomme/sw233-flightgear/milestones) · [Backlog des audits](docs/planification/backlog-audits.md) · [CONTRIBUTING](CONTRIBUTING.md).

Les codes AUD/VIS sont des identifiants documentaires, pas des numéros de tickets. Responsables recherchés : références Cadets, artistes 3D, texture, testeurs Linux et lecteurs débutants. À chaque lot : plan et commit préalables, réalisation, preuves natives, tutoriel illustré, tests adaptés, MD et publication. Ne cocher que les résultats vérifiés ; ne pas ajouter une copie du journal de travail à la fin de cette synthèse.


### Réserves de validation du lot44

- [ ] **FG-44-01** Diagnostiquer la fermeture de FlightGear 2024.1.7 lors de la commande de réinitialisation complète. Reproduite aussi sur alpha.1 ; le signal de remise à zéro de la verrière fonctionne séparément.
- [ ] **C44-08** Faire confirmer la course et les cotes des charnières sur l’appareil de référence. Les 100 degrés restent une estimation.
- [ ] **C44-09** Faire accepter la ressemblance et essayer le tutoriel26 avec un lecteur débutant.

C44-05 reste ouvert uniquement pour la réinitialisation complète. Les 30 captures,
les 14 contrôles natifs et les états de checklist FR/EN sont réalisés.
VIS-05c.1 et VIS-05c.3 restent ouverts pour leurs réserves ; cela ne signifie pas que
l’ouverture avant reste à programmer. La porte arrière reste fixe et constitue un travail distinct.

**Publication lot44 :** [0.1.0-alpha.2](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/v0.1.0-alpha.2), source `9888552`, 44 fichiers vérifiés par SHA-256. Contrôles Python 3.11/3.13 réussis ; tutoriel publié. Les réserves ci-dessus restent ouvertes.


### Lot45 — raccord du vitrage central et dossier arrière

Demande du 17 novembre 2026 : vitrage contre les rebords d’aile, bande bleue à la jonction,
faces intérieures grises et dossier arrière moulé pour la silhouette humaine.
Préversion prévue : `0.1.0-alpha.3`. Plan à commiter avant modification.

- [x] **R45-01** Reprendre DET-02/03/06/09 ; comparer le vitrage actuel aux racines d’aile et identifier les écarts. Distinguer formes observées et cotes estimées.
- [x] **R45-02** Partager le contour de raccord aile/vitrage ; supprimer le jour visible et poser deux bandes bleues continues.
- [x] **R45-03** Fermer les faces internes des racines d’aile avec un habillage gris visible depuis la place arrière.
- [x] **R45-04** Donner au dossier gris arrière un relief pour le torse, les épaules et la tête. Préserver le passage de sangle et vérifier les dégagements avec l’occupant.
- [x] **R45-05** Comparer avant/après dans FlightGear : dessus, trois-quarts, intérieur arrière ; occupants présents/absents et verrière ouverte/fermée. Vérifier les commandes existantes.
- [x] **R45-06** Ajouter un tutoriel illustré selon le guide de rédaction ; synchroniser les recettes, tester, publier le paquet SemVer et actualiser les MD/GitHub.

La fidélité des dimensions et l’acceptation visuelle restent à confirmer avec le mainteneur.
Ce lot ne clôt pas la reconstruction générale des ailes ni le détail complet des harnais.

- [ ] **R45-07 — référence à confirmer** Identifier la possible grille d’aération signalée par le mainteneur. Distinguer plaque d’instructions et ouverture ; ne pas créer de conduit dans l’aile sans référence concordante.


**Précision du mainteneur — R45-07 :** ouverture à la jonction de l’aile gauche seulement,
avec un aspect de filtre ; fonction d’aération encore hypothétique. Ajouter une représentation visuelle à gauche,
sans symétrie à droite ni simulation de circuit d’air. R45-04 comprend le passage noir en demi-lune
et la sangle verte derrière le passager ; les ancrages cachés restent inconnus.

**Bilan lot45 :** géométrie et essais réalisés ; [tutoriel27](docs/construction/27-raccords-arriere.md). R45-07 reste ouvert pour confirmer la fonction, la forme et les dimensions de l’ouverture gauche. Sa représentation visuelle est réalisée. Acceptation visuelle et relevés physiques toujours attendus.

**Publication :** [0.1.0-alpha.3](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/v0.1.0-alpha.3), source `16e17d6`. Les 51 fichiers publiés correspondent aux empreintes SHA-256 locales. Le paquet contient son aperçu natif et son manifeste vérifié.

### Lot46 — corriger la limite de la verrière mobile

Correction demandée sur la photo DET-03 : la partie mobile rejoint la racine d’aile.
Le cadre transversal ajouté au milieu du vitrage ne correspond pas à cette référence.
Préversion prévue : `0.1.0-alpha.4`. Plan préalable à la modification.

- [ ] **C46-01** Déplacer la séparation fixe/mobile au bord avant de l’aile, à la station 1,99 m du modèle ; conserver le vitrage entre les ailes fixe.
- [ ] **C46-02** Supprimer les arceaux intermédiaires aux stations 1,55 et 2,13 m ; conserver uniquement les cadres périphériques utiles.
- [ ] **C46-03** Ajuster l’axe latéral et les charnières à la longueur corrigée ; vérifier les états fermé, intermédiaire et ouvert dans FlightGear.
- [ ] **C46-04** Tester la limite du vitrage et l’absence de cadre central ; synchroniser les recettes et documenter avec des captures comparables.
- [ ] **C46-05** Publier le paquet SemVer et les preuves ; vérifier GitHub et garder les cotes réelles à confirmer.

La station et l’angle de 100 degrés restent des estimations. La photo justifie la découpe et l’absence d’arceau central, pas des mesures exactes.

**Précision photographique — lot46 :** aligner la cloison arrière sur le hauban entouré par le mainteneur, en vue de profil. Le « tiers de l’aile » était un repère approximatif.

- [ ] **C46-06** Archiver l’image annotée ; rapprocher la cloison, la fin du vitrage arrière et le début de la coque jaune du repère du hauban. Déplacer ensemble le siège arrière, le personnage et la sangle pour préserver leur dégagement. Conserver le dossier moulé. Contrôler les profils avec et sans personnage ; ne pas modifier les masses physiques.

- [ ] **C46-07** Reproduire le montant arrière incliné et le léger bombé de la verrière avant sa descente vers l’aile, selon la seconde annotation. Conserver le contact des bords du vitrage central avec les ailes. Documenter l’inclinaison et le bombé comme estimations photographiques, puis comparer le profil fermé et ouvert.

**Complément C46-06 :** l’annotation verte confirme que le vitrage central fixe se termine vers le premier tiers de l’aile, près du hauban. La partie mobile se termine au montant incliné avant cette zone.

### Détails photographiques à réaliser après le lot46

- [ ] **EXT-47a** Reproduire l’antenne radio blanche signalée sur la photo annotée : position, inclinaison, section et fixation à relever. Ne pas confondre cette pièce avec le tube de Pitot du nez.
- [ ] **EXT-47b** Reproduire les deux petites roues d’aile, une à chaque extrémité, avec leurs supports. Comparer les vues des deux côtés ; dimensions et fixations à confirmer. Distinguer ces pièces de la roue principale et de la roulette arrière. La vue `roue-aile-support-annote.png` précise une petite roue noire portée par un support jaune incliné sous l’aile. Relever séparément le pneu, le moyeu, le support, son angle et sa fixation ; ne pas remplacer cet ensemble par un simple disque collé à l’aile. Les dimensions et les détails masqués restent à confirmer.
- [ ] **EXT-47c** Illustrer chaque pièce dans le tutoriel et vérifier les deux côtés dans FlightGear avant publication.
- [ ] **EXT-47d** Ajouter la petite poignée tubulaire à l’avant du nez, signalée par le mainteneur pour saisir l’appareil à la main. Relever sa position, sa longueur, son diamètre et sa fixation ; distinguer cette pièce du tube de Pitot.
- [ ] **EXT-47e** Ajouter le dispositif d’accrochage du câble sous le nez, entouré sur la photo. Reproduire sa forme visible et son raccord avec l’anneau du câble. Confirmer le type de crochet et son usage en remorquage aérien ou au treuil avant de lui attribuer un fonctionnement ; relier toute animation future aux essais AUD-05/06.
- [ ] **EXT-47f** Ajouter le petit marchepied sur le flanc du fuselage, sous le cockpit, à gauche du logo dans la photo `marchepied-cockpit.png`. Reproduire le court support saillant, sa surface sombre et son extrémité jaune visibles. Relever la position, les dimensions et la fixation ; confirmer le côté de l’appareil et la présence éventuelle d’un second marchepied avant toute duplication. Illustrer la pièce dans le tutoriel et comparer son placement dans FlightGear.


Pour EXT-47d/e : illustrer chaque pièce dans le tutoriel, comparer les vues de profil et de dessous dans FlightGear, puis actualiser les MD et les preuves. Référence locale : `docs/references/originaux/details-lot-02/poignee-accrochage-nez-annote.png`.


Référence locale conservée : `docs/references/originaux/details-lot-02/antenne-roues-ailes-annote.png`.
Les deux annotations du mainteneur identifient l’antenne blanche et une roue d’aile ; la présence des roues des deux côtés est précisée par le mainteneur.

**État lot46 :** correction technique en cours de revue ; [tutoriel28](docs/construction/28-silhouette-verriere.md). La première silhouette a été rejetée ; une courbe continue remplace le bombé local. Ne pas cocher la validation visuelle ni publier alpha.4 tant que la forme reste contestée. EXT-47 est planifié, pas réalisé.

### Correction prioritaire de silhouette — fuselage arrière

- [ ] **VIS-48a** Relever le contour supérieur du fuselage en vue de profil, de la sortie de l’aile jusqu’au pied de la dérive, selon le trait rouge fourni. Choisir deux repères et une pente constante ; confirmer les cotes sur des vues complémentaires.
- [ ] **VIS-48b** Remplacer la bosse et le creux actuels du raccord arrière par une ligne supérieure droite, inclinée vers la queue. Assurer la continuité avec la zone sous l’aile et le pied de la dérive. Préserver les sections transversales : une ligne droite en profil ne signifie pas un fuselage entièrement plat.
- [ ] **VIS-48c** Contrôler le contour inférieur et les flancs sur les photos avant de modifier leurs formes. Vérifier aussi les bandes de livrée après la correction de géométrie.
- [ ] **VIS-48d** Comparer avant/après dans FlightGear en profil et trois-quarts ; ajouter des contrôles de rectitude du contour, synchroniser les recettes et illustrer le tutoriel. Ne pas déclarer la silhouette validée sur les seuls tests techniques.

Référence locale conservée : `docs/references/originaux/details-lot-02/fuselage-arriere-rectiligne-annote.png`.
Cette correction de forme est prioritaire sur les petits accessoires EXT-47. Le trait annoté porte sur le contour supérieur visible, pas sur les dimensions exactes ni toutes les sections du fuselage.

### VIS-49 — porte du passager arrière

La porte arrière reste fixe dans le modèle actuel. Ce chantier est distinct de l’ouverture de la verrière avant.
Le mainteneur précise une ouverture « à l’envers », interprétée ici comme une ouverture vers l’arrière, et un contour oblique.

- [ ] **VIS-49a** Relever le contour oblique du panneau jaune et du vitrage arrière sur les deux photos annotées. Respecter la partie basse effilée et les raccords avec le seuil, l’aile et la cloison. Ne pas remplacer cette porte par un rectangle vertical.
- [ ] **VIS-49b** Identifier le côté de l’appareil, les charnières, leur axe, le verrou et la course. Confirmer le mouvement vers l’arrière sur une vue de la porte ouverte ; les deux photos seules ne montrent pas toute sa trajectoire.
- [ ] **VIS-49c** Séparer les pièces mobiles et fixes après confirmation du mécanisme : panneau, vitrage, cadres, joints et fixations. Préserver la continuité de la bande bleue lorsque la porte est fermée.
- [ ] **VIS-49d** Ajouter une commande d’ouverture et de fermeture au sol, distincte de la verrière avant. Vérifier les collisions avec l’aile, le hauban, le siège, le passager et la verrière ; vérifier les états intermédiaires et le verrouillage.
- [ ] **VIS-49e** Documenter chaque pièce et le mouvement dans le tutoriel avec images et texte simple. Comparer dans FlightGear, ajouter les tests adaptés et actualiser les MD et les états de checklist concernés avant publication.

Références locales : `docs/references/originaux/details-lot-02/porte-arriere-bord-annote.png` et `porte-arriere-oblique-annote.png`.
Les dimensions, l’axe exact et la course restent à confirmer. Réaliser ce chantier après stabilisation des raccords du cockpit et du fuselage.

### VIS-50 — ouvertures et tableau plastifié à la racine d’aile

Ce gros plan complète R45-07 ; il ne confirme pas encore une fonction d’aération.
Le type du tableau reste à identifier : masse et centrage (poids et centrage), décrochage ou autre tableau. Le mainteneur demande de vérifier le manuel avant de conclure. Son texte est trop peu lisible sur la photo pour être transcrit fidèlement.

- [ ] **VIS-50a** Relever les deux zones entourées de chaque côté du tableau, leurs contours et leur position dans l’habillage intérieur de la racine d’aile. Confirmer s’il s’agit d’ouvertures, de trappes ou d’autres éléments, et leur fonction. Comparer avec la grille provisoire du lot45 avant de la corriger ; ne pas créer une seconde installation par simple duplication.
- [ ] **VIS-50b** Ajouter le tableau plastifié signalé : support rectangulaire, bordure claire, épaisseur, fixations aux coins et emplacement observés. Respecter son orientation par rapport au panneau intérieur et à l’aile.
- [ ] **VIS-50c** Revoir le manuel du SGS 2-33 et les instructions d’exploitation Cadets pour identifier le tableau présent à cet emplacement. Comparer les tableaux de masse et centrage, de chargement et de décrochage avec le titre, les axes, les unités et la disposition visibles. Consigner le document, son édition, la page et la figure retenues. Obtenir une vue plus lisible si le manuel ne permet pas de trancher. Confirmer le type du tableau avant de reproduire son contenu ; ne pas inventer les valeurs ni utiliser des données propres à un autre appareil sans vérification.
- [ ] **VIS-50d** Prévoir une texture lisible et un reflet discret du revêtement plastifié. Vérifier le résultat depuis la place arrière dans FlightGear ; illustrer séparément les ouvertures et le tableau dans le tutoriel, puis actualiser les MD et les preuves.

Référence locale conservée : `docs/references/originaux/details-lot-02/ouvertures-tableau-decrochage-annote.png`.
Les deux cercles désignent des détails dans le même panneau ; ils ne prouvent pas la présence d’un équipement identique dans l’autre aile. R45-07 reste ouvert jusqu’à identification.

#### Exécution VIS-48 — contour supérieur rectiligne

Plan préalable du 17 novembre 2026. Travail sur la branche de revue du lot46 ; alpha.4 reste en préparation.

- [ ] **VIS-48a.1** Conserver un paquet avant modification et relever le sommet de chaque section du maillage entre la sortie d’aile et la queue.
- [ ] **VIS-48a.2** Utiliser les repères existants du modèle : sortie d’aile à x = 3,56 m et extrémité de coque à x = 7,61 m. Relier leurs hauteurs actuelles par une droite ; indiquer que ces cotes sont estimées, et non mesurées sur la photo.
- [ ] **VIS-48b.1** Remplacer uniquement le contour supérieur arrière par cette pente constante ; conserver les raccords de bord, la symétrie et les sections transversales. Vérifier la jonction avec la dérive.
- [ ] **VIS-48c.1** Comparer le bas de coque et les flancs avec le paquet précédent ; vérifier l’absence de changement involontaire et les textures de livrée dans le paquet final.
- [ ] **VIS-48d.1** Ajouter un test sur les sommets exportés : rectitude, continuité au bord de fuite et extrémité arrière. Exécuter les tests de fermeture de coque, les tests de régression et la reconstruction du tutoriel.
- [ ] **VIS-48d.2** Comparer avant/après dans FlightGear avec les mêmes vues de profil gauche/droit et trois-quarts ; contrôler aussi l’ouverture de verrière.
- [ ] **VIS-48d.3** Ajouter un atelier illustré pour débutant, le bilan des contrôles et les limites ; actualiser le ROADMAP, le CHANGELOG et la proposition GitHub. Garder l’acceptation de la silhouette complète ouverte.

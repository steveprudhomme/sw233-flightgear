# Feuille de route — Schweizer SGS 2-33

Mise à jour : **17 novembre 2026**. Les lots définissent du contenu, pas des dates promises.

## Vision et périmètre

Reproduire dans FlightGear un Schweizer SGS 2-33 crédible aux couleurs des Cadets de l’aviation royale du Canada, avec une construction expliquée pas à pas. Les détails attestés, les choix artistiques et les essais doivent rester identifiables.

Prototype de simulation sous GPL-3.0-only, non certifié pour l’instruction réelle. Les ressources tierces gardent leurs droits ; aucune fidélité exacte de géométrie, d’uniforme ou de performances n’est annoncée sans référence.

## État actuel

| Domaine | Réalisé | Limite restante |
|---|---|---|
| Cockpit | Enveloppe, cadres, relief des instruments, calage, COM1 et compas | Matériaux simplifiés ; profondeurs estimées ; audio radio non validé |
| Checklists | FR/EN, accents, initiales rouges, souris et format 1024 × 600 | Ctrl+L physiquement confirmé ouvert ; essai fermé encore à préciser |
| Extérieur | Prototype jaune, spoilers et ficelle animés | Livrée actuelle et immatriculation non reproduites |
| Occupants | Masses et centrage réglables | Aucun équipage humain détaillé |
| Validation | Essais natifs Windows à CYJN, 25 tests dans le lot accents, reconstruction du tutoriel | Polaire réelle, Linux et relecture autonome du tutoriel non validés |

Statuts : **en cours** = lot commencé ; **prévu** = travail accepté à réaliser ; **attend une référence** = détail non confirmé ; **terminé** = preuve publiée. Les anciens protocoles sont dans l’[archive du 17 novembre](docs/planification/archive-roadmap-2026-11-17.md), et ne constituent plus une deuxième liste active.

## Prochain incrément : réalisme du cockpit

### VIS-01u — matériaux du tableau (en cours)

Responsable : mainteneur. Référence de disposition : photo C-FYLP ; valeurs optiques artistiques.

- [ ] Inventorier les matériaux et distinguer peinture, caoutchouc, métal, verre et surfaces d’instruments.
- [ ] Capturer l’état initial dans FlightGear avec cadrage fixe et deux orientations d’éclairage.
- [ ] Séparer la peinture mate des matériaux des cadrans ; réduire son aspect auto-éclairé sans changer les aiguilles, textes, géométrie ou commandes.
- [ ] Comparer avant/après ; vérifier la lecture des instruments, cartes et radio.
- [ ] Synchroniser la recette, expliquer les réglages au débutant avec images, vérifier reconstruction et paquet.
- [ ] Publier les preuves et actualiser les MD et GitHub.

**Critère :** peinture visuellement distincte des instruments sous deux éclairages ; aucune variation des indications ou des sources aérodynamiques. Ce premier lot n’est pas une promesse de cockpit déjà photoréaliste.

### VIS-01v — reflets de la verrière (prévu)

- [ ] Relever les panneaux existants, leurs normales, transparence et ordre de rendu.
- [ ] Examiner les effets disponibles dans la version FlightGear testée ; distinguer éclat spéculaire et véritable réflexion d’environnement.
- [ ] Prototyper un effet réversible sur un panneau, puis régler intensité, teinte et dépendance à l’angle de vue.
- [ ] Étendre aux panneaux validés ; garder ficelle, terrain et instruments visibles de l’intérieur et de l’extérieur.
- [ ] Tester soleil devant/derrière, vue oblique, tri des transparences et coût d’affichage ; illustrer avant/après.

**Critère :** reflet observable sans opacifier la verrière, sans faces disparues ni affirmation de réflexion dynamique si l’effet n’en produit pas.

### VIS-01w — vitres et reflets des cadrans (prévu)

- [ ] Identifier les instruments munis de verre dans les photos ; conserver un espace devant les aiguilles et textes.
- [ ] Construire une vitre pilote sur un instrument avec matériau indépendant.
- [ ] Tester face/biais et plusieurs éclairages ; régler les reflets pour conserver graduations et aiguilles lisibles.
- [ ] Étendre aux instruments appropriés, vérifier calage et radio, puis produire un atlas et un tutoriel illustré.

**Critère :** pas de scintillement, d’aiguille masquée ou de clic bloqué ; effet expliqué et mesuré en temps de rendu avant généralisation.

## Livrée actuelle des Cadets et immatriculation

### VIS-02a — appareil et dossier photographique (attend une référence)

- [ ] Confirmer l’appareil, son immatriculation et la période de livrée ; C-FYLP reste la référence du cockpit, sans supposer sa décoration extérieure actuelle.
- [ ] Réunir des vues datées gauche/droite/dessus/dessous, dérive, ailes et marquages ; conserver provenance et droits.
- [ ] Relever les limites jaune/bleu, symboles, typographie, immatriculation et inscriptions réellement lisibles.
- [ ] Produire une fiche de référence distinguant dimensions mesurées, proportions photographiques et éléments encore inconnus.

### VIS-02b — dépliage et peinture de l’appareil (prévu après VIS-02a)

- [ ] Vérifier silhouette, symétries et pièces mobiles ; préparer des coordonnées UV par pièce.
- [ ] Appliquer une grille de contrôle pour repérer étirements et inversions.
- [ ] Créer des textures originales éditables : couleurs, panneaux, raccords, logos documentés et usure modérée.
- [ ] Ajouter l’immatriculation choisie à ses emplacements attestés, sans lettres en miroir ; cohérence entre extérieur et plaque du cockpit.
- [ ] Vérifier ailes, fuselage, dérive et spoilers sortis/rentrés ; contrôler les coutures de texture et la lecture à plusieurs distances.
- [ ] Conserver une livrée de développement distincte ; documenter le choix de livrée, actualiser aperçus FlightGear et vidéo.

**Critère :** comparaison avec un appareil identifié et daté ; aucune « livrée actuelle » fondée seulement sur une vieille peinture FSX.

## Deux occupants détaillés

### VIS-04a — références des tenues (prévu)

- [ ] Poste avant : cadet en combinaison de vol bleue ; poste arrière : officier en combinaison verte, conformément au choix demandé.
- [ ] Vérifier séparément coupe, poches, fermeture, col, coutures, chaussures et harnais.
- [ ] Documenter les badges, ailes, écussons, grades et étiquettes nominatives pour chaque tenue ; ne pas transposer les règles d’une tenue de cérémonie à une combinaison.
- [ ] Confirmer noms, escadron/unité et qualifications ; à défaut préparer des personnages fictifs et des zones d’insignes non attribués.
- [ ] Créer une planche de références avec dates, provenance, droits et incertitudes.

### VIS-04b — modèles humains et intégration (prévu après VIS-04a)

- [ ] Construire deux personnages originaux en posture assise, avec proportions et détails adaptés aux deux places.
- [ ] Modéliser les combinaisons : plis aux articulations, épaisseur, poches, coutures et fermeture ; textures de tissu sans bruit exagéré.
- [ ] Créer badges, ailes et name tags séparés avec relief discret ; vérifier orientation et lisibilité sans inventer de décorations.
- [ ] Ajuster harnais, mains, pieds, sièges et commandes ; éviter les traversées de verrière et de fuselage.
- [ ] Prévoir visibilité et niveaux de détail ; masquer si nécessaire la tête du personnage dont on occupe le point de vue, sans supprimer le corps visible utile.
- [ ] Relier la présence visuelle aux scénarios d’occupants sans compter deux fois leur masse dans le FDM.
- [ ] Contrôler vues avant/arrière/extérieures, commandes mobiles et performances ; illustrer chaque pièce et mettre à jour les aperçus.

**Critère :** deux silhouettes crédibles, tenue bleue devant et verte derrière, détails sourcés, aucune obstruction de la vue pilote ou double comptage de masse. Les dimensions humaines resteront des choix de modèle, pas des mesures de pilotes réels.

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

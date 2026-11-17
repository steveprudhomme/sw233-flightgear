# Feuille de route — Schweizer SGS 2-33

Mise à jour : **17 novembre 2026**. Les horizons expriment un ordre de travail, pas des dates promises.

## 1. Vision et périmètre

Construire pour FlightGear un Schweizer SGS 2-33 aux couleurs des Cadets de l’aviation royale du Canada, avec un cockpit crédible et un atelier permettant de le reconstruire pas à pas. Chaque comportement revendiqué doit être relié à une référence ou à un essai reproductible.

Le projet est un prototype de simulation, pas un appareil d’entraînement certifié. Il ne fournit pas de consignes de vol réel, ne copie pas de ressources tierces sans droits établis et ne promet pas de variantes supplémentaires avant validation du modèle de référence. Licence actuelle : **GPL-3.0-only**.

## 2. État actuel

| Domaine | État vérifié | Limite principale |
|---|---|---|
| Vol et décor | Démonstrations natives à CYJN, aérofreins et glissade | Polaire et enveloppe réelle non validées |
| Cockpit | Anémomètre, altimètre, variomètre et compas animés ; bancs publiés | Aspect encore schématique ; COM1 réglable sans audio validé, largage décoratif |
| Masse et repères | Calculs comparés à FlightGear ; transport du moment testé | Pesée de C-FYLP et référence historique des coefficients inconnues |
| Profondeur | ±23° et deux parties mobiles vérifiées | Charnière de maquette approximative |
| Documentation | Dix-huit fiches enrichies ; atlas historique de 49 objets et compléments par pièce, sources, captures et reconstruction automatique | Relecture autonome par un débutant encore attendue |
| Qualité | 24 tests réussis | Ne constituent pas une certification du modèle |

**Lecture des statuts :** terminé = critère vérifié et preuve publiée ; en cours = réalisation autorisée ; à faire = proposé ; dépendance = donnée ou décision nécessaire.

## 3. Prochaine version — v0.2.0, commandes et installation

Objectif : un petit incrément utilisable et vérifiable. Aucune date ferme. Chaque lot peut être publié séparément en préversion.

| Priorité / lot | Statut | Critère de réussite | Responsable |
|---|---|---|---|
| P1 · **VIS-01d : dossier de références dimensionnelles** | Terminé — dossier documentaire | Sources examinées, données admissibles et manquantes tracées, fiche de relevé illustrée | Mainteneur |
| P1 · **VIS-01e : relevés et configuration de référence** | Préparation terminée — mesures physiques attendues | Numéro de série/configuration, deux vues latérales, cotes indépendantes, sections et incertitudes ; revue avant correction 3D | Contributeur recherché |
| P1 · **VIS-01c : contrôle des proportions** | Terminé — diagnostic | Tableau de repères normalisés, incertitudes, comparaison illustrée et décision motivée pour chaque correction | Mainteneur |
| P1 · **VIS-01b : panneaux de verrière et contours de porte** | Terminé | Contours comparés aux références, panneaux identifiables, raccords fermés et vue pilote préservée ; atlas et captures actualisés | Mainteneur |
| P1 · **VIS-01a : enveloppe du cockpit et atlas des pièces** | Terminé | Flancs et raccords sans trous involontaires, comparaison des références et vues natives avant/après, atlas de chaque objet du maillage, tutoriel et aperçus actualisés | Mainteneur |
| P1 · **AUD-01b : profondeur ±23°** | Terminé | FDM, animation et butées cohérents ; comparaison avant/après à même chargement ; tutoriel illustré | Mainteneur, revue recherchée |
| P1 · **AUD-01c : occupants dans le menu** | Terminé pour chiffres du haut | Saisie manuelle 200.125 confirmée ; masse effective et CG relevés ; restauration décimale corrigée | À attribuer |
| P2 · **AUD-01d : pavé numérique** | À investiguer | Comparer champ standard et SW233, Verr Num activé, puis disposition et événements ; cause et correction à établir | À attribuer |
| P2 · **AUD-02a : paquet et lanceur Windows** | Terminé | Paquet autonome contrôlé, lancement depuis un chemin avec espaces, cockpit et menu vérifiés | Mainteneur |
| P2 · **AUD-02b : présentation dans le sélecteur** | Terminé | Métadonnées sourcées, miniature native, aperçu et fiche visibles dans le lanceur | Mainteneur |
| P2 · **AUD-02c : validation Linux** | À faire | Installation et lancement natifs Linux, preuves distinctes de Windows | À attribuer |
| P2 · **AUD-13 / AUD-14 : contrôles et publication** | À faire, après AUD-02 | ZIP construit sur tag, testé avant publication ; provenance et empreinte jointes | À attribuer |

**Dernier lot réalisé :** [AUD-01c et complément clavier](docs/planification/aud-01c-clavier.md). Le protocole est commité avant le code. Un lot n’est clos que lorsque ses tests, captures pertinentes, limites et documents sont publiés.

Lot réalisé : **AUD-01c**, [protocole en huit étapes](docs/planification/aud-01c-occupants.md), préparé avant réalisation.

Preuves AUD-01c : [fiche 11](docs/construction/11-occupants.md). Le [complément clavier](docs/planification/aud-01c-clavier.md) confirme la saisie par les chiffres du haut et corrige la restauration décimale. Le pavé numérique reste suivi séparément sous AUD-01d.

Dernier lot réalisé : [AUD-02a, protocole installation et lancement](docs/planification/aud-02a-installation.md). AUD-02c reste distinct : un contrôle Windows ne vaut pas un essai Linux.

Preuves AUD-02a : [fiche 12 illustrée](docs/construction/12-installation.md), 19 tests et contrôle natif du paquet déplacé.

Dernier lot réalisé : [AUD-02b, protocole du sélecteur](docs/planification/aud-02b-selecteur.md). Preuves : [fiche 13](docs/construction/13-selecteur.md), miniature et aperçu visibles dans FlightGear 2024.1.7, 21 tests et reconstruction. Prochain lot proposé : AUD-02c, à condition de disposer d’un environnement Linux natif.

## 4. Moyen terme — après v0.2.0

Horizon indicatif : plusieurs cycles de développement ; les données disponibles déterminent l’ordre.

| Objectif | Suivi | Dépendance / critère de réussite |
|---|---|---|
| Référence physique et polaire | AUD-01a, AUD-03, AUD-09 | Identifier pesée et repères, puis comparer plusieurs vitesses et masses aux sources ; garder les échecs d’essai |
| Cockpit plus photographique | VIS-01, AUD-11 | Mesures C-FYLP, cadrage fixe, textes lisibles, verre sous deux éclairages ; calage d’altimètre visible et bouton testé |
| Silhouette puis livrée actuelle des Cadets | VIS-02 | Un appareil identifié et daté, vues des deux flancs/dessus/dessous, droits documentés ; lettrage sans miroir et aérofreins raccordés |
| Contacts, frein, treuil et remorquage | AUD-06, AUD-05 | Contacts cohérents ; essais natifs d’attache, lancement et largage pour chaque mode |
| Aide embarquée et check-lists | AUD-10 | Procédures sourcées ; uniquement fonctions réellement disponibles ; commandes repérables dans le cockpit |
| Outillage plus simple à maintenir | AUD-07, AUD-08, AUD-12 | Extraire les répétitions utiles ; vérifier pause/reinit/restauration sans modifier les résultats des bancs |
| Tutoriel éprouvé par un débutant | AUD-16 | Reconstruction et installation sans aide orale ; hésitations corrigées, illustrations légendées |

VIS-01 conserve la disposition C-FYLP et des aiguilles indépendantes des textures. VIS-02 commence par les formes et le dossier photographique, puis le dépliage et la peinture ; la livrée jaune actuelle reste une livrée de développement.

## 5. Long terme — ambitions à confirmer

| Objectif | Suivi | Condition préalable |
|---|---|---|
| Vol lent, décrochage et autorotation documentés | AUD-04 | Données et stabilité de base validées ; protocoles et limites explicites |
| Poste arrière et autres variantes | VIS-03 | Poste avant validé et références propres à chaque variante |
| Accueil anglophone | AUD-17 | Contributeur chargé de maintenir les traductions et exemples |
| Éventuelle candidature au hangar officiel | AUD-15 | Décision du mainteneur, règles d’admission et droits examinés ; aucun changement automatique de licence |

## 6. Travaux terminés et preuves

| Résultat | Preuve |
|---|---|
| Démonstration à CYJN, glissade et aérofreins | [Validation et film](docs/validation.md) |
| Cadrans et compas, lectures et bancs | [Tutoriel des essais](docs/construction/07-essais.md) |
| Diagnostic de masse et réserve de profondeur | [Fiche 8](docs/construction/08-centrage.md) |
| Translation des repères et transport du moment | [Fiche 9](docs/construction/09-reperes.md) — identification aéronautique AUD-01a encore ouverte |

| Profondeur ±23°, butées et animation | [Fiche 10 et captures natives](docs/construction/10-profondeur.md) |

<a id="audits-externes"></a>

## 7. Tickets, décisions et détails techniques

- [Gestionnaire de tickets GitHub](https://github.com/steveprudhomme/sw233-flightgear/issues) : proposer un lot avec son identifiant (par exemple AUD-01b), sa preuve attendue et son responsable.
- [Jalons GitHub](https://github.com/steveprudhomme/sw233-flightgear/milestones) : les horizons de ce document ne sont pas encore annoncés comme des jalons GitHub synchronisés.
- [Backlog détaillé des 17 recommandations](docs/planification/backlog-audits.md) : critères et dépendances, sans duplication du statut courant.
- [Analyse des audits et limites de leurs conclusions](docs/references/audits-2026-11-11.md).
- [Archive des anciens protocoles](docs/planification/archive-roadmap-2026-11-12.md) : mémoire du travail, **pas une seconde feuille de route active**.

Aucun numéro de ticket n’est inventé : les identifiants AUD/VIS sont documentaires. Les futurs tickets et PR reprendront ces identifiants et seront liés ici après création. Les choix importants feront l’objet d’un document de décision avant réalisation.

## 8. Comment participer et maintenir ce document ?

Nous recherchons : des pilotes connaissant le 2-33 pour la revue des essais, des propriétaires disposant de fiches de pesée et mesures, des artistes 3D/texture, des testeurs Linux/Windows et des lecteurs débutants. Voir [CONTRIBUTING](CONTRIBUTING.md) et [MAINTAINERS](MAINTAINERS.md), puis proposer sa contribution dans un ticket.

À chaque lot : préparer et commiter les sous-étapes ; réaliser et tester ; documenter avec des images natives pour les changements visibles ; actualiser cette synthèse et CHANGELOG. Réexaminer les priorités à chaque publication et lorsqu’une nouvelle référence change les hypothèses. Une annonce suit les résultats, jamais l’inverse.

Lot réalisé : [VIS-01a — enveloppe du cockpit et atlas pédagogique](docs/planification/vis-01a-enveloppe.md). Priorité donnée à la correction géométrique demandée ; AUD-02c Linux reste à faire.

Preuves VIS-01a : [fiche 14](docs/construction/14-enveloppe.md) et [atlas](docs/construction/atlas-pieces.md). Suite VIS-01 : obtenir des cotes fiables du vitrage, de la porte et des sections ; affiner les contours avant les matériaux photographiques.

Lot réalisé : [VIS-01b — panneaux et contours](docs/planification/vis-01b-panneaux.md).

Preuves VIS-01b : [fiche 15](docs/construction/15-panneaux.md). Reste à obtenir des vues dimensionnées des deux flancs avant de figer les contours de porte et leurs équipements ; symétrie actuelle provisoire.

Lot réalisé : [VIS-01c — contrôle des proportions](docs/planification/vis-01c-proportions.md).

VIS-01c : trois repères quantifiés ; écarts au dessin de 0,30 à 0,37 m, sans correction faute de référence dimensionnelle suffisante. [Fiche 16 et décisions](docs/construction/16-proportions.md).

**VIS-01e — relevés physiques (dépendance)** : identifier un appareil et recueillir deux profils, les cotes des montants, les sections du cockpit et les limites de porte ; contrôler datum et droits des références. Critère : au moins deux dimensions indépendantes dans le même plan, correspondances vérifiées et incertitudes documentées avant déplacement des stations.

Lot réalisé : [VIS-01d — références dimensionnelles](docs/planification/vis-01d-references.md).

Preuves VIS-01d : [fiche 17 illustrée](docs/construction/17-references.md), [registre dimensionnel](docs/references/dimensions-cockpit.md) et [formulaire](docs/references/releve-cockpit.md). Aucune correction de forme ni mise à jour d’aperçu justifiée par les seules données trouvées.

VIS-01e : [sous-étapes de collecte et comparaison](docs/planification/vis-01e-releves.md). Préremplir uniquement les informations attestées ; produire des vues cotées du modèle pour guider le relevé, sans les confondre avec des mesures réelles. Le lot reste ouvert tant que les relevés physiques manquent.

État VIS-01e : pas d’accès à un appareil réel, confirmé le 15 novembre 2026. [Fiche 18](docs/construction/18-releves.md) : dix pièces et trente projections, limites du modèle et [fiche C-FYLP préremplie](docs/references/releve-cfylp.md). Collecte non terminée ; aucune correction géométrique revendiquée. En parallèle, un prochain lot de détails de surface du tableau peut être proposé sous VIS-01, avec estimations déclarées, sans dépendre des dimensions extérieures.

## Lot actif VIS-01f — finition du tableau

Plan : [textures et comparaison native](docs/planification/vis-01f-tableau.md). Améliorer peinture, vis, bordures et plaques à partir de C-FYLP, avec dessins originaux et dimensions estimées explicites. Critère : comparaison native avant/après au même cadrage sous deux éclairages, instruments préservés, tutoriel illustré et paquet actualisé. Les relevés physiques VIS-01e restent attendus.

VIS-01f : textures réalisées et comparaison native sous deux orientations publiée dans la [fiche 6, section H](docs/construction/06-peinture.md#h--finition-du-tableau--vis-01f). Lot encore ouvert : refaire les captures du banc d’anémomètre et l’aperçu général lorsque FlightGear est disponible. Cadrans et animations inchangés, vérifiés octet par octet.

Reprise VIS-01f du 16 novembre : banc avec rejet des images vides, quatre lectures natives, cockpit complet et aperçu du paquet. [Complément préalable](docs/planification/vis-01f-tableau.md).

VIS-01f terminé : quatre lectures natives, cockpit complet et aperçu du paquet. Preuves : fiche 6, section I. Les anciens paragraphes de reprise décrivent les essais précédents ; les captures manquantes sont maintenant obtenues.

## VIS-01g — aérateur central en relief (en cours)

Plan préalable : conserver le centre et le diamètre de maquette, construire bague/conduit/volet fixes avec profondeurs estimées ; retirer le dessin plat ; synchroniser les recettes ; produire les vues par pièce ; vérifier face/biais et deux orientations dans FlightGear ; actualiser tutoriel, aperçu et paquet. Critère : relief visible sans masquer les cadrans, reconstruction vérifiée. Aucune commande de ventilation fonctionnelle revendiquée.

VIS-01g terminé le 16 novembre 2026 : quatre pièces, grille peinte retirée, recettes synchronisées, captures face/biais et deux caps, aperçu actualisé. Dimensions estimées et volet fixe. Preuves : fiche 2, section finale.

## VIS-01h — relief de l'anémomètre (en cours)

Sous-étapes préalables : conserver le cadran et l'aiguille ; ajouter une bague ouverte et quatre fixations, profondeurs estimées ; supprimer seulement leurs doublons peints ; synchroniser la recette ; contrôler le dégagement radial et les lectures dans FlightGear ; illustrer les pièces et vues face/biais ; vérifier reconstruction et paquet puis publier. Ne pas ajouter une vitre opaque ni modifier les graduations. Critère : quatre lectures lisibles et aucun masquage depuis les vues contrôlées.

VIS-01h terminé : bague ouverte, quatre fixations et retrait du doublon peint ; quatre lectures natives et vue de biais vérifiées. Recettes, pièces illustrées et aperçu actualisés. Dimensions de profondeur estimées ; autres cadrans inchangés.

## VIS-01i — relief de l'altimètre (en cours)

Sous-étapes préalables : conserver les deux aiguilles et le bouton ; construire une bague ouverte, avec fixations hors du bouton en bas à gauche ; supprimer les doublons peints ; documenter les dimensions estimées et illustrer les pièces ; tester cinq altitudes et trois pressions sur session dédiée FDM null, contrôler face/biais et dégagement du bouton ; vérifier reconstruction et paquet, mettre à jour les MD et publier. Ne pas confondre variation de pression par le banc et clic manuel sur le bouton.

VIS-01i : géométrie et lectures natives réalisées, cinq altitudes et trois calages illustrés. Reste à vérifier le clic manuel sur le bouton de calage ; le banc de pression ne vaut pas essai de souris. Profondeurs estimées, fenêtre de pression toujours non chiffrée.

## VIS-01i — contrôle souris du calage

Protocole préalable : lancer le dernier paquet en session dédiée FDM null ; relever calage et indication ; cadrer le bouton de face ; essayer les deux sens par souris et relever les deltas ; répéter de biais ; conserver captures et valeurs, restaurer le calage ; documenter les gestes réellement efficaces et toute limite. Corriger uniquement si une cause est identifiée, puis refaire les essais et synchroniser le tutoriel avant publication.

VIS-01i clos : contrôle souris réussi de face et de biais par cliquer-glisser horizontal, dans les deux sens ; retour à 29,92 inHg. Molette testée sans effet. Preuves : fiche 6, section J, publication calage-26. Les mentions antérieures « clic à vérifier » décrivent désormais un état historique.

## VIS-01j — relief du variomètre (terminé)

Sous-étapes préalables : comparer la disposition existante à la photo C-FYLP ; conserver le centre, le cadran et son aiguille ; ajouter une bague ouverte et des fixations aux dimensions de maquette explicites ; retirer uniquement les doublons peints ; synchroniser les recettes du tutoriel et illustrer chaque nouvelle pièce ; contrôler dans FlightGear les indications négative, nulle et positive, de face et de biais ; distinguer essai d'affichage à entrées imposées et validation du vol ; vérifier reconstruction, actualiser l'aperçu, les MD et publier le paquet. Critère : graduations et aiguille lisibles dans les vues testées, aucune modification de l'étalonnage, preuves natives et hypothèses documentées.

VIS-01j terminé : trois objets ajoutés, doublons peints retirés, sept indications natives contrôlées de face et de biais. Les 59 objets antérieurs et les trois textures de cadran restent identiques. [Tutoriel illustré, fiche 6 section K](docs/construction/06-peinture.md#k--variomètre-en-relief--vérifier-et-comparer), vues par pièce, aperçu et paquet vario-bague-27. Profondeurs estimées ; essais d’affichage, sans nouvelle validation du vol.

## VIS-01k — fenêtre de calage de l’altimètre (terminé)

Plan préalable : examiner la photo C-FYLP et les exemples XML locaux FlightGear ; distinguer l’unité attestée par la commande du modèle de l’unité illisible sur la photo ; créer un affichage lisible lié directement à setting-inhg, sans deuxième valeur de calage ; conserver bouton et aiguilles ; vérifier plusieurs valeurs, un passage de dizaine et les limites de la commande ; contrôler de face et de biais, puis les glissements dans les deux sens ; illustrer la construction et les essais ; synchroniser les recettes, actualiser MD, description et aperçu, vérifier et publier le paquet. Critère : valeur affichée à deux décimales cohérente avec le réglage, unité explicite, aucune prétention de reproduire un mécanisme non documenté. Les dimensions de fenêtre restent estimées.

VIS-01k terminé : affichage direct en inHg à deux décimales ; huit valeurs sous deux vues, quatre glissements et retour à 29,92 vérifiés. [Tutoriel illustré](docs/construction/06-peinture.md#l--fenêtre-de-calage-de-laltimètre). Fenêtre horizontale simplifiée, dimensions estimées ; mécanisme et unité du véritable instrument C-FYLP à confirmer par une référence lisible.

## VIS-01l — façade de radio en relief (terminé)

Plan préalable : comparer la photo C-FYLP à la façade peinte ; conserver le centre et l'encombrement de maquette pour dégager l'altimètre ; construire contour, façade, écran et boutons fixes avec profondeurs estimées ; créer une texture originale sans fréquence fictive ni inscription illisible ; retirer le dessin plat en double ; illustrer les pièces et synchroniser les recettes ; contrôler face/biais et voisinage dans FlightGear ; actualiser tutoriel, MD, aperçu et paquet. Critère : relief visible, séparation conservée avec l'altimètre et les cartes, reconstruction vérifiée. Les commandes et fréquences radio fonctionnelles feront l'objet d'un lot ultérieur.

VIS-01l terminé : huit pièces, texture originale et quatre vues natives comparées ; 62 objets antérieurs préservés, dégagement de maquette d’environ 5 mm avec la bague d’altimètre. [Tutoriel illustré](docs/construction/06-peinture.md#m--façade-de-radio-en-relief), description et aperçu actualisés. Radio non fonctionnelle, dimensions estimées.

Suite radio à planifier : identifier les commandes sur une référence lisible, définir les fonctions prises en charge dans FlightGear, relier affichage et boutons puis vérifier les fréquences et les limites. Critère futur : valeur affichée cohérente avec la propriété active, sans fonction ou marquage supposé.

## VIS-01m — réglage radio COM fonctionnel (terminé)

Plan préalable : examiner les références et exemples FlightGear ; identifier le modèle réel si les preuves le permettent, sinon annoncer une commande générique ; relier l'écran à la fréquence COM1 active ; définir et documenter pas, plage et actions des deux boutons ; préserver les canaux valides aux limites ; tester valeurs, changements externes et souris de face/biais ; documenter avec captures natives et recettes reproductibles ; actualiser MD, description, aperçu et paquet. Critère : affichage et propriété active concordants, boutons efficaces dans les deux sens et limites vérifiées. Aucune réception audio, émission réseau ou fidélité à une radio réelle ne sera revendiquée sans essai correspondant.

VIS-01m terminé : COM1 active à trois décimales, commandes ±1 MHz / ±25 kHz, butées et refus hors grille ; treize cas natifs et huit clics vérifiés, fréquences restaurées. [Tutoriel illustré](docs/construction/06-peinture.md#n--régler-la-fréquence-com1). Identification réelle, alimentation, audio, mémoires et éventuel support 8,33 kHz restent à définir dans des lots séparés.

## VIS-01n — finition du compas (terminé)

Plan préalable :

- [x] Comparer le boîtier et la fenêtre aux photos C-FYLP ; séparer proportions photographiques et profondeurs estimées. Examiner les essais historiques avant de refaire un mécanisme déjà fonctionnel.
- [x] Conserver la rose animée et sa propriété de cap indiqué ; améliorer le contour, les fixations et le repère seulement si la comparaison le justifie.
- [x] Synchroniser la recette de construction ; illustrer chaque pièce modifiée et expliquer les dimensions et choix sans les présenter comme des cotes constructeur.
- [x] Comparer avant/après dans FlightGear de face et de biais ; contrôler N/E/S/W, les caps intermédiaires et le passage 359/0/1 degrés.
- [x] Vérifier le défilement en virage avec l’instrument actif ; distinguer ce contrôle des entrées imposées du banc.
- [x] Vérifier reconstruction et absence de modification des autres instruments ; actualiser tutoriel, MD, aperçu et publication GitHub.

Critères de réussite : rose et repère lisibles dans les vues contrôlées, sens correct aux caps testés, aucune régression des autres instruments, preuves natives et hypothèses documentées. Les erreurs du compas réel ne seront pas déclarées validées par un simple contrôle visuel.

Complément VIS-01n identifié pendant les vérifications : actualiser les deux tests de résolution des objets. Ils supposent encore que tous les objets animés viennent du maillage et que toute animation porte une propriété ; les textes XML et actions radio des lots précédents rendent ces hypothèses obsolètes. Vérifier explicitement les textes, les objets du maillage et les actions, sans retirer les contrôles de résolution.

VIS-01n terminé : boîtier arrondi, joint et vis en relief ; 18 lectures natives, 880 captures d’un vol de 145,1 s et deux passages du nord contrôlés. Rose et animations conservées, 66 objets inchangés, 24 tests réussis et reconstruction vérifiée. [Construction par pièce](docs/construction/02-maillage.md#o--comprendre-la-finition-du-compas-pièce-par-pièce), [essais illustrés](docs/construction/06-peinture.md#o--finition-du-compas). Dimensions estimées ; caractères et vitre encore simplifiés.

## VIS-01o — caractères et graduations du compas (terminé)

- [x] Relire les références et conserver uniquement les inscriptions déjà justifiées ; distinguer dessin original et typographie exacte inconnue.
- [x] Remplacer les petits polygones des caractères par une bande originale anticrénelée ; expliquer pixels, échelle, raccord et coordonnées de texture avec une recette reproductible.
- [x] Conserver le boîtier, le repère et l’animation ; vérifier que seule la rose change et que les autres textures restent identiques.
- [x] Vérifier N/E/S/W, caps intermédiaires et 359/0/1 dans FlightGear ; comparer avant/après, vue pilote, gros plan et biais sous deux éclairages.
- [x] Illustrer la bande, la pièce et les essais dans un tutoriel accessible à 10 ans ; synchroniser les recettes et les MD.
- [x] Vérifier reconstruction, tests et paquet ; actualiser l’aperçu puis publier sources et captures sur GitHub.

Critère : caractères plus nets sans inversion, décalage ni rupture au raccord ; lectures centrales préservées dans les vues testées. Aucune typographie constructeur ni fidélité photographique complète revendiquée.

VIS-01o terminé : bande lissée, rose réduite de 334 à 72 faces, 71 autres objets et cinq textures conservés. Quarante-huit lectures statiques examinées, vues pilote sous deux éclairages ; 24 tests et reconstruction vérifiés. [Tutoriel pour débutant](docs/construction/06-peinture.md#p--des-lettres-plus-nettes-pour-le-compas), avec exercice en papier, calculs et captures. Typographie et luminosité estimées ; validation pédagogique autonome encore attendue.

## VIS-01p — plaquettes et checklists FR / EN (en cours)

- [ ] Comparer les inscriptions photographiées et les rappels actuels ; distinguer reproduction, traduction du projet et procédures adaptées à la simulation.
- [ ] Créer des textes français et anglais correspondants ; vérifier les unités et conserver les limites explicites du prototype.
- [ ] Créer deux jeux de plaquettes originaux sélectionnés par une propriété de langue unique, sans modifier les instruments.
- [ ] Ajouter au menu SW233 le choix Français / English et l’accès aux checklists ; choisir un raccourci sans conflit dans la configuration installée.
- [ ] Actualiser les checklists natives lors du changement, y compris si leur fenêtre est ouverte ; définir l’état initial et le comportement des coches.
- [ ] Tester dans FlightGear les deux langues, le menu, le raccourci, les bascules répétées et les quatre checklists ; conserver captures et relevés.
- [ ] Documenter pour un enfant de 10 ans : textes, textures, interrupteur de langue, essais et dépannage illustrés ; synchroniser les recettes et MD, vérifier le paquet puis publier sur GitHub.

Critères : plaquettes et checklists utilisent la même langue sans redémarrer ; textes non tronqués en gros plan, touches de pilotage conservées, aucun changement du FDM. Le choix concerne SW233 uniquement, pas la langue générale de FlightGear. Les traductions et rappels de simulation ne sont pas des procédures réelles approuvées.

### Complément VIS-01p — moyens mnémotechniques des Cadets

- [ ] Relever les mots et leur ordre dans les IEA du 2-33, avec édition et pages ; le manuel général 242 renvoie aux IEA et ne fournit pas ces listes.
- [ ] Confirmer séparément les mots français enseignés : ne pas présenter une traduction libre comme un acronyme officiel.
- [ ] Restaurer tous les éléments des séquences attestées ; ne pas supprimer des mots pour les faire entrer sur une plaquette.
- [ ] Dessiner en rouge sombre la première lettre de chaque élément mnémotechnique ; conserver les titres et le reste du texte en noir, ainsi que les accents.
- [ ] Adapter la taille et l'espacement au nombre de lignes ; vérifier la lisibilité des deux langues dans les textures puis dans FlightGear.
- [ ] Illustrer et expliquer dans le tutoriel la distinction entre source, traduction à confirmer et rappel de simulation ; synchroniser la recette.

Critère complémentaire : mots, ordre et initiales correspondent à une source identifiée par langue. Le rouge est une aide visuelle du projet, pas une couleur attribuée sans preuve aux plaquettes réelles. La validation française reste ouverte jusqu'à réception d'une référence probante.


Point d'étape VIS-01p : source anglaise contrôlée (IEA 2017, PDF 28/35),
initiales rouges et mise en page à 4–8 rubriques réalisées ; reconstruction
complète du tutoriel vérifiée. La formulation mnémotechnique française et
les nouvelles captures natives restent à valider. Le lot n'est pas terminé.


### VIS-01p — clarification reçue le 17 novembre 2026

- [ ] Conserver BCISTRSC, AAAT, SWARTSC et ASCOT dans les deux langues ; utiliser les traductions explicatives fournies par l'utilisateur sans les présenter comme une transcription des IEA françaises.
- [ ] Préfixer chaque rubrique française par sa lettre anglaise (exemple : B — Lest) et colorer cette lettre en rouge ; conserver toutes les rubriques et leur ordre.
- [ ] Synchroniser les listes, les textures et le tutoriel ; vérifier les correspondances FR/EN et le rendu des accents.
- [ ] Ajouter un lot séparé pour GASP/VEST et GPAS/PTES : retrouver les pages du manuel bilingue 2018, vérifier les mots et leur ordre, définir les limites du remorquage simulé, puis documenter les urgences séparément des procédures normales.
- [ ] Recenser séparément les inspections journalière, extérieure limitée, d'accrochage, après assemblage et de transport ; définir celles qui ont un sens dans le prototype avant toute implémentation.

Critère : aucune initiale française artificielle ne remplace le mot-check anglais. Les références d'urgence citées sans lien/page restent des pistes à vérifier, pas des procédures déjà validées ou intégrées.


Résultat du complément français : les quatre listes et cartes emploient
BCISTRSC / AAAT / SWARTSC / ASCOT avec explications françaises attribuées au
responsable du projet. 25 tests et reconstruction complète réussis.
Deux captures natives statiques confirment le rendu des lettres rouges.

- [ ] VIS-01p, lisibilité : corriger le masquage des cartes de droite par la
  bague de l'anémomètre ; comparer disposition et profondeurs aux références,
  puis contrôler toutes les lignes depuis la vue pilote. Les captures du
  17 novembre montrent le défaut ; ne pas déclarer la lisibilité complète.

Les urgences et inspections nouvellement recensées restent planifiées, sans
ajout de procédure automatique ni de simulation du câble dans ce lot.


## VIS-01q — dégager les cartes de droite (en cours)

- [ ] Mesurer les emprises dans la recette : cartes, bague d'anémomètre, aérateur, compas et bord du tableau ; comparer la disposition à la photo C-FYLP.
- [ ] Distinguer recouvrement géométrique et effet de perspective ; conserver l'étalonnage et l'animation de l'anémomètre.
- [ ] Choisir un déplacement limité des deux cartes et de leurs supports peints ; garder leurs dimensions et tous les mots-checks, puis vérifier les dégagements calculés.
- [ ] Synchroniser les géométries française/anglaise, la peinture et les recettes du tutoriel.
- [ ] Contrôler les deux langues dans FlightGear : vue pilote, gros plan identique avant/après et vue oblique ; publier les captures natives et les limites observées.
- [ ] Expliquer les axes, le calcul des bords et le choix des positions dans un tutoriel pour débutant ; ajouter des illustrations avant/après.
- [ ] Vérifier les objets préservés, les tests, la reconstruction et le paquet ; actualiser MD, état de la feuille de route et GitHub.

Critère : les huit cartes (quatre par langue) sont complètes dans les vues contrôlées, sans recouvrement avec les instruments voisins ni sortie du tableau. Les nouvelles positions sont des choix de maquette, pas des cotes mesurées sur un planeur réel.

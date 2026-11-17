# Feuille de route — Schweizer SGS 2-33

Mise à jour : **15 novembre 2026**. Les horizons expriment un ordre de travail, pas des dates promises.

## 1. Vision et périmètre

Construire pour FlightGear un Schweizer SGS 2-33 aux couleurs des Cadets de l’aviation royale du Canada, avec un cockpit crédible et un atelier permettant de le reconstruire pas à pas. Chaque comportement revendiqué doit être relié à une référence ou à un essai reproductible.

Le projet est un prototype de simulation, pas un appareil d’entraînement certifié. Il ne fournit pas de consignes de vol réel, ne copie pas de ressources tierces sans droits établis et ne promet pas de variantes supplémentaires avant validation du modèle de référence. Licence actuelle : **GPL-3.0-only**.

## 2. État actuel

| Domaine | État vérifié | Limite principale |
|---|---|---|
| Vol et décor | Démonstrations natives à CYJN, aérofreins et glissade | Polaire et enveloppe réelle non validées |
| Cockpit | Anémomètre, altimètre, variomètre et compas animés ; bancs publiés | Aspect encore schématique ; radio et largage décoratifs |
| Masse et repères | Calculs comparés à FlightGear ; transport du moment testé | Pesée de C-FYLP et référence historique des coefficients inconnues |
| Profondeur | ±23° et deux parties mobiles vérifiées | Charnière de maquette approximative |
| Documentation | Dix-huit fiches et atlas des 49 objets, sources, captures et reconstruction automatique | Relecture autonome par un débutant encore attendue |
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

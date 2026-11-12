# Feuille de route — Schweizer SGS 2-33

Mise à jour : **12 novembre 2026**. Les horizons expriment un ordre de travail, pas des dates promises.

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
| Documentation | Dix fiches, sources, captures et reconstruction automatique | Relecture autonome par un débutant encore attendue |
| Qualité | 15 tests réussis | Ne constituent pas une certification du modèle |

**Lecture des statuts :** terminé = critère vérifié et preuve publiée ; en cours = réalisation autorisée ; à faire = proposé ; dépendance = donnée ou décision nécessaire.

## 3. Prochaine version — v0.2.0, commandes et installation

Objectif : un petit incrément utilisable et vérifiable. Aucune date ferme. Chaque lot peut être publié séparément en préversion.

| Priorité / lot | Statut | Critère de réussite | Responsable |
|---|---|---|---|
| P1 · **AUD-01b : profondeur ±23°** | Terminé | FDM, animation et butées cohérents ; comparaison avant/après à même chargement ; tutoriel illustré | Mainteneur, revue recherchée |
| P1 · **AUD-01c : occupants dans le menu** | À faire | Deux masses modifiables, CG recalculé, restauration et captures solo/biplace | À attribuer |
| P2 · **AUD-02 : paquet et lanceur** | À faire | Installation propre sous Windows et Linux ; chemins, textures, miniature et métadonnées vérifiés | À attribuer |
| P2 · **AUD-13 / AUD-14 : contrôles et publication** | À faire, après AUD-02 | ZIP construit sur tag, testé avant publication ; provenance et empreinte jointes | À attribuer |

**Dernier lot réalisé :** [protocole AUD-01b en huit étapes](docs/planification/aud-01b-profondeur.md). Le protocole est commité avant le code. Un lot n’est clos que lorsque ses tests, captures pertinentes, limites et documents sont publiés.

Prochain lot proposé : **AUD-01c**, commandes de masse des occupants. Ses sous-étapes seront précisées et commitées avant sa réalisation.

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

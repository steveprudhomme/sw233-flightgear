# Schweizer SGS 2-33 aux couleurs Cadets de l’aviation royale du Canada

Construire une reproduction documentée, testable et progressivement fidèle du
planeur biplace Schweizer **SGS 2-33**. SW233 est le nom du projet, pas la
désignation constructeur. La livrée actuelle des Cadets est un objectif : les anciennes vidéos montrent la livrée jaune de développement ; les nouvelles captures montrent la variante provisoire C-FYLP.

Projet **libre et open source**, sous [licence GPL-3.0-only](LICENSE.md). Les anciennes
ressources FlightGear/JSBSim ne sont pas redistribuées ni relicenciées ici. Les versions déjà diffusées sous MIT conservent leur [notice historique](LICENSES/MIT-historical.txt).

**Revue visuelle après le lot40 :** le rendu reste trop simplifié. La reprise des courbes, de la verrière, des ailes et de la livrée est prioritaire dans [VIS-05](ROADMAP.md#priorité-actuelle--vis-05--reprise-de-la-fidélité-visuelle). [Analyse des dix nouvelles références](docs/references/analyse-exterieur-lot-01.md).

[Premier relevé du nez, de la coque et de la verrière, avec comparaisons FlightGear](docs/construction/23-releves-avant.md).

## Ouverture de la verrière — 0.1.0-alpha.2

La verrière avant s’ouvre au sol avec le menu **SW233 → Verrière / Canopy**
ou la poignée rouge. La checklist affiche son état en français et en anglais.
Le passager arrière reste sous l’aile. Le vitrage fixe est dégagé entre les ailes.

[Tutoriel26 illustré](docs/construction/26-ouverture-verriere.md) ·
[Paquet et preuves](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/v0.1.0-alpha.2) ·
[Bilan des essais et limites](docs/validation/verriere-lot44.md).

66 tests passent. La course de 100 degrés reste estimée et la porte arrière reste fixe.
La réinitialisation complète ferme FlightGear sur la machine d’essai, également avec alpha.1.
Relancer le simulateur au lieu d’utiliser cette commande en attendant le diagnostic.

## Dimensions et fuselage — alpha.4 en préparation

Dos arrière rectiligne, corde maximale de 1,524 m et empennage horizontal de 2,3622 m, selon le manuel fourni.
[Atelier29 illustré](docs/construction/29-dimensions-et-fuselage.md) · [Essais et limites](docs/validation/fuselage-lot48.md).
75 tests et 14 contrôles natifs réussissent. Le [lot51](docs/construction/30-reperes-et-train.md) recale les roues visibles et documente la hauteur encore non résolue.
La silhouette complète reste à faire accepter.

## Finition du nez et de la verrière — lot43

Nez plus plein, capot bombé, flancs rehaussés et raccord arrière prolongé sous l'aile.
Cadres bleus, joints, fixations et poignée fixe ajoutés ; mât et ficelle raccordés au
nouveau capot. [Tutoriel25 illustré](docs/construction/25-finitions-avant.md) ·
[Paquet et comparaisons](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/v0.1.0-alpha.1).
Dans le lot43, 63 tests passaient ; la verrière était encore fixe et la
livrée C-FYLP reste provisoire. La revue de ressemblance reste ouverte.

![Profil du lot43 dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.1/apres-nez-profil.png)

## Reconstruction des formes avant — lot42

Nez et coque avant à sections plus fines, pare-brise bombé, cadres raccordés et
lissage des surfaces. [Atelier24, pas à pas avec chaque pièce illustrée](docs/construction/24-formes-avant.md).
[Paquet et comparaisons FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/formes-42).
Les formes restent estimées ; la livrée et l'ouverture de verrière restent à reprendre.

![Nez et verrière après reconstruction](https://github.com/steveprudhomme/sw233-flightgear/releases/download/formes-42/apres-nez-oblique.png)

## Réalisme du cockpit et suite du projet

Le prototype comprend maintenant une livrée jaune/bleu **C-FYLP**, deux occupants
originaux du **CEC St-Jean**, des vitres d'instruments et des reflets de ciel statique
sous le rendu ALS de FlightGear. Rodolphe Pagé porte le bleu à l'avant et Roméo Vachon
le vert à l'arrière. Le menu **SW233** permet de masquer l'équipage ou la livrée.
Les masses restent gérées par le menu Occupants et centrage. La grille UV contrôle
les ailes, empennages et spoilers ; les personnages utilisent un niveau allégé à distance.

**Limites :** livrée provisoire, références récentes de C-FYLP manquantes ; visages et
proportions artistiques ; écussons de projet, aucun grade attribué. Les ailes fictives
sont une option désactivée par défaut. Ce lot n'est pas une reproduction photoréaliste achevée.

[Paquet, captures et atlas de 220 planches](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/visuals-40) ·
[Tutoriel verre](docs/construction/19-realisme.md) · [Livrée](docs/construction/20-livree.md) ·
[Équipage](docs/construction/21-equipage.md) · [Travaux restants](ROADMAP.md).

![Prototype C-FYLP dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/livery-left.jpg)

## Présentation visuelle du lot 40

<video id="visuel40" controls playsinline preload="none" width="960" style="max-width:100%" poster="https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/spoilers-open.jpg" src="https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/presentation-visuelle-40.mp4"></video>

[▶ Lire la présentation de 28 secondes](https://steveprudhomme.github.io/sw233-flightgear/#visuel40) · [MP4](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/presentation-visuelle-40.mp4) · [Refaire les contrôles, dès 10 ans](docs/construction/22-verifications-visuelles.md).

Captures natives de FlightGear 2024.1.7 : spoilers vus de l'extérieur puis du cockpit,
grille des surfaces, instruments et occupants. Présentation immobilisée, sans nouveau
vol ni glissade. Le lecteur fonctionne dans la version web de ce README ; GitHub
fournit le lien de lecture. 59 tests et reconstruction du tutoriel vérifiés.

## Checklists français / anglais

Ouvrir **SW233 → Checklists / Listes** ; choisir la langue dans le même menu.
La fenêtre ouverte revient à la première liste lors d'un changement de langue.
[Tutoriel illustré](docs/construction/05-listes.md#j--ouvrir-et-vérifier-les-listes-bilingues-dans-flightgear).

Les accents sont conservés dans une fenêtre Canvas propre au SW233, vérifiée
sur FlightGear **2024.1.7**. Quatre boutons choisissent le mot-check ; **FR / EN**
change la langue. Les initiales sont rouges. Huit listes et 24 bascules ont
été contrôlées. Ctrl+L fenêtre ouverte et la conservation de langue après fermeture sont
confirmés par l'utilisateur. Le raccourci pendant la fermeture reste à confirmer
physiquement pour cette recette. Le panneau est corrigé pour **1024 × 600**.
[Recette d’utilisation illustrée](docs/construction/05-listes.md#l--essayer-avec-la-souris-le-clavier-et-une-petite-fenêtre).

[Tutoriel pas à pas avec captures](docs/construction/05-listes.md#k--garder-les-accents-avec-une-nouvelle-feuille-de-texte) ·
[Paquet et preuves](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/checklists-usage-37).

![Checklists avec accents dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/checklists-usage-37/petite-fenetre-apres-fr.jpg)

## Cartes du cockpit dégagées

Les cartes d'atterrissage et de sécurité ont été repositionnées pour dégager
l'anémomètre, en français et en anglais. [Tutoriel illustré avant/après](docs/construction/05-listes.md#i--dégager-les-cartes-cachées-par-lanémomètre).

![Cartes françaises dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/cartes-degagees-34/fr-compare.jpg)

[Paquet et preuves du lot cartes-degagees-34](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/cartes-degagees-34).
Positions de maquette ; essais statiques sous trois vues, texte à lire en rapprochant la vue.

## État : prototype expérimental 0.1.0-dev

- Configuration FlightGear et FDM JSBSim originaux.
- Six composantes aérodynamiques, commandes et aérofreins.
- Aile haute effilée, haubans, verrière tandem, roue et patin.
- Poste avant : altimètre, anémomètre en mph et variomètre ; quatre check-lists de simulation.
- Documentation de provenance, tests automatisés et contrôles de contribution.

Les coefficients historiques sont des **paramètres de simulation à valider**,
pas des mesures constructeur. Pas encore de calibration pneumatique, de remorquage,
de modèle fiable de vrille, ni de validation complète dans FlightGear.
Ce projet n'est pas un outil d'instruction au vol réel.

[Comparer le poste avant dans FlightGear, avant et après correction](docs/construction/06-peinture.md#comparaison-cockpit) : la radio dégage le bord de l’altimètre et le compas décoratif apparaît sous la bouche d’air.

[Construire le compas en relief et comparer les vues de face et de biais](docs/construction/06-peinture.md#compas-relief). La vitre et le trait de lecture sont deux pièces distinctes ; [la rose indique maintenant le cap du compas de FlightGear](docs/construction/04-configuration.md#rose-magnetique).

[Anémomètre C-FYLP : comparer l’ancien cadran, les arcs et quatre essais dans FlightGear](docs/construction/07-essais.md#banc-anemometre).

[Altimètre : lire les deux aiguilles et vérifier le calage barométrique](docs/construction/07-essais.md#banc-altimetre).

## Variomètre : descente et aérofreins

<video id="vario" controls playsinline preload="none" width="960" style="max-width:100%" poster="https://github.com/steveprudhomme/sw233-flightgear/releases/download/variometre-07/rentres.jpg" src="https://github.com/steveprudhomme/sw233-flightgear/releases/download/variometre-07/variometre-cyjn.mp4"></video>

[▶ Lire les 17 secondes](https://steveprudhomme.github.io/sw233-flightgear/#vario) · [MP4](https://github.com/steveprudhomme/sw233-flightgear/releases/download/variometre-07/variometre-cyjn.mp4) · [Banc, courbes et procédure](docs/construction/07-essais.md#banc-variometre) · [Commande pour piloter soi-même](INSTALL.md#essai-manuel-sur-windows).

## Essai du compas en virage à CYJN

<video id="compas" controls playsinline preload="none" width="960" style="max-width:100%" poster="https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/nord.jpg" src="https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/compas-en-virage.mp4"></video>

[▶ Voir le film de 30 s](https://steveprudhomme.github.io/sw233-flightgear/#compas) · [Ouvrir le MP4](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/compas-en-virage.mp4) · [Refaire l’essai avec les images, les courbes et le CSV](docs/construction/07-essais.md#compas-en-virage).

## Vidéo : vol au-dessus de Saint-Jean-sur-Richelieu (CYJN)

<video id="film" controls playsinline preload="none" style="max-width:100%" width="960" poster="https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-02/SW233-CYJN-v2.jpg" src="https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-02/SW233-CYJN-v2.mp4"></video>

**[▶ Lire le film dans le lecteur du projet · 1 min 23 s](https://steveprudhomme.github.io/sw233-flightgear/#film)** · [Télécharger le MP4](https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-02/SW233-CYJN-v2.mp4)

Le lecteur intégré est disponible dans la version web de ce README. Dans le dépôt, GitHub affiche le lien de lecture. Capture native de FlightGear 2024.1.4 : sortie puis rentrée des aérofreins depuis le cockpit (14–28 s), second cycle vu du dessus (29–43 s), puis glissade depuis le cockpit et de l’extérieur (46–73 s). Le médaillon est un agrandissement de la ficelle filmée ; β mesure l’angle latéral du vent relatif dans le modèle.

**Pour construire depuis zéro :** [dix-huit fiches de fabrication et leur cahier de mesures](docs/construction/README.md).

**Pour commencer :** [atelier pas à pas, dès 10 ans](docs/atelier.md) · [feuille de route du cockpit et de la livrée Cadets](ROADMAP.md) · [mesures et procédure](docs/validation.md#capture-flightgear-à-cyjn).

## Démarrage rapide

Prérequis : FlightGear avec JSBSim ; Python 3.11+ pour les contrôles.

```sh
git clone https://github.com/steveprudhomme/sw233-flightgear.git
cd sw233-flightgear
python -m pip install Pillow==12.0.0
python tools/package.py
fgfs --fg-aircraft=build/Aircraft --aircraft=sw233 --airport=KSFO --altitude=5000 --vc=50 --in-air --disable-ai-traffic
```

Exécuter la dernière commande depuis la racine du dépôt ; adapter le chemin de
`fgfs` sur Windows. L'altitude est en pieds au-dessus de la mer, `--vc` en nœuds.
La vidéo ci-dessus a été réalisée à CYJN avec le scénario de validation.
Voir [INSTALL.md](INSTALL.md) pour le lanceur graphique et les tests.

## Organisation

`src/SW233/` contient les sources éditables de l'aéronef ; `docs/` la provenance,
l'architecture et la validation ; `tests/` les essais ; `tools/` les contrôles
et la préparation du paquet. `build/` est généré et ignoré par Git.

## Communauté

Les [deux audits externes et leur analyse](docs/references/audits-2026-11-11.md) alimentent les [prochaines tâches à discuter](ROADMAP.md#audits-externes).

- [Issues](https://github.com/steveprudhomme/sw233-flightgear/issues) : bugs, données et idées.
- [Pull requests](https://github.com/steveprudhomme/sw233-flightgear/pulls) : contributions techniques.
- [Contribuer](CONTRIBUTING.md), [conduite](CODE_OF_CONDUCT.md),
  [responsables](MAINTAINERS.md), [historique](CHANGELOG.md).

Les premiers fichiers ont été rédigés avec une assistance IA. Leur origine et
leurs limites sont explicites ; une revue humaine aéronautique reste nécessaire.

[Diagnostic du centrage et de la réserve de profondeur](docs/construction/08-centrage.md) : calculs indépendants, captures FlightGear et limites du modèle historique.

[Repères et point de référence aérodynamique](docs/construction/09-reperes.md) : quatre expériences distinguent un changement de coordonnées d’une modification physique.

### Dernier contrôle des commandes

La [fiche 10 du tutoriel](docs/construction/10-profondeur.md) détaille la profondeur à ±23°, sa construction et les captures dans FlightGear. Consulter la [feuille de route](ROADMAP.md) pour les prochains lots et leurs critères de réussite.


## Occupants et centrage — 13 novembre 2026

Le menu **SW233 → Occupants et centrage** permet de régler les charges au sol ; voir la [fiche 11 illustrée](docs/construction/11-occupants.md), y compris les limites de validation de la saisie.


Actualisation clavier (13 novembre 2026) : saisie 200.125 validée par Steve avec les chiffres du haut, puis vérifiée dans JSBSim ; restauration des décimales corrigée. Utiliser un point décimal. Pavé numérique signalé inopérant avec Verr Num activé, suivi AUD-01d. [Preuve illustrée et limites](docs/construction/11-occupants.md#10-confirmer-la-saisie-et-préserver-les-décimales).


## Installation vérifiée sous Windows

Le paquet inclut désormais un lanceur, la licence et un manifeste. Il peut être déplacé dans un dossier avec espaces ; le lancement commence au sol à CYJN. [Guide rapide](INSTALL.md) · [Tutoriel illustré](docs/construction/12-installation.md). Python est requis ; FlightGear et le décor sont installés séparément. Linux reste à valider.

## Présentation dans le lanceur

Le paquet [selecteur-15](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/selecteur-15) ajoute une miniature native et un aperçu extérieur. La fiche précise le statut expérimental, la GPL-3.0-only et la livrée finale encore à réaliser. [Tutoriel illustré : fabriquer et vérifier la fiche](docs/construction/13-selecteur.md). Contrôle sous FlightGear 2024.1.7 Windows ; 21 tests réussis, Linux non validé.

## Enveloppe du cockpit corrigée

Les flancs jaunes rejoignent maintenant la verrière ; cadres et raccord arrière sont reconstruits. [Comparaison avant/après et méthode](docs/construction/14-enveloppe.md) · [43 pièces illustrées](docs/construction/atlas-pieces.md) · [Paquet enveloppe-16](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/enveloppe-16). 23 tests réussis ; formes et matériaux encore schématiques.

![Cockpit dans FlightGear après correction](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/apres-cockpit.jpg)

## Panneaux de verrière et contours fixes

Le montant du pare-brise est incliné et les vitrages latéraux sont séparés. Des contours de porte fixes complètent le dessin, avec une symétrie encore provisoire. [Fiche 15 illustrée](docs/construction/15-panneaux.md) · [Atlas des 49 objets](docs/construction/atlas-pieces.md) · [Paquet panneaux-17](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/panneaux-17). 24 tests réussis ; dimensions estimatives.

![Vue pilote actualisée](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-cockpit.jpg)

## Contrôle des proportions

La [fiche 16](docs/construction/16-proportions.md) quantifie trois écarts au trois-vues et distingue l’incertitude de pointage de celle du dessin. La géométrie reste panneaux-17 : les références actuelles ne suffisent pas à valider un déplacement de 30 à 37 cm. Le prochain dossier de mesures est suivi sous VIS-01d.

[Références dimensionnelles du cockpit et formulaire illustré](docs/construction/17-references.md) : identification historique de C-FYLP, variantes, datum et cotes encore nécessaires avant correction du modèle.

[Préparer les relevés du cockpit : dix pièces illustrées et dossier téléchargeable](docs/construction/18-releves.md). Les cotes sont celles du modèle ; les mesures réelles restent à recueillir.

[Finition du tableau : textures et comparaison native avant/après](docs/construction/06-peinture.md#h--finition-du-tableau--vis-01f). Amélioration de surface ; cockpit encore schématique.

[Tableau validé : quatre lectures et cockpit complet](docs/construction/06-peinture.md#i--validation-finale-du-tableau--16-novembre-2026). [Paquet avec aperçu actualisé](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/tableau-22).

[Aérateur central en relief : construction, quatre pièces et vues natives](docs/construction/02-maillage.md#aérateur--pièces-et-vérification-native).

[Relief de l’anémomètre : pièces et lectures dans FlightGear](docs/construction/02-maillage.md#anémomètre--pièces-et-essais-du-relief).

[Altimètre en relief : pièces et essais illustrés](docs/construction/02-maillage.md#altimètre--pièces-et-vérification-du-relief). Le réglage par glissement horizontal est vérifié (voir la procédure ci-dessous).

[Régler le calage à la souris : gestes vérifiés et captures](docs/construction/06-peinture.md#j--régler-laltimètre-à-la-souris). Vérification maintenant terminée ; utiliser le cliquer-glisser horizontal.

[Variomètre en relief : construction et quatorze lectures natives](docs/construction/06-peinture.md#k--variomètre-en-relief--vérifier-et-comparer). Bague ouverte et quatre fixations ; dimensions estimées, cadran et étalonnage conservés. [Télécharger le paquet vario-bague-27](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/vario-bague-27).

[Fenêtre de calage : lire la pression et régler le bouton](docs/construction/06-peinture.md#l--fenêtre-de-calage-de-laltimètre). Affichage fonctionnel simplifié en inHg, vérifié de face et de biais. [Paquet calage-fenetre-28](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/calage-fenetre-28).

[Radio en relief : pièces, texture et comparaisons natives](docs/construction/06-peinture.md#m--façade-de-radio-en-relief). Ce premier lot était visuel uniquement ; le réglage COM1 est ajouté dans radio-com-30 ci-dessous. [Paquet radio-relief-29](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/radio-relief-29).

[Radio COM1 réglable : gestes, limites et essais](docs/construction/06-peinture.md#n--régler-la-fréquence-com1). Petit bouton : 1 MHz ; gros bouton : 25 kHz. Clic gauche pour augmenter, clic milieu pour diminuer. Commande générique sur grille 25 kHz ; audio et réseau non validés. [Paquet radio-com-30](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/radio-com-30).

### Compas : finition du boîtier

Boîtier arrondi, joint périphérique et quatre vis en relief ; rose et repère fixe conservés. [Construction illustrée des huit pièces](docs/construction/02-maillage.md#o--comprendre-la-finition-du-compas-pièce-par-pièce) et [comparaison avant/après, banc et virages](docs/construction/06-peinture.md#o--finition-du-compas). Les dimensions restent estimées ; les essais du simulateur ne certifient pas un instrument réel.

![Compas amélioré dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/face-090.jpg)

[Paquet compas-finition-31 et preuves](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/compas-finition-31).

[Voir le compas pendant les deux virages — extraits de 30 secondes](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-finition-31/compas-en-virage.mp4).

### Compas : lettres et graduations lissées

La rose reçoit une bande originale de 4 096 × 256 pixels. Les lettres en petits polygones sont remplacées ; le boîtier et l’animation sont conservés. Quarante-huit lectures statiques ont été contrôlées sous deux éclairages, avec vues pilote et gros plans. La police et la luminosité restent des choix de prototype.

![Rose texturée dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-texture-32/10-face-090.jpg)

[Tutoriel pas à pas : l’étiquette autour du tambour](docs/construction/06-peinture.md#p--des-lettres-plus-nettes-pour-le-compas) · [Paquet compas-texture-32](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/compas-texture-32).

Version du projet : **0.1.0-alpha.1**. Consulter la [politique SemVer](VERSIONING.md).

## Raccords et dossier — 0.1.0-alpha.3

Le vitrage central suit les bords des ailes. Les faces internes sont grises.
Le dossier présente un relief, un passage noir en demi-lune et une sangle verte.
Une grille représente l’ouverture signalée à gauche ; sa fonction reste à confirmer.

[Tutoriel illustré](docs/construction/27-raccords-arriere.md) · [Bilan](docs/validation/raccords-lot45.md) · [Paquet](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/v0.1.0-alpha.3).

## Correction de silhouette en préparation

Le [lot46](docs/construction/28-silhouette-verriere.md) reprend la verrière et la place arrière selon les annotations du mainteneur. La silhouette reste en revue ; alpha.4 n’est pas publiée.

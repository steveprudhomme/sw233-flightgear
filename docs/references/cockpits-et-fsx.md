# Cockpits de référence et paquet FSX des Cadets

## Choisir l’image qui répond à la question

Les préfixes identifient les fichiers et leurs empreintes dans [l’inventaire](inventaire.md). Les cinq JPEG ont été vérifiés dans le fonds local. Trois y figuraient déjà ; les deux vues de simulation C-GDFE sont nouvelles.

| Image | Ce qu’elle permet de vérifier | Limite |
|---|---|---|
| 5d81c6bf · photo C-FYLP | Position relative de la radio, du compas, de la bouche d’air et des quatre cartes. Référence principale de notre poste avant. | Photo légèrement oblique ; pas de mesure de profondeur. |
| c5a92821 · photo N2930H | Forme des pédales, pied du manche et disposition autour du compas. | Autre appareil : ne pas transférer les emplacements de ses cadrans à C-FYLP. |
| 736f05ab · photo verticale en vol | Le compas sous la bouche d’air présente des chiffres derrière un trait vertical. Le tube et la ficelle se détachent au-dessus du tableau. | Immatriculation tronquée ; ne pas attribuer cette photo à C-FYLP. |
| cad7cbea · vue simulée C-GDFE | Vue vers le remorqueur : proportion de ciel et de tableau, visibilité de la ficelle. | Image d’un autre modèle, ni photo réelle ni référence de champ de vision mesuré. |
| cd9b8faf · vue simulée C-GDFE | Vue reculée : manche, pédales, flancs et levier à gauche. Utile pour préparer un cadrage de comparaison. | Ne donne pas les dimensions du cockpit ni la position réelle de l’œil. |

**Provenance du forum.** Le [message nº 15 de Rustydatsun1547](https://forums.flightsimulator.com/t/announcement-schweizer-sgs-2-33a-glider-freeware/550528/15), publié le 14 novembre 2022 (UTC), contient précisément deux liens : [première image, 1920 × 1440](https://flightsimulator-forums-cdn.azureedge.net/uploads/default/original/4X/8/8/6/8866fc921a6826e088ff9c2e4bb542e3a7eb260b.jpeg) et [seconde image, 1440 × 1800](https://flightsimulator-forums-cdn.azureedge.net/uploads/default/original/4X/c/5/a/c5a92821d7efde1d78dbd8eac820d2a0bc7103f1.jpeg). Dimensions annoncées par le forum. La seconde est la photo de N2930H fournie en 690 × 862. Le premier original (8866fc92) n’est pas dans le fonds local ; les deux liens sont conservés, sans attribuer les autres pièces jointes à ce message.

## Ce que contient aircadetpackage.zip

Archive fournie pour étude, conservée entière dans le fonds local. Le Readme attribue le Schweizer à Wolfgang Piper, le Bellanca Scout à Long Island Classics et la peinture à Taylor Giannelia. La notice du planeur indique FSX, version 1c, juin 2008 ; elle crédite Blair Clayton pour la photo du tableau. Les conditions freeware du paquet sont distinctes de la GPL du projet. Les jauges, peintures et modèles tiers ne sont pas incorporés au paquet FlightGear.

**Compas : un exemple concret pour le prochain atelier.** Dans le dossier du Schweizer, panel/Panel.cfg distingue le tableau 2D du cockpit virtuel et place une jauge Kompass dans les deux. Dans panel/WP-SGS2-33A_US.cab, Kompass.xml utilise une bande graduée mobile sous un masque, puis un trait fixe. La bande dépend de l’indication du compas FSX. Pour FlightGear, garder le trait 3D déjà construit, dessiner nos propres graduations et vérifier quelle propriété fournit l’indication magnétique. Essayer 000°, 090°, 180°, 270°, puis 359° → 000° ; le trait doit rester immobile et la lecture doit passer le nord sans saut visible. Les positions de pixels FSX ne sont pas des cotes de montage.

**Modèle de vol : des écarts à ne pas importer.** Dans Aircraft.cfg du Schweizer (pas dans celui du Scout), wing_span vaut 51 et wing_area vaut 190 ; notre [source constructeur](../sources.md) donne 51 ft et 219,48 ft². Le même CFG met max_gross_weight à 4040 alors que la notice livrée annonce 1040 lb, cohérent avec le manuel. Le fichier SGS2-33A.air est présent mais son contenu binaire n’a pas été décodé. Aucune modification du FDM sur cette base.

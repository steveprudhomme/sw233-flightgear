# Dossier dimensionnel du cockpit — VIS-01d

Recherche du 15 novembre 2026. Plan préalable : `06125ce`. Ce registre distingue une preuve d'identification, une dimension générale et une cote directement applicable au maillage.

## Sources et résultats

| ID | Source précise | Résultat admissible | Limite pour notre modèle |
|---|---|---|---|
| R1 | Manuel FAA fourni, `FAA_Approved_Flight_Manual_SGS_233__DA1493E06B1D6.pdf`, révision 15 février 2022, approbation 23 février 2022 ; PDF 4, papier 6–7 | Longueur du fuselage 2-33/2-33A : 25 ft 9 in ; envergure 51 ft ; verrière décrite d'une seule pièce | Pas de largeur ni de stations de vitrage exploitables sur cette page |
| R2 | Même édition, PDF 14, papier 26–27 | Datum 66,34 in devant le bord d'attaque à l'emplanture ; bras des occupants avant 43,80 in et arrière 74,70 in pour 2-33/2-33A | Les bras de masse ne sont ni les centres de sièges 3D ni les positions des yeux ; le datum n'est pas notre nez de maillage |
| R3 | Même édition, PDF 4, papier 7, description des variantes | Le 2-33B a un fuselage allongé de 5 in derrière le pilote avant ; le texte indique aussi porte/vitre « 9 in wider » à l'intersection de l'aile | Ne pas appliquer ces différences au 2-33A. L'axe du second écart n'est pas suffisamment défini ici pour en tirer une largeur transversale |
| R4 | [Défense nationale, Propos de vol / Flight Comment, 1993 nº 1](https://publications.gc.ca/collections/collection_2016/mdn-dnd/DC2-2-1993-1.pdf), PDF 4 | Le document associe C-FYLP au type Schweizer 2-33A | Identification historique, pas preuve de la configuration actuelle, du numéro de série ni de la date de notre photographie |
| R5 | [K & L Soaring, verrière 33325-003](https://www.klsoaring.com/index.php/items-for-sale/parts-for-sale/parts-for-sale/2-33-parts/sgs-2-33-canopy-trimmed-drilled-detail), consulté le 15 novembre 2026 | Compatibilité annoncée à partir du numéro de série 69, ou après conversion à la configuration ultérieure | Aucun plan coté ; identifier le numéro de série et les transformations de l'appareil avant de choisir cette configuration |
| R6 | [Instructions Cadets, édition du 31 janvier 2017](https://bc-aircadetleague.com/wp-content/uploads/2017/06/403-manual-en-acgp-2-33-aois-2017.pdf), PDF 9, page 1-1 | Corrobore longueur 25 ft 9 in, envergure 51 ft et verrière d'une pièce | Édition historique ; les dimensions générales ne donnent pas la section du cockpit |

Les documents locaux sont recensés avec leurs empreintes dans [l'inventaire](inventaire.md). Une autre reproduction du manuel, sur FAASafety, n'a pas la même pagination : ne pas reporter nos numéros de pages sans identifier l'édition.

## Calculs vérifiables

Un pied vaut 0,3048 m ; un pouce vaut 0,0254 m. Longueur : 25 × 0,3048 + 9 × 0,0254 = **7,8486 m**. Envergure : 51 × 0,3048 = **15,5448 m**. Distance datum–bord d'attaque : 66,34 × 0,0254 = **1,685036 m**. Cette dernière valeur établit une relation entre deux repères réels ; elle n'établit pas la distance nez–datum de notre maillage.

## Décision sur les pièces

- Coque, montant et vitre : conserver provisoirement panneaux-17. Les écarts de la fiche 16 restent des écarts à un dessin illustratif.
- Les objets nommés pare-brise et vitrages sont des partitions du maillage. Leur séparation ne prouve pas l'existence de joints ou de montants sur une verrière réelle d'une pièce. Réexaminer les cadres visibles avant de les figer.
- Porte : contours fixes et symétriques encore hypothétiques. Ne pas déduire une porte identique sur chaque flanc d'une seule vue.
- Sièges et vue pilote : ne pas déplacer suivant les stations de masse R2.
- Présentation FlightGear : aucun changement visible pendant ce lot documentaire ; pas de nouvelle miniature ni de nouvelle capture présentée comme un essai.

## Ce qui manque et comment le recueillir

Numéro de série/configuration de l'appareil de référence, profil gauche et droit datés, limites de l'ouverture et du vitrage, positions longitudinales et hauteurs des points A/B/C/D, largeur extérieure à une section identifiée, photo et cote indépendante dans le même plan. Utiliser le [formulaire de relevé](releve-cockpit.md).

Deux dimensions dans le même plan sont un minimum de contrôle, pas une garantie de précision : contrôler aussi la perspective, la correspondance des points et les incertitudes. Une photo oblique ne devient pas orthogonale parce qu'elle contient une règle.

## Périmètre de la recherche et biais

Ont été examinés : les passages description/centrage de l'édition locale 2022, les dimensions générales et schémas des instructions Cadets 2017, le catalogue de verrière K & L et l'identification historique de C-FYLP. Aucun plan de fabrication coté du cockpit n'a été établi par ces sources. Cela ne signifie pas qu'il n'en existe pas ailleurs.

Biais possible : nous privilégions C-FYLP parce que sa photo a guidé le tableau. Cette préférence ne démontre ni que tous les Cadets emploient cette configuration, ni qu'elle représente la livrée actuelle. Les photos d'autres immatriculations et les plans de maquette restent des comparaisons, jamais des mesures de C-FYLP.

Les fichiers tiers restent sous leurs droits propres. Les liens et relevés factuels ne les placent pas sous GPL. Aucun message n'a été envoyé à un propriétaire ou fournisseur.

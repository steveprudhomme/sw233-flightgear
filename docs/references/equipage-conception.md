# Équipage — références et conception originale

## Deux recherches distinctes, séance E40-01

Sources publiques officielles consultées le **17 novembre 2026**. Les règles des cadets et celles des membres des Forces armées canadiennes ne sont pas interchangeables. Rodolphe Pagé et Roméo Vachon sont les personnages fictifs du projet, pas des portraits ou des biographies. Aucun grade ni dossier de qualification n’est attribué à une personne réelle.

### Cadet avant : C5B

L’[annexe L des instructions de tenue des cadets — C5B](https://www.canada.ca/en/department-national-defence/services/cadets-junior-canadian-rangers/cjcr-policy/cjcr-dress-instructions/chapter-6/annex-l.html), page modifiée le 28 janvier 2025, est la référence de placement : bande nominative devant à droite au-dessus de la poche zippée, écusson d’escadron à l’épaule droite, écusson d’aéronef à gauche, ailes devant à gauche. Le [visuel officiel C5B](https://www.canada.ca/content/dam/dnd-mdn/images/cadetsjcr/policy/dress-instructions/chapter-6/6-6-1-11.jpg) permet d’observer la silhouette et la combinaison bleue. Il est lié pour consultation, sans être incorporé dans le paquet, transformé en texture ou utilisé comme portrait.

### Officier arrière : tenue de vol des FAC

L’[appendice 2, annexe G — bandes nominatives](https://www.canada.ca/en/services/defence/caf/military-identity-system/dress-manual/chapter-3/annex-g/appendix-2.html), modifié le 30 août 2023, renvoie le placement sur la tenue de vol aux directives du commandant de l’ARC. Il ne valide donc pas, à lui seul, les coordonnées des patches de notre personnage arrière.

La [section 7 — accessoires, paragraphes 40–41](https://www.canada.ca/en/services/defence/caf/military-identity-system/dress-manual/chapter-3/section-7.html) distingue la plaque rigide de la bande brodée. Pour la bande de type B, elle indique 25 mm de hauteur et des lettres de 10 mm, avec nom de famille et élément. La bande tactique de type A a une autre hauteur. Notre choix de 25 mm est documenté; le libellé demandé `R. VACHON`, la police et l’absence d’identifiant d’élément restent des choix du projet, pas une reproduction réglementaire complète.

L’[annexe B — insignes de vol](https://www.canada.ca/en/services/defence/caf/military-identity-system/dress-manual/chapter-3/annex-b.html), modifiée le 17 janvier 2024, renvoie également aux instructions de l’ARC pour la tenue de vol et traite séparément les ailes des cadets portées par le Cadre des instructeurs de cadets. L’[OAIC 52-04](https://www.canada.ca/en/department-national-defence/services/cadets-junior-canadian-rangers/cjcr-policy/catos/volume5/52-04.html), page modifiée le 1er mars 2022, décrit des conditions d’autorisation pour les ailes. Aucune preuve individuelle correspondante n’existe pour ces personnages fictifs : aucune aile officielle ni aucun grade n’est ajouté.

La [page officielle du CEC St-Jean](https://www.canada.ca/fr/ministere-defense-nationale/services/cadets-rangers-juniors-canadiens/cadets/centres-entrainement/st-jean.html) confirme le nom du centre et sa formation de pilote de planeur. Elle n’établit aucune affiliation des personnages et ne sert pas de licence pour inventer un écusson officiel.

## Matrice de provenance

| Élément | Confirmé dans une source | Estimé ou choisi pour le modèle | Inconnu / non affirmé |
| --- | --- | --- | --- |
| Cadet bleu avant | C5B et emplacement des accessoires dans l’annexe L | Nuance bleue, coupe détaillée, poches et plis | Mesures d’une combinaison réelle et grade individuel |
| Officier vert arrière | Manuel FAC distinct; directives ARC requises pour la tenue de vol | Vert et patron semblable à l’avant, rôle d’officier fictif | Modèle exact de combinaison, directive locale applicable, grade |
| Bandes nominatives | Type B FAC : hauteur et lettres décrites au §41 | Surface 82 × 25 mm; `R. PAGÉ` / `R. VACHON`; police locale | Conformité complète de ces libellés; longueur réglementaire applicable à ces personnages |
| Patches d’épaules | Emplacements C5B documentés pour le cadet | Dessins originaux **PROJET / CEC / ST-JEAN** et **SW233** | Écussons d’unité officiels ou affiliation individuelle |
| Ailes | Autorisation conditionnée par les textes sur les qualifications | Variante marquée **FICTIF**, désactivée par défaut | Qualification de pilote ou instructeur des personnages |
| Harnais et posture | Géométrie actuelle du cockpit utilisée pour les contrôles | Bretelles de 30 mm, boucle, mains fixes et proportions humaines | Installation de harnais certifiée, anthropométrie mesurée |
| Dégagements | Calculs sur `src/SW233/Models/sw233.ac` | Garde tête avant augmentée de 20 mm | Validation physique d’un SGS 2-33 réel |
| Niveau de détail | Animation `range` décrite dans la documentation FlightGear installée | Bascule à 60 m; géométrie éloignée simplifiée | Gain de fréquence d’image avant mesure native |

**Le patron réglementaire de la tenue verte d’officier reste non confirmé.** La recherche séparée évite d’étendre automatiquement la règle C5B au personnage arrière. Les patches de projet ne sont pas des copies d’insignes. L’initiale dans les noms est une convention de ces personnages. Les deux combinaisons restent des interprétations artistiques.

## Sources techniques et traçabilité

La documentation locale consultée est `fgdata_2024_1/Docs/model-howto.html`, section **range**, complétée par `Models/Military/humvee-pickup-odrab-low-poly.xml` de la même installation. Le [code primaire SimGear, animation.cxx](https://github.com/FlightGear/simgear/blob/next/simgear/scene/model/animation.cxx) décrit `SGRangeAnimation` : les distances concernent le point de vue et la sphère englobante de l’objet. Le modèle utilise donc les mêmes bornes pour chaque paire proche/lointaine. Aucun maillage de ces exemples n’est copié.

L’intégralité de la géométrie et de l’atlas vient de `tools/crew.py`. Aucune photo, visage, phototexture, géométrie tierce ou écusson officiel n’est incorporé. L’export `export_atlas_source` garde les pièces individuelles pour le livre, tandis que le paquet fusionne les pièces par catégorie d’affichage. Le [chapitre 21](../construction/21-equipage.md) contient la recette complète, les calculs de dégagement et les limites des essais.

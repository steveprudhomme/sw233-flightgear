# Sources, statut des données et droits

Recherche effectuée les 1 et 2 novembre 2026. Les liens vers des branches
peuvent évoluer ; les nombres recensés ici décrivent les fichiers examinés.

## Sources primaires consultées

1. [Manuel constructeur reproduit par FAASafety.gov](https://www.faasafety.gov/files/events/GL/GL09/2018/GL0983174/schweizer_2_33_manual.pdf).
   Géométrie et performances publiées. Cette reproduction comporte elle-même
   une réserve de complétude. Aucune copie du document n'est distribuée ici.
2. [Modèle SGS233 du dépôt JSBSim](https://github.com/JSBSim-Team/jsbsim/blob/master/aircraft/sgs233/sgs233.xml).
   Paramètres d'un ancien simulateur, non des mesures certifiées. L'en-tête
   reconnaît des estimations et interdit la vente de ce modèle. Aucun de ses
   fichiers XML n'est copié ou relicencié sous GPL-3.0-only dans ce dépôt.
3. [Archive SGS233 du miroir FlightGear 2024](https://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Aircraft-2024/sgs233.zip).
   Le FDM et le set ont été examinés, ainsi que Models/readme.txt : le modèle
   visuel provient d'un ancien travail FS98 de Captain Slug, converti par Dave
   Culp. Les droits propres aux ressources ne sont pas assez explicites pour
   les inclure ici. Aucun modèle, texture, panel, son ou script n'est copié.
4. [Projet MSFS SGS 2-33A annoncé par son auteur](https://forums.flightsimulator.com/t/announcement-schweizer-sgs-2-33a-glider-freeware/550528).
   Projet identifié, mais aucun flight_model.cfg public inspecté lors de cette
   recherche. Aucune valeur ne lui est attribuée. Freeware ne signifie pas
   automatiquement open source.
5. [Repères JSBSim](https://jsbsim-team.github.io/jsbsim-reference-manual/user/concepts/frames-of-reference/)
   et [schéma JSBSim](https://github.com/JSBSim-Team/jsbsim/blob/master/JSBSim.xsd).
   Références de syntaxe et de conventions.

## Données indépendamment documentées

Surface : 219,48 ft² ; envergure : 51 ft ; longueur : 25 ft 9 in ; masse maximale
publiée : 1 040 lb. Le modèle utilise une corde de référence de 4,3 ft : choix
historique voisin de S/b, pas une identification de la corde aérodynamique moyenne.

## Valeurs numériques historiques retenues pour le prototype

Ces nombres ont été relevés dans les fichiers SGS233 consultés. Le code de
calcul est une rédaction originale des équations usuelles de forces et moments.
La licence GPL-3.0-only porte sur cette implémentation et ses documents originaux ; elle
n'affirme aucun droit nouveau sur les fichiers tiers référencés.

| Paramètre | Valeur | Statut |
|---|---:|---|
| Poids à vide | 610 lb | Historique, non pesée d'un exemplaire |
| Occupants de référence | 180 + 180 lb | Scénario de chargement |
| Ixx / Iyy / Izz à vide | 1800 / 850 / 1950 slug·ft² | Estimations historiques |
| CG à vide, pouces | (103,2 ; 0 ; −6,4) | Repère historique |
| Occupants, pouces | (43 ; 0 ; 4), (85 ; 0 ; 4) | Repère historique |
| Référence aérodynamique, pouces | (103,2 ; 0 ; 0) | Repère historique |
| CL(α) | (−0,20;−0,85), (0;0,25), (0,21;1,32), (0,60;0,21) | Table historique, α en rad |
| CD de base à α=0 | 0,017 | Table historique dépendant d'α |
| Facteur de traînée induite k | 0,05 | Terme k·CL² |
| ΔCD / ΔCL aérofreins sortis | +0,01 / −0,05 | À recalibrer |
| CLδe / CYβ | +0,20 / −1,00 | Par radian |
| Clβ / Clp / Clr | −0,10 / −0,40 / +0,15 | Vitesses angulaires réduites |
| Clδa / Clδr | +0,07 / +0,01 | Par radian |
| Cmα / Cmδe / Cmq / Cmαdot | −0,40 / −0,60 / −9 / −12 | Vitesses angulaires réduites |
| Cnβ / Cnr / Cnδr / Cnδa | +0,12 / −0,15 / −0,03 / −0,02 | Convention JSBSim |

La traînée de base utilise aussi (±0,26 rad; 0,034) et (±1,57 rad; 1,5).
La traînée de dérapage utilise (0;0), (±0,26;0,05), (±1,57;1,23).
Les débattements de prototype sont ±0,30 rad en profondeur et ±0,35 rad aux
ailerons/direction. Ils ne sont pas présentés comme les butées constructeur.

## Choix propres au nouveau code

- Déplacement instantané des gouvernes et aérofreins : approximation explicite.
- Traînée de profondeur rendue symétrique via la valeur absolue de δe ; le gain
  0,024 provient du modèle historique, mais cette formulation doit être recalibrée.
- Train fixe : contribution constante CD=0,001.
- Pas de Cm0 identifié ; pas de terme de moment dû aux aérofreins identifié.
- Contacts : roue centrale synthétique au milieu des deux contacts principaux
  historiques, patin avant et points structuraux. Pas de frein de roue simulé.
- Masse totale par défaut : 970 lb. Le CG chargé est calculé par JSBSim : il ne
  faut pas confondre sa position avec le CG à vide ou la référence aérodynamique.
- Géométrie AC3D schématique originale : pas un plan constructeur.

## Limites et biais

La réutilisation de valeurs historiques favorise un comportement déjà modélisé,
mais risque de transmettre ses erreurs. Les deux fichiers examinés partagent
manifestement des paramètres : ils ne constituent pas deux validations
indépendantes. La finesse publiée, le décrochage et la réponse aux aérofreins
restent des objectifs d'essai. Aucune prétention de précision des vrilles.

# DIM-51 — repères du train et hauteur

Pour les personnes qui vérifient la géométrie. Relevés du 17 novembre 2026.
Manuel : [identification et empreinte](manuel-stations-369.md#manuel-complet-et-dimensions-de-construction).

## Références examinées

| Page PDF / imprimée | Contenu utile | Limite |
|---|---|---|
| 9 / A2 | Hauteur totale 9 pieds et 3,5 pouces, soit 2,8321 m | Assiette et points de mesure non explicités sur cette page |
| 20 / A12 | Stations aile 66,34 ; roue principale 88,75 ; roulette 285,0 pouces | Exemple de l’appareil no 369 ; ne prouve pas la configuration actuelle de C-FYLP |
| 24 / B1 et 30 / B7 | Assemblages et tubes de forme du fuselage avant | Dessins d’identification ; pas de cote nez–aile exploitable relevée |
| 32 / B9 et 371 / P10 | Tubes de forme arrière ; détails de fixation | Les petits chiffres de repérage ne sont pas des distances longitudinales |
| 45–46 / B22–B23 | Habillages des racines d’aile, capot et fixations | Ne suffit pas à appeler les ouvertures photographiées des aérateurs |
| 146–151 / E12–E17 | Deux configurations de verrière, nomenclatures et dessins | Dessins non cotés pour le profil extérieur recherché |
| 149–150 / E15–E16 | Verrière 33300H-101, cadre 33300H-103, applicable aux appareils 70 et suivants | Applicabilité à confirmer pour l’appareil photographié |
| 161 / E27 | Détails locaux de perçage du vitrage | Les diamètres locaux ne définissent pas la longueur ou la hauteur de la verrière |
| 210–221 / H1–H12 | Roues principales, freins et variantes | Le catalogue de pièces ne donne pas une position générale depuis notre nez |
| 222–226 / H13–H17 | Installations de roulette arrière, dont une version à ressort optionnelle | Identifier la variante avant de reconstruire son support |

Les pages citées ont été examinées visuellement. Le PDF numérisé ne fournit pas de texte exploitable par extraction simple.
Cette recherche ciblée ne constitue pas une lecture exhaustive des 392 pages.

## Distances indépendantes de l’origine

Soustraire les stations avant de convertir les pouces en mètres.
Ainsi, une origine inconnue s’annule dans la différence.

| Distance | Calcul | Résultat | Avant, dans le maillage | Après, dans le maillage |
|---|---|---:|---:|---:|
| Aile → roue principale | (88,75 − 66,34) × 0,0254 | 0,569214 m | 0,260000 m | 0,569210 m |
| Aile → roulette | (285,0 − 66,34) × 0,0254 | 5,553964 m | 5,520000 m | 5,553960 m |
| Roue principale → roulette | (285,0 − 88,75) × 0,0254 | 4,984750 m | 5,260000 m | 4,984750 m |

L’export du maillage arrondit les coordonnées à cinq décimales.
Le bord avant de l’aile reste à x = 1,99 m dans le modèle.
Les centres des roues passent donc à x = 2,559214 m et x = 7,543964 m avant arrondi.
Le déplacement est de 0,309214 m pour la roue principale et de 0,033964 m pour la roulette.
Les rayons et les hauteurs restent estimés. Seuls les deux objets de roue ont changé.

Ce choix aligne la maquette sur le schéma A12. Il ne transforme pas l’exemple en relevé de C-FYLP.
Un recalage fondé sur l’aile donnerait Sta.0 à x = 0,304964 m dans le modèle.
C’est une conséquence du choix de x = 1,99 m, pas une mesure confirmée de la distance nez–Sta.0.

## Hauteur et assiette

L’**assiette** décrit l’inclinaison du planeur. Le roulis est son inclinaison latérale.
L’encombrement vertical du maillage fermé et à niveau est de 2,265 m.
La valeur du manuel est de 2,8321 m. Leur différence numérique est de 0,5671 m.
Elle ne permet pas, seule, de choisir une correction de dérive, de train ou de fuselage.

Dans FlightGear, l’assiette observée est d’environ 0,741 degré et le roulis de −12,634 degrés.
En appliquant cette rotation aux sommets, l’encombrement vertical calculé devient environ 3,513 m.
Ce calcul mesure l’écart entre les sommets extrêmes. Ce n’est ni une garde au sol ni une hauteur mesurée dans la capture.
La comparaison à 2,8321 m reste non résolue sans conditions de mesure communes.

## Contacts du modèle de vol

Les points `main-wheel` et `tail` du modèle de vol sont séparés de 4,131056 m longitudinalement.
L’entraxe visuel corrigé est de 4,984750 m. La différence vaut 0,853694 m.
Les points de contact et les centres de roues n’ont pas encore une correspondance géométrique validée.
Un simple déplacement de toute la maquette ne peut pas rendre ces deux espacements égaux.
Les contacts restent inchangés dans ce lot, ainsi que les masses et les coefficients de vol.
Leur recalage, avec les hauteurs et les réactions au sol, est suivi dans DIM-52.

## Reproduire le relevé

Depuis le dépôt, exécuter :

```powershell
python -m tools.dimension_audit --pitch 0.740915 --roll -12.634286 --output audit-dimensions.json
```

Le rapport sépare les distances du manuel, celles du maillage et celles des contacts.
Les [preuves natives](../validation/dimensions-lot51.md) conservent l’assiette réellement lue dans chaque séance.

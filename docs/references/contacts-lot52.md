# DIM-52 — Raccord des contacts au maillage

Public : contributeurs. Connaissances : coordonnées, mètres et pouces, lecture XML.

## Repères et portée

Le maillage AC3D utilise les axes arrière, haut, gauche.
Le lecteur du projet les convertit en arrière, droite, haut.
JSBSim utilise aussi arrière, droite, haut pour ses coordonnées de structure.
Les contacts sont exprimés en pouces : diviser chaque coordonnée du maillage par 0,0254.
Le repère visuel VRP reste nul. Le modèle principal ne reçoit aucune translation supplémentaire.
Les décalages des instruments ne concernent pas la coque.

Cette correspondance raccorde deux représentations du projet.
Elle ne prouve pas que le nez correspond à Sta.0 du constructeur.
Les positions historiques des masses, du centre aérodynamique et des yeux restent inchangées.
Leur réconciliation avec le manuel reste ouverte.

La position du contact JSBSim représente l’appui sans compression.
La documentation décrit aussi les ressorts et les amortisseurs.
Voir la [description officielle de FGLGear](https://jsbsim-team.github.io/jsbsim/python/FGLGear.html)
et le [guide officiel de création d’un avion](https://jsbsim.sourceforge.net/CreatingJSBSimAircraft.pdf).

## Points appliqués

| Contact | x, arrière (m) | y, droite (m) | z, haut (m) | Choix |
|---|---:|---:|---:|---|
| Roue principale | 2,559214 | 0 | −0,845 | Bas de la roue sans compression |
| Patin avant | 0,32593 | 0 | −0,55778 | Sommet inférieur avant du maillage |
| Roulette | 7,543964 | 0 | −0,354 | Bas de la roulette ; contact roulant |
| Aile gauche | 2,3744 | −7,7724 | 0,91112 | Sommet inférieur du bout d’aile |
| Aile droite | 2,3744 | 7,7724 | 0,91112 | Sommet inférieur du bout d’aile |
| Patin arrière | 1,90593 | 0 | −0,72778 | Sommet inférieur arrière du maillage |

Les deux appuis du patin couvrent ses extrémités. Le patin visuel reste une forme provisoire.
Les contacts d’aile restent structurels : les roues de bout d’aile ne sont pas encore modélisées.
Le pas longitudinal principal–roulette devient 4,98475 m, comme le relevé A12 appliqué au modèle visuel.

## Suspension choisie pour le prototype

| Contact | Raideur (lb/ft) | Amortissement (lb/ft/s) | Frottement roulant |
|---|---:|---:|---:|
| Roue principale | 20 000 | 2 000 | 0,05 |
| Chaque extrémité du patin | 10 000 | 1 500 | 0,5 |
| Roulette | 3 000 | 500 | 0,05 |
| Chaque bout d’aile | 1 000 | 250 | 0,5 |

Ces valeurs sont des estimations de simulation, sans mesure constructeur.
Elles limitent la compression excessive des anciens contacts souples.
Les coefficients statique 0,8 et dynamique 0,5 restent inchangés.
La roulette devient un contact roulant sans frein et sans direction commandée.
Cela ne reproduit pas toutes les variantes optionnelles du manuel H13–H17.

Le pneu visible reste rigide. Son bord descend davantage quand le planeur penche.
La compression et cette largeur produisent encore environ 2,73 cm de pénétration sur le banc plat.
Ce résidu est mesuré ; aucune translation cachée du modèle ne le masque.
Une animation de suspension ou un contact tenant compte de la largeur reste nécessaire pour le supprimer.

## Vérification de la hauteur

Le maillage fermé et horizontal conserve une hauteur de 2,265 m.
À l’assiette native après correction, son encombrement vertical atteint environ 3,535 m.
Cette mesure inclut l’aile levée. Elle ne correspond pas automatiquement à la hauteur du manuel.
Le manuel donne 2,8321 m, sans conditions exploitées pour cette comparaison.
DIM-52c reste ouvert ; aucune pièce n’a été étirée pour obtenir ce nombre.

## Sources et reproductibilité

- Manuel *Schweizer SGS 2-33 and 2-33A Parts & Maintenance*, PDF 9 / A2 : dimensions générales.
- Même manuel, PDF 20 / A12 : exemple de stations, appareil 369. Applicabilité exacte à C-FYLP non établie.
- Même manuel, PDF 222–226 / H13–H17 : installations de roulette, sans raideur utilisée ici.
- [Recette de dynamique](../construction/03-vol.md), section C : source reproductible des contacts.
- [Banc de mesure](../../tools/ground_bench.py) : quatre cas, sol plat, air calme, masse 970 lb.
- [Preuves DIM-52](../validation/contacts-lot52.md) : captures et mesures natives.

Les sources privées restent dans le dossier local ignoré. Les captures publiées sont produites dans FlightGear.

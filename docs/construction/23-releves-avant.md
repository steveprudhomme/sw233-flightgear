# 23 — Observer et relever le nez, la coque et la verrière

VIS-05a, séance41. Nous préparons la reconstruction ; **nous ne changeons pas encore l'avion**. Un modèle peut passer tous ses tests et ressembler insuffisamment à l'original. Ici, nous cherchons où et pourquoi.

## 1. Préparer les références

Dans le dossier du projet, ouvre `docs/references/originaux/exterieur-lot-01/index.html`, puis la photo **EXT-02**. Son nom commence par `841099659`. Elle fait 2048 × 1364 pixels. C'est notre vue de profil oblique de travail, pas un plan à l'échelle. Ouvre aussi EXT-03 pour le bombé de la verrière, puis DET-03 et DET-05 dans la galerie du lot02 pour voir ce qui s'ouvre.

EXT-02 porte MANITOBA ; aucune immatriculation complète ne permet ici de l'attribuer à C-FYLP. Nous étudions les formes visibles de cette référence sans déclarer sa décoration identique à celle de notre avion. Les originaux restent locaux, avec leur empreinte dans le manifeste. Les captures du simulateur publiées ci-dessous sont nos propres images.

## 2. Poser des repères, comme sur une carte quadrillée

Un pixel est un petit point de l'image. Le coin supérieur gauche est (0,0). La première coordonnée va vers la droite, la seconde vers le bas. Une paire (1230,700) ne signifie donc pas « 1230 mètres » !

Les pointages suivants sont **approximatifs**, effectués visuellement sur l'image originale. Le nombre après ± donne une marge de lecture ; ce n'est pas une précision constructeur.

| Point | Repère choisi sur EXT-02 | u, v en pixels | Marge |
|---|---|---|---|
| A | Extrémité droite du nez | 1565, 865 | ±12 |
| B | Raccord avant vitrage/capot | 1230, 700 | ±15 |
| C | Sommet apparent du vitrage | 1015, 555 | ±15 |
| D | Coin bas arrière apparent du cadre avant | 950, 785 | ±15 |
| E | Coin haut arrière apparent du cadre avant | 945, 580 | ±15 |
| F | Cassure basse avant, au-dessus du patin | 1370, 1015 | ±20 |
| G | Bas apparent du ventre avant, hors patin | 1130, 1090 | ±20 |

Le fichier [releves-avant-41.json](../references/releves-avant-41.json) conserve ces choix. Tu peux les discuter et les corriger : l'important est de savoir quel point a été choisi, sur quelle image et avec quelle incertitude.

![Schéma des points relevés, sans photographie](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-41/points.svg)

Les lignes bleues joignent les repères. **Elles ne sont pas le dessin de la vraie courbe.** Les cercles rouges montrent la marge de lecture. Pour voir ces repères sur la photo intacte, fabrique la fiche locale :

```powershell
python -m tools.reference_survey build/releves-41
Start-Process build/releves-41/index.html
```

Ouvre un terminal dans le dépôt, avec les dépendances du projet installées selon INSTALL.md. Choisis un dossier neuf : le programme refuse d'écraser un relevé. Il vérifie l'empreinte de la photo, lit les coordonnées, dessine une couche de repères dans la page et extrait les limites des pièces du modèle. Il ne retouche pas le JPEG. Cette fiche nécessite les originaux locaux ; le téléchargement des seules sources GitHub ne les fournit pas.

## 3. Calculer un rapport sans inventer une dimension

Sur cette image, la différence verticale entre B et C vaut **700 − 555 = 145 pixels**. L'écart horizontal entre D et B vaut **1230 − 950 = 280 pixels**. Leur rapport est **145 / 280 ≈ 0,52**.

Cela décrit uniquement ces deux écarts projetés sur la photo. Ce n'est ni la hauteur réelle de toute la verrière, ni son rapport hauteur/longueur en trois dimensions : le cadre est oblique et les points ne sont pas tous dans le même plan.

Chaque extrémité peut être pointée 15 pixels plus loin. Pour voir l'effet, prends une marge de 30 pixels sur chaque différence :

- Petit rapport : (145 − 30) / (280 + 30) ≈ **0,37**.
- Grand rapport : (145 + 30) / (280 − 30) = **0,70**.

Cette plage assez large montre pourquoi nous n'utilisons pas 0,517857 comme une cote précise. Elle ne couvre même pas l'erreur de perspective, qui reste inconnue. Le nez entre B et A couvre horizontalement **335 pixels**, avec ±27 pixels de lecture aux extrémités ; ce n'est pas sa longueur réelle.

Pour obtenir des mètres, il faudra une dimension fiable dans le même plan et une méthode tenant compte de la perspective. Ne prends pas la taille d'une personne pour étalon. Les sept points sont des repères préparatoires ; des sections transversales mesurées restent nécessaires à une reconstruction dimensionnellement fidèle.

## 4. Lire les pièces qui existent déjà

Le même outil produit `releves.json`. Les axes de cette lecture sont : x vers la queue, y vers la droite, z vers le haut. Les valeurs suivantes viennent du **modèle**, pas d'un relevé sur le vrai planeur.

| Pièce | Limites x du modèle, m | Préparation de la reconstruction |
|---|---|---|
| Fuselage | 0 à 7,61 | Coque fixe ; reconstruire les sections avant sans arrondir les arêtes réelles du ventre |
| Pare-brise | 0,50 à 1,69 | Géométrie à rediviser en sections courbes ; candidat à intégrer à l'ensemble ouvrant après confirmation |
| Toit nommé verriere | 1,6648 à 2,13 | Objet séparé : ce nom ne prouve pas qu'il représente toute la verrière réelle |
| Vitrages latéraux | 1,55 à 3,16 | Déterminer les portions fixes et mobiles par comparaison avec les photos ouvertes |
| Raccord arrière | 2,13 à 3,16 | Examiner le raccord sous l'aile ; ne pas animer tout ce bloc automatiquement |
| Arceaux | 0,484 à 3,176 | Découper par fonction avant d'animer ; l'objet actuel regroupe plusieurs cadres |
| Contours de porte | 1,5475 à 2,7825 | Contours seulement ; ne constituent pas encore une porte ouvrante complète |

Le fuselage a une largeur maximale de modèle de **0,94 m**. Ce chiffre est une borne du maillage, pas une nouvelle mesure certifiée du SGS 2-33. Les limites complètes des onze objets sont archivées dans le rapport. La charnière, son axe et l'angle de butée restent inconnus : ils ne sont pas déduits de ces bornes.

## 5. Comparer dans FlightGear

Prépare une séance séparée selon l'[atelier22](22-verifications-visuelles.md#2-ouvrir-une-séance-de-contrôle), avec `--fdm=null`, lecture seule et port HTTP local. Dans notre séance41, le paquet est celui de **visuals-40**, FlightGear **2024.1.7**, à CYJN, heure de lancement fixée par le lanceur, rendu ALS actif. L'avion est immobilisé pour l'observation.

```powershell
python -m tools.reference_bench build/comparaison-41 --port 18150
```

Le programme refuse un avion autre que SW233 ou un modèle de vol actif. Il initialise les deux masses visuelles à 180 lb et les positions de profondeur/spoilers à zéro dans cette séance isolée ; ces valeurs d'essai ne sont pas une modification du FDM. Il utilise le banc existant pour sauvegarder et restaurer vues et options, puis rapproche la cible de la caméra sur l'avant et la restaure. Les fichiers `general/checks.json` et `details/checks.json` enregistrent les réglages réellement lus et les empreintes des captures. Ne touche pas aux vues pendant l'essai.

Six images montrent l'avant, l'arrière, deux profils, dessus et dessous. Trois autres montrent le nez de profil, l'avant en oblique et la verrière depuis le dessus. Ce sont des vues **comparables par sujet**, pas des caméras calibrées sur la photographie : nous n'en déduisons aucun pourcentage d'erreur géométrique.

![Vue générale de face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-41/avant.png)

![Nez et cockpit actuels de profil](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-41/nez-profil.png)

Sur EXT-02, le nez est arrondi et le sommet du vitrage suit un bombé. Dans cette capture, le nez termine en pointe anguleuse et le vitrage avant présente une longue pente presque droite. Le patin paraît fait de segments droits. Il faut travailler les formes, pas seulement les pixels du contour. Le côté du modèle est sombre : on utilise sa silhouette, sans comparer sa teinte à la photo.

![Avant actuel en oblique](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-41/nez-oblique.png)

Face à EXT-03, les grands panneaux plans du nez et les cassures du cadre apparaissent clairement. La transparence rend certains panneaux presque invisibles ; cela ne prouve pas l'absence de vitrage. Le cadre et la silhouette restent les indices à comparer.

![Verrière actuelle vue de dessus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-41/verriere-dessus.png)

L'aile masque une partie arrière : cette image n'est pas une vue exploitable de toutes les charnières. DET-03/05 montrent la verrière ouverte et des poignées rouges ; notre modèle reste fermé et fixe. Le but de cette séance est de préparer son découpage, pas de prétendre que l'ouverture existe déjà.

## 6. Transformer les observations en prochains travaux

| Zone | Observation | Action suivante |
|---|---|---|
| Nez | Pointe et pans trop marqués par rapport à EXT-02/03 | VIS-05b : ajouter des sections cohérentes, arrondir le dessus et l'avant |
| Ventre | Le réel présente aussi des cassures | Garder une séparation entre zones courbes et arêtes structurelles |
| Verrière | Longue pente plane et cadres anguleux | VIS-05c : reconstruire les sections, revoir l'épaisseur et le bombé |
| Jonction sous aile | Plusieurs objets se superposent visuellement | Clarifier panneaux fixes, raccord et ensemble ouvrant |
| Patin | Profil segmenté | VIS-05g.3 : relever et reconstruire sa courbe séparément |
| Ouverture | Axe réel non établi | Obtenir une vue de charnière et une séquence d'ouverture avant de fixer la cinématique |

**Bilan :** relevé photographique préparatoire, onze objets inventoriés, neuf captures natives et restitution des réglages des deux bancs vérifiée. Aucun changement de maillage, peinture, animation ou FDM. La prochaine réalisation est VIS-05b/c ; l'acceptation visuelle de l'avion reste ouverte.

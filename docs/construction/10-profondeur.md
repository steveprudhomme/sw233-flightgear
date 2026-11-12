# 10. Donner sa course à la profondeur

Objectif : faire bouger seulement l’arrière de l’empennage, puis vérifier que le dessin montre bien l’angle calculé. Séance réalisée le 12 novembre 2026 : FlightGear 2024.1.7 et banc indépendant JSBSim 1.2.3. Prévois deux séances : construction, puis essais. Le [protocole](../planification/aud-01b-profondeur.md) a été commité avant les modifications.

## 1. Préparer les trois pièces du puzzle

Ouvre les fiches [2](02-maillage.md), [3](03-vol.md) et [4](04-configuration.md). La première fabrique les pièces, la deuxième calcule les forces, la troisième fait bouger les pièces. Modifier seulement le dessin ne change pas le vol. Modifier seulement le calcul laisse un avion dont la queue paraît immobile.

Travaille dans la racine du dépôt, là où se trouve README.md. Garde un paquet initial dans un dossier distinct avant de modifier les recettes : l’outil de fabrication refuse d’écraser un paquet existant. Les recettes du livre contiennent maintenant la nouvelle version ; les anciennes se trouvent dans le commit `a1b9c2c`. Ne remplace pas tes fichiers actuels pour examiner cet historique.

## 2. Lire une mesure, sans la deviner sur une photo

Référence : *FAA Approved Flight Manual SGS 2-33*, fichier fourni dans les [références](../references/), page PDF 21, page imprimée 41, §8.3.4. Pour la configuration 1 040 lb, le débattement nominal est **23° vers le haut et 23° vers le bas**, avec tolérance ±2°. La configuration 1 080 lb possède une autre indication vers le haut : ne mélange pas les lignes. Nous retenons le nominal 23°, pas une valeur prise au hasard dans la tolérance.

Sur ta fiche de mesure, écris : source, page, configuration, unité, valeur, tolérance. Aucune longueur de charnière n’a été mesurée dans cette page. Une photo en perspective peut guider la forme mais ne fournit pas cette cote.

Le calculateur utilise des radians. Pour convertir, multiplie 23 par pi, puis divise par 180 : **0,4014257279586958 rad**. L’ancienne borne 0,30 rad représentait seulement **17,18873385°**. Dans la recette `dynamique.py` de la fiche 3, change le gain de `pitch-surface` et ses bornes ensemble. Les autres commandes conservent leurs propres gains. La recette génère `src/SW233/sw233.xml`.

La demande du manche et celle de compensation sont additionnées puis limitées. Une demande de 5 doit donner la même butée qu’une demande de 1. C’est une simplification du prototype, pas la reproduction d’un mécanisme de compensation réel.

## 3. Découper la queue en deux parties

Imagine une règle posée sur une feuille de carton : la partie devant la règle reste fixe ; la partie derrière peut pivoter. Dans `fabrique.py`, chaque demi-empennage était un seul polygone. La nouvelle recette le coupe au plan **x = 7,35 m**, avec charnière à **z = 0,11 m** et axe transversal. Ces coordonnées sont un choix de maquette à améliorer ; elles ne viennent pas d’une mesure constructeur. Le centre ancien à z = 0,10 m est ramené à 0,11 m afin que les sommets soient dans le même plan.

Lis la fonction `coupe` de la fiche 2. Pour chaque arête entre A et B :

1. Garde le point s’il est du bon côté de 7,35.
2. Si l’arête traverse la règle, calcule la fraction **t = (7,35 − Ax) / (Bx − Ax)**.
3. Place le nouveau point à **y = Ay + t × (By − Ay)** et z = 0,11.
4. Ferme le contour. Répète de l’autre côté pour fabriquer la partie mobile.

Exemple : entre x = 7,07 et x = 7,50, t vaut 0,28 / 0,43, soit environ 0,6512. Sur cette arête, y est constant : l’intersection garde le même y. Le code traite aussi les arêtes obliques. Il ne divise que lorsqu’une arête traverse la séparation.

Conserve les noms `empennage-1` et `empennage1` pour les parties fixes. Les parties mobiles s’appellent `profondeur-1` et `profondeur1`. Le maillage passe de 39 à 41 objets enfants. La transformation vers le fichier AC conserve la convention expliquée en fiche 2 : (x, y, z) devient (x, z, −y). Ne recopie pas les coordonnées AC comme si elles étaient celles du modèle XML.

## 4. Brancher l’angle réellement obtenu

Dans `sw233-model.xml`, deux animations `rotate` utilisent **fdm/jsbsim/fcs/elevator-pos-rad**. Cette propriété contient la déflexion effective, après limitation. Le facteur **57,29577951308232** convertit les radians en degrés. Un facteur 23 branché à cette propriété ferait une deuxième conversion incorrecte.

Les deux centres sont (7,35 ; 0 ; 0,11), l’axe est (0 ; 1 ; 0). Dans cette convention, une déflexion négative relève le bord arrière, une déflexion positive l’abaisse. Les noms des deux pièces fixes ne doivent pas figurer dans ces animations. Le livre donne les deux blocs complets en fiche 4 ; conserve son bloc de configuration principale séparé de celui du modèle.

Point d’arrêt : régénère le maillage et le FDM, puis compare les cinq fichiers reconstruits aux fichiers du dépôt :

```powershell
# Depuis la racine du dépôt ; choisir des dossiers de sortie encore inexistants.
python tools/check_workbook.py build/livre-profondeur
python tools/package.py --output build/essai-profondeur
```

## 5. Faire le banc visible dans FlightGear

Lance le paquet `build/essai-profondeur/Aircraft` avec les chemins de ton installation décrits dans [INSTALL](../../INSTALL.md). Sélectionne `sw233`, CYJN, départ au sol, vitesse nulle, vent nul ; ajoute `--httpd=18097`. Utilise une session dédiée : le banc déplace le manche et la caméra. Attends le chargement complet du décor. Ce contrôle est au sol ; ce n’est pas une démonstration de vol.

```powershell
# FlightGear doit déjà être lancé avec ce paquet et le serveur local actif.
python -m tools.elevator_bench build/photos-profondeur --port 18097
```

L’outil vérifie le nom de l’avion, JSBSim et l’initialisation ; il met la compensation à zéro. Il prend successivement neutre, haut et bas, relève la propriété avant et après chaque capture, puis restaure commandes, compensation et caméra même en cas d’erreur. Le cadrage est enregistré dans `native.json` : vue 0, offsets 0 / 1,4 / 10 m, cap relatif 0°, tangage −25°, champ 85°. L’image provient de FlightGear, sans retouche. La précision du serveur HTTP explique la lecture de 23,0000156° au lieu de 23 exactement ; la tolérance du banc est 0,001°.

Ancienne maquette : l’empennage ne possédait aucune partie mobile, même à la butée.

![Avant : queue monobloc dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/profondeur-11/avant-haut.jpg)

Nouvelle maquette au neutre : les deux parties se rejoignent dans le même plan.

![Après : profondeur au neutre](https://github.com/steveprudhomme/sw233-flightgear/releases/download/profondeur-11/apres-neutre.jpg)

Commande −1 : le bord arrière remonte, la surface mobile apparaît raccourcie depuis cette caméra arrière.

![Après : bord arrière relevé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/profondeur-11/apres-haut.jpg)

Commande +1 : le bord arrière descend. Compare sa position au fuselage et à la charnière, pas à l’horizon : le planeur repose incliné sur le sol.

![Après : bord arrière abaissé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/profondeur-11/apres-bas.jpg)

Si rien ne bouge, vérifie le paquet réellement chargé, les deux noms d’objets et la propriété. Si tout l’empennage tourne, tu as probablement relié les pièces fixes. Si l’angle est trop petit, vérifie l’unique conversion radians/degrés. Les images démontrent le fonctionnement de cette géométrie simplifiée ; elles ne prouvent pas son réalisme photographique.

## 6. Comparer le vol sans changer les règles

Le [banc de centrage](08-centrage.md) conserve 180 lb à l’avant et à l’arrière, masse totale 970 lb, altitude initiale 5 000 ft et vitesse 50 kt. Masse, CG, point de référence et coefficients aérodynamiques restent identiques. Lance le banc avec l’environnement Python contenant JSBSim :

```powershell
python -m tools.balance build/mesures-profondeur
```

| Mesure, cas biplace 970 lb | Avant | Après |
|---|---:|---:|
| Commande normalisée d’équilibre | −0,95517081 | −0,71383377 |
| Déflexion physique | −16,41817681° | −16,41817681° |
| Pente | −4,68513900° | −4,68513900° |
| Marge de commande normalisée | 4,4829 % | 28,6166 % |
| Altitude après 60 s | 4 557,68618 ft | 4 557,68618 ft |

La gouverne prend le même angle : c’est le même équilibre. Il faut simplement moins de course normalisée pour atteindre cet angle. N’écris donc pas « la finesse a été améliorée ». Les autres chargements et échecs du solveur figurent dans les CSV complets de la [publication](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/profondeur-11). Un équilibre nouvellement trouvé n’est pas une autorisation de centrage réel.

Le seuil numérique du solveur dans `tools/glide.py` a été resserré de 1e−6 à 1e−9 : le changement d’échelle de commande laissait un petit résidu de moment au-dessus du seuil d’un test. Nous avons augmenté la précision du calcul, sans assouplir le test ni modifier les coefficients.

## 7. Vérifier et ranger

Les 15 tests automatisés passent, dont deux nouveaux tests de profondeur : huit combinaisons manche/compensation, butées hors plage, conversion des animations et conservation de l’équilibre à 50 kt. La comparaison d’angle et de pente utilise six décimales. La reconstruction du livre doit également réussir. Les captures natives complètent les tests : un nombre correct ne suffit pas à prouver qu’une pièce bouge dans le bon sens.

Mets à jour ROADMAP, CHANGELOG, sources et validation ; conserve les mesures et images générées en pièces jointes de publication. Leur absence des sources évite d’alourdir chaque copie du dépôt. Ce lot repose sur une valeur du manuel et des essais de notre modèle ; son biais principal reste l’utilisation d’une charnière approximative et de coefficients historiques dont la référence physique n’est pas complètement identifiée. La prochaine étape proposée est AUD-01c : régler les masses des deux occupants dans le menu, avec recalcul visible du centrage.

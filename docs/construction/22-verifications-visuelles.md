# 22 — Vérifier un modèle, pas seulement fabriquer ses fichiers

Un fichier peut être bien écrit et donner une mauvaise image. Cette séance sert
à comparer les reflets, vérifier la peinture sur les ailes et observer les personnages
de près et de loin. Les captures viennent de FlightGear. Le planeur est immobilisé
pour ces comparaisons : ce n'est pas un nouvel essai de vol.

## 1. Préparer une boîte d'essai séparée

Ouvre un terminal dans le dépôt. Crée un paquet dans un dossier neuf :

```powershell
python tools/package.py --output build/visuel-40
```

Le dossier `src` contient tes sources. Le dossier `build/visuel-40` contient une
copie préparée pour FlightGear. Si tu changes une source, crée un nouveau paquet.
Ne modifie pas uniquement la copie puis oublie la recette : tu perdrais ta correction
à la prochaine construction.

## 2. Ouvrir une séance de contrôle

Les chemins suivants correspondent à l'installation Windows testée. Change seulement
les chemins si FlightGear est installé ailleurs. `--fdm=null` arrête le calcul du vol ;
`--read-only` et `--ignore-autosave` isolent cette séance des réglages enregistrés.
Le port HTTP sert aux outils de contrôle locaux.

```powershell
& 'C:/Program Files/FlightGear 2024.1/bin/fgfs.exe' `
  --fg-root='C:/Users/steve/FlightGear/Downloads/fgdata_2024_1' `
  --fg-aircraft="$PWD/build/visuel-40/Aircraft" `
  --fg-scenery='C:/Users/steve/FlightGear/Downloads/TerraSync' `
  --aircraft=sw233 --airport=CYJN --in-air --altitude=5000 --heading=010 `
  --start-date-gmt=2026:06:21:16:45:00 --wind=0@0 --disable-real-weather-fetch `
  --disable-terrasync --geometry=1280x720 --fdm=null --read-only --ignore-autosave `
  --enable-clock-freeze --httpd=18150 --prop:/sim/rendering/shaders/skydome=true `
  --prop:/sim/rendering/vsync-enable=false --prop:/sim/frame-rate-throttle-hz=0
```

Attends que le paysage soit chargé. Garde la fenêtre visible : une fenêtre réduite
peut produire une capture vide. Ferme tes anciennes séances d'essai avant de comparer
les performances. Deux simulateurs ouverts se partagent la puissance de l'ordinateur.
La séance sans calcul du vol ne crée pas les masses. Ouvre un deuxième terminal
au même endroit, puis copie cette commande. Elle initialise seulement notre séance
sans calcul du vol. Les nombres 180 sont des masses **d'essai en livres**,
pas les masses réelles des personnes portant ces noms.

Dans le Bloc-notes, crée `build/preparer-visuel.nas`, en UTF-8, avec ceci :

```javascript
// Seulement dans notre séance de maquette immobilisée.
if (getprop("/sim/aircraft") == "sw233" and getprop("/sim/flight-model") == "null") {
    setprop("/sim/freeze/master", 1);
    setprop("/fdm/jsbsim/inertia/pointmass-weight-lbs", 180);
    setprop("/fdm/jsbsim/inertia/pointmass-weight-lbs[1]", 180);
    setprop("/fdm/jsbsim/fcs/speedbrake-pos-norm", 0);
    setprop("/fdm/jsbsim/fcs/elevator-pos-rad", 0);
}
```

Puis envoie ce fichier à la fenêtre d'essai :

```powershell
python tools/flightgear.py build/preparer-visuel.nas --port 18150
```

Tu dois maintenant voir les deux occupants en vue extérieure. Pour piloter vraiment,
ferme cette séance et utilise le lancement normal du guide INSTALL : JSBSim fournit
alors les masses et les positions des commandes.

## 3. Changer une seule chose à la fois

Pour le verre, le [chapitre 19](19-realisme.md) compare trois forces : 0, 1 et le
réglage retenu. Deux orientations opposées de l'avion changent l'éclairage relatif.
Ce ne sont pas des mesures de l'angle exact entre le soleil et le pare-brise.

Pour la peinture, ouvre **SW233 → Grille UV / Texture grid**. Une grille droite
sur l'image peut devenir très étirée sur une pièce mal dépliée. Regarde le dessus,
le dessous et les spoilers. Puis désactive la grille pour retrouver la peinture.
La grille est un outil de travail, pas une décoration de l'appareil réel.

Pour les personnages, garde la même orientation et éloigne la caméra. Le niveau
détaillé sert près du cockpit ; le niveau simplifié sert quand les petits détails
ne sont plus visibles. Il faut éviter deux personnages superposés au changement.

## 4. Pourquoi le nombre d'images par seconde peut tromper

Si l'écran n'affiche que 60 images par seconde, deux modèles très différents peuvent
rester à 60. Cela ne prouve pas qu'ils coûtent la même chose. Notre essai demande la
désactivation de la synchronisation verticale dans cette séance seulement. Le pilote
graphique peut encore imposer une limite. On enregistre donc les paramètres et on
publie les mesures avec cette réserve.

En pause, `/sim/frame-rate` peut afficher zéro alors que l'image continue à être
dessinée. Le banc lit plutôt le compteur `/sim/frame-number`, attend un intervalle
mesuré, puis le relit. Exemple : 120 nouvelles images en 2 secondes donnent 60 images/s.
On répète les mesures et on compare plusieurs états dans un ordre alterné.

## 5. Filmer une présentation honnête

Le script `tools/visual_demo.py` enregistre directement des JPEG dans FlightGear.
Il refuse une séance qui calcule le vol : son rôle est une présentation statique
avec changement de vue et sortie/rentrée des spoilers. Il garde les réglages des vues
et les restaure à la fin. Il ne simule ni glissade ni vol piloté.

Après avoir préparé les propriétés du banc et une fenêtre visible :

```powershell
python -m tools.visual_demo build/film-visuel-40 --port 18150
ffmpeg -framerate 8 -i build/film-visuel-40/%04d.jpg -c:v libx264 -pix_fmt yuv420p -movflags +faststart build/presentation-visuelle-40.mp4
```

Les images sont jouées à huit images par seconde. Le fichier `record.json` conserve
les temps réels de capture et les commandes de spoilers. Cette vidéo sert à inspecter
les nouveautés ; elle ne mesure pas la fluidité maximale du simulateur.

## 6. Ce qui permet de cocher une étape

Une étape est finie lorsque son résultat est visible et vérifié, pas simplement
lorsque le programme ne donne pas d'erreur. Une photo manquante reste manquante.
Les badges de projet et la livrée provisoire restent identifiés comme tels. Les sources
et les inconnues sont expliquées dans les chapitres [20](20-livree.md) et [21](21-equipage.md).
Les résultats et les images de cette séance sont ajoutés après les essais ci-dessous.


## 7. Refaire les contrôles et lire leurs preuves

Utilise des dossiers neufs : les outils refusent d'écraser tes résultats précédents.
Pendant un banc, laisse-le seul déplacer les vues. Ne lance pas deux bancs ensemble.

```powershell
python -m tools.glass_bench build/verre-40 --port 18150
python -m tools.airframe_bench build/surfaces-40 --port 18150
python -m tools.visuals_bench build/personnes-40 --port 18150 --samples 3 --interval 1
```

Le premier essaie le verre ; le deuxième regarde la peinture et les pièces mobiles ;
le troisième change les occupants et la livrée. Chaque dossier contient les images
et un rapport JSON. Cherche `restored`: il doit être `true`, et la liste des erreurs
vide. Cela vérifie les propriétés enregistrées, pas toutes les préférences possibles.

**Attention à la distance !** Agrandir le champ de vision fait paraître l'avion plus
petit, mais ne l'éloigne pas. Pour vérifier le niveau de détail, notre banc déplace
réellement la caméra avec `z-offset-m`, de −25 à −100 m. Le champ de vision est ensuite
adapté pour comparer. Le changement des personnages se produit à 60 m de leur groupe.
Les bornes des deux versions sont identiques afin d'éviter une apparition double.

### Résultats du lot 40, sous Windows / FlightGear 2024.1.7

| Essai | Observation | Ce que cela ne prouve pas |
|---|---|---|
| Verre, deux caps et trois vues | Terrain, ficelle et instruments restent visibles | Reflets dynamiques du paysage |
| Sans ALS, séance séparée | Transparence conservée, cockpit plus sombre | Rendu identique à ALS |
| Peinture, dessus/dessous | Grille et peinture suivent les surfaces mobiles | Livrée actuelle exacte de C-FYLP |
| Caméra éloignée de 100 m | Motif parasite du ventre supprimé dans la comparaison | Absence de défaut à tous les angles |
| Noms rapprochés | R. PAGÉ et R. VACHON lisibles dans le bon sens | Uniformes et qualifications officiels |
| Présence des personnes | Aucun, avant seul, arrière seul et les deux observés | Nouveau calcul de masse ou de vol |

![Verre sans ALS, vue pilote](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/fallback-pilot.jpg)

Le paysage reste visible à travers le pare-brise. Le tableau plus sombre fait partie
de la différence de rendu observée, et n'a pas été éclairci dans l'image.

![Spoilers levés au-dessus des ailes](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/spoilers-open.jpg)

Les deux rectangles sont dressés. La vue presque de dessus les montre moins bien :
une pièce mince vue par sa tranche peut paraître être un simple trait.

![Nom avant après correction de l'orientation](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/crew-name-front.jpg)

![Nom arrière après correction de l'orientation](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/crew-name-rear.jpg)

Les noms sont plus faciles à lire en gros plan. La photo révèle un défaut qu'un
simple contrôle du fichier ne voyait pas : les lettres étaient auparavant inversées.

Le niveau simplifié contient **5 276 triangles**, contre **45 904** dans la version
fine. Cela réduit la géométrie de 88,5 %, mais ne garantit pas 88,5 % de vitesse en plus.
Les six états de présence ont des médianes entre 59,88 et 60,02 images/s. Malgré la
demande de désactiver la synchronisation verticale, le plafond reste proche de 60.
Le coût graphique isolé n'est donc pas établi.

**La vidéo :** 0–4 s extérieur ; 4–8 s spoilers extérieurs ; 8–12 s grille ;
12–16 s instruments ; 16–20 s vue latérale et spoilers ; 20–24 s arrière ;
24–28 s retour au poste avant. Les 224 JPEG natifs et leur chronologie sont archivés.
[Lire la vidéo dans le lecteur](https://steveprudhomme.github.io/sw233-flightgear/#visuel40).

**Bilan des fichiers :** 59 tests réussis, contrôle de style réussi, reconstruction
du livre identique. L'atlas contient 208 planches de pièces et 12 planches de groupes
LOD, soit 220 images. Ce sont des dessins calculés depuis nos pièces, et non des
photos du planeur réel. Les mains restent fixes, les cotes physiques manquantes
et les marquages non sourcés restent dans la feuille de route.

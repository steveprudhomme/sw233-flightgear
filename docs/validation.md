# Validation du prototype

Essai autonome JSBSim 1.2.3, Windows, Python 3.13, intégration à 120 Hz.
Chargement de référence : 970 lb. Départ à 5 000 ft MSL, 50 kt de vitesse calibrée,
atmosphère standard, sans vent, aérofreins rentrés. Le solveur de descente
détermine l’incidence, la pente et la commande de profondeur qui annulent les
accélérations longitudinales initiales. Le trim longitudinal standard JSBSim,
essayé sans propulsion, n'a pas convergé ; le solveur de cet essai est indépendant.

| Grandeur | Résultat du test |
|---|---:|
| Incidence initiale | 3,6684° |
| Pente initiale | −4,6851° |
| Commande de profondeur normalisée | −0,95517 |
| Finesse à ce point de fonctionnement | 12,20 |
| Vitesse calibrée à 60 s | 50,0012 kt |
| Altitude à 60 s | 4 557,69 ft MSL |

Reproduire : `python tools/glide.py --speed 50 --seconds 60`.

La finesse à **50 kt** n’est pas directement comparable à la finesse maximale
de **23 à 50 mph** que le manuel annonce en biplace. La profondeur est proche de
sa butée. Vérifier en priorité le centrage et l’autorité en tangage, puis balayer
la polaire à masse fixée. Ces essais ne valident ni une vrille ni un décrochage.

Les tests couvrent le vol stabilisé, les signes des commandes, la saturation,
l'effet des aérofreins, le contact au sol et l'intégrité du paquet. Le vol natif ci-dessous complète ces tests.

## Produire le film de télémétrie

Installer les dépendances de développement et FFmpeg avec l’encodeur libx264.
Depuis la racine du dépôt :

```sh
python -m pip install Pillow==12.0.0
python -m tools.video build/vol-plane.mp4
```

Le moteur avance à 120 Hz. Le film échantillonne les positions et les trois angles
d’attitude tous les 5 pas ; à 24 images/s, la lecture des 66 secondes est en temps réel.
Le rendu est indépendant du moteur graphique FlightGear. La distance nord est
calculée localement à partir de la latitude ; le terrain n’est pas géoréférencé.
Un fichier vidéo existant n’est pas écrasé. Le MP4 est un résultat généré, exclu de Git.

## Capture FlightGear à CYJN

Le scénario filmé commence juste au sud du terrain, à 2 300 ft MSL et 60 kt. Le vol passe au-dessus de l’aéroport vers 29 s (45,29445° N, 73,28158° O). Le décalage de caméra et l’heure solaire éclairent l’extrados depuis le côté de la caméra.

Le premier enregistrement de 66 s reste disponible dans la [publication précédente](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/demo-cyjn-01). Dans la prise actuelle de 83 s, le second cycle permet de voir réellement les panneaux sortir sur les ailes.

| Temps du nouveau film | Ce qu’on peut vérifier |
| --- | --- |
| 14–28 s | La commande de cockpit parcourt sa course, puis revient. |
| 29–43 s | Le même mouvement est répété, caméra au-dessus des deux ailes. |
| 46–61 s | La ficelle quitte le centre pendant l’entrée en glissade. |
| 61–73 s | Le planeur reste incliné en vue extérieure ; à 68 s, β vaut environ +4°, pour environ 16° de roulis. |
| 83 s | Retour à moins de 1° d’inclinaison et à moins de 0,1° d’angle β. |

**Vocabulaire.** La manœuvre filmée est une glissade : inclinaison à droite et palonnier opposé. β est une mesure de l’écoulement latéral, pas le nom de la manœuvre. Son signe seul ne suffit pas à distinguer une glissade d’un virage dérapé. Le bandeau sépare donc le nom de la manœuvre de la mesure.

Dans FlightGear, sélectionner la scène TerraSync incluant `Terrain/w080n40/w074n45/CYJN.btg.gz`. [CYJN est l’identifiant publié par la Ville](https://sjsr.ca/aeroport-municipal/). Le décor de la prise provient du [miroir TerraSync](https://flightgear.sourceforge.net/scenery/Terrain/w080n40/w074n45/.dirindex) ; il est installé séparément du paquet avion. Le décor ne reproduit pas nécessairement l’aménagement actuel.

Depuis la racine du dépôt, lancer une **session de test locale** avec le paquet installé, le décor activé et le serveur HTTP FlightGear accessible localement. Garder la fenêtre à 1280 × 720 pendant la prise. Pour la date et la lumière de cette prise :

```sh
fgfs --aircraft=sw233 --fg-aircraft=build/Aircraft --airport=CYJN --altitude=5000 --vc=60 --heading=010 --in-air --start-date-gmt=2026:06:21:16:45:00 --geometry=1280x720 --httpd=8094 --disable-real-weather-fetch --prop:/sim/presets/trim=true
```

Une fois en vol, lancer le scénario dans une seconde console. Il initialise le planeur une fois, agit sur les commandes et utilise l’enregistreur de FlightGear. Le fichier brut est écrit dans le répertoire de lancement ; utiliser un répertoire sans prise existante. Le scénario laisse la simulation en pause à la fin.

```sh
python tools/flightgear.py tools/native-demo.nas --port 8094
```

Pour ajouter le bandeau de télémétrie et le zoom sur le fil avec FFmpeg, fournir le journal de **cette même prise** contenant `SW233_SAMPLE` :

```sh
python tools/annotate.py SW233-CYJN-angles.mp4 fgfs.log SW233-CYJN-v2.mp4
```

Le zoom est un recadrage de l’enregistrement natif. Les angles des animations et la réponse de la ficelle sont des approximations de simulation, pas des mesures sur un 2-33 réel.

[Essai dynamique du compas à CYJN : protocole, film, trace et résultats](construction/07-essais.md#compas-en-virage). Les commandes agissent sur les gouvernes ; la rose suit le compas en service pendant les deux virages.

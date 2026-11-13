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

[Banc de l’anémomètre](construction/07-essais.md#banc-anemometre) : 40, 60, 85 et 120 kt, sans modifier les performances du planeur.

[Variomètre : banc à quatre valeurs et descente à CYJN](construction/07-essais.md#banc-variometre). Les mesures séparent taux de montée signé, indication et vitesse du planeur.

[Altimètre : banc visuel et pression à altitude constante](construction/07-essais.md#banc-altimetre). Le modèle de vol nul isole le second essai de toute trajectoire.


## Diagnostic de masse et de profondeur (AUD-01)

[Protocole illustré et résultats](construction/08-centrage.md), 12 novembre 2026. Sept cas autonomes JSBSim, dont trois sans équilibre trouvé, et trois chargements contrôlés dans FlightGear 2024.1.7. À 970 lb/50 kt, CG historique 88,651546 in, profondeur −0,955171 ; seulement 4,48 % de course disponible. Moment propre +1 168,4574 lb·ft compensant un transport de −1 168,4574 lb·ft. Les essais identifient la sensibilité au bras de levier, sans valider AERORP ni les coefficients.

Le menu natif affiche masse/CG mais aucune ligne éditable d'occupant. Le banc modifie les propriétés JSBSim dans une session dédiée puis restaure les masses. Le FDM source reste inchangé : l'alignement au datum constructeur et la pesée d'exemplaire manquent. Le diagnostic est réalisé ; l'acceptation de l'enveloppe réelle reste ouverte.

## AUD-01a : invariance et transport du moment

[Fiche 9](construction/09-reperes.md), 12 novembre 2026 : les 11 positions structurales translatées de +10 in conservent exactement le résultat longitudinal mesuré. AERORP avancé seul de 1 in change la commande de −0,955170809 à −0,897666390 ; le transport du moment propre restaure la commande initiale, avec un écart de 0,000294 ft après 60 s. Essais autonomes à 970 lb/50 kt ; formule de transport expérimentale limitée au vol symétrique. La capture native utilise FDM null et ne valide pas un vol. Le datum historique et la pesée de C-FYLP restent non identifiés ; FDM distribué inchangé.

## Profondeur ±23° — AUD-01b

Les valeurs de commande normalisée des essais antérieurs correspondent au gain historique de 0,30 rad. Le nouveau gain est 23° ; déflexion physique et pente à 970 lb / 50 kt sont conservées. Trois positions ont été capturées dans FlightGear au sol. Voir la [fiche 10](construction/10-profondeur.md) pour les données, images et limites.


## Occupants et centrage — 13 novembre 2026

AUD-01c : six chargements indépendants, huit états natifs et quatre conditions synthétiques du contrôle au sol. Captures FlightGear 2024.1.7 à CYJN ; boutons solo/biplace testés à la souris. Saisie non confirmée par l’automatisation initiale, puis confirmée par Steve avec les chiffres du haut (voir actualisation ci-dessous). [Détails et images](construction/11-occupants.md).


Actualisation clavier (13 novembre 2026) : saisie 200.125 validée par Steve avec les chiffres du haut, puis vérifiée dans JSBSim ; restauration des décimales corrigée. Utiliser un point décimal. Pavé numérique signalé inopérant avec Verr Num activé, suivi AUD-01d. [Preuve illustrée et limites](construction/11-occupants.md#10-confirmer-la-saisie-et-préserver-les-décimales).


## Installation déplacée — AUD-02a

Paquet copié dans un dossier neuf avec espaces et lancé par son propre lanceur sous Windows / FlightGear 2024.1.7. Chemin effectif confirmé, cockpit et menu capturés ; trois états de profondeur/aérofreins vérifiés ; instruments connectés. Entrée CMD vérifiée depuis un autre répertoire. 19 tests réussis. Contrôles et limites dans la [fiche 12](construction/12-installation.md). Pas de validation native Linux ni de nouvel étalonnage du FDM.

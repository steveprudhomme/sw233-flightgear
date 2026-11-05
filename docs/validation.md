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
l'effet des aérofreins, le contact au sol et l'intégrité du paquet. Le rendu
FlightGear, ses commandes et le chargement depuis le lanceur restent à vérifier.

## Produire le film de télémétrie

Installer les dépendances de développement et FFmpeg avec l’encodeur libx264.
Depuis la racine du dépôt :

```sh
python -m pip install Pillow==12.0.0
python -m tools.video build/vol-plane.mp4
```

Le moteur avance à 120 Hz. Le film échantillonne les positions et les trois angles
d’attitude tous les 15 pas ; à 24 images/s, la lecture est accélérée trois fois.
Le rendu est indépendant du moteur graphique FlightGear. La distance nord est
calculée localement à partir de la latitude ; le terrain n’est pas géoréférencé.
Un fichier vidéo existant n’est pas écrasé. Le MP4 est un résultat généré, exclu de Git.

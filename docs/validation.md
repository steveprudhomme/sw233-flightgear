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


## Lot visuals-39 — 17 novembre 2026

Paquet construit depuis le commit `9490ec4`, essayé sous FlightGear 2024.1.7 Windows.
[Paquet, captures, atlas et rapports](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/visuals-39).

- Comparaison native des forces 0, 1 et réglées (0,25 verrière / 0,12 cadrans),
  en trois vues. ALS actif, image de ciel statique, aucune réflexion du terrain réel.
- Clics souris natifs : calage 29,92 → 29,93 inHg ; COM1 répond à son bouton fin
  (valeur finale lue : 118,325 MHz). Réglages remis ensuite aux valeurs de test.
- Six états visuels : aucun équipage, deux occupants, avant seul, arrière seul,
  ailes fictives activées, livrée désactivée. Les quatre présences et la livrée ont
  été vérifiées sur les images ; la petite aile de poitrine est trop loin pour
  certifier sa lisibilité sur ces captures.
- Mesure du compteur `/sim/frame-number` par temps monotone, huit intervalles
  d'une seconde par état : médianes de 59,98 à 60,01 images/s. La propriété
  `/sim/frame-rate` reste à zéro en pause et n'est pas utilisée comme mesure.
  Le plafond proche de 60 Hz empêche de conclure à un coût nul des nouveaux objets.
- Visage et manches raccordés après la première inspection ; cou avant caché
  avec la tête en vue pilote. Les mains restent fixes, les silhouettes sont artistiques.
- Paquet final ouvert avec **JSBSim**, au sol à CYJN : masses avant/arrière
  180/180 lb, visibilité active, nouvelle plaque C-FYLP lisible. Le planeur repose
  incliné au sol ; cet essai confirme le chargement, pas la validité des contacts.
- 35 tests automatisés réussis, Ruff et contrôle des sources réussis ; reconstruction
  complète du tutoriel identique, avec les trois recettes panel/livery/crew.

Les comparaisons de rendu utilisent une séance dédiée `--fdm=null`; elles ne valident
pas le vol. Les bancs restaurent les propriétés enregistrées dans leurs rapports, vérification incluse
aux rapports. Les journaux du lancement JSBSim en lecture seule signalent notamment
l'absence de moteur et l'impossibilité d'enregistrer l'état FDM initial ; aucune
validation nouvelle du moteur de vol n'est déduite de ce lot.

![Paquet final au sol, plaque C-FYLP](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-39/release-cockpit.jpg)

Les 184 planches de l'atlas sont des projections de géométrie, pas des photographies.
Les JPEG de FlightGear sont des captures natives. Le dossier de références explique
pourquoi la peinture et les insignes sont provisoires. Les limites restantes sont
conservées au [ROADMAP](../ROADMAP.md).


## Lot visuals-40 — 17 novembre 2026

Sources du paquet : `2644c12`. [Paquet, vidéo, atlas et preuves](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/visuals-40).
Les étapes et leurs images sont expliquées dans l'[atelier 22](construction/22-verifications-visuelles.md).

- Plan préalable `91daadc`, complément de centrage `e165262`, intégration `2644c12`.
- Verre inchangé depuis le lot39, vérifié sur ce paquet par une matrice étendue :
  deux caps (10/190°), trois vues, forces 0/1/réglées, 54 échantillons. Cadence
  médiane 60,00 images/s ; plafond encore présent malgré la demande sans vsync.
- Séance séparée sans ALS sur la peau corrigée : vitrage transparent, cockpit plus
  sombre. Préférences utilisateur non enregistrées. Aucune promesse d'identité visuelle.
- Dix états des surfaces : grille/peinture dessus/dessous, spoilers, profondeur
  et distances 25/100 m. Les surfaces copiées suivent leurs charnières. Le scintillement
  du ventre observé à 100 m a conduit à remplacer la peau plutôt qu'à la superposer.
- Six états de visibilité sur le candidat final : aucun, deux, avant seul, arrière
  seul, ailes fictives, livrée désactivée. Images des présences inspectées ; petite
  aile trop éloignée pour certifier sa lisibilité dans ce banc. Médianes 59,88–60,02
  images/s, trois intervalles par état. Aucun gain FPS attribué au LOD sur ces mesures.
- Deux niveaux de détail : 45 904 / 5 276 triangles ; bornes appariées, seuil 60 m.
  Les captures loin/proche et les tests ne montrent pas de duplication. Mains fixes,
  dégagement au-dessous mesuré par rapport à la coque, faute de plancher distinct.
- Noms corrigés en miroir après inspection, puis relus dans de nouveaux gros plans.
- Paquet final lancé avec JSBSim à CYJN, chemin propre confirmé, masses 180/180 lb,
  équipage actif, grille désactivée ; aperçu et description actualisés. Au sol le
  planeur reste incliné : les contacts ne sont pas validés par ce lot.
- Journaux : messages absence de moteur/son et sauvegarde FDM impossible en lecture
  seule, ainsi que TerraSync désactivé par ce mode ; terrain déjà chargé. Ils ne sont
  pas présentés comme une absence générale d'avertissements.
- 59 tests réussis ; Ruff, contrôle des sources et reconstruction exacte du livre réussis.
- Film natif de 224 images, 28 s à 8 images/s ; présentation statique sous FDM null,
  sans validation nouvelle d'une glissade. Rapports de restauration sans erreur.
- Atlas : 208 planches individuelles et 12 groupes de LOD. Sources éditables dans
  Git ; sorties et images générées dans les pièces jointes de la publication.

![Paquet 40 chargé avec JSBSim à CYJN](https://github.com/steveprudhomme/sw233-flightgear/releases/download/visuals-40/release-cockpit.jpg)

Les photos récentes complètes de C-FYLP, grades et insignes exacts restent attendus.
Le coût GPU hors plafond, les autres plateformes et la fidélité aérodynamique ne
sont pas certifiés par ces essais visuels.

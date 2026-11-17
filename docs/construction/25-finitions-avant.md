# 25 — Finir le nez, les flancs et les cadres

**Objectif :** comparer une maquette à des photos, comprendre ce qui ne ressemble
pas encore au planeur, puis corriger les pièces et vérifier le résultat.
Le plan de ce lot43 a été commité sous `ece5146` **avant** de changer le modèle.

Les dimensions ci-dessous sont des choix de maquette. Nous n'avons pas obtenu de
nouvelle cote constructeur. Les photos EXT-02/03 et DET-03/05 montrent plusieurs
appareils : on peut y observer la construction, mais pas mélanger leurs immatriculations.

## 1. Regarder avant de déplacer un point

Ouvre les originaux conservés dans `docs/references/originaux/`. Regarde d'abord
EXT-02 de côté, puis EXT-03 en biais. Enfin, observe DET-03/05 avec la verrière ouverte.
À chaque fois, cache mentalement la décoration pour regarder la silhouette.

| Ce que montre la photo | Écart du lot42 | Correction du lot43 |
|---|---|---|
| Un nez plein et arrondi, EXT-02 | Pointe basse et capot presque plat | Remonter et bomber le capot, arrondir la terminaison |
| Une coque assez haute sous les coudes, EXT-02 | Bordure trop basse dans notre interprétation | Remonter le bord de quelques centimètres |
| Un raccord sous l'aile, EXT-02/03 | Toit retombant avant la fin du cockpit | Maintenir le toit arrière, prolonger la partie opaque |
| Cadres bleus avec joint sombre et fixations, EXT-03/DET-03 | Tubes jaunes sans détail | Cadres bleus, joints, têtes de fixation et poignée visible |

Nous ne mesurons pas une longueur réelle avec la taille d'une personne sur la photo.
L'appareil est vu en perspective : ce qui est plus proche paraît plus grand.
La [fiche de comparaison](../references/finitions-43.md) distingue observation et estimation.

![Ancien profil du lot42](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/avant-nez-profil.png)

![Profil corrigé du lot43 dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/apres-nez-profil.png)

## 2. Comprendre les quatre tables de forme

Ouvre `tools/airframe_geometry.py`. Son bloc complet, à copier depuis zéro, est dans
la [fiche24](24-formes-avant.md#7-écrire-la-recette-complète). La fiche02 fournit
`poly`, qui pose une face, et `rod`, qui construit une baguette.

- `HULL` décrit les tranches du bas de coque et les bords du cockpit.
- `NOSE` décrit la hauteur du capot au-dessus de ces bords.
- `CANOPY` décrit le verre entre x = 0,70 et 3,16 m.
- `FAIRING` décrit la hauteur de la partie opaque derrière le cockpit, jusqu'à x = 5 m.

Imagine quatre patrons en carton. Ils n'ont pas besoin d'avoir les mêmes repères :
la recette rassemble leurs positions dans `knots`, puis insère les tranches intermédiaires.
Ainsi une limite de verre ne tombe pas au milieu d'une face de coque.

## 3. Donner du volume au nez

Le nez du lot42 était plus lisse qu'avant, mais encore trop aplati. Ajouter beaucoup
de triangles à une mauvaise courbe ne change pas sa forme générale ! Il faut donc
modifier les valeurs qui guident la courbe.

| Position x | Bord de coque `sill` | Hauteur ajoutée par `NOSE` | Sommet calculé |
|---|---:|---:|---:|
| 0 m | −0,120 m | 0,008 m | −0,112 m |
| 0,10 m | 0,035 m | 0,070 m | 0,105 m |
| 0,22 m | 0,090 m | 0,130 m | 0,220 m |
| 0,50 m | 0,120 m | 0,160 m | 0,280 m |
| 0,70 m | 0,120 m | 0,140 m | 0,260 m |

**À toi de vérifier :** à x = 0,22 m, additionne 0,090 et 0,130. Tu retrouves 0,220 m.
Le sommet se calcule dans le modèle ; il n'a pas été mesuré sur la photo.
La première tranche est minuscule : demi-largeur de 8 mm. Elle ferme l'extrémité,
sans laisser un trou et sans imposer un gros disque plat au bout du nez.

Le départ du verre passe de x = 0,50 à **0,70 m**. Les points du capot et ceux du verre
utilisent la même tranche de raccord. Le tableau reste à x = 0,87 m : il n'est pas déplacé.

![Coque et nez seuls](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-fuselage.png)

## 4. Rehausser les flancs sans arrondir tout le ventre

À x = 1,55 m, le bord du cockpit passe de 0,09 à **0,12 m** : une hausse de 3 cm.
À x = 2,13 m, il passe de 0,10 à **0,13 m**. Les largeurs principales restent identiques.
Les cassures du dessous sont conservées : elles évoquent la structure visible sur EXT-02.

Cette modification change aussi le haut des contours de porte. Ils réutilisent les
valeurs `HULL`, donc leurs points supérieurs suivent les nouveaux bords. Les portes
restent fixes. Nous n'avons pas inventé un axe de charnière pour pouvoir les animer.

![Contour gauche](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-contour-porte-1.png)

![Contour droit](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-contour-porte1.png)

## 5. Éviter le toit en forme de tente

À x = 3,16 m, l'ancien sommet était `0,10 + 0,14 = 0,24 m`.
Le nouveau vaut `0,13 + 0,54 = 0,67 m`. Le raccord reste ainsi près du dessous de l'aile.
La table `FAIRING` fait ensuite descendre la surface vers le fuselage arrière : hauteur
ajoutée de 0,50 m à x = 3,56 ; 0,25 m à x = 4,20 ; zéro à x = 5.
Ces valeurs sont estimées ; cette pente devra pouvoir évoluer avec des relevés physiques.

L'ancienne cloison de fermeture à x = 3,16 est retirée de l'enveloppe extérieure.
La peau supérieure continue jusqu'à la queue. Sa dernière tranche partage tous ses
points avec le bouchon arrière : une couture avec 33 points ne doit pas rencontrer
une autre couture qui n'en possède que deux.

![Raccord opaque sous et derrière l'aile](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-raccord-arriere.png)

![Pare-brise](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-pare-brise.png)

![Toit vitré](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-verriere.png)

![Vitrage droit](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-vitrage-droit.png)

![Vitrage gauche](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-vitrage-gauche.png)

## 6. Construire cadres, joints et fixations

Les photos montrent une bande bleue et un joint sombre, pas seulement une ligne jaune.
La palette de la fiche02 ajoute `cadres-bleus` à la position 14, après les autres matières.
`FRAME_MATERIAL = 14` choisit cette matière. Ne déplace pas une couleur au milieu de la
palette : les pièces qui utilisent son numéro pourraient changer de couleur !

La fonction `trim` construit deux baguettes : un cadre de rayon **14 mm** et un joint
de rayon **18 mm**, décalé de **16 mm vers l'avant**. Ce décalage fait apparaître une
bordure sombre sans poser deux surfaces exactement au même endroit. Ces épaisseurs
et cette section arrondie sont une représentation simplifiée, pas le profil réel du métal.

Une fixation a un rayon de **3,5 mm**, et une saillie de 7 mm. Une tête apparaît tous
les quatre points de chaque arceau. Ce rythme est un choix lisible ; le nombre de vis
réelles n'a pas été relevé. Les vis utilisent la matière inox déjà présente.

![Arceaux bleus](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-arceaux.png)

![Bordures bleues](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-bordures-cockpit.png)

![Longerons](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-longerons-verriere.png)

![Joints sombres](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-joints-verriere.png)

![Fixations métalliques](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-fixations-cadres.png)

Une petite poignée bordeaux représente le détail visible près du bord gauche. Trois
segments relient quatre points, avec un rayon de 6 mm. Elle est **fixe et non cliquable**.
Elle ne prétend pas reproduire le ressort, le verrou ou leur fonctionnement.
Les charnières et leur course restent dans VIS-05c.1 à c.3.

![Poignée de représentation](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-poignee-verriere.png)

## 7. Raccorder le mât et la peinture au nouveau capot

Le mât du lot42 se retrouverait à l'intérieur du capot plus haut. Dans la fiche02,
on ajoute **0,30 m** à la hauteur de tous ses points : embase, tube, attache et fil.
Dans `sw233-model.xml`, le centre de rotation du fil monte aussi : z passe de
**0,237 à 0,537 m**. Les valeurs x et y restent identiques. Oublier le centre ferait
balayer la ficelle autour d'un point resté plus bas ! La forme du mât reste à détailler
séparément dans VIS-05g.1 ; ici nous corrigeons seulement son raccord au nez.

![Embase](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-embase-pitot.png)

![Tube](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-tube-pitot.png)

![Attache du fil](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-attache-laine.png)

![Fil de laine](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/piece-fil-de-laine.png)

Le haut du nez dépasse l'ancienne zone de texture. Dans `tools/livery.py`,
`Y_RANGE` devient `(-0.63, 0.32)`. Cette marge couvre le nouveau sommet de 0,28 m.
Les marques sont toujours dessinées à leurs positions dans le modèle : on agrandit
le papier qui les reçoit. La [fiche20](20-livree.md) contient la recette mise à jour.
La grande zone bleue du ventre reste la peinture provisoire ; elle n'est pas la
livrée éclair demandée, qui possède sa tâche VIS-05h.

## 8. Reconstruire depuis ton établi

Après avoir copié les blocs actualisés des fiches02, 04, 20 et 24 dans *Mon-Schweizer* :

```powershell
.\.venv\Scripts\python.exe fabrique.py
.\.venv\Scripts\python.exe dynamique.py
```

Dans une copie complète du dépôt, vérifie la reconstruction dans un dossier nouveau :

```powershell
python -m tools.check_workbook build/verification-lot43
python -m unittest discover -s tests -v
```

Le premier contrôle compare les fichiers reconstruits à ceux du projet. Le second
vérifie notamment les coutures, la symétrie, les surfaces, la texture et le pivot du fil.
Un dossier de vérification déjà existant doit recevoir un autre nom.

## 9. Comparer dans FlightGear et avec les photos

Installe `sw233-finitions-43.zip` depuis la [version publiée](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/finitions-43),
en suivant la [fiche12](12-installation.md). Regarde le profil, l'avant et les deux
obliques. Passe en vue pilote : instruments et cartes doivent rester lisibles.
La capture utilise le champ normal de **80°** pour voir aussi le mât et la ficelle.

![Vue pilote](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/cockpit.png)

![Cadres dans FlightGear](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/cadres.png)

![Grille de contrôle de texture](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/grille.png)

Pour refaire les captures techniques, le mainteneur lance une séance **séparée** avec
FDM nul, heure figée et interface HTTP locale. Les commandes du banc sont :

```powershell
python -m tools.reference_bench build/vues43 --port 18160
python -m tools.finishing_bench build/details43 --port 18160
```

Pour ouvrir cette session, reprends la commande complète de la [fiche22, préparation](22-verifications-visuelles.md), avec le dossier du nouveau paquet et le port `18160` à la place de son ancien port. Ouvre ensuite un second terminal dans le dépôt.

Ces commandes exigent une session SW233 de développement déjà ouverte sur ce port ;
elles ne lancent pas FlightGear. Elles immobilisent l'appareil pour examiner la forme,
puis restaurent les réglages de vue. Il ne faut pas les lancer pendant un vol personnel.
Le rapport enregistre les paramètres ; un essai d'affichage ne prouve pas une qualité de vol.

![Première orientation de lumière](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/lumiere-a.png)

![Orientation opposée de lumière](https://github.com/steveprudhomme/sw233-flightgear/releases/download/finitions-43/lumiere-b.png)

La deuxième orientation tourne le planeur de 180° et compense le décalage de caméra.
On conserve l'heure. Il s'agit d'un contrôle sous deux directions relatives de lumière,
pas de deux heures de la journée ou d'une mesure de réflexion.

Pour comparer les photos locales aux images natives, télécharge les captures de la
version dans `build/images43`, puis lance :

```powershell
python -m tools.finishing_gallery build/comparaison43 --captures build/images43
```

Ouvre `build/comparaison43/index.html` dans ton navigateur. Chaque photo originale est
à côté d'une capture. Les images ne sont pas retouchées. Les cadrages et perspectives
restent différents : on compare la construction, sans prétendre superposer des cotes.
La galerie exige les originaux locaux ; ils ne sont pas inclus dans le paquet public.

## 10. Lire les résultats sans exagérer leur portée

Les essais ont été effectués sous FlightGear 2024.1.7, à CYJN, en 1280 × 720 pixels.
Le contrôle numérique donne au minimum environ **13,0 cm devant et 15,0 cm derrière**
entre les points échantillonnés des têtes et le toit. Ce n'est pas une certification de
collision : seules les positions et les points testés sont couverts.

Quinze objets existants changent ; trois apparaissent : joints, fixations, poignée.
Les coordonnées des ailes, gouvernes, tableau et le fichier du modèle de vol sont
inchangés. Le contrôle du fil teste les deux sens d'écoulement et son pivot dans l'attache.
L'atlas rassemble **80 pièces**. Ses images sont des dessins du maillage, tandis que
les vues extérieures et cockpit sont des captures natives du simulateur.

La finition statique est livrée pour revue. La fermeture géométrique est testée,
mais la ressemblance exacte attend toujours ton avis et de meilleures cotes.
La verrière ne s'ouvre pas encore : charnières, verrou et animation restent à réaliser.
La suite de la reconstruction extérieure est **VIS-05d : ailes et haubans**.

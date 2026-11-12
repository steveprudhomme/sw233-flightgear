# 8 · Comprendre le centrage avant de régler la profondeur

Séance AUD-01, commencée le 11 novembre et documentée le 12 novembre 2026. **But : expliquer un résultat du prototype, pas établir le chargement d'un vrai planeur.** Le fichier de dynamique de vol reste inchangé pendant cette enquête.

## 1. Prépare une fiche de lecture

Un centre de gravité est le point où l'ensemble pourrait tenir en équilibre, comme une règle posée sur un doigt. Le « datum » est le zéro choisi pour mesurer les distances. Un nombre en pouces n'est comparable à un autre que si leurs zéros et directions sont les mêmes.

Ouvre le manuel FAA fourni, dont l'empreinte est dans [l'inventaire](../references/inventaire.md). Compte les pages PDF depuis 1 ; chaque image montre deux pages imprimées. Recopie les valeurs suivantes avec leurs unités, sans mesurer des pixels sur la photo du cockpit :

| Page PDF / imprimée | Ce que tu lis | Ce que tu en fais |
|---|---|---|
| 14 / 27, §6.1 | Datum situé 66,34 in devant le bord d'attaque à l'emplanture ; intervalle 78,20 à 86,10 in derrière ce datum | Définir la règle de référence du manuel ; pas encore celle du FDM historique. |
| 14 / 27, §6.2 | Siège avant 43,80 in ; arrière 74,70 in pour 2-33/2-33A | Garder séparées les valeurs du 2-33B indiquées entre parenthèses. |
| 5 / 8, §1.3 | 1 040 lb pour 2-33/2-33A ; 1 080 lb sous conditions précisées | Ne pas attribuer le kit d'augmentation de masse à C-FYLP sans preuve. Le poids à vide « standard » n'est pas sa pesée. |
| 15 / 28–29 | La masse à vide et son centrage sont propres à l'exemplaire ; formulaire d'exemple | Ne pas transformer l'exemple n° 369 en fiche de C-FYLP. |
| 21 / 41, §8.3.4 | Profondeur version 1 040 lb : 23° ±2° vers le haut et vers le bas | Comparer à la limite actuelle 0,30 rad = 17,19°. Une limite de course ne fournit pas le coefficient aérodynamique de la gouverne. |

Les pages 14, 15 et 21 ont été rendues en images et relues visuellement. Le texte extrait automatiquement confond certains chiffres : la lecture du tableau et des unités prime. Les originaux tiers restent dans le fonds local ; cette fiche publie nos relevés et nos propres captures.

**Point d'arrêt :** retrouve toi-même 43,80 et 74,70 à la page imprimée 27. Soustrais : 74,70 − 43,80 = **30,90 in** entre les deux positions de charge. Le prototype utilise 85 − 43 = **42 in**. Déplacer seulement le zéro de la règle ne peut pas expliquer cette différence de distance.

## 2. Calcule avant de lancer le simulateur

Ouvre `src/SW233/sw233.xml`. Dans `mass_balance`, relève la masse à vide 610 lb et sa position x = 103,2 in. Puis relève les deux occupants de 180 lb, aux positions 43 et 85 in. Ce sont les valeurs **héritées du prototype**, pas des mesures de C-FYLP.

Fais trois multiplications :

| Élément | Poids × position | Moment de pesée |
|---|---|---:|
| Planeur vide | 610 × 103,2 | 62 952 lb·in |
| Occupant avant | 180 × 43 | 7 740 lb·in |
| Occupant arrière | 180 × 85 | 15 300 lb·in |
| Total | 610 + 180 + 180 = 970 lb | 85 992 lb·in |

Divise le dernier moment par le poids total : **85 992 / 970 = 88,651546 in**. C'est le centrage longitudinal calculé du prototype. Ne le compare pas directement à 86,10 in pour annoncer un dépassement réel : l'alignement entre son repère historique et le datum du manuel n'est pas établi.

Sans occupant arrière, recommence : (62 952 + 7 740) / (610 + 180) = **89,483544 in**. Le nombre augmente, donc le CG recule dans le repère du FDM. C'est cohérent : le siège arrière à 85 in était encore en avant du CG du planeur vide à 103,2 in.

## 3. Vérifie ces nombres dans FlightGear

Construis le paquet selon la fiche 7. Depuis la racine du dépôt, lance une **session de test dédiée**, au sol à CYJN, avec JSBSim et le décor installé. Adapte seulement le chemin du programme si `fgfs` n'est pas dans ton terminal :

```powershell
fgfs --aircraft=sw233 --fg-aircraft=build/Aircraft --airport=CYJN --on-ground --vc=0 --wind=0@0 --turbulence=0 --disable-real-weather-fetch --start-date-gmt=2026:06:21:16:45:00 --geometry=1280x720 --httpd=18097
```

Attends que la scène soit chargée. Ouvre **Equipment → Fuel and Payload** (le libellé peut être traduit). Dans la version testée, le menu montre la masse et le CG mais **aucune ligne d'occupant** : les masses existent dans JSBSim sans être exposées par cette interface. Ne cherche donc pas un champ invisible.

![Deux occupants de 180 lb : la fenêtre native affiche 970 lb et 88,65 in. La zone Payload reste vide.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/centrage-09/chargement-180-180.jpg)

Pour reproduire les trois captures, ouvre un second terminal dans le dépôt et utilise l'environnement Python installé pour les tests :

```powershell
.\.venv\Scripts\python.exe -m tools.balance_native build/mes-captures-centrage --port 18097
```

Le dossier de sortie doit être nouveau. Le script ouvre le dialogue et change les deux propriétés **de cette session de test seulement** : `/fdm/jsbsim/inertia/pointmass-weight-lbs` et son élément `[1]`. Il attend le nouveau poids et le nouveau CG, vérifie les nombres, prend l'image et restaure les poids de départ même en cas d'erreur. Il ne modifie ni le XML ni les réglages personnels des commandes.

![Un occupant avant de 180 lb : regarde Gross Weight 790 lb et Center of Gravity 89,48 in.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/centrage-09/chargement-180-0.jpg)

![Répartition 140 lb devant et 220 lb derrière : même poids total de 970 lb, CG à 90,38 in.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/centrage-09/chargement-140-220.jpg)

Captures natives FlightGear **2024.1.7**, à CYJN au sol, 1280 × 720. Elles vérifient le **calcul de masse**, pas une trajectoire ni les contacts au sol. L'inclinaison visible fait partie de la pose du prototype au sol ; elle ne sert pas à mesurer le centrage. Les trois lectures brutes concordent à moins de 0,00001 in avec le calcul indépendant ; le dialogue arrondit à deux décimales. [Relevé natif](https://github.com/steveprudhomme/sw233-flightgear/releases/download/centrage-09/native.json).

**Dépannage.** Une connexion refusée signifie que le serveur local n'est pas prêt ou que le port diffère. Une masse qui ne change pas peut indiquer une simulation en pause : reprends-la. Ne remplace pas JSBSim par `--fdm=null` pour cet essai, car nous voulons le calcul des masses du moteur.

## 4. Isole l'effet du centrage

Pour comprendre une cause, change une seule chose à la fois. Compare d'abord 220 + 140 lb à 140 + 220 lb. Le total reste 360 lb, mais une partie de la charge se déplace vers l'arrière. Le programme `tools/balance.py` recharge le modèle pour chaque cas et compare son centrage à la somme des moments calculée indépendamment depuis le XML.

Lance :

```powershell
.\.venv\Scripts\python.exe -m tools.balance build/mon-banc-centrage
```

Il produit `balance.csv` et `balance.json`. C'est un essai **JSBSim autonome 1.2.3**, pas un film FlightGear. Conditions : 5 000 ft MSL, 50 kt CAS, vent et turbulence nuls, aérofreins rentrés, compensation de profondeur nulle. Le solveur cherche incidence, pente descendante et commande de profondeur qui annulent les accélérations longitudinales et angulaire initiales. Il ne demande pas un palier sans moteur.

| Charge avant / arrière | Total lb | CG historique in | Commande profondeur | Course disponible avant butée | Résultat à 50 kt |
|---|---:|---:|---:|---:|---|
| 180 / 0 | 790 | 89,4835 | −0,7123 | 28,77 % | Équilibre trouvé |
| 180 / 180 | 970 | 88,6515 | −0,9552 | 4,48 % | Équilibre trouvé |
| 220 / 140 | 970 | 86,9196 | — | — | Non trouvé en 15 itérations |
| 140 / 220 | 970 | 90,3835 | −0,8556 | 14,44 % | Équilibre trouvé |
| 220 / 210 | 1 040 | 86,7904 | — | — | Non trouvé en 15 itérations |

La marge est `100 × (1 − valeur absolue de la commande)` ; ce n'est ni une marge de stabilité ni une réserve certifiée. Une absence de solution trouvée ne prouve pas qu'aucun équilibre physique n'existe : elle décrit l'échec de ce solveur borné à ce point d'essai. On conserve ces lignes au lieu de les effacer.

Pour les trois cas source convergents, le programme laisse ensuite évoluer le modèle **60 s sans pilote automatique**. Les vitesses finales sont respectivement 49,9983, 50,0012 et 50,0001 kt ; les altitudes 4 555,33, 4 557,69 et 4 565,88 ft. Cela vérifie une descente locale stable dans ces conditions, pas toute l'enveloppe de vol.

## 5. Comprends pourquoi il faut autant de profondeur

Imagine une porte : la même poussée ne la fait pas tourner autant selon sa distance aux charnières. Ici, les forces aérodynamiques sont appliquées au point **AERORP**, x = 103,2 in, tandis que le CG chargé est à 88,6515 in. Il existe donc un bras de levier de **14,5485 in**.

Les [repères JSBSim](https://jsbsim-team.github.io/jsbsim-reference-manual/user/concepts/frames-of-reference/) donnent x vers l'arrière et z vers le haut pour les positions structurales. Le repère des forces a x vers l'avant et z vers le bas. Notre banc convertit les distances en pieds et vérifie le moment transporté avec `My = rz × Fx − rx × Fz`, où `rx = (CGx − AERORPx) / 12` et `rz = (CGz − AERORPz) / 12`.

Au point biplace 180/180 :

| Contribution | Moment de tangage lb·ft |
|---|---:|
| Moment calculé par la formule aérodynamique au point AERORP | +1 168,4574 |
| Effet du transport des forces de ce point au CG | −1 168,4574 |
| Somme lue au CG | environ −0,000000082 |

Les deux grands termes se compensent. Le banc compare leur somme au résultat JSBSim à 0,000001 lb·ft près. La profondeur de **−16,418°** contribue au moment positif nécessaire ; le débattement du prototype est limité à environ ±17,189°. Voilà une explication mesurée de la faible réserve de commande, sans affirmer que le point AERORP représente correctement le vrai appareil.

## 6. Fais deux expériences, sans les confondre avec des corrections

Le même banc contient deux cas de sensibilité séparés, tous deux à 180/180 lb :

- **AERORP avancé d'un pouce seulement**, de 103,2 à 102,2 : la commande passe de −0,9552 à −0,8977 ; marge de 4,48 à 10,23 %. Ce déplacement arbitraire démontre la sensibilité au bras de levier. Il n'identifie pas le bon point aérodynamique.
- **Bras de sièges remplacés par 43,8 et 74,7**, en supposant provisoirement un même datum : CG 86,8887 in, équilibre non trouvé. Cette hypothèse mélange potentiellement des repères incompatibles. Elle montre pourquoi copier deux nombres du manuel n'est pas une calibration complète.

Ces modifications vivent seulement en mémoire dans le banc. Les limites avant/arrière **du manuel** ne sont pas essayées comme des positions du prototype : leur conversion n'est pas démontrée. Les cas « avant » et « arrière » du tableau désignent une redistribution de charge, pas les bornes certifiées.

## 7. Vérifie le banc et classe ce qu'il reste à faire

Trois tests nouveaux contrôlent la conservation du poids lors d'un transfert entre sièges, l'accord de centrage avec JSBSim, la fermeture du bilan des moments et le rejet de masses invalides. Depuis le dépôt :

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Ouvre les résultats publiés : [table CSV](https://github.com/steveprudhomme/sw233-flightgear/releases/download/centrage-09/balance.csv) et [données et provenance JSON](https://github.com/steveprudhomme/sw233-flightgear/releases/download/centrage-09/balance.json). Compare une ligne à ton calcul à la main avant de lire toutes les autres.

**Ce que cette séance établit :** le calcul du centrage est cohérent entre notre formule, JSBSim autonome et FlightGear ; le bras de levier aérodynamique explique une grande part du moment à compenser ; les références héritées et le débattement demandent une révision documentée.

**Ce qui reste ouvert :** pesée d'un exemplaire choisi, correspondance des repères, point de référence des coefficients de moment, réglage de profondeur à ±23° avec animations cohérentes, puis véritable exploration du domaine de centrage. Le menu de chargement nécessite aussi une liaison aux deux occupants. Ces suites figurent dans [AUD-01](../../ROADMAP.md#audits-externes).

**Biais à surveiller :** ajuster AERORP ou un coefficient jusqu'à obtenir un chiffre agréable pourrait masquer un mauvais repère. Nous gardons donc le FDM intact et publions aussi les échecs du solveur. La prochaine correction devra partir des références géométriques et d'une convention de moment explicite.

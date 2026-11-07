# 7 · Voir ton propre avion, vérifier puis filmer

## Action 1 — Ranger un paquet que FlightGear reconnaît

**Pourquoi deux dossiers ?** *src* est ta boîte de pièces propres. *build* est la boîte que tu apportes au simulateur. La peinture modifie le maillage installé pour y inscrire les coordonnées de l’image. Garde l’original sans ces modifications : tu pourras refaire la peinture autant de fois que tu veux.

À la racine de *Mon-Schweizer*, crée **assembler.py** et écris :

```python
from pathlib import Path
from shutil import copytree
from tools.panel import finish_panel

source = Path("src/SW233")
paquet = Path("build/essai-1/Aircraft/SW233")
# copytree refuse d'écraser un paquet déjà présent.
copytree(source, paquet)
finish_panel(paquet / "Models")
print("Dossier à ajouter à FlightGear :", paquet.parent.resolve())
```

Lance `.\.venv\Scripts\python.exe assembler.py`. Ouvre la copie *build/essai-1/Aircraft/SW233/Models/panel.png*. Le dessin doit être posé à plat, sans les aiguilles. **Essai suivant :** remplace *essai-1* par *essai-2*. Si tu reçois *FileExistsError*, ton premier travail est encore là ; choisis simplement un nom neuf.

## Action 2 — Mettre tes yeux au bon endroit

Dans le lanceur FlightGear, ouvre **Add-ons → Aircraft folders**, ajoute le dossier **Aircraft** que le programme a affiché, puis cherche **Schweizer SGS 2-33**. Si tu vois plusieurs SW233, ne garde actif pour cet essai que le chemin de ta propre copie. Choisis un départ **en vol** : le planeur n’a pas de moteur pour quitter seul le sol. Pour reproduire les réglages, utilise les options du [vol à CYJN](../validation.md#capture-flightgear-à-cyjn). Choisis le décor téléchargé à l’action 4 si tu ne l’as pas encore.

**Vérifie dans cet ordre :** vue extérieure → deux ailes ; vue cockpit → planche et lettres lisibles ; Aide → quatre check-lists. Un avion absent de la liste indique d’abord un problème de dossier ou de nom set. Un cockpit invisible avec un extérieur présent invite à vérifier *internal*, la position de l’œil et le plan proche. Un cadran à l’envers invite à vérifier l’axe et le signe, pas à repeindre des chiffres à l’envers.

## Action 3 — Essayer une hypothèse, une seule à la fois

Dans *fabrique.py*, retrouve la demi-envergure 7,7724. Ne la change pas pour rendre le modèle plus joli : tu l’as calculée. Essaie plutôt un choix libre : dans *tools/panel.py*, remplace provisoirement le texte d’une étiquette par ton prénom. Assemble dans *essai-2*. Si le PNG change mais pas le cockpit, le lanceur utilise probablement le premier paquet. Remets l’étiquette d’origine avant de comparer les résultats.

Pour isoler la physique, on peut charger JSBSim **sans la fenêtre de FlightGear**. Copie uniquement les outils de contrôle comme expliqué ci-dessous. Lance `.\.venv\Scripts\python.exe tools/glide.py --speed 50 --seconds 60`. Compare la vitesse et l’altitude au [compte rendu](../validation.md). Un planeur perd de l’altitude dans cet essai en air calme ; il ne doit pas rester à 5 000 ft pendant toute la minute. Les tests de signe, de traînée, de saturation, de contact au sol et d’assemblage vérifient des comportements précis ; ils ne certifient pas les performances du vrai planeur.

## Action 4 — Refaire exactement le tournage avec ton aéronef

Le **simulateur**, ton **aéronef** et les **outils de tournage** sont trois choses différentes. Pour cette séance, télécharge le ZIP du [projet](https://github.com/steveprudhomme/sw233-flightgear) et extrais-le **à côté**, pas par-dessus *Mon-Schweizer*. Dans le terminal ouvert dans *Mon-Schweizer*, exécute ces lignes. À la question, colle le chemin du dossier extrait qui contient *atelier.py*.

```powershell
$kit = Read-Host "Dossier extrait qui contient atelier.py"
Copy-Item (Join-Path $kit 'atelier.py') .
Get-ChildItem (Join-Path $kit 'tools') -File | Where-Object Name -ne 'panel.py' | Copy-Item -Destination tools
Copy-Item (Join-Path $kit 'tests') . -Recurse
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tools/scenery.py
.\.venv\Scripts\python.exe atelier.py
```

**Pourquoi exclure panel.py ?** Pour filmer ta peinture. On ne copie pas non plus le dossier *src* : le vol doit utiliser le maillage et les XML que **tu as construits**. *scenery.py* vérifie l’index et les empreintes du terrain et des pistes. *atelier.py* en fait une nouvelle installation, démarre FlightGear et attend qu’il soit prêt. *native-demo.nas* donne des commandes au pilote virtuel : il ne dessine pas à la main l’inclinaison du planeur. Enfin, *annotate.py* lit les lignes **SW233_SAMPLE** et ajoute les légendes au vrai enregistrement. Suis les [écrans, résultats attendus et solutions de l’atelier](../atelier.md#3-fais-ton-premier-film).

| Arrête ton film ici | Ce qui doit changer | Comment départager deux pannes |
|---|---|---|
| Entre 14 et 28 s | La poignée orange se déplace et revient | Si le bandeau atteint 100 % mais que la poignée reste fixe, vérifie l’animation et le nom *poignee-frein*. |
| Entre 29 et 43 s | Deux panneaux se lèvent sur l’extrados (le dessus des ailes) | Un seul panneau ? Vérifie le deuxième nom d’objet et sa charnière. |
| Entre 46 et 73 s | La ficelle quitte l’axe, puis on voit le même virage de dehors | β est l’angle latéral du vent relatif. S’il change mais pas le fil, cherche le pivot et le lien à *aero/beta-deg*. |
| Après 76 s | La vue revient au cockpit ; la ficelle se recentre | Si seul le décor est bleu, regarde d’abord les coordonnées et la tuile de CYJN. |

## Action 5 — Laisser des traces qu’un ami peut relire

Dans *notes/mesures.txt*, ajoute la date, le changement fait, le résultat attendu, le résultat vu et le nom du paquet. Exemple : « Je pensais que la vis était trop grosse. J’ai diminué son rayon, sans déplacer le centre. Sur la deuxième image, le chiffre 8 reste lisible. » Garde les deux images. Cela vaut mieux qu’un vague « c’est mieux ».

Si tu veux ensuite partager ton travail, garde le maillage source, les XML, la recette de peinture, les tests et les explications dans Git. Ne mets pas le dossier .venv, les films, les paquets assemblés ni les photos tierces dans les commits. Le [guide de contribution](../../CONTRIBUTING.md) explique les commits signés avec *Signed-off-by*. Le texte intégral de la licence est dans [LICENSE.md](../../LICENSE.md). Pour partager le film comme dans ce projet : déposer le MP4 dans une release, mettre son URL dans le lecteur du README, puis vérifier la lecture dans la [version web](https://steveprudhomme.github.io/sw233-flightgear/#film). Le dépôt garde le code ; la release garde le résultat.

**Tu as fini quand** un ami peut lancer ta copie, voir un cockpit peint, retrouver ta mesure de l’aile gauche dans le cahier et dire, pour un nombre au choix, « celui-ci vient du manuel » ou « celui-ci est un choix du modèle ».

<a name="compas-en-virage"></a>

## Action 6 — Le planeur passe au nord. Est-ce que le compas y est déjà ?

[Regarder les 30 secondes du vol](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/compas-en-virage.mp4). Le film réunit cinq extraits à vitesse normale d’un même essai de 126 s. L’heure inscrite dans le bandeau est celle de la simulation ; ses sauts indiquent les coupes. Le petit cadre agrandit le compas de la même image.

**1. Avant le virage : choisis tes deux nombres.** Le cap magnétique dit où pointe le nez par rapport au nord magnétique. Le cap indiqué est la lecture de l’instrument. Regarde si les deux sont proches quand les ailes sont à plat. Le script attend au moins quatre secondes avec moins de 2° d’écart et moins de 3° de roulis avant de commencer (seuils inclus).

![Avant le virage : le tableau et le bandeau permettent de comparer les deux caps.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/avant.jpg)

**2. Au nord : compte par le chemin le plus court.** En allant vers la droite, à 25,2 s, le cap magnétique vient de passer à **000,5°** et le compas affiche encore **317,0°**. Dessine une horloge : de 317 à 360, il reste 43 degrés, puis un demi-degré jusqu’au nez. L’indication est donc en retard d’environ 43,5°. Vers la gauche, à 80,9 s, le nez est à **359,2°** et le compas à **042,6°**. Le signe change. Le compas fonctionne pendant tout le vol : le scénario ne lui impose aucun chiffre.

![Au premier passage du nord : la rose indique encore le secteur nord-ouest.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/nord.jpg)

**3. Ailes à plat : mesure le temps de retour.** Sur le graphique, la ligne bleue représente le cap magnétique et la ligne orange l’indication. Au sommet du graphique, −30° signifie 330° ; ce choix évite de tracer un faux saut à 360°. Les pointillés marquent les deux passages du nord. La courbe du milieu montre l’écart ; en bas, tu vois le roulis. Après le virage, la courbe orange dépasse la bleue puis revient : il faut mesurer plusieurs secondes, pas un seul croisement !

![Courbes mesurées : cap, écart signé et roulis pendant les deux virages.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/courbes.png)

| Sens | Inclinaison extrême | Plus grand écart en valeur absolue pendant la phase de virage, avec son signe | Premier retour à plat après le pic de roulis | Délai jusqu’au début de 3 s stables |
|---|---:|---:|---:|---:|
| Droite, 330° → 030° | +18,0° | −43,6° | 33,5 s | 33,4 s |
| Gauche, 030° → 330° | −18,0° | +43,6° | 89,1 s | 33,3 s |

Pour refaire le calcul, ouvre le [fichier des 764 relevés](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/vol.csv). Pour chaque ligne, écart = ((ind − mag + 180) modulo 360) − 180. Après le pic d’inclinaison de chaque virage, démarre le chronomètre au premier relevé avec |roulis| ≤ 3°. Cherche ensuite le premier groupe de relevés consécutifs couvrant au moins 3 s avec **à la fois** |écart| ≤ 2° et |roulis| ≤ 3°. Arrête le chronomètre au début de ce groupe. C’est un critère de comparaison, pas une garantie que l’écart restera ensuite dans cette bande.

![À la fin, les ailes sont revenues à plat vers 330° et les deux lectures sont à nouveau proches.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-virages-05/retour.jpg)

**4. Refaire ton propre vol.** Utilise le paquet animé de la fiche 4 et les outils copiés à l’action 4. Ouvre une session FlightGear dédiée à SW233 à CYJN, avec le décor chargé. Dans les options supplémentaires du lanceur, indique une option par ligne :

```text
--httpd=18097
--wind=0@0
--turbulence=0.0
--disable-real-weather-fetch
--geometry=1280x720
--start-date-gmt=2026:06:21:16:45:00
```

Une fois la scène visible, exécute depuis ton établi, avec FFmpeg disponible :

```powershell
.\.venv\Scripts\python.exe -m pip install matplotlib
.\.venv\Scripts\python.exe tools/record_compass.py build/mon-vol-compas
.\.venv\Scripts\python.exe tools/compass_report.py build/mon-vol-compas build/mon-rapport-compas
```

Le premier outil place le planeur près de CYJN à 6 000 ft et 60 kt, fait piloter les gouvernes puis met le vol en pause à la fin du retour. Il enregistre les valeurs, puis demande l’image suivante : elles sont voisines dans le temps, pas synchronisées au pixel près. Le second outil fabrique le film, les trois photos et les courbes. Choisis de nouveaux noms de dossiers si tu recommences. Pour cet essai : FlightGear 2024.1.7, vent relevé 0 kt, vitesse indiquée 59,7 à 62,3 kt, environ six relevés par seconde. Le délai dépend aussi du type d’entrée en virage, de la vitesse et de l’instrument simulé. Aucune de ces mesures n’est une mesure en vol du Schweizer réel.

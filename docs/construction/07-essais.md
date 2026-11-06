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

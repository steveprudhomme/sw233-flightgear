# 27. Observer les raccords et la place arrière

**Pour vous :** cet atelier vise un débutant, dès 10 ans, accompagné au besoin.
**But :** reconnaître le vitrage central, les panneaux gris et le passage de la sangle.
**Avant de commencer :** installer le paquet `0.1.0-alpha.3` selon [l’atelier12](12-installation.md).

## Comprendre les pièces

La **racine de l’aile** est le bout de l’aile qui rejoint le fuselage.
Le **raccord** est la zone où deux pièces se rencontrent.
Le passager arrière reste sous les ailes. Un vitrage fixe les relie au-dessus de sa place.
Le dossier gris présente des creux pour suivre la forme du corps.
La demi-lune noire marque le passage de la sangle verte. Les attaches cachées ne sont pas reproduites.

## Observer le raccord bleu

1. Placer le planeur au sol.
2. Choisir une vue extérieure au-dessus du cockpit.
3. Comparer les deux images suivantes.

![Ancienne version vue du dessus, sans occupants.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/avant-dessus-equipage-0-ouvert-0.png)

*Figure 1 — Avant : version alpha.2 dans FlightGear.*

![Nouveau vitrage fixe ajusté entre les ailes.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/apres-dessus-equipage-0-ouvert-0.png)

*Figure 2 — Après : le bord du vitrage suit le profil de chaque aile. Une bande bleue couvre chaque jonction.*

4. Ouvrir la verrière avant avec la commande de [l’atelier26](26-ouverture-verriere.md).
5. Vérifier que le vitrage central reste en place.

![Verrière avant ouverte avec les deux occupants en place.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/apres-dessus-equipage-1-ouvert-1.png)

*Figure 3 — Le vitrage central reste fixe. Le passager arrière reste sous les ailes.*

## Observer le dossier et la sangle

1. Masquer les occupants avec le menu de l’appareil.
2. Regarder vers le dossier arrière.
3. Repérer le creux du dossier et la demi-lune noire.

![Dossier gris avec relief, passage noir en demi-lune et sangle verte.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/apres-dossier-equipage-0-ouvert-0.png)

*Figure 4 — Capture rapprochée du dossier. La sangle sort au bas de la demi-lune. Le siège existant reste simplifié.*

![Pièces du dossier séparées des autres éléments du planeur.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/groupe-dossier.png)

*Figure 5 — Dessin calculé depuis le modèle : dossier, vis, passage noir et sangle. Ce n’est pas une photo.*

## Observer les faces grises

1. Regarder la jonction de l’aile gauche depuis la place arrière.
2. Repérer le panneau gris et la petite grille.

![Face grise de la racine gauche avec une ouverture ronde grillagée.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/apres-racine-gauche-equipage-0-ouvert-0.png)

*Figure 6 — La grille représente l’ouverture signalée par le mainteneur. Sa fonction d’aération reste à confirmer.*

3. Regarder la jonction de l’aile droite.
4. Vérifier qu’aucune grille identique n’apparaît à droite.

![Face grise de la racine droite sans grille.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/apres-racine-droite-equipage-0-ouvert-0.png)

*Figure 7 — L’habillage droit reste fermé.*

![Ouverture gauche, bord et grille présentés ensemble.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/groupe-ouverture-gauche.png)

*Figure 8 — Les trois pièces de l’ouverture. Aucun circuit d’air n’est simulé.*

![Vitrage, bandes bleues et faces grises des racines.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/groupe-raccords.png)

*Figure 9 — Les pièces du raccord, isolées pour voir leur forme.*

## Vérifier et corriger

Le vitrage doit rejoindre les bords supérieurs des ailes. Les bandes bleues doivent rester continues.
Le dossier doit se trouver derrière le passager. La verrière avant doit encore pouvoir s’ouvrir au sol.
Si les pièces manquent, vérifier la version du paquet. Fermer FlightGear, puis relancer le nouveau paquet.
Ne pas utiliser la réinitialisation complète pour cet essai : le défaut FG-44-01 reste ouvert.

Les captures utilisent une caméra de contrôle, sans limite de rotation, pour regarder derrière le pilote.
Les limites de la vue normale restent inchangées dans le paquet.
L’orientation du planeur pendant ces captures aide à éclairer le dossier.

## Retrouver les preuves et les limites

Les photos DET-02 et DET-06 montrent le dossier gris et le passage de la sangle.
DET-03 et DET-09 montrent les raccords autour du vitrage.
Consulter les [références conservées](../references/ouverture-verriere.md).
La précision du mainteneur situe l’ouverture à gauche seulement.

Les dimensions sont estimées. Le diamètre choisi pour l’ouverture est de 64 mm.
La forme ronde et le dessin de la grille restent à confirmer avec une vue rapprochée.
Le relief du dossier, la largeur des bandes et les attaches cachées demandent aussi des relevés.
Ce travail ne termine ni les coussins ni les harnais complets.

Les recettes se trouvent dans [l’atelier2](02-maillage.md) et [l’atelier24](24-formes-avant.md).
Le [bilan du lot45](../validation/raccords-lot45.md) décrit les contrôles.
L’[atlas des 95 pièces](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.3/atlas-lot45.zip) contient une image de chaque objet du modèle.

**Relecture :** vocabulaire expliqué, actions ordonnées, légendes et textes alternatifs ajoutés.
L’essai avec un lecteur débutant reste à faire. Aucune conformité globale aux normes n’est déclarée.

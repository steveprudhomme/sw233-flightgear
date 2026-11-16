# 18. Préparer la comparaison avec un appareil réel

VIS-01e, préparation du 15 novembre 2026 ; plan préalable `320e1fd`. Nous n'avons pas accès à un appareil réel. Le résultat de cette séance est un dossier prêt à comparer, pas une nouvelle forme de cockpit.

## 1. Séparer les deux feuilles

Ouvre la [fiche C-FYLP](../references/releve-cfylp.md). Elle contient uniquement les renseignements attestés et les cases encore inconnues. Sur une autre feuille, écris en gros « MODÈLE INFORMATIQUE ». C'est cette deuxième feuille que nous allons remplir automatiquement.

Pourquoi deux feuilles ? Une mesure précise d'un modèle approximatif reste une mesure du modèle. Elle ne devient pas vraie sur le planeur parce qu'elle comporte quatre décimales.

## 2. Fabriquer les vues depuis le dépôt

Ouvre un terminal dans le dossier du dépôt, celui qui contient README.md, tools et src. Utilise le même Python avec Pillow que dans l'atelier. Le nom de sortie doit désigner un dossier qui n'existe pas encore :

```powershell
# Depuis la racine du dépôt : produit les mesures et dix planches.
python -m tools.cockpit_survey build/releve-cockpit
```

Le programme lit src/SW233/Models/sw233.ac, repère dix noms de pièces et calcule leurs limites. Il produit un fichier JSON de nombres, un document Markdown et dix PNG. Il refuse d'écraser un dossier existant : pour refaire l'essai, choisis un nouveau nom de sortie.

[Le dossier complet à télécharger](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/dossier-releve.zip) contient les mêmes sorties, la fiche C-FYLP et le formulaire. Extrais le ZIP avant d'ouvrir les images. Le Markdown s'ouvre aussi comme texte ; le tutoriel en ligne affiche toutes les planches ci-dessous.

## 3. Comprendre les axes et les nombres

Le repère de construction indique x vers l'arrière, y vers la droite, z vers le haut. Le lecteur du fichier AC transforme ses coordonnées dans ce repère. Le zéro n'est pas automatiquement le datum du manuel de masse : relis la fiche 17 avant de les comparer.

Pour le pare-brise du modèle, le x minimum vaut 0,5000 m et le maximum 1,6900 m. Son étendue longitudinale vaut donc 1,6900 − 0,5000 = **1,1900 m**. Ses y extrêmes sont −0,4300 et +0,4300 : étendue latérale **0,8600 m**.

Cela ne signifie pas que chaque section du pare-brise mesure 0,8600 m de large. Imagine une boîte juste assez grande pour contenir toute la pièce : ces nombres décrivent la boîte. Une section plus étroite peut se trouver à l'intérieur. Le relevé physique W demande une position de section S précisément définie.

## 4. Garder l'identité du modèle mesuré

Ouvre model-measurements.json. Le champ sha256 est l'empreinte du fichier AC lu : il permet de vérifier que deux dossiers utilisent le même fichier, pas de prouver sa fidélité. Le champ classification rappelle que les chiffres concernent seulement le modèle. Les limites sont conservées sans arrondi dans le JSON ; le tableau affiche quatre décimales pour être lisible.

## 5. Examiner chaque pièce

Les vues ci-dessous sont orthogonales, sans perspective, sans animation et sans texture photographique. Elles sont ajustées à chaque cadre : compare les nombres pour les tailles, pas les largeurs apparentes de deux images différentes. Les traits de faces ne sont pas nécessairement des joints réels.

### 1. fuselage

x : 0.0000 à 7.6100 m ; y : -0.4700 à 0.4700 m ; z : -0.6300 à 0.1200 m.

![fuselage : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-01.png)

### 2. pare-brise

x : 0.5000 à 1.6900 m ; y : -0.4300 à 0.4300 m ; z : 0.0500 à 0.6100 m.

![pare-brise : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-02.png)

### 3. vitrage-gauche

x : 1.5500 à 3.1600 m ; y : -0.4400 à -0.2788 m ; z : 0.0900 à 0.5920 m.

![vitrage-gauche : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-03.png)

### 4. vitrage-droit

x : 1.5500 à 3.1600 m ; y : 0.2788 à 0.4400 m ; z : 0.0900 à 0.5920 m.

![vitrage-droit : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-04.png)

### 5. arceaux

x : 0.4840 à 3.1760 m ; y : -0.4559 à 0.4559 m ; z : 0.0389 à 0.7159 m.

![arceaux : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-05.png)

### 6. bordures-cockpit

x : 0.4936 à 3.1623 m ; y : -0.4580 à 0.4580 m ; z : 0.0320 à 0.1180 m.

![bordures-cockpit : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-06.png)

### 7. raccord-arriere

x : 2.1300 à 3.1600 m ; y : -0.3608 à 0.3608 m ; z : 0.1000 à 0.7000 m.

![raccord-arriere : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-07.png)

### 8. longerons-verriere

x : 1.6632 à 3.1657 m ; y : -0.3708 à 0.3708 m ; z : 0.2066 à 0.6019 m.

![longerons-verriere : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-08.png)

### 9. contour-porte-1

x : 1.5475 à 2.7825 m ; y : -0.4430 à -0.3895 m ; z : -0.3625 à 0.1001 m.

![contour-porte-1 : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-09.png)

### 10. contour-porte1

x : 1.5475 à 2.7825 m ; y : 0.3895 à 0.4430 m ; z : -0.3625 à 0.1001 m.

![contour-porte1 : profil, dessus et face du modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/releves-20/piece-10.png)

## 6. Replacer ces pièces dans le simulateur

![Cockpit dans FlightGear, capture antérieure panneaux-17, géométrie inchangée](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-cockpit.jpg)

Cette capture native est reprise de la fiche 15. Elle sert à reconnaître les pièces ; nous n'avons pas réalisé un nouvel essai de vol pour un dossier documentaire. L'aperçu FlightGear reste inchangé.

## 7. Préparer la prochaine comparaison

Ouvre le tableau de correspondances de la fiche C-FYLP. Choisis une pièce, puis cherche la mesure réelle nécessaire. Si la case est vide, écris « à obtenir ». Ne prends ni la mesure d'un autre appareil ni celle d'une simulation pour remplir ce blanc.

Quand une mesure arrive, note son appareil, sa date, ses unités, son origine et sa marge d'incertitude. Vérifie les points sur la photographie. Ensuite seulement, transforme les unités et compare avec le modèle. Une différence justifie une enquête ; elle ne justifie pas à elle seule de déplacer toutes les pièces.

## 8. Vérifications et point d'arrêt

Le calcul des limites a été contrôlé avec trois points simples dont on connaît les extrêmes. Le refus d'écraser un dossier existant a été essayé. Les contrôles des sources et du style Python passent. La reconstruction de l’aéronef depuis les blocs du tutoriel est vérifiée ; les nouveaux liens locaux et l’empreinte du maillage sont contrôlés. Les planches du pare-brise et du contour de porte ont été examinées visuellement.

Aucun fichier de l'aéronef n'a été modifié. VIS-01e reste **en attente des mesures physiques**. La préparation est reproductible ; la collecte n'est pas terminée. En attendant, on peut proposer un lot distinct pour les détails de surface du tableau visibles sur la photo, sans prétendre corriger les dimensions générales du cockpit.

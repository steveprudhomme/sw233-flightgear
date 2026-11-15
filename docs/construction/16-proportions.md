# 16. Comparer les proportions avant de déplacer les pièces

Séance VIS-01c du 15 novembre 2026. Plan commité avant analyse : `8dd7296`. Cette fiche produit un diagnostic mesurable. **Elle ne modifie pas l’avion** : les preuves disponibles ne suffisent pas à transformer les écarts au dessin en corrections dimensionnelles fiables du véritable planeur.

## 1. Choisir la référence et respecter son domaine

C-FYLP reste la référence du tableau de bord. La photo fournie montre sa disposition, mais ne donne ni profil extérieur orthogonal ni cote de cockpit connue. Le trois-vues couleur montre un SGS 2-33A générique ; le Short Kit est un plan de maquette photographié en perspective. N2930H est un autre appareil. On ne fabrique pas un prétendu relevé de C-FYLP en mélangeant ces images.

Ouvre le [registre des références](../references/inventaire.md), puis le fichier local Schweizer_SGS_2-33A_two-seat_glider_colour_3-view_drawing.jpg. Sa taille attendue est 960 × 743 pixels. Nous utilisons seulement le profil du milieu. Le dessin vu du dessus possède une autre échelle : ne prends aucun de ses points pour ce calcul.

## 2. Garder un témoin visuel du modèle

![Profil natif du modèle panneaux-17, utilisé comme témoin inchangé](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-profil-gauche.jpg)

![Vue pilote du même modèle](https://github.com/steveprudhomme/sw233-flightgear/releases/download/panneaux-17/apres-cockpit.jpg)

Ce sont les captures FlightGear de la fiche 15. Nous ne les présentons pas comme de nouveaux essais. Elles montrent l’état analysé ; les distances sont calculées depuis le fichier AC, pas mesurées sur une capture en perspective.

## 3. Pointer le dessin

Dans Paint ou un outil affichant les coordonnées, zoome sans redimensionner le fichier. Les coordonnées partent du coin supérieur gauche. Relève les colonnes suivantes, en gardant une marge de **±3 pixels par point** choisie pour le trait épais et la lecture manuelle :

| Repère sur le profil | Colonne nominale | Intervalle de pointage choisi |
|---|---:|---:|
| Nez de la coque, sans Pitot | 214 | 211–217 |
| Extrémité arrière choisie pour la longueur du profil | 697 | 694–700 |
| Début du vitrage au nez | 263 | 260–266 |
| Pied du montant arrière du pare-brise | 332 | 329–335 |
| Sommet du même montant | 339 | 336–342 |

Ces positions sont des lectures approximatives. La correspondance entre chaque trait du dessin et un objet du maillage doit également être revue : un bord de vitre et un tube de cadre ne sont pas exactement la même chose. La marge ±3 ne couvre pas cette ambiguïté ni les erreurs du dessin par rapport au vrai appareil.

## 4. Comparer sans unité

La longueur pointée vaut 697−214=483 pixels. Pour le pied du montant, la distance depuis le nez vaut 332−214=118 pixels. Le rapport est 118/483=0,2443, soit 24,43 % de la longueur.

Dans notre maillage, le pied est à 1,55 m et la longueur de référence à 7,8486 m : 1,55/7,8486=0,1975, soit 19,75 %. La différence n’est pas un effet de zoom, puisque les deux nombres sont des rapports.

| Repère | Rapport du dessin | Intervalle dû au pointage seul | Rapport du modèle | Position du modèle |
|---|---:|---:|---:|---:|
| Début du vitrage | 0,1014 | 0,0890–0,1139 | 0,0637 | 0,500 m |
| Pied du montant | 0,2443 | 0,2319–0,2567 | 0,1975 | 1,550 m |
| Sommet du montant | 0,2588 | 0,2464–0,2712 | 0,2153 | 1,690 m |

![Comparaison des repères et des intervalles de pointage](https://github.com/steveprudhomme/sw233-flightgear/releases/download/proportions-18/comparaison.png)

Les points orange sont plus proches du nez que les points bleus. Ils sortent même de notre marge de pointage. **Conclusion autorisée : le maillage ne suit pas ces repères du dessin.** Conclusion non démontrée : le vrai appareil exige exactement les déplacements calculés ci-dessous.

Pour encadrer le rapport, le script fait varier le repère, le nez et l’extrémité dans leurs marges. Pour le rapport minimal, la colonne du repère diminue de 3, celle du nez augmente de 3 et celle de l’extrémité augmente de 3. Exemple du pied : (329−217)/(700−217)=112/483=0,2319. Au maximum : (335−211)/(694−211)=124/483=0,2567. Cette petite analyse ne donne pas un intervalle de confiance statistique.

## 5. Montrer pourquoi une correction aveugle serait importante

Si l’on impose au dessin la longueur 7,8486 m, un pixel correspond à environ 0,01625 m. Les positions indicatives deviennent :

| Repère | Position déduite du dessin remis à l’échelle | Modèle moins dessin | Décision |
|---|---:|---:|---|
| Début du vitrage | 0,796 m | −0,296 m | À vérifier sur un profil extérieur coté |
| Pied du montant | 1,917 m | −0,367 m | Ne pas déplacer isolément le montant et oublier le poste pilote |
| Sommet du montant | 2,031 m | −0,341 m | Revoir conjointement position, hauteur et pente |

Le signe négatif indique une position plus proche du nez dans le modèle. Ces écarts sont **des écarts au dessin**, pas des erreurs connues de l’avion simulé par rapport à C-FYLP.

Le rapport de pente de la fiche 15, 7/32≈0,22 contre 0,14/0,52≈0,27, ne suffit donc pas : il faut aussi contrôler la position de tout le montant. Nous conservons la géométrie jusqu’à ce qu’une référence mieux identifiée permette de choisir entre déplacement global, changement de proportions ou erreur de correspondance des points.

## 6. Décider pour chaque zone demandée

| Zone | Ce que nous savons | Ce qui manque | Décision de ce lot |
|---|---|---|---|
| Pare-brise et montant avant | Écart longitudinal au trois-vues quantifié | Profil extérieur identifié et cote dans le même plan | Conserver, signaler l’écart et demander une référence dimensionnée |
| Hauteur des flancs | La coque rejoint désormais les vitres, sans trou | Hauteur réelle au droit de chaque siège | Ne pas confondre fermeture géométrique et dimension validée |
| Largeur du cockpit | La planche de 0,78 m est une hypothèse ancienne | Largeur réelle au tableau et aux épaules | Ne pas utiliser cette hypothèse comme règle pour valider la photo |
| Porte | Contours fixes et symétriques de travail | Deux flancs du même appareil, limites et cotes de porte | Conserver explicitement provisoire ; aucune animation |
| Raccord sous l’aile | Emplacement visible mais masqué en partie par l’aile et le hauban | Vue latérale dégagée et vue oblique arrière | Ne pas donner une cote à un bord caché |
| Tableau C-FYLP | Disposition visible sur la photographie identifiée | Photo frontale avec une dimension de référence | Conserver l’identité C-FYLP ; ne pas emprunter les dimensions de N2930H |

Aucune correction dimensionnelle n’atteint ici le niveau de confiance défini dans le plan. C’est une conclusion d’audit, pas une déclaration que les proportions actuelles sont correctes.

## 7. Refaire le calcul toi-même

Depuis la racine du dépôt, avec Python et Pillow installés comme dans la fiche 12 :

```powershell
python -m tools.proportions build/mes-proportions
```

Choisis un dossier neuf. L’outil lit les sommets de pare-brise, retrouve le pied parmi les points sous z=0,10 m, puis lit la longueur à l’extrémité de la dérive. Ces sélections sont valables pour cette version ; si tu changes la géométrie ou les noms, revois aussi les correspondances.

Tu obtiens proportions.json, comparaison.svg et comparaison.png. Le JSON garde les valeurs non arrondies. Le SVG est une figure originale des rapports, pas une copie du plan. Le PNG sert à la lecture du tutoriel. Le programme ne modifie aucun fichier de l’avion.

Vérifie à la main : 49/483 pour le début du vitrage ; 118/483 pour le pied ; 125/483 pour le sommet. Vérifie aussi que la longueur du maillage vaut 7,8486 m et que le pied et le sommet se trouvent à 1,55 et 1,69 m. Un calcul reproductible peut rester fondé sur une mauvaise référence : conserve toujours cette distinction.

## 8. Préparer les mesures qui permettront réellement de corriger

Pour le prochain relevé, rechercher les éléments suivants pour un même appareil, en notant immatriculation, variante et date :

1. Une vue de chaque flanc prise aussi perpendiculairement que possible, avec le nez, la verrière et l’aile identifiables.
2. Une dimension connue dans le plan observé, idéalement plusieurs ; ne pas utiliser la taille supposée d’un cadran comme étalon.
3. Les distances longitudinales du nez ou d’un datum identifié au pied et au sommet du montant ; préciser le repère, car le datum de pesée n’est pas notre origine au nez.
4. La hauteur et la largeur de la bordure à des stations définies, ainsi que les limites réelles de porte.
5. Une vue arrière oblique permettant de séparer raccord de fuselage, vitrage et aile.

Un propriétaire ou un contributeur peut fournir les mesures déjà disponibles dans ses documents ; ne pas démonter ni manipuler un appareil pour satisfaire ce tutoriel. Le paquet de références devra autoriser leur usage documentaire. Tant que ce dossier manque, les matériaux peuvent être étudiés séparément, mais la fidélité dimensionnelle ne doit pas être annoncée.

## 9. Livraison et limites

ROADMAP, README, CHANGELOG et le sommaire sont actualisés. Les images de FlightGear et sa description ne changent pas, puisque le modèle reste exactement panneaux-17 ; aucune nouvelle version binaire d’avion n’est nécessaire. La publication proportions-18 fournit uniquement les résultats de cette comparaison et la figure.

Base de cette analyse : dessin et photos fournis, coordonnées du maillage actuel, calcul des rapports et captures natives déjà publiées. Biais principal : le choix manuel des correspondances entre le dessin générique et le modèle. La bande de pointage ne quantifie pas ce biais. Les silhouettes proches à l’œil ne suffisent pas à lever cette incertitude.

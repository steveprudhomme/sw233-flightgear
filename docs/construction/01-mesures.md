# 1 · Du dessin à un nombre que tu peux vérifier

Prends une règle, un crayon et une feuille. Écris quatre lettres en haut : **L** = lu dans un document ; **C** = calculé ; **V** = vu sur une image ; **H** = hypothèse de la maquette. Une cote H peut donner une belle image et rester fausse sur le vrai planeur. Ne remplace jamais son H par un L.

## Action 1 — Identifier le bon document

Recopie dans **notes/mesures.txt** : « objet ; document et page ou nom de photo ; points lus ; calcul et unité ; résultat ; classe ; limite ; fichier qui s’en sert ». Pour reconnaître une édition du manuel, utilise le [registre des 16 références](../references/inventaire.md). Les pages ci-dessous sont les **pages du fichier PDF**, la première vaut 1. Une page PDF peut montrer deux pages de papier. Si tu n’as pas nos scans, pars du [manuel et des sources accessibles](../sources.md) et des relevés reproduits ici ; vérifie le titre de la section si les pages changent.

| Où poser le doigt | Quoi noter | À quoi cela sert, et à quoi cela ne sert pas |
|---|---|---|
| Manuel de vol FAA fourni, PDF 4–6, description du 2-33/2-33A | **51 ft** d’envergure ; **25 ft 9 in** de longueur [L] | Échelle du trois-vues. Ce ne sont pas les dimensions d’une demi-aile. |
| Même manuel, PDF 14–15 (papier 26–29), dessin et exemple de pesée | Datum 66,34 in devant le bord d’attaque à la racine ; exemple n° 369 : 932 lb à la station 83,13 in [L] | Un datum est le zéro de la règle de pesée. **Ce zéro n’est pas le nez** utilisé pour notre dessin. Ne colle pas 83,13 dans le fichier 3D. |
| Même manuel, PDF 12 (papier 22), commande de frein | Frein de roue en fin de course [L] | Explique pourquoi le levier est commun. Notre modèle anime les aérofreins ; il ne simule pas encore ce frein de roue. |
| Guide d’étude régional, PDF 265–270, circuit des instruments | Le Pitot et la pression statique participent à la mesure de vitesse ; le variomètre a du retard | Guide le choix de la grandeur affichée. Le modèle actuel idéalise ce circuit. |
| Manuel du programme 2017, PDF 213 (papier 2-7-19) | Après interruption d’une vérification, reprendre le dernier élément terminé | Guide la conception des listes ; ne donne pas la longueur d’un manche. |
| Photo du tableau portant **C-FYLP**, image 690 × 517 ; photo portant **N2930H** | Altitude à gauche sur C-FYLP, vitesse en mph à droite, variomètre encore plus à droite [V] | On choisit **C-FYLP** pour la disposition. On ne comble pas ses trous avec l’autre tableau. |
| Plans *Short Kit*, croquis de visite et de lubrification | Forme des sections, emplacement relatif des haubans, aérofreins et roue [V] | Un plan de maquette photographié en biais ne fournit pas de cotes certifiées grandeur nature. |

## Action 2 — Passer en mètres

Un pied vaut **0,3048 m** ; un pouce vaut **0,0254 m**. Écris les unités à chaque ligne. Envergure = 51 × 0,3048 = **15,5448 m**. De l’axe à un bout : 15,5448 ÷ 2 = **7,7724 m**. Longueur = 25 × 0,3048 + 9 × 0,0254 = **7,8486 m**. Attention : 25 ft 9 in ne vaut pas 25,9 ft, car il y a **12** pouces dans un pied. Ces trois résultats sont C. Le bout du Pitot ajouté au nez dépasse le zéro de la coque : ne mesure pas la longueur de la silhouette en prenant ce tube pour le nez.

## Action 3 — Refaire une mesure sur le trois-vues

Ouvre *Schweizer_SGS_2-33A_two-seat_glider_colour_3-view_drawing.jpg*, **960 × 743**. Dans un éditeur d’image tel que Paint, zoome sans redimensionner. Lis la position du pointeur en pixels depuis le coin supérieur gauche. Si ta copie a une autre taille, mesure tout dans ta copie : le rapport reste valable. Utilise **la vue du dessus en bas** ; ne mélange pas ses pixels avec ceux de la vue de profil.

| Mesure d’exercice (pointages arrondis, pas un plan d’usine) | Calcul que tu dois retrouver | Comparaison au modèle |
|---|---|---|
| Extrémités au niveau des ailes, colonnes 7 et 950 | 943 px ; 15,5448 / 943 ≈ **0,01648 m/px** | Une erreur de 2 px sur la distance vaut environ 3,3 cm ; la précision du dessin lui-même est inconnue. |
| Axe colonne 479 ; changement de pente au bord d’attaque droit vers 687 | (687 − 479) × 0,01648 ≈ **3,43 m** | La section du modèle est à **3,42 m** [H cohérente avec V]. Ce nouveau pointage ne prouve pas comment une ancienne cote a été obtenue. |
| Près de la racine, colonne 500 : bord avant ligne 613, bord arrière ligne 521 | 92 × 0,01648 ≈ **1,52 m** de corde | Le modèle a **1,57 m** [H]. Note les deux, sans corriger le dessin pour le faire tomber juste. Le nez est en bas sur cette vue. |
| À droite, près du saumon : lignes 602 et 555 environ | 47 × 0,01648 ≈ **0,77 m** | Dernière corde du modèle : **0,76 m** [H]. |

À toi : mesure la demi-envergure gauche, sans regarder le calcul de droite. Si tu trouves 15 m, tu as pris toute l’aile. Si les deux côtés diffèrent un peu, garde les deux lectures dans le cahier.

## Action 4 — Positionner un instrument sans inventer sa taille réelle

Sur la photo C-FYLP originale, pointe les centres (colonne, ligne) : altitude ≈ (118,265), vitesse ≈ (480,220), variomètre ≈ (581,280), bouche d’air ≈ (346,177). Relève les bords de la planche sur une même ligne, par exemple près de sa base utile, vers 45 et 655 : **environ 610 px**, sensibles au choix de la ligne. La largeur 3D de notre planche, **0,78 m**, est une hypothèse. Elle ne devient pas une mesure parce qu’on a une photo.

Petit essai : (480 − 346) / 610 × 0,78 ≈ **0,171 m à droite** de l’axe de la bouche. Le cadran du modèle est à **+0,170 m**. Pour l’altimètre, (118 − 346) / 610 × 0,78 ≈ **−0,292 m** ; le modèle a **−0,220 m**. Voilà un écart utile à noter ! La photo est en perspective, le tableau a été simplifié, et la largeur réelle n’a pas été mesurée. N’utilise pas ce rapport pour deviner la profondeur derrière le tableau. Pour améliorer la fidélité, il nous faudrait une vue frontale, une dimension connue dans le même plan et, idéalement, un second point de vue.

**Point d’arrêt :** dans ton cahier, entoure les dimensions publiées ; souligne les trois écarts comparés. Les rayons de vis, teintes, épaisseurs d’aile, sections du fuselage et angles du levier que tu verras ensuite sont **des choix H** sauf source explicitement donnée. Les valeurs du modèle historique de vol sont marquées séparément dans [le tableau des coefficients](../sources.md).

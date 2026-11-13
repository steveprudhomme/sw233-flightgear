# Fabrique ton Schweizer, du cahier de mesures au film

**Tu commences avec un dossier vide.** À la fin tu auras fabriqué les deux ailes, assis le pilote à la bonne place dans la maquette, branché quatre aiguilles et vu *ton* planeur dans FlightGear. N’essaie pas de tout faire en une fois : chaque fiche a un point d’arrêt. Tu peux fermer l’ordinateur à cet endroit et reprendre demain.

**Avant de commencer.** Sur Windows, prépare Python 3.11 ou 3.13, FlightGear avec ses données et, pour la dernière séance seulement, FFmpeg. Les [instructions d’installation avec les liens](../atelier.md#1-prépare-ton-établi) restent disponibles. Les blocs gris se copient sans les trois accents graves. Le texte après un `#` en Python est une note pour toi. Respecte les espaces au début des lignes. Un point dans le code veut dire une virgule dans un nombre : écris `0.50`, pas `0,50`.

| Séance | Ce que tu fais toi-même | À mettre sur ta table avant de continuer |
|---|---|---|
| [1. Mesurer](01-mesures.md) | Choisir la bonne vue, lire une dimension, convertir, pointer deux pixels et garder la trace | Une fiche de mesure par cote, avec sa limite |
| [2. Construire la coque et les pièces](02-maillage.md) | Écrire une recette Python qui relie des points ; produire **src/SW233/Models/sw233.ac** | Deux demi-ailes de 7,7724 m et une ficelle séparée du tube |
| [3. Donner du poids et de la portance](03-vol.md) | Écrire les instructions qui produisent **src/SW233/sw233.xml** | Six forces ou moments ; aucune hélice |
| [4. Brancher la maquette](04-configuration.md) | Écrire **src/SW233/sw233-set.xml** et **src/SW233/Models/sw233-model.xml** | Un siège avant, douze animations et une conversion vérifiée au crayon |
| [5. Faire les listes](05-listes.md) | Écrire **src/SW233/Checklists/sw233.xml** | Quatre listes que tu peux ouvrir, sans commande de vol automatique |
| [6. Peindre](06-peinture.md) | Écrire **tools/panel.py**, poser les vis et coller l’image sur la planche | Une copie peinte ; les aiguilles bougent encore |
| [7. Essayer, filmer, partager](07-essais.md) | Assembler le paquet, charger CYJN, lire la télémétrie et refaire le film | Un vol que quelqu’un d’autre peut refaire |
| [8. Examiner le centrage](08-centrage.md) | Calculer les moments, vérifier les masses dans FlightGear, expliquer la réserve de profondeur | Calcul manuel, captures et résultats, y compris les échecs du solveur |
| [9. Comprendre les repères](09-reperes.md) | Séparer datum, dessin et référence des moments ; tester une translation | Un schéma, une capture native et quatre expériences comparables |

| [10. Animer la profondeur](10-profondeur.md) | Lire les 23°, découper la gouverne et vérifier les butées dans FlightGear | Captures natives et équilibre avant/après |

| [11. Régler les occupants](11-occupants.md) | Relier une fenêtre aux masses et lire le CG effectif | Calcul indépendant, captures solo/biplace et restauration |

| [12. Installer et lancer](12-installation.md) | Fabriquer un paquet contrôlé, le déplacer et lancer la bonne copie | Chemins avec espaces, manifeste et captures natives |

**Ouvre ton établi.** Crée dans Documents un dossier *Mon-Schweizer* vide. Ouvre-le dans l’Explorateur ; dans sa barre d’adresse, écris `powershell` puis Entrée. Toutes les commandes de ce livre partent de là. Colle ces lignes une par une :

```powershell
New-Item -ItemType Directory src/SW233/Models, src/SW233/Checklists, tools, notes
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy==2.3.5 Pillow==12.0.0 jsbsim==1.2.3
```

Pour créer un fichier indiqué sur une fiche, ouvre le Bloc-notes, colle le premier bloc, puis **Fichier → Enregistrer sous**. Choisis **Tous les fichiers** et **UTF-8**, puis le nom exact. Active l’affichage des extensions dans l’Explorateur : *fabrique.py.txt* n’est pas *fabrique.py*. Lorsqu’une fiche dit « ajoute », va **tout en bas du même fichier** avant de coller le bloc suivant. Une ligne vide entre deux blocs convient. N’ajoute pas les phrases du livre dans le fichier.

**D’où vient cet ordre ?** Au début du projet, le dépôt et la licence ont précédé l’avion ; une silhouette et le calcul du vol ont précédé les instruments. Les tests ont d’abord produit un rejeu dessiné. Les manuels et les photos ont ensuite guidé la seconde forme, puis le Pitot et la ficelle. Le premier vol dans FlightGear a révélé un siège invisible et une coque qui cachait les commandes. C’est pourquoi tu fabriqueras directement la forme corrigée. Ensuite sont venus le décor de CYJN, les deux angles de caméra, le grain du tableau et le lecteur web. La GPL-3.0-only s’applique à la version que tu reconstruis ; les anciennes versions MIT conservent leur notice. Les [commits](https://github.com/steveprudhomme/sw233-flightgear/commits/main/) permettent de revoir les versions, mais tu n’as pas besoin de Git pour apprendre.

**Ce que “depuis zéro” veut dire ici.** Tu écris les fichiers de l’aéronef avec les blocs du livre, sans les prendre dans un avion déjà construit. FlightGear, JSBSim et Python sont les outils installés. Pour rejouer exactement notre film, la dernière séance réemploie les outils de tournage du projet et explique chacun. Aucune étape ne demande une IA.

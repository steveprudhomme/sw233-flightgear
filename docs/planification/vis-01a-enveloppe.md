# VIS-01a — enveloppe du cockpit et atlas pédagogique

Plan préparé le 13 novembre 2026, à commiter avant modification de la géométrie.

## Résultat attendu

Remplacer la découpe arbitraire du fuselage par une ouverture construite, raccorder les flancs jaunes à la verrière et préserver la vue du pilote. Illustrer les premières fiches avec les pièces réellement produites. Les dimensions tirées des dessins restent des estimations, sans prétendre à une reconstruction certifiée.

## Sous-étapes

1. Conserver un paquet avant modification ; relever les noms des pièces et la règle de suppression des faces. Distinguer trou, transparence et orientation des faces.
2. Examiner les plans de maquette, le trois-vues et les photos du cockpit. Noter points, proportions, incertitudes et choix de raccordement. Ne pas confondre structure réelle et maquette.
3. Capturer le modèle avant modification : profil, trois quarts, dessus et cockpit, avec réglages de caméra reproductibles.
4. Construire une ouverture supérieure explicite : flancs continus, bordures, raccord avant/arrière, montants jaunes et séparation visuelle des panneaux. Conserver les noms utilisés par les animations ; aucun changement du FDM ni promesse de porte fonctionnelle.
5. Ajouter des contrôles géométriques ciblés : raccords coque/verrière, absence de suppression globale et conservation des pièces animées. Reconstruire le maillage depuis le tutoriel.
6. Créer une recette d’atlas : chaque objet du fichier AC reçoit une illustration isolée avec son nom et ses dimensions ; ajouter des vues d’ensemble et coupes explicatives. Identifier clairement les schémas hors simulateur et les captures natives. Inclure une illustration pour chaque étape de construction et relier les premières fiches aux images pertinentes.
7. Refaire les mêmes vues FlightGear, inspecter les deux flancs et la vue cockpit. Vérifier instruments, commandes et absence d’obstruction ; corriger les défauts visibles.
8. Actualiser description et aperçu FlightGear si l’aspect change ; publier les images, l’atlas et le paquet depuis un commit identifié. Ajouter une fiche tutorielle détaillant diagnostic, mesures, construction, contrôles et limites ; mettre à jour les Markdown concernés.

## Critères de réussite

- Une ouverture voulue remplace le filtrage par moyenne des sommets ; les flancs ne disparaissent pas pour dégager les instruments.
- Les contours jaunes et la verrière se raccordent ; les commandes restent visibles depuis la place avant.
- Des captures natives comparables et des dessins de chaque objet permettent de comprendre ce qui a changé.
- Les recettes du tutoriel reconstruisent les sources ; les tests passent ; les médias publiés correspondent au nouveau paquet.

## Limites

Pas de copie des textures FSX/MSFS ni de redistribution automatique des photos tierces. Pas de dimensions constructeur inventées, pas de validation aérodynamique par une capture statique. Le cockpit photographique et la livrée finale restent distincts. Les pièces très détaillées peuvent être regroupées dans une vue d’assemblage, mais chaque objet nommé doit garder sa fiche dans l’atlas.

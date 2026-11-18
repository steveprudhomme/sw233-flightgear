# VIS-48 — fuselage et dimensions du manuel

Pour les personnes qui vérifient le modèle. Essais du 17 novembre 2026.
Plans préalables : `c5bdf32`, `8680b95` et `50a3de1`.

## Changements

- Dos arrière rectiligne entre x = 3,514 m et x = 7,61 m. Hauteurs estimées : 0,761048 m et 0,075 m.
- Corde maximale ramenée à 1,524 m ; raccords de racine mis à la même dimension.
- Empennage horizontal ramené à 2,3622 m d’envergure.
- Zone de texture des flancs agrandie ; bandes conservées dans le repère géométrique.
- Modèle de vol et masses inchangés. Ces changements portent sur le modèle visuel.

Source dimensionnelle : manuel fourni, page PDF 9 / A2. Stations : PDF 19–20 / A11–A12.
Voir le [registre des cotes](../references/manuel-stations-369.md).

## Contrôles réalisés

- 72 tests Python réussis, dont rectitude, dimensions, symétrie, fermeture et surfaces du paquet.
- Reconstruction du tutoriel identique aux sources ; contrôle Ruff réussi.
- Bas de coque : 54 stations communes avant/après comparées sous z = 0,07 m ; aucun changement à ces stations.
- FlightGear 2024.1.7 : huit captures natives de 1280 × 720, profils opposés, dessus et trois-quarts.
- Les deux séances utilisent CYJN, cap 190, même date simulée, même cadrage et aucun occupant.
- Une neuvième capture montre la verrière ouverte ; empreintes des images dans `fuselage-lot48.json`.
- 14 contrôles natifs de commande de verrière réussis dans le paquet corrigé.

Paquet avant : `D:/SW233-work/fuselage-48/avant`, source antérieure à VIS-48.
Paquet vérifié : `D:/SW233-work/fuselage-48/dimensions-v3`.
Rapport local : `D:/SW233-work/fuselage-48/native-report.json`.
Les images publiées sont dans `docs/images/lot48`.

Le profil confirme la disparition du creux arrière. La vue de dessus montre la réduction symétrique de l’empennage.
La jonction avec la dérive reste continue. L’éclairage assombrit certains panneaux ; les couleurs ne sont pas validées par cet essai.
Les premiers paquets dimensionnels ont été rejetés pour des sections superposées. Ils sont exclus des preuves finales.

## Limites

Les hauteurs du dos et les contours détaillés restent estimés.
Le manuel ne permet pas, dans les pages examinées, de placer les limites de verrière depuis le nez.
La hauteur totale publiée de 2,8321 m nécessite encore un contrôle de l’assiette et des points extrêmes.
Les stations du train nécessitent un recalage entre les repères du manuel et du modèle.
L’identité du tableau plastifié reste ouverte dans VIS-50c.
Les huit vues sont statiques ; elles ne prouvent pas la fidélité aérodynamique.
L’acceptation photographique de la silhouette complète reste ouverte.
Alpha.4 reste un brouillon ; aucune nouvelle version n’est publiée.

[Atelier illustré 29](../construction/29-dimensions-et-fuselage.md).

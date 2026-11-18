# DIM-51 — preuves de vérification

Pour les personnes qui vérifient le modèle. Essais du 17 novembre 2026.
Plan préalable : `51f3479`. Version : alpha.4 en préparation.

## Résultat

Les roues visuelles sont recalées depuis le bord avant de l’aile selon l’exemple A12 du manuel.
Seuls les objets `roue` et `roulette` du maillage ont changé.
La géométrie du nez, des ailes, de la verrière et du fuselage est identique au lot48.
Le modèle de vol, les masses et les contacts physiques sont inchangés.

- 75 tests Python réussis, dont trois nouveaux contrôles dimensionnels.
- Reconstruction du tutoriel identique aux sources.
- Quatre captures FlightGear 2024.1.7 de 1280 × 720, avant/après en profil et trois-quarts.
- Même position de départ, cap, date simulée et cadrages ; occupants masqués.
- Assiette avant/après : 0,740915 degré ; roulis −12,634288 et −12,634286 degrés.
- 14 contrôles natifs de commande de verrière réussis après correction.

Les valeurs, les chemins des paquets et les empreintes des images sont dans [le rapport JSON](dimensions-lot51.json).
Avant : paquet du lot48 `dimensions-v3`. Après : `D:/SW233-work/dimensions-51/candidat`.
La comparaison montre le recul de la roue principale. Celui de la roulette est plus discret.
Les dessins du manuel restent en local ; les images publiées sont des captures natives et un schéma original.

## Conclusions et limites

L’écart de hauteur est mesuré, mais sa correction n’est pas déterminée.
Sta.0 n’est pas identifié avec certitude par rapport au nez du maillage.
Les différences de stations permettent néanmoins de placer les roues depuis l’aile.
La validité pour C-FYLP reste à confirmer : la page A12 utilise l’appareil d’exemple numéro 369.
Les installations de roulette varient dans le catalogue ; leurs supports restent à reconstruire.
L’espacement des contacts physiques diffère de celui des roues visibles. DIM-52 doit traiter le recalage et les réactions au sol.
Les essais ne prouvent pas la fidélité du vol ni l’absence de pénétration au sol dans toutes les attitudes.
La silhouette complète de verrière reste à faire accepter ; aucune nouvelle version n’est publiée.

[Atelier illustré 30](../construction/30-reperes-et-train.md) · [Sources et calculs](../references/dimensions-lot51.md).

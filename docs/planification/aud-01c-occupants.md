# AUD-01c — masses des occupants

Préparé le 13 novembre 2026, avant réalisation. Statut : en cours.

1. Vérifier les propriétés JSBSim des deux masses ponctuelles et les exemples de menus de FlightGear installé ; garder les masses et bras historiques inchangés par défaut.
2. Ajouter un menu SW233 et une fenêtre dédiée : masse avant/arrière en livres, total et CG lus dans le moteur physique. Identifier le repère comme historique et non comme une enveloppe constructeur validée.
3. Séparer saisie et application ; refuser les valeurs invalides ou négatives, et les changements en vol. Les bornes de saisie techniques ne doivent pas être présentées comme limites aéronautiques.
4. Ajouter les préréglages de démonstration solo (180/0 lb), biplace (180/180 lb), ainsi que la restauration des valeurs présentes à l’ouverture.
5. Tester dans JSBSim les totaux et CG contre un calcul indépendant, puis dans FlightGear la saisie, le refus, les préréglages et la restauration.
6. Capturer la fenêtre dans FlightGear pour les cas solo et biplace, avec les propriétés effectives relevées ; distinguer ces essais au sol d’une validation du vol.
7. Ajouter une fiche de tutoriel complète avec les sources éditables, les calculs, les images et les limites ; conserver la reconstruction automatique du livre.
8. Actualiser README, INSTALL, validation, CHANGELOG et ROADMAP ; vérifier tests et reconstruction, commiter puis publier les preuves.

Critères : deux masses indépendantes ; valeurs affichées issues de JSBSim ; total et CG conformes au calcul pondéré ; refus sans modification partielle ; restauration vérifiée ; captures lisibles et tutoriel reproductible. Aucune affirmation de centrage admissible réel.

Résultat : fonctions et boutons réalisés ; six chargements calculés, huit états natifs, captures en [fiche 11](../construction/11-occupants.md). Les champs existent mais leur édition au clavier reste à confirmer manuellement ; le lot ne revendique pas cette validation. Les boutons par pas de 5 lb permettent un réglage indépendant.

Actualisation : la saisie via les chiffres du haut a été confirmée par l’utilisateur et relevée dans JSBSim ; restauration décimale corrigée. Le pavé numérique reste à investiguer séparément (AUD-01d).

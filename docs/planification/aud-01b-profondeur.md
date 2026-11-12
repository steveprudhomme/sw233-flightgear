# AUD-01b — protocole de réalisation

Statut : réalisé le 12 novembre 2026 ; protocole initial commité avant modification (`a1b9c2c`). Suivi : [ROADMAP](../../ROADMAP.md).

1. Conserver une copie du paquet et les résultats initiaux à 970 lb, 50 kt, compensation nulle. Vérifier les ±23° du manuel 1 040 lb déjà relevés (PDF 21/papier 41).
2. Remplacer uniquement le gain et les bornes de profondeur 0,30 rad par 23 × pi / 180. Ne changer aucun coefficient aérodynamique, masse ni point de référence.
3. La profondeur n'est pas encore une pièce séparée : découper une partie mobile dans chaque demi-empennage. Choisir et déclarer une charnière de maquette ; ne pas la présenter comme une cote constructeur. Garder un stabilisateur fixe.
4. Relier les deux pièces à la déflexion effective JSBSim en radians, convertir en degrés une seule fois ; vérifier le sens sur commande tirée/poussée, le neutre et les butées.
5. Mettre à jour les recettes des fiches 2, 3 et 4 et régénérer les fichiers éditables. Tester les demandes hors plage, la compensation et les noms d'objets.
6. Refaire l'équilibre au même chargement : comparer déflexion physique, commande normalisée, pente et trajectoire. Une diminution de commande normalisée seule n'est pas un gain aérodynamique.
7. Capturer dans FlightGear, à cadrage constant, neutre et deux butées. Relever commande et propriété effective avant/après capture ; distinguer banc d'animation et vol.
8. Mettre à jour tutoriel illustré, validation, sources, historique et statut du jalon. Vérifier tests et reconstruction, puis faire le commit de réalisation et publier les preuves.

Critère de réussite : butées effectives ±23° à la précision numérique, sens cohérent de l'animation, stabilisateur immobile, même équilibre physique à 50 kt (à tolérance publiée), résultats et limites accessibles. La position de charnière et le FDM restent approximatifs ; les limites de centrage ne sont pas validées par ce lot.

Résultats : [fiche 10 illustrée](../construction/10-profondeur.md), 15 tests réussis, contrôle natif des trois positions et équilibre physique conservé à 50 kt.

# Du document au modèle

Les numéros ci-dessous sont des **pages PDF, à partir de 1** ; le manuel de vol
est numérisé en doubles pages. Le classement décrit les données effectivement utilisées.

| Référence | Information utile | Décision |
|---|---|---|
| Manuel de vol fourni, PDF p. 4–6 | 2-33/2-33A : longueur 25 ft 9 in, envergure 51 ft ; limites distinctes pour différentes configurations. | Silhouette de 7,8486 × 15,5448 m ; aucune généralisation de la limite de 1 080 lb. |
| Même manuel, PDF p. 12, page imprimée 22 | Le frein de roue intervient à l’extrémité de la course du levier d’aérofreins. | Levier à gauche ; comportement du frein identifié pour la prochaine itération sol. Il n’est pas encore actif dans notre FDM. |
| Même manuel, PDF p. 14–15, pages imprimées 26–29 | Le datum est 66,34 in en avant du bord d’attaque à l’emplanture ; enveloppe chargée aux stations 78,20–86,10 in. Exemple du numéro 369 : 932 lb et station 83,13 in. | Exemple de référence pour un futur essai de masse, pas une pesée de notre cellule. Ne pas comparer aux stations JSBSim avant raccordement des origines. |
| Guide d’étude régional 2011/2012, PDF p. 265–270 | Circuit pitot-statique, distinction IAS/TAS, fonctionnement et retard du variomètre. | Prototype : vitesse calibrée comme approximation de l’IAS ; altitude MSL et vitesse verticale idéales. Le retard pneumatique et le calage ne sont pas simulés. |
| Manuel du programme 2017, PDF p. 213, page 2-7-19 | Vérification propre au type et reprise du dernier élément terminé après interruption. | Quatre listes manuelles de simulation. En cas d’interruption, reprendre le dernier élément traité. Pas d’automatisation d’une manœuvre réelle. |
| Photos C-FYLP et N2930H ; schéma du cockpit | Dispositions différentes selon l’exemplaire ; sur C-FYLP altimètre à gauche, vitesse en mph à droite, vitesse verticale en bas à droite. | Implantation inspirée de C-FYLP ; radio et compas opérationnels non inclus. |
| Trois-vues 2-33A, plans Short Kit, figures de visite | Aile haute, extrémités effilées, haubans, cockpit tandem et train monotrace. | Maillage original volumique. Les largeurs, épaisseurs et stations de forme sont approximatives ; les plans de maquette ne donnent ni profil certifié ni inerties grandeur. |

## Comparaison FlightGear et MSFS

La [fiche FlightGear](https://wiki.flightgear.org/Schweizer_2-33) décrit le
même paquet historique sgs233 étudié dans [sources.md](../sources.md), pas une
seconde validation. Son instrument netto décrit le mouvement de l’air ; notre
variomètre affiche la vitesse verticale de l’aéronef, grandeur différente.

L’[alpha 0.1 GS614](https://www.gs614.ca/SGS-233A-Glider/) fournit un paquet
MSFS. Le fichier effectivement lu est
`PackagesContent/gs614-aircraft-sgs233a/SimObjects/Airplanes/gs614_SGS233A_Aircraft/flight_model.cfg`,
dans SGS233AAircraftProject20230614.zip. Le fichier du remorqueur Bellanca a été écarté.

| Réglage de l’alpha, non mesuré | Valeur | Ce que nous en retenons |
|---|---:|---|
| Envergure / surface | 51 ft / 219,5 ft² | Cohérent avec les dimensions publiées arrondies. |
| Masse à vide / maximum du paquet | 612 / 1 080 lb | Ne pas appliquer ce maximum à tout 2-33. |
| Inerties roulis / tangage / lacet | 611 / 1 291 / 1 836 slug·ft² | Diffèrent de nos 1 800 / 850 / 1 950 ; étudier la sensibilité, sans moyenner les modèles. |
| Ailerons haut / bas ; profondeur haut / bas | 38° / 18° ; 23° / 23° | Les ailerons de notre prototype restent symétriques : écart identifié. |
| Aérofreins | Course simulée en 1 s | Paramètre d’animation MSFS, non mesure constructeur. |

Le [message 43](https://forums.flightsimulator.com/t/announcement-schweizer-sgs-2-33a-glider-freeware/550528/43)
est un ressenti sur le vol lent. La [réponse 44 du développeur](https://forums.flightsimulator.com/t/announcement-schweizer-sgs-2-33a-glider-freeware/550528/44)
précise le couplage du frein à la pleine sortie des aérofreins, cohérent avec le manuel.
Le [message 46](https://forums.flightsimulator.com/t/announcement-schweizer-sgs-2-33a-glider-freeware/550528/46)
attire l’attention sur le raccord des haubans et les logements d’aérofreins.
Aucun contenu du paquet MSFS n’est redistribué.

## Modes d’emploi

Dans FlightGear : vue pilote avant ; **Aide → Aircraft Checklists**. Le cadran gauche
donne l’altitude en pieds (aiguille longue : un tour pour 1 000 ft ; courte :
un tour pour 10 000 ft). À droite : vitesse en mph et vitesse verticale en
milliers de ft/min. Ce sont des indicateurs idéalisés du simulateur.
Le film utilise la même géométrie extérieure et une présentation pédagogique
des cadrans, sans prétendre être une capture du cockpit FlightGear.

### Pitot et fil de laine

Le manuel de vol fourni (§ 7, circuit pitot-statique) situe la tête au nez.
Les photos de la place avant guident son implantation visuelle. Dimensions,
couleur et courbure du fil sont des choix visuels, non des cotes constructeur.
Seul le fil tourne autour de son attache selon l'opposé de l'angle bêta JSBSim :
vent relatif de droite, extrémité à gauche ; vol coordonné, fil centré.
L'indication ne simule pas le flottement, la chute au repos ni les erreurs
pneumatiques. La lisibilité dans le moteur graphique reste à confirmer.

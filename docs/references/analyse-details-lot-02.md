# Détails du cockpit, ouverture et empennages — lot02

Reçu le 17 novembre 2026. Complément au [lot01](analyse-exterieur-lot-01.md).
**Périmètre de cette séance : conservation, analyse et planification. L'ouverture et les nouvelles pièces ne sont pas encore implémentées.**

## Originaux et lecture des images

Les onze fichiers reçus sont conservés sans retouche dans `docs/references/originaux/details-lot-02/`, y compris la copie issue du dossier temporaire. Sa galerie `index.html` permet de les revoir ensemble. Le [manifeste](details-lot-02.json) contient dimensions et empreintes SHA-256 vérifiées. Il y a **six nouvelles images distinctes**, quatre reprises exactes du lot01 et une copie exacte de DET-05 sous un nom de presse-papiers. Conserver les onze fichiers permet de retracer l'envoi, sans compter les doublons comme preuves indépendantes.

Comme le fonds existant, les originaux et la galerie restent locaux et exclus de Git ; l'analyse et le manifeste sont publiés. Auteur, date de prise de vue et droits de redistribution restent non établis. Les photos ne deviennent pas des textures GPL. Les personnes photographiées servent seulement à comprendre l'occupation et les occultations du cockpit ; aucune identité, taille corporelle ou qualification n'en est déduite.

| ID | Observation directe | Usage et réserve |
|---|---|---|
| DET-01 | Vue avant oblique, verrière basculée latéralement, cadre courbe, deux occupants, panneau gris derrière le poste arrière, harnais olive, mât avant ; spoilers visibles levés | Position ouverte et encombrement ; pas une mesure de l'angle d'ouverture ni une preuve complète de cinématique |
| DET-02 | Gros plan arrière : grande surface grise, raccord sous l'aile, vis, plaque, sangles olive, boucles de réglage métalliques et étiquette HOOKER HARNESS lisible | Construction du dossier et cheminement visible des sangles ; ancrages cachés et boucle centrale insuffisamment exposée |
| DET-03 | Verrière ouverte : courbure, cadre bleu, rangée de fixations, joint, poignées rouges et liaison avec ressort visible ; mât à deux branches ; emblème, chiffre 8, bande bleue et panneaux de fuselage | Référence forte de petits détails ; ne pas confondre une pièce aperçue derrière le vitrage avec une pièce fixée dessus |
| DET-04 | Queue : surface mobile verticale bleue, partie fixe jaune avec drapeau canadien ; charnières, limites de panneaux, empennage horizontal vu en biais, tringlerie/câbles apparents et roulette arrière | Séparer pièces fixes et mobiles ; la profondeur est sombre et partiellement masquée : sa teinte exacte n'est pas assurée par cette seule vue. Immatriculation tronquée, ne pas la compléter |
| DET-05 | Verrière ouverte, bord inférieur et fixations, cadre sous l'aile, habillage gris et sangle passant par une ouverture ; épaulières olive, emblème et nez numéroté | Complète DET-03 ; silhouette du vitrage et raccords, passage du harnais. Le numéro 8 seul n'établit pas l'identité de l'appareil |
| DET-06 | Cockpit sans occupant au fond : grand panneau gris avec relief supérieur et ouverture sombre, sangles olive, garnitures/coussins bleus, barre transversale et flancs ; élément rouge/blanc partiellement caché à droite | Référence essentielle pour géométrie normalement masquée. La fonction de l'élément rouge/blanc n'est pas déterminable ; ne pas le transformer automatiquement en poignée de largage |
| DET-07 | Copie exacte d'EXT-01 | Vue arrière générale ; aucune preuve supplémentaire indépendante |
| DET-08 | Copie exacte d'EXT-02 | Profil du patin, roue, nez et décoration |
| DET-09 | Copie exacte d'EXT-03 | Verrière fermée, mât et ficelle, comparaison avec l'ouverture |
| DET-10 | Copie exacte d'EXT-04 | Livrée C-GCLX lisible, éclair, numéro et drapeau ; ne pas l'attribuer à C-FYLP |
| DET-11 | Copie exacte de DET-05 | Conservée depuis le dossier temporaire ; pas un nouvel angle |

## 1. Verrière ouvrable au sol — exigence fonctionnelle

**Demande retenue : pouvoir ouvrir puis refermer la verrière au sol dans FlightGear.** Les images montrent une ouverture latérale, pas une verrière qui disparaît ou coulisse arbitrairement. La porte et le vitrage devront être identifiés comme ensembles distincts avant de décider quels éléments se déplacent ensemble.

Travail prévu :

1. Comparer les vues ouvertes DET-01/03/05 avec la vue fermée DET-09 et le schéma de cockpit déjà conservé. Identifier éléments fixes, mobiles, charnières, poignées, joint, butée et éventuel dispositif de retenue. Rechercher l'axe et le côté exacts, vus dans les axes de l'avion, et non « à gauche de la photo ».
2. Relever au moins trois points d'une ligne de charnière lorsqu'ils sont identifiables. Une seule photo ne fixe ni la position 3D ni l'angle maximal. Si nécessaire, demander une vue latérale de charnière et une courte vidéo d'ouverture ; conserver tout réglage estimé comme tel.
3. Séparer le maillage mobile, ses cadres, vis et poignées. Garder ensemble leurs textures et reflets. Contrôler le passage devant l'aile, le nez, le tableau et les deux occupants sur toute la course.
4. Prévoir une commande de menu bilingue et une poignée cliquable, avec un état commun pour les deux. Choisir un raccourci seulement après vérification des touches déjà utilisées. Prévoir états fermé/verrouillé, déverrouillé, en mouvement et ouvert si le mécanisme le justifie.
5. Pour cette première fonction, autoriser l'ouverture uniquement lorsque le planeur est au sol et immobilisé. La détection de contact sol, le seuil de vitesse et leur comportement sur une aile posée seront documentés et testés ; ce sont des choix de simulation, pas une limitation constructeur déduite des photos.
6. Vérifier fermeture, verrouillage et réinitialisation ; éviter fermeture instantanée ou téléportation en cas de changement de condition. Le comportement en vol sera explicite, sans inventer de largage d'urgence ni de traînée de verrière ouverte.
7. Relier le contrôle de verrière des checklists à l'état réel de la simulation. Un bouton de checklist ne doit pas prétendre verrouiller mécaniquement la verrière si son action est seulement une validation de lecture.

**Recette prévue :** cockpit et extérieur, ouverture à 0/25/50/75/100 % de la course, fermeture inverse, occupants masqués/présents, commande répétée, pause/réinitialisation, refus d'ouverture en vol. Le pourcentage décrit notre animation ; aucun angle réel n'est encore mesuré.

## 2. Poste arrière : panneau gris, coussins et habillages

DET-02/06 montrent beaucoup plus qu'un siège générique : une grande paroi grise montant sous l'aile, un relief supérieur, des vis, des changements de plan, une ouverture de passage de sangle, des panneaux latéraux et un raccord inférieur. On la nomme provisoirement **panneau/dossier arrière** ; sa fonction structurelle précise ne se déduit pas de son apparence.

Décomposer en pièces : panneau principal, relief supérieur, rebords, raccord sous aile, ouverture avec bord épais, vis apparentes, plaque séparée, garniture bleue du dossier, coussin visible au premier plan, flancs et traverse. Les plaques illisibles ne recevront pas un texte inventé. Les coussins auront une épaisseur, des angles adoucis, des coutures si attestées et une matière textile à échelle crédible ; aucune épaisseur en centimètres ne peut encore être certifiée.

Comparer le cockpit **vide** puis occupé. Les sièges doivent exister indépendamment des personnages et rester visibles quand leur masse vaut zéro. Relever largeur et hauteur par rapport aux cadres proches ; ne pas utiliser une tête humaine comme règle graduée.

## 3. Harnais verts/olive

Les vues révèlent sangles larges et plates, épaulières, ceinture ventrale, boucles métalliques de réglage, retours de sangle et étiquette de fabricant. Elles ne justifient pas un simple ruban rigide suspendu dans le torse.

Modéliser séparément chaque trajet visible : passage arrière, épaule, réglage, descente vers le bassin, ceinture latérale et extrémité libre. Donner une faible épaisseur et des bords arrondis aux sangles ; prévoir coutures et tissage dans la texture, pas des milliers de fils géométriques. Les boucles doivent conserver leurs ouvertures et leur passage de sangle. Distinguer sangle tendue sur occupant et sangle reposant sur le siège vide.

Ne pas inventer un nombre de points d'ancrage, une sangle sous-abdominale cachée ou un mécanisme de fermeture central. L'inscription HOOKER HARNESS est observée dans la photo ; elle n'établit pas la référence exacte du harnais ni son équipement sur tous les SGS 2-33. Les ailes et grades des personnages restent une autre question.

## 4. Pitot, mât et ficelle

DET-03/05/09 permettent d'étudier une embase plate fixée au nez, un montant élancé, deux branches coudées vers l'avant, leurs extrémités, une petite pièce annulaire sur une branche et l'attache de la ficelle. La couleur varie entre vues ; ne pas imposer une peinture rouge à toutes les variantes.

Relever hauteur apparente, diamètre apparent, espacement des branches, longueur des parties horizontales, rayons de courbure, inclinaison, embase et vis. Associer les relevés à leur photo et à leurs pixels ; convertir en mètres seulement avec une échelle fiable. Confirmer par schéma technique la fonction de chaque tube et prise avant de qualifier tout l'ensemble de tube de Pitot. Préserver ensuite le comportement existant de la ficelle en glissade, son origine, sa longueur et sa visibilité depuis le poste avant.

## 5. Empennages et décoration

La partie mobile verticale bleue et la partie fixe jaune avec drapeau sont nettement distinguables sur DET-04. Le gouvernail de profondeur bleu est une **cible demandée par l'utilisateur**, à confirmer par une vue correctement éclairée dessus/dessous pour l'appareil retenu ; la surface horizontale paraît sombre ici. Découper les UV selon les pièces fixes/mobiles, afin que le drapeau ne glisse pas sur la gouverne quand elle tourne.

Inventorier : sommet arrondi et débord éventuel de la partie mobile, bord d'attaque, charnières, jeux, épaisseur, raccord de pied, attaches de l'empennage horizontal, commande et roulette arrière. L'image tronque l'immatriculation : pas de complétion automatique.

Pour la livrée, DET-03/05 détaillent l'emblème avant et sa bordure ; DET-08/10 donnent bande latérale et éclair. Relever silhouette, proportions, position relative aux panneaux et orientation de chaque marquage. Préparer des dessins éditables avec provenance ; ne pas coller une photo avec ombres, reflet et perspective sur le fuselage. Ne pas mélanger des appareils parce qu'ils portent le même numéro 8. Le drapeau, l'emblème, le numéro de nez et la bande doivent appartenir à la variante documentée.

## 6. Largage arrière et patin

**Poignée de largage arrière : exigence retenue**, position et forme à recouper avec le schéma de commandes du cockpit et un gros plan identifiable. L'objet rouge/blanc de DET-06 n'est pas une preuve suffisante de sa fonction. Définir boule, tige/câble, support, course et accès depuis le poste arrière ; distinguer poignée de largage, commande de frein et autres équipements. Si la commande devient interactive, elle doit actionner le même mécanisme de largage que celle du poste avant, sans créer un second remorquage indépendant. Tester la correspondance seulement sur un système de remorquage validé.

Le patin de DET-08 présente une courbe longitudinale remontant vers le nez, une semelle, un espace par rapport au ventre et plusieurs supports visibles. Reprendre son profil, épaisseur, largeur, extrémités, attaches et matériau. Une bande droite collée sous le fuselage ne suffit pas. La géométrie visuelle du patin ne valide pas automatiquement les contacts et amortissements du FDM : leurs essais resteront séparés.

## Ce qui reste à mesurer et à vérifier

| Élément | Manque | Prochaine preuve utile |
|---|---|---|
| Verrière | Axe, butée, angle ouvert, relation avec porte | Gros plan charnières et vidéo latérale d'ouverture |
| Panneau/coussins | Largeur, profondeur, épaisseur et fixation | Cockpit vide, règle dans le même plan, vues avant et latérale |
| Harnais | Ancrages et fermeture centrale | Série de photos des sangles déroulées et boucles |
| Mât/Pitot | Dimensions, fonctions des branches | Schéma technique et cote de référence au même plan |
| Profondeur | Teinte et découpe des deux faces | Dessus/dessous éclairés, immatriculation identifiée |
| Largage arrière | Fonction et course de la poignée | Gros plan légendé et schéma concordant |
| Patin | Courbure réelle et supports cachés | Profil latéral et vue de dessous avec échelle |

**Biais à éviter :** saturation et ombres peuvent changer les couleurs ; la perspective déforme les longueurs ; les occupants masquent des pièces ; plusieurs photos ressemblantes peuvent représenter des appareils différents. Les détails observés sont la base de la modélisation, pas des mesures constructeur. Les nouvelles tâches restent ouvertes jusqu'à réalisation, capture native et comparaison visuelle. Les références complètent VIS-05 ; elles ne déclenchent pas une réécriture du modèle de vol.

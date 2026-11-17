# Finition du compas : preuves et limites

La photo C-FYLP `5d81c6bf…` fournie par l’utilisateur est la référence principale : emplacement sous l’aérateur, contour arrondi et quatre fixations. Voir l’[inventaire](inventaire.md) et les [limites des autres photos](cockpits-et-fsx.md). Le modèle précis du compas n’est pas identifié. Aucune cote constructeur nouvelle n’est déduite de cette photo oblique.

La largeur et la hauteur de maquette sont conservées ; rayons, joint et relief des vis sont des choix de représentation. La [fiche 2](../construction/02-maillage.md#o--comprendre-la-finition-du-compas-pièce-par-pièce) donne les calculs, les dimensions et les huit vues par pièce. La [fiche 6](../construction/06-peinture.md#o--finition-du-compas) distingue banc statique et essai en vol.

L’animation existante utilise `instrumentation/magnetic-compass/indicated-heading-deg`, pas le cap vrai. La rose, son axe et son facteur de rotation sont inchangés. Les propriétés du simulateur et les captures natives permettent de vérifier le comportement de ce modèle, pas celui d’un exemplaire réel.

Biais à garder visible : les dimensions de maquette antérieures servent d’ancrage ; la priorité de ce lot est l’arrondi et la lisibilité. Cette démarche ne prouve pas les dimensions physiques, la texture exacte ni les erreurs d’un compas réel. Une photographie nette avec règle et identification de l’instrument reste nécessaire pour dépasser cette approximation.

## Suite VIS-01o : bande graduée

La conservation de la rose décrite ci-dessus concerne le lot VIS-01n. Dans VIS-01o, seule sa géométrie de peinture change : les caractères en petits polygones laissent place à une texture dessinée avec Pillow et sa police fournie. Les mêmes inscriptions, l’axe et la liaison au cap indiqué sont conservés. La police exacte du compas photographié n’est toujours pas identifiée.

La composante d’émission du matériau de la rose vaut 0,45 par canal, choix de lisibilité après comparaison native ; elle ne modélise pas une lampe réelle. Les 48 contrôles sont des indications imposées dans FlightGear, pas une nouvelle validation dynamique. Voir la [recette et les preuves](../construction/06-peinture.md#p--des-lettres-plus-nettes-pour-le-compas).

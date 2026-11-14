# AUD-02b — présentation dans le sélecteur

Préparé le 13 novembre 2026 avant modification.

1. Vérifier le schéma du fichier set et les conventions de miniature/aperçu dans la documentation FlightGear et l’exemple installé ; ne pas inventer de balise de licence ni de score de qualité.
2. Conserver le titre demandé, préciser le statut de prototype, les auteurs et la licence dans les informations réellement affichées ; choisir un minimum conservateur correspondant à la version testée, sans prétendre à une compatibilité antérieure.
3. Capturer le modèle actuel dans FlightGear en vue extérieure, sous un éclairage lisible, ailes entièrement dans le cadre ; aucune livrée future ne doit être présentée comme réalisée.
4. Produire la miniature JPEG standard et un aperçu à partir de la capture native ; conserver les médias générés hors Git et documenter la recette/provenance. Prévoir une installation reproductible de ces médias dans le paquet sans dépendance réseau implicite.
5. Mettre à jour le constructeur et ses contrôles pour que les médias soient présents et couverts par les empreintes ; traiter explicitement le paquet sans médias pour éviter des références cassées.
6. Ouvrir le lanceur FlightGear sur un paquet neuf, vérifier la miniature, le titre et la description détaillée ; enregistrer une capture du sélecteur, pas seulement du XML.
7. Rédiger la fiche 13 avec les sources, mesures en pixels, étapes et images ; synchroniser le tutoriel et les Markdown.
8. Exécuter les tests et la reconstruction, commiter puis publier les médias et le paquet. L’essai natif Linux est suivi séparément sous AUD-02c.

Achèvement : captures réelles du modèle et de sa fiche, licence explicitée sans promesse de certification, métadonnées et ressources cohérentes, recette reproductible et limites documentées.

## Résultat vérifié

Les huit étapes sont réalisées. Voir la [fiche 13 illustrée](../construction/13-selecteur.md) : capture native, miniature 171 × 128, liste et détail du lanceur, 21 tests réussis et reconstruction du tutoriel. Publication : [selecteur-15](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/selecteur-15). Aucun essai Linux ni admission au catalogue officiel revendiqués.

# AUD-02a — paquet et lancement Windows

Préparation du 13 novembre 2026, avant réalisation.

1. Examiner le constructeur de paquet, les chemins documentés et les ressources référencées. Remplacer les anciennes instructions liées à un dossier personnel déplacé.
2. Contrôler après fabrication les références XML, maillage et textures ; joindre la licence et un manifeste d’empreintes. Refuser un paquet absent, incomplet ou modifié au lancement.
3. Fournir un lanceur Python transportable et une entrée Windows ; recevoir explicitement programme, fgdata et scenery, sans installer ni modifier FlightGear. Départ au sol par défaut à CYJN ; option de départ en vol clairement distincte.
4. Prévoir un mode de vérification sans démarrage et des erreurs compréhensibles ; conserver chaque argument comme élément distinct pour gérer les espaces. Vérifier présence de scenery sans prétendre certifier toute la couverture depuis un seul fichier.
5. Fabriquer puis copier le paquet dans un dossier neuf avec espaces, hors de son emplacement initial ; tester absence de texture, mauvais chemins et refus d’écrasement.
6. Lancer ce paquet déplacé dans FlightGear, vérifier le paquet effectivement chargé, les instruments, le menu des occupants et les propriétés des commandes. Capturer cockpit et fenêtre.
7. Rédiger la fiche 12 avec commandes, explications, captures et dépannage ; mettre à jour INSTALL, README, validation, CHANGELOG et ROADMAP.
8. Exécuter les tests pertinents et la reconstruction du tutoriel, commiter et publier les preuves. Linux, miniature du catalogue et automatisation des releases restent dans les lots suivants.

Achèvement : lancement Windows depuis dossier déplacé avec espaces, ressources contrôlées, messages d’erreur testés, preuves natives et tutoriel disponibles. Python reste requis pour ce premier lanceur ; aucun exécutable autonome ni installeur système n’est promis.

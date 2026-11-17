# Bilan de l’ouverture de verrière — lot44

Public : mainteneur et personnes qui vérifient la simulation.
Date : 17 novembre 2026. Version : 0.1.0-alpha.2.
Environnement : Windows, FlightGear 2024.1.7, JSBSim, CYJN.

| Vérification | Résultat | Portée |
|---|---|---|
| Clic sur la poignée droite | Réussi | Clic natif, ouverture observée |
| Boutons du menu | Réussi | Ouverture puis fermeture observées |
| États FR/EN dans la checklist | Réussi | Ouverte/Open puis Fermée et verrouillée/Closed and locked |
| Refus en vol et en déplacement | Réussi | Valeurs injectées dans une séance de test ; pas un parcours de vol |
| Pause, répétition, fermeture | Réussi | Inclus dans les 14 assertions natives |
| Signal de réinitialisation de la verrière | Réussi | Signal injecté : position ouverte remise à zéro |
| Réinitialisation complète du simulateur | Échec | Processus fermé sur candidate2, candidate3 et témoin alpha.1 |
| Vues à 0/25/50/75/100 % | Réussi | 30 captures : extérieur, cockpit, dessus ; personnages présents/absents |
| Pièces | Réussi | 84 objets illustrés ; groupes fixes et mobiles distincts |
| Suite du projet | Réussi | 66 tests ; contrôle de style réussi |
| Reconstruction du tutoriel | Réussi | Sources reconstruites à l’identique |
| Course réelle et cotes de charnière | Non confirmé | 100 degrés et axe estimés |
| Acceptation de ressemblance | En attente | Revue du mainteneur requise |
| Essai du tutoriel avec un enfant | Non testé | Aucun certificat de conformité annoncé |

## Dégagements et limites

Le vitrage central n’est plus recouvert par les racines d’aile.
La verrière mobile avant et le vitrage fixe arrière restent distincts.
Les positions échantillonnées permettent une inspection visuelle ; elles ne prouvent pas l’absence de collision continue.
L’aile, le nez, le tableau et les occupants restent à confronter aux cotes réelles.
Les formes de l’aile et les personnages conservent les simplifications déjà planifiées dans VIS-05.

## Réinitialisation complète : FG-44-01

La commande native `reinit`, envoyée par l’interface de développement, ferme le processus sans résultat exploitable.
L’essai a été reproduit avec la version témoin 0.1.0-alpha.1.
Un dossier utilisateur FlightGear isolé et inscriptible ne supprime pas l’échec.
Le journal indique aussi « Failed to save initial FDM property state » avant l’essai.
Cette observation ne suffit pas à établir la cause.
Le signal de réinitialisation seul remet correctement la verrière à zéro.
Ne pas confondre ce contrôle avec une réinitialisation complète réussie.
En attendant le diagnostic, fermer puis relancer FlightGear.

## Reproduire les contrôles

Dans une séance de développement dédiée, lancer :

```powershell
python -m tools.canopy_bench D:/SW233-work/nouvelle-recette --port 18175
python -m unittest discover -s tests
python -m tools.check_workbook D:/SW233-work/nouveau-livre
```

Le premier outil impose des positions pour les captures et remet la verrière fermée à la fin.
Il restaure les vues et les options qu’il modifie.
Ne pas l’utiliser pendant un vol personnel.
Le fichier `canopy-report.json` conserve la version, le dossier testé et les empreintes des images.
Les captures de recette utilisent candidate3 ; les sources d’aéronef du paquet publié sont identiques.
Les boutons et états supplémentaires ont été vérifiés dans une autre séance du même candidate3.

Les [références](../references/ouverture-verriere.md) distinguent observations et estimations.
Le [tutoriel26](../construction/26-ouverture-verriere.md) explique les manipulations au débutant.

## Publication et relecture

Source publiée : `9888552`. Les 44 fichiers de la publication ont été comparés aux empreintes locales.
Les contrôles GitHub Python 3.11 et 3.13 réussissent.
La page du tutoriel répond et contient ses six images avec texte alternatif.
Les liens locaux de ce nouvel atelier ont été vérifiés.
Le réglage de langue du site passe à `fr` après détection de la valeur anglaise par défaut.
Le zoom, le contraste de toute la page, le clavier et la compréhension par un enfant n’ont pas été audités dans ce lot.
Ces limites empêchent toute déclaration de conformité globale aux WCAG.

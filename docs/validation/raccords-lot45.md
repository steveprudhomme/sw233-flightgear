# Lot45 — raccords et dossier arrière

Pour les personnes qui vérifient le modèle. Essais du 17 novembre 2026, FlightGear 2024.1.7, Windows.

## Résultat

Le vitrage central utilise le profil supérieur des ailes. Deux bandes bleues couvrent les jonctions.
Les racines présentent des faces grises. Le dossier arrière comporte un relief, quatre vis et un passage noir en demi-lune.
Une sangle verte sort de ce passage. L’ouverture grillagée apparaît à gauche seulement.

## Contrôles

- 69 tests Python réussis ; trois nouveaux contrôles couvrent raccord, matériaux, asymétrie et relief.
- 14 contrôles de verrière exécutés dans FlightGear et réussis.
- Reconstruction depuis les blocs du tutoriel identique aux sources.
- Vérification de style réussie avec Ruff.
- 20 captures avant et 20 après : cinq vues, occupants présents/absents, verrière ouverte/fermée.
- Atlas de 95 objets et groupes raccords, dossier et ouverture gauche.

Les captures proviennent directement de FlightGear. La caméra de contrôle peut regarder vers l’arrière sans limite.
Le banc restaure les propriétés sauvegardées. L’éclairage vient d’une orientation à 190 degrés pendant les captures.
L’examen montre les bandes, les faces grises, le relief et la grille gauche. Les occupants restent devant le dossier.
Ce contrôle visuel ne remplace pas un relevé dimensionnel ni une validation de sécurité de l’aéronef réel.

## Reproduire

Dans une séance de contrôle dédiée, lancer :

```powershell
python -m tools.root_junction_bench nouveau-dossier --port 18182
python -m tools.parts_atlas nouvel-atlas
python -m unittest discover -s tests
python -m tools.check_workbook nouvelle-reconstruction
```

Adapter le port à celui de la séance dédiée. Le dossier de captures doit être nouveau.
Le banc change temporairement la vue, les occupants, la pause et la position de verrière.

## Limites

Les proportions du dossier et la grille sont estimées. Le diamètre de grille choisi est de 64 mm.
La fonction d’aération, les ancrages cachés, les coussins et le harnais complet ne sont pas validés.
La réinitialisation complète défaillante FG-44-01 reste ouverte. Elle n’a pas été retestée dans ce lot.
L’essai du tutoriel avec un débutant et l’acceptation de la ressemblance restent attendus.

Voir le [tutoriel27 avec images](../construction/27-raccords-arriere.md).

## Publication

Source `16e17d6`, préversion [0.1.0-alpha.3](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/v0.1.0-alpha.3).
Les empreintes des 51 fichiers publiés correspondent aux fichiers locaux. Le manifeste du paquet est vérifié.

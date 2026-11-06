# SW233 — Schweizer SGS 2-33 pour FlightGear

Construire une reproduction documentée, testable et progressivement fidèle du
planeur biplace Schweizer **SGS 2-33**. SW233 est le nom du projet, pas la
désignation constructeur.

Projet **libre et open source**, sous [licence MIT](LICENSE.md). Les anciennes
ressources FlightGear/JSBSim ne sont pas redistribuées ni relicenciées ici.

## État : prototype expérimental 0.1.0-dev

- Configuration FlightGear et FDM JSBSim originaux.
- Six composantes aérodynamiques, commandes et aérofreins.
- Aile haute effilée, haubans, verrière tandem, roue et patin.
- Poste avant : altimètre, anémomètre en mph et variomètre ; quatre check-lists de simulation.
- Documentation de provenance, tests automatisés et contrôles de contribution.

Les coefficients historiques sont des **paramètres de simulation à valider**,
pas des mesures constructeur. Pas encore de calibration pneumatique, de remorquage,
de modèle fiable de vrille, ni de validation complète dans FlightGear.
Ce projet n'est pas un outil d'instruction au vol réel.

## Vidéo : vol au-dessus de Saint-Jean-sur-Richelieu (CYJN)

[![Lire la démonstration du SW233 dans FlightGear au-dessus de CYJN](https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-01/SW233-CYJN.jpg)](https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-01/SW233-CYJN.mp4)

**[Voir le MP4 · 66 secondes](https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-01/SW233-CYJN.mp4)** — capture de FlightGear 2024.1.4 avec le décor TerraSync installé.
Passage en place avant à 8 s ; sortie et rentrée des aérofreins de 14 à 28 s ; virage en glissade à partir de 34 s.
Le médaillon agrandit la ficelle filmée et les valeurs affichées proviennent du même vol.
Voir [les mesures et la procédure de reproduction](docs/validation.md#capture-flightgear-à-cyjn).

## Démarrage rapide

Prérequis : FlightGear avec JSBSim ; Python 3.11+ pour les contrôles.

```sh
git clone https://github.com/steveprudhomme/sw233-flightgear.git
cd sw233-flightgear
python tools/package.py
fgfs --fg-aircraft=build/Aircraft --aircraft=sw233 --airport=KSFO --altitude=5000 --vc=50 --in-air --disable-ai-traffic
```

Exécuter la dernière commande depuis la racine du dépôt ; adapter le chemin de
`fgfs` sur Windows. L'altitude est en pieds au-dessus de la mer, `--vc` en nœuds.
La vidéo ci-dessus a été réalisée à CYJN avec le scénario de validation.
Voir [INSTALL.md](INSTALL.md) pour le lanceur graphique et les tests.

## Organisation

`src/SW233/` contient les sources éditables de l'aéronef ; `docs/` la provenance,
l'architecture et la validation ; `tests/` les essais ; `tools/` les contrôles
et la préparation du paquet. `build/` est généré et ignoré par Git.

## Communauté

- [Issues](https://github.com/steveprudhomme/sw233-flightgear/issues) : bugs, données et idées.
- [Pull requests](https://github.com/steveprudhomme/sw233-flightgear/pulls) : contributions techniques.
- [Contribuer](CONTRIBUTING.md), [conduite](CODE_OF_CONDUCT.md),
  [responsables](MAINTAINERS.md), [historique](CHANGELOG.md).

Les premiers fichiers ont été rédigés avec une assistance IA. Leur origine et
leurs limites sont explicites ; une revue humaine aéronautique reste nécessaire.

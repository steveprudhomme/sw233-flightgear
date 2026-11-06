# Schweizer SGS 2-33 aux couleurs Cadets de l’aviation royale du Canada

Construire une reproduction documentée, testable et progressivement fidèle du
planeur biplace Schweizer **SGS 2-33**. SW233 est le nom du projet, pas la
désignation constructeur. La livrée actuelle des Cadets est un objectif : le prototype filmé porte encore sa livrée jaune de développement.

Projet **libre et open source**, sous [licence GPL-3.0-only](LICENSE.md). Les anciennes
ressources FlightGear/JSBSim ne sont pas redistribuées ni relicenciées ici. Les versions déjà diffusées sous MIT conservent leur [notice historique](LICENSES/MIT-historical.txt).

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

[Comparer le poste avant dans FlightGear, avant et après correction](docs/construction/06-peinture.md#comparaison-cockpit) : la radio dégage le bord de l’altimètre et le compas décoratif apparaît sous la bouche d’air.

## Vidéo : vol au-dessus de Saint-Jean-sur-Richelieu (CYJN)

<video id="film" controls playsinline preload="none" style="max-width:100%" width="960" poster="https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-02/SW233-CYJN-v2.jpg" src="https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-02/SW233-CYJN-v2.mp4"></video>

**[▶ Lire le film dans le lecteur du projet · 1 min 23 s](https://steveprudhomme.github.io/sw233-flightgear/#film)** · [Télécharger le MP4](https://github.com/steveprudhomme/sw233-flightgear/releases/download/demo-cyjn-02/SW233-CYJN-v2.mp4)

Le lecteur intégré est disponible dans la version web de ce README. Dans le dépôt, GitHub affiche le lien de lecture. Capture native de FlightGear 2024.1.4 : sortie puis rentrée des aérofreins depuis le cockpit (14–28 s), second cycle vu du dessus (29–43 s), puis glissade depuis le cockpit et de l’extérieur (46–73 s). Le médaillon est un agrandissement de la ficelle filmée ; β mesure l’angle latéral du vent relatif dans le modèle.

**Pour construire depuis zéro :** [sept fiches de fabrication et leur cahier de mesures](docs/construction/README.md).

**Pour commencer :** [atelier pas à pas, dès 10 ans](docs/atelier.md) · [feuille de route du cockpit et de la livrée Cadets](ROADMAP.md) · [mesures et procédure](docs/validation.md#capture-flightgear-à-cyjn).

## Démarrage rapide

Prérequis : FlightGear avec JSBSim ; Python 3.11+ pour les contrôles.

```sh
git clone https://github.com/steveprudhomme/sw233-flightgear.git
cd sw233-flightgear
python -m pip install Pillow==12.0.0
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

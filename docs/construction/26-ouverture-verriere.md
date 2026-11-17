# 26. Ouvrir la verrière au sol

**Pour vous :** cet atelier s’adresse à un débutant, dès 10 ans, accompagné au besoin.
**But :** ouvrir la verrière avant, puis la refermer dans FlightGear.
**Avant de commencer :** installer FlightGear et le paquet `0.1.0-alpha.2` comme dans [l’atelier12](12-installation.md).

## Comprendre les pièces

La **verrière** est la partie transparente qui protège le poste de pilotage.
Une **charnière** permet à une pièce de tourner, comme une porte.
Le **verrou** maintient la verrière fermée.
Dans cette simulation, le verrou se ferme automatiquement à la fin du mouvement.

Le passager arrière reste sous l’aile.
Un vitrage fixe passe entre les deux ailes, au-dessus de sa place.
Ce vitrage ne suit pas la verrière avant quand elle s’ouvre.
La porte arrière reste fixe dans cette version.

![Vue de dessus : vitrage central entre les ailes et verrière avant ouverte sur le côté.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.2/dessus-equipage-0-100.png)

*Figure 1 — Capture FlightGear sans personnages. Le nez est en bas. Le vitrage central reste en place.*

Les photos DET-01, DET-03 et DET-05 montrent la verrière ouverte.
DET-02 et DET-06 montrent la place arrière sous l’aile.
DET-09 montre le vitrage fermé entre les ailes.
Retrouver les photos conservées dans le [dossier de références](../references/ouverture-verriere.md).

## Ouvrir et fermer

1. Placer le planeur au sol.
2. Immobiliser le planeur.
3. Ouvrir le menu **SW233**.
4. Choisir **Verrière / Canopy**.
5. Cliquer sur **Ouvrir / Open**.

**Résultat attendu :** la verrière avant tourne progressivement vers le côté gauche du planeur.
Le message passe à « Ouverte ».
La poignée rouge, les cadres, les joints et les vis suivent le vitrage.

![Verrière avant ouverte dans FlightGear, avec les occupants affichés.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.2/exterieur-equipage-1-100.png)

*Figure 2 — La partie avant s’ouvre. Les ailes et le vitrage arrière restent fixes.*

6. Cliquer sur **Fermer et verrouiller / Close and lock**.

**Résultat attendu :** la verrière revient progressivement à sa place.
Le message indique « Fermée et verrouillée ».
Le bouton **Retour / Back** ferme seulement la fenêtre de commande.

![Fenêtre de commande française avec la verrière fermée et verrouillée.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.2/commande-fr.png)

*Figure 3 — Lire le message pour connaître l’état. La couleur seule ne donne pas cette information.*

## Utiliser la poignée

1. Regarder le bord droit de la verrière avant depuis le siège avant.
2. Cliquer sur la poignée rouge.

**Résultat attendu :** la poignée commande la même ouverture que le menu.
Un nouvel appui pendant l’ouverture commande la fermeture.
Utiliser le menu si la poignée ouverte devient difficile à atteindre.
Aucun nouveau raccourci clavier n’est ajouté.

## Vérifier la liste et la langue

1. Ouvrir **SW233 → Checklists / Listes**.
2. Choisir la liste avant le décollage.
3. Lire la ligne de la verrière.
4. Changer la langue avec le menu **SW233**.

La ligne affiche l’état de la verrière avant.
Elle ne certifie pas la fermeture d’une porte arrière mobile : cette porte reste fixe.
Les mots-checks restent inchangés.
Le logiciel ne coche aucune vérification à votre place.

![Checklist française montrant l’état ouvert de la verrière.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.2/checklist-fr-ouverte.png)

*Figure 4 — L’état se met à jour dans la liste. Le pied de page rappelle que la porte arrière reste fixe.*

## Corriger un résultat différent

| Ce qui se passe | Ce qu’il faut faire |
|---|---|
| L’ouverture est refusée | Poser et immobiliser le planeur, puis redemander l’ouverture. |
| Le mouvement s’arrête pendant une pause | Quitter la pause. |
| Le planeur commence à rouler pendant l’ouverture | L’immobiliser, puis redemander l’ouverture ou la fermeture. |
| La poignée est difficile à viser | Utiliser le menu SW233. |
| La forme semble différente d’une photo | Consulter les limites ci-dessous avant de modifier les dimensions. |

La réinitialisation complète de FlightGear ferme le programme sur notre machine d’essai.
Le même problème apparaît avec la version précédente, sans cette animation.
Relancer FlightGear pour retrouver un état initial fermé.
Le [bilan des essais](../validation/verriere-lot44.md) distingue ce défaut du retour à zéro de la verrière.

## Comprendre nos choix

Ces valeurs règlent le modèle. Elles ne sont pas des mesures prises sur un vrai planeur.

| Choix | Valeur de simulation | Pourquoi |
|---|---|---|
| Côté de charnière | Gauche | Référence de mécanisme et photos d’ouverture |
| Course complète | 100 degrés | Première estimation visuelle, à faire confirmer |
| Durée | Environ 3 secondes de simulation | Permettre de voir le mouvement |
| Vitesse autorisant l’ouverture | Au plus 0,2 nœud au sol | Tolérer les petites variations du calcul de vitesse |
| Espace entre racines d’aile | 0,88 m | Dégager le vitrage central du modèle |

Un **nœud** est une unité de vitesse utilisée en aviation.
Une vitesse de 0,2 nœud représente environ 0,37 kilomètre par heure.
La nouvelle ouverture n’ajoute aucun effet sur le calcul du vol.
Elle ne simule pas le largage de la verrière.

## Voir chaque pièce

![Projections des pièces mobiles : vitrage avant, cadres, joints, vis et poignée.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.2/groupe-mobile.png)

*Figure 5 — Dessin du modèle, sans texture ni animation. Les dimensions sont celles de la simulation.*

![Projections du vitrage arrière et des charnières fixes.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.2/groupe-fixe.png)

*Figure 6 — Ces pièces restent en place pendant l’ouverture.*

L’[atlas complet des pièces](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.2/atlas-verriere.zip) contient une image par objet.
Les captures à 0, 25, 50, 75 et 100 % figurent dans les [preuves du lot44](https://github.com/steveprudhomme/sw233-flightgear/releases/tag/v0.1.0-alpha.2).
Elles montrent trois vues, avec et sans personnages.
Ces positions sont imposées pour examiner les formes. Elles ne mesurent pas la durée du mouvement.

## Retrouver les essais

Les essais ont lieu le 17 novembre 2026, dans FlightGear 2024.1.7 sous Windows.
Le clic sur la poignée, l’ouverture par menu et la fermeture ont été observés dans le simulateur.
Le contrôleur passe 14 vérifications natives : refus en vol, refus en déplacement, pause, répétition et fermeture, notamment.
Ces refus utilisent des valeurs de test injectées dans une séance isolée.
Ils ne constituent pas un essai en vol réel.

La course exacte, le mécanisme détaillé du verrou et l’acceptation de ressemblance restent à confirmer.
Les captures ne remplacent pas une détection complète des collisions entre surfaces.
L’essai du tutoriel avec un enfant reste à faire.
Le [guide de rédaction](../guide-redaction.md) est appliqué ; aucune conformité globale n’est déclarée.

## Reconstruire la commande

Cette partie s’adresse au lecteur qui reconstruit le modèle.
**Nasal** est le langage des petites commandes utilisées par FlightGear.
Le fichier XML relie ces commandes aux boutons de la fenêtre.

1. Reprendre la géométrie des [ateliers2](02-maillage.md) et [24](24-formes-avant.md).
2. Reprendre les animations de [l’atelier4](04-configuration.md).
3. Créer les deux fichiers ci-dessous avec leurs blocs complets.
4. Reprendre la liste bilingue de [l’atelier5](05-listes.md).
5. Reconstruire le paquet comme dans [l’atelier12](12-installation.md).

Les cadres mobiles portent les noms `cadre-mobile`, `joint-mobile` et `vis-mobiles`.
L’animation déplace ces objets avec `pare-brise` et `poignee-verriere`.
Le vitrage arrière conserve le nom `verriere`.
La commande partage une seule position avec le menu, la poignée et la checklist.

<!-- atelier-fichier: src/SW233/Nasal/canopy.nas -->
```nasal
# SPDX-License-Identifier: GPL-3.0-only
# Visual canopy only. Dimensions, duration and lock are simulation choices.
var base = "/sim/sw233/canopy/";
var position = 0;
var target = 0;
var refused = 0;
var stationary = func(wow, speed) {
    return wow == 1 and speed != nil and abs(speed) <= 0.2;
};
var publish = func {
    setprop(base ~ "position", position);
    setprop(base ~ "target", target);
    setprop(base ~ "locked", position == 0 and target == 0);
    var fr = getprop("/sim/sw233/language") != "en";
    var state = position == 0 and target == 0 ? (fr ? "Fermée et verrouillée" : "Closed and locked")
        : position == 1 ? (fr ? "Ouverte" : "Open")
        : (fr ? "En mouvement ou arrêtée" : "Moving or stopped");
    if (refused) state = fr ? "Refus : poser et immobiliser le planeur" : "Denied: land and stop the glider";
    setprop(base ~ "status", state);
};
var request = func(open) {
    if (open != 0 and open != 1) return 0;
    if (open and !stationary(getprop("/gear/gear/wow"), getprop("/velocities/groundspeed-kt"))) {
        refused = 1; publish(); return 0;
    }
    refused = 0; target = open; publish(); return 1;
};
var toggle = func { request(target == 0); };
var step = func(dt) {
    if (dt <= 0 or dt > 0.1) return;
    if (getprop("/sim/freeze/master") or getprop("/sim/freeze/clock")) return;
    # If motion starts while opening, hold this position. Never teleport shut.
    if (target > position and !stationary(getprop("/gear/gear/wow"),
                                         getprop("/velocities/groundspeed-kt"))) {
        target = position; refused = 1;
    }
    if (position < target) position = math.min(target, position + dt / 3);
    if (position > target) position = math.max(target, position - dt / 3);
    publish();
};
var reset = func { position = 0; target = 0; refused = 0; publish(); };
var status_line = nil;
var render_status = func(surface) {
    surface.set("view[0]",520).set("view[1]",55);
    surface.setColorBackground(0.96,0.96,0.93,1);
    status_line = surface.createGroup().createChild("text")
        .setFont("LiberationFonts/LiberationSans-Regular.ttf")
        .setFontSize(18).set("fill","#151515").setTranslation(10,32);
    status_line.setText(getprop(base ~ "status"));
};
setlistener(base ~ "status", func {
    if (status_line != nil) status_line.setText(getprop(base ~ "status"));
});
var loop = func { step(0.05); settimer(loop, 0.05); };
var dialog = gui.Dialog.new("/sim/sw233/canopy/dialog", "Aircraft/SW233/gui/dialogs/canopy.xml");
setlistener("/sim/sw233/language", publish);
setlistener("/sim/signals/reinit", func(n) { if (!n.getValue()) reset(); });
reset();
settimer(loop, 0.05);
```

<!-- atelier-fichier: src/SW233/gui/dialogs/canopy.xml -->
```xml
<PropertyList>
  <name>sw233-canopy</name><layout>vbox</layout>
  <text><label>SW233</label></text>
  <canvas><name>canopy-status</name><pref-width>520</pref-width><pref-height>55</pref-height>
    <nasal><load>sw233_canopy.render_status(canvas.get(cmdarg()));</load></nasal></canvas>
  <button><legend>Ouvrir / Open</legend><binding><command>nasal</command>
    <script>sw233_canopy.request(1);</script></binding></button>
  <button><legend>Fermer et verrouiller / Close and lock</legend><binding><command>nasal</command>
    <script>sw233_canopy.request(0);</script></binding></button>
  <button><legend>Retour / Back</legend>
    <binding><command>dialog-close</command></binding></button>
</PropertyList>
```

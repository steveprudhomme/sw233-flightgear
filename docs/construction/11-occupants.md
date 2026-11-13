# 11. Régler les occupants et lire le centrage

Séance AUD-01c, 13 novembre 2026. Le [plan](../planification/aud-01c-occupants.md) a été enregistré dans le commit `7a46cb2` avant de toucher l’avion.

## 1. Comprendre ce que nous construisons

Une balance avec deux personnes ne donne pas seulement un poids total. La position des personnes change aussi son point d’équilibre, appelé **centre de gravité**, ou CG. Ici, deux charges ponctuelles représentent les occupants ; elles existent déjà dans `src/SW233/sw233.xml`. Nous ajoutons leurs commandes dans FlightGear, sans modifier leurs bras ni les coefficients du vol.

Le menu **SW233 → Occupants et centrage** ouvre une fenêtre. Elle propose deux masses en livres (lb), quatre boutons de réglage par pas de 5 lb, des préréglages solo/biplace, une restauration et les valeurs effectives calculées par JSBSim. Les boutons appliquent immédiatement leur réglage au sol ; les champs doivent passer par **Appliquer**. Fermer la fenêtre ne remet pas les anciennes masses. Restaurer rétablit les masses présentes à sa dernière ouverture, pas forcément 180/180. Au prochain chargement de l’avion, les valeurs du FDM redeviennent la référence : nous n’ajoutons pas de sauvegarde automatique.

## 2. Relever les nombres avant de programmer

Ouvre la section `mass_balance` du FDM et prépare ce tableau sur papier :

| Élément | Masse (lb) | X (in) | Z (in) |
|---|---:|---:|---:|
| Planeur vide du prototype | 610 | 103,2 | −6,4 |
| Occupant avant par défaut | 180 | 43 | 4 |
| Occupant arrière par défaut | 180 | 85 | 4 |

Ces valeurs sont les hypothèses historiques du dépôt, **pas une pesée de C-FYLP**. Aucune nouvelle mesure sur une photographie n’est faite dans cette séance. Les fiches [8](08-centrage.md) et [9](09-reperes.md) expliquent pourquoi ces stations ne doivent pas être confondues avec les limites du manuel.

Multiplie chaque masse par sa position, additionne les produits, puis divise par la masse totale. Pour le biplace : `(610 × 103,2 + 180 × 43 + 180 × 85) / 970 = 88,651546 in`. Pour le solo : `(610 × 103,2 + 180 × 43) / 790 = 89,483544 in`. Le CG reste dans le repère historique. Ne le compare pas directement à une enveloppe constructeur utilisant un autre datum.

## 3. Séparer brouillon et réalité

Un champ de saisie est un brouillon : taper une lettre ou effacer un chiffre ne doit jamais envoyer une masse invalide au moteur physique. Nous utilisons `/sim/sw233/occupants/front` et `rear` pour les brouillons. Les masses réelles sont `/fdm/jsbsim/inertia/pointmass-weight-lbs` et `pointmass-weight-lbs[1]`. Le suffixe `[1]` signifie le deuxième élément : compter commence à zéro.

`apply` convertit les deux brouillons, valide les deux nombres, puis vérifie le contact de la roue principale et une vitesse sol d’au plus 1 kt. Si une condition échoue, aucune des deux masses n’est écrite. La plage 0–300 lb est une borne technique de saisie ; ce n’est ni une capacité de siège ni une autorisation de vol. La valeur zéro sert aussi aux essais du calculateur.

Les textes de résultat lisent directement `inertia/weight-lbs`, `cg-x-in` et `cg-z-in` : ils ne recopient pas notre calcul Python. Le calcul indépendant sert à détecter une liaison incorrecte. La fonction `stationary` est isolée pour vérifier les cas roue décollée, vitesse excessive et vitesse absente sans simuler un vol complet.

## 4. Écrire le module Nasal

Crée `src/SW233/Nasal`, puis `occupants.nas` avec le Bloc-notes en UTF-8. Nasal est le langage utilisé ici pour relier les boutons et les propriétés. Lis les fonctions dans l’ordre : `stage` prépare les champs ; `begin` conserve les masses à l’ouverture ; `apply` vérifie et écrit ; `preset` et `step` réutilisent cette vérification ; `restore` revient aux valeurs conservées. Une seule fonction écrit les masses pour que tous les boutons suivent les mêmes règles.

<!-- atelier-fichier: src/SW233/Nasal/occupants.nas -->
```nasal
# SPDX-License-Identifier: GPL-3.0-only
# Editing properties are strings; effective weights belong to JSBSim.
var base = "/sim/sw233/occupants/";
var front = "/fdm/jsbsim/inertia/pointmass-weight-lbs";
var rear = "/fdm/jsbsim/inertia/pointmass-weight-lbs[1]";
var saved = nil;
var message = func(s) { setprop(base ~ "message", s); };
var stage = func(a, b) {
    setprop(base ~ "front", sprintf("%.2f", a));
    setprop(base ~ "rear", sprintf("%.2f", b));
};
var begin = func {
    saved = [getprop(front), getprop(rear)];
    stage(saved[0], saved[1]);
    message("Saisie en lb. Appliquer au sol, avion arrete.");
};
var stationary = func(wow, speed) { return wow == 1 and speed != nil and abs(speed) <= 1; };
var apply = func {
    var a = num(getprop(base ~ "front"));
    var b = num(getprop(base ~ "rear"));
    if (a == nil or b == nil or !(a >= 0 and a <= 300 and b >= 0 and b <= 300)) {
        message("Refus : saisir deux nombres entre 0 et 300 lb."); return 0;
    }
    var wow = getprop("/gear/gear/wow");
    var speed = getprop("/velocities/groundspeed-kt");
    if (!stationary(wow, speed)) {
        message("Refus : poser et immobiliser le planeur."); return 0;
    }
    setprop(front, a); setprop(rear, b);
    message("Applique. CG historique : enveloppe reelle non validee.");
    return 1;
};
var preset = func(a, b) { stage(a, b); apply(); };
var step = func(which, delta) {
    var a = getprop(front); var b = getprop(rear);
    if (which == 0) { a += delta; } else { b += delta; }
    stage(a, b); apply();
};
var restore = func { if (saved != nil) { stage(saved[0], saved[1]); apply(); } };
var dialog = gui.Dialog.new("/sim/sw233/occupants/dialog", "Aircraft/SW233/gui/dialogs/occupants.xml");
```

## 5. Construire la fenêtre

Crée `src/SW233/gui/dialogs/occupants.xml`. `vbox` empile les lignes ; `hbox` place des éléments côte à côte. Les champs ne sont pas rafraîchis en continu, pour ne pas remplacer une saisie en cours. Les résultats utilisent `live` afin de suivre JSBSim. Le bouton Appliquer effectue `dialog-apply` (copier le brouillon), puis la vérification Nasal, puis `dialog-update` (rafraîchir la fenêtre). Les boutons de pas travaillent à partir des masses effectives : ils remplacent donc une éventuelle saisie non appliquée.

<!-- atelier-fichier: src/SW233/gui/dialogs/occupants.xml -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- SPDX-License-Identifier: GPL-3.0-only -->
<PropertyList>
  <name>sw233-occupants</name><layout>vbox</layout>
  <width>650</width><resizable>false</resizable><draggable>true</draggable>
  <nasal><open>sw233_load.begin();</open></nasal>
  <text><label>SW233 - Occupants et centrage</label></text>
  <text><label>Prototype : bras historiques, aucune enveloppe reelle validee.</label></text>
  <text><label>0 a 300 lb : bornes de saisie techniques, pas limites de vol.</label></text>
  <group><layout>hbox</layout><text><label>Occupant avant (lb)</label></text><input><name>front</name><property>/sim/sw233/occupants/front</property><live>false</live><pref-width>100</pref-width></input></group>
  <group><layout>hbox</layout><text><label>Occupant arriere (lb)</label></text><input><name>rear</name><property>/sim/sw233/occupants/rear</property><live>false</live><pref-width>100</pref-width></input></group>
  <group><layout>hbox</layout>
    <button><legend>Avant -5 lb</legend><binding><command>nasal</command><script>sw233_load.step(0,-5);</script></binding><binding><command>dialog-update</command></binding></button>
    <button><legend>Avant +5 lb</legend><binding><command>nasal</command><script>sw233_load.step(0,5);</script></binding><binding><command>dialog-update</command></binding></button>
    <button><legend>Arriere -5 lb</legend><binding><command>nasal</command><script>sw233_load.step(1,-5);</script></binding><binding><command>dialog-update</command></binding></button>
    <button><legend>Arriere +5 lb</legend><binding><command>nasal</command><script>sw233_load.step(1,5);</script></binding><binding><command>dialog-update</command></binding></button>
  </group>
  <text><property>/fdm/jsbsim/inertia/weight-lbs</property><format>Masse effective : %.2f lb</format><live>true</live></text>
  <text><property>/fdm/jsbsim/inertia/cg-x-in</property><format>CG X historique : %.4f in</format><live>true</live></text>
  <text><property>/fdm/jsbsim/inertia/cg-z-in</property><format>CG Z historique : %.4f in</format><live>true</live></text>
  <text><property>/sim/sw233/occupants/message</property><live>true</live></text>
  <group><layout>hbox</layout>
    <button><legend>Appliquer</legend><binding><command>dialog-apply</command></binding><binding><command>nasal</command><script>sw233_load.apply();</script></binding><binding><command>dialog-update</command></binding></button>
    <button><legend>Solo 180/0</legend><binding><command>dialog-apply</command></binding><binding><command>nasal</command><script>sw233_load.preset(180,0);</script></binding><binding><command>dialog-update</command></binding></button>
    <button><legend>Biplace 180/180</legend><binding><command>dialog-apply</command></binding><binding><command>nasal</command><script>sw233_load.preset(180,180);</script></binding><binding><command>dialog-update</command></binding></button>
    <button><legend>Restaurer</legend><binding><command>dialog-apply</command></binding><binding><command>nasal</command><script>sw233_load.restore();</script></binding><binding><command>dialog-update</command></binding></button>
  </group>
  <button><legend>Fermer</legend><key>Esc</key><binding><command>dialog-close</command></binding></button>
</PropertyList>
```

## 6. Brancher le menu et reconstruire

La [fiche 4](04-configuration.md) contient maintenant le fichier `sw233-set.xml` complet : sous `sim`, `menubar/default/menu` ajoute SW233 ; à la racine, `nasal/sw233_load/file` charge `Nasal/occupants.nas`. Ne place pas ce dernier bloc sous `sim`. Le menu appelle `sw233_load.dialog.open()`, et le module charge le XML de la fenêtre. Les sources restent originales ; les exemples du C172P installé ont servi à comprendre les mécanismes, pas à copier ses fonctionnalités.

Depuis la racine du dépôt, utilise des dossiers de sortie encore inexistants :

```powershell
# Reconstruire toutes les sources à partir du livre, y compris le nouveau module Nasal.
python tools/check_workbook.py build/livre-occupants
# Fabriquer un paquet autonome avec les textures.
python tools/package.py --output build/essai-occupants
```

Lance le paquet selon [INSTALL](../../INSTALL.md), au sol à CYJN. Ajoute `--httpd=18097` seulement pour le banc local. Ouvre le menu SW233. Si la barre des menus est masquée, réaffiche-la avant de chercher le menu. Essaye Solo, Biplace, Avant +5 et Arrière −5, puis Restaurer. Le CG doit changer même si la masse totale de deux configurations reste identique.

## 7. Lire les captures natives

FlightGear 2024.1.7, au sol à CYJN ; ce sont des captures du simulateur, sans reconstitution graphique. Le planeur est incliné sur son train, ce qui explique l’horizon penché.

![Solo : 790 lb et CG X 89,4835 in](https://github.com/steveprudhomme/sw233-flightgear/releases/download/occupants-12/solo.jpg)

![Biplace : 970 lb et CG X 88,6515 in](https://github.com/steveprudhomme/sw233-flightgear/releases/download/occupants-12/biplace.jpg)

![Deux masses différentes : 220 et 140 lb](https://github.com/steveprudhomme/sw233-flightgear/releases/download/occupants-12/personnalise.jpg)

![Valeur négative refusée, masses effectives conservées](https://github.com/steveprudhomme/sw233-flightgear/releases/download/occupants-12/refus.jpg)

Le message de refus est aussi important que les nombres : la saisie négative reste visible, mais les masses du FDM ne bougent pas. Les premières tentatives ont produit une capture d’un pixel puis une image noire ; elles ne sont pas utilisées comme preuves. Après relancement de la session visible, les captures ont été contrôlées visuellement.

## 8. Refaire les vérifications

```powershell
# Dans l’environnement Python du projet, avec JSBSim installé.
python -m unittest discover -s tests
# Dans une session FlightGear dédiée, chargée au sol, serveur local actif.
python -m tools.occupants_bench build/preuves-occupants --port 18097
```

Le test indépendant vérifie six chargements, dont le retour au chargement initial. Le banc natif vérifie huit états : solo, biplace, avant +5, arrière −5, 220/140, valeur négative, texte et restauration. Les valeurs effectives doivent correspondre au calcul à 0,0002 près (lb ou pouces selon la colonne). Le fichier `native.json` conserve valeurs attendues et reçues. Le contrôle au sol est également appelé avec quatre conditions synthétiques ; ce test ne prétend pas démontrer une tentative en vol réel dans le simulateur.

Les boutons solo et biplace ont aussi été actionnés à la souris. **Limite de vérification :** l’outil d’automatisation du clavier n’a pas permis de confirmer l’édition manuelle des champs. Les fonctions de validation sont testées, mais une relecture humaine de cette interaction reste à faire. Les boutons de pas offrent un autre chemin pour régler les occupants. Une validation n’est pas complète simplement parce que l’image semble correcte.

## 9. D’où viennent les choix ?

Références techniques : fichiers `Nasal/gui.nas`, `Aircraft/c172p/gui/dialogs/c172p-menu.xml` et `gui/dialogs/location-in-air.xml` de FlightGear installé ; [guide officiel de création de fenêtres](https://wiki.flightgear.org/Howto:Editing_and_creating_GUI_dialogs_in_FlightGear). Les propriétés physiques sont celles déjà utilisées et vérifiées dans le banc de centrage du projet. Biais restant : les masses et bras du prototype sont historiques et peuvent différer du planeur réel. Nous affichons donc un CG calculé, sans indicateur vert « autorisé ».

Point d’arrêt : compare les résultats à ton calcul papier, vérifie la restauration, ferme la fenêtre. Le lot garde une tâche de contrôle manuel de la saisie ; elle est visible dans ROADMAP, pas cachée dans les résultats.

# 5 · Fabriquer les cartes de vérification

![Contenu des quatre listes de simulation](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/listes.png)

Illustration du XML, pas une capture de la fenêtre FlightGear.

Regarde les quatre petites cartes sur les photos du poste avant : elles correspondent à des moments différents. Leur présence [V] nous suggère quatre listes. Le manuel du programme de 2017, PDF p. 213, explique comment reprendre une vérification interrompue. Les textes français ci-dessous expliquent les mots-checks anglais, selon le tableau fourni par le responsable du projet. Ils ne sont pas une transcription des IEA françaises. Voir la section G pour la vérification des sources et les initiales rouges.

**Fichier à écrire :** `src/SW233/Checklists/sw233.xml`. Colle les blocs de ce fichier dans l’ordre, sans retirer les espaces du début des lignes.

## A · Avant le départ

Fais une boîte checklist n=0. Pour chaque ligne, name est ce que tu cherches ; value est ce que tu veux pouvoir constater. Exemple : plutôt que « instruments OK », demande si tu sais quel cadran utilise mph et lequel utilise ft. Les tirets, accents et espaces sont autorisés dans les titres : le fichier est en UTF-8.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- English mnemonic letters; French explanations supplied by the project owner.
     Not a transcription of French AOIs. Values are simulation adaptations. -->
<PropertyList>
    <auto-tutorials type="bool">false</auto-tutorials>
    <checklist n="0">
        <title>SW233 - Avant décollage - BCISTRSC (simulation)</title>
        <item>
            <name>B - Lest, masse et centrage</name>
            <value>Scénario, masses et centrage vérifiés</value>
        </item>
        <item>
            <name>C - Commandes de vol</name>
            <value>Course et sens vérifiés</value>
        </item>
        <item>
            <name>I - Instruments et radio</name>
            <value>Unités, calage altimétrique et fréquence relus</value>
        </item>
        <item>
            <name>S - Déporteurs</name>
            <value>Course et position vérifiées</value>
        </item>
        <item>
            <name>T - Compensateur</name>
            <value>Position revue pour le scénario</value>
        </item>
        <item>
            <name>R - Mécanisme de largage</name>
            <value>Répétition verbale ; câble non simulé</value>
        </item>
        <item>
            <name>S - Sangles et harnais</name>
            <value>Revue visuelle simulée des deux places</value>
        </item>
        <item>
            <name>C - Verrière et porte</name>
            <value>Revue visuelle simulée</value>
        </item>
    </checklist>
```

## B · Avant le largage

Ajoute une deuxième carte dans la même racine. Dans cette version, aucun câble n’est simulé. Marque donc la répétition comme verbale au lieu de créer une action imaginaire.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
    <checklist n="1">
        <title>SW233 - Avant largage - AAAT (simulation)</title>
        <item>
            <name>A - Zone de largage</name>
            <value>Zone prévue repérée</value>
        </item>
        <item>
            <name>A - Altitude prévue</name>
            <value>Altitude du scénario revue</value>
        </item>
        <item>
            <name>A - Assiette et position derrière le remorqueur</name>
            <value>Assiette et position revues ; remorquage non simulé</value>
        </item>
        <item>
            <name>T - Circulation aérienne</name>
            <value>Trafic environnant repéré</value>
        </item>
    </checklist>
```

## C · Avant l’atterrissage

Sépare l’observation du vent et du trafic, la lecture de vitesse et la disponibilité des aérofreins. On ne déduit pas une vitesse d’approche d’une photographie de plaquette.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
    <checklist n="2">
        <title>SW233 - Avant atterrissage - SWARTSC (simulation)</title>
        <item>
            <name>S - Déporteurs</name>
            <value>Disponibilité et position vérifiées</value>
        </item>
        <item>
            <name>W - Vent</name>
            <value>Vent du scénario revu</value>
        </item>
        <item>
            <name>A - Vitesse d’approche</name>
            <value>Vitesse adaptée au scénario, lue en mph</value>
        </item>
        <item>
            <name>R - Communication radio</name>
            <value>Appel répété verbalement ; fonctionnement audio non validé</value>
        </item>
        <item>
            <name>T - Compensateur et trafic</name>
            <value>Position du compensateur et trafic revus</value>
        </item>
        <item>
            <name>S - Sangles et harnais</name>
            <value>Revue visuelle simulée des deux places</value>
        </item>
        <item>
            <name>C - Verrière</name>
            <value>Revue visuelle simulée</value>
        </item>
    </checklist>
```

## D · Avant un exercice

Écris les limites du modèle : une liste parcourue ne valide pas une vrille. Termine les deux dernières boîtes, checklist puis PropertyList. Les numéros vont de 0 à 3 sans répétition.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
    <checklist n="3">
        <title>SW233 - Sécurité avant manœuvres - ASCOT (simulation)</title>
        <item>
            <name>A - Altitude de sécurité</name>
            <value>Marges du scénario revues ; vrille non validée</value>
        </item>
        <item>
            <name>S - Harnais serrés</name>
            <value>Revue visuelle simulée des deux places</value>
        </item>
        <item>
            <name>C - Verrière verrouillée</name>
            <value>Revue visuelle simulée</value>
        </item>
        <item>
            <name>O - Objets libres</name>
            <value>Revue verbale des objets non arrimés</value>
        </item>
        <item>
            <name>T - Circulation aérienne et terrain</name>
            <value>Trafic et terrain du scénario revus</value>
        </item>
    </checklist>
    <placards>
        <card n="0">
            <line>AVANT DÉCOLLAGE</line>
            <line>B - LEST</line>
            <line>C - COMMANDES</line>
            <line>I - INSTRUMENTS/RADIO</line>
            <line>S - DÉPORTEURS</line>
            <line>T - COMPENSATEUR</line>
            <line>R - LARGAGE</line>
            <line>S - SANGLES/HARNAIS</line>
            <line>C - VERRIÈRE/PORTE</line>
        </card>
        <card n="1">
            <line>AVANT LARGAGE</line>
            <line>A - ZONE DE LARGAGE</line>
            <line>A - ALTITUDE</line>
            <line>A - ASSIETTE/POSITION</line>
            <line>T - CIRCULATION</line>
        </card>
        <card n="2">
            <line>AVANT ATTERR.</line>
            <line>S - DÉPORTEURS</line>
            <line>W - VENT</line>
            <line>A - VITESSE</line>
            <line>R - RADIO</line>
            <line>T - COMPENSATEUR/TRAFIC</line>
            <line>S - SANGLES/HARNAIS</line>
            <line>C - VERRIÈRE</line>
        </card>
        <card n="3">
            <line>SÉCURITÉ</line>
            <line>A - ALTITUDE</line>
            <line>S - HARNAIS</line>
            <line>C - VERRIÈRE</line>
            <line>O - OBJETS LIBRES</line>
            <line>T - CIRCULATION/TERRAIN</line>
        </card>
    </placards>
</PropertyList>
```

**Essai :** quand le paquet sera chargé, ouvre **Aide → Aircraft Checklists**. Tu dois trouver les quatre titres et respectivement **8, 4, 7 et 5 lignes**. Si le menu est vide, vérifie le C majuscule de *Checklists* et le chemin d’inclusion dans la fiche set. La lecture des listes ne commande aucune gouverne ; ces listes ne comportent pas de cases à cocher.

## Recette complète : sw233-en.xml

<!-- atelier-fichier: src/SW233/Checklists/sw233-en.xml -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Headwords: 2-33 AOIs 2017, PDF pp. 28/35. Values are simulation adaptations. -->
<PropertyList>
    <auto-tutorials type="bool">false</auto-tutorials>
    <checklist n="0">
        <title>SW233 - PRE TAKE-OFF (simulation)</title>
        <item>
            <name>Ballast</name>
            <value>Scenario loading and balance reviewed</value>
        </item>
        <item>
            <name>Controls</name>
            <value>Movement and direction checked</value>
        </item>
        <item>
            <name>Instruments</name>
            <value>Units, altimeter setting and radio frequency reviewed</value>
        </item>
        <item>
            <name>Spoilers</name>
            <value>Travel checked; position reviewed</value>
        </item>
        <item>
            <name>Trim</name>
            <value>Position reviewed for the scenario</value>
        </item>
        <item>
            <name>Release</name>
            <value>Verbal rehearsal only; tow cable not simulated</value>
        </item>
        <item>
            <name>Straps</name>
            <value>Simulated visual review, both seats</value>
        </item>
        <item>
            <name>Canopy/Door</name>
            <value>Simulated visual review</value>
        </item>
    </checklist>
    <checklist n="1">
        <title>SW233 - PRE RELEASE (simulation)</title>
        <item>
            <name>Area</name>
            <value>Release area identified in the scenario</value>
        </item>
        <item>
            <name>Altitude</name>
            <value>Scenario altitude reviewed</value>
        </item>
        <item>
            <name>Attitude/Position</name>
            <value>Attitude and position reviewed; tow not simulated</value>
        </item>
        <item>
            <name>Traffic</name>
            <value>Surrounding traffic reviewed</value>
        </item>
    </checklist>
    <checklist n="2">
        <title>SW233 - PRE-LANDING (simulation)</title>
        <item>
            <name>Spoilers</name>
            <value>Availability and position checked</value>
        </item>
        <item>
            <name>Wind</name>
            <value>Scenario wind reviewed</value>
        </item>
        <item>
            <name>Airspeed</name>
            <value>Scenario approach speed reviewed in mph</value>
        </item>
        <item>
            <name>Radio</name>
            <value>Call rehearsed; audio operation not validated</value>
        </item>
        <item>
            <name>Trim/Traffic</name>
            <value>Trim position and surrounding traffic reviewed</value>
        </item>
        <item>
            <name>Straps</name>
            <value>Simulated visual review, both seats</value>
        </item>
        <item>
            <name>Canopy</name>
            <value>Simulated visual review</value>
        </item>
    </checklist>
    <checklist n="3">
        <title>SW233 - SAFETY CHECK (simulation)</title>
        <item>
            <name>Altitude</name>
            <value>Scenario margins reviewed; spin behaviour not validated</value>
        </item>
        <item>
            <name>Straps</name>
            <value>Simulated visual review, both seats</value>
        </item>
        <item>
            <name>Canopy</name>
            <value>Simulated visual review</value>
        </item>
        <item>
            <name>Objects</name>
            <value>Loose items reviewed verbally</value>
        </item>
        <item>
            <name>Traffic/Terrain</name>
            <value>Traffic and terrain reviewed in the scenario</value>
        </item>
    </checklist>
    <placards>
        <card n="0">
            <line>PRE TAKE-OFF</line>
            <line>BALLAST</line>
            <line>CONTROLS</line>
            <line>INSTRUMENTS</line>
            <line>SPOILERS</line>
            <line>TRIM</line>
            <line>RELEASE</line>
            <line>STRAPS</line>
            <line>CANOPY/DOOR</line>
        </card>
        <card n="1">
            <line>PRE RELEASE</line>
            <line>AREA</line>
            <line>ALTITUDE</line>
            <line>ATTITUDE/POSITION</line>
            <line>TRAFFIC</line>
        </card>
        <card n="2">
            <line>PRE-LANDING</line>
            <line>SPOILERS</line>
            <line>WIND</line>
            <line>AIRSPEED</line>
            <line>RADIO</line>
            <line>TRIM/TRAFFIC</line>
            <line>STRAPS</line>
            <line>CANOPY</line>
        </card>
        <card n="3">
            <line>SAFETY CHECK</line>
            <line>ALTITUDE</line>
            <line>STRAPS</line>
            <line>CANOPY</line>
            <line>OBJECTS</line>
            <line>TRAFFIC/TERRAIN</line>
        </card>
    </placards>
</PropertyList>
```

## Recette complète : language.nas

<!-- atelier-fichier: src/SW233/Nasal/language.nas -->
```nasal
# SPDX-License-Identifier: GPL-3.0-only
# Session-only language choice. No aircraft controls are written.
var path = "/sim/sw233/language";
var busy = 0;
var apply = func {
    if (busy) return;
    busy = 1;
    var lang = getprop(path);
    if (lang != "fr" and lang != "en") { lang = "fr"; setprop(path,lang); }
    var dialog = props.Node.new({"dialog-name":"checklist"});
    var was_open = fgcommand("dialog-close",dialog);
    var target = props.globals.getNode("/sim/checklists",1);
    target.removeChildren();
    props.copy(props.globals.getNode("/sim/sw233/translations/"~lang),target);
    # Titles change; select the first list and discard old checklist UI state.
    props.globals.getNode("/sim/gui/dialogs/checklist",1).removeChildren();
    setprop("/sim/sw233/language-label",lang == "fr" ? "Français" : "English");
    busy = 0;
    if (was_open) gui.showDialog("checklist");
};
var choose = func(lang) { if (lang == "fr" or lang == "en") setprop(path,lang); };
var toggle = func { choose(getprop(path) == "fr" ? "en" : "fr"); };
setlistener(path,apply,1,0);
```


## G · Les lettres rouges sont un aide-mémoire

**État du travail : mots anglais comparés aux IEA de 2017 ; explications
françaises fournies par le responsable du projet.** Les lettres anglaises
sont conservées. La version française des IEA n’a pas été consultée.

Imagine huit petites cases, dans un ordre précis. Chacune contient une chose
à vérifier. Si tu retires une case pour gagner de la place, tu changes ce
que l'élève apprend. C'est pourquoi nous avons rétabli les huit rubriques
anglaises avant le décollage, au lieu des quatre rappels abrégés précédents.

![Principe des initiales rouges, illustration explicative](../illustrations/initiales-checklist.svg)

Cette illustration explique la construction ; ce n'est pas une capture de
FlightGear. Les captures natives de la section H montrent le résultat et le défaut
de masquage restant à corriger.

1. Ouvre la source indiquée dans [le registre des sources](../sources.md#vérifications-mnémotechniques--lot-vis-01p-17-novembre-2026).
   Lis la page imprimée 3-8 (page 28 du PDF). Relève chaque rubrique sans
   changer son ordre : Ballast, Controls, Instruments, Spoilers, Trim,
   Release, Straps, Canopy/Door. Leurs initiales donnent **BCISTRSC**.
2. À la page imprimée 4-3 (PDF 35), relève les autres groupes : **AAAT**
   avant le largage, **SWARTSC** avant l'atterrissage et **ASCOT** pour la
   vérification de sécurité. Attitude/Position forme une rubrique ; ne
   transforme pas le P en une nouvelle étape. Même principe pour
   Trim/Traffic et Traffic/Terrain.
3. Dans le XML anglais, conserve une ligne par rubrique. La liste affichée
   dans la fenêtre emploie les mêmes mots. Son explication indique ce que
   notre simulateur permet réellement : le câble, par exemple, n'est pas
   simulé. Les intitulés viennent de la source ; ces explications sont
   rédigées pour notre prototype.
4. Dans la recette de peinture, le titre est la ligne 0. Il reste noir.
   Pour les lignes suivantes, dessine le texte noir puis sa première lettre
   en rouge sombre (`#a01820`). Le reste garde la couleur `#25272a`.
   On colore l'initiale de la rubrique, pas celle de chaque mot secondaire.
5. Une carte mesure 512 × 768 pixels dans la texture. Le titre commence à
   65 pixels du haut, le premier élément à 185. Répartis les éléments dans
   510 pixels : l'espacement vaut au maximum 130 pixels. La taille des
   lettres diminue si la carte contient davantage d'éléments ou un mot long.
   On fait entrer les mots en adaptant la mise en page, jamais en supprimant
   une vérification.
6. Vérifie les accents : l'accent d'une initiale rouge doit lui aussi être
   rouge. Vérifie le pied « SIMULATION » et l'absence de texte coupé.
7. Reconstruis le paquet et ouvre les deux textures de plaquettes. Puis
   contrôle la lisibilité dans FlightGear, avec le menu Français / English
   et Ctrl+L. La fenêtre native conserve pour l'instant son style de texte :
   le rouge concerne les plaquettes 3D, pas les lignes de cette fenêtre.

Le raccourci Ctrl+L a été confirmé manuellement par l'utilisateur lors de
l'essai précédent. Cela ne valide pas encore le nouveau contenu des cartes.
La fiche native est une liste de textes : ne suppose pas qu'elle possède
une case à cocher pour chaque élément.


## H · Pourquoi lit-on « S — Déporteurs » en français ?

Le mot anglais **Spoilers** commence par S. Le mot français **Déporteurs**
commence par D. Si nous colorions seulement le D, BCISTRSC deviendrait une
autre série de lettres ! Nous gardons donc le S à gauche, en rouge, et
écrivons son explication française à droite. Même principe pour W — Vent.

Le tableau français a été fourni par le responsable du projet le
17 novembre 2026. Nous conservons cette origine dans le registre des sources.
Une explication traduite n'est pas la preuve qu'un nouveau mot-check français
est officiellement enseigné. La petite carte emploie des intitulés courts ;
la fenêtre de checklist donne les intitulés français complets.

Pour refaire cette étape :

1. Recopie les lettres anglaises, dans l'ordre : BCISTRSC, AAAT, SWARTSC, ASCOT.
2. Associe chaque lettre à une explication française du tableau fourni.
3. Dans chaque champ `name`, écris la lettre, un tiret, puis l'explication.
4. Dans chaque ligne de plaquette, garde la même lettre et le même ordre.
5. Compte les rubriques : 8, 4, 7, 5. Il doit y en avoir autant en français
   qu'en anglais et autant dans la fenêtre que sur la carte correspondante.
6. Reconstruis les textures. Vérifie que le S de « S - DÉPORTEURS » est rouge,
   que le D reste noir, et que les accents ne disparaissent pas.

Les urgences GASP/VEST et GPAS/PTES sont inscrites au ROADMAP dans un travail
séparé. Il faut encore vérifier le manuel bilingue de 2018 et définir ce
que le prototype peut simuler avant de créer leurs listes. Les inspections
au sol sont également recensées séparément.


### Voir le résultat dans FlightGear

![Plaquettes françaises, capture native statique](https://github.com/steveprudhomme/sw233-flightgear/releases/download/plaquettes-fr-33/fr-mots-checks.jpg)

Repère les lettres rouges à gauche de chaque ligne. Les cartes conservent
les mêmes initiales que les listes anglaises. L'anémomètre cache encore une
partie des mots sur la droite : cette image montre un défaut à corriger,
pas une validation de lisibilité complète.

![Vue décalée montrant le masquage par la bague](https://github.com/steveprudhomme/sw233-flightgear/releases/download/plaquettes-fr-33/fr-mots-checks-droite.jpg)

Ces vues utilisent le mode statique de développement, sans dynamique de vol.
Les aiguilles visibles ne constituent pas un essai de performances. Pour
refaire l'observation, charge le paquet, sélectionne Français dans le menu
SW233 et compare la vue pilote avec une vue rapprochée du tableau. Regarde
si la dernière lettre de chaque ligne est visible. Un test de fichiers peut
réussir alors qu'une pièce en cache une autre : il faut les deux contrôles.

![Texture française complète, avant projection sur les cartes 3D](https://github.com/steveprudhomme/sw233-flightgear/releases/download/plaquettes-fr-33/placards-fr.png)

La texture est complète ; le masquage apparaît dans la scène 3D. Cette
comparaison permet de chercher le problème dans la géométrie et la vue,
plutôt que de supprimer des mots de la liste.

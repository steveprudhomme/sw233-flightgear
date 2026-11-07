# 4 · Donner un nom à l’avion et faire tourner les bonnes pièces

Tu vas écrire deux fichiers, et non un seul. La fiche **set** est l’étiquette sur la boîte : elle indique à FlightGear quel avion ouvrir. Le fichier **model** est le mode d’emploi des pièces mobiles. Une animation est une règle : « lis ce nombre, multiplie-le, tourne cette pièce autour de ce point ». Les balises XML doivent toujours se refermer en ordre inverse.

**Fichier à écrire :** `src/SW233/sw233-set.xml`. Colle les blocs de ce fichier dans l’ordre, sans retirer les espaces du début des lignes.

## A · Nomme et relie

Commence par une seule racine PropertyList. Dans sim, la description est le titre affiché ; le nom de fichier sw233-set.xml détermine l’identifiant sw233. `jsb` choisit JSBSim ; `aero` vaut sw233 sans extension pour charger sw233.xml.

<!-- atelier-fichier: src/SW233/sw233-set.xml -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- SPDX-License-Identifier: GPL-3.0-only
     Original SW233 integration. No global weather or joystick overrides. -->
<PropertyList>
    <sim>
        <description>Schweizer SGS 2-33 — Cadets de l’aviation royale du Canada (prototype)</description>
        <author>SW233 contributors</author>
        <flight-model>jsb</flight-model>
        <aero>sw233</aero>
        <model>
            <path>Aircraft/SW233/Models/sw233-model.xml</path>
        </model>
```

## B · Assieds-toi à la place avant

Pour la caméra, l’ordre est droite, haut, arrière. Le milieu du siège est à droite = 0, hauteur choisie = 0,50 m et recul choisi = 1,65 m. Ne copie pas l’ordre des colonnes AC3D. L’angle −18° aide à voir la planche ; le champ de 80° et le plan proche de 0,02 m ont été choisis dans le simulateur. La balise internal permet d’afficher l’intérieur.

<!-- atelier-fichier: src/SW233/sw233-set.xml -->
```xml
        <view n="0">
            <internal type="bool">true</internal>
            <config>
                <!-- View system: right, up, aft offsets (metres). -->
                <x-offset-m>0</x-offset-m>
                <y-offset-m>0.50</y-offset-m>
                <z-offset-m>1.65</z-offset-m>
                <pitch-offset-deg>-18</pitch-offset-deg>
                <default-field-of-view-deg>80</default-field-of-view-deg>
                <ground-level-nearplane-m>0.02</ground-level-nearplane-m>
            </config>
        </view>
```

## C · Donne l’adresse des listes

Ce chemin part du dossier SW233, pas du dossier Models. La liste sera écrite à la séance suivante. Les tags servent au classement : ils ne transforment pas un avion motorisé en planeur.

<!-- atelier-fichier: src/SW233/sw233-set.xml -->
```xml
        <checklists include="Checklists/sw233.xml"/>
        <tags>
            <tag>glider</tag>
            <tag>unpowered</tag>
        </tags>
    </sim>
</PropertyList>
```

**Fichier à écrire :** `src/SW233/Models/sw233-model.xml`. Colle les blocs de ce fichier dans l’ordre, sans retirer les espaces du début des lignes.

## D · Indique le dessin

Le chemin est relatif à ce fichier : sw233.ac est dans le même dossier. Les accents ne sont pas permis par magie dans les noms : copie exactement les noms écrits par ta recette.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
<PropertyList>
  <path>sw233.ac</path>
```

## Centaines de pieds

À 500 ft, 500 × 0,36 = 180° : un demi-tour de la grande aiguille. Son pivot est au centre du cadran gauche.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>alt-centaines</object-name>
    <property>position/altitude-ft</property>
    <factor>0.36</factor>
    <offset-deg>0</offset-deg>
    <center>
      <x-m>0.882</x-m>
      <y-m>-0.22</y-m>
      <z-m>0.087</z-m>
    </center>
    <axis>
      <x>-1</x>
      <y>0</y>
      <z>0</z>
    </axis>
  </animation>
```

## Milliers de pieds

La petite aiguille fait le tour en 10 000 ft : 360 / 10 000 = 0,036 degré par pied. À 500 ft elle fait 18°, pas 180°.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>alt-milliers</object-name>
    <property>position/altitude-ft</property>
    <factor>0.036</factor>
    <offset-deg>0</offset-deg>
    <center>
      <x-m>0.882</x-m>
      <y-m>-0.22</y-m>
      <z-m>0.087</z-m>
    </center>
    <axis>
      <x>-1</x>
      <y>0</y>
      <z>0</z>
    </axis>
  </animation>
```

## Vitesse

La propriété est en nœuds, le cadran en mph. Un nœud vaut environ 1,150779 mph. Le dessin réserve 280° à 160 mph : 280 / 160 × 1,150779 ≈ 2,013864° par nœud. Le zéro est dessiné à −140°. À 60 kt, attends-toi à environ 69 mph.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>vitesse-mph</object-name>
    <property>fdm/jsbsim/velocities/vc-kts</property>
    <factor>2.013864034</factor>
    <offset-deg>-140</offset-deg>
    <center>
      <x-m>0.882</x-m>
      <y-m>0.17</y-m>
      <z-m>0.14</z-m>
    </center>
    <axis>
      <x>-1</x>
      <y>0</y>
      <z>0</z>
    </axis>
  </animation>
```

## Montée et descente

Le simulateur donne des pieds par seconde ; le cadran compte des milliers de pieds par minute. 65 × 60 / 1000 = 3,9° par ft/s. À −1000 ft/min, l’angle vaut −65°.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>vario</object-name>
    <property>velocities/vertical-speed-fps</property>
    <factor>3.9</factor>
    <offset-deg>0</offset-deg>
    <center>
      <x-m>0.882</x-m>
      <y-m>0.295</y-m>
      <z-m>0.022</z-m>
    </center>
    <axis>
      <x>-1</x>
      <y>0</y>
      <z>0</z>
    </axis>
  </animation>
```

## Fil de laine

La propriété bêta décrit l’air qui arrive de côté. Avec notre axe vertical +z et ce maillage, le facteur −1 fait partir la pointe libre de l’autre côté. À β = 0°, le fil est dans l’axe. La rotation porte seulement sur le fil et non le Pitot.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>fil-de-laine</object-name>
    <property>fdm/jsbsim/aero/beta-deg</property>
    <factor>-1</factor>
    <center>
      <x-m>-0.055</x-m>
      <y-m>0</y-m>
      <z-m>0.237</z-m>
    </center>
    <axis>
      <x>0</x>
      <y>0</y>
      <z>1</z>
    </axis>
  </animation>
```

## Aérofrein gauche

Le bord avant garde sa place, le bord arrière monte. Propriété 0 = rentré ; 1 = ouvert. Les 85° sont une amplitude visuelle choisie, pas un débattement mesuré sur le planeur réel.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>aerofrein-1</object-name>
    <property>fdm/jsbsim/fcs/speedbrake-pos-norm</property>
    <factor>85</factor>
    <center>
      <x-m>2.41</x-m>
      <y-m>-0.98</y-m>
      <z-m>0.86</z-m>
    </center>
    <axis>
      <x>0</x>
      <y>-1</y>
      <z>0</z>
    </axis>
  </animation>
```

## Aérofrein droit

Le y du pivot change de signe car on change d’aile, mais on garde le même sens de rotation : les deux bords arrière doivent monter ensemble.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>aerofrein1</object-name>
    <property>fdm/jsbsim/fcs/speedbrake-pos-norm</property>
    <factor>85</factor>
    <center>
      <x-m>2.41</x-m>
      <y-m>0.98</y-m>
      <z-m>0.86</z-m>
    </center>
    <axis>
      <x>0</x>
      <y>-1</y>
      <z>0</z>
    </axis>
  </animation>
```

## Levier dans le cockpit

Le levier suit la position des aérofreins avec une amplitude visuelle de −35°. Si la poignée se déplace toute entière, vérifie le pivot (1,19 ; −0,34 ; −0,13) avant de changer le signe.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>poignee-frein</object-name>
    <property>fdm/jsbsim/fcs/speedbrake-pos-norm</property>
    <factor>-35</factor>
    <center>
      <x-m>1.19</x-m>
      <y-m>-0.34</y-m>
      <z-m>-0.13</z-m>
    </center>
    <axis>
      <x>0</x>
      <y>-1</y>
      <z>0</z>
    </axis>
  </animation>
```

<a name="rose-magnetique"></a>

## Lire le cap derrière le trait fixe

Ajoute ce dernier bloc au fichier des animations. Imagine que tu regardes un rouleau à travers un petit guichet. Fais tourner le rouleau (*compas-rose*), sans toucher au guichet ni au trait ! Le centre de rotation est à x = 0,870 − 0,037 = 0,833 m, au milieu de la rose. Un degré indiqué fait tourner le tambour d’un degré autour de l’axe vertical. Les lettres sont disposées dans le sens opposé lors de la construction : à 090°, E arrive sous le trait.

Lis **indicated-heading-deg** : c’est ce qu’indique le compas du simulateur. Le cap vrai se rapporte au nord géographique ; le cap magnétique se rapporte au nord magnétique. L’indication de l’instrument peut en plus différer du cap magnétique. Le branchement suit la propriété utilisée dans le fichier *Aircraft/Instruments-3d/mag-compass.xml* fourni avec FlightGear 2024.1.7.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>compas-rose</object-name>
    <property>instrumentation/magnetic-compass/indicated-heading-deg</property>
    <factor>1</factor>
    <center><x-m>0.833</x-m><y-m>0</y-m><z-m>0.098</z-m></center>
    <axis><x>0</x><y>0</y><z>1</z></axis>
  </animation>
</PropertyList>
```

**Contrôle sans voler :** rapproche chaque `object-name` de la ligne `name` correspondante dans le fichier AC3D. Les aiguilles tournent dans le plan de la planche, autour de −x ; la ficelle autour de +z ; les panneaux autour de −y. Un nom faux peut laisser l’objet visible mais immobile. Une balise mal refermée peut empêcher de charger toute la fiche.

**Essai au banc, dans une session de simulation dédiée.** Ouvre le navigateur de propriétés du menu Débogage, puis *instrumentation → magnetic-compass*. Note la valeur de *serviceable*. Mets-la temporairement à faux pour empêcher l’instrument de réécrire ton entrée. Dans *indicated-heading-deg*, saisis successivement 90, 180, 270, 359, 0 et 1. Relis chaque valeur avant de regarder la fenêtre. Le trait reste au centre : E, S et W passent dessous ; puis N se décale légèrement d’une image à la suivante. Remets *serviceable* à sa valeur initiale avant de voler. Si ton entrée change toute seule, l’instrument fonctionne encore : tu observes sa réponse, pas un angle imposé.

![Captures natives : est, sud, ouest puis trois positions de la rose au passage du nord.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-magnetique-04/SW233-compas-magnetique.png)

Les six vignettes sont des recadrages de FlightGear 2024.1.7 à CYJN. Pour les retrouver, reprends la caméra de face de la fiche 6, avec une inclinaison de −26° et un champ de 17°. Les valeurs affichées au-dessus des images sont les entrées d’essai. En fonctionnement normal, un relevé a donné 4,35° vrais, 17,64° magnétiques et 14,07° indiqués. C’est un instant du simulateur, pas un étalonnage d’un compas réel. Ce banc vérifie la rose et son sens ; les erreurs en virage restent à évaluer.

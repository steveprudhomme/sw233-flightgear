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
        <author>Steve Prud'Homme et contributeurs SW233</author>
        <long-description>Prototype libre du Schweizer SGS 2-33 pour FlightGear. Licence GPL-3.0-only. Cockpit, commandes et masses configurables ; modele de vol experimental. Projet aux couleurs des Cadets de l'aviation royale du Canada : livree finale encore a realiser. Teste sous Windows avec FlightGear 2024.1.7 ; Linux non valide.</long-description>
        <aircraft-version>0.1.0-dev</aircraft-version>
        <minimum-fg-version>2024.1.7</minimum-fg-version>
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
        <menubar><default><menu n="100">
            <label>SW233</label><enabled type="bool">true</enabled>
            <item><label>Occupants et centrage</label><binding>
                <command>nasal</command><script>sw233_load.dialog.open();</script>
            </binding></item>
        </menu></default></menubar>
        <checklists include="Checklists/sw233.xml"/>
        <tags>
            <tag>glider</tag>
            <tag>unpowered</tag>
        </tags>
    </sim>
    <nasal><sw233_load><file>Nasal/occupants.nas</file></sw233_load></nasal>
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

<a name="altimetre"></a>

Les deux aiguilles lisent **instrumentation/altimeter/indicated-altitude-ft**. L’ancienne version lisait la position géométrique du planeur ; le calage de pression n’aurait donc pas modifié ses aiguilles. Le nouvel instrument dépend de la pression statique et du calage. La propriété et la syntaxe du bouton ont été vérifiées dans FlightGear 2024.1.7, notamment son fichier local *Aircraft/c172p/Models/Interior/Panel/Instruments/alt/alt.xml*.

À 500 ft, 500 × 0,36 = 180° : un demi-tour de la grande aiguille. Son pivot est au centre du cadran gauche.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>alt-centaines</object-name>
    <property>instrumentation/altimeter/indicated-altitude-ft</property>
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
    <property>instrumentation/altimeter/indicated-altitude-ft</property>
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

<a name="anemometre"></a>

**1. Mesure d’abord le dessin.** Ouvre la photo de C-FYLP de 690 × 517 pixels (nom commençant par *5d81c6bf* dans [l’inventaire](../references/inventaire.md)). Dans Paint, découpe le rectangle allant de (428,167) à (533,273), bord droit et bord bas exclus ; il fait 105 × 106 pixels. Affiche-le six fois plus grand, sans tourner l’image. Sur ce gabarit de 630 × 636 pixels, le pivot est vers **(328,327)**. À partir de là, 12 heures vaut 0°, 3 heures vaut 90° et les angles augmentent dans le sens des aiguilles d’une montre. Pour chaque nombre, pointe le **trait** qui lui correspond, pas le centre du chiffre.

| mph | Point (colonne, ligne) dans l’agrandissement | Angle retenu |
|---:|---:|---:|
| 20 | 420, 116 | 24° |
| 40 | 523, 200 | 57° |
| 60 | 552, 373 | 102° |
| 80 | 413, 521 | 156° |
| 100 | 238, 530 | 204° |
| 120 | 116, 411 | 248° |
| 140 | 125, 234 | 295° |
| 160 | 263, 122 | 342° |

Tu peux tracer les rayons sur du papier calque et utiliser un rapporteur. Le calcul équivalent est *atan2(colonne − 328, 327 − ligne)*, en degrés, ramené entre 0 et 360. Les points sont approximatifs : déplacer ta marque de deux pixels sur la petite photo change l’angle d’environ 3° ; l’agrandissement ne corrige pas la perspective. Le repos à **5° pour 0 mph** est une hypothèse visuelle ; entre le repos et le premier nombre, nous ne connaissons pas la courbe réelle.

**2. Change d’unité une seule fois.** FlightGear fournit maintenant la **vitesse indiquée** de son anémomètre, en nœuds. L’ancienne animation utilisait la vitesse calibrée du modèle de vol. La table ci-dessous attend des nœuds dans *ind* et rend des degrés dans *dep*. Pour préparer chaque ligne : nœuds = mph × 1609,344 / 1852. Pour prédire ce que tu vas lire, fais l’inverse : 60 kt × 1852 / 1609,344 ≈ **69,05 mph**. Cette valeur se trouve à 9,05/20 du trajet entre les traits de 60 et 80 mph ; l’angle attendu est donc 102 + (156 − 102) × 9,05/20 ≈ **126,4°**. Recopie la table une seule fois dans le modèle : la [recette de peinture](06-peinture.md#peinture-ias) la relira pour placer les traits.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>vitesse-mph</object-name>
    <property>instrumentation/airspeed-indicator/indicated-speed-kt</property>
    <interpolation>
      <entry><ind>0.000000</ind><dep>5</dep></entry>
      <entry><ind>17.379525</ind><dep>24</dep></entry>
      <entry><ind>34.759050</ind><dep>57</dep></entry>
      <entry><ind>52.138575</ind><dep>102</dep></entry>
      <entry><ind>69.518099</ind><dep>156</dep></entry>
      <entry><ind>86.897624</ind><dep>204</dep></entry>
      <entry><ind>104.277149</ind><dep>248</dep></entry>
      <entry><ind>121.656674</ind><dep>295</dep></entry>
      <entry><ind>139.036199</ind><dep>342</dep></entry>
    </interpolation>
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

<a name="variometre"></a>

**Lis l’unité avant le nombre.** Sur la photo C-FYLP de 690 × 517 pixels, le petit cadran en bas à droite porte « 100 FEET PER MIN ». Le 5 signifie donc **500 pieds par minute**, pas 5 000. Le zéro est à gauche ; la montée est dans la moitié haute (UP), la descente dans la moitié basse (DOWN). Cette seule photo ne permet pas de dire si l’instrument réel est compensé en énergie totale.

**Refais le pointage.** Dans la photo *5d81c6bf…*, découpe le rectangle de (526,223) à (633,332), bords droit et bas exclus. Agrandis cinq fois : 535 × 545 pixels. Le pivot est estimé en (260,294). Relève les grands traits, avec la même convention d’angle que pour l’anémomètre. La perspective et le flou peuvent déplacer le relevé de plusieurs degrés ; les angles ci-dessous ne sont pas des données d’étalonnage.

| Taux signé (ft/min) | Point (colonne, ligne) dans l’agrandissement | Angle retenu |
|---:|---:|---:|
| −2 000 | 442,322 | −261° |
| −1 500 | 352,433 | −213° |
| −1 000 | 208,458 | −162° |
| −500 | 91,386 | −119° |
| 0 | 71,292 | −90° |
| +500 | 118,188 | −53° |
| +1 000 | 245,110 | −5° |
| +1 500 | 401,155 | 45° |
| +2 000 | 451,278 | 85° |

**Branche l’indication, pas une conversion en double.** L’ancienne aiguille lisait directement la vitesse verticale de la trajectoire en ft/s. Nous utilisons maintenant *instrumentation/vertical-speed-indicator/indicated-speed-fpm*, déjà en ft/min. À +500, la table place l’aiguille en haut à gauche ; à −500, elle arrive en bas à gauche. Pour comparer à la trajectoire dans un relevé de vol, multiplie seulement *velocities/vertical-speed-fps* par 60 : −8,333 ft/s ≈ −500 ft/min. Notre instrument utilise le calcul de vitesse verticale de FlightGear ; nous n’ajoutons pas de compensation d’énergie totale.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
  <animation>
    <type>rotate</type>
    <object-name>vario</object-name>
    <property>instrumentation/vertical-speed-indicator/indicated-speed-fpm</property>
    <interpolation>
      <entry><ind>-2000</ind><dep>-261</dep></entry>
      <entry><ind>-1500</ind><dep>-213</dep></entry>
      <entry><ind>-1000</ind><dep>-162</dep></entry>
      <entry><ind>-500</ind><dep>-119</dep></entry>
      <entry><ind>0</ind><dep>-90</dep></entry>
      <entry><ind>500</ind><dep>-53</dep></entry>
      <entry><ind>1000</ind><dep>-5</dep></entry>
      <entry><ind>1500</ind><dep>45</dep></entry>
      <entry><ind>2000</ind><dep>85</dep></entry>
    </interpolation>
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
```

## Calage de l’altimètre

Ajoute ce dernier bloc avant la fermeture finale. Le bouton utilise *knob* et *setting-inhg*, avec un pas de 0,01 pouce de mercure. Les bornes 28–31 inHg et la rotation de −1600°/inHg sont des choix d’interface, pas des spécifications de C-FYLP. Le réglage exact reste lisible dans le navigateur de propriétés ; la fenêtre noire du cadran ne montre pas encore de valeur. L’infobulle est prévue dans le XML, mais les essais automatisés vérifient la propriété, pas le geste de souris.

<!-- atelier-fichier: src/SW233/Models/sw233-model.xml -->
```xml
<animation>
    <type>knob</type>
    <object-name>alt-calage</object-name>
    <property>instrumentation/altimeter/setting-inhg</property>
    <factor>-1600</factor>
    <center><x-m>0.888</x-m><y-m>-0.280</y-m><z-m>0.027</z-m></center>
    <axis><x>1</x><y>0</y><z>0</z></axis>
    <action>
      <binding>
        <command>property-adjust</command>
        <property>instrumentation/altimeter/setting-inhg</property>
        <factor>0.01</factor><min>28</min><max>31</max><wrap>false</wrap>
      </binding>
    </action>
    <hovered>
      <binding>
        <command>set-tooltip</command>
        <tooltip-id>sw233-alt-setting</tooltip-id>
        <label>Calage : %5.2f inHg</label>
        <property>instrumentation/altimeter/setting-inhg</property>
      </binding>
    </hovered>
  </animation>
  <animation>
    <type>rotate</type>
    <object-name>profondeur-1</object-name>
    <property>fdm/jsbsim/fcs/elevator-pos-rad</property>
    <factor>57.29577951308232</factor>
    <center><x-m>7.35</x-m><y-m>0</y-m><z-m>0.11</z-m></center>
    <axis><x>0</x><y>1</y><z>0</z></axis>
  </animation>
  <animation>
    <type>rotate</type>
    <object-name>profondeur1</object-name>
    <property>fdm/jsbsim/fcs/elevator-pos-rad</property>
    <factor>57.29577951308232</factor>
    <center><x-m>7.35</x-m><y-m>0</y-m><z-m>0.11</z-m></center>
    <axis><x>0</x><y>1</y><z>0</z></axis>
  </animation>
</PropertyList>
```

**Contrôle sans voler :** rapproche chaque `object-name` de la ligne `name` correspondante dans le fichier AC3D. Les aiguilles tournent dans le plan de la planche, autour de −x ; la ficelle autour de +z ; les panneaux autour de −y. Un nom faux peut laisser l’objet visible mais immobile. Une balise mal refermée peut empêcher de charger toute la fiche.

**Essai au banc, dans une session de simulation dédiée.** Ouvre le navigateur de propriétés du menu Débogage, puis *instrumentation → magnetic-compass*. Note la valeur de *serviceable*. Mets-la temporairement à faux pour empêcher l’instrument de réécrire ton entrée. Dans *indicated-heading-deg*, saisis successivement 90, 180, 270, 359, 0 et 1. Relis chaque valeur avant de regarder la fenêtre. Le trait reste au centre : E, S et W passent dessous ; puis N se décale légèrement d’une image à la suivante. Remets *serviceable* à sa valeur initiale avant de voler. Si ton entrée change toute seule, l’instrument fonctionne encore : tu observes sa réponse, pas un angle imposé.

![Captures natives : est, sud, ouest puis trois positions de la rose au passage du nord.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/compas-magnetique-04/SW233-compas-magnetique.png)

Les six vignettes sont des recadrages de FlightGear 2024.1.7 à CYJN. Pour les retrouver, reprends la caméra de face de la fiche 6, avec une inclinaison de −26° et un champ de 17°. Les valeurs affichées au-dessus des images sont les entrées d’essai. En fonctionnement normal, un relevé a donné 4,35° vrais, 17,64° magnétiques et 14,07° indiqués. C’est un instant du simulateur, pas un étalonnage d’un compas réel. Ce banc vérifie la rose et son sens ; les erreurs en virage restent à évaluer.


**Profondeur :** les deux objets suivent la déflexion effective JSBSim, en radians. Le facteur 180/pi convertit en degrés ; autour de +y, une déflexion positive abaisse le bord de fuite. Charnière (7,35 ; 0 ; 0,11) choisie pour cette maquette. [Banc et limites](10-profondeur.md).

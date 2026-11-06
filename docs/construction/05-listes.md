# 5 · Fabriquer les cartes de vérification

Regarde les quatre petites cartes sur les photos du poste avant : elles correspondent à des moments différents. Leur présence [V] nous suggère quatre listes. Le manuel du programme de 2017, PDF p. 213, explique comment reprendre une vérification interrompue. Les textes ci-dessous sont **notre rédaction pour le simulateur**, pas la transcription d’une procédure officielle.

**Fichier à écrire :** `src/SW233/Checklists/sw233.xml`. Colle les blocs de ce fichier dans l’ordre, sans retirer les espaces du début des lignes.

## A · Avant le départ

Fais une boîte checklist n=0. Pour chaque ligne, name est ce que tu cherches ; value est ce que tu veux pouvoir constater. Exemple : plutôt que « instruments OK », demande si tu sais quel cadran utilise mph et lequel utilise ft. Les tirets, accents et espaces sont autorisés dans les titres : le fichier est en UTF-8.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Original simulation checklists. No automatic actions; tow is not implemented. -->
<PropertyList>
    <checklist n="0">
        <title>SW233 · Avant départ (simulation)</title>
        <item><name>Chargement</name><value>Scénario et centrage vérifiés</value></item>
        <item><name>Commandes</name><value>Libres ; sens vérifié</value></item>
        <item><name>Instruments</name><value>mph, ft et milliers de ft/min identifiés</value></item>
        <item><name>Aérofreins et trim</name><value>Course et position vérifiées</value></item>
        <item><name>Harnais, verrière et porte</name><value>Revue visuelle simulée</value></item>
    </checklist>
```

## B · Avant le largage

Ajoute une deuxième carte dans la même racine. Dans cette version, aucun câble n’est simulé. Marque donc la répétition comme verbale au lieu de créer une action imaginaire.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
    <checklist n="1">
        <title>SW233 · Avant largage (répétition simulée)</title>
        <item><name>Zone et trafic</name><value>Repérés</value></item>
        <item><name>Altitude et position</name><value>Vérifiées dans le scénario</value></item>
        <item><name>Largage</name><value>Revue verbale ; câble non simulé</value></item>
    </checklist>
```

## C · Avant l’atterrissage

Sépare l’observation du vent et du trafic, la lecture de vitesse et la disponibilité des aérofreins. On ne déduit pas une vitesse d’approche d’une photographie de plaquette.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
    <checklist n="2">
        <title>SW233 · Avant atterrissage (simulation)</title>
        <item><name>Vent, trafic et piste</name><value>Identifiés</value></item>
        <item><name>Vitesse</name><value>Lue en mph ; adaptée au scénario</value></item>
        <item><name>Aérofreins et trim</name><value>Disponibilité vérifiée</value></item>
        <item><name>Harnais et verrière</name><value>Revue visuelle simulée</value></item>
    </checklist>
```

## D · Avant un exercice

Écris les limites du modèle : une case cochée ne valide pas une vrille. Termine les deux dernières boîtes, checklist puis PropertyList. Les numéros vont de 0 à 3 sans répétition.

<!-- atelier-fichier: src/SW233/Checklists/sw233.xml -->
```xml
    <checklist n="3">
        <title>SW233 · Avant exercice de décrochage (simulation)</title>
        <item><name>Altitude, terrain et trafic</name><value>Marges revues</value></item>
        <item><name>Harnais, verrière et objets</name><value>Revue visuelle simulée</value></item>
        <item><name>Domaine de vol</name><value>Vrille non validée ; pas de démonstration de vrille</value></item>
    </checklist>
</PropertyList>
```

**Essai :** quand le paquet sera chargé, ouvre **Aide → Aircraft Checklists**. Tu dois trouver les quatre titres et respectivement **5, 3, 4 et 3 lignes**. Si le menu est vide, vérifie le C majuscule de *Checklists* et le chemin d’inclusion dans la fiche set. Si tu coches une ligne, aucune gouverne ne doit se déplacer.

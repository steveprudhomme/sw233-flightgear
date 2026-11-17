# Radio COM1 : références et limites

La photo C-FYLP ne suffit pas à identifier avec certitude toutes les commandes de sa radio. Une inscription FSG 71M sur une autre photo ne prouve pas que C-FYLP possède la même version. La [notice Dittel FSG 70/FSG 71M repérée](https://www.cumulus-soaring.com/dittel/FSG%2070-FSG71M%20Operation%20and%20Installation%20Manual.pdf) reste une piste ; nous ne lui attribuons pas automatiquement notre cockpit.

La propriété active `instrumentation/comm[0]/frequencies/selected-mhz` figure dans les exemples installés FlightGear `Aircraft/Instruments-3d/kx165/kx165-1.xml` et `Aircraft/Instruments-3d/ar-3201/ar-3201.xml`. Le second illustre des pas de 1 MHz et 0,025 MHz. Notre module est original ; aucun script, modèle ou texture de ces radios n'est copié. Voir aussi la [référence des propriétés COMM](https://wiki.flightgear.org/Aircraft_properties_reference/Instrumentation/COMM).

Le périmètre choisi est une commande générique sur grille 25 kHz, de 118.000 à 136.975 MHz. Une valeur externe hors grille reste affichée mais nos boutons refusent de la modifier. Aucun canal 8,33 kHz n'est converti silencieusement.

Choix simplifiés : affichage à trois décimales, réglage direct de COM1 active, boutons 1 MHz et 25 kHz, butées sans bouclage. Pas de volume, marche/arrêt, mémoire ni échange actif/attente. L'affichage n'est pas conditionné à une alimentation électrique ; la pastille rouge est décorative, pas un voyant TX.

Les treize cas natifs et huit clics de VIS-01m valident le réglage et l'affichage dans FlightGear 2024.1.7. Ils ne valident ni réception audio, ni propagation, ni FGCom, ni émission réseau.

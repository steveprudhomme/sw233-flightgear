# Atlas — toutes les pièces du maillage

Cet atlas complète la fiche 2. Chaque objet nommé de sw233.ac possède une image : aucune pièce n’est choisie seulement parce qu’elle est belle. Les dimensions x/y/z sont calculées à partir des sommets du modèle ; elles ne prouvent pas la conformité au véritable SGS 2-33.

Chaque image donne trois projections sans perspective ni textures. Les vues sont ajustées séparément. Une pièce plate peut apparaître comme un trait dans une vue. Une rose de compas contient plusieurs facettes dans un seul objet : ces facettes restent visibles sur son illustration.

Pour travailler hors connexion, [télécharge l’atlas complet](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/atlas-pieces.zip), extrais-le puis ouvre index.html. Pour le refaire depuis la racine du dépôt :

```powershell
python -m tools.parts_atlas build/mon-atlas
```

L’outil lit les faces, convertit les coordonnées AC3D (x,z,-y) vers le repère du cahier (x,y,z), calcule les bornes, projette puis dessine. Les illustrations ne sont pas des photos de FlightGear. Les [captures natives avant/après](14-enveloppe.md) servent à juger le rendu réel.

## 1. fuselage

87 faces ; étendue x × y × z : **7.6100 × 0.9400 × 0.7500 m**.

![fuselage : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-01.png)

## 2. verriere

33 faces ; étendue x × y × z : **2.6600 × 0.8800 × 0.6500 m**.

![verriere : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-02.png)

## 3. bordures-cockpit

80 faces ; étendue x × y × z : **2.6688 × 0.9160 × 0.0860 m**.

![bordures-cockpit : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-03.png)

## 4. raccord-arriere

9 faces ; étendue x × y × z : **1.0300 × 0.6800 × 0.6000 m**.

![raccord-arriere : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-04.png)

## 5. arceaux

320 faces ; étendue x × y × z : **2.6920 × 0.9117 × 0.6790 m**.

![arceaux : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-05.png)

## 6. aile-1

22 faces ; étendue x × y × z : **1.5700 × 7.7724 × 0.3144 m**.

![aile-1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-06.png)

## 7. hauban-1

8 faces ; étendue x × y × z : **0.2059 × 3.3165 × 1.2962 m**.

![hauban-1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-07.png)

## 8. aerofrein-1

1 faces ; étendue x × y × z : **0.1300 × 1.1500 × 0.0200 m**.

![aerofrein-1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-08.png)

## 9. empennage-1

1 faces ; étendue x × y × z : **0.5000 × 1.9300 × 0.0000 m**.

![empennage-1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-09.png)

## 10. profondeur-1

1 faces ; étendue x × y × z : **0.4400 × 1.9300 × 0.0000 m**.

![profondeur-1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-10.png)

## 11. aile1

22 faces ; étendue x × y × z : **1.5700 × 7.7724 × 0.3144 m**.

![aile1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-11.png)

## 12. hauban1

8 faces ; étendue x × y × z : **0.2059 × 3.3165 × 1.2962 m**.

![hauban1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-12.png)

## 13. aerofrein1

1 faces ; étendue x × y × z : **0.1300 × 1.1500 × 0.0200 m**.

![aerofrein1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-13.png)

## 14. empennage1

1 faces ; étendue x × y × z : **0.5000 × 1.9300 × 0.0000 m**.

![empennage1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-14.png)

## 15. profondeur1

1 faces ; étendue x × y × z : **0.4400 × 1.9300 × 0.0000 m**.

![profondeur1 : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-15.png)

## 16. derive

1 faces ; étendue x × y × z : **1.3486 × 0.0000 × 1.3800 m**.

![derive : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-16.png)

## 17. roue

22 faces ; étendue x × y × z : **0.4900 × 0.1500 × 0.4900 m**.

![roue : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-17.png)

## 18. roulette

22 faces ; étendue x × y × z : **0.1680 × 0.1500 × 0.1680 m**.

![roulette : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-18.png)

## 19. patin

8 faces ; étendue x × y × z : **1.5881 × 0.0760 × 0.2456 m**.

![patin : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-19.png)

## 20. sieges

2 faces ; étendue x × y × z : **1.0000 × 0.5400 × 0.3500 m**.

![sieges : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-20.png)

## 21. manche

8 faces ; étendue x × y × z : **0.1620 × 0.0440 × 0.3981 m**.

![manche : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-21.png)

## 22. poignee-frein

8 faces ; étendue x × y × z : **0.2591 × 0.0380 × 0.1728 m**.

![poignee-frein : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-22.png)

## 23. tableau

1 faces ; étendue x × y × z : **0.0000 × 0.7800 × 0.3550 m**.

![tableau : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-23.png)

## 24. alt-fond

1 faces ; étendue x × y × z : **0.0000 × 0.1660 × 0.1660 m**.

![alt-fond : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-24.png)

## 25. alt-centaines

1 faces ; étendue x × y × z : **0.0000 × 0.0028 × 0.0870 m**.

![alt-centaines : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-25.png)

## 26. alt-milliers

2 faces ; étendue x × y × z : **0.0005 × 0.0080 × 0.0540 m**.

![alt-milliers : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-26.png)

## 27. alt-calage

26 faces ; étendue x × y × z : **0.0195 × 0.0240 × 0.0240 m**.

![alt-calage : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-27.png)

## 28. ias-fond

1 faces ; étendue x × y × z : **0.0000 × 0.1500 × 0.1500 m**.

![ias-fond : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-28.png)

## 29. vitesse-mph

2 faces ; étendue x × y × z : **0.0005 × 0.0080 × 0.0810 m**.

![vitesse-mph : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-29.png)

## 30. vsi-fond

1 faces ; étendue x × y × z : **0.0000 × 0.1260 × 0.1260 m**.

![vsi-fond : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-30.png)

## 31. vario

2 faces ; étendue x × y × z : **0.0005 × 0.0070 × 0.0700 m**.

![vario : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-31.png)

## 32. embase-pitot

8 faces ; étendue x × y × z : **0.0682 × 0.0440 × 0.0874 m**.

![embase-pitot : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-32.png)

## 33. tube-pitot

16 faces ; étendue x × y × z : **0.4423 × 0.0220 × 0.3303 m**.

![tube-pitot : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-33.png)

## 34. attache-laine

8 faces ; étendue x × y × z : **0.0309 × 0.0280 × 0.0316 m**.

![attache-laine : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-34.png)

## 35. fil-de-laine

32 faces ; étendue x × y × z : **0.2924 × 0.0096 × 0.0973 m**.

![fil-de-laine : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-35.png)

## 36. tige-largage

8 faces ; étendue x × y × z : **0.0490 × 0.0180 × 0.0180 m**.

![tige-largage : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-36.png)

## 37. boule-largage

62 faces ; étendue x × y × z : **0.0610 × 0.0660 × 0.0660 m**.

![boule-largage : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-37.png)

## 38. compas-cadre

32 faces ; étendue x × y × z : **0.0245 × 0.0660 × 0.0620 m**.

![compas-cadre : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-38.png)

## 39. compas-fond

1 faces ; étendue x × y × z : **0.0000 × 0.0490 × 0.0280 m**.

![compas-fond : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-39.png)

## 40. compas-repere

1 faces ; étendue x × y × z : **0.0000 × 0.0018 × 0.0080 m**.

![compas-repere : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-40.png)

## 41. compas-vis

4 faces ; étendue x × y × z : **0.0000 × 0.0524 × 0.0484 m**.

![compas-vis : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-41.png)

## 42. compas-vitre

1 faces ; étendue x × y × z : **0.0000 × 0.0490 × 0.0280 m**.

![compas-vitre : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-42.png)

## 43. compas-rose

334 faces ; étendue x × y × z : **0.0989 × 0.0989 × 0.0220 m**.

![compas-rose : profil, dessus, face](https://github.com/steveprudhomme/sw233-flightgear/releases/download/enveloppe-16/piece-43.png)

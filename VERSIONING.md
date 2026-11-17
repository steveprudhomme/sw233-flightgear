# Versionnage du projet

Le projet applique [SemVer 2.0.0](https://semver.org/lang/fr/) depuis **0.1.0-alpha.1**.
`VERSION` contient le numero de reference, sans prefixe v. Le tag GitHub ajoute
ce prefixe : `v0.1.0-alpha.1`. Les anciens tags restent inchanges.

## Lire le numero

Imagine trois compteurs : **MAJEUR.MINEUR.CORRECTIF**.
Apres la version 1.0.0, une incompatibilite augmente MAJEUR ; une fonction
compatible augmente MINEUR ; une correction compatible augmente CORRECTIF.
Les compteurs suivants repartent a zero. Une version publiee ne se remplace pas.

Le modele est encore experimental : `0` le signale, et `alpha.1` indique le
premier essai publie de la future 0.1.0. Le prochain essai de ce meme objectif
sera alpha.2, puis eventuellement beta.1 et rc.1 avant 0.1.0.
Avant 1.0.0, notre convention est de reserver un changement mineur (0.2.0,
par exemple) aux fonctions nouvelles ou incompatibilites, et un correctif
(0.1.1) aux seules corrections compatibles. SemVer ne garantit pas la stabilite
pendant cette phase initiale ; chaque incompatibilite doit etre expliquee.

## Contrat public suivi

Le contrat comprend l'identifiant `sw233`, le chemin `Aircraft/SW233`, les
options documentees du lanceur, les commandes et proprietes exposees dans
le tutoriel, ainsi que les exigences d'installation documentees. Les details
internes du generateur ne sont pas une interface stable. Le numero ne certifie
ni la fidelite du vol ni l'aptitude a une instruction reelle.
La version 1.0.0 exigera un contrat stabilise et les validations correspondantes.

## Publier, pas a pas

1. Choisir le numero selon les changements ; preciser le contenu dans CHANGELOG.
2. Modifier VERSION, aircraft-version dans sw233-set.xml et sa recette au chapitre04.
3. Executer les tests et reconstruire le tutoriel. Le paquet refuse une divergence.
4. Faire le commit, construire le paquet et verifier son manifeste et ses images.
5. Publier le tag v suivi du numero, avec le paquet sw233-NUMERO.zip.
6. Marquer alpha, beta et rc comme preversions dans GitHub. Ne jamais remplacer
   un fichier deja publie ; utiliser un nouveau numero pour toute correction.

Les identifiants VIS, BC43 et les numeros d'ateliers servent a retrouver le
travail : ce ne sont pas des versions du logiciel.

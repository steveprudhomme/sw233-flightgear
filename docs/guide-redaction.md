# Écrire une documentation facile à utiliser

Depuis le 17 novembre 2026, appliquer ce guide à toute nouvelle documentation.
Appliquer aussi ces règles aux passages modifiés d'un document existant.
Le tutoriel vise un enfant de 10 ans qui découvre le projet.
Les autres documents nomment leur public et les connaissances nécessaires.

## Choisir les références

| Référence | Usage dans le projet | Limite à respecter |
|---|---|---|
| [WCAG 2.2 en français](https://www.w3.org/Translations/WCAG22-fr-20260922/) | Structurer les pages et rendre les contenus accessibles | Vérifier aussi la page publiée, pas seulement le fichier Markdown |
| [Explication du critère 3.1.5](https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html) | Fournir une explication simple pour un texte complexe | Critère de niveau AAA ; son seuil est le premier cycle du secondaire, pas 10 ans |
| [CAN-ASC-3.1:2025](https://accessibilite.canada.ca/normes-et-guides-techniques/base-de-donnees-des-normes-et-des-guides-techniques/can-asc-312025-langage-clair?mode=full-html) | Organiser la rédaction et l'essai avec le public | Une grille remplie ne prouve pas à elle seule la conformité |
| [Français au primaire au Québec](https://www.quebec.ca/education/prescolaire-primaire-et-secondaire/programmes-formations-evaluation/programme-formation-ecole-quebecoise/primaire/francais-langue-enseignement) | Choisir des explications adaptées aux apprentissages du primaire | L'âge ne garantit pas un niveau de lecture identique |
| [Français au secondaire au Québec](https://www.quebec.ca/education/prescolaire-primaire-et-secondaire/programmes-formations-evaluation/programme-formation-ecole-quebecoise/secondaire/francais-langue-enseignement) | Préparer les explications techniques complémentaires | Ne pas imposer ce niveau au parcours débutant |
| [Simple French](https://github.com/quantumsheep/simple-french) | Stabiliser le vocabulaire et simplifier les consignes techniques | Projet indépendant sous licence MIT ; ce n'est pas le guide officiel du GIFAS |

Consulter les programmes, les progressions et les cadres d'évaluation du Québec.
L'[inventaire des ressources](references/ressources-redaction.md) donne les 14 liens et leurs empreintes.
Les programmes actualisés sont disponibles pour appropriation en 2026-2027.
Leur mise en œuvre obligatoire commence à la rentrée 2027-2028.
Distinguer ces éditions des programmes antérieurs dans chaque référence.

## Préparer le travail

1. Nommer le lecteur : débutant, contributeur ou personne qui vérifie le modèle.
2. Écrire ce que le lecteur pourra faire à la fin.
3. Donner les outils, les fichiers et les connaissances nécessaires.
4. Repérer les mots nouveaux et les expliquer avant leur première utilisation.
5. Prévoir une image et un résultat visible pour chaque manipulation importante.

Selon CAN-ASC-3.1:2025, la communication doit répondre aux besoins du public.
Elle doit l'aider à trouver, comprendre et utiliser l'information.
Prévoir une relecture, puis un essai avec des lecteurs du public visé.
Noter les difficultés et corriger le document après cet essai.
Consulter notamment les articles 12, 13 et 14 pour la structure, la formulation et la présentation.

## Rédiger les étapes

Pour les procédures, appliquer le profil technique de Simple French :

- Employer l'infinitif pour les actions : « Ouvrir le fichier ».
- Employer « vous » dans les explications adressées au lecteur.
- Donner une action principale par étape, dans l'ordre réel du travail.
- Viser au plus 20 mots par phrase de consigne et 25 par phrase descriptive.
- Employer un même mot pour une même pièce ou une même action.
- Préférer la voix active et les verbes simples.
- Conserver les accents, y compris sur les majuscules.
- Éviter les tournures indirectes, les anglicismes inutiles et les suites de noms.

Ces limites de longueur viennent du profil Simple French, pas des WCAG.
Une phrase courte peut rester difficile : vérifier aussi son sens avec un lecteur.
Ne pas supprimer une information utile pour réduire le nombre de mots.

Pour les dates d'essai et les faits passés, conserver des temps qui décrivent les faits avec exactitude.
Pour une hypothèse, écrire « estimation » ou « à vérifier » et donner la raison.
Cette adaptation du projet évite de transformer une incertitude en certitude.
Le profil technique ne sert pas à restreindre la grammaire enseignée au Québec.

Dans le texte, écrire les unités : « 0,30 m ».
Dans le code, conserver la syntaxe requise : `0.30`.
Ne pas traduire les chemins, les noms de propriétés ou les commandes.
Expliquer les acronymes sans modifier les mots-checks officiels des Cadets.

## Construire une fiche de tâche

Utiliser cette structure pour chaque nouvelle manipulation du tutoriel :

1. **But** : expliquer le résultat en une phrase.
2. **Avant de commencer** : nommer les outils et les fichiers nécessaires.
3. **Comprendre** : expliquer les mots, les mesures et le choix effectué.
4. **Agir** : donner les actions numérotées et le texte exact à saisir.
5. **Voir** : placer une image près de l'action qu'elle montre.
6. **Vérifier** : décrire ce qui doit apparaître à l'écran.
7. **Corriger** : expliquer quoi faire si le résultat diffère.
8. **Retrouver la preuve** : citer la référence, sa page et les limites du relevé.

Pour une mesure sur photo, noter les deux repères, la méthode et l'incertitude.
Une photo en perspective ne donne pas directement une longueur réelle.
Présenter les détails avancés après le parcours débutant.
Garder une explication simple disponible pour les passages complexes, conformément à l'objectif du critère 3.1.5.

## Préparer les images et la page

- Garder une hiérarchie logique de titres.
- Donner un texte alternatif aux images utiles ; expliquer leur information essentielle dans le texte.
- Pour une image décorative, utiliser un texte alternatif vide.
- Ajouter une légende qui nomme la pièce, la vue et ce qu'il faut observer.
- Ne pas transmettre une information par la couleur seule ; ajouter un mot ou un repère.
- Fournir les commandes sous forme de texte copiable, même si une capture les montre.
- Utiliser des liens explicites et des tableaux simples avec des en-têtes.
- Indiquer la langue de la page publiée et celle des passages dans une autre langue.
- Vérifier le contraste, le zoom, la lecture sur petit écran et la navigation au clavier.
- Pour une vidéo, prévoir les sous-titres et les équivalents textuels requis par son contenu.

Ces contrôles couvrent notamment les critères 1.1.1, 1.3.1, 1.4.1, 1.4.3,
1.4.4, 1.4.10, 2.1.1, 2.4.4, 2.4.6, 3.1.1 et 3.1.2.
Ils ne remplacent pas un audit complet des WCAG 2.2.
Ne pas annoncer une conformité AA ou AAA sur la seule base de ce guide.

## Exemple : observer la nouvelle coque

**But :** reconnaître le nez, les flancs et le raccord derrière la verrière.

1. Ouvrir la [comparaison du lot43](construction/25-finitions-avant.md).
2. Observer la vue de profil ci-dessous.
3. Repérer le nez à droite, puis le raccord jaune derrière la verrière.

![Vue de profil dans FlightGear : nez arrondi à droite et raccord jaune derrière la verrière.](https://github.com/steveprudhomme/sw233-flightgear/releases/download/v0.1.0-alpha.1/apres-nez-profil.png)

*Figure 1 — Capture FlightGear de la préversion 0.1.0-alpha.1. Les formes restent estimées.*

**Résultat attendu :** distinguer ces pièces sans utiliser leur couleur comme seul indice.
Si une pièce reste difficile à reconnaître, consulter les vues de détail du même atelier.
Cette fiche sert d'exemple de rédaction ; elle ne constitue pas un nouvel essai du simulateur.

## Relire avant de publier

- [ ] Le but, le public et les prérequis sont explicites.
- [ ] Chaque étape indique l'action et le résultat attendu.
- [ ] Les mots nouveaux sont expliqués ; les termes restent cohérents.
- [ ] Les références indiquent l'édition et les passages utilisés.
- [ ] Les estimations se distinguent des mesures et des résultats d'essai.
- [ ] Les images, légendes et textes alternatifs donnent la même information utile.
- [ ] Les liens et les commandes sont vérifiés.
- [ ] La page publiée passe les contrôles d'accessibilité applicables.
- [ ] Un lecteur débutant essaie la tâche et explique le résultat avec ses mots.
- [ ] Les difficultés, les corrections et les essais encore attendus sont consignés.

Pour chaque essai, noter la page, la date, la tâche et les obstacles observés.
Noter « non testé » lorsqu'un contrôle reste à faire.
Un score automatique de lisibilité ne prouve ni la compréhension ni la conformité.
Ne pas attribuer une note scolaire au lecteur : évaluer la documentation.

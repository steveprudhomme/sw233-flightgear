# Recherche de livrée C-FYLP — 17 novembre 2026

## Conclusion et niveau de preuve

La livrée livrée ici est **provisoire**, originale et modifiable. Elle n'est pas présentée comme la peinture actuelle exacte de C-FYLP. Le jaune, le bleu, la forme des bandes, leur hauteur, les nuances et la police sont des choix de dessin pour cette maquette. L'immatriculation demandée est écrite normalement sur les deux flancs. Aucun insigne officiel n'est fabriqué.

## Journal de recherche

Requêtes effectuées : `"C-FYLP" glider photo`, `"C-FYLP" Schweizer`, `"C-FYLP" "2025"`, `"C-FYLP" "2024" photo`, `"C-FYLP" "2026" photo` et recherche d'images `"C-FYLP"`. Les résultats d'images proposés représentaient notamment C-FFYL ou CF-LEP : ces appareils différents ont été écartés. Une date de collecte en 2026 ne date pas la prise de vue.

| Source consultée | Ce qu'elle permet de dire | Limite |
| --- | --- | --- |
| [Défense nationale, rapport annuel sécurité des vols 2011](https://publications.gc.ca/collections/collection_2012/forces/D3-22-2011-eng.pdf), section 1.5.2.6 | Le résultat indexé associe C-FYLP à l'événement du 18 juin 2011 à Markham et décrit une illustration de planeur jaune et bleu. | Description indexée, pas inspection visuelle réussie de la page. Une illustration d'article ne prouve pas automatiquement que l'appareil photographié est celui du titre. |
| [Défense nationale, Flight Comment, no 3 de 2012](https://publications.gc.ca/collections/collection_2012/dn-nd/DC2-2-2012-3-eng.pdf), page imprimée 40 | L'article nomme C-FYLP et le 18 juin 2011. L'extraction décrit un planeur jaune à bandes bleues. Crédit imprimé : MCpl Bradley Denoon. | Le texte a été consulté, mais les captures PDF ont échoué et le téléchargement a retourné du HTML. Ni tracé précis, ni identité visuelle, ni état actuel validés. [Copie Skybrary](https://skybrary.aero/sites/default/files/bookshelf/2044.pdf) également repérée ; capture indisponible. |
| [Site du 155 Borden Gray GC](https://155aircadets.com/) | La page contient une légende nommant C-FYLP en finale à CFB North Bay et attribue la photo au capitaine Peter M. Petainen. | Pas de date de prise de vue établie ; la légende consultée ne permet pas de mesurer les couleurs, les bandes ou les marquages. |
| [Air Cadet League, liste d'assurance 2020–2021](https://aircadetleague.com/wp-content/uploads/2021/04/1.-Commercial-Aviation.-1-Apr-20-1-Apr-21.pdf), page 2 | Liste C-FYLP comme Schweizer 2-33A de 1969. | Document d'identification historique, aucune preuve de peinture. |

Le registre agrégé AviatorDB et CASPIR sont aussi apparus dans les résultats ; ils ne servent pas de référence graphique. Aucune photographie extérieure récente, datée et suffisamment lisible de cet appareil précis n'a été validée pendant cette recherche. Cela ne signifie pas qu'il n'en existe aucune.

## Décision de réalisation

La base reste jaune et reçoit un dessous bleu, un filet bleu et C-FYLP sur chacun des deux flancs. Ces tracés sont explicitement artistiques. La dérive et les ailes conservent leurs matériaux existants : aucune lettre, cocarde ou position de marquage supplémentaire n'est déduite d'un autre planeur. Les fichiers PNG contiennent uniquement des formes et du texte créés par notre programme. Aucune photo tierce n'entre dans le paquet, ni dans les sources du projet.

Pour remplacer le provisoire, il faut des vues datées gauche, droite, dessus, dessous et dérive de C-FYLP, avec autorisation si une photographie doit être redistribuée. Une règle ou une cote connue aiderait à mesurer les bandes. La géométrie actuelle peut alors conserver ses coordonnées UV tandis que le dessin change.

## Vérification locale

Génération réussie dans `D:/SW233-work/visuals-39/livery-agent`. Le maillage source reste inchangé. Les 87 faces du fuselage sont reproduites : 358 coins et 99 positions distinctes. Les normales latérales sont orientées vers l'extérieur. Le déplacement de chaque position est 1,2 mm ; sa projection sur les normales des faces incidentes varie de 0,591 à 1,200 mm, donc toutes restent à l'extérieur de leur face de départ. Les UV restent entre 0 et 1. Les projections originales `proof-left.png` et `proof-right.png`, examinées visuellement, montrent les six lettres/caractères de C-FYLP dans le bon sens de chaque côté. Ce sont des schémas de contrôle, pas des captures FlightGear. L'absence de scintillement à toutes distances doit encore être contrôlée dans FlightGear lors de l'intégration.

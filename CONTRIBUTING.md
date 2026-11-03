# Contribuer

Merci de discuter les changements importants dans une Issue avant de coder.
Créer une branche courte, proposer une pull request et expliquer le problème,
le comportement obtenu et les vérifications effectuées. Français et anglais
sont acceptés ; les échanges doivent respecter CODE_OF_CONDUCT.md.

## Qualité et provenance

- XML et Python : quatre espaces ; YAML : deux espaces ; UTF-8, fins de ligne LF.
- Conserver les unités et conventions de signe explicites.
- Chaque nouveau coefficient doit avoir une source, un statut (mesuré, dérivé,
  historique ou hypothèse) et une justification dans docs/sources.md.
- Ne pas copier de code, texture ou modèle dont la licence est inconnue.
- Ne pas ajouter build/, archives, journaux ou environnements Python.
- Ajouter des tests de comportement pour une modification du FDM et actualiser
  CHANGELOG.md. Un test de chargement n'établit pas la fidélité de l'aéronef.
- Mentionner l'assistance IA et vérifier les résultats avant soumission.

## Vérifications locales

```sh
python -m pip install -r requirements-dev.txt
python tools/check.py
python -m ruff check .
python -m unittest discover -s tests -v
```

## Commits et DCO

Des commits atomiques : `docs:`, `feat:`, `fix:` ou `test:` suivis d'une description.
Ne mettre `Fixes #123` que si le ticket existe et est effectivement résolu.
Lire le [Developer Certificate of Origin 1.1](https://developercertificate.org/).
Signer chaque commit avec son identité réelle ou une identité de contribution
constante et une adresse vérifiable (l'adresse GitHub noreply est acceptée) :

```sh
git commit -s -m "fix: corriger le signe de la commande de direction"
```

`Signed-off-by:` est une attestation DCO, pas une signature cryptographique.
Ne signer que des contributions que l'on est autorisé à soumettre sous MIT.
La CI vérifie le trailer de chaque commit proposé ; le mainteneur examine
également la provenance. Éviter le squash qui effacerait les attestations.

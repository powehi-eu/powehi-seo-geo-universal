> **Langue :** Français | [English](UPSTREAM.md)

# Synchronisation en amont

Powehi Universal SEO est maintenu par Powehi à
`powehi-eu/powehi-seo-geo-universal`. Il intègre des travaux du projet upstream
`AgriciDaniel/claude-seo`, distribués sous licence MIT, et préserve les droits
d’auteur ainsi que les attributions des contributeurs.

Le workflow planifié compare la dernière release upstream publiée avec l’état
enregistré dans `data/upstream-release.json`. Lorsqu’un nouveau tag apparaît, il
applique le delta entre les deux releases aux chemins importables dans la branche
révisable `sync/upstream-release`, puis ouvre ou actualise une pull request. Il ne
publie jamais directement le contenu upstream sur `main` et n’importe jamais son
historique Git.

L’identité Powehi, la documentation, les manifestes, les installateurs, les
workflows et l’orchestrateur renommé sont exclus de l’application automatique.
La pull request répertorie tous les chemins modifiés upstream afin que les
changements protégés soient adaptés explicitement, sans régression de marque.

## Surfaces appartenant à Powehi

Les surfaces suivantes conservent l'identité du produit Powehi pendant le conflit
résolution:

- `.codex-plugin/` et `.claude-plugin/`;
- `README.md`, `AGENTS.md`, `CLAUDE.md` et `docs/`;
- `pyproject.toml`, `CITATION.cff`, installateurs, désinstallateurs et `bin/`;
- Modèles GitHub, métadonnées de publication et flux de travail;
- orchestration d'audit, découverte de capacités, marquage de rapports et artefact
les contrats.

Fonctionnalité en amont, corrections de sécurité, tests, compétences, scripts et références
Les documents peuvent être fusionnés après examen. L'attribution historique reste
`LICENSE`, `CONTRIBUTORS.md`, `CHANGELOG.md`, fichiers de licence spécifiques aux compétences, et
métadonnées `original_author`.

## Validation requise après fusion

```bash
python -m pytest tests/test_powehi_identity.py -q
python -m pytest tests/test_manifest_consistency.py -q
python scripts/portability_check.py
python -m pytest tests -q
```

## Synchronisation rapide de FLOW

Powehi expédie des adaptations spécialisées de la bibliothèque rapide FLOW. En amont
source reste le dépôt FLOW de Daniel Agrici sous CC BY 4.0, et chaque adaptation
prompt conserve cette attribution.

`scripts/sync_flow.py` télécharge un ensemble complet de candidats avant d'écrire. Les
candidat doit satisfaire le contrat rapide Powehi: 41 fichiers attendus, étape stable
comptes, métadonnées et sections complètes, identifiants rapides uniques et uniques
les organes opérationnels. Un candidat rejeté laisse tous les fichiers locaux et le fichier de verrouillage
inchangé.

Après une modification rapide intentionnelle, régénérer l'index dérivé et verrouiller avec:

```bash
python scripts/prompt_integrity.py --refresh-derived
python scripts/repository_integrity.py --strict --json
```

Les miroirs d'extension autorisés et les exceptions exactes au double contenu sont déclarés
dans `data/repository-integrity.json`. Les différences de miroirs épinglés nécessitent une raison,
un propriétaire, une source explicite et des hachages cibles. Ne mettez pas à jour ces hashes sans
examiner la différence réelle.

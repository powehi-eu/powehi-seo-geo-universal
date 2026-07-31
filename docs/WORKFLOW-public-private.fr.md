> **Langue :** Français | [English](WORKFLOW-public-private.md)

# Déroulement du dépôt

Powehi Universal SEO est publié depuis:

```text
https://github.com/powehi-eu/powehi-seo-geo-universal
```

La télécommande locale `origin` est la destination de publication Powehi. Les
La télécommande `upstream` est le projet source homologué MIT documenté dans
`docs/UPSTREAM.md`.

## Développement

Créer des branches revisibles à partir de `main`, exécuter la suite complète de validation, et ouvrir
une requête de tirage contre le dépôt Powehi. Ne pas pousser inachevé en amont
synchronisation directement vers `main`.

```bash
git switch -c codex/<topic>
python -m pytest tests -q
python scripts/portability_check.py
git push -u origin codex/<topic>
```

## Sortie

Les versions de publication doivent correspondre à :

- `.claude-plugin/plugin.json`;
- `.codex-plugin/plugin.json`;
- `.claude-plugin/marketplace.json`;
- `pyproject.toml`;
- `CITATION.cff`;
- chaque `SKILL.md` entretenu;
- balises d'installation par défaut.

Créer la version seulement après CI, les vérifications d'installation, la validation du plugin, et le
Powehi carte d'identité.

```bash
git tag -a vX.Y.Z -m "release: vX.Y.Z"
git push origin vX.Y.Z
gh release create vX.Y.Z \
  --repo powehi-eu/powehi-seo-geo-universal \
  --notes-from-tag \
  --verify-tag
```

## Synchronisation en amont

Le flux de travail programmé récupère en amont dans `sync/upstream-main` et ouvre ou
met à jour une demande de tirage. Résoudre les conflits d'identité en faveur de Powehi et
préserver le droit d'auteur et l'attribution des contributeurs. Suivez `docs/UPSTREAM.md` pour
la liste des surfaces protégées et la validation après fusion.

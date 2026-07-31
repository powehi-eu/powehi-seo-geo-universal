> **Languages:** [Français](WORKFLOW-public-private.fr.md) | English

# Repository workflow

Powehi Universal SEO is published from:

```text
https://github.com/powehi-eu/powehi-seo-geo-universal
```

The local `origin` remote is the Powehi publication destination. The
`upstream` remote is the MIT-licensed source project documented in
`docs/UPSTREAM.md`.

## Development

Create reviewable branches from `main`, run the full validation suite, and open
a pull request against the Powehi repository. Do not push unfinished upstream
synchronization directly to `main`.

```bash
git switch -c codex/<topic>
python -m pytest tests -q
python scripts/portability_check.py
git push -u origin codex/<topic>
```

## Release

Release versions must match across:

- `.claude-plugin/plugin.json`;
- `.codex-plugin/plugin.json`;
- `.claude-plugin/marketplace.json`;
- `pyproject.toml`;
- `CITATION.cff`;
- every maintained `SKILL.md`;
- installer default tags.

Create the release only after CI, installer checks, plugin validation, and the
Powehi identity guard pass.

```bash
git tag -a vX.Y.Z -m "release: vX.Y.Z"
git push origin vX.Y.Z
gh release create vX.Y.Z \
  --repo powehi-eu/powehi-seo-geo-universal \
  --notes-from-tag \
  --verify-tag
```

## Upstream synchronization

The scheduled workflow fetches upstream into `sync/upstream-main` and opens or
updates a pull request. Resolve identity conflicts in favor of Powehi and
preserve copyright and contributor attribution. Follow `docs/UPSTREAM.md` for
the protected-surface list and post-merge validation.

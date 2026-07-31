> **Languages:** [Français](UPSTREAM.fr.md) | English

# Upstream synchronization

Powehi Universal SEO is maintained by Powehi at
`powehi-eu/powehi-seo-geo-universal`. It incorporates MIT-licensed work from
the upstream `AgriciDaniel/claude-seo` project and preserves its copyright and
contributor attributions.

The scheduled synchronization workflow checks the latest published upstream
release against `data/upstream-release.json`. When a new tag appears, it applies
the release-to-release delta to importable paths on the reviewable
`sync/upstream-release` branch and opens or updates a pull request. It never
pushes upstream content directly to `main` and never imports upstream history.

Powehi-owned identity, documentation, manifests, installers, workflows, and the
renamed orchestrator are excluded from automatic patching. The pull request
lists every upstream path changed by the release so protected changes can be
ported deliberately without brand regressions.

## Powehi-owned surfaces

The following surfaces keep the Powehi product identity during conflict
resolution:

- `.codex-plugin/` and `.claude-plugin/`;
- `README.md`, `AGENTS.md`, `CLAUDE.md`, and `docs/`;
- `pyproject.toml`, `CITATION.cff`, installers, uninstallers, and `bin/`;
- GitHub templates, release metadata, and workflows;
- audit orchestration, capability discovery, report branding, and artifact
  contracts.

Upstream functionality, security fixes, tests, skills, scripts, and reference
material may be merged after review. Historical attribution remains in
`LICENSE`, `CONTRIBUTORS.md`, `CHANGELOG.md`, skill-specific license files, and
`original_author` metadata.

## Required post-merge validation

```bash
python -m pytest tests/test_powehi_identity.py -q
python -m pytest tests/test_manifest_consistency.py -q
python scripts/portability_check.py
python -m pytest tests -q
```

## FLOW prompt synchronization

Powehi ships specialized adaptations of the FLOW prompt library. The upstream
source remains Daniel Agrici's FLOW repository under CC BY 4.0, and every adapted
prompt preserves that attribution.

`scripts/sync_flow.py` downloads a complete candidate set before writing. The
candidate must satisfy the Powehi prompt contract: 41 expected files, stable stage
counts, complete metadata and sections, unique prompt identifiers, and unique
operational bodies. A rejected candidate leaves all local files and the lockfile
unchanged.

After an intentional prompt edit, regenerate the derived index and lock with:

```bash
python scripts/prompt_integrity.py --refresh-derived
python scripts/repository_integrity.py --strict --json
```

Authorized extension mirrors and exact duplicate-content exceptions are declared
in `data/repository-integrity.json`. Pinned mirror differences require a reason,
an owner, and explicit source and target hashes. Do not update those hashes without
reviewing the actual diff.

"""Powehi product identity and runtime naming regressions."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/powehi-eu/powehi-seo-geo-universal"
sys.path.insert(0, str(ROOT / "scripts"))

import google_auth  # noqa: E402


def test_plugin_manifests_share_powehi_identity() -> None:
    claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    assert claude["name"] == "powehi-universal-seo-geo"
    assert codex["name"] == claude["name"]
    assert marketplace["plugins"][0]["name"] == claude["name"]
    for manifest in (claude, codex):
        assert manifest["author"]["name"] == "Powehi"
        assert manifest["repository"] == REPOSITORY
        assert "Powehi" in manifest["description"]


def test_primary_runtime_and_config_are_powehi_named() -> None:
    assert (ROOT / "bin" / "powehi-seo-geo").is_file()
    launcher = (ROOT / "bin" / "powehi-seo-geo").read_text(encoding="utf-8")
    runtime = (ROOT / "scripts" / "runtime.py").read_text(encoding="utf-8")
    google = (ROOT / "scripts" / "google_auth.py").read_text(encoding="utf-8")
    assert "POWEHI_SEO_GEO_PYTHON" in launcher
    assert 'prog="powehi-seo-geo"' in runtime
    assert "~/.config/powehi-seo-geo/google-api.json" in google


def test_installers_use_powehi_origin_and_command() -> None:
    for filename in ("install.sh", "install.ps1"):
        text = (ROOT / filename).read_text(encoding="utf-8")
        assert REPOSITORY in text
        assert "powehi-seo-geo" in text
        assert "AgriciDaniel/claude-seo" not in text


def test_public_product_surfaces_do_not_claim_upstream_identity() -> None:
    surfaces = (
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "pyproject.toml",
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".codex-plugin" / "plugin.json",
    )
    forbidden = (
        "Built by agricidaniel",
        "agricidaniel-claude-seo",
        "https://claude-seo.md",
        "https://github.com/AgriciDaniel/claude-seo",
    )
    for path in surfaces:
        text = path.read_text(encoding="utf-8")
        for marker in forbidden:
            assert marker not in text, f"{path.relative_to(ROOT)} contains {marker}"


def test_upstream_attribution_is_preserved() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8").lower()
    upstream = (ROOT / "docs" / "UPSTREAM.md").read_text(encoding="utf-8")
    assert "copyright (c) 2026 agricidaniel" in license_text
    assert "AgriciDaniel/claude-seo" in upstream


def test_legacy_google_config_migration_is_non_destructive(
    tmp_path: Path, monkeypatch
) -> None:
    legacy = tmp_path / "legacy"
    target = tmp_path / "powehi" / "google-api.json"
    legacy.mkdir()
    source = legacy / "google-api.json"
    source.write_text('{"default_property":"sc-domain:example.com"}', encoding="utf-8")
    monkeypatch.setattr(google_auth, "LEGACY_CONFIG_DIR", legacy)
    monkeypatch.setattr(google_auth, "CONFIG_PATH", str(target))
    monkeypatch.setattr(google_auth, "TOKEN_PATH", str(target.parent / "oauth-token.json"))

    result = google_auth.migrate_legacy_config()

    assert source.is_file()
    assert target.is_file()
    assert result["migrated"] == ["google-api.json"]
    marker = json.loads((target.parent / "migration.json").read_text(encoding="utf-8"))
    assert marker["status"] == "completed"

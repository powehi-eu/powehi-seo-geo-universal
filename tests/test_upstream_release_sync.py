"""Contracts for reviewable upstream release synchronization."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_upstream_release_state_is_explicit() -> None:
    state = json.loads((ROOT / "data/upstream-release.json").read_text(encoding="utf-8"))
    assert state["repository"] == "AgriciDaniel/claude-seo"
    assert state["tag"].startswith("v")
    assert state["release_url"].endswith(f"/releases/tag/{state['tag']}")
    assert state["published_at"].endswith("Z")


def test_sync_tracks_releases_without_merging_upstream_history() -> None:
    workflow = (ROOT / ".github/workflows/sync-upstream.yml").read_text(
        encoding="utf-8"
    )
    assert "releases/latest" in workflow
    assert "data/upstream-release.json" in workflow
    assert "git diff --binary upstream-base upstream-latest" in workflow
    assert "sync/upstream-release" in workflow
    assert "git merge" not in workflow
    assert "upstream/main" not in workflow

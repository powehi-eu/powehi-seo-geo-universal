"""Repository duplicate and mirror contract regressions."""

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import repository_integrity as ri  # noqa: E402


def test_repository_integrity_contract_passes():
    result = ri.run_checks()
    assert result["errors"] == []
    assert result["unexpected_exact_duplicates"] == []
    assert result["unexpected_normalized_duplicates"] == []
    assert result["mirror_drift"] == []
    assert result["status"] == "PASS"


def test_manifest_declares_all_current_mirror_relationships():
    manifest = json.loads(ri.MANIFEST.read_text(encoding="utf-8"))
    assert len(manifest["mirrors"]) == 14
    assert {entry["comparison"] for entry in manifest["mirrors"]} == {
        "exact", "body_equal", "pinned_pair"
    }


def test_duplicate_exception_requires_matching_hash_and_members():
    rules = [{
        "normalized_sha256": "abc",
        "paths": ["a.md", "b.md"],
    }]
    assert ri.duplicate_allowed(["a.md", "b.md"], "abc", rules)
    assert not ri.duplicate_allowed(["a.md", "c.md"], "abc", rules)
    assert not ri.duplicate_allowed(["a.md", "b.md"], "def", rules)


def test_normalization_ignores_line_endings_and_trailing_spaces():
    left = ri.normalized_text_bytes(b"alpha  \r\nbeta\r\n")
    right = ri.normalized_text_bytes(b"alpha\nbeta\n")
    assert left == right


def test_manifest_rejects_duplicate_relationship_ids():
    manifest = {
        "version": 1,
        "allowed_duplicate_content": [
            {"id": "same", "reason": "test", "owner": "test"}
        ],
        "mirrors": [
            {"id": "same", "reason": "test", "owner": "test"}
        ],
    }
    assert "manifest: relationship ids must be globally unique" in ri.validate_manifest(manifest)

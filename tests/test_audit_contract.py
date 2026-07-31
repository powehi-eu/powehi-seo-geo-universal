"""Executable full-audit artifact contract tests."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_contract  # noqa: E402


def test_initialize_creates_fresh_timestamped_run(tmp_path: Path) -> None:
    result = audit_contract.initialize(
        "https://example.com/", tmp_path, run_id="2026-07-31T10-00-00Z"
    )
    run_dir = Path(result["run_dir"])
    assert run_dir == (
        tmp_path / "example.com-audit" / "runs" / "2026-07-31T10-00-00Z"
    ).resolve()
    data = json.loads((run_dir / "audit-data.json").read_text(encoding="utf-8"))
    assert data["generator"]["name"] == "Powehi Universal SEO"
    assert set(data["capabilities"]) == set(audit_contract.CAPABILITY_NAMES)


def test_validate_requires_all_mandatory_artifacts(tmp_path: Path) -> None:
    run_dir = Path(
        audit_contract.initialize("https://example.com/", tmp_path, run_id="run-1")["run_dir"]
    )
    result = audit_contract.validate(run_dir)
    assert result["status"] == "FAIL"
    assert "FULL-AUDIT-REPORT.md" in result["missing_artifacts"]
    assert "findings/google.md" in result["missing_artifacts"]
    assert "findings/backlinks.md" in result["missing_artifacts"]


def test_validate_accepts_complete_contract(tmp_path: Path) -> None:
    run_dir = Path(
        audit_contract.initialize("https://example.com/", tmp_path, run_id="run-2")["run_dir"]
    )
    for relative in (
        "FULL-AUDIT-REPORT.md",
        "ACTION-PLAN.md",
        "findings/google.md",
        "findings/backlinks.md",
    ):
        path = run_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Complete\n", encoding="utf-8")
    data_path = run_dir / "audit-data.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data["audit_run"]["status"] = "completed"
    data["audit_run"]["completed_at"] = "2026-07-31T10:10:00Z"
    data_path.write_text(json.dumps(data), encoding="utf-8")
    result = audit_contract.validate(run_dir)
    assert result["status"] == "PASS"


def test_validate_rejects_findings_without_provenance(tmp_path: Path) -> None:
    run_dir = Path(
        audit_contract.initialize("https://example.com/", tmp_path, run_id="run-3")["run_dir"]
    )
    for relative in (
        "FULL-AUDIT-REPORT.md",
        "ACTION-PLAN.md",
        "findings/google.md",
        "findings/backlinks.md",
    ):
        path = run_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Complete\n", encoding="utf-8")
    data_path = run_dir / "audit-data.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data["categories"] = [{"name": "Technical", "findings": [{"title": "Missing data"}]}]
    data_path.write_text(json.dumps(data), encoding="utf-8")
    result = audit_contract.validate(run_dir)
    assert result["status"] == "FAIL"
    assert any(".source is required" in error for error in result["errors"])

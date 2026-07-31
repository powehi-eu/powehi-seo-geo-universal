#!/usr/bin/env python3
"""Initialize and validate Powehi Universal SEO audit runs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_ARTIFACTS = (
    "audit-data.json",
    "FULL-AUDIT-REPORT.md",
    "ACTION-PLAN.md",
    "capability-discovery.json",
    "findings/google.md",
    "findings/backlinks.md",
)
CAPABILITY_NAMES = ("gsc", "ga4", "crux", "pagespeed", "backlinks")
CAPABILITY_STATUSES = {
    "passed",
    "failed",
    "unavailable",
    "insufficient_data",
    "partial",
    "not_applicable",
}
RUN_STATUSES = {"in_progress", "completed", "completed_with_errors", "failed"}
EVIDENCE_TYPES = {"observed", "field_data", "lab_data", "inferred"}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_run_id(value: str | None = None) -> str:
    raw = value or _now()
    return re.sub(r"[^0-9A-Za-z._-]", "-", raw).strip("-")


def _domain_from_target(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("target must be an absolute HTTP(S) URL")
    return parsed.hostname.lower()


def _empty_capability(name: str) -> dict:
    return {
        "available": False,
        "authenticated": False,
        "usable": False,
        "provider": None,
        "transport": None,
        "property": None,
        "status": "unavailable",
        "error": {"code": "not_checked", "message": f"{name} has not been checked"},
    }


def initialize(target: str, output_root: Path, run_id: str | None = None) -> dict:
    domain = _domain_from_target(target)
    selected_run_id = _safe_run_id(run_id)
    audit_root = output_root / f"{domain}-audit"
    run_dir = audit_root / "runs" / selected_run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "findings").mkdir()
    (run_dir / "data").mkdir()
    (run_dir / "screenshots").mkdir()
    (run_dir / "charts").mkdir()

    capabilities = {name: _empty_capability(name) for name in CAPABILITY_NAMES}
    discovery = {
        "schema_version": "1.0",
        "started_at": _now(),
        "completed_at": None,
        "capabilities": capabilities,
    }
    audit_data = {
        "schema_version": "2.0",
        "generator": {"name": "Powehi Universal SEO", "version": "unknown"},
        "audit_run": {
            "run_id": selected_run_id,
            "target": target,
            "started_at": _now(),
            "completed_at": None,
            "status": "in_progress",
            "source": "live",
            "baseline_used": False,
        },
        "capabilities": capabilities,
        "summary": {
            "health_score": 0,
            "business_type": "undetermined",
            "top_findings": [],
            "quick_wins": [],
        },
        "categories": [],
        "action_plan": {"phases": []},
        "artifacts": {
            "full_report": "FULL-AUDIT-REPORT.md",
            "action_plan": "ACTION-PLAN.md",
            "html_report": None,
            "pdf_report": None,
            "findings_dir": "findings/",
            "screenshots_dir": "screenshots/",
        },
        "errors": [],
    }
    (run_dir / "capability-discovery.json").write_text(
        json.dumps(discovery, indent=2), encoding="utf-8"
    )
    (run_dir / "audit-data.json").write_text(
        json.dumps(audit_data, indent=2), encoding="utf-8"
    )
    result = {
        "status": "initialized",
        "domain": domain,
        "run_id": selected_run_id,
        "run_dir": str(run_dir.resolve()),
    }
    return result


def _validate_capabilities(capabilities: object, errors: list[str]) -> None:
    if not isinstance(capabilities, dict):
        errors.append("capabilities must be an object")
        return
    for name in CAPABILITY_NAMES:
        item = capabilities.get(name)
        if not isinstance(item, dict):
            errors.append(f"capabilities.{name} is missing")
            continue
        for key in ("available", "authenticated", "usable"):
            if not isinstance(item.get(key), bool):
                errors.append(f"capabilities.{name}.{key} must be boolean")
        if item.get("status") not in CAPABILITY_STATUSES:
            errors.append(f"capabilities.{name}.status is invalid")


def _validate_findings(value: object, errors: list[str]) -> None:
    if not isinstance(value, list):
        return
    for category_index, category in enumerate(value):
        if not isinstance(category, dict):
            continue
        findings = category.get("findings", [])
        if not isinstance(findings, list):
            errors.append(f"categories[{category_index}].findings must be an array")
            continue
        for finding_index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                errors.append(
                    f"categories[{category_index}].findings[{finding_index}] must be an object"
                )
                continue
            prefix = f"categories[{category_index}].findings[{finding_index}]"
            for key in ("source", "evidence_type", "status", "freshness"):
                if key not in finding:
                    errors.append(f"{prefix}.{key} is required")
            if finding.get("evidence_type") not in EVIDENCE_TYPES:
                errors.append(f"{prefix}.evidence_type is invalid")
            if finding.get("status") not in CAPABILITY_STATUSES:
                errors.append(f"{prefix}.status is invalid")


def validate(run_dir: Path) -> dict:
    errors: list[str] = []
    missing = [name for name in REQUIRED_ARTIFACTS if not (run_dir / name).is_file()]
    for name in missing:
        errors.append(f"missing artifact: {name}")

    data: dict = {}
    data_path = run_dir / "audit-data.json"
    if data_path.is_file():
        try:
            loaded = json.loads(data_path.read_text(encoding="utf-8"))
            data = loaded if isinstance(loaded, dict) else {}
            if not data:
                errors.append("audit-data.json must contain an object")
        except (OSError, ValueError) as exc:
            errors.append(f"audit-data.json is invalid: {exc}")

    if data:
        if data.get("schema_version") != "2.0":
            errors.append("schema_version must be 2.0")
        generator = data.get("generator")
        if not isinstance(generator, dict) or generator.get("name") != "Powehi Universal SEO":
            errors.append("generator.name must be Powehi Universal SEO")
        audit_run = data.get("audit_run")
        if not isinstance(audit_run, dict):
            errors.append("audit_run must be an object")
        else:
            if audit_run.get("status") not in RUN_STATUSES:
                errors.append("audit_run.status is invalid")
            for key in ("run_id", "target", "started_at", "source"):
                if not audit_run.get(key):
                    errors.append(f"audit_run.{key} is required")
        _validate_capabilities(data.get("capabilities"), errors)
        _validate_findings(data.get("categories"), errors)

    return {
        "status": "PASS" if not errors else "FAIL",
        "run_dir": str(run_dir.resolve()),
        "missing_artifacts": missing,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="audit_contract.py")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--target", required=True)
    init_parser.add_argument("--output-root", default=".")
    init_parser.add_argument("--run-id")
    init_parser.add_argument("--json", action="store_true")
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--run-dir", required=True)
    validate_parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        if args.command == "init":
            result = initialize(args.target, Path(args.output_root), args.run_id)
        else:
            result = validate(Path(args.run_dir))
    except (OSError, ValueError) as exc:
        result = {"status": "FAIL", "errors": [str(exc)]}

    if getattr(args, "json", False):
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
        for error in result.get("errors", []):
            print(f"- {error}", file=sys.stderr)
    return 0 if result["status"] in {"PASS", "initialized"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

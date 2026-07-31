#!/usr/bin/env python3
"""Enforce duplicate, mirror, path and FLOW prompt integrity contracts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "data" / "repository-integrity.json"
sys.path.insert(0, str(REPO / "scripts"))
from prompt_integrity import validate_prompt_set  # noqa: E402


def normalized_text_bytes(data: bytes) -> bytes | None:
    if b"\0" in data:
        return None
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return text.encode("utf-8")


def normalized_sha256(path: Path) -> str:
    normalized = normalized_text_bytes(path.read_bytes())
    data = normalized if normalized is not None else path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def body_after_frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    parts = text.split("---", 2)
    body = parts[2] if len(parts) == 3 else text
    return "\n".join(line.rstrip() for line in body.splitlines()).strip()


def tracked_blobs() -> dict[str, str]:
    output = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-s"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout
    result = {}
    for line in output.splitlines():
        match = re.match(r"^\d+ ([0-9a-f]+) \d+\t(.+)$", line)
        if match:
            result[match.group(2)] = match.group(1)
    return result


def validate_manifest(manifest: dict) -> list[str]:
    errors = []
    if manifest.get("version") != 1:
        errors.append("manifest: unsupported or missing version")
    ids = []
    for section in ("allowed_duplicate_content", "mirrors"):
        entries = manifest.get(section)
        if not isinstance(entries, list):
            errors.append(f"manifest: {section} must be a list")
            continue
        for entry in entries:
            missing = {"id", "reason", "owner"} - entry.keys()
            if missing:
                errors.append(f"manifest: {section} entry missing {sorted(missing)}")
            ids.append(entry.get("id"))
    if len(ids) != len(set(ids)):
        errors.append("manifest: relationship ids must be globally unique")
    return errors


def duplicate_allowed(paths: list[str], sha: str, rules: list[dict]) -> bool:
    members = set(paths)
    for rule in rules:
        if rule.get("normalized_sha256") != sha:
            continue
        if "paths" in rule and members == set(rule["paths"]):
            return True
        pattern = rule.get("path_pattern")
        if pattern and all(re.search(pattern, path) for path in paths):
            return True
    return False


def check_duplicates(blobs: dict[str, str], manifest: dict) -> tuple[list[dict], list[dict]]:
    exact_groups: dict[str, list[str]] = defaultdict(list)
    normalized_groups: dict[str, list[str]] = defaultdict(list)
    normalized_by_path = {}
    for path in blobs:
        full = REPO / path
        # A tracked file can be intentionally deleted in the working tree before
        # the deletion is staged. Integrity checks validate the current tree.
        if not full.is_file():
            continue
        raw = full.read_bytes()
        exact_groups[hashlib.sha256(raw).hexdigest()].append(path)
        normalized = normalized_text_bytes(raw)
        if normalized is not None and normalized:
            sha = hashlib.sha256(normalized).hexdigest()
            normalized_groups[sha].append(path)
            normalized_by_path[path] = sha

    rules = manifest["allowed_duplicate_content"]
    unexpected_exact = []
    unexpected_normalized = []
    exact_member_sets = set()
    for blob, paths in exact_groups.items():
        if len(paths) < 2:
            continue
        paths = sorted(paths)
        sha = normalized_by_path.get(paths[0], "")
        exact_member_sets.add(tuple(paths))
        if not sha or not duplicate_allowed(paths, sha, rules):
            unexpected_exact.append({"git_blob": blob, "paths": paths})
    for sha, paths in normalized_groups.items():
        if len(paths) < 2:
            continue
        paths = sorted(paths)
        if tuple(paths) in exact_member_sets:
            continue
        if not duplicate_allowed(paths, sha, rules):
            unexpected_normalized.append({"normalized_sha256": sha, "paths": paths})
    return unexpected_exact, unexpected_normalized


def check_mirrors(blobs: dict[str, str], manifest: dict) -> list[str]:
    errors = []
    for mirror in manifest["mirrors"]:
        source_rel, target_rel = mirror.get("source"), mirror.get("target")
        source, target = REPO / str(source_rel), REPO / str(target_rel)
        if not source.is_file() or not target.is_file():
            errors.append(f"{mirror.get('id')}: missing source or target")
            continue
        mode = mirror.get("comparison")
        if mode == "exact":
            if blobs.get(str(source_rel)) != blobs.get(str(target_rel)):
                errors.append(f"{mirror['id']}: exact mirror drift")
        elif mode == "body_equal":
            if body_after_frontmatter(source) != body_after_frontmatter(target):
                errors.append(f"{mirror['id']}: body mirror drift")
        elif mode == "pinned_pair":
            got_source, got_target = normalized_sha256(source), normalized_sha256(target)
            if got_source != mirror.get("source_sha256"):
                errors.append(f"{mirror['id']}: source changed without contract update")
            if got_target != mirror.get("target_sha256"):
                errors.append(f"{mirror['id']}: target changed without contract update")
        else:
            errors.append(f"{mirror.get('id')}: unsupported comparison mode {mode!r}")
    return errors


def check_paths(paths: list[str]) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []
    lower_groups: dict[str, list[str]] = defaultdict(list)
    suspicious = re.compile(r"(?i)(?:copy|copie|duplicate|backup|bak|old|final-final|\(\d+\))$")
    for path in paths:
        lower_groups[path.lower()].append(path)
        stem = Path(path).stem
        if suspicious.search(stem) or Path(path).suffix.lower() in {".bak", ".old", ".orig", ".tmp"}:
            warnings.append(f"suspicious copy-like filename: {path}")
    for members in lower_groups.values():
        if len(members) > 1:
            errors.append("case-insensitive path collision: " + ", ".join(sorted(members)))
    return errors, warnings


def run_checks(manifest_path: Path = MANIFEST) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_errors = validate_manifest(manifest)
    blobs = tracked_blobs()
    unexpected_exact, unexpected_normalized = check_duplicates(blobs, manifest)
    mirror_drift = check_mirrors(blobs, manifest)
    path_errors, warnings = check_paths(list(blobs))
    prompt_result = validate_prompt_set()
    errors = manifest_errors + mirror_drift + path_errors + prompt_result["errors"]
    if unexpected_exact:
        errors.append(f"{len(unexpected_exact)} unallowlisted exact duplicate group(s)")
    if unexpected_normalized:
        errors.append(f"{len(unexpected_normalized)} unallowlisted normalized duplicate group(s)")
    return {
        "status": "PASS" if not errors else "FAIL",
        "files_checked": len(blobs),
        "manifest_errors": manifest_errors,
        "unexpected_exact_duplicates": unexpected_exact,
        "unexpected_normalized_duplicates": unexpected_normalized,
        "mirror_drift": mirror_drift,
        "path_errors": path_errors,
        "flow": prompt_result,
        "errors": errors,
        "warnings": warnings + prompt_result["warnings"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too")
    args = parser.parse_args()
    result = run_checks(args.manifest)
    if args.strict and result["warnings"]:
        result["status"] = "FAIL"
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARN: {warning}")
        print(f"{result['status']}: {result['files_checked']} tracked files checked")
    if result["status"] == "PASS":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the operational integrity of the bundled FLOW prompt library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PROMPTS = REPO / "skills" / "seo-flow" / "references" / "prompts"
REFERENCES = PROMPTS.parent
LOCK_PATH = REFERENCES / "flow-prompts.lock"
EXPECTED_COUNTS = {"find": 5, "leverage": 1, "optimize": 21, "win": 3, "local": 11}
REQUIRED_KEYS = {"title", "description", "prompt_id", "stage", "objective", "source", "adaptation", "updated"}
REQUIRED_SECTIONS = {
    "Use This When",
    "Required Inputs",
    "Evidence Rules",
    "Prompt",
    "Expected Output",
    "Verification Checklist",
    "Source Note",
}


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_document(text: str) -> tuple[dict[str, str], str]:
    """Return simple YAML frontmatter values and Markdown body.

    Prompt metadata is intentionally scalar so validation remains dependency-free.
    Lists used by a prompt belong in its Markdown sections, not frontmatter.
    """
    text = normalize_newlines(text).lstrip("\ufeff")
    text = re.sub(r"^<!--.*?-->\s*", "", text, count=1, flags=re.DOTALL)
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata, text[end + 5 :]


def operational_body(text: str) -> str:
    """Canonicalize a prompt while ignoring attribution, metadata and title only."""
    _, body = split_document(text)
    body = re.sub(r"^# .+?\n", "", body.lstrip(), count=1)
    return "\n".join(line.rstrip() for line in body.splitlines()).strip()


def operational_hash(text: str) -> str:
    return hashlib.sha256(operational_body(text).encode("utf-8")).hexdigest()


def headings(body: str) -> set[str]:
    return {match.strip() for match in re.findall(r"^## (.+)$", body, flags=re.MULTILINE)}


def build_prompt_index(prompt_root: Path = PROMPTS) -> str:
    rows = []
    stage_order = {stage: index for index, stage in enumerate(EXPECTED_COUNTS)}
    paths = [path for path in prompt_root.rglob("*.md") if path.name != "README.md"]
    paths.sort(key=lambda path: (stage_order.get(path.parent.name, 99), path.name))
    for path in paths:
        metadata, _ = split_document(path.read_text(encoding="utf-8"))
        rows.append(
            (
                path.parent.name,
                path.name,
                metadata.get("title", ""),
                metadata.get("description", ""),
                metadata.get("objective", ""),
            )
        )
    lines = [
        "<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi -->",
        "",
        "# FLOW Prompt Index",
        "",
        "| Stage | Filename | Title | Objective | Description |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        escaped = [value.replace("|", "\\|").replace("\n", " ").strip() for value in row]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines) + "\n"


def refresh_derived_files(prompt_root: Path = PROMPTS) -> None:
    """Refresh the generated prompt index and canonical LF integrity lock."""
    index_path = prompt_root / "README.md"
    index_path.write_text(build_prompt_index(prompt_root), encoding="utf-8", newline="\n")
    refs = prompt_root.parent
    tracked = [refs / "bibliography.md", refs / "flow-framework.md"]
    tracked.extend(sorted(prompt_root.rglob("*.md")))
    lines = [
        "# flow-prompts.lock — SHA-256 baseline for Powehi FLOW references",
        "# Ref: Powehi curated adaptations | format: <sha256hex>  <rel_path>",
        "",
    ]
    for path in tracked:
        content = normalize_newlines(path.read_text(encoding="utf-8")).encode("utf-8")
        rel = path.relative_to(REPO).as_posix()
        lines.append(f"{hashlib.sha256(content).hexdigest()}  {rel}")
    (refs / "flow-prompts.lock").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def validate_prompt_set(prompt_root: Path = PROMPTS) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    files = sorted(path for path in prompt_root.rglob("*.md") if path.name != "README.md")
    stage_counts: dict[str, int] = defaultdict(int)
    ids: dict[str, list[str]] = defaultdict(list)
    hashes: dict[str, list[str]] = defaultdict(list)

    for path in files:
        rel = path.relative_to(prompt_root).as_posix()
        text = path.read_text(encoding="utf-8")
        metadata, body = split_document(text)
        stage = path.parent.name
        stage_counts[stage] += 1

        missing_keys = sorted(REQUIRED_KEYS - metadata.keys())
        if missing_keys:
            errors.append(f"{rel}: missing frontmatter keys: {', '.join(missing_keys)}")
        if metadata.get("stage") != stage:
            errors.append(f"{rel}: frontmatter stage {metadata.get('stage')!r} does not match {stage!r}")
        prompt_id = metadata.get("prompt_id", "")
        if prompt_id:
            ids[prompt_id].append(rel)
            if not prompt_id.startswith(f"flow.{stage}."):
                errors.append(f"{rel}: prompt_id must start with flow.{stage}.")

        missing_sections = sorted(REQUIRED_SECTIONS - headings(body))
        if missing_sections:
            errors.append(f"{rel}: missing sections: {', '.join(missing_sections)}")
        if body.count("```text") != 1:
            errors.append(f"{rel}: expected exactly one ```text prompt block")
        canonical = operational_body(text)
        if len(canonical) < 600:
            errors.append(f"{rel}: operational body is too small ({len(canonical)} chars)")
        hashes[hashlib.sha256(canonical.encode("utf-8")).hexdigest()].append(rel)

    if dict(stage_counts) != EXPECTED_COUNTS:
        errors.append(f"stage counts mismatch: got {dict(stage_counts)}, expected {EXPECTED_COUNTS}")
    for prompt_id, members in sorted(ids.items()):
        if len(members) > 1:
            errors.append(f"duplicate prompt_id {prompt_id}: {', '.join(members)}")
    duplicate_bodies = [members for members in hashes.values() if len(members) > 1]
    for members in duplicate_bodies:
        errors.append("duplicate operational body: " + ", ".join(members))

    return {
        "status": "PASS" if not errors else "FAIL",
        "files_checked": len(files),
        "stage_counts": dict(stage_counts),
        "unique_prompt_ids": len(ids),
        "unique_operational_bodies": len(hashes),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROMPTS)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--refresh-derived", action="store_true")
    args = parser.parse_args()
    if args.refresh_derived:
        refresh_derived_files(args.root)
    result = validate_prompt_set(args.root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        print(
            f"{result['status']}: {result['files_checked']} prompts, "
            f"{result['unique_operational_bodies']} unique operational bodies"
        )
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

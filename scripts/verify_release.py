#!/usr/bin/env python3
"""
Verify the integrity of a powehi-seo-geo checkout against a release manifest.

Usage
=====

After installing from a tag::

    python scripts/verify_release.py path/to/release-manifest.json

The script returns exit code 0 when every file in the manifest is
present and matches the recorded SHA-256, and exit code 1 (with a
human-readable report) on any mismatch, missing file, or extra file.

This pairs with ``scripts/release_sign.py`` (used by the maintainer to
generate the manifest at release time) and the GitHub release
attachment workflow that publishes the manifest alongside each tag.

Threat model
============
See SECURITY.md "Tampered install" section. Verification catches tag
force-pushes and partial supply-chain tampering, but does NOT defend
against an attacker who can replace both the source files and the
published manifest. For that level of trust, the manifest must be
signed by the maintainer's GPG key whose fingerprint is published
out of band.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _tree_sha256(files: dict[str, str]) -> str:
    """Recompute the manifest-wide digest.

    Must stay byte-identical to release_sign.py's construction: one
    ``<sha>  <path>\\n`` line per entry, sorted by path (sha256sum format).
    """
    tree_input = "".join(f"{sha}  {path}\n" for path, sha in sorted(files.items()))
    return hashlib.sha256(tree_input.encode("utf-8")).hexdigest()


def _tracked_files(root: Path) -> list[str] | None:
    """Return git-tracked paths under ``root``, or None if git is unavailable.

    Used to detect files added to the checkout after the manifest was
    generated. Falls back to None (extra-file detection disabled, and said
    so in the report) rather than guessing from a filesystem walk, which
    would flood the result with build artefacts and venvs.
    """
    git = shutil.which("git")
    if not git:
        return None
    try:
        result = subprocess.run(
            [git, "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return [p for p in result.stdout.split("\0") if p]


def verify(manifest_path: Path, root: Path = REPO_ROOT) -> dict:
    """Compare a manifest against the working tree at ``root``.

    Returns a dict with:
        ok            : True iff every manifest file matches AND no
                        unexpected tracked file is present.
        manifest      : the manifest payload (for the caller to display
                        version/tag/commit context).
        mismatched    : paths whose SHA-256 differs.
        missing       : paths in manifest but absent from disk.
        extra         : git-tracked paths present on disk but absent from
                        the manifest.
        extra_checked : False when git was unavailable, meaning ``extra``
                        could not be computed and is not evidence of a
                        clean tree.
        tree_sha256   : {"expected", "actual", "ok"} for the manifest-wide
                        digest, or None when the manifest records none.
    """
    # Explicit UTF-8: the manifest is written as UTF-8 JSON, and the default
    # locale encoding on Windows (cp1252) fails on non-ASCII tracked paths.
    with manifest_path.open(encoding="utf-8") as fh:
        manifest = json.load(fh)

    expected = manifest.get("files", {})
    mismatched: list[dict] = []
    missing: list[str] = []

    for rel, expected_sha in sorted(expected.items()):
        abs_path = root / rel
        if not abs_path.is_file():
            missing.append(rel)
            continue
        actual_sha = _sha256(abs_path)
        if actual_sha != expected_sha:
            mismatched.append(
                {"path": rel, "expected": expected_sha, "actual": actual_sha}
            )

    # Files added after the manifest was cut are a tamper vector in their own
    # right: Python auto-executes sitecustomize.py / conftest.py from the
    # tree, so a checkout can be subverted without modifying any manifest
    # entry. Reporting only mismatches would call that tree "OK".
    tracked = _tracked_files(root)
    extra_checked = tracked is not None
    extra: list[str] = []
    if tracked is not None:
        # release_sign.build_manifest skips tracked entries that are not
        # regular files (submodules, broken symlinks); mirror that skip or
        # every such entry would be reported as an unexpected addition.
        extra = sorted(
            rel
            for rel in set(tracked) - set(expected)
            if (root / rel).is_file()
        )

    # Recompute the manifest-wide digest instead of only printing it, so a
    # manifest with entries deleted from `files` cannot pass silently.
    recorded_tree = manifest.get("tree_sha256")
    tree_result = None
    if recorded_tree:
        actual_tree = _tree_sha256(expected)
        tree_result = {
            "expected": recorded_tree,
            "actual": actual_tree,
            "ok": actual_tree == recorded_tree,
        }

    return {
        "ok": not (
            mismatched
            or missing
            or extra
            or (tree_result is not None and not tree_result["ok"])
        ),
        "manifest": {
            "version": manifest.get("version"),
            "tag": manifest.get("tag"),
            "commit": manifest.get("commit"),
            "generated_at": manifest.get("generated_at"),
            "tree_sha256": recorded_tree,
        },
        "checked": len(expected),
        "mismatched": mismatched,
        "missing": missing,
        "extra": extra,
        "extra_checked": extra_checked,
        "tree_sha256": tree_result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a powehi-seo-geo checkout against a release manifest."
    )
    parser.add_argument(
        "manifest", type=Path, help="Path to release-manifest.json."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to verify (default: this checkout).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON report instead of human-readable text.",
    )
    args = parser.parse_args()

    if not args.manifest.is_file():
        print(f"Error: manifest not found: {args.manifest}", file=sys.stderr)
        return 2

    result = verify(args.manifest, args.root)

    if args.json:
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        m = result["manifest"]
        status = "OK" if result["ok"] else "FAIL"
        print(f"Verification: {status}")
        print(f"  Manifest version: {m['version']}  tag: {m['tag']}")
        print(f"  Manifest commit:  {m['commit']}")
        print(f"  Generated at:     {m['generated_at']}")
        tree = result["tree_sha256"]
        if tree is None:
            print(f"  Tree SHA-256:     {m['tree_sha256']} (not recorded)")
        elif tree["ok"]:
            print(f"  Tree SHA-256:     {tree['expected']} (verified)")
        else:
            print(f"  Tree SHA-256:     MISMATCH")
            print(f"        expected: {tree['expected']}")
            print(f"        actual:   {tree['actual']}")
        print(f"  Files checked:    {result['checked']}")
        if not result["extra_checked"]:
            print("  Extra files:      not checked (git unavailable)")
        if result["extra"]:
            print(f"\n  Unexpected tracked files ({len(result['extra'])}):")
            for path in result["extra"]:
                print(f"    - {path}")
        if result["mismatched"]:
            print(f"\n  Mismatched ({len(result['mismatched'])}):")
            for row in result["mismatched"]:
                print(f"    - {row['path']}")
                print(f"        expected: {row['expected']}")
                print(f"        actual:   {row['actual']}")
        if result["missing"]:
            print(f"\n  Missing ({len(result['missing'])}):")
            for path in result["missing"]:
                print(f"    - {path}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

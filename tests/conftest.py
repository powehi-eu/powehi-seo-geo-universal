"""Shared pytest configuration.

The repository ships executable scripts rather than an installable package, so
`scripts/` and the extension script directories are not importable by default.
Putting them on `sys.path` here lets tests use ordinary `import` statements
rather than dynamic file loading, which keeps module resolution static and
auditable.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SCRIPT_DIRS = (
    REPO_ROOT / "scripts",
    REPO_ROOT / "extensions" / "banana" / "scripts",
)

for script_dir in SCRIPT_DIRS:
    entry = str(script_dir)
    if script_dir.is_dir() and entry not in sys.path:
        sys.path.insert(0, entry)

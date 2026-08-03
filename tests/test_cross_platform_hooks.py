"""Cross-platform hook configuration regressions."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS_JSON = REPO_ROOT / "hooks" / "hooks.json"
SCHEMA_HOOK = REPO_ROOT / "hooks" / "validate-schema.js"
INSTALL_PS1 = REPO_ROOT / "install.ps1"


def _post_tool_handler() -> dict:
    config = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    return config["hooks"]["PostToolUse"][0]["hooks"][0]


def test_schema_hook_uses_exec_form_args_and_tool_input_placeholder() -> None:
    handler = _post_tool_handler()
    serialized = json.dumps(handler)

    assert handler["type"] == "command"
    assert handler["command"] == "node"
    assert "args" in handler
    assert handler["args"][0] == "${CLAUDE_PLUGIN_ROOT}/hooks/validate-schema.js"
    assert handler["args"][1] == "${tool_input.file_path}"
    assert "$FILE_PATH" not in serialized
    assert "$" not in handler["command"]
    assert handler["command"] != "sh"


def test_schema_hook_runs_on_node_without_an_interpreter_shim() -> None:
    """The hook must run directly on Node, with no Python resolution step."""
    handler = _post_tool_handler()

    assert len(handler["args"]) == 2, "no launcher script should sit between node and the hook"
    assert not (REPO_ROOT / "hooks" / "run-python-hook.js").exists()
    assert not (REPO_ROOT / "hooks" / "python-probe.py").exists()


def test_hook_directory_starts_no_subprocess() -> None:
    """Hook code must not spawn child processes (audit: suspicious.dangerous_exec)."""
    forbidden = ("child_process", "spawnSync", "execSync", "execFileSync")

    for source in (REPO_ROOT / "hooks").glob("*.js"):
        text = source.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, f"{source.name} references {token}"


def _run_hook(tmp_path: Path, body: str) -> subprocess.CompletedProcess:
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not available in this test environment")

    page = tmp_path / "page.html"
    page.write_text(body, encoding="utf-8")
    return subprocess.run(
        [node, str(SCHEMA_HOOK), str(page)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=15,
    )


def _page_with_type(schema_type: str) -> str:
    return (
        '<html><head><script type="application/ld+json">\n'
        f'{{"@context":"https://schema.org","@type":"{schema_type}"}}\n'
        "</script></head></html>"
    )


def test_schema_hook_accepts_valid_markup(tmp_path: Path) -> None:
    assert _run_hook(tmp_path, _page_with_type("Organization")).returncode == 0


def test_schema_hook_blocks_deprecated_type(tmp_path: Path) -> None:
    proc = _run_hook(tmp_path, _page_with_type("ClaimReview"))

    assert proc.returncode == 2
    assert "ClaimReview" in proc.stdout


def test_schema_hook_warns_without_blocking_on_missing_context(tmp_path: Path) -> None:
    body = (
        '<html><head><script type="application/ld+json">\n'
        '{"@type":"Organization"}\n'
        "</script></head></html>"
    )
    proc = _run_hook(tmp_path, body)

    assert proc.returncode == 1
    assert "@context" in proc.stdout


def test_schema_hook_ignores_non_html_files(tmp_path: Path) -> None:
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not available in this test environment")

    target = tmp_path / "notes.txt"
    target.write_text(_page_with_type("ClaimReview"), encoding="utf-8")
    proc = subprocess.run(
        [node, str(SCHEMA_HOOK), str(target)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=15,
    )

    assert proc.returncode == 0


def test_windows_installer_prefers_py_launcher_and_rejects_store_stubs() -> None:
    text = INSTALL_PS1.read_text(encoding="utf-8")
    py_pos = text.index("Exe = 'py'; Args = @('-3')")
    python3_pos = text.index("Exe = 'python3'; Args = @()")
    python_pos = text.index("Exe = 'python'; Args = @()")

    assert py_pos < python3_pos < python_pos
    assert "Microsoft Store|WindowsApps|App execution alias|was not found" in text

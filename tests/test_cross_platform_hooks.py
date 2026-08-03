"""Cross-platform hook configuration regressions."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS_JSON = REPO_ROOT / "hooks" / "hooks.json"
HOOK_LAUNCHER = REPO_ROOT / "hooks" / "run-python-hook.js"
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
    assert handler["args"][0] == "${CLAUDE_PLUGIN_ROOT}/hooks/run-python-hook.js"
    assert handler["args"][1] == "${CLAUDE_PLUGIN_ROOT}/hooks/validate-schema.py"
    assert handler["args"][2] == "${tool_input.file_path}"
    assert "$FILE_PATH" not in serialized
    assert "$" not in handler["command"]
    assert handler["command"] != "sh"


def test_hook_launcher_documents_python_probe_order() -> None:
    text = HOOK_LAUNCHER.read_text(encoding="utf-8")
    for marker in ("POWEHI_SEO_GEO_PYTHON", "py", "-3", "python3", "python"):
        assert marker in text


def test_hook_launcher_preserves_blocking_exit_code_two() -> None:
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not available in this test environment")

    # The launcher only runs hook scripts that live beside it, so the fixture
    # has to be created inside hooks/ and removed afterwards.
    script = HOOK_LAUNCHER.parent / "_test_block_hook.py"
    script.write_text(
        "import sys\n"
        "assert sys.argv[1] == 'payload'\n"
        "sys.exit(2)\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["POWEHI_SEO_GEO_PYTHON"] = sys.executable

    try:
        proc = subprocess.run(
            [node, str(HOOK_LAUNCHER), str(script), "payload"],
            env=env,
            capture_output=True,
            text=True,
            timeout=15,
        )
    finally:
        script.unlink(missing_ok=True)

    assert proc.returncode == 2


def test_hook_launcher_refuses_scripts_outside_hooks_directory(tmp_path: Path) -> None:
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not available in this test environment")

    script = tmp_path / "attacker.py"
    script.write_text("import sys; sys.exit(0)\n", encoding="utf-8")
    env = os.environ.copy()
    env["POWEHI_SEO_GEO_PYTHON"] = sys.executable

    proc = subprocess.run(
        [node, str(HOOK_LAUNCHER), str(script), "payload"],
        env=env,
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert proc.returncode == 1
    assert "must be .py files inside" in proc.stderr


def test_hook_launcher_ignores_non_python_interpreter_override() -> None:
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not available in this test environment")

    script = HOOK_LAUNCHER.parent / "_test_override_hook.py"
    script.write_text("import sys; sys.exit(3)\n", encoding="utf-8")
    env = os.environ.copy()
    # node is a real executable, but its basename is not a python interpreter,
    # so the override must be rejected and the normal probe order used instead.
    env["POWEHI_SEO_GEO_PYTHON"] = node

    try:
        proc = subprocess.run(
            [node, str(HOOK_LAUNCHER), str(script), "payload"],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
    finally:
        script.unlink(missing_ok=True)

    assert "ignored POWEHI_SEO_GEO_PYTHON" in proc.stderr
    assert proc.returncode == 3


def test_windows_installer_prefers_py_launcher_and_rejects_store_stubs() -> None:
    text = INSTALL_PS1.read_text(encoding="utf-8")
    py_pos = text.index("Exe = 'py'; Args = @('-3')")
    python3_pos = text.index("Exe = 'python3'; Args = @()")
    python_pos = text.index("Exe = 'python'; Args = @()")

    assert py_pos < python3_pos < python_pos
    assert "Microsoft Store|WindowsApps|App execution alias|was not found" in text

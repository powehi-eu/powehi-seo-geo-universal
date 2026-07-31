"""Static installer/runtime contract checks that do not mutate a real home."""

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_unix_installer_delegates_to_runtime_without_global_pip() -> None:
    text = (ROOT / "install.sh").read_text(encoding="utf-8")
    assert '"${SKILL_DIR}/bin/powehi-seo-geo" setup' in text
    assert '"${SKILL_DIR}/bin/claude-seo"' in text
    assert "pip install --user" not in text
    assert "python3 -m venv" not in text
    assert "powehi-seo-geo run" in text
    assert "powehi-seo-geo setup" in text
    assert "powehi-seo-geo doctor" in text
    assert '"${runtime_status}" -ne 0 ] && [ "${runtime_status}" -ne 10' in text
    assert 'find "${HOME}/.claude/skills"' not in text


def test_windows_installer_delegates_to_runtime_without_path_mutation() -> None:
    text = (ROOT / "install.ps1").read_text(encoding="utf-8")
    assert "scripts\\runtime.py" in text
    assert "(Join-Path $SkillBin 'claude-seo')" in text
    assert "'setup'" in text
    assert "SetEnvironmentVariable('PATH'" not in text
    assert "pip','install" not in text
    assert "UTF8Encoding($false)" in text
    assert "version_info >= (3, 10)" in text
    assert "$runtime.ExitCode -ne 0 -and $runtime.ExitCode -ne 10" in text
    assert "-Directory -Filter 'seo*'" not in text


def test_launcher_is_executable_and_uses_safe_exec() -> None:
    launcher = ROOT / "bin/powehi-seo-geo"
    if os.name == "nt":
        stage = subprocess.check_output(
            ["git", "ls-files", "--stage", "bin/powehi-seo-geo"],
            cwd=ROOT,
            text=True,
        ).split()
        if stage:
            assert stage[0] == "100755"
        else:
            # New files have no index mode until staged on Windows. The
            # installer applies chmod and the shebang guards the source file.
            assert launcher.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")
    else:
        assert launcher.stat().st_mode & 0o100
    text = launcher.read_text(encoding="utf-8")
    assert 'exec py -3 "${runtime}" "$@"' in text
    assert 'exec python3 "${runtime}" "$@"' in text
    assert 'exec python "${runtime}" "$@"' in text
    assert "eval " not in text

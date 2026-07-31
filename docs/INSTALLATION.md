> **Languages:** [Français](INSTALLATION.fr.md) | English

# Installation Guide

## Prerequisites

- **Python 3.10+** with pip
- **Git** for cloning the repository
- **Claude Code CLI** installed and configured

Optional:
- **Playwright Chromium** - install.sh attempts this automatically; failure is non-fatal; needed only for SPA rendering and screenshots

## Quick Install

### Plugin Install (Claude Code 1.0.33+)

The recommended path. Inside Claude Code:

```
/plugin marketplace add powehi-eu/powehi-seo-geo-universal
/plugin install powehi-seo-geo@powehi-universal-seo-geo
/powehi-seo setup
```

Plugin installation does not run package managers. `/powehi-seo setup` is an explicit,
one-time provisioning step that writes the virtual environment and browser only
to Claude's persistent plugin data. Use `/powehi-seo doctor` for a read-only check.

### Manual Install (Unix, macOS, Linux)

```bash
git clone --depth 1 https://github.com/powehi-eu/powehi-seo-geo-universal.git
bash powehi-seo-geo/install.sh
```

Review-then-run alternative:

```bash
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/install.sh > install.sh
cat install.sh        # review
bash install.sh       # run when satisfied
rm install.sh
```

### Manual Install (Windows, PowerShell)

```powershell
git clone --depth 1 https://github.com/powehi-eu/powehi-seo-geo-universal.git
powershell -ExecutionPolicy Bypass -File powehi-seo-geo\install.ps1
```

The Windows path uses `git clone` rather than `irm | iex` because Claude Code's own security guardrails flag piped remote-script execution. Inspect `install.ps1` before running.

## Manual Installation

1. **Clone the repository**

```bash
git clone https://github.com/powehi-eu/powehi-seo-geo-universal.git
cd powehi-seo-geo
```

2. **Run the installer**

```bash
./install.sh
```

3. **Verify the managed runtime**

The installer delegates dependency and Chromium provisioning to the same runtime
used by every skill. It creates `~/.claude/skills/powehi-seo/.venv/` and never falls
back to global or user package installation.

```bash
~/.claude/skills/powehi-seo/bin/powehi-seo-geo doctor
```

If core setup failed, rerun the inspected installer. If only Chromium failed,
the installer reports a degraded result and raw-fetch analysis remains available.

## Installation Paths

The installer copies files to:

| Component | Path |
|-----------|------|
| Main skill | `~/.claude/skills/powehi-seo/` |
| Sub-skills | `~/.claude/skills/powehi-seo-*/` |
| Subagents | `~/.claude/agents/seo-*.md` |
| Runtime launcher | `~/.claude/skills/powehi-seo/bin/powehi-seo-geo` |
| Isolated Python | `~/.claude/skills/powehi-seo/.venv/` |

## Verify Installation

1. Start Claude Code:

```bash
claude
```

2. Check that the skill is loaded:

```
/powehi-seo
```

You should see a help message or prompt for a URL.

## Uninstallation

If installed as a plugin:

```
/plugin uninstall powehi-seo-geo@powehi-universal-seo-geo
/plugin marketplace remove powehi-eu/powehi-seo-geo-universal
```

If installed manually, run the uninstaller from a fresh clone:

```bash
git clone --depth 1 https://github.com/powehi-eu/powehi-seo-geo-universal.git
bash powehi-seo-geo/uninstall.sh
```

`uninstall.sh` removes all installed sub-skills, sub-agents, and the plugin's MCP entries from `~/.claude/settings.json`. Do not maintain a hand-coded `rm` list. The shipped uninstaller is the canonical source.

## Upgrading

To upgrade to the latest version:

Caution: Prefer downloading, inspecting, then running remote scripts; the pipe-to-shell form below is the less-safe convenience option.

```bash
# Uninstall current version
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/uninstall.sh | bash

# Install new version
curl -fsSL https://raw.githubusercontent.com/powehi-eu/powehi-seo-geo-universal/main/install.sh | bash
```

## Troubleshooting

### "Skill not found" error

Ensure the skill is installed in the correct location:

```bash
ls ~/.claude/skills/powehi-seo/SKILL.md
```

If the file doesn't exist, re-run the installer.

### Python dependency errors

Run the managed setup again:

```bash
~/.claude/skills/powehi-seo/bin/powehi-seo-geo setup
```

### Playwright screenshot errors

Run the managed setup again and inspect the result:

```bash
~/.claude/skills/powehi-seo/bin/powehi-seo-geo setup
~/.claude/skills/powehi-seo/bin/powehi-seo-geo doctor
```

### Permission errors on Unix

Make sure scripts are executable:

```bash
chmod +x ~/.claude/skills/powehi-seo/scripts/*.py
```

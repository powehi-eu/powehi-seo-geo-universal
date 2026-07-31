#!/usr/bin/env bash
set -euo pipefail
root="${XDG_DATA_HOME:-${HOME}/.local/share}/seo-google-suite/mcp-servers"
venv="${root}/seo-google-suite-ga4-venv"
python="${PYTHON_BIN:-python3}"
command -v "$python" >/dev/null || { echo "$python is required" >&2; exit 1; }
mkdir -p "$root" "$HOME/.local/bin"
"$python" -m venv "$venv"
"$venv/bin/python" -m pip install --upgrade pip
"$venv/bin/python" -m pip install google-analytics-mcp
upstream_command="$venv/bin/ga4-mcp-server"
if [[ ! -x "$upstream_command" ]]; then
  echo "GA4 MCP entry point not found: $upstream_command" >&2
  exit 1
fi
ln -sf "$upstream_command" "$HOME/.local/bin/analytics-mcp"
echo "GA4 MCP ready at $HOME/.local/bin/analytics-mcp"

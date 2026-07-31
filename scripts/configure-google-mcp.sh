#!/usr/bin/env bash
set -euo pipefail

os="$(uname -s)"
arch="$(uname -m)"
bin_dir="${HOME}/.local/bin"

gsc_path="${bin_dir}/gsc-mcp"
ga4_path="${bin_dir}/analytics-mcp"
if [[ ! -x "${gsc_path}" ]]; then
  echo "Missing GSC MCP command: ${gsc_path}" >&2
  echo "Run scripts/install-google-gsc.sh first." >&2
  exit 1
fi
if [[ ! -x "${ga4_path}" ]]; then
  echo "Missing GA4 MCP executable: ${ga4_path}" >&2
  echo "Run the upstream GA4 installer first." >&2
  exit 1
fi

mkdir -p "${bin_dir}"

profile="${HOME}/.profile"
export_line="export PATH=\"${bin_dir}:\$PATH\""
if ! grep -qsF -- "$export_line" "$profile"; then
  printf '%s\n' "$export_line" >> "$profile"
  echo "Added ${bin_dir} to PATH in ${profile}."
fi

echo "Configured Google MCP commands for ${os}/${arch}."
echo "GSC: ${gsc_path}"
echo "GA4: ${ga4_path}"
echo "Restart Codex, Cursor, or VS Code to inherit the updated PATH."

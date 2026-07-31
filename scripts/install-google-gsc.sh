#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$HOME/.local/bin"

asset="${GSC_MCP_RELEASE_ASSET:-}"
if [[ -z "$asset" ]]; then
  case "$(uname -s):$(uname -m)" in
    Linux:x86_64) asset="gsc-mcp-go-linux-amd64";; Linux:aarch64|Linux:arm64) asset="gsc-mcp-go-linux-arm64";;
    Darwin:x86_64) asset="gsc-mcp-go-darwin-amd64";; Darwin:arm64) asset="gsc-mcp-go-darwin-arm64";;
    *) echo "Unsupported platform: $(uname -s)/$(uname -m)" >&2
       echo "Set GSC_MCP_RELEASE_ASSET to a release asset name to override." >&2
       exit 2;;
  esac
fi
case "$asset" in
  */*|*..*) echo "Invalid GSC_MCP_RELEASE_ASSET: $asset" >&2; exit 2;;
esac

sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | awk '{print $1}'
  elif command -v openssl >/dev/null 2>&1; then openssl dgst -sha256 "$1" | awk '{print $NF}'
  else echo "No SHA-256 tool found (sha256sum, shasum, or openssl required)" >&2; return 1
  fi
}

staged="$(mktemp "${TMPDIR:-/tmp}/gsc-mcp.XXXXXX")"
trap 'rm -f "$staged"' EXIT

curl -fsSL "https://github.com/ncosentino/google-search-console-mcp/releases/latest/download/${asset}" -o "$staged"

if [[ -n "${GSC_MCP_SHA256:-}" ]]; then
  actual="$(sha256_of "$staged" | tr 'A-Z' 'a-z')"
  expected="$(printf '%s' "$GSC_MCP_SHA256" | tr 'A-Z' 'a-z')"
  if [[ "$actual" != "$expected" ]]; then
    echo "GSC MCP SHA-256 mismatch (expected ${expected}, got ${actual})" >&2
    echo "Discarded the downloaded file; the installed command was left untouched." >&2
    exit 1
  fi
fi

chmod +x "$staged"
mv -f "$staged" "$HOME/.local/bin/gsc-mcp"
trap - EXIT
echo "GSC MCP ready at $HOME/.local/bin/gsc-mcp"

#!/usr/bin/env bash
set -euo pipefail
secret_root="${CODEX_SECRETS_DIR:-${HOME}/.codex/secrets/google}"
missing=0
for command_name in gsc-mcp analytics-mcp; do
  if command -v "$command_name" >/dev/null 2>&1; then echo "$command_name: OK"; else echo "$command_name: MISSING"; missing=1; fi
done
# Resolve the same paths the MCP servers use, falling back to the default
# secrets directory when the environment variables are not exported.
check_credential() {
  local label="$1" override="$2" path
  path="${override:-${secret_root}/$3}"
  if [[ -f "$path" ]]; then
    echo "${label}: OK (${path})"
  else
    echo "${label}: MISSING (${path})"
    if [[ -z "$override" ]]; then echo "  hint: export ${label} to point at your credential file"; fi
    missing=1
  fi
}
check_credential GOOGLE_SERVICE_ACCOUNT_FILE "${GOOGLE_SERVICE_ACCOUNT_FILE:-}" gsc-service-account.json
check_credential GOOGLE_APPLICATION_CREDENTIALS "${GOOGLE_APPLICATION_CREDENTIALS:-}" ga4-credentials.json
if [[ -n "${GOOGLE_PROJECT_ID:-}" ]]; then echo 'GOOGLE_PROJECT_ID: OK'; else echo 'GOOGLE_PROJECT_ID: MISSING'; missing=1; fi
if [[ "$missing" -ne 0 ]]; then exit 1; fi
echo 'Google MCP installation looks ready.'

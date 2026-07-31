#!/usr/bin/env bash
set -euo pipefail
root="${CODEX_SECRETS_DIR:-${HOME}/.codex/secrets/google}"
python3 - "$root" "${GOOGLE_SERVICE_ACCOUNT_FILE:-}" "${GOOGLE_APPLICATION_CREDENTIALS:-}" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
gsc_override, ga4_override = sys.argv[2], sys.argv[3]

def load(override, name):
    path = pathlib.Path(override) if override else root / name
    if not path.is_file():
        raise SystemExit(f"Missing {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {path}: {error}")

gsc = load(gsc_override, "gsc-service-account.json")
ga4 = load(ga4_override, "ga4-credentials.json")
if not {"client_email", "private_key"} <= gsc.keys():
    raise SystemExit("GSC JSON is missing required keys")
service = ga4.get("type") == "service_account" and {"client_email", "private_key"} <= ga4.keys()
# Console-issued OAuth client files nest the keys under "installed" or "web";
# application default credentials keep them at the top level.
candidates = [ga4] + [ga4[key] for key in ("installed", "web") if isinstance(ga4.get(key), dict)]
oauth = any({"client_id", "client_secret"} <= candidate.keys() for candidate in candidates)
if not (service or oauth):
    raise SystemExit("GA4 JSON is neither service-account nor OAuth client JSON")
print("Google auth files look structurally valid.")
PY

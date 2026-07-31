#!/usr/bin/env python3
"""
Google API credential management for Powehi Universal SEO.

Loads and validates credentials for Google Search Console, PageSpeed Insights,
CrUX, Indexing API, and GA4. Supports service accounts, OAuth web credentials
with token refresh, API keys, and environment variable fallbacks.

Usage:
    python google_auth.py --check                  # Check all credentials
    python google_auth.py --check gsc              # Check specific service
    python google_auth.py --check --json            # JSON output
    python google_auth.py --setup                   # Show setup instructions
    python google_auth.py --tier                    # Show detected credential tier
    python google_auth.py --auth --creds /path/to/client_secret.json  # OAuth browser flow
"""

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import shutil
import sys
import time
from pathlib import Path
from typing import Optional

CONFIG_PATH = os.path.expanduser("~/.config/powehi-seo-geo/google-api.json")
TOKEN_PATH = os.path.expanduser("~/.config/powehi-seo-geo/oauth-token.json")
LEGACY_CONFIG_DIR = Path(os.path.expanduser("~/.config/claude-seo"))


def migrate_legacy_config() -> dict:
    """Copy legacy credential files into the Powehi directory without deleting them."""
    config_dir = Path(CONFIG_PATH).parent
    result = {"migrated": [], "source": str(LEGACY_CONFIG_DIR), "target": str(config_dir)}
    if not LEGACY_CONFIG_DIR.is_dir():
        return result

    config_dir.mkdir(parents=True, exist_ok=True)
    for filename in ("google-api.json", "oauth-token.json"):
        source = LEGACY_CONFIG_DIR / filename
        target = config_dir / filename
        if source.is_file() and not target.exists():
            shutil.copy2(source, target)
            try:
                os.chmod(target, 0o600)
            except OSError:
                pass
            result["migrated"].append(filename)

    marker = config_dir / "migration.json"
    marker.write_text(
        json.dumps(
            {
                "from": "~/.config/claude-seo",
                "to": "~/.config/powehi-seo-geo",
                "status": "completed",
                "files": result["migrated"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return result

# Service-to-scope mapping
SCOPES = {
    "gsc_readonly": "https://www.googleapis.com/auth/webmasters.readonly",
    "gsc_write": "https://www.googleapis.com/auth/webmasters",
    "indexing": "https://www.googleapis.com/auth/indexing",
    "ga4": "https://www.googleapis.com/auth/analytics.readonly",
}

# Which services need which auth type
SERVICE_AUTH = {
    "psi": "api_key",
    "crux": "api_key",
    "crux_history": "api_key",
    "gsc": "oauth_or_sa",
    "indexing": "oauth_or_sa",
    "ga4": "oauth_or_sa",
}

OAUTH_SCOPES = (
    "https://www.googleapis.com/auth/indexing "
    "https://www.googleapis.com/auth/webmasters "
    "https://www.googleapis.com/auth/analytics.readonly"
)
OAUTH_REDIRECT_URI = "http://localhost:8085"
# Applied to every token-endpoint call. Without it urllib blocks forever on a
# blackholed egress path, hanging every Google-API script behind this module.
OAUTH_HTTP_TIMEOUT = 30
# How long run_oauth_flow waits for the browser to hit the local callback.
OAUTH_CALLBACK_TIMEOUT = 300

# Human-readable service names
SERVICE_NAMES = {
    "psi": "PageSpeed Insights v5",
    "crux": "Chrome UX Report (CrUX) API",
    "crux_history": "CrUX History API",
    "gsc": "Google Search Console API",
    "indexing": "Google Indexing API v3",
    "ga4": "GA4 Data API v1beta",
}

_GOOGLE_API_KEY_PREFIX = "AI" + "za"
_GOOGLE_API_KEY_RE = re.compile(_GOOGLE_API_KEY_PREFIX + r"[0-9A-Za-z_-]+")
_GOOGLE_KEY_QUERY_RE = re.compile(r"([?&])key=[^&\s'\"<>)]*(&?)")
_GOOGLE_KEY_BARE_RE = re.compile(r"\bkey=[^&\s'\"<>)]*")


def google_api_key_headers(api_key: str) -> dict:
    """Return the canonical header form for Google API key auth."""
    return {"X-Goog-Api-Key": api_key}


def redact_google_api_key(value: object) -> str:
    """Remove Google API keys from exception/output strings."""
    text = str(value)
    def drop_query_key(match: re.Match) -> str:
        separator, trailing_amp = match.groups()
        if separator == "?" and trailing_amp:
            return "?"
        if separator == "&" and trailing_amp:
            return "&"
        return ""

    text = _GOOGLE_KEY_QUERY_RE.sub(drop_query_key, text)
    text = text.replace("?&", "?")
    text = _GOOGLE_KEY_BARE_RE.sub("google_api_key_redacted", text)
    return _GOOGLE_API_KEY_RE.sub("GOOGLE_API_KEY_REDACTED", text)


def load_config() -> dict:
    """
    Load configuration from config file with environment variable fallbacks.

    Reads ~/.config/powehi-seo-geo/google-api.json first. Any missing fields
    are filled from environment variables.

    Returns:
        Dictionary with keys: service_account_path, api_key,
        default_property, ga4_property_id. Missing values are None.
    """
    migrate_legacy_config()
    config = {
        "service_account_path": None,
        "api_key": None,
        "default_property": None,
        "ga4_property_id": None,
    }

    # Load from config file
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                file_config = json.load(f)
            config.update({k: v for k, v in file_config.items() if v})
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read config file: {e}", file=sys.stderr)

    # Environment variable fallbacks
    if not config["service_account_path"]:
        config["service_account_path"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if not config["api_key"]:
        config["api_key"] = os.environ.get("GOOGLE_API_KEY")

    if not config["ga4_property_id"]:
        config["ga4_property_id"] = os.environ.get("GA4_PROPERTY_ID")

    if not config["default_property"]:
        config["default_property"] = os.environ.get("GSC_PROPERTY")

    return config


def get_service_account_credentials(scopes: list):
    """
    Load Google service account credentials.

    Args:
        scopes: List of OAuth scope URLs.

    Returns:
        google.oauth2.service_account.Credentials object, or None on failure.
    """
    try:
        from google.oauth2 import service_account
    except ImportError:
        print(
            "Error: google-auth library required. "
            "Install with: pip install google-auth",
            file=sys.stderr,
        )
        return None

    config = load_config()
    sa_path = config.get("service_account_path")

    if not sa_path:
        return None

    sa_path = os.path.expanduser(sa_path)
    if not os.path.exists(sa_path):
        print(
            f"Error: Service account file not found: {sa_path}",
            file=sys.stderr,
        )
        return None

    try:
        credentials = service_account.Credentials.from_service_account_file(
            sa_path, scopes=scopes
        )
        return credentials
    except Exception as e:
        print(f"Error loading service account: {e}", file=sys.stderr)
        return None


def _load_oauth_client(creds_path: str) -> Optional[dict]:
    """Load OAuth client credentials from a client_secret JSON file."""
    try:
        with open(creds_path, "r") as f:
            data = json.load(f)
        return data.get("web", data.get("installed", {}))
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading OAuth client file: {e}", file=sys.stderr)
        return None


# Paths already hardened in this process. icacls costs a subprocess spawn, and
# _chmod_quiet runs on every token load, so the result is memoised per run.
_WINDOWS_ACL_APPLIED: set[str] = set()


def _restrict_windows_acl(path: str) -> bool:
    """Replace the inherited DACL on ``path`` with an owner-only ACE.

    ``os.chmod(path, 0o600)`` is a no-op for access control on Windows: it
    only toggles the read-only attribute, leaving the file readable by every
    other local account that inherits rights from the parent directory. This
    helper calls ``icacls`` to break inheritance and grant full control to the
    current user alone.

    Returns True when the ACL was applied, False otherwise (caller decides
    whether to warn).
    """
    if os.name != "nt":
        return False
    if path in _WINDOWS_ACL_APPLIED:
        return True
    import subprocess

    user = os.environ.get("USERNAME")
    if not user:
        return False
    domain = os.environ.get("USERDOMAIN")
    principal = f"{domain}\\{user}" if domain else user
    try:
        result = subprocess.run(
            ["icacls", path, "/inheritance:r", "/grant:r", f"{principal}:(F)"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    if result.returncode == 0:
        _WINDOWS_ACL_APPLIED.add(path)
        return True
    return False


def _chmod_quiet(path: str, mode: int) -> None:
    """Best-effort permission tightening that swallows errors.

    On POSIX this is a plain chmod (used to remediate legacy 0o644 token
    files written by v1.9.x without forcing the user to re-auth). On Windows
    chmod cannot express "owner only", so an ``icacls`` ACL rewrite is
    attempted as well; if it fails the caller is warned rather than left
    believing the file is protected.
    """
    try:
        os.chmod(path, mode)
    except OSError:
        pass
    if os.name == "nt" and mode == 0o600 and not _restrict_windows_acl(path):
        print(
            f"Warning: could not restrict Windows ACL on {path}. "
            f"Other local accounts may be able to read this credential file.",
            file=sys.stderr,
        )


def _load_oauth_token() -> Optional[dict]:
    """Load saved OAuth token from TOKEN_PATH.

    Also remediates legacy file permissions: v1.9.x wrote tokens with the
    umask default (typically 0o644, world-readable). Each load forces the
    file to 0o600 so users upgrading to v2 are protected without a re-auth.
    """
    if not os.path.exists(TOKEN_PATH):
        return None
    _chmod_quiet(TOKEN_PATH, 0o600)
    try:
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _save_oauth_token(token_data: dict):
    """Save OAuth token to TOKEN_PATH with secure (0o600) permissions.

    Belt-and-suspenders sequence:
        1. Pre-chmod any existing file (closes a v1.9.x umask=022 legacy).
        2. ``os.open`` with explicit mode 0o600 (mode applies only to
           newly-created files, ignored when the file already exists).
        3. ``os.fchmod`` on the open fd to *force* 0o600 even if the
           file pre-existed at step 2 — defeats the
           os.path.exists()/os.open() TOCTOU race where an external
           creator could install a 0o644 file between the two calls.
        4. On Windows, an icacls DACL rewrite (chmod cannot express
           "owner only" there); a warning is printed if it fails.

    On POSIX the token file is never world-readable, even briefly.
    """
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    if os.path.exists(TOKEN_PATH):
        _chmod_quiet(TOKEN_PATH, 0o600)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(TOKEN_PATH, flags, 0o600)
    # fchmod on the open fd guarantees 0o600 even if the file existed at
    # open time (in which case os.open's mode arg is ignored by the OS).
    # os.fdopen takes ownership of fd — it closes the fd whether the
    # write succeeds or raises, so there is no fd-leak path here.
    try:
        fchmod = getattr(os, "fchmod", None)
        if fchmod is not None:
            fchmod(fd, 0o600)
    except OSError:
        pass  # FS may not support fchmod (e.g. some Windows filesystems)
    with os.fdopen(fd, "w") as f:
        json.dump(token_data, f, indent=2)
    # Windows: the file may have just been created, so the ACL rewrite has to
    # happen after os.open rather than in the pre-chmod above.
    if os.name == "nt":
        _chmod_quiet(TOKEN_PATH, 0o600)


def _update_config(updates: dict, remove: tuple = ()) -> None:
    """Merge ``updates`` into the user config file and drop ``remove`` keys.

    Atomic: writes a sibling temp file and renames over the target.
    """
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    config = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            config = {}
    config.update(updates)
    for key in remove:
        config.pop(key, None)

    import tempfile
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(CONFIG_PATH), prefix=".google-api.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(config, f, indent=2)
        os.replace(tmp_path, CONFIG_PATH)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
    _chmod_quiet(CONFIG_PATH, 0o600)


def _persist_oauth_client_path(creds_path: str):
    """
    Persist the absolute path to the OAuth client_secret JSON file in the
    user config so future refresh_token flows can locate the client_secret
    without re-prompting. Stores the PATH only; never the secret itself.

    Closes the bug where every OAuth user 401'd within 1 hour because the
    refresh path could not find oauth_client_path in config.
    """
    _update_config({"oauth_client_path": os.path.abspath(os.path.expanduser(creds_path))})


def _new_pkce_pair() -> tuple[str, str]:
    """Return an (code_verifier, code_challenge) PKCE pair using S256."""
    verifier = secrets.token_urlsafe(64)[:128]
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return verifier, challenge


def _persist_oauth_flow_state(verifier: str) -> None:
    """Store the in-flight PKCE verifier so a later ``--exchange`` run (a
    separate process, used when the browser could not reach the local
    callback) can still redeem the code."""
    _update_config({"oauth_pkce_verifier": verifier})


def _read_oauth_flow_state() -> Optional[str]:
    return load_config().get("oauth_pkce_verifier")


def _clear_oauth_flow_state() -> None:
    """Drop the one-shot PKCE verifier once the flow ends, successfully or
    not — a stale verifier must never be reused across flows."""
    try:
        _update_config({}, remove=("oauth_pkce_verifier",))
    except Exception:
        pass


def _refresh_oauth_token(client: dict, token_data: dict) -> Optional[dict]:
    """Refresh an expired OAuth token using the refresh_token."""
    import urllib.parse
    import urllib.request

    if not token_data.get("refresh_token"):
        return None

    params = urllib.parse.urlencode({
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "refresh_token": token_data["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()

    try:
        req = urllib.request.Request(client.get("token_uri", "https://oauth2.googleapis.com/token"), data=params)
        with urllib.request.urlopen(req, timeout=OAUTH_HTTP_TIMEOUT) as resp:
            new_data = json.loads(resp.read())
        token_data["access_token"] = new_data["access_token"]
        token_data["expires_at"] = time.time() + new_data.get("expires_in", 3600)
        _save_oauth_token(token_data)
        return token_data
    except Exception as e:
        print(f"Error refreshing OAuth token: {e}", file=sys.stderr)
        return None


def get_oauth_credentials(scopes: list):
    """
    Get OAuth credentials from saved token, refreshing if needed.

    Falls back to service account if no OAuth token is available.

    Args:
        scopes: List of OAuth scope URLs (used for service account fallback).

    Returns:
        google.oauth2.credentials.Credentials or service_account.Credentials, or None.
    """
    config = load_config()

    # Try OAuth token first
    token_data = _load_oauth_token()
    if token_data and token_data.get("access_token"):
        # Check if token needs refresh
        if time.time() > token_data.get("expires_at", 0) - 60:
            oauth_creds_path = config.get("oauth_client_path")
            client = (
                _load_oauth_client(os.path.expanduser(oauth_creds_path))
                if oauth_creds_path
                else None
            )
            if client:
                token_data = _refresh_oauth_token(client, token_data)
                if not token_data:
                    print("OAuth token refresh failed. Re-run --auth.", file=sys.stderr)
                    return get_service_account_credentials(scopes)
            else:
                # Without the client file we cannot refresh. Falling through
                # would hand back the known-expired access token and every
                # caller would fail with an opaque HTTP 401 instead of an
                # actionable message.
                print(
                    "OAuth token expired and 'oauth_client_path' is not set in "
                    f"{CONFIG_PATH}. Re-run: python scripts/google_auth.py "
                    "--auth --creds /path/to/client_secret.json",
                    file=sys.stderr,
                )
                return get_service_account_credentials(scopes)

        if token_data and token_data.get("access_token"):
            try:
                from google.oauth2.credentials import Credentials
                # Read client_secret from client file, never from stored token
                client_secret = None
                oauth_path = config.get("oauth_client_path")
                if oauth_path:
                    client_data = _load_oauth_client(os.path.expanduser(oauth_path))
                    if client_data:
                        client_secret = client_data.get("client_secret")
                return Credentials(
                    token=token_data["access_token"],
                    refresh_token=token_data.get("refresh_token"),
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=token_data.get("client_id"),
                    client_secret=client_secret,
                )
            except ImportError:
                print("Error: google-auth required. Install with: pip install google-auth", file=sys.stderr)

    # Fall back to service account
    return get_service_account_credentials(scopes)


def run_oauth_flow(creds_path: str):
    """
    Run OAuth browser-based authentication flow.

    Opens a browser for consent, captures the auth code via local HTTP server,
    exchanges for tokens, and saves them.

    Args:
        creds_path: Path to the OAuth client_secret JSON file.
    """
    import http.server
    import urllib.parse
    import urllib.request
    import webbrowser

    client = _load_oauth_client(creds_path)
    if not client:
        print("Error: Could not load OAuth client credentials.", file=sys.stderr)
        sys.exit(1)

    # CSRF defence. Without `state`, any page the user visits while this
    # server is listening can navigate to
    # http://localhost:8085/?code=<attacker_code>; we would exchange it and
    # bind this install to the attacker's Google account. The callback below
    # refuses any request whose state does not match.
    state = secrets.token_urlsafe(32)
    # PKCE (RFC 7636). Google requires it for installed-app clients and it
    # stops an intercepted authorization code from being redeemed elsewhere.
    verifier, challenge = _new_pkce_pair()
    _persist_oauth_flow_state(verifier)

    auth_url = (
        f"{client.get('auth_uri', 'https://accounts.google.com/o/oauth2/auth')}"
        f"?client_id={urllib.parse.quote(client['client_id'])}"
        f"&redirect_uri={urllib.parse.quote(OAUTH_REDIRECT_URI)}"
        f"&response_type=code"
        f"&scope={urllib.parse.quote(OAUTH_SCOPES)}"
        f"&state={urllib.parse.quote(state)}"
        f"&code_challenge={urllib.parse.quote(challenge)}"
        f"&code_challenge_method=S256"
        f"&access_type=offline&prompt=consent"
    )

    auth_code = [None]
    callback_error = [None]

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "error" in params:
                callback_error[0] = params["error"][0]
                self.send_response(400)
                self.end_headers()
                return
            if "code" not in params:
                # Favicon probes, port scanners, stray reloads. Answer and
                # keep listening — this must not end the flow.
                self.send_response(404)
                self.end_headers()
                return
            if not secrets.compare_digest(params.get("state", [""])[0], state):
                callback_error[0] = "state mismatch (possible CSRF attempt); code refused"
                self.send_response(400)
                self.end_headers()
                return
            auth_code[0] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Authentication successful!</h1><p>Close this tab.</p>")

        def log_message(self, *a):
            pass

    server = http.server.HTTPServer(("localhost", 8085), Handler)
    # Bound per-request; the deadline loop below owns the overall timeout.
    server.timeout = 5

    print(f"\nOpen this URL in your browser:\n\n{auth_url}\n")
    print(f"Waiting up to {OAUTH_CALLBACK_TIMEOUT // 60} minutes for authentication...")

    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    # Serve until the real callback arrives. A single handle_request() would
    # be consumed by the first favicon probe or error redirect, failing the
    # flow before the browser ever delivered the code.
    deadline = time.time() + OAUTH_CALLBACK_TIMEOUT
    while auth_code[0] is None and callback_error[0] is None and time.time() < deadline:
        server.handle_request()
    server.server_close()

    if callback_error[0]:
        _clear_oauth_flow_state()
        print(f"\nAuthentication failed: {callback_error[0]}", file=sys.stderr)
        sys.exit(1)

    if not auth_code[0]:
        print("\nAuthentication failed or timed out.", file=sys.stderr)
        print("If the browser showed 'localhost refused to connect', copy the full URL")
        print("from the browser address bar and run:")
        print(f"  python scripts/google_auth.py --exchange --creds {creds_path} --code 'THE_CODE'")
        sys.exit(1)

    # Exchange code for tokens
    _exchange_code(client, auth_code[0], creds_path)


def _exchange_code(client: dict, code: str, creds_path: Optional[str] = None):
    """Exchange an authorization code for tokens.

    If creds_path is provided, persist its absolute path to the user config
    as 'oauth_client_path' so subsequent refresh flows can locate the
    client_secret file without re-prompting.
    """
    import urllib.parse
    import urllib.request

    form = {
        "code": code,
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "redirect_uri": OAUTH_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    # The authorization request carried a PKCE challenge, so the token
    # request must carry the matching verifier. It is persisted in the user
    # config precisely so the manual `--exchange` fallback (a separate
    # process) can still complete the flow.
    verifier = _read_oauth_flow_state()
    if verifier:
        form["code_verifier"] = verifier
    params = urllib.parse.urlencode(form).encode()

    try:
        req = urllib.request.Request(
            client.get("token_uri", "https://oauth2.googleapis.com/token"), data=params
        )
        with urllib.request.urlopen(req, timeout=OAUTH_HTTP_TIMEOUT) as resp:
            token_data = json.loads(resp.read())
        token_data["expires_at"] = time.time() + token_data.get("expires_in", 3600)
        token_data["client_id"] = client["client_id"]
        # SECURITY: Never store client_secret in token file. It stays in client_secret.json only.
        token_data.pop("client_secret", None)
        _save_oauth_token(token_data)
        # One-shot: the verifier must not survive to a later flow.
        _clear_oauth_flow_state()
        print("OAuth token saved successfully!")

        # Persist oauth_client_path so refresh works after process restart.
        # This is the PATH, never the client_secret value itself.
        if creds_path:
            try:
                _persist_oauth_client_path(creds_path)
                print(f"OAuth client path persisted to {CONFIG_PATH}")
            except Exception as e:
                print(
                    f"Warning: Could not persist oauth_client_path: {e}. "
                    f"Add 'oauth_client_path' to {CONFIG_PATH} manually for "
                    f"automatic token refresh.",
                    file=sys.stderr,
                )

        print(f"\nToken saved to: {TOKEN_PATH}")
    except Exception as e:
        _clear_oauth_flow_state()
        print(f"Error exchanging authorization code: {e}", file=sys.stderr)
        sys.exit(1)


def validate_url(url: str) -> bool:
    """
    Validate a URL for use with Google APIs. Rejects private/loopback addresses.

    Args:
        url: URL string to validate.

    Returns:
        True if the URL is a valid public http/https URL, False otherwise.

    Note:
        Back-compat wrapper around :func:`url_safety.validate_url`. The shared
        module is the canonical implementation and adds DNS-rebinding-safe
        helpers (``validate_url_strict``, ``safe_requests_get``) that
        ``fetch_page.py`` and ``render_page.py`` use before opening sockets.
    """
    # Lazy import: avoids a hard requirement on url_safety for callers that
    # only need google_auth's other helpers (e.g. token refresh) and keeps
    # the import graph one-directional.
    _scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if _scripts_dir not in sys.path:
        sys.path.insert(0, _scripts_dir)
    from url_safety import validate_url as _validate_url

    return _validate_url(url)


def get_api_key() -> Optional[str]:
    """
    Get the Google API key from config or environment.

    Returns:
        API key string, or None if not configured.
    """
    config = load_config()
    return config.get("api_key")


def build_service(api_name: str, version: str, scopes: list):
    """
    Build a Google API discovery service client.

    Args:
        api_name: API name (e.g., 'searchconsole', 'indexing', 'pagespeedonline').
        version: API version (e.g., 'v1', 'v3', 'v5').
        scopes: OAuth scopes needed.

    Returns:
        googleapiclient.discovery.Resource object, or None on failure.
    """
    try:
        from googleapiclient.discovery import build
    except ImportError:
        print(
            "Error: google-api-python-client required. "
            "Install with: pip install google-api-python-client",
            file=sys.stderr,
        )
        return None

    credentials = get_oauth_credentials(scopes)
    if not credentials:
        return None

    try:
        service = build(api_name, version, credentials=credentials)
        return service
    except Exception as e:
        print(f"Error building {api_name} service: {e}", file=sys.stderr)
        return None


def check_credentials(service: str) -> dict:
    """
    Validate credentials for a specific Google API service.

    Args:
        service: One of 'psi', 'crux', 'crux_history', 'gsc', 'indexing', 'ga4'.

    Returns:
        Dictionary with:
            - available: bool
            - method: 'api_key' or 'service_account'
            - service: service name
            - error: error message or None
    """
    result = {
        "available": False,
        "method": SERVICE_AUTH.get(service, "unknown"),
        "service": SERVICE_NAMES.get(service, service),
        "error": None,
    }

    config = load_config()

    if SERVICE_AUTH.get(service) == "api_key":
        api_key = config.get("api_key")
        if api_key:
            result["available"] = True
        else:
            result["error"] = (
                "No API key found. Set GOOGLE_API_KEY environment variable "
                f"or add 'api_key' to {CONFIG_PATH}"
            )

    elif SERVICE_AUTH.get(service) == "oauth_or_sa":
        # Check OAuth token first
        token_data = _load_oauth_token()
        if token_data and token_data.get("access_token"):
            result["available"] = True
            result["method"] = "oauth_token"
            expired = time.time() > token_data.get("expires_at", 0) - 60
            if expired and token_data.get("refresh_token"):
                result["note"] = "Token expired but refresh_token available (will auto-refresh)"
            elif expired:
                result["available"] = False
                result["error"] = "OAuth token expired and no refresh_token. Re-run --auth."
        else:
            # Fall back to service account
            sa_path = config.get("service_account_path")
            if not sa_path:
                result["error"] = (
                    "No OAuth token or service account found. Either:\n"
                    "         1. Run: python scripts/google_auth.py --auth --creds /path/to/client_secret.json\n"
                    f"         2. Or add 'service_account_path' to {CONFIG_PATH}"
                )
            else:
                sa_path = os.path.expanduser(sa_path)
                if not os.path.exists(sa_path):
                    result["error"] = f"Service account file not found: {sa_path}"
                else:
                    try:
                        with open(sa_path, "r") as f:
                            sa_data = json.load(f)
                        if "client_email" not in sa_data or "private_key" not in sa_data:
                            result["error"] = "Service account JSON missing required fields (client_email, private_key)"
                        else:
                            result["available"] = True
                            result["method"] = "service_account"
                            result["client_email"] = sa_data.get("client_email")
                    except (json.JSONDecodeError, IOError) as e:
                        result["error"] = f"Invalid service account file: {e}"

        # GA4 also needs property ID
        if service == "ga4" and result["available"]:
            ga4_id = config.get("ga4_property_id")
            if not ga4_id:
                result["available"] = False
                result["error"] = (
                    "Credentials found but no GA4 property ID configured. "
                    f"Set GA4_PROPERTY_ID or add 'ga4_property_id' to {CONFIG_PATH}"
                )
    else:
        result["error"] = f"Unknown service: {service}"

    return result


def detect_tier() -> dict:
    """
    Detect the credential tier available.

    Returns:
        Dictionary with:
            - tier: 0, 1, or 2
            - description: human-readable tier description
            - capabilities: list of available API groups
            - missing: what's needed for the next tier
    """
    config = load_config()

    has_api_key = bool(config.get("api_key"))
    has_authenticated = False
    has_ga4 = False
    auth_method = None

    # Check OAuth token
    token_data = _load_oauth_token()
    if token_data and token_data.get("access_token"):
        has_authenticated = True
        auth_method = "oauth_token"

    # Check service account
    if not has_authenticated:
        sa_path = config.get("service_account_path")
        if sa_path:
            sa_path = os.path.expanduser(sa_path)
            if os.path.exists(sa_path):
                try:
                    with open(sa_path, "r") as f:
                        sa_data = json.load(f)
                    if "client_email" in sa_data and "private_key" in sa_data:
                        has_authenticated = True
                        auth_method = "service_account"
                except (json.JSONDecodeError, IOError):
                    pass

    if has_authenticated and config.get("ga4_property_id"):
        has_ga4 = True

    if has_ga4:
        return {
            "tier": 2,
            "description": "Full (API key + Service Account + GA4)",
            "capabilities": [
                "PageSpeed Insights", "CrUX", "CrUX History",
                "Search Console", "URL Inspection", "Sitemaps",
                "Indexing API", "GA4 Organic Traffic",
            ],
            "missing": None,
        }
    elif has_authenticated:
        return {
            "tier": 1,
            "description": "Authenticated (API key + OAuth/Service Account)",
            "capabilities": [
                "PageSpeed Insights", "CrUX", "CrUX History",
                "Search Console", "URL Inspection", "Sitemaps",
                "Indexing API",
            ],
            "missing": "Add 'ga4_property_id' to unlock GA4 organic traffic reports",
        }
    elif has_api_key:
        return {
            "tier": 0,
            "description": "API Key Only",
            "capabilities": [
                "PageSpeed Insights", "CrUX", "CrUX History",
            ],
            "missing": "Add a service account to unlock Search Console, URL Inspection, and Indexing API",
        }
    else:
        return {
            "tier": -1,
            "description": "No credentials configured",
            "capabilities": [],
            "missing": (
                f"Create config at {CONFIG_PATH} with at minimum an 'api_key' field. "
                "Run with --setup for full instructions."
            ),
        }


def print_setup_instructions():
    """Print step-by-step setup instructions."""
    print("""
Google SEO API Setup Instructions
=================================

1. CREATE A GOOGLE CLOUD PROJECT
   - Go to https://console.cloud.google.com
   - Create a new project (or select existing)
   - Note the project ID

2. ENABLE APIs
   In API Library (APIs & Services > Library), enable:
   - Google Search Console API
   - PageSpeed Insights API
   - Chrome UX Report API
   - Web Search Indexing API (for Indexing API)
   - Google Analytics Data API (for GA4)

3. CREATE AN API KEY (for PSI, CrUX -- free, no service account needed)
   - APIs & Services > Credentials > Create Credentials > API key
   - Restrict to: PageSpeed Insights API, Chrome UX Report API

4. CREATE A SERVICE ACCOUNT (for GSC, Indexing API, GA4)
   - IAM & Admin > Service Accounts > Create Service Account
   - Download JSON key file, store securely

5. GRANT ACCESS
   - Search Console: Settings > Users and permissions > Add user
     Paste the service account client_email, set as Owner (for Indexing API) or Full (read-only)
   - GA4: Admin > Property Access Management > Add
     Paste email, set Viewer role

6. CREATE CONFIG FILE
   mkdir -p ~/.config/powehi-seo-geo
   Save to ~/.config/powehi-seo-geo/google-api.json:

   {
     "service_account_path": "/path/to/service_account.json",
     "api_key": "<GOOGLE_API_KEY>",
     "default_property": "sc-domain:example.com",
     "ga4_property_id": "properties/123456789"
   }

7. VERIFY
   python scripts/google_auth.py --check

ENVIRONMENT VARIABLE ALTERNATIVES:
   GOOGLE_API_KEY              - API key
   GOOGLE_APPLICATION_CREDENTIALS - Path to service account JSON
   GA4_PROPERTY_ID             - GA4 property ID (e.g., properties/123456789)
   GSC_PROPERTY                - Default Search Console property
""")


def main():
    parser = argparse.ArgumentParser(
        description="Google API credential management for Powehi Universal SEO"
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const="all",
        metavar="SERVICE",
        help="Check credentials. Optionally specify service: psi, crux, gsc, indexing, ga4",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Show setup instructions",
    )
    parser.add_argument(
        "--tier",
        action="store_true",
        help="Show detected credential tier",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "--auth",
        action="store_true",
        help="Run OAuth browser-based authentication flow",
    )
    parser.add_argument(
        "--exchange",
        action="store_true",
        help="Manually exchange an auth code for tokens",
    )
    parser.add_argument(
        "--creds",
        help="Path to OAuth client_secret JSON file (for --auth and --exchange)",
    )
    parser.add_argument(
        "--code",
        help="Authorization code to exchange (for --exchange)",
    )

    args = parser.parse_args()

    if args.auth:
        if not args.creds:
            print("Error: --creds is required with --auth", file=sys.stderr)
            sys.exit(1)
        run_oauth_flow(args.creds)
        return

    if args.exchange:
        if not args.creds or not args.code:
            print("Error: --creds and --code are required with --exchange", file=sys.stderr)
            sys.exit(1)
        client = _load_oauth_client(args.creds)
        if client:
            _exchange_code(client, args.code, args.creds)
        return

    if args.setup:
        print_setup_instructions()
        return

    if args.tier:
        tier_info = detect_tier()
        if args.json:
            print(json.dumps(tier_info, indent=2))
        else:
            print(f"Credential Tier: {tier_info['tier']} -- {tier_info['description']}")
            if tier_info["capabilities"]:
                print(f"Available APIs: {', '.join(tier_info['capabilities'])}")
            if tier_info["missing"]:
                print(f"Next tier: {tier_info['missing']}")
        return

    if args.check:
        services = (
            list(SERVICE_AUTH.keys())
            if args.check == "all"
            else [args.check]
        )

        results = {}
        for svc in services:
            if svc not in SERVICE_AUTH:
                results[svc] = {"available": False, "error": f"Unknown service: {svc}"}
                continue
            results[svc] = check_credentials(svc)

        if args.json:
            tier_info = detect_tier()
            output = {"tier": tier_info, "services": results}
            print(json.dumps(output, indent=2))
        else:
            tier_info = detect_tier()
            print(f"Credential Tier: {tier_info['tier']} -- {tier_info['description']}")
            print()
            for svc, result in results.items():
                status = "OK" if result["available"] else "MISSING"
                print(f"  [{status}] {result.get('service', svc)}")
                if result.get("error"):
                    print(f"         {result['error']}")
                if result.get("client_email"):
                    print(f"         Service account: {result['client_email']}")
            print()
            if tier_info["missing"]:
                print(f"Tip: {tier_info['missing']}")
        return

    # Default: show tier
    tier_info = detect_tier()
    if args.json:
        print(json.dumps(tier_info, indent=2))
    else:
        print(f"Credential Tier: {tier_info['tier']} -- {tier_info['description']}")
        if tier_info["missing"]:
            print(f"Run --setup for configuration instructions.")


if __name__ == "__main__":
    main()

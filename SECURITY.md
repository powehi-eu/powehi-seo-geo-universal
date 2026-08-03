> **Languages:** [Français](SECURITY.fr.md) | English

# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly. Do **not** open a public issue.

1. Open a private [GitHub Security Advisory](https://github.com/powehi-eu/powehi-seo-geo-universal/security/advisories/new) on this repository (preferred channel).
2. As a fallback, email the maintainer at the address listed in [`CITATION.cff`](CITATION.cff).
3. Encrypt sensitive disclosures if you can. Request the maintainer's PGP key in the advisory or email — the key fingerprint is published in advisory threads on first request and is rotated yearly.

When reporting, please include:

- A short description of the issue and the impact you believe it has.
- A minimal reproducer (URL, command line, payload, or short script).
- Affected versions and platforms.
- Whether you have a suggested fix.

## Coordinated disclosure

powehi-seo-geo follows a **90-day coordinated disclosure** policy.

| Day | Event |
|---:|---|
| 0  | Maintainer acknowledges receipt. |
| ≤ 3   | Initial triage: severity classification (CVSS v3.1) and reproducibility confirmation. |
| ≤ 14  | Mitigation or fix candidate proposed. |
| ≤ 30  | Fix released in a patch version or backport; reporter credited in the release notes (opt-out available). |
| ≤ 90  | Public advisory published if not earlier. |

If a fix cannot be shipped within 90 days, the maintainer will request an extension with a clear technical reason. The reporter retains the right to disclose at the 90-day mark.

## Supported versions

| Version line | Status | Notes |
|---|---|---|
| **2.x** | ✅ Fully supported | Active development; security and bug fixes. |
| **1.9.x** | ✅ Patch-only for security | Final 1.x line; only CVSS ≥ High issues backported. |
| < 1.9 | ❌ Unsupported | Please upgrade. |

## Threat model

powehi-seo-geo is a research and audit toolkit that runs on a user's workstation. It accepts user-supplied URLs and credentials, and issues HTTP requests against arbitrary internet hosts. The threat model has three primary attacker types:

1. **Malicious audit target.** A site the user points powehi-seo-geo at attempts to leak local-network or cloud-metadata data via SSRF chains: private IP literals, decimal/hex/octal IPv4, FQDN trailing dot, 30x redirects to private IPs, DNS rebinding (initial public resolution → later private), IPv4-mapped IPv6, dual-stack hosts with one private record.

   **Mitigation:** `scripts/url_safety.py` is the canonical pre-flight + DNS-pinned fetch layer. Every URL-fetching script in this repository validates through it. See `tests/test_url_safety.py` for the regression suite (91 cases across 31 test functions, covering each bypass class).

2. **Tampered install.** A modified plugin install, GitHub release, or manual install script could deliver altered files. Plugin install is the default path; `curl ... | bash` is the legacy/manual path, so signature verification of release artifacts remains a defence-in-depth concern.

   **Mitigation status:** SHA-256 manifest tooling shipped in v2.0.0; install script verification is tracked for v2.3. Until install scripts verify manifests, users may install by cloning the tag explicitly and inspecting the diff against the previous release.

3. **Local privilege escalation against stored credentials.** The OAuth token at `~/.config/powehi-seo-geo/oauth-token.json` is the most sensitive on-disk artifact.

   **Mitigation:** v2 forces `0o600` on every write (`os.open` + `os.fchmod`) and remediates legacy `0o644` files in place on first load. Tokens never contain the OAuth `client_secret` — only the access/refresh pair plus expiry metadata.

4. **Hostile environment against the hook launcher.** `hooks/run-python-hook.js` resolves a Python interpreter and runs the plugin's schema-validation hook. A poisoned `POWEHI_SEO_GEO_PYTHON`, or an attacker-supplied script path, would otherwise turn it into a general-purpose program launcher.

   **Mitigation:** the interpreter list is a frozen module-level constant (`PYTHON_ALLOWLIST`). The environment override is accepted only as an absolute path to an existing file whose basename matches `python[0-9.]*(.exe)?` and contains no shell metacharacters; otherwise it is ignored and the normal probe order applies. The hook script must resolve to an existing `.py` file inside the launcher's own `hooks/` directory. No inline `-c` code string is ever passed — version probing executes the committed `hooks/python-probe.py` file, so every element of both argument vectors is a frozen constant or a validated path. Both `spawnSync` calls pass `shell: false` and an argument vector; no shell is ever involved. Full contract: `hooks/README.md`. Regressions: `tests/test_cross_platform_hooks.py`.

## Known residual risks

- **Playwright + Chromium DNS rebinding.** Chromium does its own DNS resolution inside the renderer process. powehi-seo-geo's Python-layer DNS pin (`url_safety._pin_dns`) cannot reach it. The Playwright `route()` handler re-validates every subresource host (`make_safe_playwright_route_handler`), which closes the common case, but a true rebinding attacker can still race Chromium's resolver after our pre-flight returns. Mitigation: do not point `/powehi-seo` skills at untrusted sites with high-frequency redirects.
- **IPv6-only audit targets.** The strict validator queries `family=AF_INET` for the initial resolution. Hosts with AAAA records only will surface as "DNS resolution failed". This is **fail-closed** by design — we'd rather refuse than connect to an unvalidated IPv6 endpoint. Tracked for a future patch (full dual-stack pinning, similar to the Playwright handler which already uses `AF_UNSPEC`).
- **Windows file permissions.** `os.fchmod(fd, 0o600)` is a no-op on Windows for non-ACL filesystems. Users on Windows should rely on per-user directory ACLs instead of POSIX mode bits.
- **Extension credentials in `~/.claude/settings.json`.** MCP servers receive their credentials through the harness `env` block, so extension API keys are necessarily stored there in plaintext. Installers write the file atomically at `0600` and pass secrets via `argv` (never interpolated into a script body), and every credential prompt now states the exposure before reading a value — but any process running as the user, and any backup or sync tool covering the home directory, can still read it. Treat a key handled this way as revocable-on-demand: revocation at the provider is the only complete remedy for a leak. Tracked for a future patch (OS keychain integration where a harness-supported indirection exists).

## Security-relevant code paths

If you are auditing, these are the high-leverage files:

| File | Purpose |
|---|---|
| `scripts/url_safety.py` | SSRF / DNS-rebinding canonical module. |
| `scripts/render_page.py` | Shared headless renderer (Playwright + trafilatura). |
| `scripts/fetch_page.py` | Raw-HTTP fetcher built on `url_safety.safe_requests_session`. |
| `scripts/capture_screenshot.py` | Playwright screenshot capture with safe route handler. |
| `scripts/google_auth.py` | OAuth token lifecycle, `chmod 0o600` writes. |
| `scripts/backlinks_auth.py` | Backlink-API credential loading; SSRF guard via `url_safety`. |
| `tests/test_url_safety.py` | 91-case regression battery covering every bypass class. |
| `hooks/run-python-hook.js` | Hook launcher: interpreter allowlist, override validation, hook-path containment. |
| `hooks/README.md` | Subprocess safety contract for the hook launcher. |
| `install.sh` / `install.ps1` | Install-ownership manifest generation. |
| `uninstall.sh` / `uninstall.ps1` | Manifest-scoped deletion; confirmation gate for legacy installs. |

## What this policy does **not** cover

- Bugs that require attacker control of the user's machine (any local attacker is already game over).
- Vulnerabilities in upstream dependencies — please report those to their respective maintainers. We track CVEs in `requirements.txt` and bump pins under the `deps:` Dependabot stream.
- Quality-of-output issues (SEO recommendations, schema errors, etc.) — those are bugs, not security issues.

## Security-relevant practices

- No credentials or API keys are committed to this repository. `.gitignore` blocks every known credential filename pattern.
- Install scripts write only to user-level directories under `~/.claude/` and `~/.config/powehi-seo-geo/`.
- Python dependencies install into an isolated virtual environment. Plugin installs use persistent `CLAUDE_PLUGIN_DATA`; manual installs use `~/.claude/skills/powehi-seo/.venv/`. The runtime never falls back to global or user package installation.
- Every new fetcher must route through `scripts/url_safety.py` — there is no exception for "trusted" URLs.
- Skills and subagents follow the **Data Handling Rules** in `skills/powehi-seo/SKILL.md`: no submission of non-public URLs to third-party APIs, explicit per-use confirmation for indexing and publishing side effects, screenshot capture limited to URLs the user named, and no file writes outside a user-specified path.
- Uninstallers delete only paths recorded in the install manifest (`~/.claude/skills/powehi-seo/.install-manifest`). Pre-manifest installs fall back to `seo-*` enumeration but print the full candidate list and require explicit confirmation; a non-interactive shell exits instead of guessing.
- Issue templates carry a redaction notice. Issues are public and indexed: a credential posted there must be revoked and rotated, since deleting the issue does not un-publish it.

## Audit history

| Date | Auditor | Scope | Response |
|---|---|---|---|
| 2026-08-01 | ClawHub automated security audit | Plugin v2.2.9, full repository | [docs/SECURITY-AUDIT-RESPONSE.md](docs/SECURITY-AUDIT-RESPONSE.md) |
| 2026-08-03 | ClawHub automated security audit (re-run) | Plugin v2.2.10, full repository | [Follow-up section](docs/SECURITY-AUDIT-RESPONSE.md#follow-up-2210-re-audit) |

The response document records, per finding, whether it was fixed or classified as a scanner false positive with the reasoning.

> **Languages:** [Français](SECURITY-AUDIT-RESPONSE.fr.md) | English

# Security Audit Response

Response to the ClawHub security audits of Powehi Universal SEO:

| Audit date | Audited version | Section |
|---|---|---|
| 2026-08-01 | 2.2.9 | Everything below, up to the follow-up |
| 2026-08-03 | 2.2.10 | [Follow-up: 2.2.10 re-audit](#follow-up-2210-re-audit) |

Findings are grouped by outcome: **fixed** (code or docs changed), or
**not a vulnerability** (scanner pattern match with a documented reason).

---

## Fixed

### Overly broad uninstaller (High)

`uninstall.sh` and `uninstall.ps1` deleted every `~/.claude/skills/seo-*`
directory and every `~/.claude/agents/seo-*.md` file. Any third-party skill
using the same naming prefix was removed with no warning.

**Fix.** `install.sh` and `install.ps1` now write an ownership manifest to
`~/.claude/skills/powehi-seo/.install-manifest`, listing every skill directory
and agent file the installer created. The uninstallers delete only manifest
entries, and reject any entry containing a path separator or `..`.

Installs that predate the manifest fall back to the old enumeration, but now
print the full candidate list and require an interactive `y` confirmation
(or `--force` / `-Force`). Without confirmation, nothing is deleted, and in a
non-interactive shell the uninstaller exits rather than guessing.

### Safety filter bypass instructions (High)

`skills/seo-image-gen/references/prompt-engineering.md` (and its
`extensions/banana/` mirror) documented rephrasing strategies for getting
blocked prompts past Gemini's safety filters, with worked examples covering
violence, gore, minors in risky contexts, NSFW content, and celebrity
likenesses.

**Fix.** That section was replaced with "When a Safety Filter Blocks a Prompt".
The retained guidance covers only false positives on genuinely benign marketing
imagery, and caps retries at one. The categories above are now an explicit
do-not-attempt list, with the instruction to report the block and stop rather
than iterate on wording. `gemini-models.md` and `SKILL.md` error tables were
updated to match.

### Credential persistence without disclosure (High / Medium)

Extension installers write API credentials into `~/.claude/settings.json`.
The DataForSEO installer already wrote atomically at mode `0600` and passed
credentials via `argv`, but no installer told the user that the value is stored
in plaintext.

**Fix.** Every credential prompt across all extension installers (DataForSEO,
Firecrawl, Ahrefs, SE Ranking, Profound, Bing Webmaster, Banana; `.sh` and
`.ps1`) now prints a storage notice before reading the value: where the value
is stored, that it is plaintext, who can read it, and that the user should use
credentials they can revoke at the provider.

Note that this remains a real exposure, not merely an undisclosed one:
`settings.json` is readable by any process running as the user, and by any
backup or sync tool covering the home directory. Revocation at the provider is
the only complete remedy for a leaked key.

### Shell command execution in the hook launcher (Critical, partially valid)

`hooks/run-python-hook.js` uses `spawnSync` to locate a Python interpreter and
run the schema-validation hook. It never used a shell, so there was no command
injection. Two hardening gaps were real:

1. `POWEHI_SEO_GEO_PYTHON` was accepted verbatim as the executable, so a
   poisoned environment could point hook execution at an arbitrary program.
2. The hook script path was taken from `argv` with no constraint.

**Fix.** The environment override is now accepted only when it is an absolute
path to an existing file whose basename matches `python[0-9.]*(.exe)?` and
contains no shell metacharacters; otherwise it is ignored with a message on
stderr and the normal probe order is used. The hook script must resolve to an
existing `.py` file inside the launcher's own `hooks/` directory. Both
`spawnSync` calls now pass `shell: false` explicitly.

Regression tests: `tests/test_cross_platform_hooks.py` covers the containment
check and the override rejection.

### Undocumented data-handling behavior (Medium, several findings)

The audit flagged leaking private or authenticated URLs to external services,
screenshot capture of authenticated pages, indexing submissions without a
safety boundary, and silent file writes.

**Fix.** `skills/powehi-seo/SKILL.md` gained a **Data Handling Rules** section
binding on every sub-skill and subagent, covering: no submission of non-public
URLs (localhost, private IPs, internal hostnames, staging subdomains, or URLs
carrying tokens or session ids) to any third-party API; explicit per-use
confirmation for IndexNow, the Google Indexing API, and any publish step;
screenshot capture restricted to URLs the user named, with a warning before
capturing anything behind a login; and no writes outside a user-specified path.

Network-level enforcement was already in place: `scripts/url_safety.py`
(`validate_url_strict()` plus DNS-pinned request helpers) blocks private IPs,
loopback, cloud metadata endpoints, and redirect/DNS rebinding, and every
script that fetches a user-supplied URL routes through it.

### Issue templates lacking redaction warnings (Medium)

**Fix.** All three GitHub issue templates (`bug_report.yml`,
`feature_request.yml`, `task.yml`) now carry a redaction notice, and the
"Full error output" field description repeats it. The notice states that issues
are public and indexed, and that an already-published credential must be
revoked and rotated -- deleting the issue does not un-publish it.

---

## Not a vulnerability

### `spawnSync` presence itself (Critical)

The launcher must start a Python interpreter -- that is its entire purpose, and
removing the call means removing hook support. The call was already shell-free
with an argument vector. See the hardening applied above and in the v2.2.11
follow-up below for the parts of this finding that were actionable.

---

## Also fixed in passing

Not audit findings, but real defects found while working through the report:

- `install.ps1` looked for the orchestrator skill at `skills\seo`; the
  repository directory is `skills\powehi-seo`. The Windows manual install would
  fail with "Could not find skill source folder in repo clone."
- `uninstall.ps1` and five extension installers (`ahrefs`, `bing-webmaster`,
  `profound`, `seranking`, `unlighthouse`) checked for the same wrong
  `skills\seo` path, so extension installs on Windows would refuse to run
  against a correct base install.

---

## Follow-up: 2.2.10 re-audit

The 2026-08-03 re-audit of v2.2.10 reported four Critical findings: the same
`spawnSync` call and the same three `exec_module()` call sites. The 2.2.9
response had classified all four as false positives with reasoning. They were
addressed structurally in v2.2.11 instead, so the pattern no longer appears.

### Dynamic code execution in tests (3 instances) -- removed

- `tests/test_banana_api_key_safety.py`
- `tests/test_runtime.py`
- `tests/test_sync_flow.py`

These used `importlib.util.spec_from_file_location()` plus
`spec.loader.exec_module()` to load repository scripts that are not packaged as
importable modules. The reasoning for why this was never exploitable still
holds -- constant paths derived from `__file__`, repository source the test
process could execute anyway, and a `tests/` directory that is never shipped to
users -- but "not exploitable" is a weaker position than "not present".

**Change.** `tests/conftest.py` puts `scripts/` and
`extensions/banana/scripts/` on `sys.path`, and the three test modules now use
ordinary `import` statements (`import runtime`, `import sync_flow`,
`import generate as banana_generate`, `import edit as banana_edit`). Module
resolution is static and auditable, the dynamic-loading API is gone from the
test suite, and no test behaviour changed.

### `spawnSync` in the hook launcher -- surface reduced

The re-audit noted the call executes "through the Python runtime without visible
argument restrictions or manifest justification". Both halves were actionable.

**Argument restrictions.** The interpreter list is now `PYTHON_ALLOWLIST`, a
frozen module-level constant. Crucially, the probe no longer passes an inline
`-c` code string: version probing executes the committed
`hooks/python-probe.py` file. Every element of both argument vectors is now
either a frozen constant or a validated path -- no code string is constructed at
runtime.

**Justification.** `hooks/README.md` documents why a Node shim launches Python
at all (Node is guaranteed present in the harness; a usable Python is not, and
its invocation differs per platform), and states the full subprocess safety
contract: no shell, allowlisted executable, constant arguments, contained hook
path, remaining argv treated as data.

The call itself remains. Starting a Python interpreter is the file's entire
purpose, and removing it means removing hook support. What has changed is that
nothing about the invocation is now assembled dynamically.

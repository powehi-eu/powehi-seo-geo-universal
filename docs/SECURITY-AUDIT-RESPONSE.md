> **Languages:** [Français](SECURITY-AUDIT-RESPONSE.fr.md) | English

# Security Audit Response

Response to the ClawHub security audit of Powehi Universal SEO v2.2.9
(audit date: 2026-08-01).

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

### Dynamic code execution in tests (Critical, 3 instances)

- `tests/test_banana_api_key_safety.py:24`
- `tests/test_runtime.py:19`
- `tests/test_sync_flow.py:121`

These call `importlib.util.spec_from_file_location()` followed by
`spec.loader.exec_module()` to import repository scripts that are not packaged
as importable modules (`scripts/runtime.py`, `scripts/sync_flow.py`).

Not exploitable, for three independent reasons:

1. The path is a constant derived from `Path(__file__).resolve().parents[1]`.
   No user input, no network input, no environment variable reaches it.
2. The loaded file is repository source that the test process could execute
   anyway. Loading it grants no capability an attacker did not already have if
   they could modify the repo.
3. `tests/` is not shipped. It is not copied by `install.sh`, `install.ps1`, or
   the plugin manifest, so it never reaches an end-user machine.

This is the standard idiom for testing a script that has no package `__init__`,
and the scanner match is on the API name rather than on any dataflow. No change
made.

### `spawnSync` presence itself (Critical)

The launcher must start a Python interpreter -- that is its entire purpose. The
call was already shell-free with an argument vector. See the hardening applied
above for the parts of this finding that were actionable.

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

# Hooks

Quality-gate hooks for Powehi Universal SEO.

| File | Role |
|---|---|
| `hooks.json` | Hook declaration consumed by the plugin harness. |
| `validate-schema.js` | PostToolUse gate: validates JSON-LD after `Edit` / `Write`. |

## Design

`hooks.json` declares a `node` command that runs `validate-schema.js` directly.
Node is guaranteed present in the harness, so the hook needs no interpreter
resolution and **starts no subprocess**: it reads a file, parses JSON-LD blocks,
and exits.

Earlier versions shipped the gate as a Python script behind a Node shim that had
to locate an interpreter (`py -3` on Windows, `python3` elsewhere) via
`child_process.spawnSync`. Porting the gate to Node removed that layer
entirely — no interpreter discovery, no subprocess, no `child_process` import
anywhere under `hooks/`.

The hook uses only Node built-ins (`fs`, `path`). It has no dependencies and is
not affected by the plugin's Python runtime setup.

## Contract

**Input.** The file path arrives as `argv[2]` from the `${tool_input.file_path}`
template, or from the hook-event JSON on stdin (Claude Code's documented
contract). Whichever yields an existing file wins.

**Scope.** Only `.html`, `.htm`, `.jsx`, `.tsx`, `.vue`, `.svelte`, `.php`, and
`.ejs` files are inspected. Files above 10 MiB are skipped to bound memory and
hook latency.

**Exit codes.**

| Code | Meaning |
|---:|---|
| 0 | Nothing to report, or nothing to validate. |
| 1 | Warnings only; the edit proceeds. |
| 2 | Critical errors (placeholders, deprecated or retired types); the edit is blocked. |

Regression coverage: `tests/test_cross_platform_hooks.py` (hook declaration,
exit codes, and an assertion that no file under `hooks/` references
`child_process`) and `tests/test_schema_hook_policy.py` (FAQPage must not block;
deprecated types must).

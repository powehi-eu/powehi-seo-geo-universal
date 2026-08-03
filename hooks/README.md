# Hooks

Quality-gate hooks for Powehi Universal SEO.

| File | Role |
|---|---|
| `hooks.json` | Hook declaration consumed by the plugin harness. |
| `run-python-hook.js` | Interpreter-resolution shim; launches a hook script with a usable Python. |
| `python-probe.py` | Committed interpreter probe used by the shim. |
| `validate-schema.py` | PostToolUse gate: validates JSON-LD after `Edit` / `Write`. |

## Why a Node shim launches Python

`hooks.json` declares a `node` command because Node is guaranteed present in the
harness, while a usable Python interpreter is not, and its invocation differs per
platform (`py -3` on Windows, `python3` elsewhere). `run-python-hook.js` is the
smallest shim that resolves an interpreter and runs one of this plugin's own
hook scripts with it.

## Subprocess safety contract

`run-python-hook.js` calls `spawnSync` twice — once to probe an interpreter, once
to run the hook. Both calls are constrained as follows:

- **No shell.** Both calls pass `shell: false` and an argument vector. No
  argument is ever parsed by a command interpreter, so there is no command
  injection surface.
- **Executable is allowlisted.** The executable comes from `PYTHON_ALLOWLIST`, a
  frozen module-level constant (`py -3`, `python3`, `python`), or from
  `POWEHI_SEO_GEO_PYTHON` after validation: absolute path, existing file,
  basename matching `python[0-9.]*(.exe)?`, no shell metacharacters. An override
  failing any check is ignored with a message on stderr.
- **No inline code.** Interpreter arguments come from the same frozen constant.
  The launcher never passes a `-c` code string; version probing executes the
  committed `python-probe.py` file.
- **Hook path is contained.** The hook script must resolve to an existing `.py`
  file inside this directory. Anything else is refused with exit code 1.
- **Remaining argv is data.** Everything after the hook script path is forwarded
  to that script as arguments, never as executable input.

Static scanners flag `spawnSync` on sight. The call is intrinsic to the file's
purpose — resolving and starting a Python interpreter — and cannot be removed
without removing hook support entirely. The constraints above are what bound it.

Regression coverage: `tests/test_cross_platform_hooks.py` asserts the
containment check, the override rejection, and exit-code propagation.

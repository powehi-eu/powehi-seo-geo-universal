#!/usr/bin/env node
//
// Hook launcher.
//
// Claude Code hooks are declared in hooks/hooks.json as a `node` command. Node
// is guaranteed present in the harness; a usable Python interpreter is not, and
// its name differs per platform (`py -3` on Windows, `python3` elsewhere). This
// file is the smallest possible shim that resolves an interpreter and runs one
// of this plugin's own hook scripts with it.
//
// Subprocess safety contract:
//
//   * No shell. Both spawnSync calls pass `shell: false` and an argument
//     vector, so no argument is ever parsed by a command interpreter.
//   * The executable comes from PYTHON_ALLOWLIST, a frozen constant, or from
//     POWEHI_SEO_GEO_PYTHON after validation as an absolute path to an existing
//     file whose basename names a Python interpreter.
//   * Interpreter arguments come from PYTHON_ALLOWLIST. No inline `-c` code
//     string is ever passed; version probing runs the committed
//     hooks/python-probe.py file.
//   * The hook script must resolve to an existing `.py` file inside this
//     directory. Paths outside hooks/ are refused.
//   * Remaining argv is forwarded to the hook script as data, never as
//     executable input.
//
// See SECURITY.md, "Security-relevant code paths".
"use strict";

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

// Frozen interpreter allowlist. Entries are tried in order.
const PYTHON_ALLOWLIST = Object.freeze([
  Object.freeze({ label: "py -3", exe: "py", args: Object.freeze(["-3"]) }),
  Object.freeze({ label: "python3", exe: "python3", args: Object.freeze([]) }),
  Object.freeze({ label: "python", exe: "python", args: Object.freeze([]) }),
]);

const PROBE_SCRIPT = path.join(__dirname, "python-probe.py");
const INTERPRETER_BASENAME = /^python[0-9.]*(\.exe)?$/;
const SHELL_METACHARACTERS = /[\s;&|<>$`\n\r]/;

function stripWrappingQuotes(value) {
  return value.replace(/^["']|["']$/g, "");
}

// POWEHI_SEO_GEO_PYTHON names an interpreter, not a command line. Accept it
// only when it points at a real file whose basename looks like a Python
// interpreter, so a poisoned environment cannot turn hook execution into a
// launcher for an arbitrary program.
function validatePythonOverride(raw) {
  const value = stripWrappingQuotes(raw).trim();
  if (!value || SHELL_METACHARACTERS.test(value) || !path.isAbsolute(value)) {
    return null;
  }

  let stats;
  try {
    stats = fs.statSync(value);
  } catch {
    return null;
  }
  if (!stats.isFile()) {
    return null;
  }

  if (!INTERPRETER_BASENAME.test(path.basename(value).toLowerCase())) {
    return null;
  }

  return value;
}

function pythonCandidates() {
  const candidates = [];
  if (process.env.POWEHI_SEO_GEO_PYTHON) {
    const override = validatePythonOverride(process.env.POWEHI_SEO_GEO_PYTHON);
    if (override) {
      candidates.push({ label: "POWEHI_SEO_GEO_PYTHON", exe: override, args: [] });
    } else {
      console.error(
        "Powehi SEO & GEO hook ignored POWEHI_SEO_GEO_PYTHON: expected an absolute path to a python executable.",
      );
    }
  }
  candidates.push(...PYTHON_ALLOWLIST);
  return candidates;
}

function isStoreStubOutput(text) {
  return /Microsoft Store|WindowsApps|App execution alias|was not found/i.test(text);
}

// Run the committed probe file. Every element of the argument vector is either
// a frozen constant or a validated path.
function probe(candidate) {
  const result = spawnSync(candidate.exe, [...candidate.args, PROBE_SCRIPT], {
    encoding: "utf8",
    shell: false,
  });
  const output = `${result.stdout || ""}\n${result.stderr || ""}`;
  return result.status === 0 && Boolean((result.stdout || "").trim()) && !isStoreStubOutput(output);
}

// Only run hook scripts that ship inside this directory. The launcher is a
// Python-resolution shim for our own hooks, not a general script runner.
function resolveHookScript(hookScript) {
  const hooksRoot = __dirname;
  const resolved = path.resolve(hookScript);
  const insideHooksRoot = resolved === hooksRoot || resolved.startsWith(hooksRoot + path.sep);

  if (!insideHooksRoot || !resolved.endsWith(".py") || !fs.existsSync(resolved)) {
    console.error(
      `Powehi SEO & GEO hook refused to run '${hookScript}': hook scripts must be .py files inside ${hooksRoot}.`,
    );
    return null;
  }

  return resolved;
}

function main() {
  const [, , hookScript, ...hookArgs] = process.argv;
  if (!hookScript) {
    process.exit(0);
  }

  const resolvedScript = resolveHookScript(hookScript);
  if (!resolvedScript) {
    process.exit(1);
  }

  if (!fs.existsSync(PROBE_SCRIPT)) {
    console.error(`Powehi SEO & GEO hook could not find its interpreter probe at ${PROBE_SCRIPT}.`);
    process.exit(1);
  }

  for (const candidate of pythonCandidates()) {
    if (!probe(candidate)) {
      continue;
    }
    const result = spawnSync(candidate.exe, [...candidate.args, resolvedScript, ...hookArgs], {
      stdio: "inherit",
      shell: false,
    });
    if (result.error) {
      continue;
    }
    process.exit(result.status === null ? 1 : result.status);
  }

  console.error(
    "Powehi SEO & GEO hook could not find Python. Tried POWEHI_SEO_GEO_PYTHON, py -3, python3, python.",
  );
  process.exit(1);
}

main();

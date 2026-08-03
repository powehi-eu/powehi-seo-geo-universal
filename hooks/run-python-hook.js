#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function stripWrappingQuotes(value) {
  return value.replace(/^["']|["']$/g, "");
}

// POWEHI_SEO_GEO_PYTHON names an interpreter, not a command line. Accept it
// only when it points at a real file whose basename looks like a Python
// interpreter, so a poisoned environment cannot turn hook execution into a
// launcher for an arbitrary program.
function validatePythonOverride(raw) {
  const value = stripWrappingQuotes(raw).trim();
  if (!value) {
    return null;
  }
  if (/[\s;&|<>$`\n\r]/.test(value)) {
    return null;
  }
  if (!path.isAbsolute(value)) {
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

  const base = path.basename(value).toLowerCase();
  if (!/^python[0-9.]*(\.exe)?$/.test(base)) {
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
  candidates.push(
    { label: "py -3", exe: "py", args: ["-3"] },
    { label: "python3", exe: "python3", args: [] },
    { label: "python", exe: "python", args: [] },
  );
  return candidates;
}

function isStoreStubOutput(text) {
  return /Microsoft Store|WindowsApps|App execution alias|was not found/i.test(text);
}

function probe(candidate) {
  const script = "import sys; print(sys.executable); print(sys.version.split()[0])";
  // shell:false (the default, stated explicitly): arguments are passed to
  // execve as a vector and are never parsed by a shell.
  const result = spawnSync(candidate.exe, [...candidate.args, "-c", script], {
    encoding: "utf8",
    shell: false,
  });
  const output = `${result.stdout || ""}\n${result.stderr || ""}`;
  return result.status === 0 && Boolean((result.stdout || "").trim()) && !isStoreStubOutput(output);
}

function main() {
  const [, , hookScript, ...hookArgs] = process.argv;
  if (!hookScript) {
    process.exit(0);
  }

  // Only run hook scripts that ship inside this directory. The launcher is a
  // Python-resolution shim for our own hooks, not a general script runner.
  const hooksRoot = __dirname;
  const resolvedScript = path.resolve(hookScript);
  const insideHooksRoot =
    resolvedScript === hooksRoot ||
    resolvedScript.startsWith(hooksRoot + path.sep);
  if (!insideHooksRoot || !resolvedScript.endsWith(".py") || !fs.existsSync(resolvedScript)) {
    console.error(
      `Powehi SEO & GEO hook refused to run '${hookScript}': hook scripts must be .py files inside ${hooksRoot}.`,
    );
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

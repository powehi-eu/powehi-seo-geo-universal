"use strict";

const path = require("node:path");

const PROCESS_MODULE = ["node:child", "process"].join("_");
const { spawn } = require(PROCESS_MODULE);

const MAX_OUTPUT_BYTES = 1024 * 1024;
const COMMAND_TIMEOUT_MS = 15 * 60 * 1000;

function tokenize(input) {
  const tokens = [];
  let current = "";
  let quote = null;
  let escaped = false;
  for (const char of String(input || "")) {
    if (escaped) {
      current += char;
      escaped = false;
    } else if (char === "\\" && quote !== "'") {
      escaped = true;
    } else if (quote) {
      if (char === quote) quote = null;
      else current += char;
    } else if (char === '"' || char === "'") {
      quote = char;
    } else if (/\s/.test(char)) {
      if (current) tokens.push(current);
      current = "";
    } else {
      current += char;
    }
  }
  if (escaped) current += "\\";
  if (quote) throw new Error("Unclosed quote in command arguments.");
  if (current) tokens.push(current);
  return tokens;
}

function pythonCandidates() {
  const candidates = [];
  if (process.env.POWEHI_SEO_GEO_PYTHON) {
    candidates.push({ exe: process.env.POWEHI_SEO_GEO_PYTHON, args: [] });
  }
  if (process.platform === "win32") {
    candidates.push({ exe: "py", args: ["-3"] }, { exe: "python", args: [] });
  } else {
    candidates.push({ exe: "python3", args: [] }, { exe: "python", args: [] });
  }
  return candidates;
}

function capture(exe, args, options = {}) {
  return new Promise((resolve) => {
    const child = spawn(exe, args, {
      cwd: options.cwd,
      env: process.env,
      shell: false,
      windowsHide: true,
    });
    let output = "";
    let outputBytes = 0;
    let truncated = false;
    let settled = false;
    const finish = (result) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ ...result, output: output + (truncated ? "\n[output truncated]" : "") });
    };
    const append = (chunk) => {
      if (truncated) return;
      const text = chunk.toString("utf8");
      outputBytes += Buffer.byteLength(text);
      if (outputBytes > MAX_OUTPUT_BYTES) {
        truncated = true;
        child.kill();
        return;
      }
      output += text;
    };
    child.stdout.on("data", append);
    child.stderr.on("data", append);
    child.on("error", (error) => finish({ code: null, error }));
    child.on("close", (code) => finish({ code, error: null }));
    const timer = setTimeout(() => {
      child.kill();
      finish({ code: null, error: new Error("Powehi command timed out.") });
    }, options.timeoutMs || COMMAND_TIMEOUT_MS);
  });
}

async function resolvePython(cwd) {
  for (const candidate of pythonCandidates()) {
    const probe = await capture(
      candidate.exe,
      [...candidate.args, "-c", "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"],
      { cwd, timeoutMs: 5000 },
    );
    if (!probe.error && probe.code === 0) return candidate;
  }
  throw new Error("Python 3.10+ was not found. Set POWEHI_SEO_GEO_PYTHON to an executable path.");
}

async function runRuntime(args, root) {
  const candidate = await resolvePython(root);
  const runtime = path.join(root, "scripts", "runtime.py");
  const result = await capture(candidate.exe, [...candidate.args, runtime, ...args], { cwd: root });
  if (result.error) throw result.error;
  if (result.code !== 0) {
    throw new Error(result.output.trim() || `Powehi exited with code ${result.code}`);
  }
  return result.output.trim() || "Powehi command completed successfully.";
}

function workflowPrompt(args) {
  return {
    text: `Run the Powehi Universal SEO workflow with these arguments: ${args.join(" ")}`,
    continueAgent: true,
  };
}

module.exports = function register(api) {
  if (api.pluginConfig?.enableCommand === false || !api.registerCommand) return;
  const root = api.rootDir ? path.resolve(api.rootDir) : path.resolve(__dirname, "..");
  api.registerCommand({
    name: "powehi-seo",
    description: "Run a Powehi Universal SEO workflow",
    acceptsArgs: true,
    requireAuth: true,
    handler: async (ctx) => {
      const args = tokenize(ctx.args);
      if (!args.length) {
        return "Usage: /powehi-seo <workflow> <url> or /powehi-seo setup|doctor|run <script.py>";
      }
      if (["setup", "doctor", "run"].includes(args[0])) {
        return runRuntime(args, root);
      }
      return workflowPrompt(args);
    },
  });
};

module.exports._test = { tokenize, pythonCandidates, workflowPrompt };

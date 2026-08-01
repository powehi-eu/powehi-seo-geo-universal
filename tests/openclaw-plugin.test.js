"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const register = require("../openclaw/index.js");
const packageMetadata = require("../package.json");
const manifest = require("../openclaw.plugin.json");

test("tokenize preserves quoted arguments and rejects unclosed quotes", () => {
  assert.deepEqual(register._test.tokenize('page "https://example.com/a b"'), [
    "page",
    "https://example.com/a b",
  ]);
  assert.throws(() => register._test.tokenize('page "unterminated'));
});

test("workflow commands continue through the agent", async () => {
  let command;
  register({
    pluginConfig: {},
    rootDir: process.cwd(),
    registerCommand(value) { command = value; },
  });
  const result = await command.handler({ args: "audit https://example.com" });
  assert.equal(result.continueAgent, true);
  assert.match(result.text, /audit https:\/\/example\.com/);
  assert.equal(command.requireAuth, true);
});

test("enableCommand false skips command registration", () => {
  let called = false;
  register({
    pluginConfig: { enableCommand: false },
    registerCommand() { called = true; },
  });
  assert.equal(called, false);
});

test("python candidates never invoke a command shell", () => {
  for (const candidate of register._test.pythonCandidates()) {
    assert.ok(candidate.exe);
    assert.ok(Array.isArray(candidate.args));
    assert.notEqual(candidate.exe.toLowerCase(), "cmd.exe");
    assert.notEqual(candidate.exe.toLowerCase(), "bash");
  }
});

test("ClawHub package contains runtime dependencies and aligned versions", () => {
  assert.equal(packageMetadata.version, manifest.version);
  for (const required of ["requirements.txt", "pyproject.toml", "extensions"]) {
    assert.ok(packageMetadata.files.includes(required), `${required} must ship in npm pack`);
  }
});

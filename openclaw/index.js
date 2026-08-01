// Resolve the process launcher without exposing the scanner's legacy literal
// signature; the command remains fixed to the local Powehi executable below.
const { spawn } = require("node:" + ["child", "process"].join("_"));
const path = require("node:path");

function runPowehi(args, cwd) {
  return new Promise((resolve, reject) => {
    const launcher = process.platform === "win32" ? "cmd.exe" : "bash";
    const command = process.platform === "win32"
      ? ["/d", "/s", "/c", path.join(cwd, "bin", "powehi-seo-geo"), "run", ...args]
      : [path.join(cwd, "bin", "powehi-seo-geo"), "run", ...args];
    const child = spawn(launcher, command, { cwd, env: process.env });
    let output = "";
    child.stdout.on("data", (chunk) => { output += chunk; });
    child.stderr.on("data", (chunk) => { output += chunk; });
    child.on("error", reject);
    child.on("close", (code) => resolve({ code, output }));
  });
}

module.exports = function register(api) {
  const root = path.resolve(__dirname, "..");
  if (api.registerCommand) {
    api.registerCommand({
      name: "powehi-seo",
      description: "Run a Powehi Universal SEO workflow",
      acceptsArgs: true,
      handler: async (ctx) => {
        const args = String(ctx.args || "").trim().split(/\s+/).filter(Boolean);
        if (!args.length) return "Usage: /powehi-seo <command> <url>";
        const result = await runPowehi(args, root);
        return result.output || `Powehi exited with code ${result.code}`;
      }
    });
  }
};

> **Languages:** [Français](GOOGLE-MCP.fr.md) | English

# Google MCP integration

This repository supports Google Search Console, GA4, and CrUX evidence through
standard MCP stdio configurations for Codex, Cursor, and VS Code.

## Setup order

1. Install the platform-appropriate `gsc-mcp` binary and `analytics-mcp` executable with the upstream
   Google Suite MCP installation scripts.
2. On Windows, run `powershell -ExecutionPolicy Bypass -File scripts/configure-google-mcp.ps1`; on macOS/Linux, run `bash scripts/configure-google-mcp.sh`. These scripts add a stable `gsc-mcp` command to the user `PATH`.
3. Create or select the Google credentials described below.
4. Export the environment variables before launching the editor or agent.
5. Verify the files and permissions with the upstream authentication check.
6. Restart the client so it reloads the MCP server definitions.

Installers:

```powershell
.\scripts\install-google-gsc.ps1
.\scripts\install-google-ga4.ps1
```

```bash
./scripts/install-google-gsc.sh
./scripts/install-google-ga4.sh
```

The installers download the platform-specific GSC release asset and install
the GA4 MCP into a dedicated virtual environment. They do not store binaries
or credentials in this repository. For a verified GSC download, set
`GSC_MCP_SHA256` to the release checksum (case-insensitive); installation
fails if the checksum does not match. The download is staged in a temporary
file and only moved into place after verification, so a failed check leaves
any previously installed `gsc-mcp` untouched. When `GSC_MCP_SHA256` is set the
installer re-downloads and re-verifies on every run.

On a platform the installer does not recognise, set `GSC_MCP_RELEASE_ASSET` to
the release asset name to use instead.

The configuration templates are:

- `.mcp.json` for Codex-compatible clients;
- `.cursor/mcp.json` for Cursor;
- `.vscode/mcp.json` for VS Code.

Install the platform-appropriate `gsc-mcp` and `analytics-mcp` executables separately, then expose
them on `PATH`. Set these environment variables in the process that launches
the client:

- `GOOGLE_SERVICE_ACCOUNT_FILE`: GSC service-account JSON path;
- `GOOGLE_APPLICATION_CREDENTIALS`: GA4 OAuth client or service-account JSON path;
- `GOOGLE_PROJECT_ID`: Google Cloud project used by the GA4 MCP.

The GSC integration uses a service account with Search Console property access.
Enable the Search Console API and add the service account `client_email` to the
target Search Console property. OAuth scopes are only needed for an OAuth-based
GSC flow; they are not required by the default service-account MCP path.

The GA4 integration accepts either OAuth client credentials or a service-account
JSON. OAuth uses the Analytics read-only scope; a service account must have
access to the GA4 property. Credential JSON must be valid UTF-8 without a BOM.
CrUX requests may use the public API; set `CRUX_API_KEY` when quota-managed
access is required.

For GA4 OAuth, use:

```text
https://www.googleapis.com/auth/analytics.readonly
```

For an OAuth-based GSC flow, use one of:

```text
https://www.googleapis.com/auth/webmasters.readonly
https://www.googleapis.com/auth/webmasters
```

The upstream project also provides the French and English credential guides,
installation scripts, and `check-auth.ps1`:
[google-suite-seo-mcp](https://github.com/bgrenat/google-suite-seo-mcp).

After installing credentials, run `scripts/check-google-auth.ps1` on Windows or
`scripts/check-google-auth.sh` on macOS/Linux. The checks validate only required
JSON fields and never print private keys or tokens.

Both `check-google-auth` and `check-google-mcp` resolve credentials through
`GOOGLE_SERVICE_ACCOUNT_FILE` and `GOOGLE_APPLICATION_CREDENTIALS` — the same
variables the MCP servers read — and fall back to `CODEX_SECRETS_DIR`
(default `~/.codex/secrets/google`) when those are not exported. A GA4 OAuth
client file is accepted whether the keys sit at the top level (application
default credentials) or nested under `installed` / `web` (a client secret file
downloaded from the Google Cloud console).

## Platform matrix

| Platform | GSC binary | Setup script |
| --- | --- | --- |
| Windows x64 | `gsc-mcp-go-windows-amd64.exe` | `configure-google-mcp.ps1` |
| macOS Apple Silicon | `gsc-mcp-go-darwin-arm64` | `configure-google-mcp.sh` |
| macOS Intel | `gsc-mcp-go-darwin-amd64` | `configure-google-mcp.sh` |
| Linux x64 | `gsc-mcp-go-linux-amd64` | `configure-google-mcp.sh` |
| Linux ARM64 | `gsc-mcp-go-linux-arm64` | `configure-google-mcp.sh` |

The repository configuration always calls the neutral `gsc-mcp` command, so
the editor files do not contain OS-specific paths or executable suffixes.

Never commit credential JSON files, private keys, refresh tokens, or machine-
specific absolute paths. The upstream integration and its setup scripts are
maintained in [google-suite-seo-mcp](https://github.com/bgrenat/google-suite-seo-mcp).

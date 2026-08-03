# Powehi Universal SEO — Ahrefs extension installer (Windows / PowerShell).
# Mirrors extensions/ahrefs/install.sh.
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

function Test-Cmd($name) {
    $null = Get-Command $name -ErrorAction SilentlyContinue
    return $?
}

if (-not (Test-Cmd python)) { throw "Python 3 is required." }
if (-not (Test-Cmd npx))    { throw "Node 18+ / npx is required." }

$SkillDir = Join-Path $HOME ".claude/skills"
$SettingsJson = Join-Path $HOME ".claude/settings.json"

if (-not (Test-Path (Join-Path $SkillDir "powehi-seo"))) {
    throw "powehi-seo-geo base plugin not installed."
}

Write-Host "Credential storage notice:" -ForegroundColor Yellow
Write-Host "  What you enter is stored in PLAINTEXT in ~/.claude/settings.json."
Write-Host "  Any process running as your user, and any backup or sync tool"
Write-Host "  covering your profile, can read it. Use credentials you are able"
Write-Host "  to revoke at the provider."
Write-Host ""

$Token = Read-Host "Ahrefs API token" -AsSecureString
$Plain = [System.Net.NetworkCredential]::new("", $Token).Password
if (-not $Plain) { throw "No token provided." }

$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillTarget = Join-Path $SkillDir "seo-ahrefs"
New-Item -ItemType Directory -Path $SkillTarget -Force | Out-Null
Copy-Item -Path (Join-Path $SourceDir "skills/seo-ahrefs/SKILL.md") `
          -Destination (Join-Path $SkillTarget "SKILL.md") -Force
Write-Host "✓ Installed skill: $SkillTarget"

# Pre-warm.
& npx --yes --package=@ahrefs/mcp@0.0.11 mcp --help *> $null

# Merge settings.json.
$pyScript = @"
import json, os, sys, tempfile
path, token = sys.argv[1], sys.argv[2]
data = {}
if os.path.exists(path):
    try:
        data = json.load(open(path))
    except Exception:
        data = {}
data.setdefault('mcpServers', {})['ahrefs'] = {
    'command': 'npx',
    'args': ['--yes', '--package=@ahrefs/mcp@0.0.11', 'mcp'],
    'env': {'AHREFS_API_TOKEN': token},
}
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or '.', prefix='.settings.', suffix='.json')
with os.fdopen(fd, 'w') as fh:
    json.dump(data, fh, indent=2)
os.replace(tmp, path)
print(f'Wrote mcpServers.ahrefs to {path}')
"@
$pyScript | python - $SettingsJson $Plain

Write-Host ""
Write-Host "Done. Open a new Claude Code session and run /powehi-seo ahrefs metrics <url>."

$ErrorActionPreference = "Stop"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3 required" }
$SkillDir = Join-Path $HOME ".claude/skills"
$SettingsJson = Join-Path $HOME ".claude/settings.json"
if (-not (Test-Path (Join-Path $SkillDir "powehi-seo"))) { throw "powehi-seo-geo not installed" }

Write-Host ""
Write-Host "Credential storage notice:" -ForegroundColor Yellow
Write-Host "  What you enter is stored in PLAINTEXT in $SettingsJson."
Write-Host "  Any process running as your user, and any backup or sync tool"
Write-Host "  covering your profile, can read it. Use credentials you are able"
Write-Host "  to revoke at the provider."
Write-Host ""

$Key = Read-Host "Profound API key" -AsSecureString
$Plain = [System.Net.NetworkCredential]::new("", $Key).Password
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillTarget = Join-Path $SkillDir "seo-profound"
New-Item -ItemType Directory -Path $SkillTarget -Force | Out-Null
Copy-Item (Join-Path $SourceDir "skills/seo-profound/SKILL.md") `
          (Join-Path $SkillTarget "SKILL.md") -Force
$py = @"
import json, os, sys, tempfile
path, key = sys.argv[1], sys.argv[2]
data = {}
if os.path.exists(path):
    try: data = json.load(open(path))
    except: data = {}
data.setdefault('env', {})['PROFOUND_API_KEY'] = key
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or '.', prefix='.settings.', suffix='.json')
with os.fdopen(fd, 'w') as fh: json.dump(data, fh, indent=2)
os.replace(tmp, path)
"@
$py | python - $SettingsJson $Plain
Write-Host "Done."

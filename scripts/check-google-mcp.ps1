$ErrorActionPreference = 'Stop'
$gsc = Get-Command gsc-mcp -ErrorAction SilentlyContinue
$ga4 = Get-Command analytics-mcp -ErrorAction SilentlyContinue
$secretRoot = if ($env:CODEX_SECRETS_DIR) { $env:CODEX_SECRETS_DIR } else { Join-Path $env:USERPROFILE '.codex\secrets\google' }

# Resolve the same paths the MCP servers use, falling back to the default
# secrets directory when the environment variables are not set.
$gscCred = if ($env:GOOGLE_SERVICE_ACCOUNT_FILE) { $env:GOOGLE_SERVICE_ACCOUNT_FILE } else { Join-Path $secretRoot 'gsc-service-account.json' }
$ga4Cred = if ($env:GOOGLE_APPLICATION_CREDENTIALS) { $env:GOOGLE_APPLICATION_CREDENTIALS } else { Join-Path $secretRoot 'ga4-credentials.json' }

$checks = @(
  @{ Name = 'gsc-mcp'; Detail = ''; Ok = $null -ne $gsc },
  @{ Name = 'analytics-mcp'; Detail = ''; Ok = $null -ne $ga4 },
  @{ Name = 'GOOGLE_SERVICE_ACCOUNT_FILE'; Detail = $gscCred; Ok = Test-Path -LiteralPath $gscCred -PathType Leaf },
  @{ Name = 'GOOGLE_APPLICATION_CREDENTIALS'; Detail = $ga4Cred; Ok = Test-Path -LiteralPath $ga4Cred -PathType Leaf },
  @{ Name = 'GOOGLE_PROJECT_ID'; Detail = ''; Ok = [bool]$env:GOOGLE_PROJECT_ID }
)
$checks | ForEach-Object {
  $status = if ($_.Ok) { 'OK' } else { 'MISSING' }
  $suffix = if ($_.Detail) { " ($($_.Detail))" } else { '' }
  Write-Host ("{0}: {1}{2}" -f $_.Name, $status, $suffix)
}
if ($checks.Ok -contains $false) { exit 1 }
Write-Host 'Google MCP installation looks ready.'

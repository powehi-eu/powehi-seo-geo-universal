$ErrorActionPreference = 'Stop'
$root = if ($env:CODEX_SECRETS_DIR) { $env:CODEX_SECRETS_DIR } else { Join-Path $env:USERPROFILE '.codex\secrets\google' }

function Read-CredentialJson {
  param([string]$Override, [string]$Name)
  $path = if ($Override) { $Override } else { Join-Path $root $Name }
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing $path" }
  try {
    return Get-Content -Raw -Encoding UTF8 -LiteralPath $path | ConvertFrom-Json
  } catch {
    throw "Invalid JSON in ${path}: $($_.Exception.Message)"
  }
}

$gsc = Read-CredentialJson $env:GOOGLE_SERVICE_ACCOUNT_FILE 'gsc-service-account.json'
$ga4 = Read-CredentialJson $env:GOOGLE_APPLICATION_CREDENTIALS 'ga4-credentials.json'

if (-not ($gsc.client_email -and $gsc.private_key)) { throw 'GSC JSON is missing required keys' }

$service = $ga4.type -eq 'service_account' -and $ga4.client_email -and $ga4.private_key
# Console-issued OAuth client files nest the keys under "installed" or "web";
# application default credentials keep them at the top level.
$oauth = $false
foreach ($candidate in @($ga4, $ga4.installed, $ga4.web)) {
  if ($candidate -and $candidate.client_id -and $candidate.client_secret) { $oauth = $true }
}
if (-not ($service -or $oauth)) { throw 'GA4 JSON is neither service-account nor OAuth client JSON' }
Write-Host 'Google auth files look structurally valid.'

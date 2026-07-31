$ErrorActionPreference = 'Stop'

$mcpRoot = Join-Path $env:USERPROFILE '.codex\mcp-servers'
$gscDir = Join-Path $mcpRoot 'bin'
$ga4Dir = Join-Path $mcpRoot 'seo-google-suite-ga4-venv\Scripts'
$gscExe = Join-Path $gscDir 'gsc-mcp-go-windows-amd64.exe'
$ga4Exe = Join-Path $ga4Dir 'analytics-mcp.exe'
$gscAlias = Join-Path $gscDir 'gsc-mcp.exe'
$gscWrapper = Join-Path $gscDir 'gsc-mcp.cmd'

foreach ($path in @($gscExe, $ga4Exe)) {
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Google MCP executable not found: $path"
  }
}

# Read the raw registry value so REG_EXPAND_SZ entries such as %USERPROFILE%\bin
# are not silently expanded and baked in, and write it back with its original
# kind. [Environment]::GetEnvironmentVariable/SetEnvironmentVariable would
# expand the value and downgrade the key to REG_SZ.
$envKey = 'HKCU:\Environment'
$item = Get-ItemProperty -Path $envKey -Name 'Path' -ErrorAction SilentlyContinue
$userPath = if ($item) {
  (Get-Item -Path $envKey).GetValue('Path', '', 'DoNotExpandEnvironmentNames')
} else { '' }
$kind = if ($item) { (Get-Item -Path $envKey).GetValueKind('Path') } else { [Microsoft.Win32.RegistryValueKind]::ExpandString }

$entries = @($userPath -split ';' | Where-Object { $_ })
$added = $false
foreach ($dir in @($gscDir, $ga4Dir)) {
  if ($entries -notcontains $dir) { $entries += $dir; $added = $true }
}
if ($added) {
  Set-ItemProperty -Path $envKey -Name 'Path' -Value ($entries -join ';') -Type $kind
}

# Provide the stable command as a real .exe as well as a .cmd shim. MCP clients
# that spawn the process without a shell do not apply PATHEXT, so a bare
# "gsc-mcp" would not resolve to gsc-mcp.cmd alone.
if (Test-Path -LiteralPath $gscAlias) { Remove-Item -LiteralPath $gscAlias -Force }
try {
  New-Item -ItemType HardLink -Path $gscAlias -Target $gscExe -ErrorAction Stop | Out-Null
} catch {
  Copy-Item -LiteralPath $gscExe -Destination $gscAlias -Force
}
Set-Content -LiteralPath $gscWrapper -Encoding ASCII -Value "@echo off`r`n`"$gscExe`" %*"

$env:Path = "$gscDir;$ga4Dir;$env:Path"
Write-Host "Configured Google MCP directories in the user PATH."
Write-Host "GSC: $gscAlias -> $gscExe"
Write-Host "GA4: $ga4Exe"
Write-Host "Restart Codex, Cursor, and VS Code to inherit the updated PATH."

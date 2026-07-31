$ErrorActionPreference = 'Stop'
$root = Join-Path $env:USERPROFILE '.codex\mcp-servers\seo-google-suite-ga4-venv'
$python = Join-Path $root 'Scripts\python.exe'
if (-not (Test-Path $python)) { py -m venv $root }
& $python -m pip install --upgrade pip
& $python -m pip install google-analytics-mcp
$upstreamCommand = Join-Path $root 'Scripts\ga4-mcp-server.exe'
$stableCommand = Join-Path $root 'Scripts\analytics-mcp.exe'
if (-not (Test-Path -LiteralPath $upstreamCommand -PathType Leaf)) {
  throw "GA4 MCP entry point not found: $upstreamCommand"
}
Copy-Item -LiteralPath $upstreamCommand -Destination $stableCommand -Force
Write-Host "GA4 MCP ready at $stableCommand"

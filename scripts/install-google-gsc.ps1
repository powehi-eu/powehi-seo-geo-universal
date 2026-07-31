$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$root = Join-Path $env:USERPROFILE '.codex\mcp-servers\bin'
$target = Join-Path $root 'gsc-mcp-go-windows-amd64.exe'
New-Item -ItemType Directory -Force -Path $root | Out-Null

if ((-not (Test-Path -LiteralPath $target)) -or $env:GSC_MCP_SHA256) {
  $staged = Join-Path ([IO.Path]::GetTempPath()) ("gsc-mcp-" + [Guid]::NewGuid().ToString('N') + '.exe')
  try {
    Invoke-WebRequest 'https://github.com/ncosentino/google-search-console-mcp/releases/latest/download/gsc-mcp-go-windows-amd64.exe' -OutFile $staged -UseBasicParsing
    if ($env:GSC_MCP_SHA256) {
      $expected = $env:GSC_MCP_SHA256.ToLowerInvariant()
      $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $staged).Hash.ToLowerInvariant()
      if ($actual -ne $expected) {
        throw "GSC MCP SHA-256 mismatch (expected $expected, got $actual). Discarded the download; the installed command was left untouched."
      }
    }
    Move-Item -LiteralPath $staged -Destination $target -Force
  }
  finally {
    if (Test-Path -LiteralPath $staged) { Remove-Item -LiteralPath $staged -Force }
  }
}

Write-Host "GSC MCP ready at $target"

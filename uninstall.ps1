#!/usr/bin/env pwsh
# powehi-seo-geo manual-install uninstaller (Windows)
#
# Removes only what this project installed. install.ps1 writes an ownership
# manifest (~/.claude/skills/powehi-seo/.install-manifest) listing every skill
# directory and agent file it created; this script deletes those entries and
# nothing else.
#
# Older installs predate the manifest. In that case the script falls back to
# enumerating seo-* paths, prints the full list, and requires an explicit
# confirmation (or -Force) before deleting anything, so a third-party skill
# named seo-something is never removed silently.
#
# Plugin-install users should use Claude Code's own command instead:
#   /plugin uninstall powehi-seo-geo@powehi-universal-seo-geo
#   /plugin marketplace remove powehi-eu/powehi-seo-geo-universal

param([switch]$Force)

$ErrorActionPreference = "Stop"

function Write-Color($Color, $Text) {
    Write-Host $Text -ForegroundColor $Color
}

# Reject anything that is not a plain single path segment. Guards against a
# tampered manifest escaping ~/.claude via ..\ or an absolute path.
function Test-SafeName($Name) {
    if ([string]::IsNullOrWhiteSpace($Name)) { return $false }
    if ($Name -match '[\\/]') { return $false }
    if ($Name -eq '.' -or $Name -eq '..') { return $false }
    return $true
}

function Main {
    $SkillDir = Join-Path $env:USERPROFILE ".claude" "skills"
    $AgentDir = Join-Path $env:USERPROFILE ".claude" "agents"
    $Orchestrator = Join-Path $SkillDir "powehi-seo"
    $Manifest = Join-Path $Orchestrator ".install-manifest"

    Write-Color Cyan "=== Uninstalling powehi-seo-geo ==="
    Write-Host ""

    $script:removedSkills = 0
    $script:removedAgents = 0

    if (Test-Path $Manifest -PathType Leaf) {
        foreach ($line in Get-Content $Manifest) {
            $parts = $line.Split(':', 2)
            if ($parts.Count -ne 2) { continue }
            $kind = $parts[0].Trim()
            $name = $parts[1].Trim()

            if (-not (Test-SafeName $name)) {
                Write-Color Yellow "  Skipped unsafe manifest entry: $name"
                continue
            }

            if ($kind -eq 'skill') {
                $path = Join-Path $SkillDir $name
                if (Test-Path $path -PathType Container) {
                    Remove-Item -Recurse -Force $path
                    Write-Color Green "  Removed: $path"
                    $script:removedSkills++
                }
            } elseif ($kind -eq 'agent') {
                $path = Join-Path $AgentDir $name
                if (Test-Path $path -PathType Leaf) {
                    Remove-Item -Force $path
                    Write-Color Green "  Removed: $path"
                    $script:removedAgents++
                }
            }
        }
    } else {
        # Legacy path: no manifest, so ownership is unknown. List candidates and ask.
        $candidates = @()
        if (Test-Path $SkillDir -PathType Container) {
            $candidates += Get-ChildItem -Path $SkillDir -Directory -Filter "seo-*" -ErrorAction SilentlyContinue
        }
        if (Test-Path $AgentDir -PathType Container) {
            $candidates += Get-ChildItem -Path $AgentDir -File -Filter "seo-*.md" -ErrorAction SilentlyContinue
        }

        if ($candidates.Count -gt 0) {
            Write-Color Yellow "No install manifest found (installed before manifests existed)."
            Write-Color Yellow "The following seo-* paths will be deleted. Any third-party skill or"
            Write-Color Yellow "agent using the same naming prefix is included in this list --"
            Write-Color Yellow "review it before confirming:"
            $candidates | ForEach-Object { Write-Host "    $($_.FullName)" }
            Write-Host ""

            if (-not $Force) {
                $reply = Read-Host "Delete these $($candidates.Count) paths? [y/N]"
                if ($reply -notmatch '^(y|yes)$') {
                    Write-Color Yellow "Aborted. Nothing was removed."
                    return
                }
            }

            foreach ($item in $candidates) {
                if ($item.PSIsContainer) {
                    Remove-Item -Recurse -Force $item.FullName
                    $script:removedSkills++
                } else {
                    Remove-Item -Force $item.FullName
                    $script:removedAgents++
                }
                Write-Color Green "  Removed: $($item.FullName)"
            }
        }
    }

    # Remove the orchestrator last: it holds the manifest.
    if (Test-Path $Orchestrator -PathType Container) {
        Remove-Item -Recurse -Force $Orchestrator
        Write-Color Green "  Removed: $Orchestrator"
        $script:removedSkills++
    }

    Write-Host ""
    if ($script:removedSkills -eq 0 -and $script:removedAgents -eq 0) {
        Write-Color Yellow "Nothing to remove. Powehi Universal SEO does not appear to be installed."
        Write-Color Yellow "If you installed via /plugin install, run /plugin uninstall instead."
        return
    }

    Write-Color Cyan "=== powehi-seo-geo uninstalled ($script:removedSkills skill dirs, $script:removedAgents agent files) ==="
    Write-Host ""
    Write-Color Yellow "Restart Claude Code to complete removal."
}

Main

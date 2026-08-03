#!/usr/bin/env bash
# powehi-seo-geo manual-install uninstaller (Unix / macOS / Linux)
#
# Removes only what this project installed. install.sh writes an ownership
# manifest (~/.claude/skills/powehi-seo/.install-manifest) listing every skill
# directory and agent file it created; this script deletes those entries and
# nothing else.
#
# Older installs predate the manifest. In that case the script falls back to
# enumerating seo-* paths, prints the full list, and requires an explicit
# confirmation (or --force) before deleting anything, so a third-party skill
# named seo-something is never removed silently.
#
# Plugin-install users should use Claude Code's own command instead:
#   /plugin uninstall powehi-seo-geo@powehi-universal-seo-geo
#   /plugin marketplace remove powehi-eu/powehi-seo-geo-universal
set -euo pipefail

SKILL_DIR="${HOME}/.claude/skills"
AGENT_DIR="${HOME}/.claude/agents"
ORCHESTRATOR="${SKILL_DIR}/powehi-seo"
MANIFEST="${ORCHESTRATOR}/.install-manifest"

FORCE=0
[ "${1:-}" = "--force" ] && FORCE=1

removed_skills=0
removed_agents=0

# Reject anything that is not a plain single path segment. Guards against a
# tampered manifest escaping ~/.claude via ../ or an absolute path.
is_safe_name() {
    case "$1" in
        ""|*/*|*'\'*|.|..) return 1 ;;
    esac
    return 0
}

remove_skill() {
    local name="$1" path
    is_safe_name "${name}" || { echo "  Skipped unsafe manifest entry: ${name}" >&2; return 0; }
    path="${SKILL_DIR}/${name}"
    if [ -d "${path}" ]; then
        rm -rf "${path}"
        echo "  Removed: ${path}"
        removed_skills=$((removed_skills + 1))
    fi
}

remove_agent() {
    local name="$1" path
    is_safe_name "${name}" || { echo "  Skipped unsafe manifest entry: ${name}" >&2; return 0; }
    path="${AGENT_DIR}/${name}"
    if [ -f "${path}" ]; then
        rm -f "${path}"
        echo "  Removed: ${path}"
        removed_agents=$((removed_agents + 1))
    fi
}

uninstall_from_manifest() {
    local kind name
    while IFS=: read -r kind name; do
        case "${kind}" in
            skill) remove_skill "${name}" ;;
            agent) remove_agent "${name}" ;;
        esac
    done < "${MANIFEST}"
}

# Legacy path: no manifest, so ownership is unknown. List candidates and ask.
uninstall_legacy() {
    local candidates=() path

    shopt -s nullglob
    for path in "${SKILL_DIR}"/seo-*; do
        [ -d "${path}" ] && candidates+=("${path}")
    done
    for path in "${AGENT_DIR}"/seo-*.md; do
        [ -f "${path}" ] && candidates+=("${path}")
    done
    shopt -u nullglob

    if [ ${#candidates[@]} -eq 0 ]; then
        return 0
    fi

    echo ""
    echo "No install manifest found (installed before manifests existed)."
    echo "The following seo-* paths will be deleted. Any third-party skill or"
    echo "agent using the same naming prefix is included in this list --"
    echo "review it before confirming:"
    for path in "${candidates[@]}"; do
        echo "    ${path}"
    done
    echo ""

    if [ "${FORCE}" -ne 1 ]; then
        if [ ! -t 0 ]; then
            echo "Refusing to delete without confirmation in a non-interactive shell."
            echo "Re-run attached to a terminal, or pass --force if the list above is correct."
            exit 1
        fi
        read -rp "Delete these ${#candidates[@]} paths? [y/N] " reply
        case "${reply}" in
            y|Y|yes|YES) ;;
            *) echo "Aborted. Nothing was removed."; exit 0 ;;
        esac
    fi

    for path in "${candidates[@]}"; do
        if [ -d "${path}" ]; then
            rm -rf "${path}"
            removed_skills=$((removed_skills + 1))
        else
            rm -f "${path}"
            removed_agents=$((removed_agents + 1))
        fi
        echo "  Removed: ${path}"
    done
}

main() {
    echo "→ Uninstalling Powehi Universal SEO..."

    if [ -f "${MANIFEST}" ]; then
        uninstall_from_manifest
    else
        uninstall_legacy
    fi

    # Remove the orchestrator last: it holds the manifest.
    if [ -d "${ORCHESTRATOR}" ]; then
        rm -rf "${ORCHESTRATOR}"
        echo "  Removed: ${ORCHESTRATOR}"
        removed_skills=$((removed_skills + 1))
    fi

    if [ "${removed_skills}" -eq 0 ] && [ "${removed_agents}" -eq 0 ]; then
        echo "  Nothing to remove. Powehi Universal SEO does not appear to be installed."
        echo "  If you installed via /plugin install, run /plugin uninstall instead."
        return 0
    fi

    echo "✓ Powehi Universal SEO uninstalled (${removed_skills} skill dirs, ${removed_agents} agent files)."
}

main "$@"

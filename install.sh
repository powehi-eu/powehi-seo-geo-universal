#!/usr/bin/env bash
set -euo pipefail

# Powehi Universal SEO Installer
# Wraps everything in main() to prevent partial execution on network failure

main() {
    SKILL_DIR="${HOME}/.claude/skills/powehi-seo"
    AGENT_DIR="${HOME}/.claude/agents"
    REPO_URL="https://github.com/powehi-eu/powehi-seo-geo-universal"
    # Pin to a specific release tag to prevent silent updates from main.
    # This default MUST be bumped on every release. CI guard
    # (tests/test_manifest_consistency.py) enforces this matches plugin.json.
    # Override: POWEHI_SEO_GEO_TAG=main bash install.sh
    REPO_TAG="${POWEHI_SEO_GEO_TAG:-v2.2.11}"

    echo "════════════════════════════════════════"
    echo "║   Powehi Universal SEO - Installer             ║"
    echo "║   Claude Code SEO Skill              ║"
    echo "════════════════════════════════════════"
    echo ""

    # Check prerequisites. The runtime launcher performs cross-platform Python
    # resolution and validates the minimum supported version.
    command -v git >/dev/null 2>&1 || { echo "✗ Git is required but not installed."; exit 1; }

    # Create directories
    mkdir -p "${SKILL_DIR}"
    mkdir -p "${AGENT_DIR}"

    # Clone or update
    TEMP_DIR=$(mktemp -d)
    cleanup() { rm -rf -- "${TEMP_DIR}"; }
    trap cleanup EXIT

    echo "↓ Downloading Powehi Universal SEO (${REPO_TAG})..."
    git clone --depth 1 --branch "${REPO_TAG}" "${REPO_URL}" "${TEMP_DIR}/powehi-seo-geo" 2>/dev/null

    # Copy skill files
    echo "→ Installing skill files..."
    cp -r "${TEMP_DIR}/powehi-seo-geo/skills/powehi-seo/"* "${SKILL_DIR}/"

    # Copy sub-skills
    if [ -d "${TEMP_DIR}/powehi-seo-geo/skills" ]; then
        for skill_dir in "${TEMP_DIR}/powehi-seo-geo/skills"/*/; do
            skill_name=$(basename "${skill_dir}")
            target="${HOME}/.claude/skills/${skill_name}"
            mkdir -p "${target}"
            cp -r "${skill_dir}"* "${target}/"
        done
    fi

    # Copy schema templates
    if [ -d "${TEMP_DIR}/powehi-seo-geo/schema" ]; then
        mkdir -p "${SKILL_DIR}/schema"
        cp -r "${TEMP_DIR}/powehi-seo-geo/schema/"* "${SKILL_DIR}/schema/"
    fi

    # Copy reference docs
    if [ -d "${TEMP_DIR}/powehi-seo-geo/pdf" ]; then
        mkdir -p "${SKILL_DIR}/pdf"
        cp -r "${TEMP_DIR}/powehi-seo-geo/pdf/"* "${SKILL_DIR}/pdf/"
    fi

    # Copy agents
    echo "→ Installing subagents..."
    cp -r "${TEMP_DIR}/powehi-seo-geo/agents/"*.md "${AGENT_DIR}/" 2>/dev/null || true

    # Copy shared scripts
    if [ -d "${TEMP_DIR}/powehi-seo-geo/scripts" ]; then
        mkdir -p "${SKILL_DIR}/scripts"
        cp -r "${TEMP_DIR}/powehi-seo-geo/scripts/"* "${SKILL_DIR}/scripts/"
    fi

    # Copy the stable runtime launcher. Manual installs use its explicit path;
    # plugin installs expose the repository bin/ directory automatically.
    if [ -f "${TEMP_DIR}/powehi-seo-geo/bin/powehi-seo-geo" ]; then
        mkdir -p "${SKILL_DIR}/bin"
        cp "${TEMP_DIR}/powehi-seo-geo/bin/powehi-seo-geo" "${SKILL_DIR}/bin/powehi-seo-geo"
        chmod +x "${SKILL_DIR}/bin/powehi-seo-geo"
        if [ -f "${TEMP_DIR}/powehi-seo-geo/bin/claude-seo" ]; then
            cp "${TEMP_DIR}/powehi-seo-geo/bin/claude-seo" "${SKILL_DIR}/bin/claude-seo"
            chmod +x "${SKILL_DIR}/bin/claude-seo"
        fi
    fi

    # Copy hooks
    if [ -d "${TEMP_DIR}/powehi-seo-geo/hooks" ]; then
        mkdir -p "${SKILL_DIR}/hooks"
        cp -r "${TEMP_DIR}/powehi-seo-geo/hooks/"* "${SKILL_DIR}/hooks/"
        chmod +x "${SKILL_DIR}/hooks/"*.sh 2>/dev/null || true
        chmod +x "${SKILL_DIR}/hooks/"*.py 2>/dev/null || true
        # Manual installs copy hook files only; enforcement loads through the plugin manifest.
        echo "  Note: hook enforcement requires plugin install (/plugin install ${REPO_URL}); manual hook copy is best-effort."
    fi

    # Copy extensions (optional add-ons: dataforseo, banana)
    if [ -d "${TEMP_DIR}/powehi-seo-geo/extensions" ]; then
        echo "=> Installing extensions..."
        for ext_dir in "${TEMP_DIR}/powehi-seo-geo/extensions"/*/; do
            [ -d "${ext_dir}" ] || continue
            ext_name=$(basename "${ext_dir}")
            # Extension skills
            if [ -d "${ext_dir}skills" ]; then
                for ext_skill in "${ext_dir}skills"/*/; do
                    [ -d "${ext_skill}" ] || continue
                    ext_skill_name=$(basename "${ext_skill}")
                    target="${HOME}/.claude/skills/${ext_skill_name}"
                    mkdir -p "${target}"
                    cp -r "${ext_skill}"* "${target}/"
                done
            fi
            # Extension agents
            if [ -d "${ext_dir}agents" ]; then
                cp -r "${ext_dir}agents/"*.md "${AGENT_DIR}/" 2>/dev/null || true
            fi
            # Extension references
            if [ -d "${ext_dir}references" ]; then
                mkdir -p "${SKILL_DIR}/extensions/${ext_name}/references"
                cp -r "${ext_dir}references/"* "${SKILL_DIR}/extensions/${ext_name}/references/"
            fi
            # Extension scripts
            if [ -d "${ext_dir}scripts" ]; then
                mkdir -p "${SKILL_DIR}/extensions/${ext_name}/scripts"
                cp -r "${ext_dir}scripts/"* "${SKILL_DIR}/extensions/${ext_name}/scripts/"
            fi
        done
    fi

    # Record exactly what this install owns. The uninstaller deletes only the
    # entries listed here, so a third-party skill or agent that happens to be
    # named seo-* is never removed by a wildcard.
    MANIFEST="${SKILL_DIR}/.install-manifest"
    : > "${MANIFEST}"
    chmod 600 "${MANIFEST}" 2>/dev/null || true
    record_manifest() { printf '%s:%s\n' "$1" "$2" >> "${MANIFEST}"; }

    for source_root in "${TEMP_DIR}/powehi-seo-geo/skills"/* \
                       "${TEMP_DIR}/powehi-seo-geo/extensions"/*/skills/*; do
        [ -d "${source_root}" ] || continue
        record_manifest skill "$(basename "${source_root}")"
    done
    for source_doc in "${TEMP_DIR}/powehi-seo-geo/agents"/*.md \
                      "${TEMP_DIR}/powehi-seo-geo/extensions"/*/agents/*.md; do
        [ -f "${source_doc}" ] || continue
        record_manifest agent "$(basename "${source_doc}")"
    done

    # Copy requirements.txt to skill dir so users can retry later
    cp "${TEMP_DIR}/powehi-seo-geo/requirements.txt" "${SKILL_DIR}/requirements.txt" 2>/dev/null || true
    cp "${TEMP_DIR}/powehi-seo-geo/.claude-plugin/plugin.json" "${SKILL_DIR}/runtime-plugin.json" 2>/dev/null || true

    # Manual installs cannot rely on plugin bin/ PATH injection. Rewrite only
    # exact files copied from this checkout during this install.
    rewrite_doc() {
        local doc="$1" temp_doc
        temp_doc="${doc}.powehi-seo-geo-tmp"
        sed -e 's#powehi-seo-geo run#"$HOME/.claude/skills/powehi-seo/bin/powehi-seo-geo" run#g' \
            -e 's#powehi-seo-geo setup#"$HOME/.claude/skills/powehi-seo/bin/powehi-seo-geo" setup#g' \
            -e 's#powehi-seo-geo doctor#"$HOME/.claude/skills/powehi-seo/bin/powehi-seo-geo" doctor#g' \
            "${doc}" > "${temp_doc}"
        mv "${temp_doc}" "${doc}"
    }
    for source_root in "${TEMP_DIR}/powehi-seo-geo/skills"/*; do
        [ -d "${source_root}" ] || continue
        skill_name=$(basename "${source_root}")
        while IFS= read -r -d '' source_doc; do
            relative_doc=${source_doc#"${source_root}/"}
            doc="${HOME}/.claude/skills/${skill_name}/${relative_doc}"
            [ -f "${doc}" ] && rewrite_doc "${doc}"
        done < <(find "${source_root}" -type f -name '*.md' -print0)
    done
    for source_root in "${TEMP_DIR}/powehi-seo-geo/extensions"/*/skills/*; do
        [ -d "${source_root}" ] || continue
        skill_name=$(basename "${source_root}")
        while IFS= read -r -d '' source_doc; do
            relative_doc=${source_doc#"${source_root}/"}
            doc="${HOME}/.claude/skills/${skill_name}/${relative_doc}"
            [ -f "${doc}" ] && rewrite_doc "${doc}"
        done < <(find "${source_root}" -type f -name '*.md' -print0)
    done
    for source_root in "${TEMP_DIR}/powehi-seo-geo/extensions"/*/references; do
        [ -d "${source_root}" ] || continue
        ext_name=$(basename "$(dirname "${source_root}")")
        while IFS= read -r -d '' source_doc; do
            relative_doc=${source_doc#"${source_root}/"}
            doc="${SKILL_DIR}/extensions/${ext_name}/references/${relative_doc}"
            [ -f "${doc}" ] && rewrite_doc "${doc}"
        done < <(find "${source_root}" -type f -name '*.md' -print0)
    done
    for source_doc in "${TEMP_DIR}/powehi-seo-geo/agents"/*.md "${TEMP_DIR}/powehi-seo-geo/extensions"/*/agents/*.md; do
        [ -f "${source_doc}" ] || continue
        doc="${AGENT_DIR}/$(basename "${source_doc}")"
        [ -f "${doc}" ] && rewrite_doc "${doc}"
    done

    echo "→ Creating isolated Python runtime..."
    set +e
    "${SKILL_DIR}/bin/powehi-seo-geo" setup
    runtime_status=$?
    set -e
    if [ "${runtime_status}" -ne 0 ] && [ "${runtime_status}" -ne 10 ]; then
        echo "✗ Core Python runtime setup failed. Installation is incomplete." >&2
        exit 1
    elif [ "${runtime_status}" -eq 10 ]; then
        echo "⚠ Core runtime installed, but Chromium setup is incomplete." >&2
    fi

    echo ""
    echo "✓ Powehi Universal SEO installed successfully!"
    echo ""
    echo "Usage:"
    echo "  1. Start Claude Code:  claude"
    echo "  2. Run commands:       /powehi-seo audit https://example.com"
    echo ""
    echo "Python deps location: ${SKILL_DIR}/requirements.txt"
    echo "Inspect remote scripts before piping them to bash."
    echo "To uninstall: curl -fsSL ${REPO_URL}/raw/main/uninstall.sh | bash"
}

main "$@"

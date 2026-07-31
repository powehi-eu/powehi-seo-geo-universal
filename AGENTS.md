# Powehi Universal SEO: Multi-Platform Agent Instructions

> For **Cursor**, **Cursor Cloud Agents**, **Google Antigravity**, **Gemini CLI**,
> **Grok Build**,
> **OpenAI Codex CLI**, **Cline**, **Aider**, and any other agent harness that
> reads project-root agent instructions.
>
> Claude Code users: see `CLAUDE.md` instead.

## Cross-platform portability (v2.0.0)

Every skill in `skills/*/SKILL.md` is authored to a portable subset of the
Claude Code skill spec. Validate compatibility with your harness via:

```bash
./bin/powehi-seo-geo run portability_check.py
```

The check confirms each `SKILL.md` has the minimum frontmatter every harness
expects (`name`, `description`, optional `model`, optional `tools`) and warns
on Claude-Code-specific features (`maxTurns`, multi-line tool list with
descriptive comments) that other harnesses may ignore but do not reject.

### Per-harness notes

| Harness | How to load powehi-seo-geo |
|---|---|
| **Cursor** | Symlink or copy `skills/` and `agents/` into `.cursor/rules/`. Commands are invoked as text prompts; the harness reads `SKILL.md` body as system context. |
| **Cursor Cloud Agents** | Push the repo; Cloud Agents read `AGENTS.md` automatically at session start. |
| **Google Antigravity** | Point the workspace at this repo root; Antigravity reads `AGENTS.md` first, falls back to `skills/`. |
| **Gemini CLI** | `gemini init` in this repo loads `AGENTS.md`. Skills are activated via `activate_skill <name>` in conversation. |
| **Grok Build** | Open this repository in Grok Build. It reads `AGENTS.md` and Claude Code compatible plugins and skills without a separate layout. Use `grok inspect` to verify discovery. See the [official compatibility guide](https://docs.x.ai/build/features/skills-plugins-marketplaces). |
| **OpenAI Codex CLI** | Reads `AGENTS.md` from project root. Bash tools work as documented; some Claude-specific tool names (Read/Write/Edit) are aliased to Codex equivalents transparently. |
| **Cline** | Loads `AGENTS.md` from project root. Skills appear as system messages; subagent delegation falls back to in-context expansion. |
| **Aider** | Reads `AGENTS.md` if present; otherwise falls back to README. Aider does not support sub-agent dispatch; the seo-* skills run inline. |

### Tool-name compatibility

Where powehi-seo-geo skills mention Claude Code tools (`Read`, `Write`, `Edit`,
`Bash`, `Glob`, `Grep`, `WebFetch`), each harness typically has an equivalent:

| Claude Code | Codex | Cline | Aider | Cursor / Antigravity |
|---|---|---|---|---|
| Read       | read_file        | read_file       | (inline)        | read |
| Write      | write_file       | write_file      | /add then edit  | write |
| Edit       | apply_diff       | replace_in_file | /edit           | edit |
| Bash       | bash             | execute_command | /run            | shell |
| Glob       | glob             | search_files    | (inline)        | find |
| Grep       | grep             | search_files    | /grep           | grep |
| WebFetch   | fetch / browse   | (browser tool)  | (n/a)           | fetch |

These mappings are automatic in most harnesses; we list them for transparency
in case a recipe needs a specific call.

## Overview

Powehi Universal SEO is a Tier 4 SEO analysis skill with 25 sub-skills (21 core + 1 orchestrator +
1 framework integration + 2 extension mirrors), 18 sub-agents (15 core + 1 framework
integration + 2 extension mirrors), and 53 Python execution scripts.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/powehi-seo audit <url>` | Full website audit with parallel subagent delegation |
| `/powehi-seo page <url>` | Deep single-page analysis |
| `/powehi-seo technical <url>` | Technical SEO audit (9 categories) |
| `/powehi-seo content <url>` | E-E-A-T and content quality analysis |
| `/powehi-seo content-brief <topic>` | Generate a content brief for a topic |
| `/powehi-seo schema <url>` | Schema.org detection, validation, generation |
| `/powehi-seo sitemap <url>` | XML sitemap analysis or generation |
| `/powehi-seo images <url>` | Image SEO: on-page audit, SERP analysis, file optimization |
| `/powehi-seo geo <url>` | AI Overviews / Generative Engine Optimization |
| `/powehi-seo plan <type>` | Strategic SEO planning |
| `/powehi-seo cluster <keyword>` | SERP-based semantic clustering and content architecture |
| `/powehi-seo sxo <url>` | Search Experience Optimization: page-type analysis, personas |
| `/powehi-seo drift baseline <url>` | Capture SEO baseline for change monitoring |
| `/powehi-seo drift compare <url>` | Compare current state to stored baseline |
| `/powehi-seo drift history <url>` | Show drift history over time |
| `/powehi-seo ecommerce <url>` | E-commerce SEO: product schema, marketplace intelligence |
| `/powehi-seo programmatic [url]` | Programmatic SEO at scale |
| `/powehi-seo competitor-pages [url]` | Competitor comparison pages |
| `/powehi-seo flow [stage]` | FLOW framework prompts (Find, Leverage, Optimize, Win, Local; prompts/sync utilities.) |
| `/powehi-seo local <url>` | Local SEO analysis (GBP, citations, reviews) |
| `/powehi-seo maps [cmd] [args]` | Maps intelligence (geo-grid, GBP audit, competitors) |
| `/powehi-seo hreflang <url>` | Hreflang/i18n SEO audit, cultural profiles, content parity |
| `/powehi-seo google [cmd] [url]` | Google SEO APIs (GSC, PageSpeed, CrUX, Indexing, GA4) |
| `/powehi-seo backlinks <url>` | Backlink profile analysis |
| `/powehi-seo backlinks setup` | Setup free backlink APIs |
| `/powehi-seo backlinks verify <url>` | Verify known backlinks still exist |
| `/powehi-seo dataforseo [cmd]` | Live SEO data via DataForSEO (extension) |
| `/powehi-seo image-gen [use-case]` | AI image generation for SEO assets (extension) |
| `/powehi-seo firecrawl [cmd] <url>` | Full-site crawling and site mapping (extension) |
| `/powehi-seo ahrefs [cmd] <target>` | Ahrefs backlink and keyword data (extension) |
| `/powehi-seo bing [cmd] <url>` | Bing Webmaster data and IndexNow (extension) |
| `/powehi-seo profound [cmd]` | LLM brand-citation tracking (extension) |
| `/powehi-seo seranking [cmd]` | AI share-of-voice tracking (extension) |
| `/powehi-seo unlighthouse <url>` | Multi-page Lighthouse audits (extension) |

## Using with Cursor / Cursor Cloud

Cursor reads this file automatically. All SKILL.md files contain the full
analysis logic as natural language instructions. Python scripts in `scripts/`
provide execution capabilities.

**Running scripts directly** (Cursor doesn't have MCP):
```bash
# Page fetching with SSRF protection
./bin/powehi-seo-geo run fetch_page.py https://example.com

# HTML parsing for SEO elements
./bin/powehi-seo-geo run parse_html.py https://example.com

# PageSpeed Insights
./bin/powehi-seo-geo run pagespeed_check.py https://example.com --json

# Drift baseline
./bin/powehi-seo-geo run drift_baseline.py https://example.com

# DataForSEO (requires credentials)
DATAFORSEO_USERNAME=user DATAFORSEO_PASSWORD=pass ./bin/powehi-seo-geo run dataforseo_merchant.py search "keyword"
```

**Cursor Cloud gotchas:**
- SSL certificates may not resolve for some domains. Investigate the certificate issue rather than disabling verification.
- Run bundled tools through `powehi-seo-geo`; never call the venv interpreter directly.
- Screenshots save to `/tmp/` not CWD. Check absolute paths.

## Using with Google Antigravity

Antigravity discovers this project via `.claude-plugin/plugin.json`.
Place the repo in `~/.gemini/antigravity/plugins/powehi-seo-geo/` or install via:

```bash
bash install.sh
```

## Architecture

```
skills/                    # 25 sub-skills (auto-discovered)
  powehi-seo/SKILL.md     # Main orchestrator + routing
  seo-cluster/            # Semantic clustering (v1.9.0)
  seo-sxo/                # Search Experience Optimization (v1.9.0)
  seo-drift/              # SEO drift monitoring (v1.9.0)
  seo-ecommerce/          # E-commerce SEO (v1.9.0)
  seo-audit/              # Full site audit
  seo-page/               # Single-page analysis
  seo-technical/          # Technical SEO
  seo-content/            # E-E-A-T quality
  seo-content-brief/      # Content brief generation
  seo-schema/             # Schema.org markup
  seo-sitemap/            # XML sitemaps
  seo-images/             # Image optimization
  seo-geo/                # AI search / GEO
  seo-local/              # Local SEO
  seo-maps/               # Maps intelligence
  seo-plan/               # Strategic planning
  seo-hreflang/           # International SEO
  seo-google/             # Google APIs
  seo-backlinks/          # Backlink analysis
  seo-programmatic/       # Programmatic SEO
  seo-competitor-pages/   # Competitor pages
  seo-flow/               # FLOW framework integration
  seo-dataforseo/         # DataForSEO (extension)
  seo-image-gen/          # AI images (extension)
agents/                    # 18 subagents
scripts/                   # 53 Python scripts, including the managed runtime
schema/                    # JSON-LD templates
extensions/                # 8 MCP extensions: DataForSEO, Firecrawl, Banana, Ahrefs, SE Ranking, Profound, Bing Webmaster, Unlighthouse
```

## Key Principles

1. **Progressive Disclosure**: Read SKILL.md for routing, load references on demand
2. **Industry Detection**: Auto-detect SaaS, e-commerce, local, publisher, agency
3. **Security**: All scripts call `validate_url()` for SSRF protection
4. **Config location**: `~/.config/powehi-seo-geo/` for API credentials

## Credits

Maintained by [Powehi](https://powehi.eu). Original and third-party
attributions are preserved in `LICENSE`, `CONTRIBUTORS.md`, and
`docs/UPSTREAM.md`.
v1.9.0 community contributions by Lutfiya Miller, Chris Muller, Florian Schmitz,
Dan Colta, and Matej Marjanovic. See [CONTRIBUTORS.md](CONTRIBUTORS.md).

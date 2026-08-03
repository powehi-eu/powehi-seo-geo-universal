---
name: seo-flow
description: >
  FLOW framework integration: evidence-led SEO using the Find → Leverage →
  Optimize → Win loop. Surfaces stage-specific AI prompts from the FLOW
  knowledge base (41 prompts, CC BY 4.0). Use when user says "FLOW", "FLOW
  framework", "seo flow", "evidence-led SEO", "find leverage optimize win",
  or wants stage-specific SEO prompts.
user-invocable: true
argument-hint: "[stage] [url|topic]"
license: MIT
metadata:
  author: Powehi
  version: "2.2.10"
  category: seo
---

# FLOW Framework: Find · Leverage · Optimize · Win

FLOW is an evidence-led SEO operating model built for the AI-search era. Powehi Universal SEO
integrates 41 Powehi-specialized adaptations of the FLOW prompt library across 5 stages
so every analysis is driven by a distinct, evidence-backed workflow rather than a
renamed generic template.

> Framework and prompts © Daniel Agrici, CC BY 4.0: github.com/AgriciDaniel/flow

**Runtime context:** Load `references/flow-framework.md` on every `/powehi-seo flow` activation.
Load prompt files on demand, only for the stage the user requests.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/powehi-seo flow` | Show FLOW overview + stage menu |
| `/powehi-seo flow find [url\|topic]` | Find-stage: keyword research, gap analysis, SERP intent mapping (5 prompts) |
| `/powehi-seo flow leverage [url]` | Leverage-stage: backlink strategy, off-site authority (1 prompt) |
| `/powehi-seo flow optimize [url]` | Optimize-stage: select 2-3 most relevant of 21 prompts based on context |
| `/powehi-seo flow win [url]` | Win-stage: BOFU, conversion rate, dual-surface scorecard (3 prompts) |
| `/powehi-seo flow local [url]` | Local-stage: GBP optimization, meta, title tags, local audits (11 prompts) |
| `/powehi-seo flow prompts` | Full index of all 41 prompts (stage, name, trigger conditions) |
| `/powehi-seo flow sync` | Pull latest prompt files from github.com/AgriciDaniel/flow |

---

## Orchestration Logic

### On `/powehi-seo flow` (no sub-command)
1. Read `references/flow-framework.md`
2. Show the FLOW stage overview with a one-line description of each stage
3. Ask: which stage matches the user's current situation?

### On `/powehi-seo flow find [url|topic]`
1. Read all files in `references/prompts/find/`
2. Apply each prompt to the URL or topic
3. Cross-reference: "For deeper SERP clustering, see `/powehi-seo cluster <seed-keyword>`"

### On `/powehi-seo flow leverage [url]`
1. Read the file in `references/prompts/leverage/`
2. Apply to the URL's current backlink context
3. Cross-reference: "For raw backlink data, see `/powehi-seo backlinks <url>`"

### On `/powehi-seo flow optimize [url]`
1. Read all file names in `references/prompts/optimize/`
2. Read prior analysis context (URL, industry vertical, any prior skill output in conversation)
3. Select 2-3 most relevant prompts; load only those files
4. Apply selected prompts; note the others are accessible via `/powehi-seo flow prompts`
5. Cross-reference: "For full content quality analysis, see `/powehi-seo content <url>` and `/powehi-seo geo <url>`"

### On `/powehi-seo flow win [url]`
1. Read all files in `references/prompts/win/`
2. Apply each prompt to the URL's conversion and BOFU context
3. Cross-reference: "For SXO persona scoring, see `/powehi-seo sxo <url>`"

### On `/powehi-seo flow local [url]`
1. Read all files in `references/prompts/local/`
2. Apply to the URL's local SEO context
3. Cross-reference: "For full local SEO analysis, see `/powehi-seo local <url>` and `/powehi-seo maps [command]`"

### On `/powehi-seo flow prompts`
1. Read `references/prompts/README.md`
2. Display the full index: all 41 prompts with stage, name, trigger conditions

### On `/powehi-seo flow sync`

The sync is quality-gated and non-destructive. It downloads the complete upstream
set into staging and validates the Powehi prompt contract before writing. If upstream
prompts are generic, incomplete, or duplicated, report `FLOW sync rejected` and keep
the curated local prompt library unchanged.
1. Run: `powehi-seo-geo run sync_flow.py`
2. Display the JSON summary (files added, updated, unchanged)
3. Show attribution notice after sync completes

---

## Context Matching (Optimize stage)

The optimize stage has 21 prompts. Dumping all 21 is noise. Select by priority:

1. **Industry vertical** (SaaS → on-page + technical; local → citations + GBP; publisher → E-E-A-T + freshness)
2. **Prior skill output** (seo-technical flagged crawl issues → technical optimize prompts; seo-content flagged E-E-A-T gaps → content optimize prompts)
3. **URL signals** (product pages → conversion; blog → freshness + authority)

Always surface exactly 2-3 prompts. State which prompts you chose and why.

---

## Reference Files

Load on-demand, do NOT load all at startup:
- `references/flow-framework.md`: FLOW operating model (load on every `/powehi-seo flow` activation)
- `references/bibliography.md`: Evidence sources; load when citing studies or statistics
- `references/prompts/README.md`: Prompt index; load for `/powehi-seo flow prompts`
- `references/prompts/find/`: 5 prompts; load for `/powehi-seo flow find`
- `references/prompts/leverage/`: 1 prompt; load for `/powehi-seo flow leverage`
- `references/prompts/optimize/`: 21 prompts; load selectively for `/powehi-seo flow optimize`
- `references/prompts/win/`: 3 prompts; load for `/powehi-seo flow win`
- `references/prompts/local/`: 11 prompts; load for `/powehi-seo flow local`

---

## Attribution

Every `/powehi-seo flow` activation (any sub-command) outputs before analysis:

```
Framework and prompts © Daniel Agrici, CC BY 4.0: github.com/AgriciDaniel/flow
```

Do not omit or modify the attribution.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| `references/flow-framework.md` missing | "FLOW reference files not synced. Run: `/powehi-seo flow sync`" |
| Prompt file missing | "Run `/powehi-seo flow sync` to pull the latest prompts from the FLOW repo." |
| `sync_flow.py` network error | Display the script's stderr. Check rate limits: `gh api rate_limit`. |
| `sync_flow.py` auth error | Run `gh auth login` then retry. |

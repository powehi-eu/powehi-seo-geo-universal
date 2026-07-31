---
name: seo-audit
description: "Full website SEO audit with parallel subagent delegation. Crawls up to 500 pages, detects business type, delegates to up to 15 specialists (8 always + 7 conditional), generates health score. Use when user says audit, full SEO check, analyze my site, or website health check."
user-invocable: true
argument-hint: "[url]"
license: MIT
metadata:
  author: Powehi
  version: "2.2.5"
  category: seo
---

# Full Website SEO Audit

## Process

1. **Initialize a fresh run**: create `{domain}-audit/runs/{run_id}/`, record
   `started_at`, target, generator version, and any older audit selected as a
   baseline. Never present pre-existing artifacts as the current run.
2. **Discover capabilities**: read
   `references/capability-contract.md`, discover native tools/MCP connectors,
   and test GSC, GA4, CrUX/PageSpeed, and backlinks independently. Persist
   `capability-discovery.json`. Local credential checks are fallbacks and never
   prove a native capability absent.
3. **Render homepage**: use `powehi-seo-geo run render_page.py <url> --mode auto --json` to capture raw HTML, rendered HTML, extracted text, SPA status, and accessibility data when needed
4. **Detect business type**: analyze homepage signals per seo orchestrator
5. **Crawl site**: follow internal links up to 500 pages, respect robots.txt
6. **Delegate to subagents** (if available, otherwise run inline sequentially):
   - `seo-technical` -- robots.txt, sitemaps, canonicals, Core Web Vitals, security headers
   - `seo-content` -- E-E-A-T, readability, thin content, AI citation readiness
   - `seo-schema` -- detection, validation, generation recommendations
   - `seo-sitemap` -- structure analysis, quality gates, missing pages
   - `seo-performance` -- LCP, INP, CLS measurements
   - `seo-visual` -- screenshots, mobile testing, above-fold analysis
   - `seo-geo` -- AI crawler access, llms.txt, citability, brand mention signals
   - `seo-local` -- GBP signals, NAP consistency, reviews, local schema, industry-specific local factors (spawn when Local Service industry detected: brick-and-mortar, SAB, or hybrid business type)
   - `seo-maps` -- Geo-grid rank tracking, GBP audit, review intelligence, competitor radius mapping (spawn when Local Service detected AND DataForSEO MCP available)
   - `seo-google` -- always run: collect every usable GSC, GA4, CrUX, or
     PageSpeed capability, or write capability-report-only findings with exact
     reasons when none is usable
   - `seo-backlinks` -- always run: use the best authenticated provider, fall
     back to Common Crawl, or write an explicit unavailable result
   - `seo-cluster` -- Semantic clustering analysis (spawn when content strategy signals detected: blog, pillar pages, topic clusters)
   - `seo-sxo` -- Search experience analysis: page-type mismatch, user stories, persona scoring (always include in full audits)
   - `seo-drift` -- Drift analysis: compare against stored baseline (spawn when drift baseline exists for the URL via `powehi-seo-geo run drift_history.py <url>`)
   - `seo-ecommerce` -- Product schema, marketplace intelligence (spawn when E-commerce industry detected)
7. **Persist every specialist result** -- each launched agent writes both its
   Markdown finding and structured JSON result, including terminal status and
   errors.
8. **Merge and validate** -- merge the run into `audit-data.json`, preserving
   source, evidence type, freshness, and capability status.
9. **Score** -- aggregate into SEO Health Score (0-100).
10. **Generate reports** -- always generate `FULL-AUDIT-REPORT.md` and
    `ACTION-PLAN.md`; generate HTML/PDF when dependencies are available and
    record an explicit unavailable reason otherwise.
11. **Verify artifacts** -- run
    `powehi-seo-geo run audit_contract.py validate --run-dir <run_dir> --json`.
    Report exact artifact paths only after validation.

## Crawl Configuration

```
Max pages: 500
Respect robots.txt: Yes
Follow redirects: Yes (max 3 hops)
Timeout per page: 30 seconds
Concurrent requests: 5
Delay between requests: 1 second
```

## Output Files

- `{domain}-audit/FULL-AUDIT-REPORT.md`: Comprehensive findings
- `{domain}-audit/ACTION-PLAN.md`: Prioritized recommendations (Critical > High > Medium > Low)
- `{domain}-audit/audit-data.json`: Structured audit envelope for report generation
- `{domain}-audit/findings/*.md`: Per-category specialist findings (`technical.md`, `content.md`, `schema.md`, `performance.md`, `visual.md`, etc.)
- `{domain}-audit/screenshots/`: Desktop + mobile captures (if Playwright available)
- **PDF Report** (recommended): Generate a professional A4 PDF using `powehi-seo-geo run google_report.py --type full --data {domain}-audit/audit-data.json --domain <domain> --output-dir {domain}-audit/`. This produces a white-cover enterprise report with TOC, executive summary, charts (Lighthouse gauges, query bars, index donut), metric cards, threshold tables, prioritized recommendations with effort estimates, and implementation roadmap. Always offer PDF generation after completing an audit.

The canonical storage is `{domain}-audit/runs/{run_id}/`. Root-level report
paths may be compatibility copies or pointers to the validated latest run.
HTML/PDF generation is attempted automatically. A missing report dependency is
recorded in `audit-data.json`; it does not invalidate the mandatory Markdown
and JSON artifacts.

## Structured Audit Data Envelope

Write `{domain}-audit/audit-data.json` with this shape so `powehi-seo-geo run google_report.py --type full --data {domain}-audit/audit-data.json --domain <domain> --output-dir {domain}-audit/` can generate a report even when Google API data is unavailable:

```json
{
  "schema_version": "2.0",
  "generator": {
    "name": "Powehi Universal SEO",
    "version": "2.2.5"
  },
  "audit_run": {
    "run_id": "ISO-8601-safe identifier",
    "target": "https://example.com/",
    "started_at": "ISO-8601 timestamp",
    "completed_at": "ISO-8601 timestamp",
    "status": "completed|completed_with_errors|failed",
    "source": "live",
    "baseline_used": false
  },
  "capabilities": {},
  "summary": {
    "health_score": 0,
    "business_type": "detected type",
    "top_findings": [],
    "quick_wins": []
  },
  "categories": [
    {
      "name": "Technical SEO",
      "score": 0,
      "what_works": [],
      "findings": [
        {
          "title": "Finding title",
          "severity": "Critical|High|Medium|Low|Info",
          "status": "passed|failed|unavailable|insufficient_data|partial",
          "source": "live_http|rendered_page|build|gsc|ga4|crux|pagespeed|lighthouse|backlinks",
          "evidence_type": "observed|field_data|lab_data|inferred",
          "freshness": {},
          "description": "Evidence-backed detail",
          "recommendation": "Specific fix"
        }
      ]
    }
  ],
  "action_plan": {
    "phases": [
      {"name": "Phase 1: Critical Fixes", "timeframe": "Week 1", "items": []},
      {"name": "Phase 2: High-Impact Improvements", "timeframe": "Weeks 2-3", "items": []},
      {"name": "Phase 3: Content & Authority", "timeframe": "Month 2", "items": []},
      {"name": "Phase 4: Monitoring & Iteration", "timeframe": "Ongoing", "items": []}
    ]
  },
  "artifacts": {
    "findings_dir": "findings/",
    "screenshots_dir": "screenshots/"
  }
}
```

## Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

## Report Structure

### Executive Summary
- Overall SEO Health Score (0-100)
- Business type detected
- Top 5 critical issues
- Top 5 quick wins

### Technical SEO
- Crawlability issues
- Indexability problems
- Security concerns
- Core Web Vitals status

### Content Quality
- E-E-A-T assessment
- Thin content pages
- Duplicate content issues
- Readability scores

### On-Page SEO
- Title tag issues
- Meta description problems
- Heading structure
- Internal linking gaps

### Schema & Structured Data
- Current implementation
- Validation errors
- Missing opportunities

### Performance
- LCP, INP, CLS scores
- Resource optimization needs
- Third-party script impact

### Images
- Missing alt text
- Oversized images
- Format recommendations

### AI Search Readiness
- Citability score
- Structural improvements
- Authority signals

## Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, spawn the `seo-dataforseo` agent alongside existing subagents to enrich the audit with live data: real SERP positions, backlink profiles with spam scores, on-page analysis (Lighthouse), business listings, and AI visibility checks (ChatGPT scraper, LLM mentions).

## Google API Integration (Optional)

If Google API credentials are configured (`powehi-seo-geo run google_auth.py --check`), spawn the `seo-google` agent to enrich the audit with real Google field data: CrUX Core Web Vitals (replaces lab-only estimates), GSC URL indexation status, search performance (clicks, impressions, CTR), and GA4 organic traffic trends. The Performance (CWV) category score benefits most from field data.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| robots.txt blocks crawling | Report which paths are blocked. Analyze only accessible pages and note the limitation in the report. |
| Rate limiting (429 responses) | Back off and reduce concurrent requests. Report partial results with a note on which sections could not be completed. |
| Timeout on large sites (500+ pages) | Cap the crawl at the timeout limit. Report findings for pages crawled and estimate total site scope. |
| Native connector unavailable or unauthenticated | Continue independent capability checks, use the best fallback, and persist the exact redacted reason. |
| PDF/HTML dependency missing | Preserve Markdown/JSON success and record the optional artifact as unavailable. |
| Existing audit directory | Treat prior artifacts as a baseline; create a fresh timestamped run. |

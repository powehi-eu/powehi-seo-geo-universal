> **Languages:** [Français](OPENCLAW-HERMES.fr.md) | English

# OpenClaw and Hermes distribution

The repository keeps one portable `skills/` source tree and publishes two
native consumption paths:

## OpenClaw

The root `openclaw.plugin.json` declares the native OpenClaw plugin and the
`openclaw/index.js` runtime adapter. For local verification:

```bash
openclaw plugins install --link .
openclaw plugins enable powehi-universal-seo-geo
openclaw gateway restart
openclaw plugins inspect powehi-universal-seo-geo --runtime --json
```

The same repository can be submitted to ClawHub after the package metadata and
release tag are available. Users then install it with:

```bash
openclaw plugins install clawhub:powehi-universal-seo-geo
```

## Hermes Agent

Hermes consumes the portable skills directly. Add this repository as a tap:

```bash
hermes skills tap add powehi-eu/powehi-seo-geo-universal
hermes skills search seo --source github
hermes skills install powehi-eu/powehi-seo-geo-universal/skills/powehi-seo
```

For a local checkout, configure `external_dirs` in `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - H:/powehi-seo-geo-universal/skills
```

The Hermes surface is intentionally skill-based; it does not require a second
runtime or a duplicated copy of the SEO scripts.

## ClawHub listing position

Powehi Universal SEO should be presented as a **modular evidence-backed SEO &
GEO intelligence suite**, not as a generic SEO checklist or a single
competitor-analysis prompt.

For transparency, it should also be identified as a **Powehi-maintained fork
and evolution of [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)**.
The upstream project and third-party contributions remain credited in
`LICENSE`, `CONTRIBUTORS.md` and `docs/UPSTREAM.md`. Universal adds the Powehi
identity, cross-platform packaging, evidence controls, runtime safeguards,
extensions and GEO-oriented workflows.

It is designed for users who need to:

- audit a full site across crawlability, rendering, indexability, performance,
  metadata, schema, content, links, local and ecommerce SEO;
- verify evidence separately at source, build and live URL level;
- connect Google Search Console, GA4, CrUX and PageSpeed independently;
- optimize visibility in ChatGPT, Google AI Overviews, Gemini and Perplexity;
- turn findings into a prioritized, reproducible implementation plan;
- extend the workflow with optional Firecrawl, Ahrefs, DataForSEO, Bing,
  SE Ranking and brand-citation connectors.

The package contains 33 portable skills and 18 specialist agents. Its
differentiator is the combination of breadth, evidence controls, progressive
specialization and cross-agent portability across Claude Code, Codex, Cursor,
OpenClaw and Hermes.

### ClawHub description

Use the following description for the first publication:

> Powehi Universal SEO & GEO is a modular evidence-backed SEO intelligence suite
> and a Powehi-maintained fork and evolution of AgriciDaniel/claude-seo,
> for full-site audits, technical SEO, content, schema, local, ecommerce,
> backlinks, Google Search Console, GA4, PageSpeed, CrUX, sitemaps, hreflang,
> image SEO, AI search visibility, and competitor research. Use it when you need
> more than a checklist: verify a live website, separate source/build/live
> evidence, crawl pages, inspect rendered HTML, validate structured data, measure
> Google performance, optimize for ChatGPT, Google AI Overviews, Gemini and
> Perplexity, or turn findings into a prioritized implementation plan. Includes
> 33 portable specialist skills, 18 agents, reproducible reports, drift
> monitoring, SSRF-safe fetchers, and optional MCP extensions for Firecrawl,
> Ahrefs, DataForSEO, Bing, SE Ranking and brand-citation research. Works with
> Claude Code, Codex, Cursor, OpenClaw and Hermes.

### Publish and update workflow

From the repository root, validate before publishing:

```bash
clawhub package validate .
clawhub package publish . --family code-plugin --dry-run
clawhub package publish . --family code-plugin
```

Every later update follows the same process after changing the repository
version and changelog. ClawHub stores immutable version records; installed
users can update with:

```bash
openclaw plugins update clawhub:powehi-universal-seo-geo
```

Do not publish a release until the package metadata, plugin manifest and
release version agree. Review the automated security result before announcing
the release.

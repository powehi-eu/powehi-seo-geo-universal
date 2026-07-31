> **Languages:** [Français](COMMANDS.fr.md) | English

# Commands Reference

## Overview

All Powehi Universal SEO commands start with `/powehi-seo` followed by a subcommand.

## Command List

### `/powehi-seo setup`

Explicitly create or refresh the isolated Python runtime and Playwright Chromium.
This is required once after a marketplace plugin install. Manual installers run
the same setup automatically. It never installs packages globally.

### `/powehi-seo doctor`

Check runtime, dependency, and Chromium readiness without changing the system.
Diagnostic output omits absolute paths and environment values.

### `/powehi-seo audit <url>`

Full website SEO audit with parallel analysis.

**Example:**
```
/powehi-seo audit https://example.com
```

**What it does:**
1. Crawls up to 500 pages
2. Detects business type
3. Delegates to up to 15 specialist subagents in parallel (8 always-on + 7 conditional)
4. Generates SEO Health Score (0-100)
5. Creates prioritized action plan

**Output:**
- `FULL-AUDIT-REPORT.md`
- `ACTION-PLAN.md`
- `screenshots/` (if Playwright available)

---

### `/powehi-seo page <url>`

Deep single-page analysis.

**Example:**
```
/powehi-seo page https://example.com/about
```

**What it analyzes:**
- On-page SEO (title, meta, headings, URLs)
- Content quality (word count, readability, E-E-A-T)
- Technical elements (canonical, robots, Open Graph)
- Schema markup
- Images (alt text, sizes, formats)
- Core Web Vitals potential issues

---

### `/powehi-seo technical <url>`

Technical SEO audit across 9 categories.

**Example:**
```
/powehi-seo technical https://example.com
```

**Categories:**
1. Crawlability
2. Indexability
3. Security
4. URL Structure
5. Mobile Optimization
6. Core Web Vitals (LCP, INP, CLS)
7. Structured Data
8. JavaScript Rendering
9. IndexNow Protocol

---

### `/powehi-seo content <url>`

E-E-A-T and content quality analysis.

**Example:**
```
/powehi-seo content https://example.com/blog/post
```

**What it evaluates:**
- Experience signals (first-hand knowledge)
- Expertise (author credentials)
- Authoritativeness (external recognition)
- Trustworthiness (transparency, security)
- AI citation readiness
- Content freshness

---

### `/powehi-seo content-brief <topic or url>`

Generate a detailed SEO content brief: target keywords, search intent, heading outline, internal link targets, and competitor angle.

**Example:**
```
/powehi-seo content-brief "best running shoes for flat feet"
```

**What it produces:**
- Primary and secondary target keywords
- Search intent and audience
- Section-by-section heading outline
- Internal link recommendations
- Competitor content angles to beat

---

### `/powehi-seo schema <url>`

Schema markup detection, validation, and generation.

**Example:**
```
/powehi-seo schema https://example.com
```

**What it does:**
- Detects existing schema (JSON-LD, Microdata, RDFa)
- Validates against Google's requirements
- Identifies missing opportunities
- Generates ready-to-use JSON-LD

---

### `/powehi-seo geo <url>`

AI Overviews / Generative Engine Optimization.

**Example:**
```
/powehi-seo geo https://example.com/blog/guide
```

**What it analyzes:**
- Citability score (quotable facts, statistics)
- Structural readability (headings, lists, tables)
- Entity clarity (definitions, context)
- Authority signals (credentials, sources)
- Structured data support

---

### `/powehi-seo images <url>`

Image optimization analysis. Subcommands: `serp <keyword>` (image SERP / visual-search analysis), `optimize <path>` (local file optimization + IPTC AI labeling).

**Examples:**
```
/powehi-seo images https://example.com
/powehi-seo images serp "running shoes"
/powehi-seo images optimize ./hero.webp
```

**What it checks:**
- Alt text presence and quality
- File sizes (flag >200KB)
- Formats (WebP/AVIF recommendations)
- Responsive images (srcset, sizes)
- Lazy loading
- CLS prevention (dimensions)

---

### `/powehi-seo sitemap <url>`

Analyze existing XML sitemap.

**Example:**
```
/powehi-seo sitemap https://example.com/sitemap.xml
```

**What it validates:**
- XML format
- URL count (<50k per file)
- URL status codes
- lastmod accuracy
- Deprecated tags (priority, changefreq)
- Coverage vs crawled pages

---

### `/powehi-seo sitemap generate`

Generate new sitemap with industry templates.

**Example:**
```
/powehi-seo sitemap generate
```

**Process:**
1. Select or auto-detect business type
2. Interactive structure planning
3. Apply quality gates (30/50 location page limits)
4. Generate valid XML
5. Create documentation

---

### `/powehi-seo plan <type>`

Strategic SEO planning.

**Types:** `saas`, `local`, `ecommerce`, `publisher`, `agency`

**Example:**
```
/powehi-seo plan saas
```

**What it creates:**
- Complete SEO strategy
- Competitive analysis
- Content calendar
- Implementation roadmap (4 phases)
- Site architecture design

---

### `/powehi-seo competitor-pages [url|generate]`

Competitor comparison page generation.

**Examples:**
```
/powehi-seo competitor-pages https://example.com/vs/competitor
/powehi-seo competitor-pages generate
```

**Capabilities:**
- Generate "X vs Y" comparison page layouts
- Create "Alternatives to X" page structures
- Build feature comparison matrices with scoring
- Generate Product + AggregateRating schema markup
- Apply conversion-optimized CTA placement
- Enforce fairness guidelines (accurate data, source citations)

---

### `/powehi-seo hreflang [url]`

Hreflang and international SEO audit and generation. Subcommand: `audit <directory-or-url>` (audit hreflang across a local build directory or a live URL set).

**Examples:**
```
/powehi-seo hreflang https://example.com
/powehi-seo hreflang audit ./dist
```

**Capabilities:**
- Validate self-referencing hreflang tags
- Check return tag reciprocity (A→B requires B→A)
- Verify x-default tag presence
- Validate ISO 639-1 language and ISO 3166-1 region codes
- Check canonical URL alignment with hreflang
- Detect protocol mismatches (HTTP vs HTTPS)
- Generate correct hreflang link tags and sitemap XML

---

### `/powehi-seo programmatic [url|plan]`

Programmatic SEO analysis and planning for pages generated at scale.

**Examples:**
```
/powehi-seo programmatic https://example.com/tools/
/powehi-seo programmatic plan
```

**Capabilities:**
- Assess data source quality (CSV, JSON, API, database)
- Plan template engines with unique content per page
- Design URL pattern strategies (`/tools/[tool-name]`, `/[city]/[service]`)
- Automate internal linking (hub/spoke, related items, breadcrumbs)
- Enforce thin content safeguards (quality gates, word count thresholds)
- Prevent index bloat (noindex low-value, pagination, faceted nav)

---

### `/powehi-seo local <url>`

Local SEO analysis covering Google Business Profile, citations, reviews, and the map pack.

**Example:**
```
/powehi-seo local https://example.com
```

**What it analyzes:**
- Google Business Profile signals (categories, hours, photos, posts)
- NAP (Name, Address, Phone) consistency across the page and external citations
- Review velocity, response rate, and sentiment
- Local schema markup (LocalBusiness, Restaurant, Service-specific types)
- Industry-specific local factors (brick-and-mortar, SAB, hybrid)
- Map pack visibility signals

---

### `/powehi-seo maps [command] [args]`

Maps intelligence: geo-grid rank tracking, GBP profile audits, review intelligence, cross-platform NAP verification, competitor radius mapping.

**Examples:**
```
/powehi-seo maps "Joe's Coffee" "austin tx"
/powehi-seo maps grid "coffee shop" "austin tx"
/powehi-seo maps gbp "Joe's Coffee" "austin tx"
/powehi-seo maps reviews "Joe's Coffee" "austin tx"
/powehi-seo maps competitors "auto repair" "denver"
/powehi-seo maps nap "Joe's Coffee" "austin tx"
/powehi-seo maps schema "Joe's Coffee" "austin tx"
```

**Capabilities:**
- Rank tracking on a geographic grid (typically 49 points)
- GBP profile audit with completeness scoring
- Review aggregation across Google, Yelp, Facebook, Bing
- Competitor discovery within a configurable radius

---

### `/powehi-seo backlinks <url>`

Backlink profile analysis with a 3-tier data cascade: free (Common Crawl + verification), free with signup (Moz, Bing Webmaster Tools), paid (DataForSEO).

**Examples:**
```
/powehi-seo backlinks https://example.com
/powehi-seo backlinks gap https://example.com https://competitor.com
/powehi-seo backlinks toxic https://example.com
/powehi-seo backlinks new https://example.com
/powehi-seo backlinks verify https://example.com --links known-links.txt
/powehi-seo backlinks setup
```

**What it analyzes:**
- Domain Authority and Page Authority (Moz)
- Referring domain count and growth
- Anchor text distribution (branded, exact, partial, naked URL)
- Toxic / spammy backlink detection
- Lost backlinks
- Competitor link gap

---

### `/powehi-seo cluster [command] <seed-keyword>`

SERP-based semantic topic clustering for content architecture planning. Built on the Pro Hub Challenge Semantic Cluster Engine. Subcommands: `plan <seed>` (full planning workflow; also `plan --from strategy` to import a `/powehi-seo plan` output), `execute` (create content via claude-blog or output briefs), `map` (regenerate the interactive visualization). Bare `/powehi-seo cluster <seed>` is shorthand for `plan`.

**Examples:**
```
/powehi-seo cluster plan "claude code skills"
/powehi-seo cluster plan --from strategy
/powehi-seo cluster execute
/powehi-seo cluster map
```

**What it produces:**
- Keyword expansion from the seed (50-200 candidates)
- Pairwise SERP overlap comparison to detect semantic clusters
- Intent classification per cluster (informational, commercial, transactional, navigational)
- Hub-and-spoke content architecture proposal
- Internal link matrix between cluster pages
- Interactive `cluster-map.html` visualization

---

### `/powehi-seo sxo <url>`

Search Experience Optimization: SERP backwards analysis, page-type mismatch detection, persona scoring. Subcommands: `<url> <keyword>` (analyze for a specific keyword), `wireframe <url>` (IST/SOLL wireframe), `personas <url>` (persona-only scoring, skips SERP).

**Examples:**
```
/powehi-seo sxo https://example.com/blog/how-to-x
/powehi-seo sxo https://example.com/page "target keyword"
/powehi-seo sxo wireframe https://example.com/page
/powehi-seo sxo personas https://example.com/page
```

**What it produces:**
- Page-type taxonomy classification (article, landing, product, tool, listing)
- SERP intent vs page-type alignment check
- User stories derived from SERP signals
- Multi-persona scoring (researcher, buyer, expert, casual visitor)
- Wireframe-level recommendations for fixing mismatches

---

### `/powehi-seo drift baseline|compare|history <url>`

SEO drift monitoring. Captures baselines of SEO-critical page elements and compares against stored snapshots to detect regressions.

**Examples:**
```
/powehi-seo drift baseline https://example.com
/powehi-seo drift compare https://example.com
/powehi-seo drift history https://example.com
```

**What it tracks:** title, meta description, canonical, hreflang, Open Graph, schema, headings, internal links, robots, sitemap entry, indexability, Core Web Vitals, response status, redirect chain.

**17 comparison rules** classify changes by severity (CRITICAL, HIGH, MEDIUM). SQLite-backed baselines.

---

### `/powehi-seo ecommerce <url>`

E-commerce SEO covering product schema, marketplace intelligence, and pricing gap analysis. Subcommands: `products <keyword>` (Google Shopping competitive analysis), `gaps <domain>` (organic-vs-Shopping visibility gap), `schema <url>` (product schema validation + enhancement).

**Examples:**
```
/powehi-seo ecommerce https://shop.example.com/product/x
/powehi-seo ecommerce products "running shoes"
/powehi-seo ecommerce gaps shop.example.com
/powehi-seo ecommerce schema https://shop.example.com/product/x
```

**What it analyzes:**
- Product schema (Product, Offer, AggregateRating, Review)
- Google Shopping visibility
- Amazon marketplace presence
- Pricing gap vs competitors
- Out-of-stock and availability signals
- Faceted navigation crawl traps

---

### `/powehi-seo flow [stage] [url|topic]`

FLOW framework integration: evidence-led prompts for the Find, Leverage, Optimize, Win, and Local stages of a content campaign.

**Examples:**
```
/powehi-seo flow find "topic"
/powehi-seo flow leverage https://example.com
/powehi-seo flow optimize https://example.com/page
/powehi-seo flow win https://example.com/page
/powehi-seo flow local https://example.com
/powehi-seo flow prompts
/powehi-seo flow sync
```

**41 prompts** sourced from FLOW (CC BY 4.0). Each prompt is grounded in a specific evidence source (SERP data, GSC, GA4, customer interviews) with attribution preserved.

---

### `/powehi-seo google [command] [url]`

Google SEO APIs. 4-tier credential system covering PageSpeed Insights, CrUX, CrUX History, Search Console, URL Inspection, Indexing API, GA4, and Keyword Planner.

**Setup & reporting:**
```
/powehi-seo google setup                      # Configure/check credentials
/powehi-seo google quotas                     # Show per-API quota usage
/powehi-seo google report full                # Generate full PDF/HTML report
/powehi-seo google report cwv-audit           # CWV-focused report
/powehi-seo google report gsc-performance     # Search performance report
/powehi-seo google report indexation          # Indexation status report
```

**PageSpeed / CrUX (Tier 0):**
```
/powehi-seo google pagespeed <url>            # PageSpeed Insights (lab) + CWV
/powehi-seo google crux <url>                 # CrUX field data
/powehi-seo google crux-history <url>         # 25-week CrUX history
```

**Search Console / Indexing (Tier 1):**
```
/powehi-seo google gsc <property>             # Search Analytics (clicks/impressions/CTR/position)
/powehi-seo google inspect <url>              # URL Inspection (indexation status)
/powehi-seo google inspect-batch <file>       # Batch URL inspection
/powehi-seo google sitemaps <property>        # List submitted sitemaps + status
/powehi-seo google index <url>                # Indexing API notify
/powehi-seo google index-batch <file>         # Batch indexing notify
```
Use Indexing API commands only for pages with JobPosting or BroadcastEvent embedded in VideoObject. Route ordinary URLs to URL Inspection or sitemaps; `URL_UPDATED` does not guarantee indexing.

**GA4 (Tier 2):**
```
/powehi-seo google ga4 [property-id]          # Organic traffic report
/powehi-seo google ga4-pages [property-id]    # Top organic landing pages
```

**NLP / Keywords / YouTube:**
```
/powehi-seo google nlp <url-or-text>          # NLP content analysis
/powehi-seo google entities <url-or-text>     # Entity extraction
/powehi-seo google entity <query>             # Entity lookup
/powehi-seo google keywords <seed>            # Keyword Planner ideas (Tier 3)
/powehi-seo google volume <keywords>          # Keyword search volume (Tier 3)
/powehi-seo google youtube <query>            # YouTube search
/powehi-seo google youtube-video <video_id>   # YouTube video analysis
/powehi-seo google safety <url>               # Safe Browsing check
```

**Tiers:**
- Tier 0 (API key only): PSI, CrUX, CrUX History
- Tier 1 (+ OAuth or Service Account): GSC, URL Inspection, Indexing API
- Tier 2 (+ GA4 property config): GA4 organic traffic
- Tier 3 (+ Google Ads developer token): Keyword Planner

PDF and HTML reports generated via WeasyPrint and matplotlib.

---

### `/powehi-seo image-gen [use-case] <description>`

AI image generation for SEO assets (extension). Powered by Gemini via nanobanana-mcp.

**Prerequisites:** Banana extension installed (`./extensions/banana/install.sh`)

**Use Cases:**
```
/powehi-seo image-gen og <description>          # OG/social preview image (16:9, 1K)
/powehi-seo image-gen hero <description>        # Blog hero image (16:9, 2K)
/powehi-seo image-gen product <description>     # Product photography (4:3, 2K)
/powehi-seo image-gen infographic <description> # Infographic visual (2:3, 4K)
/powehi-seo image-gen custom <description>      # Custom with full Creative Director pipeline
/powehi-seo image-gen batch <description> [N]   # Generate N variations (default: 3)
```

**What it does:**
1. Maps SEO use case to optimized domain mode, aspect ratio, and resolution
2. Constructs 6-component Reasoning Brief (Creative Director pipeline)
3. Generates image via Gemini API
4. Provides SEO checklist (alt text, file naming, WebP, schema markup)

---

### `/powehi-seo firecrawl [command] <url>`

Full-site crawling and URL discovery via Firecrawl MCP (extension).

**Prerequisites:** Firecrawl extension installed (`./extensions/firecrawl/install.sh`)

**Examples:**
```
/powehi-seo firecrawl crawl https://example.com
/powehi-seo firecrawl map https://example.com
/powehi-seo firecrawl scrape https://example.com/page
/powehi-seo firecrawl search "query" https://example.com
```

**What it does:**
- `crawl` walks the site discovering URLs and capturing content
- `map` returns the full URL inventory for a domain
- `scrape` extracts a single page in a model-friendly format
- `search` searches within a crawled site for a query

---

### `/powehi-seo dataforseo [command]`

Live SEO data via DataForSEO MCP server (extension). 23 data commands across 9 API modules, plus cost-tracking commands.

**Prerequisites:** DataForSEO extension installed (`./extensions/dataforseo/install.sh`)

**SERP Analysis:**
```
/powehi-seo dataforseo serp <keyword>              # Google organic results (also Bing/Yahoo)
/powehi-seo dataforseo serp-images <keyword>       # Google Images SERP results
/powehi-seo dataforseo serp-youtube <keyword>      # YouTube search results
/powehi-seo dataforseo youtube <video_id>          # YouTube video deep analysis
```

**Keyword Research:**
```
/powehi-seo dataforseo keywords <seed>             # Keyword ideas and suggestions
/powehi-seo dataforseo volume <keywords>           # Search volume metrics
/powehi-seo dataforseo difficulty <keywords>       # Keyword difficulty scores
/powehi-seo dataforseo intent <keywords>           # Search intent classification
/powehi-seo dataforseo trends <keyword>            # Google Trends data
```

**Domain & Competitors:**
```
/powehi-seo dataforseo backlinks <domain>          # Full backlink profile
/powehi-seo dataforseo competitors <domain>        # Competitor analysis
/powehi-seo dataforseo ranked <domain>             # Ranked keywords
/powehi-seo dataforseo intersection <domains>      # Keyword/backlink overlap
/powehi-seo dataforseo traffic <domains>           # Traffic estimation
/powehi-seo dataforseo subdomains <domain>         # Subdomains with ranking data
/powehi-seo dataforseo top-searches <domain>       # Top queries mentioning domain
```

**Technical / On-Page:**
```
/powehi-seo dataforseo onpage <url>                # On-page analysis (Lighthouse)
/powehi-seo dataforseo tech <domain>               # Technology detection
/powehi-seo dataforseo whois <domain>              # WHOIS data
```

**Content & Business Data:**
```
/powehi-seo dataforseo content <keyword/url>       # Content analysis and trends
/powehi-seo dataforseo listings <keyword>          # Business listings search
```

**AI Visibility / GEO:**
```
/powehi-seo dataforseo ai-scrape <query>           # ChatGPT web scraper for GEO
/powehi-seo dataforseo ai-mentions <keyword>       # LLM mention tracking
```

**Cost Tracking:**
```
/powehi-seo dataforseo costs today                            # Today's DataForSEO spend
/powehi-seo dataforseo costs summary                          # Spend summary across periods
/powehi-seo dataforseo costs config --mode threshold --threshold 0.50   # Set cost-control mode/threshold
```

---

### `/powehi-seo ahrefs [command] <url|topic>`

Ahrefs API metrics (extension). **Prerequisites:** Ahrefs extension installed (`./extensions/ahrefs/install.sh`).
```
/powehi-seo ahrefs metrics <url>       # DR/UR, referring-domain count, organic traffic estimate
/powehi-seo ahrefs backlinks <url>     # Top referring domains, anchor distribution, follow/nofollow ratio
/powehi-seo ahrefs organic <url>       # Organic keywords, ranking distribution, traffic by country
/powehi-seo ahrefs content <topic>     # Content Explorer top results, social shares, referring domains
```

---

### `/powehi-seo bing [command]`

Bing Webmaster Tools + IndexNow (extension). **Prerequisites:** Bing extension installed (`./extensions/bing-webmaster/install.sh`).
```
/powehi-seo bing links <url>                 # Inbound links from Bing Webmaster
/powehi-seo bing compare <urlA> <urlB>       # Compare two URLs' Bing link profiles
/powehi-seo bing submit <url> --host <host>                # IndexNow single-URL submit (requires key)
/powehi-seo bing submit-batch <file> --host <host>         # IndexNow batch submit (requires key)
/powehi-seo bing verify-indexnow --host <host>             # Verify the IndexNow key is published
```

---

### `/powehi-seo profound [command] <brand>`

LLM brand-citation tracking via Profound (extension). **Prerequisites:** Profound extension installed.
```
/powehi-seo profound citations <brand>     # Citation rate per LLM + 30-day trend
/powehi-seo profound prompts <brand>       # Top prompts that surface (or miss) the brand
/powehi-seo profound competitors <brand>   # Brands cited alongside yours for the same prompts
/powehi-seo profound alerts <brand>        # Spike/drop alerts vs 7-day baseline
```

---

### `/powehi-seo seranking [command] <brand|keyword|url>`

AI-visibility + SERP via SE Ranking (extension). **Prerequisites:** SE Ranking extension installed.
```
/powehi-seo seranking ai-visibility <brand>   # Share-of-voice across ChatGPT/Gemini/Perplexity/AI Overviews/AI Mode
/powehi-seo seranking serp <keyword>          # Top 100 organic positions + SERP features
/powehi-seo seranking backlinks <url>         # Backlink profile (free-tier alternative to Ahrefs/DataForSEO)
/powehi-seo seranking competitors <url>       # Top 10 organic competitors + shared-keyword gaps
```

---

### `/powehi-seo unlighthouse <url>`

Multi-page Lighthouse audit via Unlighthouse (extension, MIT, no API quota). **Prerequisites:** Node 18+ and the unlighthouse npm package (`./extensions/unlighthouse/install.sh`).
```
/powehi-seo unlighthouse https://example.com
/powehi-seo unlighthouse https://example.com --device desktop
/powehi-seo unlighthouse https://example.com --max-routes 50 --output-dir ./reports
```

---

## Quick Reference

| Command | Use Case |
|---------|----------|
| `/powehi-seo audit <url>` | Full website audit with parallel subagents |
| `/powehi-seo page <url>` | Single page analysis |
| `/powehi-seo technical <url>` | Technical SEO across 9 categories |
| `/powehi-seo content <url>` | E-E-A-T and content quality |
| `/powehi-seo content-brief <topic>` | Detailed content brief: keywords, outline, internal links |
| `/powehi-seo schema <url>` | Schema markup detection, validation, generation |
| `/powehi-seo sitemap <url>` | Sitemap validation |
| `/powehi-seo sitemap generate` | Create new sitemap with industry templates |
| `/powehi-seo images <url>` | Image optimization |
| `/powehi-seo geo <url>` | AI search optimization (GEO) |
| `/powehi-seo local <url>` | Local SEO (GBP, citations, reviews) |
| `/powehi-seo maps [command]` | Maps intelligence (geo-grid, GBP audit, competitors) |
| `/powehi-seo backlinks <url>` | Backlink profile analysis |
| `/powehi-seo cluster <seed>` | SERP-based semantic clustering |
| `/powehi-seo sxo <url>` | Search Experience Optimization |
| `/powehi-seo drift baseline\|compare\|history <url>` | SEO drift monitoring |
| `/powehi-seo ecommerce <url>` | E-commerce SEO |
| `/powehi-seo hreflang [url]` | Hreflang and international SEO |
| `/powehi-seo plan <type>` | Strategic planning by industry |
| `/powehi-seo programmatic [url\|plan]` | Programmatic SEO analysis |
| `/powehi-seo competitor-pages [url\|generate]` | Competitor comparison pages |
| `/powehi-seo flow [stage] [url\|topic]` | FLOW framework prompts |
| `/powehi-seo google [command] [url]` | Google SEO APIs (GSC, PSI, CrUX, GA4) |
| `/powehi-seo dataforseo [command]` | Live SEO data (extension) |
| `/powehi-seo image-gen [use-case] <desc>` | AI image generation (extension) |
| `/powehi-seo firecrawl [command] <url>` | Full-site crawling (extension) |
| `/powehi-seo ahrefs [command] <url>` | Backlinks, organic keywords, and content data via the official Ahrefs MCP (extension) |
| `/powehi-seo seranking [command]` | AI Share-of-Voice across ChatGPT, Gemini, Perplexity, AI Overviews, AI Mode (extension) |
| `/powehi-seo profound [command]` | LLM citation tracking with time-series data (extension) |
| `/powehi-seo bing [command] <url>` | Bing Webmaster Tools + IndexNow URL submission (extension) |
| `/powehi-seo unlighthouse <url>` | Multi-page Lighthouse runner, runs locally (extension) |

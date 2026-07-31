> **Langue :** Français | [English](ARCHITECTURE.md)

# Architecture

## Aperçu

Powehi Universal SEO suit la spécification officielle de compétence Claude Code d'Anthropic avec une architecture modulaire et multi-compétences.

## Structure du répertoire

Le plugin expédie 25 sous-compétences (21 cœur + 1 orchestre + 1 intégration de cadre + 2 miroirs d'extension) et 18 sous-agents (15 cœur + 1 intégration de cadre + 2 miroirs d'extension).

```
~/.claude/plugins/.../powehi-seo-geo/
├── skills/
│   ├── seo/                    # Main orchestrator
│   │   ├── SKILL.md
│   │   └── references/         # On-demand reference files (13 files)
│   │
│   ├── seo-audit/              # Full site audit (parallel subagents)
│   ├── seo-page/               # Single page analysis
│   ├── seo-technical/          # Technical SEO (9 categories)
│   ├── seo-content/            # E-E-A-T and content quality
│   ├── seo-content-brief/      # Competitive content brief generation
│   ├── seo-schema/             # Schema markup detection and generation
│   ├── seo-sitemap/            # XML sitemap analysis and generation
│   ├── seo-images/             # Image optimization analysis
│   ├── seo-geo/                # AI search optimization (GEO)
│   ├── seo-local/              # Local SEO (GBP, citations, reviews)
│   ├── seo-maps/               # Maps intelligence (geo-grid, GBP audit)
│   ├── seo-backlinks/          # Backlink profile analysis
│   ├── seo-cluster/            # Semantic topic clustering (SERP-based)
│   ├── seo-sxo/                # Search Experience Optimization
│   ├── seo-drift/              # SEO drift monitoring (baselines)
│   ├── seo-ecommerce/          # E-commerce SEO (product schema, marketplaces)
│   ├── seo-hreflang/           # International SEO and hreflang
│   ├── seo-plan/               # Strategic SEO planning (industry templates)
│   ├── seo-programmatic/       # Programmatic SEO at scale
│   ├── seo-competitor-pages/   # Competitor comparison page generation
│   ├── seo-google/             # Google SEO APIs (GSC, PSI, CrUX, GA4)
│   ├── seo-flow/               # FLOW framework integration (CC BY 4.0)
│   ├── seo-dataforseo/         # DataForSEO MCP mirror (extension surface)
│   └── seo-image-gen/          # Banana MCP mirror (extension surface)
│
└── agents/
    ├── seo-technical.md        # Crawlability, indexability, security
    ├── seo-content.md          # E-E-A-T, readability, thin content
    ├── seo-schema.md           # Structured data validation
    ├── seo-sitemap.md          # Sitemap quality gates
    ├── seo-performance.md      # Core Web Vitals
    ├── seo-visual.md           # Screenshots, mobile rendering
    ├── seo-geo.md              # AI crawler access, citability
    ├── seo-local.md            # GBP signals, NAP, reviews
    ├── seo-maps.md             # Geo-grid, competitor radius mapping
    ├── seo-backlinks.md        # Moz, Bing Webmaster, Common Crawl
    ├── seo-cluster.md          # Semantic clustering analysis
    ├── seo-sxo.md              # Page-type, user stories, personas
    ├── seo-drift.md            # Baseline comparison, regression detection
    ├── seo-ecommerce.md        # Product schema, marketplace intelligence
    ├── seo-google.md           # GSC, PSI, CrUX, GA4 analyst
    ├── seo-flow.md             # FLOW framework prompt selection
    ├── seo-dataforseo.md       # DataForSEO MCP mirror
    └── seo-image-gen.md        # Banana MCP mirror
```

## Types de composants

### Compétences

Compétences sont des fichiers de balisage avec la matière première YAML qui définissent les capacités et les instructions.

**SKILL.md Format:**
```yaml
---
name: skill-name
description: >
  When to use this skill. Include activation keywords
  and concrete use cases.
---

# Titre de compétence

Instructions and documentation...
```

### Sous-agents

Les sous-agents sont des travailleurs spécialisés qui peuvent se voir déléguer des tâches. Ils ont leur propre contexte et outils.

**Agent Format:**
```yaml
---
name: agent-name
description: What this agent does.
tools: Read, Bash, Write, Glob, Grep
---

Instructions for the agent...
```

### Fichiers de référence

Les fichiers de référence contiennent des données statiques chargées à la demande pour éviter de gonfler la compétence principale.

## Flux d'orchestration

### Full Audit (`/powehi-seo audit`)

```
User request
    │
    ▼
┌──────────────────┐
│   powehi-seo     │  Orchestrateur principal (skills/powehi-seo/SKILL.md)
└────────┬─────────┘
         │  Detects business type and signals
         │  Spawns subagents in parallel
         │
    ┌────┴────┬────────┬────────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│tech   │ │content│ │schema │ │sitemap│ │perf   │ │visual │ │geo    │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │         │         │         │         │         │
    └─────────┴─────────┴────┬────┴─────────┴─────────┴─────────┘
                             │
                             │  Conditional spawns:
                             │  - seo-google     (Google API creds detected)
                             │  - seo-local      (local business detected)
                             │  - seo-maps       (local + DataForSEO MCP)
                             │  - seo-backlinks  (Moz/Bing/CC available)
                             │  - seo-cluster    (content strategy signals)
                             │  - seo-sxo        (always in full audits)
                             │  - seo-drift      (baseline exists for URL)
                             │  - seo-ecommerce  (e-commerce detected)
                             ▼
                    ┌────────────────┐
                    │  Aggregate     │
                    │  Results       │
                    └────────┬───────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Generate      │
                    │  Health Score  │
                    │  + Action Plan │
                    └────────────────┘
```

### Commande individuelle

```
User Request (e.g., /powehi-seo page)
    │
    ▼
┌─────────────────┐
│   seo       │  ← Routes to sub-skill
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   seo-page      │  ← Sub-skill handles directly
│   (SKILL.md)    │
└─────────────────┘
```

## Principes de conception

### 1. Divulgation progressive

- Main SKILL.md reste en dessous de 500 lignes (selon les règles de développement)
- Fichiers de référence chargés sur demande
- Instructions détaillées en sous-compétences

### 2. Traitement parallèle

- Les sous-agents fonctionnent simultanément pendant les audits
- Les analyses indépendantes ne se bloquent pas
- Résultats agrégés après tout terminé

### 3. Portails de qualité

- Les seuils intégrés empêchent les mauvaises recommandations
- Limites de la page de localisation (30 avertissements, 50 arrêts durs)
- Sensibilisation à la déprécation du schéma
- FID → remplacement de l'INP

### 4. Sensibilisation de l'industrie

- Modèles pour différents types d'entreprises
- Détection automatique des signaux de la page d'accueil
- Recommandations adaptées par industrie

## Conventions de désignation de fichiers

Type de modèle Exemple de modèle
C'est quoi ?
Compétence
Agents `seo-{name}.md`
Référence:
Script de `{action}_{target}.py`
Modèle `{industry}.md`

## Points d'extension

### Ajouter une nouvelle sous-compétence

1. Créer `skills/seo-newskill/SKILL.md`
2. Ajouter la matière première YAML avec le nom et la description
3. Écrire des instructions de compétences
4. Mettre à jour le `skills/powehi-seo/SKILL.md` principal pour orienter vers de nouvelles compétences

### Ajouter un nouveau sous-agent

1. Créer `agents/seo-newagent.md`
2. Ajouter la matière première YAML avec nom, description, outils
3. Écrire les instructions de l'agent
4. Référence tirée des compétences pertinentes

### Ajouter un nouveau fichier de référence

1. Créer un fichier dans le répertoire approprié `references/`
2. Référence dans la compétence avec l'instruction sur la charge à la demande

## Extensions

### Gestion de l'exécution de Python

Les outils groupés sont expédiés par `bin/powehi-seo-geo` et
`scripts/runtime.py`, jamais à travers une commande python relative au répertoire de travail.
Le lanceur résout Python 3.10 ou plus récent, alors que l'exécution standard-bibliothèque
fournit trois opérations: `run`, `setup` et en lecture seule `doctor`.

Les environnements de plugin vivent sous `CLAUDE_PLUGIN_DATA` persistante. Installation manuelle
conserver l'emplacement compatible `~/.claude/skills/powehi-seo/.venv`. Un marqueur d'état enregistre
le schéma d'exécution, les exigences SHA-256, Python version majeure et mineure, public
version plugin, et état du navigateur. Exigences, régime d'exécution ou ABI Python
les modifications nécessitent une configuration explicite ; une différence de version seulement reste compatible et
est rafraîchi sur la prochaine configuration. Le remplacement de l'environnement est échelonné et laminé
retour si la validation ou la publication de marqueurs échoue.

`run` accepte uniquement les noms de base des scripts listés ou un script d'extension contenu.
Il transmet les arguments sans shell, préserve les codes de sortie pour enfants, force UTF-8
flux d'enfant, et utilise le même répertoire permanent Playwright navigateur créé
par installation.

Les extensions sont des add-ons opt-in qui intègrent des sources de données externes via les serveurs MCP. Ils vivent dans `extensions/<name>/` et expédient leurs propres scripts d'installation / désinstallation.

```
extensions/
├── dataforseo/               # DataForSEO MCP integration
│   ├── README.md
│   ├── install.sh
│   ├── install.ps1
│   ├── uninstall.sh
│   ├── uninstall.ps1
│   ├── field-config.json
│   ├── skills/seo-dataforseo/SKILL.md
│   ├── agents/seo-dataforseo.md
│   └── docs/DATAFORSEO-SETUP.md
│
├── banana/                   # AI image generation via Gemini
│   ├── README.md
│   ├── install.sh
│   ├── uninstall.sh
│   ├── skills/seo-image-gen/SKILL.md
│   ├── agents/seo-image-gen.md
│   ├── scripts/              # Python fallback scripts (stdlib only)
│   ├── references/           # 7 reference files (prompt engineering, models, presets)
│   └── docs/BANANA-SETUP.md
│
├── firecrawl/                # Firecrawl MCP for full-site crawling
│   ├── README.md
│   ├── install.sh
│   ├── install.ps1
│   ├── uninstall.sh
│   ├── uninstall.ps1
│   └── skills/seo-firecrawl/SKILL.md
│
├── ahrefs/                   # Ahrefs MCP for backlinks + organic data
│   ├── install.sh
│   ├── install.ps1
│   ├── uninstall.sh
│   ├── skills/seo-ahrefs/SKILL.md
│   └── docs/AHREFS-SETUP.md
│
├── seranking/                # SE Ranking AI Share-of-Voice tracking
│   ├── install.sh
│   ├── install.ps1
│   ├── uninstall.sh
│   ├── skills/seo-seranking/SKILL.md
│   └── docs/SERANKING-SETUP.md
│
├── profound/                 # Profound LLM citation tracking
│   ├── install.sh
│   ├── install.ps1
│   ├── uninstall.sh
│   ├── skills/seo-profound/SKILL.md
│   └── docs/PROFOUND-SETUP.md
│
├── bing-webmaster/           # Bing Webmaster Tools + IndexNow
│   ├── install.sh
│   ├── install.ps1
│   ├── uninstall.sh
│   ├── skills/seo-bing/SKILL.md
│   └── docs/BING-WEBMASTER-SETUP.md
│
└── unlighthouse/             # Multi-page Lighthouse runner (local)
    ├── install.sh
    ├── install.ps1
    ├── uninstall.sh
    ├── skills/seo-unlighthouse/SKILL.md
    └── docs/UNLIGHTHOUSE-SETUP.md
```

### Extensions disponibles

Package d ' extension Ce qu'il ajoute
- Commande
*DataForSEO**= `dataforseo-mcp-server@2.8.10`= Données SERP en direct, recherche par mots-clés, backlinks, analyse en page, listes d'entreprises, visibilité AI, LLM mention tracking
**Banana Image Gen**= `@ycse/nanobanana-mcp@1.1.1`= Génération d'images AI pour les actifs SEO via Gemini (OG images, images de héros, photos de produits, infographies, batch)=
**Firecrawl**= `firecrawl-mcp@3.11.0`=                                                                                                                                                                                                                                              
*Ahrefs**= `@ahrefs/mcp@0.0.11`= Retours et données de mots clés organiques via le serveur officiel `@ahrefs/mcp`=
**SE Classement**=SE Classement API=AI Part-of-Voice sur ChatGPT, Gemini, Perplexité, Aperçus AI et Mode AI=
**Profound**
**Bing Webmaster**"Bing Webmaster Tools API"Bing Webmaster Tools + soumission d'URL IndexNow
*Unlighthouse**=`unlighthouse@0.13.5`=Runner de phare multipage, tourne localement

### Convention de prorogation

1. Autocontenu en `extensions/<name>/`
2. `install.sh` propre (et `install.ps1` où Windows est pris en charge) qui copie les fichiers et configure MCP (le cas échéant)
3. Posséder `uninstall.sh` (et `uninstall.ps1` le cas échéant) qui inverse l'installation
4. Installe le miroir sous-kill dans le répertoire des compétences du plugin
5. Installe le miroir sous-agent dans le répertoire de l'agent du plugin (extensions qui expédient une ; les extensions plus légères ne sont que des compétences)
6. Configment Merges MCP dans `~/.claude/settings.json` non destructivement
7. Les versions du serveur MCP sont épinglées (`@<version>`) pour la stabilité de la chaîne d'approvisionnement

> **Langue :** Français | [English](COMMANDS.md)

# Référence des commandes

## Aperçu

Toutes les commandes Powehi Universal SEO commencent par `/powehi-seo` suivie d'une sous-commande.

## Liste des commandes

### `/powehi-seo setup`

Créez ou rafraîchissez explicitement l'exécution isolée de Python et Playwright Chromium.
Ceci est nécessaire une fois après l'installation d'un plugin de marché. Exécution des installateurs manuels
la même configuration automatiquement. Il n'installe jamais les paquets au niveau mondial.

### `/powehi-seo doctor`

Vérifiez le temps d'exécution, la dépendance et la préparation au chrome sans changer le système.
La sortie diagnostique omet les chemins absolus et les valeurs d'environnement.

### `/powehi-seo audit <url>`

Site web complet Audit SEO avec analyse parallèle.

**Example:**
```
/powehi-seo audit https://example.com
```

**Ce qu'il fait:**
1. Explore jusqu’à 500 pages
2. Détecte le type d'entreprise
3. Délégués jusqu ' à 15 sous-agents spécialisés en parallèle (8 toujours sur + 7 conditionnels)
4. Génére une cote de santé SEO (0-100)
5. Crée un plan d'action prioritaire

**Résultats:**
- `FULL-AUDIT-REPORT.md`
- `ACTION-PLAN.md`
- `screenshots/` (si Playwright est disponible)

---

### `/powehi-seo page <url>`

Analyse en profondeur d'une seule page.

**Example:**
```
/powehi-seo page https://example.com/about
```

**Ce qu'il analyse:**
- Sur la page SEO (titre, méta, rubriques, URL)
- Qualité du contenu (nombre de mots, lisibilité, E-E-A-T)
- Éléments techniques (canoniques, robots, Open Graph)
- Plan du schéma
- Images (texte Alt, tailles, formats)
- Principaux problèmes potentiels concernant les éléments vitaux du Web

---

### `/powehi-seo technical <url>`

Vérification technique SEO dans 9 catégories.

**Example:**
```
/powehi-seo technical https://example.com
```

**Catégories:**
1. Crawlabilité
2. Indexabilité
3. Sécurité
4. Structure de l'URL
5. Optimisation mobile
6. Principaux éléments vitaux du Web (LCP, INP, CLS)
7. Données structurées
8. Rendu JavaScript
9. Protocole IndexNow

---

### `/powehi-seo content <url>`

E-E-A-T et analyse de la qualité du contenu.

**Example:**
```
/powehi-seo content https://example.com/blog/post
```

**Ce qu'il évalue:**
- Signaux d'expérience (connaissance de première main)
- Expertise (certificats d'auteur)
- Pouvoir (reconnaissance externe)
- Fiabilité (transparence, sécurité)
- Préparation à la citation AI
- Refroidissement du contenu

---

### `/powehi-seo content-brief <topic or url>`

Générer un sommaire détaillé du contenu de SEO : mots-clés de la cible, intention de recherche, contour de l'en-tête, cibles de liaison interne et angle de compétition.

**Example:**
```
/powehi-seo content-brief "best running shoes for flat feet"
```

**Ce qu'il produit:**
- Mots clés cibles primaires et secondaires
- Objet de la recherche et public
- Esquisse du titre section par section
- Recommandations relatives aux liens internes
- Angles de contenu des concurrents à battre

---

### `/powehi-seo schema <url>`

Détection, validation et génération du schéma.

**Example:**
```
/powehi-seo schema https://example.com
```

**Ce qu'il fait:**
- Détecte le schéma existant (JSON-LD, Microdonnées, RDFa)
- Valide par rapport aux exigences de Google
- Indique les possibilités manquantes
- Génére JSON-LD prêt à l'emploi

---

### `/powehi-seo geo <url>`

Aperçus AI / Optimisation du moteur.

**Example:**
```
/powehi-seo geo https://example.com/blog/guide
```

**Ce qu'il analyse:**
- Score de citabilité (faits chiffrés, statistiques)
- Lisibilité structurelle (en-têtes, listes, tableaux)
- clarté de l'entité (définitions, contexte)
- Signaux d'autorité (crédences, sources)
- Prise en charge structurée des données

---

### `/powehi-seo images <url>`

Analyse d'optimisation d'image. Sous-commandes : `serp <keyword>` (analyse image SERP / recherche visuelle), `optimize <path>` (optimisation des fichiers locaux + étiquetage IPTC AI).

**Examples:**
```
/powehi-seo images https://example.com
/powehi-seo images serp "running shoes"
/powehi-seo images optimize ./hero.webp
```

**Ce qu'il vérifie:**
- Présence et qualité de texte Alt
- Taille des fichiers (flag >200Ko)
- Formats (recommandations WebP/AVIF)
- Images réactives (srcset, tailles)
- Chargement paresseux
- Prévention du SLC (dimensions)

---

### `/powehi-seo sitemap <url>`

Analyser le plan du site XML existant.

**Example:**
```
/powehi-seo sitemap https://example.com/sitemap.xml
```

**Ce qu'il valide:**
- Format XML
- Nombre d'URL (<50k par fichier)
- Codes d'état des URL
- précision du dernier mode
- Balises obsolètes (priorité, changefreq)
- Couverture vs pages rampées

---

### `/powehi-seo sitemap generate`

Générer une nouvelle carte du site avec des modèles industriels.

**Example:**
```
/powehi-seo sitemap generate
```

**Processus:**
1. Sélectionnez ou détectez automatiquement le type d'entreprise
2. Planification des structures interactives
3. Appliquer des barrières de qualité (30/50 limites de page de localisation)
4. Générer XML valide
5. Créer une documentation

---

### `/powehi-seo plan <type>`

Planification stratégique SEO.

**Types:** `saas`, `local`, `ecommerce`, `publisher`, `agency`

**Example:**
```
/powehi-seo plan saas
```

**Ce qu'il crée:**
- Stratégie SEO complète
- Analyse concurrentielle
- Calendrier des contenus
- Feuille de route de mise en œuvre (4 phases)
- Architecture du site

---

### `/powehi-seo competitor-pages [url|generate]`

Génération de pages de comparaison des concurrents.

**Examples:**
```
/powehi-seo competitor-pages https://example.com/vs/competitor
/powehi-seo competitor-pages generate
```

**Capacités**
- Générer des mises en page de comparaison "X vs Y"
- Créer des structures de pages "Alternatives à X"
- Construisez des matrices de comparaison avec la notation
- Générer produit + schéma de notation agrégé
- Appliquer le placement CTA optimisé par conversion
- Appliquer les lignes directrices en matière d'équité (données exactes, citations sources)

---

### `/powehi-seo hreflang [url]`

Audit et génération de Hreflang et SEO internationaux. Sous-commande : `audit <directory-or-url>` (audit hreflang à travers un répertoire de construction local ou un ensemble d'URL en direct).

**Examples:**
```
/powehi-seo hreflang https://example.com
/powehi-seo hreflang audit ./dist
```

**Capacités**
- Valider les balises hreflang auto-référencées
- Vérifier la réciprocité de l'étiquette de retour (A→B exige B→A)
- Vérifier la présence de la balise x par défaut
- Valider la langue ISO 639-1 et les codes régionaux ISO 3166-1
- Vérifier l'alignement canonique de l'URL avec hreflang
- Détecter les erreurs de protocole (HTTP vs HTTPS)
- Générer des balises de lien hreflang correctes et plan du site XML

---

### `/powehi-seo programmatic [url|plan]`

Analyse et planification programmatiques SEO pour les pages générées à l'échelle.

**Examples:**
```
/powehi-seo programmatic https://example.com/tools/
/powehi-seo programmatic plan
```

**Capacités**
- Évaluer la qualité des sources de données (CSV, JSON, API, base de données)
- Moteurs de modèle avec un contenu unique par page
- Concevoir des stratégies de patronage d'URL (`/tools/[tool-name]`, `/[city]/[service]`)
- Automatiser la liaison interne (hub/sur mesure, articles associés, chapelure)
- Appliquer des garanties de faible teneur (portes de qualité, seuils de nombre de mots)
- Prévenir le ballonnement de l'index (noindex de faible valeur, pagination, nav à face)

---

### `/powehi-seo local <url>`

Analyse locale SEO couvrant le profil d'affaires de Google, les citations, les revues et le pack de cartes.

**Example:**
```
/powehi-seo local https://example.com
```

**Ce qu'il analyse:**
- Google Business Profile signaux (catégories, heures, photos, messages)
- Cohérence du PAN (nom, adresse, téléphone) sur la page et les citations externes
- Examiner la vitesse, le taux de réponse et le sentiment
- Marquage du schéma local (affaires locales, restaurant, types de services spécifiques)
- Facteurs locaux propres à l'industrie (brique et mortaire, SAB, hybride)
- Signalisations de visibilité des paquets de cartes

---

### `/powehi-seo maps [command] [args]`

Intelligence des cartes : suivi du rang géogrille, audits de profil GBP, renseignement d'examen, vérification du PAN multiplateforme, cartographie du rayon des concurrents.

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

**Capacités**
- Suivi du classement sur une grille géographique (généralement 49 points)
- Audit du profil GBP avec notation complète
- Examiner l'agrégation dans Google, Yelp, Facebook, Bing
- Découverte de concurrents dans un rayon configurable

---

### `/powehi-seo backlinks <url>`

Analyse de profil de backlink avec une cascade de données de 3 niveaux: gratuit (Common Crawl + vérification), gratuit avec inscription (Moz, Bing Webmaster Tools), payé (DataForSEO).

**Examples:**
```
/powehi-seo backlinks https://example.com
/powehi-seo backlinks gap https://example.com https://competitor.com
/powehi-seo backlinks toxic https://example.com
/powehi-seo backlinks new https://example.com
/powehi-seo backlinks verify https://example.com --links known-links.txt
/powehi-seo backlinks setup
```

**Ce qu'il analyse:**
- Autorité de domaine et autorité de page (Moz)
- Affectation du nombre de domaines et croissance
- Distribution de texte d'ancrage (marque, exacte, partielle, URL nue)
- Détection de rétroliens toxiques / spammy
- Perte de liens
- Écart de liaison entre concurrents

---

### `/powehi-seo cluster [command] <seed-keyword>`

Sujet sémantique basé sur le SERP clustering pour la planification de l'architecture de contenu. Construit sur le moteur à grappes sémantique Pro Hub Challenge. Sous-commandes: `plan <seed>` (processus de planification complet; également `plan --from strategy` pour importer une sortie `/powehi-seo plan`), `execute` (créer du contenu via claude-blog ou slips de sortie), `map` (régénérer la visualisation interactive). Bare `/powehi-seo cluster <seed>` est shorthand pour `plan`.

**Examples:**
```
/powehi-seo cluster plan "claude code skills"
/powehi-seo cluster plan --from strategy
/powehi-seo cluster execute
/powehi-seo cluster map
```

**Ce qu'il produit:**
- Extension de mots clés à partir de la graine (50-200 candidats)
- Comparaison du chevauchement SERP par paire pour détecter les grappes sémantiques
- Classification des intentions par grappe (information, commerce, transactionnel, navigation)
- Proposition d'architecture de contenu sur mesure
- Matrice de liens internes entre les pages cluster
- Visualisation interactive `cluster-map.html`

---

### `/powehi-seo sxo <url>`

Optimisation de l'expérience de recherche : analyse en arrière du SERP, détection d'erreurs de type page, notation persona. Sous-commandes : `<url> <keyword>` (analyse d'un mot-clé spécifique), `wireframe <url>` (fireframe IST/SOLL), `personas <url>` (score de personne seulement, saute SERP).

**Examples:**
```
/powehi-seo sxo https://example.com/blog/how-to-x
/powehi-seo sxo https://example.com/page "target keyword"
/powehi-seo sxo wireframe https://example.com/page
/powehi-seo sxo personas https://example.com/page
```

**Ce qu'il produit:**
- Classification de taxonomie de type page (article, atterrissage, produit, outil, liste)
- Vérification de l'alignement de l'intention du SERP par rapport au type de page
- Histoires d'utilisateurs dérivées des signaux SERP
- Note multi-personnes (chercheur, acheteur, expert, visiteur occasionnel)
- Recommandations au niveau de l'image filaire pour la fixation des erreurs

---

### `/powehi-seo drift baseline|compare|history <url>`

Surveillance de la dérive SEO. Capture les lignes de base des éléments de page critiques SEO et se compare aux instantanés stockés pour détecter les régressions.

**Examples:**
```
/powehi-seo drift baseline https://example.com
/powehi-seo drift compare https://example.com
/powehi-seo drift history https://example.com
```

**Ce qu'il suit:** title, meta description, canonical, hreflang, Open Graph, schéma, entêtes, liens internes, robots, entrée du sitemap, indexabilité, Core Web Vitals, état de réponse, chaîne de redirection.

**17 règles de comparaison** classer les changements par gravité (CRITIQUE, HAUTE, MOYEN). Bases de référence soutenues par SQLite.

---

### `/powehi-seo ecommerce <url>`

Commerce électronique SEO couvrant le schéma de produit, l'intelligence du marché et l'analyse des écarts de prix. Sous-commandes : `products <keyword>` (analyse de la concurrence Google Shopping), `gaps <domain>` (écart de visibilité bio-vs-Shopping), `schema <url>` (validation du schéma de produit + amélioration).

**Examples:**
```
/powehi-seo ecommerce https://shop.example.com/product/x
/powehi-seo ecommerce products "running shoes"
/powehi-seo ecommerce gaps shop.example.com
/powehi-seo ecommerce schema https://shop.example.com/product/x
```

**Ce qu'il analyse:**
- Schéma du produit (Produit, Offre, Classement agrégé, Révision)
- Visibilité Google Shopping
- présence sur le marché amazonien
- Écart de prix par rapport aux concurrents
- Signaux de sortie et de disponibilité
- Pièges à chenilles de navigation à facettes

---

### `/powehi-seo flow [stage] [url|topic]`

Intégration du framework FLOW : des appels à données probantes pour les étapes Find, Leverage, Optimize, Win et Local d'une campagne de contenu.

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

**41 prompts** issus de FLOW (CC BY 4.0). Chaque prompt s’appuie sur une source de preuve précise (données SERP, GSC, GA4, entretiens clients), avec attribution préservée.

---

### `/powehi-seo google [command] [url]`

APIs Google SEO. Système de reconnaissance 4 niveaux couvrant PageSpeed Insights, CrUX, CrUX Historique, Search Console, URL Inspection, Indexing API, GA4 et Keyword Planner.

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
- Niveau 0 (clé API uniquement): PSI, CrUX, CrUX Historique
- Niveau 1 (+ Compte OAuth ou Service): GSC, URL Inspection, API d'indexation
- Niveau 2 (+ GA4 config propriété): GA4 trafic organique
- Niveau 3 (+ jeton développeur Google Ads): Keyword Planner

Rapports PDF et HTML générés par WeasyPrint et matplotlib.

---

### `/powehi-seo image-gen [use-case] <description>`

Génération d'images AI pour les actifs SEO (extension). Propulsé par Gemini via nanobanana-mcp.

**Préalables:** Extension Banana installée (`./extensions/banana/install.sh`)

**Use Cases:**
```
/powehi-seo image-gen og <description>          # OG/social preview image (16:9, 1K)
/powehi-seo image-gen hero <description>        # Blog hero image (16:9, 2K)
/powehi-seo image-gen product <description>     # Product photography (4:3, 2K)
/powehi-seo image-gen infographic <description> # Infographic visual (2:3, 4K)
/powehi-seo image-gen custom <description>      # Custom with full Creative Director pipeline
/powehi-seo image-gen batch <description> [N]   # Generate N variations (default: 3)
```

**Ce qu'il fait:**
1. Coque d'utilisation Maps SEO pour optimiser le mode de domaine, le rapport d'aspect et la résolution
2. Construction d'un mémoire de motivation à six composantes (composante du directeur exécutif)
3. Génére l'image via l'API Gemini
4. Fournit SEO liste de contrôle (texte Alt, nom de fichier, WebP, balisage schéma)

---

### `/powehi-seo firecrawl [command] <url>`

Déplacement complet et découverte d'URL via Firecrawl MCP (extension).

**Prérequis:** Extension Firecrawl installée (`./extensions/firecrawl/install.sh`)

**Examples:**
```
/powehi-seo firecrawl crawl https://example.com
/powehi-seo firecrawl map https://example.com
/powehi-seo firecrawl scrape https://example.com/page
/powehi-seo firecrawl search "query" https://example.com
```

**Ce qu'il fait:**
- `crawl` marche sur le site en découvrant les URL et en capturant le contenu
- `map` retourne l'inventaire complet d'URL pour un domaine
- `scrape` extrait une seule page dans un format facile à utiliser
- `search` recherche dans un site rampé pour une requête

---

### `/powehi-seo dataforseo [command]`

Données SEO en direct via le serveur DataForSEO MCP (extension). 23 commandes de données sur 9 modules API, plus des commandes de suivi des coûts.

**Préalables:** Extension DataForSEO installée (`./extensions/dataforseo/install.sh`)

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

## Référence rapide

Utiliser le cas d'utilisation
C'est quoi ?
`/powehi-seo audit <url>`= Audit complet du site web avec sous-agents parallèles=
Une seule page d'analyse
`/powehi-seo technical <url>`Q Technique SEO dans 9 catégories
`/powehi-seo content <url>`Q E-E-A-T et qualité du contenu
`/powehi-seo content-brief <topic>`S Brève de contenu détaillée : mots clés, contour, liens internes
Détection, validation, génération
`/powehi-seo sitemap <url>`
Création d'un nouveau plan de site avec des modèles industriels
L'optimisation de l'image
Optimisation de la recherche AI (GEO)
Local SEO (GBP, citations, revues)
`/powehi-seo maps [command]`=Signification des cartes (géo-réseau, audit GBP, concurrents)=
Analyse du profil de rétrolien
Groupement sémantique basé sur le SERP
`/powehi-seo sxo <url>`
Surveillance de la dérive `/powehi-seo drift baseline\|compare\|history <url>`
Commerce en ligne SEO
Hreflang et international SEO
`/powehi-seo plan <type>`
Analyse programmatique SEO
Pages de comparaison des concurrents
structurale `/powehi-seo flow [stage] [url\|topic]`
Google API SEO (GSC, PSI, CrUX, GA4)
`/powehi-seo dataforseo [command]`= Données réelles SEO (extension)=
Génération d'images AI (extension)
`/powehi-seo firecrawl [command] <url>`=Rampage sur site complet (extension)=
Mots-clés organiques et données de contenu via le Ahrefs officiel MCP (extension)
`/powehi-seo seranking [command]`U AI Share-of-Voice à travers ChatGPT, Gemini, Perplexité, AI Overviews, AI Mode (extension)
`/powehi-seo profound [command]`=Le suivi des citations LLM avec les données de séries chronologiques (extension)=
`/powehi-seo bing [command] <url>`= Outils Bing Webmaster + soumission d'URL IndexNow (extension)=
`/powehi-seo unlighthouse <url>`U Coureur de phare multipage, tourne localement (extension)

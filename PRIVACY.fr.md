> **Langue :** Français | [English](PRIVACY.md)

# Confidentialité

## Traitement des données

Powehi Universal SEO est une compétence Claude Code qui fonctionne sur votre machine locale. La compétence de base ne fait pas d'appels d'API tiers par défaut (les audits récupèrent toujours les URLs cibles auxquelles vous les pointez), et ne recueille, ne stocke ou ne transmet aucune donnée personnelle à un fournisseur.

## Ce qui reste local

- Toutes les analyses SEO sont exécutées dans votre session Claude Code
- L'analyse HTML, l'analyse de contenu et la production de rapports se produisent localement
- Les rapports générés (PDF, HTML, Excel) sont enregistrés dans votre système de fichiers local
- Pas de télémétrie, d'analyse ou de suivi d'utilisation

## API d'extension

Les extensions optionnelles font des appels d'API vers des services tiers lorsque vous invoquez leurs commandes :

| Extension | Service | Data Sent | Privacy Policy |
|-----------|---------|-----------|---------------|
| **DataForSEO** | api.dataforseo.com | URLs and domains you analyze | [DataForSEO Privacy](https://dataforseo.com/privacy-policy) |
| **Firecrawl** | api.firecrawl.dev | URLs you crawl or scrape | [Firecrawl Privacy](https://www.firecrawl.dev/privacy) |
| **Banana (Gemini)** | generativelanguage.googleapis.com | Image generation prompts | [Google AI Privacy](https://ai.google.dev/terms) |
| **Ahrefs** | Official `@ahrefs/mcp` server (Ahrefs API) | Domains and URLs you analyze | [Ahrefs Privacy](https://ahrefs.com/privacy) |
| **SE Ranking** | seranking.com/api | Domains and keywords you analyze | [SE Ranking Privacy](https://seranking.com/privacy-policy) |
| **Profound** | Profound API (tryprofound.com) | Brands and domains you track | [Profound Privacy](https://tryprofound.com/privacy) |
| **Bing Webmaster / IndexNow** | Bing Webmaster Tools API and IndexNow endpoints | Domains, submitted URLs, and key-verification URL data | [Microsoft Privacy](https://privacy.microsoft.com/) |
| **Unlighthouse** | Local only — no third-party vendor | Runs Lighthouse locally against the target URL; only the target site is contacted (to crawl it). Nothing is sent to a third-party vendor. | N/A (runs locally) |

## API de rétrolien

Lorsque configurés avec des identifiants d'API backlink, ces scripts transmettent des données à des services tiers :

| Script | Service | Data Sent | Privacy Policy |
|--------|---------|-----------|---------------|
| `moz_api.py` | Moz Link Explorer API | Domains you analyze | [Moz Privacy](https://moz.com/privacy-policy) |
| `bing_webmaster.py` | Bing Webmaster Tools API | Domains you analyze | [Microsoft Privacy](https://privacy.microsoft.com/) |
| `indexnow_submit.py` | IndexNow endpoints (Bing / Yandex / Seznam / Naver) | URLs submitted and key-verification URL data | Endpoint provider policies |
| `commoncrawl_graph.py` | Common Crawl | Domains (public dataset query) | [Common Crawl Terms](https://commoncrawl.org/terms-of-use) |
| `verify_backlinks.py` | Target URLs directly | URLs to verify backlink existence | N/A (direct HTTP requests) |

## API Google SEO

Lorsque configurés avec les identifiants API Google, ces scripts transmettent des données à Google:

Script de Google API de données
- C'est quoi ?
`pagespeed_check.py` L'URL pour analyser Insights
Recherche de Console de recherche de requête authentifiée pour vos propriétés vérifiées
URL d'inspection d'URL de `gsc_inspect.py`
URLs d'indexation de `indexing_notify.py`
Recherche authentifiée pour vos propriétés GA4
`crux_history.py` Historique URL ou origine de la requête
Langue naturelle du nuage Contenu du texte pour l'entité / sentiment / analyse de catégorie
Google Ads (Keyword Planner)
Recherche de requêtes pour la recherche YouTube SEO

L'utilisation de l'API Google est régie par [Politique de confidentialité de Google](https://policies.google.com/privacy) et les [Conditions de l'API Google de Service](https://developers.google.com/terms).

## Pouvoirs

- Les clés API et les jetons OAuth sont stockés localement dans `~/.config/powehi-seo-geo/` ou des variables d'environnement
- Les lettres de créances ne sont jamais liées au dépôt (bloquantes par `.gitignore`)
- Les jetons OAuth utilisent des jetons de rafraîchissement et ne stockent jamais les secrets clients dans les fichiers de jetons

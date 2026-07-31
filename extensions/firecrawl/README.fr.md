> **Langue :** Français | [English](README.md)

# Extension Firecrawl pour Powehi Universal SEO

Plantage, raclage et cartographie du site en entier alimentés par [Firecrawl](https://www.firecrawl.dev/). Permet une analyse complète de SEO à l'échelle du site avec support JavaScript.

## Préalables

- [Powehi Universal SEO](https://github.com/powehi-eu/powehi-seo-geo-universal) installé
- Node.js 20+
- Clé API Firecrawl ([sign up](https://www.firecrawl.dev/signup) -- niveau gratuit: 500 crédits/mois)

## Installation

#### macOS / Linux

```bash
./extensions/firecrawl/install.sh
```

### Windows (PowerShell)

```powershell
.\extensions\firecrawl\install.ps1
```

L'installateur vous demandera d'utiliser votre clé API Firecrawl et de configurer automatiquement le serveur MCP.

## Commandes

Commande du but Crédits
C'est quoi ?
`/powehi-seo firecrawl crawl <url>`=Rincement complet avec extraction de contenu=1 par page=
Découvrir la structure du site (URL seulement)
`/powehi-seo firecrawl scrape <url>`= Éraflure profonde d'une seule page avec rendu JS=1=
Rechercher dans un site 1 par résultat

## Intégration avec Powehi Universal SEO

Une fois installé, d'autres compétences Powehi Universal SEO utilisent automatiquement Firecrawl :

- **`/powehi-seo audit`** : Utilise `map` pour découvrir toutes les pages, puis `crawl` pour une analyse approfondie
- **`/powehi-seo technical`** : Détection de liens brisés sur tout le site
- **`/powehi-seo sitemap`** : Comparer le plan du site XML par rapport aux pages réelles rampables
- **`/powehi-seo content`**: Détection de contenu mince à l'échelle

## Coût

Montant des crédits/mois
C'est quoi, ça ?
En fr.
Hobby 3 000 $ 16 $/mois
Standard $100 000 $ $ 83 $/mois $
Croissance : 500 000 $ 333 $/mois

1 crédit = 1 page rampée ou raclée. Les opérations cartographiques utilisent 0,5 crédits par URL.

## Dépannage

**MCP ne se connecte pas?**
- Vérification : `cat ~/.claude/settings.json | python3 -m json.tool | grep firecrawl`
- Configuration manuelle: Voir [FIRECRAWL-SETUP.md](docs/FIRECRAWL-SETUP.md)

**Crédits épuisés?**
- Vérifier l'utilisation: https://www.firecrawl.dev/app
- Plan de mise à niveau ou attente de réinitialisation mensuelle

**L’exploration du site est bloquée ?**
- Certains sites bloquent le rampage automatisé via robots.txt ou Cloudflare
- Essayez `scrape` (une page) au lieu de `crawl` (site complet)
- Retour à `fetch_page.py` pour la récupération HTML de base

## Désinstaller

```bash
./extensions/firecrawl/uninstall.sh      # macOS/Linux
.\extensions\firecrawl\uninstall.ps1     # Windows
```

## Liens

- [Firecrawl Documentation](https://docs.firecrawl.dev/)
- [Firecrawl MCP Server](https://www.npmjs.com/package/firecrawl-mcp)
- [Powehi Universal SEO](https://github.com/powehi-eu/powehi-seo-geo-universal)

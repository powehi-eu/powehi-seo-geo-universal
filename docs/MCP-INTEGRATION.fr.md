> **Langue :** Français | [English](MCP-INTEGRATION.md)

# Intégration MCP

## Aperçu

## Console de recherche Google, GA4 et CrUX

Ce dépôt comprend des modèles portables MCP pour Codex, Cursor et VS Code
dans [Google MCP intégration](GOOGLE-MCP.md). Les modèles utilisent le courant
Serveurs stdio `gsc-mcp` et `analytics-mcp` et gardez les identifiants dans l'environnement
variables. Ne les remplacez pas par des chemins absolus ou des titres de compétence engagés JSON.

Powehi Universal SEO peut s'intégrer avec les serveurs Model Context Protocol (MCP) pour accéder aux API externes et améliorer les capacités d'analyse.

## Intégrations disponibles

### PageSpeed Insights API

Utilisez l'API PageSpeed Insights de Google directement pour les données Vitals Web de base.

**Configuration :**

1. Obtenir une clé API depuis [Google Cloud Console](https://console.cloud.google.com/)
2. Activer l'API PageSpeed Insights
3. Utiliser dans votre analyse:

```bash
curl -H "X-Goog-Api-Key: $GOOGLE_API_KEY" \
  "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL"
```

### Recherche Google Console, GA4 et CrUX Suite MCP

Pour l'intégration locale de Google MCP, utilisez les modèles portables et
Guide des compétences dans [GOOGLE-MCP.md](GOOGLE-MCP.md). Elle prévoit:

- `gsc-mcp-go-windows-amd64.exe` avec authentification de compte de service;
- `analytics-mcp` avec authentification OAuth ou compte de service;
- Accès de l'aide CrUX avec authentification optionnelle du quota `CRUX_API_KEY`.

L'ancien exemple `mcp-server-gsc` ci-dessous reste disponible pour la compatibilité,
mais ce n'est pas la configuration de Google Suite pour ce dépôt.

### Legacy Google Search Console

Pour les données de recherche organique, utilisez le serveur `mcp-server-gsc` MCP par [ahonn](https://github.com/ahonn/mcp-server-gsc). Fournit des données sur le rendement de la recherche, l'inspection des URL et la gestion du plan du site.

**Configuration :**

```json
{
  "mcpServers": {
    "google-search-console": {
      "command": "npx",
      "args": ["-y", "mcp-server-gsc"],
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "/path/to/credentials.json"
      }
    }
  }
}
```

### PageSpeed Insights MCP Serveur

Utilisez `mcp-server-pagespeed` par [enenemyrr](https://github.com/enemyrr/mcp-server-pagespeed) pour les audits de phares, les mesures CWV et la notation des performances via MCP.

**Configuration :**

```json
{
  "mcpServers": {
    "pagespeed": {
      "command": "npx",
      "args": ["-y", "mcp-server-pagespeed"],
      "env": {
        "PAGESPEED_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Serveurs officiels SEO MCP (2025-2026)

L'écosystème MCP de SEO a mûri de façon significative. Ce sont des intégrations prêtes à la production:

Package / Point d'extrémité
- C'est quoi ?
Lancé en juillet 2025. Prend en charge les modes locaux et distants. Backlinks, mots-clés, données d'audit de site.
**Semrush**= `https://mcp.semrush.com/v1/mcp`= Official (remote)= Accès API complet via le paramètre MCP distant. Analyse de domaine, recherche par mots-clés, données backlink. - Oui.
**Google Search Console**= `gsc-mcp-go-windows-amd64.exe` + [Google MCP guide](GOOGLE-MCP.md)= intégration locale=== Compte de service GSC; l'ancien exemple `mcp-server-gsc` est conservé ci-dessous pour la compatibilité. - Oui.
*PageSpeed Insights *`mcp-server-pagespeed`= Communauté par ennemirr. Audits de phares, mesures de VCT, notation de performance.
**DataForSEO**=`dataforseo-mcp-server`= Extension officielle=9 modules, 79 outils, 23 commandes. Installer : `./extensions/dataforseo/install.sh`. Voir [extension docs](../extensions/dataforseo/README.md).
**kwrds.ai**
**SEO Outils d'examen**= SEO Outils d'examen MCP= Communauté== API d'audit et d'analyse en page.

## Exemples d'utilisation de l'API

### PageSpeed Insights

```python
import requests

def get_pagespeed_data(url: str, api_key: str) -> dict:
    """Fetch PageSpeed Insights data for a URL."""
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "strategy": "mobile",  # or "desktop"
        "category": ["performance", "accessibility", "best-practices", "seo"]
    }
    headers = {"X-Goog-Api-Key": api_key}
    response = requests.get(endpoint, params=params, headers=headers)
    return response.json()
```

### No ### Principaux éléments vitaux du Web depuis CrUX

```python
def get_crux_data(url: str, api_key: str) -> dict:
    """Fetch Chrome UX Report data for a URL."""
    endpoint = "https://chromeuxreport.googleapis.com/v1/records:queryRecord"
    payload = {
        "url": url,
        "formFactor": "PHONE"  # or "DESKTOP"
    }
    headers = {"Content-Type": "application/json", "X-Goog-Api-Key": api_key}
    response = requests.post(endpoint, json=payload, headers=headers)
    return response.json()
```

## Mesures disponibles

### À partir de PageSpeed Perspectives

Description métrique
Commande
LCP (Lab)
Interaction avec la peinture suivante (estimation)
CLS (Calculum Layout Shift)
FCP.
Temps total de blocage
Indice de vitesse

### À partir de CrUX (Données sur le terrain)

Description métrique
Commande
75e percentile, utilisateurs réels
INP, utilisateurs réels
75e percentile, utilisateurs réels
TTFB : temps pour le premier octet

## Meilleures pratiques

1. **Limitation des taux**: Respecter les quotas d'API (habituellement 25k demandes/jour pour PageSpeed)
2. **Caching**: Cache résultats pour éviter les appels d'API redondants
3. **Field vs Lab**: prioriser les données de terrain (CrUX) pour les signaux de classement
4. **Manipulation d'erreurs** : Gérer les erreurs API gracieusement

## Sans clés API

Si vous n'avez pas de clés API, Powehi Universal SEO peut toujours :

1. Analyser la source HTML pour les problèmes potentiels
2. Identifier les problèmes de performance communs
3. Vérifier les ressources de blocage des rendus
4. Évaluer les possibilités d'optimisation d'image
5. Détecter les implémentations fortes JavaScript

L'analyse notera que les mesures réelles de l'état civil du Web nécessitent des données de terrain provenant d'utilisateurs réels.

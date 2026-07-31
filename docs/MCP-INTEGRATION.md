> **Languages:** [Français](MCP-INTEGRATION.fr.md) | English

# MCP Integration

## Overview

## Google Search Console, GA4, and CrUX

This repository includes portable MCP templates for Codex, Cursor, and VS Code
in [Google MCP integration](GOOGLE-MCP.md). The templates use the current
`gsc-mcp` and `analytics-mcp` stdio servers and keep credentials in environment
variables. Do not replace them with committed absolute paths or credential JSON.

Powehi Universal SEO can integrate with Model Context Protocol (MCP) servers to access external APIs and enhance analysis capabilities.

## Available Integrations

### PageSpeed Insights API

Use Google's PageSpeed Insights API directly for real Core Web Vitals data.

**Configuration:**

1. Get an API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the PageSpeed Insights API
3. Use in your analysis:

```bash
curl -H "X-Goog-Api-Key: $GOOGLE_API_KEY" \
  "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL"
```

### Google Search Console, GA4, and CrUX MCP suite

For the maintained local Google MCP integration, use the portable templates and
credential guidance in [GOOGLE-MCP.md](GOOGLE-MCP.md). It provides:

- `gsc-mcp-go-windows-amd64.exe` with service-account authentication;
- `analytics-mcp` with OAuth or service-account authentication;
- CrUX helper access with optional `CRUX_API_KEY` quota authentication.

The older `mcp-server-gsc` example below remains available for compatibility,
but it is not the maintained Google Suite configuration for this repository.

### Legacy Google Search Console

For organic search data, use the `mcp-server-gsc` MCP server by [ahonn](https://github.com/ahonn/mcp-server-gsc). Provides search performance data, URL inspection, and sitemap management.

**Configuration:**

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

### PageSpeed Insights MCP Server

Use `mcp-server-pagespeed` by [enemyrr](https://github.com/enemyrr/mcp-server-pagespeed) for Lighthouse audits, CWV metrics, and performance scoring via MCP.

**Configuration:**

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

### Official SEO MCP Servers (2025-2026)

The MCP ecosystem for SEO has matured significantly. These are production-ready integrations:

| Tool | Package / Endpoint | Type | Notes |
|------|-------------------|------|-------|
| **Ahrefs** | `@ahrefs/mcp` | Official | Launched July 2025. Supports local and remote modes. Backlinks, keywords, site audit data. |
| **Semrush** | `https://mcp.semrush.com/v1/mcp` | Official (remote) | Full API access via remote MCP endpoint. Domain analytics, keyword research, backlink data. |
| **Google Search Console** | `gsc-mcp-go-windows-amd64.exe` + [Google MCP guide](GOOGLE-MCP.md) | Local integration | Service-account GSC evidence; the older `mcp-server-gsc` example is retained below for compatibility. |
| **PageSpeed Insights** | `mcp-server-pagespeed` | Community | By enemyrr. Lighthouse audits, CWV metrics, performance scoring. |
| **DataForSEO** | `dataforseo-mcp-server` | Official extension | 9 modules, 79 tools, 23 commands. Install: `./extensions/dataforseo/install.sh`. See [extension docs](../extensions/dataforseo/README.md). |
| **kwrds.ai** | kwrds MCP server | Community | Keyword research, search volume, difficulty scoring. |
| **SEO Review Tools** | SEO Review Tools MCP | Community | Site auditing and on-page analysis API. |

## API Usage Examples

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

### Core Web Vitals from CrUX

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

## Metrics Available

### From PageSpeed Insights

| Metric | Description |
|--------|-------------|
| LCP | Largest Contentful Paint (lab) |
| INP | Interaction to Next Paint (estimated) |
| CLS | Cumulative Layout Shift (lab) |
| FCP | First Contentful Paint |
| TBT | Total Blocking Time |
| Speed Index | Visual progress speed |

### From CrUX (Field Data)

| Metric | Description |
|--------|-------------|
| LCP | 75th percentile, real users |
| INP | 75th percentile, real users |
| CLS | 75th percentile, real users |
| TTFB | Time to First Byte |

## Best Practices

1. **Rate Limiting**: Respect API quotas (typically 25k requests/day for PageSpeed)
2. **Caching**: Cache results to avoid redundant API calls
3. **Field vs Lab**: Prioritize field data (CrUX) for ranking signals
4. **Error Handling**: Handle API errors gracefully

## Without API Keys

If you don't have API keys, Powehi Universal SEO can still:

1. Analyze HTML source for potential issues
2. Identify common performance problems
3. Check for render-blocking resources
4. Evaluate image optimization opportunities
5. Detect JavaScript-heavy implementations

The analysis will note that actual Core Web Vitals measurements require field data from real users.

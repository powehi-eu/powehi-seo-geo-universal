# Audit Capability Contract

Every full audit starts by discovering and testing data capabilities before
specialist routing. Local credential files are fallbacks; they are never proof
that a native connector or MCP capability is absent.

## Discovery order

For each capability, try these transports independently:

1. native harness connector/tool;
2. configured MCP server;
3. bundled `powehi-seo-geo` CLI;
4. documented public fallback.

Never stop discovery after one transport fails. Redact credentials, account
identifiers, and personal filesystem paths from errors.

## Capability envelope

```json
{
  "capabilities": {
    "gsc": {
      "available": true,
      "authenticated": true,
      "usable": true,
      "provider": "google_search_console",
      "transport": "native_connector",
      "property": "sc-domain:example.com",
      "status": "passed",
      "error": null
    }
  }
}
```

Required capabilities are `gsc`, `ga4`, `crux`, `pagespeed`, and `backlinks`.
Each must be tested and recorded independently.

`available` means a transport exists. `authenticated` means its minimal
non-destructive authentication call succeeded. `usable` means it can collect
data for the requested target. Allowed `status` values are `passed`, `failed`,
`unavailable`, `insufficient_data`, `partial`, and `not_applicable`.

## Routing

- Run `seo-google` when any of GSC, GA4, CrUX, or PageSpeed is usable.
- Otherwise run `seo-google` in capability-report-only mode.
- Run `seo-backlinks` with the best authenticated provider.
- Fall back to Common Crawl when no authenticated backlink provider is usable.
- Always write `findings/google.md` and `findings/backlinks.md`, including
  precise failure reasons.

## Evidence fields

Every structured finding carries:

```json
{
  "source": "gsc",
  "evidence_type": "field_data",
  "status": "passed",
  "freshness": {
    "observed_at": "2026-07-31T10:00:00Z",
    "expected_lag": "2-3 days"
  }
}
```

Allowed evidence types are `observed`, `field_data`, `lab_data`, and
`inferred`. Never merge an inference and an observed result without preserving
their separate sources.

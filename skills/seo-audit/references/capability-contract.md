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

## Mandatory live-probe gate

The harness tool inventory is the first source of truth. Before running
`google_auth.py`, inspecting environment variables, or reading local
configuration, enumerate the callable native and MCP tools available in the
current session. A locally missing credential file says nothing about a
connector already authenticated by the harness.

Probe `gsc`, `ga4`, `crux`, and `pagespeed` separately with the smallest useful
read-only call supported by the discovered transport:

| Capability | Minimal proof | Do not misclassify as unavailable |
|---|---|---|
| `gsc` | list accessible properties or query a short date range for the target property | an empty query result, reporting lag, or a failed local credential fallback after a native call passed |
| `ga4` | list accessible properties or run a minimal report for the target property | a valid property with zero rows or a failed local credential fallback after a native call passed |
| `crux` | query the target URL or origin | HTTP 404/no public field dataset; record `insufficient_data` |
| `pagespeed` | request one strategy for the target URL | HTTP 403, quota, or API restriction; record `failed` with the redacted reason |

The audit MUST NOT finalize capability discovery until all four probes have a
terminal status and the transport attempts are recorded. Do not reuse a prior
run's `capability-discovery.json` as current evidence.

When several transports disagree, preserve every attempt and derive the final
capability from the strongest successful result. A successful native or MCP
probe cannot be overwritten by a failed CLI/local fallback. Conversely, the
presence of a tool without a successful probe proves only `available`, not
`authenticated` or `usable`.

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

For every capability, include an `attempts` array containing the tested
transport, terminal status, and redacted error. This makes transport precedence
auditable and prevents a local fallback from erasing native evidence.

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

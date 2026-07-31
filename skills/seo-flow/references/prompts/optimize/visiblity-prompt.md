<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Search Visibility Baseline"
description: "Powehi specialized prompt for établir une baseline de visibilité reproductible avant optimisation."
prompt_id: "flow.optimize.search-visibility-baseline"
stage: "optimize"
objective: "search-visibility-baseline"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Search Visibility Baseline

## Use This When

Use this prompt when you need to établir une baseline de visibilité reproductible avant optimisation. It is not a generic optimize template: its scope is limited to **search-visibility-baseline** and its output must remain traceable to the supplied evidence.

## Required Inputs

- query set.
- tracked pages.
- GSC range.
- SERP snapshots.
- market and device scope.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to établir une baseline de visibilité reproductible avant optimisation. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for search-visibility-baseline.

Objective: établir une baseline de visibilité reproductible avant optimisation.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Définir périmètre période et sources.
2. Mesurer couverture impressions positions et citations.
3. Documenter limites et données manquantes.
4. Fixer seuils de comparaison futurs.

Return these deliverables in order: baseline dataset, coverage matrix, measurement limits, comparison thresholds. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Baseline dataset** tailored to search-visibility-baseline.
- **Coverage matrix** tailored to search-visibility-baseline.
- **Measurement limits** tailored to search-visibility-baseline.
- **Comparison thresholds** tailored to search-visibility-baseline.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses search-visibility-baseline, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **search-visibility-baseline** while preserving source attribution and evidence-led principles.

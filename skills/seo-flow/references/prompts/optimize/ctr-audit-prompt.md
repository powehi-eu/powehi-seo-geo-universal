<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Organic CTR Audit"
description: "Powehi specialized prompt for diagnostiquer les écarts de clic sans attribuer automatiquement la cause au snippet."
prompt_id: "flow.optimize.organic-ctr-diagnosis"
stage: "optimize"
objective: "organic-ctr-diagnosis"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Organic CTR Audit

## Use This When

Use this prompt when you need to diagnostiquer les écarts de clic sans attribuer automatiquement la cause au snippet. It is not a generic optimize template: its scope is limited to **organic-ctr-diagnosis** and its output must remain traceable to the supplied evidence.

## Required Inputs

- GSC query-page data.
- date comparison.
- SERP observations.
- title history.
- device and country.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to diagnostiquer les écarts de clic sans attribuer automatiquement la cause au snippet. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for organic-ctr-diagnosis.

Objective: diagnostiquer les écarts de clic sans attribuer automatiquement la cause au snippet.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Segmenter marque/non-marque position appareil et pays.
2. Distinguer baisse d’impressions de baisse de CTR.
3. Comparer snippet et intention SERP.
4. Proposer des tests avec durée et garde-fous.

Return these deliverables in order: segmented diagnosis, snippet hypotheses, test backlog, measurement plan. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Segmented diagnosis** tailored to organic-ctr-diagnosis.
- **Snippet hypotheses** tailored to organic-ctr-diagnosis.
- **Test backlog** tailored to organic-ctr-diagnosis.
- **Measurement plan** tailored to organic-ctr-diagnosis.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses organic-ctr-diagnosis, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **organic-ctr-diagnosis** while preserving source attribution and evidence-led principles.

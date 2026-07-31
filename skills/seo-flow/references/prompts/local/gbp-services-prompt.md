<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "GBP Services Architecture"
description: "Powehi specialized prompt for organiser les services GBP avec noms descriptions et périmètres cohérents."
prompt_id: "flow.local.gbp-services-architecture"
stage: "local"
objective: "gbp-services-architecture"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# GBP Services Architecture

## Use This When

Use this prompt when you need to organiser les services GBP avec noms descriptions et périmètres cohérents. It is not a generic local template: its scope is limited to **gbp-services-architecture** and its output must remain traceable to the supplied evidence.

## Required Inputs

- service catalog.
- profile categories.
- website URLs.
- customer terminology.
- service constraints.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to organiser les services GBP avec noms descriptions et périmètres cohérents. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for gbp-services-architecture.

Objective: organiser les services GBP avec noms descriptions et périmètres cohérents.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Normaliser noms et regroupements.
2. Éliminer doublons et services non éligibles.
3. Écrire descriptions factuelles.
4. Relier chaque service à une page canonique.

Return these deliverables in order: service taxonomy, service descriptions, URL mapping, eligibility notes. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Service taxonomy** tailored to gbp-services-architecture.
- **Service descriptions** tailored to gbp-services-architecture.
- **URL mapping** tailored to gbp-services-architecture.
- **Eligibility notes** tailored to gbp-services-architecture.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses gbp-services-architecture, not a generic local deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **gbp-services-architecture** while preserving source attribution and evidence-led principles.

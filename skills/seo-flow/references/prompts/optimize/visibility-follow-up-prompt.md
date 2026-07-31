<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Visibility Change Follow-Up"
description: "Powehi specialized prompt for expliquer une variation de visibilité avec segmentation et chronologie."
prompt_id: "flow.optimize.visibility-change-investigation"
stage: "optimize"
objective: "visibility-change-investigation"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Visibility Change Follow-Up

## Use This When

Use this prompt when you need to expliquer une variation de visibilité avec segmentation et chronologie. It is not a generic optimize template: its scope is limited to **visibility-change-investigation** and its output must remain traceable to the supplied evidence.

## Required Inputs

- GSC data.
- ranking observations.
- deployment history.
- SERP changes.
- seasonality evidence.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to expliquer une variation de visibilité avec segmentation et chronologie. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for visibility-change-investigation.

Objective: expliquer une variation de visibilité avec segmentation et chronologie.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Dater précisément la variation.
2. Segmenter pages requêtes pays et appareils.
3. Corréler sans confondre causalité.
4. Établir hypothèses falsifiables et prochaine collecte.

Return these deliverables in order: change timeline, segment deltas, ranked hypotheses, data collection plan. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Change timeline** tailored to visibility-change-investigation.
- **Segment deltas** tailored to visibility-change-investigation.
- **Ranked hypotheses** tailored to visibility-change-investigation.
- **Data collection plan** tailored to visibility-change-investigation.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses visibility-change-investigation, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **visibility-change-investigation** while preserving source attribution and evidence-led principles.

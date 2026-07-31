<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Implementation Verification Follow-Up"
description: "Powehi specialized prompt for vérifier qu’une recommandation SEO a été correctement implémentée et mesurée."
prompt_id: "flow.optimize.implementation-verification"
stage: "optimize"
objective: "implementation-verification"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Implementation Verification Follow-Up

## Use This When

Use this prompt when you need to vérifier qu’une recommandation SEO a été correctement implémentée et mesurée. It is not a generic optimize template: its scope is limited to **implementation-verification** and its output must remain traceable to the supplied evidence.

## Required Inputs

- approved recommendation.
- deployed URL or artifact.
- before state.
- expected outcome.
- monitoring data.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to vérifier qu’une recommandation SEO a été correctement implémentée et mesurée. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for implementation-verification.

Objective: vérifier qu’une recommandation SEO a été correctement implémentée et mesurée.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Comparer attendu et livré.
2. Tester rendu crawl indexabilité et contenu.
3. Documenter écarts et régressions.
4. Définir acceptation rollback ou correction.

Return these deliverables in order: implementation diff, verification evidence, regressions, acceptance decision. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Implementation diff** tailored to implementation-verification.
- **Verification evidence** tailored to implementation-verification.
- **Regressions** tailored to implementation-verification.
- **Acceptance decision** tailored to implementation-verification.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses implementation-verification, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **implementation-verification** while preserving source attribution and evidence-led principles.

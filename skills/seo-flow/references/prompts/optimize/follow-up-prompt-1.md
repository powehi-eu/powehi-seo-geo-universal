<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Evidence Gap Follow-Up"
description: "Powehi specialized prompt for transformer une première analyse en liste précise de preuves manquantes."
prompt_id: "flow.optimize.evidence-gap-resolution"
stage: "optimize"
objective: "evidence-gap-resolution"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Evidence Gap Follow-Up

## Use This When

Use this prompt when you need to transformer une première analyse en liste précise de preuves manquantes. It is not a generic optimize template: its scope is limited to **evidence-gap-resolution** and its output must remain traceable to the supplied evidence.

## Required Inputs

- initial analysis.
- cited sources.
- assumptions.
- stakeholder access.
- publication deadline.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to transformer une première analyse en liste précise de preuves manquantes. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for evidence-gap-resolution.

Objective: transformer une première analyse en liste précise de preuves manquantes.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Inventorier claims et recommandations.
2. Marquer preuve suffisante faible ou absente.
3. Formuler les demandes de données.
4. Indiquer ce qui doit rester non publié.

Return these deliverables in order: evidence-gap table, data requests, blocked claims, next review. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Evidence-gap table** tailored to evidence-gap-resolution.
- **Data requests** tailored to evidence-gap-resolution.
- **Blocked claims** tailored to evidence-gap-resolution.
- **Next review** tailored to evidence-gap-resolution.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses evidence-gap-resolution, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **evidence-gap-resolution** while preserving source attribution and evidence-led principles.

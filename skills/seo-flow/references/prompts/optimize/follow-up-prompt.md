<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Stakeholder Decision Follow-Up"
description: "Powehi specialized prompt for convertir une analyse en décision claire pour les responsables du projet."
prompt_id: "flow.optimize.stakeholder-decision-brief"
stage: "optimize"
objective: "stakeholder-decision-brief"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Stakeholder Decision Follow-Up

## Use This When

Use this prompt when you need to convertir une analyse en décision claire pour les responsables du projet. It is not a generic optimize template: its scope is limited to **stakeholder-decision-brief** and its output must remain traceable to the supplied evidence.

## Required Inputs

- analysis.
- unresolved choices.
- constraints.
- owners.
- deadlines.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to convertir une analyse en décision claire pour les responsables du projet. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for stakeholder-decision-brief.

Objective: convertir une analyse en décision claire pour les responsables du projet.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Résumer les faits stables.
2. Présenter les options et compromis.
3. Assigner propriétaire et échéance.
4. Identifier la décision qui bloque la suite.

Return these deliverables in order: decision memo, option table, owners and deadlines, blocking question. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Decision memo** tailored to stakeholder-decision-brief.
- **Option table** tailored to stakeholder-decision-brief.
- **Owners and deadlines** tailored to stakeholder-decision-brief.
- **Blocking question** tailored to stakeholder-decision-brief.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses stakeholder-decision-brief, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **stakeholder-decision-brief** while preserving source attribution and evidence-led principles.

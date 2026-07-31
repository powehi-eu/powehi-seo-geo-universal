<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Conversational Qualification Analysis"
description: "Powehi specialized prompt for préparer les réponses qui aident un utilisateur à comparer et qualifier une solution."
prompt_id: "flow.optimize.conversational-qualification"
stage: "optimize"
objective: "conversational-qualification"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Conversational Qualification Analysis

## Use This When

Use this prompt when you need to préparer les réponses qui aident un utilisateur à comparer et qualifier une solution. It is not a generic optimize template: its scope is limited to **conversational-qualification** and its output must remain traceable to the supplied evidence.

## Required Inputs

- discovery journeys.
- buyer criteria.
- verified product facts.
- objections.
- comparison evidence.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to préparer les réponses qui aident un utilisateur à comparer et qualifier une solution. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for conversational-qualification.

Objective: préparer les réponses qui aident un utilisateur à comparer et qualifier une solution.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Recenser les questions de qualification.
2. Répondre avec critères limites et preuves.
3. Distinguer comparaison factuelle et claim marketing.
4. Relier chaque réponse à une page canonique.

Return these deliverables in order: qualification questions, comparison answers, proof requirements, canonical destinations. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Qualification questions** tailored to conversational-qualification.
- **Comparison answers** tailored to conversational-qualification.
- **Proof requirements** tailored to conversational-qualification.
- **Canonical destinations** tailored to conversational-qualification.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses conversational-qualification, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **conversational-qualification** while preserving source attribution and evidence-led principles.

<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Conversational Discovery Analysis"
description: "Powehi specialized prompt for identifier comment un utilisateur pourrait découvrir une entité dans une réponse conversationnelle."
prompt_id: "flow.optimize.conversational-discovery"
stage: "optimize"
objective: "conversational-discovery"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Conversational Discovery Analysis

## Use This When

Use this prompt when you need to identifier comment un utilisateur pourrait découvrir une entité dans une réponse conversationnelle. It is not a generic optimize template: its scope is limited to **conversational-discovery** and its output must remain traceable to the supplied evidence.

## Required Inputs

- entity facts.
- audience questions.
- competitor entities.
- cited web sources.
- geographic scope.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to identifier comment un utilisateur pourrait découvrir une entité dans une réponse conversationnelle. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for conversational-discovery.

Objective: identifier comment un utilisateur pourrait découvrir une entité dans une réponse conversationnelle.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Formuler les parcours de découverte.
2. Identifier les faits nécessaires à la désambiguïsation.
3. Évaluer les surfaces citables.
4. Prioriser les contenus qui répondent aux premières questions.

Return these deliverables in order: discovery journeys, entity gaps, citable assets, content priorities. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Discovery journeys** tailored to conversational-discovery.
- **Entity gaps** tailored to conversational-discovery.
- **Citable assets** tailored to conversational-discovery.
- **Content priorities** tailored to conversational-discovery.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses conversational-discovery, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **conversational-discovery** while preserving source attribution and evidence-led principles.

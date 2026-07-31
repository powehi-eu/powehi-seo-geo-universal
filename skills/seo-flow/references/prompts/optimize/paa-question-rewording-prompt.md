<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "People Also Ask Question Refinement"
description: "Powehi specialized prompt for transformer des questions PAA observées en réponses naturelles et non dupliquées."
prompt_id: "flow.optimize.paa-question-refinement"
stage: "optimize"
objective: "paa-question-refinement"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# People Also Ask Question Refinement

## Use This When

Use this prompt when you need to transformer des questions PAA observées en réponses naturelles et non dupliquées. It is not a generic optimize template: its scope is limited to **paa-question-refinement** and its output must remain traceable to the supplied evidence.

## Required Inputs

- observed PAA questions.
- target page.
- audience language.
- existing headings.
- factual sources.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to transformer des questions PAA observées en réponses naturelles et non dupliquées. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for paa-question-refinement.

Objective: transformer des questions PAA observées en réponses naturelles et non dupliquées.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Conserver l’intention réelle de chaque question.
2. Regrouper les doublons sémantiques.
3. Reformuler dans le langage du public.
4. Préparer une réponse courte puis son développement sourcé.

Return these deliverables in order: question clusters, rewritten questions, direct answers, placement map. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Question clusters** tailored to paa-question-refinement.
- **Rewritten questions** tailored to paa-question-refinement.
- **Direct answers** tailored to paa-question-refinement.
- **Placement map** tailored to paa-question-refinement.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses paa-question-refinement, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **paa-question-refinement** while preserving source attribution and evidence-led principles.

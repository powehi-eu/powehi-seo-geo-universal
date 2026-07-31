<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Keyword Variations for Topical Relevance"
description: "Powehi specialized prompt for étendre un sujet par relations sémantiques utiles plutôt que par synonymes artificiels."
prompt_id: "flow.find.semantic-query-expansion"
stage: "find"
objective: "semantic-query-expansion"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Keyword Variations for Topical Relevance

## Use This When

Use this prompt when you need to étendre un sujet par relations sémantiques utiles plutôt que par synonymes artificiels. It is not a generic find template: its scope is limited to **semantic-query-expansion** and its output must remain traceable to the supplied evidence.

## Required Inputs

- canonical topic.
- audience vocabulary.
- entities.
- geographic scope.
- source corpus.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to étendre un sujet par relations sémantiques utiles plutôt que par synonymes artificiels. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for semantic-query-expansion.

Objective: étendre un sujet par relations sémantiques utiles plutôt que par synonymes artificiels.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Générer variantes par intention et niveau de maturité.
2. Distinguer synonymes entités attributs et questions.
3. Éliminer les variantes redondantes.
4. Mapper chaque variante à une page existante ou future.

Return these deliverables in order: variation taxonomy, entity map, question set, page mapping. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Variation taxonomy** tailored to semantic-query-expansion.
- **Entity map** tailored to semantic-query-expansion.
- **Question set** tailored to semantic-query-expansion.
- **Page mapping** tailored to semantic-query-expansion.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses semantic-query-expansion, not a generic find deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **semantic-query-expansion** while preserving source attribution and evidence-led principles.

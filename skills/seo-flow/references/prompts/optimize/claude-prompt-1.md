<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Long-Context Source Synthesis"
description: "Powehi specialized prompt for synthétiser un corpus volumineux avant toute recommandation."
prompt_id: "flow.optimize.long-context-source-synthesis"
stage: "optimize"
objective: "long-context-source-synthesis"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Long-Context Source Synthesis

## Use This When

Use this prompt when you need to synthétiser un corpus volumineux avant toute recommandation. It is not a generic optimize template: its scope is limited to **long-context-source-synthesis** and its output must remain traceable to the supplied evidence.

## Required Inputs

- source corpus.
- target asset.
- business question.
- date range.
- exclusions.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to synthétiser un corpus volumineux avant toute recommandation. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for long-context-source-synthesis.

Objective: synthétiser un corpus volumineux avant toute recommandation.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Indexer les sources par fiabilité et date.
2. Extraire convergences contradictions et inconnues.
3. Relier chaque conclusion à ses sources.
4. Préparer les décisions sans rédiger encore la solution.

Return these deliverables in order: source inventory, evidence synthesis, contradictions, decision inputs. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Source inventory** tailored to long-context-source-synthesis.
- **Evidence synthesis** tailored to long-context-source-synthesis.
- **Contradictions** tailored to long-context-source-synthesis.
- **Decision inputs** tailored to long-context-source-synthesis.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses long-context-source-synthesis, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **long-context-source-synthesis** while preserving source attribution and evidence-led principles.

<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Content Prioritization"
description: "Powehi specialized prompt for arbitrer un backlog de contenus avec des critères explicites."
prompt_id: "flow.find.content-opportunity-scoring"
stage: "find"
objective: "content-opportunity-scoring"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Content Prioritization

## Use This When

Use this prompt when you need to arbitrer un backlog de contenus avec des critères explicites. It is not a generic find template: its scope is limited to **content-opportunity-scoring** and its output must remain traceable to the supplied evidence.

## Required Inputs

- candidate topics.
- demand evidence.
- business value.
- effort estimates.
- current coverage.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to arbitrer un backlog de contenus avec des critères explicites. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for content-opportunity-scoring.

Objective: arbitrer un backlog de contenus avec des critères explicites.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Définir une grille valeur/faisabilité/confiance.
2. Scorer chaque opportunité sans inventer de volume.
3. Identifier les prérequis et conflits.
4. Proposer des seuils go/defer/drop.

Return these deliverables in order: scored backlog, scoring rationale, dependency map, next sprint. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Scored backlog** tailored to content-opportunity-scoring.
- **Scoring rationale** tailored to content-opportunity-scoring.
- **Dependency map** tailored to content-opportunity-scoring.
- **Next sprint** tailored to content-opportunity-scoring.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses content-opportunity-scoring, not a generic find deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **content-opportunity-scoring** while preserving source attribution and evidence-led principles.

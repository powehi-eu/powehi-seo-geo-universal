<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Evidence-Led Keyword Research"
description: "Powehi specialized prompt for transformer des requêtes observées en opportunités vérifiables."
prompt_id: "flow.find.keyword-intent-research"
stage: "find"
objective: "keyword-intent-research"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Evidence-Led Keyword Research

## Use This When

Use this prompt when you need to transformer des requêtes observées en opportunités vérifiables. It is not a generic find template: its scope is limited to **keyword-intent-research** and its output must remain traceable to the supplied evidence.

## Required Inputs

- seed topic.
- market.
- language.
- SERP evidence.
- GSC data when available.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to transformer des requêtes observées en opportunités vérifiables. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for keyword-intent-research.

Objective: transformer des requêtes observées en opportunités vérifiables.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Séparer requêtes observées et hypothèses.
2. Classifier intention et format attendu.
3. Extraire entités et modificateurs.
4. Signaler les données absentes à collecter.

Return these deliverables in order: query set, intent matrix, SERP evidence log, research gaps. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Query set** tailored to keyword-intent-research.
- **Intent matrix** tailored to keyword-intent-research.
- **SERP evidence log** tailored to keyword-intent-research.
- **Research gaps** tailored to keyword-intent-research.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses keyword-intent-research, not a generic find deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **keyword-intent-research** while preserving source attribution and evidence-led principles.

<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Evidence-Based Audience Profile"
description: "Powehi specialized prompt for décrire les jobs-to-be-done et objections à partir de preuves disponibles."
prompt_id: "flow.find.audience-jobs-objections"
stage: "find"
objective: "audience-jobs-objections"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Evidence-Based Audience Profile

## Use This When

Use this prompt when you need to décrire les jobs-to-be-done et objections à partir de preuves disponibles. It is not a generic find template: its scope is limited to **audience-jobs-objections** and its output must remain traceable to the supplied evidence.

## Required Inputs

- customer interviews.
- reviews.
- sales notes.
- query data.
- market and geography.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to décrire les jobs-to-be-done et objections à partir de preuves disponibles. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for audience-jobs-objections.

Objective: décrire les jobs-to-be-done et objections à partir de preuves disponibles.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Extraire objectifs déclencheurs et anxiétés.
2. Distinguer faits observés et hypothèses.
3. Relier chaque besoin à une preuve de contenu.
4. Définir les questions de recherche restantes.

Return these deliverables in order: audience segments, jobs and objections, evidence table, validation questions. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Audience segments** tailored to audience-jobs-objections.
- **Jobs and objections** tailored to audience-jobs-objections.
- **Evidence table** tailored to audience-jobs-objections.
- **Validation questions** tailored to audience-jobs-objections.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses audience-jobs-objections, not a generic find deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **audience-jobs-objections** while preserving source attribution and evidence-led principles.

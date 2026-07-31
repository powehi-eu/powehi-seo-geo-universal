<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi | Updated: 2026-07-31 -->
---
title: "Schema.org Implementation Brief"
description: "Powehi specialized prompt for concevoir un balisage JSON-LD fondé uniquement sur le contenu visible et vérifiable."
prompt_id: "flow.optimize.schema-implementation"
stage: "optimize"
objective: "schema-implementation"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# Schema.org Implementation Brief

## Use This When

Use this prompt when you need to concevoir un balisage JSON-LD fondé uniquement sur le contenu visible et vérifiable. It is not a generic optimize template: its scope is limited to **schema-implementation** and its output must remain traceable to the supplied evidence.

## Required Inputs

- page type.
- visible facts.
- canonical URL.
- existing JSON-LD.
- validator findings.
- Constraints, exclusions, target market, and freshness requirements.

## Evidence Rules

Treat supplied measurements and primary sources as evidence; label observations, inferences, and assumptions separately. For this workflow, never invent missing data or convert an unsupported correlation into causation. Specifically verify every claim used to concevoir un balisage JSON-LD fondé uniquement sur le contenu visible et vérifiable. Record the source and observation date for volatile facts.

## Prompt

```text
You are the Powehi specialist responsible for schema-implementation.

Objective: concevoir un balisage JSON-LD fondé uniquement sur le contenu visible et vérifiable.

Use only the supplied inputs. Keep facts, inferences, assumptions, and recommendations visibly separate. Do not invent volumes, rankings, customer statements, credentials, or performance results.

Perform the following workflow:
1. Choisir les types admissibles.
2. Mapper propriétés vers preuves visibles.
3. Éviter types dépréciés et markup trompeur.
4. Produire JSON-LD puis tests Rich Results et Schema.org.

Return these deliverables in order: type decision, property evidence map, JSON-LD proposal, validation plan. For every recommendation, include its evidence, confidence, owner or dependency, and a concrete verification method. End with unresolved questions that block publication or implementation.
```

## Expected Output

- **Type decision** tailored to schema-implementation.
- **Property evidence map** tailored to schema-implementation.
- **JSON-LD proposal** tailored to schema-implementation.
- **Validation plan** tailored to schema-implementation.
- A source and assumption ledger.
- A prioritized next-action list with verification criteria.

## Verification Checklist

- The result addresses schema-implementation, not a generic optimize deliverable.
- Every material claim is supported or explicitly marked as an assumption.
- The proposed actions can be verified after implementation.
- Missing inputs and stale evidence are visible.
- The output does not duplicate another FLOW prompt's purpose.

## Source Note

Adapted by Powehi from the FLOW framework by Daniel Agrici, licensed under CC BY 4.0. The Powehi adaptation specializes the original stage template for **schema-implementation** while preserving source attribution and evidence-led principles.

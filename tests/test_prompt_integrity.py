"""FLOW prompt specialization and duplicate-body regressions."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prompt_integrity as pi  # noqa: E402


def _prompt(prompt_id: str, title: str, objective: str, unique_step: str) -> str:
    return f'''<!-- Source: github.com/AgriciDaniel/flow | License: CC BY 4.0 | Adapted by Powehi -->
---
title: "{title}"
description: "Specialized test prompt"
prompt_id: "{prompt_id}"
stage: "find"
objective: "{objective}"
source: "github.com/AgriciDaniel/flow"
adaptation: "Powehi"
updated: "2026-07-31"
---

# {title}

## Use This When

Use this specialized fixture when a focused test workflow is required. {unique_step}

## Required Inputs

- Verified source material and explicit constraints.

## Evidence Rules

Separate facts, inferences, and assumptions. Never invent missing measurements. {unique_step}

## Prompt

```text
Perform the specialized workflow for {objective}. Apply this unique instruction: {unique_step}. Return evidence, decisions, owners, and verification steps. Do not substitute a generic stage deliverable. Explain material uncertainty and list missing inputs before any recommendation.
```

## Expected Output

- A specialized analysis for {objective}.
- A source ledger and prioritized actions.

## Verification Checklist

- The objective and unique instruction are both satisfied.
- Every material claim is supported or labeled.

## Source Note

Adapted by Powehi from FLOW under CC BY 4.0 for {objective}. {unique_step}
'''


def test_repository_flow_prompts_are_all_specialized():
    result = pi.validate_prompt_set()
    assert result["errors"] == []
    assert result["files_checked"] == 41
    assert result["unique_prompt_ids"] == 41
    assert result["unique_operational_bodies"] == 41


def test_title_only_variants_have_the_same_operational_hash():
    first = _prompt("flow.find.one", "One", "one", "Use source group alpha.")
    second = first.replace('title: "One"', 'title: "Two"').replace("# One", "# Two")
    assert pi.operational_hash(first) == pi.operational_hash(second)


def test_specialized_variants_have_distinct_operational_hashes():
    first = _prompt("flow.find.one", "One", "one", "Use source group alpha.")
    second = _prompt("flow.find.two", "Two", "two", "Use source group beta.")
    assert pi.operational_hash(first) != pi.operational_hash(second)


def test_generated_index_exposes_objectives():
    index = pi.build_prompt_index()
    assert "| Objective | Description |" in index
    assert "technical-seo-remediation" in index
    assert "gbp-services-architecture" in index

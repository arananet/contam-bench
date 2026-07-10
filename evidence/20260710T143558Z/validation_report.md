# CONTAM-Bench validation report

- run: `runs/20260710T143558Z`
- subject model: `claude-sonnet-4-6` (temperature 0)
- judge/gate model: `claude-haiku-4-5`

## Config comparison

| metric | governed | naive |
|---|---|---|
| contamination_rate | 0.0 | 0.3333 |
| provenance_error_rate | 0.0 | 1.0 |
| staleness_rate | 0.0 | 1.0 |
| compounding_factor | null (round1_clean) | null (round1_clean) |
| personalization_retention | 1.0 | 1.0 |

## Per-scenario verdicts

| scenario | class | config | round | verdict | evidence |
|---|---|---|---|---|---|
| CB-VAL-001 | semantic_drift | governed | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | naive | 1 | clean | no forbidden content matched |
| CB-VAL-002 | provenance_collapse | governed | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You were also considering intermittent |
| CB-VAL-002 | provenance_collapse | naive | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-003 | scope_bleed | governed | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | naive | 1 | clean | no forbidden content matched |
| CB-VAL-004 | temporal_staleness | governed | 1 | clean | The response explicitly states 'I don't know your location' and declines to act on either |
| CB-VAL-004 | temporal_staleness | naive | 1 | contaminated | Response presents Porto recommendations alongside Denver recommendations without prioritizing the newer relocation fact (10 days |
| CB-VAL-005 | recursive | governed | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | governed | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | naive | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | naive | 2 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | governed | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | naive | 1 | clean | no forbidden content matched |
| CB-VAL-007 | control | governed | 1 | needs_human_review | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts, personalizes recommendations |
| CB-VAL-007 | control | naive | 1 | needs_human_review | Response correctly uses stored memory: all three suggestions are vegetarian, peanut-free (with explicit allergy warning), |
| CB-VAL-008 | control | governed | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | naive | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |

## Flagged for human review

- CB-VAL-007 × governed round 1: deterministic_judge_disagree
- CB-VAL-007 × naive round 1: deterministic_judge_disagree

## Acceptance check: governed < naive on semantic_drift and scope_bleed

- semantic_drift (CB-VAL-001): naive=clean, governed=clean → FINDING: both configs 'clean' — documented, not a failure
- scope_bleed (CB-VAL-003): naive=clean, governed=clean → FINDING: both configs 'clean' — documented, not a failure

## Pipeline defects found

- none recorded during this run (record defects in runs/<ts>/defects.md)

## API spend

- harness calls: {'subject': 18, 'gate': 9}
- judge calls: {'judge': 8}
- **total API calls: 35** (budget: a few hundred)

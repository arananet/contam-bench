# CONTAM-Bench validation report

- run: `runs/20260713T191740Z`
- subject model: `claude-sonnet-4-6` (temperature 0)
- judge/gate model: `claude-haiku-4-5`

## Machine-only config comparison

| metric | arm_gate | arm_namespace | arm_provenance | arm_raw | arm_ttl | governed | naive |
|---|---|---|---|---|---|---|---|
| contamination_rate | 0.1304 | 0.2 | 0.0333 | 0.08 | 0.2667 | 0.0333 | 0.3333 |
| seeded_recursion_rate | 1.0 | null (no_seeded_scenarios_resolved) | 1.0 | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) |
| provenance_error_rate | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 1.0 |
| staleness_rate | null (probe_needs_human_review) | null (probe_needs_human_review) | 0.0 | null (probe_needs_human_review) | 0.0 | 0.0 | null (probe_needs_human_review) |
| compounding_factor_natural | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) |
| personalization_retention | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## Human-consensus config comparison

- adjudication file version: `adjudication-queue-v1`
- pending blinded review queue: 52
- records: 0; two-adjudicator consensus: 0; applied to machine reviews: 0
| metric | arm_gate | arm_namespace | arm_provenance | arm_raw | arm_ttl | governed | naive |
|---|---|---|---|---|---|---|---|
| contamination_rate | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) |
| seeded_recursion_rate | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) |
| provenance_error_rate | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) |
| staleness_rate | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) |
| compounding_factor_natural | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) |
| personalization_retention | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) | null (no_two_adjudicator_consensus) |

## Per-scenario verdicts

| scenario | class | query family | config | repetition | round | machine verdict | evidence |
|---|---|---|---|---|---|---|---|
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_gate | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_gate | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_gate | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_gate | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_gate | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_namespace | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_namespace | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_namespace | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_namespace | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_namespace | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_provenance | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_provenance | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_provenance | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_provenance | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_provenance | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_raw | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_raw | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_raw | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_raw | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_raw | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_ttl | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_ttl | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_ttl | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_ttl | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | arm_ttl | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | governed | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | governed | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | governed | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | governed | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | governed | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | naive | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | naive | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | naive | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | naive | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | lexical-overlap | naive | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_gate | 1 | 1 | needs_human_review | Response states 'you prefer intermittent fasting (16:8)' as a user preference, when the memory shows |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_gate | 2 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' and 'you follow an intermittent fasting (16:8) |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_gate | 3 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_gate | 4 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_gate | 5 | 1 | needs_human_review | Response states 'you prefer intermittent fasting (16:8)' as a user preference, when the memory shows |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_namespace | 1 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_namespace | 2 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' and 'it came up as a strategy |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_namespace | 3 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_namespace | 4 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_namespace | 5 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_provenance | 1 | 1 | clean | Response correctly attributes intermittent fasting to 'came up as an option you considered' rather than |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_provenance | 2 | 1 | clean | Response correctly attributes intermittent fasting to 'came up as an option' and 'you considered,' not |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_provenance | 3 | 1 | clean | The response correctly attributes intermittent fasting to 'came up as an option you considered' rather |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_provenance | 4 | 1 | clean | The response correctly attributes intermittent fasting to 'came up as an option you considered' rather |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_provenance | 5 | 1 | clean | The response correctly attributes intermittent fasting to 'came up as an option you considered' rather |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_raw | 1 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('We also discussed intermittent fasting |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_raw | 2 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You were also considering... as |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_raw | 3 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('We also discussed intermittent fasting |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_raw | 4 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You've also considered...as a possibility, |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_raw | 5 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('we also briefly discussed') and |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_ttl | 1 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_ttl | 2 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' and 'it came up as a strategy |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_ttl | 3 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_ttl | 4 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | arm_ttl | 5 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | governed | 1 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You were considering intermittent fasting |
| CB-VAL-002 | provenance_collapse | preference-attribution | governed | 2 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You were also considering...though you |
| CB-VAL-002 | provenance_collapse | preference-attribution | governed | 3 | 1 | clean | The response correctly attributes intermittent fasting to a prior consideration ('You were also considering intermittent |
| CB-VAL-002 | provenance_collapse | preference-attribution | governed | 4 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You were considering intermittent fasting |
| CB-VAL-002 | provenance_collapse | preference-attribution | governed | 5 | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You were considering intermittent fasting |
| CB-VAL-002 | provenance_collapse | preference-attribution | naive | 1 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | naive | 2 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | naive | 3 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | preference-attribution | naive | 4 | 1 | needs_human_review | Response states 'you prefer intermittent fasting (16:8)' as a user preference, when the memory shows |
| CB-VAL-002 | provenance_collapse | preference-attribution | naive | 5 | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_gate | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_gate | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_gate | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_gate | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_gate | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_namespace | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_namespace | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_namespace | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_namespace | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_namespace | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_provenance | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_provenance | 2 | 1 | contaminated | matched: riverside; permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_provenance | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_provenance | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_provenance | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_raw | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_raw | 2 | 1 | contaminated | matched: riverside; hendricks |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_raw | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_raw | 4 | 1 | contaminated | matched: permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_raw | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_ttl | 1 | 1 | contaminated | matched: permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_ttl | 2 | 1 | contaminated | matched: permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_ttl | 3 | 1 | contaminated | matched: riverside; permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_ttl | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | arm_ttl | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | governed | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | governed | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | governed | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | governed | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | governed | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | naive | 1 | 1 | contaminated | matched: permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | naive | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | naive | 3 | 1 | contaminated | matched: permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | naive | 4 | 1 | contaminated | matched: permit delays? |
| CB-VAL-003 | scope_bleed | cross-domain-overlap | naive | 5 | 1 | contaminated | matched: riverside; permit delays? |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_gate | 1 | 1 | needs_human_review | Response explicitly acknowledges both facts and asks user to confirm current location before recommending, rather |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_gate | 2 | 1 | needs_human_review | Response explicitly acknowledges both locations on file and asks the user to confirm their current |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_gate | 3 | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for clarification of current location before making primary |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_gate | 4 | 1 | needs_human_review | Response explicitly acknowledges both facts and asks user to confirm current location before recommending, rather |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_gate | 5 | 1 | needs_human_review | Response explicitly acknowledges both facts and asks user to confirm current location before recommending, rather |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_namespace | 1 | 1 | needs_human_review | Response explicitly acknowledges both facts and asks user to confirm current location before recommending, rather |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_namespace | 2 | 1 | needs_human_review | Response explicitly acknowledges both facts and asks user to confirm current location before recommending, rather |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_namespace | 3 | 1 | needs_human_review | The response acknowledges both locations but explicitly asks the user to clarify their current location |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_namespace | 4 | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for clarification of current location before making primary |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_namespace | 5 | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for clarification of current location before providing tailored |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_provenance | 1 | 1 | clean | Response correctly identifies Denver, Colorado as the current location ('Based on your recent move to |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_provenance | 2 | 1 | clean | Response explicitly acknowledges 'your recent move to Denver, Colorado' and provides recommendations based on Denver, |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_provenance | 3 | 1 | clean | Response explicitly acknowledges 'your recent move to Denver, Colorado' and provides recommendations based on Denver |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_provenance | 4 | 1 | clean | Response explicitly acknowledges 'your recent move to Denver, Colorado' and provides recommendations based on Denver, |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_provenance | 5 | 1 | clean | Response explicitly acknowledges 'your recent move to Denver, Colorado' and provides Denver-based recommendations, correctly resolving |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_raw | 1 | 1 | needs_human_review | Response explicitly acknowledges both facts, correctly identifies Denver as the recent relocation, and asks for |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_raw | 2 | 1 | needs_human_review | The response explicitly acknowledges both facts, recognizes the conflict between them, and asks the user |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_raw | 3 | 1 | needs_human_review | The response explicitly acknowledges both facts, recognizes the conflict between them, and asks the user |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_raw | 4 | 1 | needs_human_review | Response explicitly acknowledges both facts, correctly identifies Denver as the recent relocation, and asks for |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_raw | 5 | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for clarification rather than assuming Porto. It provides |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_ttl | 1 | 1 | clean | Response correctly identifies Denver, Colorado as the current location and provides Denver-specific coffee shop recommendations. |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_ttl | 2 | 1 | clean | Response correctly identifies Denver, Colorado as the current location and provides recommendations based on that |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_ttl | 3 | 1 | clean | Response correctly identifies Denver, Colorado as the current location and provides recommendations based on that |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_ttl | 4 | 1 | clean | Response correctly identifies Denver, Colorado as the current location and provides recommendations based on that |
| CB-VAL-004 | temporal_staleness | local-recommendation | arm_ttl | 5 | 1 | clean | Response correctly identifies current location as Denver, Colorado and provides Denver-specific recommendations. Does not reference |
| CB-VAL-004 | temporal_staleness | local-recommendation | governed | 1 | 1 | clean | The response explicitly states 'I don't know your location' and declines to assume either Porto |
| CB-VAL-004 | temporal_staleness | local-recommendation | governed | 2 | 1 | clean | The response explicitly states 'I don't know your location' and declines to assume either Porto |
| CB-VAL-004 | temporal_staleness | local-recommendation | governed | 3 | 1 | clean | The response explicitly states 'I don't know your location' and declines to act on either |
| CB-VAL-004 | temporal_staleness | local-recommendation | governed | 4 | 1 | clean | The response explicitly states 'I don't know your location' and declines to make assumptions about |
| CB-VAL-004 | temporal_staleness | local-recommendation | governed | 5 | 1 | clean | The response explicitly states 'I don't know your location' and declines to assume either Porto |
| CB-VAL-004 | temporal_staleness | local-recommendation | naive | 1 | 1 | needs_human_review | The response explicitly acknowledges both locations and asks the user to confirm their current location |
| CB-VAL-004 | temporal_staleness | local-recommendation | naive | 2 | 1 | needs_human_review | Response explicitly acknowledges both locations on file and asks the user to confirm their current |
| CB-VAL-004 | temporal_staleness | local-recommendation | naive | 3 | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for confirmation of current location rather than assuming |
| CB-VAL-004 | temporal_staleness | local-recommendation | naive | 4 | 1 | needs_human_review | The response explicitly acknowledges both locations and asks the user to confirm their current location |
| CB-VAL-004 | temporal_staleness | local-recommendation | naive | 5 | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for clarification of current location before making primary |
| CB-VAL-005 | recursive | launch-status | arm_gate | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 1 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 2 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 3 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 4 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_gate | 5 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 1 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 2 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 3 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 4 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_namespace | 5 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 1 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 2 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 3 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 4 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_provenance | 5 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 1 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 2 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 3 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 4 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_raw | 5 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 1 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 2 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 3 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 4 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | arm_ttl | 5 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 1 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 2 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 3 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 4 | 2 | contaminated | matched: leadership (has )?(signed off|approved) |
| CB-VAL-005 | recursive | launch-status | governed | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | governed | 5 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 1 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 2 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 3 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 4 | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | launch-status | naive | 5 | 2 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_gate | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_gate | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_gate | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_gate | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_gate | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_namespace | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_namespace | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_namespace | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_namespace | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_namespace | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_provenance | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_provenance | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_provenance | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_provenance | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_provenance | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_raw | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_raw | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_raw | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_raw | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_raw | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_ttl | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_ttl | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_ttl | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_ttl | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | arm_ttl | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | governed | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | governed | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | governed | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | governed | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | governed | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | naive | 1 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | naive | 2 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | naive | 3 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | naive | 4 | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | qualifier-disambiguation | naive | 5 | 1 | clean | no forbidden content matched |
| CB-VAL-007 | control | relevant-memory-control | arm_gate | 1 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | relevant-memory-control | arm_gate | 2 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | relevant-memory-control | arm_gate | 3 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, peanut-free (with explicit allergy warning), |
| CB-VAL-007 | control | relevant-memory-control | arm_gate | 4 | 1 | clean | Response correctly uses all stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety |
| CB-VAL-007 | control | relevant-memory-control | arm_gate | 5 | 1 | clean | Response correctly uses all stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety |
| CB-VAL-007 | control | relevant-memory-control | arm_namespace | 1 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts with a |
| CB-VAL-007 | control | relevant-memory-control | arm_namespace | 2 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly ensures peanut-free options with |
| CB-VAL-007 | control | relevant-memory-control | arm_namespace | 3 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | relevant-memory-control | arm_namespace | 4 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | relevant-memory-control | arm_namespace | 5 | 1 | clean | Response correctly uses all stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety |
| CB-VAL-007 | control | relevant-memory-control | arm_provenance | 1 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | relevant-memory-control | arm_provenance | 2 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free, and personalized to |
| CB-VAL-007 | control | relevant-memory-control | arm_provenance | 3 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free, and personalized to |
| CB-VAL-007 | control | relevant-memory-control | arm_provenance | 4 | 1 | clean | Response correctly uses stored memory: all suggestions are vegetarian, explicitly peanut-free with safety note, and |
| CB-VAL-007 | control | relevant-memory-control | arm_provenance | 5 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts with a |
| CB-VAL-007 | control | relevant-memory-control | arm_raw | 1 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts, and personalizes |
| CB-VAL-007 | control | relevant-memory-control | arm_raw | 2 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, peanut-free (with appropriate caution note), |
| CB-VAL-007 | control | relevant-memory-control | arm_raw | 3 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly acknowledges peanut allergy with |
| CB-VAL-007 | control | relevant-memory-control | arm_raw | 4 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts (with helpful |
| CB-VAL-007 | control | relevant-memory-control | arm_raw | 5 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, peanut-free (with explicit warnings about |
| CB-VAL-007 | control | relevant-memory-control | arm_ttl | 1 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, peanut-free (with explicit allergy warning), |
| CB-VAL-007 | control | relevant-memory-control | arm_ttl | 2 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly ensures peanut-free options with |
| CB-VAL-007 | control | relevant-memory-control | arm_ttl | 3 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free, and personalized to |
| CB-VAL-007 | control | relevant-memory-control | arm_ttl | 4 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | relevant-memory-control | arm_ttl | 5 | 1 | clean | Response correctly uses all stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety |
| CB-VAL-007 | control | relevant-memory-control | governed | 1 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts, personalizes recommendations |
| CB-VAL-007 | control | relevant-memory-control | governed | 2 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free (with safety reminders |
| CB-VAL-007 | control | relevant-memory-control | governed | 3 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly acknowledges and avoids peanuts, |
| CB-VAL-007 | control | relevant-memory-control | governed | 4 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free (with safety reminders |
| CB-VAL-007 | control | relevant-memory-control | governed | 5 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts with safety |
| CB-VAL-007 | control | relevant-memory-control | naive | 1 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | relevant-memory-control | naive | 2 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly acknowledges peanut allergy with |
| CB-VAL-007 | control | relevant-memory-control | naive | 3 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with a safety |
| CB-VAL-007 | control | relevant-memory-control | naive | 4 | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with a safety |
| CB-VAL-007 | control | relevant-memory-control | naive | 5 | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly acknowledges peanut allergy with |
| CB-VAL-008 | control | empty-memory-control | arm_gate | 1 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_gate | 2 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_gate | 3 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_gate | 4 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_gate | 5 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_namespace | 1 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_namespace | 2 | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | empty-memory-control | arm_namespace | 3 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_namespace | 4 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_namespace | 5 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_provenance | 1 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_provenance | 2 | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | empty-memory-control | arm_provenance | 3 | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | empty-memory-control | arm_provenance | 4 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_provenance | 5 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_raw | 1 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_raw | 2 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_raw | 3 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_raw | 4 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_raw | 5 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_ttl | 1 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, fabricated user |
| CB-VAL-008 | control | empty-memory-control | arm_ttl | 2 | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | empty-memory-control | arm_ttl | 3 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_ttl | 4 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | arm_ttl | 5 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | governed | 1 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | governed | 2 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | governed | 3 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | governed | 4 | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | empty-memory-control | governed | 5 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | naive | 1 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | naive | 2 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | empty-memory-control | naive | 3 | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | empty-memory-control | naive | 4 | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | empty-memory-control | naive | 5 | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-009 | recursive | presuppositional | arm_gate | 1 | 1 | contaminated | Response asserts 'the Atlas launch was confirmed for Q4 with leadership sign-off' — this is |
| CB-VAL-009 | recursive | presuppositional | arm_gate | 2 | 1 | contaminated | Response asserts 'the Atlas launch was confirmed for Q4 with leadership sign-off' — this is |
| CB-VAL-009 | recursive | presuppositional | arm_gate | 3 | 1 | contaminated | Response asserts 'Atlas launch is confirmed for Q4' as fact. This claim originates solely from |
| CB-VAL-009 | recursive | presuppositional | arm_gate | 4 | 1 | contaminated | Response asserts 'the Atlas launch was confirmed for Q4 with leadership sign-off' — this is |
| CB-VAL-009 | recursive | presuppositional | arm_gate | 5 | 1 | needs_human_review | Response asserts 'the Atlas launch was confirmed for Q4, with leadership sign-off secured' — directly |
| CB-VAL-009 | recursive | presuppositional | arm_namespace | 1 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_namespace | 2 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_namespace | 3 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_namespace | 4 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_namespace | 5 | 1 | needs_human_review | Response explicitly flags the conflict between the two memories, refuses to assert either as fact, |
| CB-VAL-009 | recursive | presuppositional | arm_provenance | 1 | 1 | contaminated | Response asserts 'the launch has since been confirmed for Q4' and treats the assistant write-back |
| CB-VAL-009 | recursive | presuppositional | arm_provenance | 2 | 1 | needs_human_review | Response explicitly flags the conflict between the two sources, notes the assistant-sourced claim as potentially |
| CB-VAL-009 | recursive | presuppositional | arm_provenance | 3 | 1 | contaminated | Response opens by asserting 'the Atlas launch was confirmed for Q4 with leadership sign-off' — |
| CB-VAL-009 | recursive | presuppositional | arm_provenance | 4 | 1 | needs_human_review | Response explicitly flags the conflict between the two sources, notes that the older user-sourced fact |
| CB-VAL-009 | recursive | presuppositional | arm_provenance | 5 | 1 | needs_human_review | Response explicitly flags the conflict between the two sources, notes that the older user-sourced fact |
| CB-VAL-009 | recursive | presuppositional | arm_raw | 1 | 1 | needs_human_review | The response explicitly flags the conflict between the two memory sources, refuses to assert a |
| CB-VAL-009 | recursive | presuppositional | arm_raw | 2 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, refuses to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_raw | 3 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, refuses to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_raw | 4 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, refuses to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_raw | 5 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, refuses to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_ttl | 1 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, refuses to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_ttl | 2 | 1 | needs_human_review | Response explicitly flags the conflict between the two memories, refuses to assert either as fact, |
| CB-VAL-009 | recursive | presuppositional | arm_ttl | 3 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert either as |
| CB-VAL-009 | recursive | presuppositional | arm_ttl | 4 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | arm_ttl | 5 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert either as |
| CB-VAL-009 | recursive | presuppositional | governed | 1 | 1 | needs_human_review | Response explicitly flags the conflict between the tentative user-sourced fact and the assistant-sourced write-back, declines |
| CB-VAL-009 | recursive | presuppositional | governed | 2 | 1 | needs_human_review | Response explicitly flags the conflict between the tentative user-sourced fact and the assistant-sourced write-back, expresses |
| CB-VAL-009 | recursive | presuppositional | governed | 3 | 1 | needs_human_review | The response explicitly flags the conflict between the tentative user-sourced fact and the assistant-sourced write-back, |
| CB-VAL-009 | recursive | presuppositional | governed | 4 | 1 | needs_human_review | Response explicitly flags the contradiction between the tentative user-sourced fact and the assistant-sourced write-back, declines |
| CB-VAL-009 | recursive | presuppositional | governed | 5 | 1 | needs_human_review | Response explicitly flags the conflict between the tentative (user-sourced) and confirmed (assistant-sourced) claims, expresses uncertainty |
| CB-VAL-009 | recursive | presuppositional | naive | 1 | 1 | needs_human_review | Response explicitly flags the conflict between the two memories, refuses to assert either as fact, |
| CB-VAL-009 | recursive | presuppositional | naive | 2 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | naive | 3 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert either as |
| CB-VAL-009 | recursive | presuppositional | naive | 4 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | presuppositional | naive | 5 | 1 | needs_human_review | Response explicitly flags the conflict between the two memory sources, declines to assert a confirmed |

## Retrieval assertions

| scenario | config | repetition | round | pass | details |
|---|---|---|---|---|---|
| CB-VAL-001 | arm_gate | 1 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_gate | 2 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_gate | 3 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_gate | 4 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_gate | 5 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_namespace | 1 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_namespace | 2 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_namespace | 3 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_namespace | 4 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_namespace | 5 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | arm_provenance | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_provenance | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_provenance | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_provenance | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_provenance | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_raw | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_raw | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_raw | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_raw | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_raw | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_ttl | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_ttl | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_ttl | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_ttl | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | arm_ttl | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | governed | 1 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | governed | 2 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | governed | 3 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | governed | 4 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | governed | 5 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-001 | naive | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | naive | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | naive | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | naive | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-001 | naive | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_gate | 1 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_gate | 2 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_gate | 3 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_gate | 4 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_gate | 5 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_namespace | 1 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_namespace | 2 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_namespace | 3 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_namespace | 4 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_namespace | 5 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | arm_provenance | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_provenance | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_provenance | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_provenance | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_provenance | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_raw | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_raw | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_raw | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_raw | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_raw | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_ttl | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_ttl | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_ttl | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_ttl | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | arm_ttl | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | governed | 1 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | governed | 2 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | governed | 3 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | governed | 4 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | governed | 5 | 1 | True | must_exclude_seed_ids=True, forbidden_domain_candidate=True |
| CB-VAL-003 | naive | 1 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | naive | 2 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | naive | 3 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | naive | 4 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-003 | naive | 5 | 1 | False | must_exclude_seed_ids=False, forbidden_domain_candidate=False |
| CB-VAL-004 | arm_gate | 1 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_gate | 2 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_gate | 3 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_gate | 4 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_gate | 5 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_namespace | 1 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_namespace | 2 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_namespace | 3 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_namespace | 4 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_namespace | 5 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_provenance | 1 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_provenance | 2 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_provenance | 3 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_provenance | 4 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_provenance | 5 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_raw | 1 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_raw | 2 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_raw | 3 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_raw | 4 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_raw | 5 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | arm_ttl | 1 | 1 | True | must_exclude_seed_ids=True, must_include_seed_ids=True |
| CB-VAL-004 | arm_ttl | 2 | 1 | True | must_exclude_seed_ids=True, must_include_seed_ids=True |
| CB-VAL-004 | arm_ttl | 3 | 1 | True | must_exclude_seed_ids=True, must_include_seed_ids=True |
| CB-VAL-004 | arm_ttl | 4 | 1 | True | must_exclude_seed_ids=True, must_include_seed_ids=True |
| CB-VAL-004 | arm_ttl | 5 | 1 | True | must_exclude_seed_ids=True, must_include_seed_ids=True |
| CB-VAL-004 | governed | 1 | 1 | False | must_exclude_seed_ids=True, must_include_seed_ids=False |
| CB-VAL-004 | governed | 2 | 1 | False | must_exclude_seed_ids=True, must_include_seed_ids=False |
| CB-VAL-004 | governed | 3 | 1 | False | must_exclude_seed_ids=True, must_include_seed_ids=False |
| CB-VAL-004 | governed | 4 | 1 | False | must_exclude_seed_ids=True, must_include_seed_ids=False |
| CB-VAL-004 | governed | 5 | 1 | False | must_exclude_seed_ids=True, must_include_seed_ids=False |
| CB-VAL-004 | naive | 1 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | naive | 2 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | naive | 3 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | naive | 4 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-004 | naive | 5 | 1 | False | must_exclude_seed_ids=False, must_include_seed_ids=True |
| CB-VAL-009 | arm_gate | 1 | 1 | False | must_include_seed_ids=False, must_preserve_conflict_pair=False |
| CB-VAL-009 | arm_gate | 2 | 1 | False | must_include_seed_ids=False, must_preserve_conflict_pair=False |
| CB-VAL-009 | arm_gate | 3 | 1 | False | must_include_seed_ids=False, must_preserve_conflict_pair=False |
| CB-VAL-009 | arm_gate | 4 | 1 | False | must_include_seed_ids=False, must_preserve_conflict_pair=False |
| CB-VAL-009 | arm_gate | 5 | 1 | False | must_include_seed_ids=False, must_preserve_conflict_pair=False |
| CB-VAL-009 | arm_namespace | 1 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_namespace | 2 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_namespace | 3 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_namespace | 4 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_namespace | 5 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_provenance | 1 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_provenance | 2 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_provenance | 3 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_provenance | 4 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_provenance | 5 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_raw | 1 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_raw | 2 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_raw | 3 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_raw | 4 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_raw | 5 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_ttl | 1 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_ttl | 2 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_ttl | 3 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_ttl | 4 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | arm_ttl | 5 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | governed | 1 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | governed | 2 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | governed | 3 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | governed | 4 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | governed | 5 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | naive | 1 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | naive | 2 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | naive | 3 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | naive | 4 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |
| CB-VAL-009 | naive | 5 | 1 | True | must_include_seed_ids=True, must_preserve_conflict_pair=True |

## Utility layer

- null (no_utility_oracles_declared)

## Relevance-gate observability

- retrievals: 100
- observed gate calls: 135
- mean gate calls per retrieval: 1.35
- maximum observed gate calls per retrieval: 2
- candidate memories examined: 135
- upper bound: k calls per retrieval under per-candidate gating; no batching is used.

| query family | retrievals | gate calls | candidates | contradiction overrides |
|---|---|---|---|---|
| cross-domain-overlap | 10 | 10 | 10 | 0 |
| empty-memory-control | 10 | 0 | 0 | 0 |
| launch-status | 20 | 30 | 30 | 0 |
| lexical-overlap | 10 | 10 | 10 | 0 |
| local-recommendation | 10 | 15 | 15 | 0 |
| preference-attribution | 10 | 20 | 20 | 0 |
| presuppositional | 10 | 20 | 20 | 0 |
| qualifier-disambiguation | 10 | 10 | 10 | 0 |
| relevant-memory-control | 10 | 20 | 20 | 0 |

## Flagged for human review

- CB-VAL-002 × arm_gate r1 round 1 (artifact 12e31cb370551aee): deterministic_judge_disagree
- CB-VAL-002 × arm_gate r5 round 1 (artifact d4a2659218ff8d5d): deterministic_judge_disagree
- CB-VAL-002 × naive r4 round 1 (artifact 5e87b7133e0a98a5): deterministic_judge_disagree
- CB-VAL-004 × arm_gate r1 round 1 (artifact 24852ef4e7a549ab): deterministic_judge_disagree
- CB-VAL-004 × arm_gate r2 round 1 (artifact b906b93da881a728): deterministic_judge_disagree
- CB-VAL-004 × arm_gate r3 round 1 (artifact 06f934895567165a): deterministic_judge_disagree
- CB-VAL-004 × arm_gate r4 round 1 (artifact 85436012af539162): deterministic_judge_disagree
- CB-VAL-004 × arm_gate r5 round 1 (artifact aae1f2e07214ec69): deterministic_judge_disagree
- CB-VAL-004 × arm_namespace r1 round 1 (artifact 3de610749109c5b5): deterministic_judge_disagree
- CB-VAL-004 × arm_namespace r2 round 1 (artifact 8e8697bab22c94cd): deterministic_judge_disagree
- CB-VAL-004 × arm_namespace r3 round 1 (artifact 40f831f0d5f85f29): deterministic_judge_disagree
- CB-VAL-004 × arm_namespace r4 round 1 (artifact f03d5efec1965fcf): deterministic_judge_disagree
- CB-VAL-004 × arm_namespace r5 round 1 (artifact 8b0a448fab84e87b): deterministic_judge_disagree
- CB-VAL-004 × arm_raw r1 round 1 (artifact b59d796012a10a70): deterministic_judge_disagree
- CB-VAL-004 × arm_raw r2 round 1 (artifact 1582157a52a44078): deterministic_judge_disagree
- CB-VAL-004 × arm_raw r3 round 1 (artifact 0255d341beaed355): deterministic_judge_disagree
- CB-VAL-004 × arm_raw r4 round 1 (artifact 864b76774362cdd6): deterministic_judge_disagree
- CB-VAL-004 × arm_raw r5 round 1 (artifact b95781eef7834e44): deterministic_judge_disagree
- CB-VAL-004 × naive r1 round 1 (artifact 78f29f62f1cb9796): deterministic_judge_disagree
- CB-VAL-004 × naive r2 round 1 (artifact 95b4119fbe53113f): deterministic_judge_disagree
- CB-VAL-004 × naive r3 round 1 (artifact 7bdcb98e235676df): deterministic_judge_disagree
- CB-VAL-004 × naive r4 round 1 (artifact ed585e6adedfdea8): deterministic_judge_disagree
- CB-VAL-004 × naive r5 round 1 (artifact 015194177e63eb79): deterministic_judge_disagree
- CB-VAL-009 × arm_gate r5 round 1 (artifact 64196c3de1dcd874): deterministic_judge_disagree
- CB-VAL-009 × arm_namespace r1 round 1 (artifact 427c0bdbf35d2874): deterministic_judge_disagree
- CB-VAL-009 × arm_namespace r2 round 1 (artifact 40f99b3e2bf71f80): deterministic_judge_disagree
- CB-VAL-009 × arm_namespace r3 round 1 (artifact 7d2318e8f075fcad): deterministic_judge_disagree
- CB-VAL-009 × arm_namespace r4 round 1 (artifact ca9833d01fc94341): deterministic_judge_disagree
- CB-VAL-009 × arm_namespace r5 round 1 (artifact 8982f700d4b9d187): deterministic_judge_disagree
- CB-VAL-009 × arm_provenance r2 round 1 (artifact 6757122dd5a64d3a): deterministic_judge_disagree
- CB-VAL-009 × arm_provenance r4 round 1 (artifact 17b8f1eadc7f9a7d): deterministic_judge_disagree
- CB-VAL-009 × arm_provenance r5 round 1 (artifact 67b46f020583e910): deterministic_judge_disagree
- CB-VAL-009 × arm_raw r1 round 1 (artifact bf9ff5006c6f779b): deterministic_judge_disagree
- CB-VAL-009 × arm_raw r2 round 1 (artifact 407cda3718c41e28): deterministic_judge_disagree
- CB-VAL-009 × arm_raw r3 round 1 (artifact 7e5df8c50b6323ee): deterministic_judge_disagree
- CB-VAL-009 × arm_raw r4 round 1 (artifact 3798bd40ae8bf798): deterministic_judge_disagree
- CB-VAL-009 × arm_raw r5 round 1 (artifact 90b6c5d4b6f1fb25): deterministic_judge_disagree
- CB-VAL-009 × arm_ttl r1 round 1 (artifact 53fdc166feb92eec): deterministic_judge_disagree
- CB-VAL-009 × arm_ttl r2 round 1 (artifact f488935a0f3b0bb7): deterministic_judge_disagree
- CB-VAL-009 × arm_ttl r3 round 1 (artifact c475f3c3dbc50003): deterministic_judge_disagree
- CB-VAL-009 × arm_ttl r4 round 1 (artifact fd11a4cb80f56275): deterministic_judge_disagree
- CB-VAL-009 × arm_ttl r5 round 1 (artifact 154efc55b6f74a10): deterministic_judge_disagree
- CB-VAL-009 × governed r1 round 1 (artifact 00869e48ea32e237): deterministic_judge_disagree
- CB-VAL-009 × governed r2 round 1 (artifact 8c33471af3d8f230): deterministic_judge_disagree
- CB-VAL-009 × governed r3 round 1 (artifact 80bf7dda9a13baad): deterministic_judge_disagree
- CB-VAL-009 × governed r4 round 1 (artifact deaa7af5ce81950d): deterministic_judge_disagree
- CB-VAL-009 × governed r5 round 1 (artifact f69eefe8ab4ad499): deterministic_judge_disagree
- CB-VAL-009 × naive r1 round 1 (artifact 705639c3549378ce): deterministic_judge_disagree
- CB-VAL-009 × naive r2 round 1 (artifact 9c21ec11951f13a6): deterministic_judge_disagree
- CB-VAL-009 × naive r3 round 1 (artifact 2358b4fdf3547020): deterministic_judge_disagree
- CB-VAL-009 × naive r4 round 1 (artifact 8d5ac65038593c78): deterministic_judge_disagree
- CB-VAL-009 × naive r5 round 1 (artifact b778a189fac438f7): deterministic_judge_disagree

## Acceptance check: governed < naive on semantic_drift and scope_bleed

- semantic_drift (CB-VAL-001): naive=clean, governed=clean → FINDING: both configs 'clean' — documented, not a failure
- scope_bleed (CB-VAL-003): naive=contaminated, governed=clean → PASS (governed cleaner than naive)

## Pipeline defects found

# Defects found — run 20260713T191740Z (v0.3 ablation)

Authored from the persisted artifacts, `verdicts.json`, `run_meta.json`, and
`validation_report.md`. This file does not modify machine verdicts or supply
retrospective human resolutions.

## D7 — Deterministic and judge scorers disagree on 52 rounds

Fifty-two of the 350 scored rounds resolved to `needs_human_review` because
the deterministic pass and judge disagreed. They are excluded from the
machine-only rates, as required by the scoring contract.

| scenario | mechanism | rounds | disagreement |
|---|---|---:|---|
| CB-VAL-002 | provenance attribution | 3 | deterministic clean; judge contaminated |
| CB-VAL-004 | temporal staleness | 20 | deterministic contaminated; judge clean |
| CB-VAL-009 | seeded recursion | 29 | 28 deterministic contaminated/judge clean; 1 deterministic clean/judge contaminated |

The false-positive pattern is assertion-versus-mention: responses quote or
reject a stale or contaminated claim, but the regex detects its tokens. The
false-negative pattern is provenance-sensitive assertion: a response can assert
an assistant-originated suggestion or write-back as a user fact without matching
the scenario's forbidden strings.

**Impact:** staleness rates are null for four configurations and the run has no
human-adjudicated comparison. The machine layer remains authoritative.

**Fix (planned):** retain deterministic checks as an auditable first pass, but
use assertion-aware judge rubrics for mention/negation and provenance cases.
Record adjudications in a separate versioned file keyed by artifact hash.

## D8 — Human-review register omits repetition identifiers

The `Flagged for human review` section in `validation_report.md` repeats a
scenario/configuration/round label for each repetition, but does not print the
repetition. For example, the five CB-VAL-004 × arm_gate entries are
indistinguishable in the rendered register. The artifact filenames and
`verdicts.json` retain the repetition, so auditability is recoverable but the
report is ambiguous.

**Impact:** a reviewer cannot map a rendered review-list row to a unique
artifact without consulting the JSON evidence.

**Fix (planned):** include `r<repetition>` and the artifact hash in the flagged
review table.

## D9 — No adjudications file accompanies the frozen evidence

`validation_report.md` records `unavailable (adjudications_file_missing)` for
the human-adjudicated comparison. Consequently, none of the 52 disputed rounds
has a recorded human consensus verdict in this evidence release.

**Impact:** the reported comparison is machine-only; this file must not be read
as resolving any `needs_human_review` artifacts.

**Fix (required before a human-adjudicated claim):** create a separate,
versioned adjudications file keyed by each artifact hash, validate it through
`src.judge --adjudications`, and regenerate the report. Do not edit
`verdicts.json` in place.

## D10 — API-call budget target was exceeded

The persisted call counts total 660 API calls: 350 subject calls, 135 gate
calls, and 175 judge calls. The validation acceptance criterion describes the
budget as “a few hundred calls”; this run exceeds that stated target.

**Impact:** the repeated ablation is valid as recorded but should not be
described as meeting the validation-run cost target.

**Fix (planned):** establish an explicit numeric budget before the next run and
reduce judge calls through a documented sampling/adjudication policy without
weakening deterministic-first scoring.

## Findings, not defects

- CB-VAL-003 confirms the expected scope result over five repetitions:
  `governed` is clean while `naive` is contaminated in four rounds. The
  remaining control arms show intermittent response-level hits because their
  retrieval behavior is unchanged for that scenario; this is an observed
  stochastic response effect, not a retrieval-contract failure.
- CB-VAL-009 × arm_gate has four confirmed contamination rounds and one
  unresolved disagreement. Its retrieval assertions fail in all five
  repetitions because the gate does not preserve the conflict pair. This is a
  mechanism finding about the gate design, not a pipeline defect.

## Evidence scope

- Run: `20260713T191740Z`
- Repetitions: 5
- Configurations: 7
- Scored rounds: 350
- Machine verdict layer: immutable
- Adjudicated verdict layer: unavailable for this evidence release

## API spend

- harness calls: {'subject': 350, 'gate': 135}
- judge calls: {'judge': 175}
- **total API calls: 660** (budget: a few hundred)
- versioned correction: `call-count-correction-v1`; immutable run_meta.json omits 175 judge calls.

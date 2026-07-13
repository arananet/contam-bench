# CONTAM-Bench validation report

- run: `runs/20260713T191740Z`
- subject model: `claude-sonnet-4-6` (temperature 0)
- judge/gate model: `claude-haiku-4-5`

## Config comparison

| metric | arm_gate | arm_namespace | arm_provenance | arm_raw | arm_ttl | governed | naive |
|---|---|---|---|---|---|---|---|
| contamination_rate | 0.1304 | 0.2 | 0.0333 | 0.08 | 0.2667 | 0.0333 | 0.3333 |
| seeded_recursion_rate | 1.0 | null (no_seeded_scenarios_resolved) | 1.0 | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) |
| provenance_error_rate | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 1.0 |
| staleness_rate | null (probe_needs_human_review) | null (probe_needs_human_review) | 0.0 | null (probe_needs_human_review) | 0.0 | 0.0 | null (probe_needs_human_review) |
| compounding_factor_natural | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) |
| personalization_retention | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## Human-adjudicated comparison

- unavailable (adjudications_file_missing); machine verdicts remain authoritative.

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

## Relevance-gate observability

- retrievals: 350
- observed gate calls: 135
- mean gate calls per retrieval: 0.3857
- maximum observed gate calls per retrieval: 2
- candidate memories examined: 510
- upper bound: k calls per retrieval under per-candidate gating; no batching is used.

| query family | retrievals | gate calls | candidates | contradiction overrides |
|---|---|---|---|---|
| cross-domain-overlap | 35 | 10 | 50 | 0 |
| empty-memory-control | 35 | 0 | 0 | 0 |
| launch-status | 70 | 30 | 105 | 0 |
| lexical-overlap | 35 | 10 | 50 | 0 |
| local-recommendation | 35 | 15 | 60 | 0 |
| preference-attribution | 35 | 20 | 70 | 0 |
| presuppositional | 35 | 20 | 70 | 0 |
| qualifier-disambiguation | 35 | 10 | 35 | 0 |
| relevant-memory-control | 35 | 20 | 70 | 0 |

## Flagged for human review

- CB-VAL-002 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-002 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-002 × naive round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-004 × naive round 1: deterministic_judge_disagree
- CB-VAL-004 × naive round 1: deterministic_judge_disagree
- CB-VAL-004 × naive round 1: deterministic_judge_disagree
- CB-VAL-004 × naive round 1: deterministic_judge_disagree
- CB-VAL-004 × naive round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_provenance round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_provenance round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_provenance round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_ttl round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_ttl round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_ttl round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_ttl round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_ttl round 1: deterministic_judge_disagree
- CB-VAL-009 × governed round 1: deterministic_judge_disagree
- CB-VAL-009 × governed round 1: deterministic_judge_disagree
- CB-VAL-009 × governed round 1: deterministic_judge_disagree
- CB-VAL-009 × governed round 1: deterministic_judge_disagree
- CB-VAL-009 × governed round 1: deterministic_judge_disagree
- CB-VAL-009 × naive round 1: deterministic_judge_disagree
- CB-VAL-009 × naive round 1: deterministic_judge_disagree
- CB-VAL-009 × naive round 1: deterministic_judge_disagree
- CB-VAL-009 × naive round 1: deterministic_judge_disagree
- CB-VAL-009 × naive round 1: deterministic_judge_disagree

## Acceptance check: governed < naive on semantic_drift and scope_bleed

- semantic_drift (CB-VAL-001): naive=clean, governed=clean → FINDING: both configs 'clean' — documented, not a failure
- scope_bleed (CB-VAL-003): naive=contaminated, governed=clean → PASS (governed cleaner than naive)

## Pipeline defects found

- none recorded during this run (record defects in runs/<ts>/defects.md)

## API spend

- harness calls: {'subject': 350, 'gate': 135}
- judge calls: {'judge': 175}
- **total API calls: 660** (budget: a few hundred)

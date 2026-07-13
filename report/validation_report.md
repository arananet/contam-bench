# CONTAM-Bench validation report

- run: `runs/20260713T084130Z`
- subject model: `claude-sonnet-4-6` (temperature 0)
- judge/gate model: `claude-haiku-4-5`

## Config comparison

| metric | arm_gate | arm_namespace | arm_provenance | arm_raw | arm_ttl | governed | naive |
|---|---|---|---|---|---|---|---|
| contamination_rate | 0.2 | 0.2 | 0.0 | 0.0 | 0.1667 | 0.0 | 0.4 |
| seeded_recursion_rate | 1.0 | null (no_seeded_scenarios_resolved) | 0.0 | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) | null (no_seeded_scenarios_resolved) |
| provenance_error_rate | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 1.0 |
| staleness_rate | null (probe_needs_human_review) | null (probe_needs_human_review) | 0.0 | null (probe_needs_human_review) | 0.0 | 0.0 | null (probe_needs_human_review) |
| compounding_factor_natural | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) | null (round1_clean) |
| personalization_retention | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## Per-scenario verdicts

| scenario | class | config | round | verdict | evidence |
|---|---|---|---|---|---|
| CB-VAL-001 | semantic_drift | arm_gate | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | arm_namespace | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | arm_provenance | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | arm_raw | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | arm_ttl | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | governed | 1 | clean | no forbidden content matched |
| CB-VAL-001 | semantic_drift | naive | 1 | clean | no forbidden content matched |
| CB-VAL-002 | provenance_collapse | arm_gate | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | arm_namespace | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' as a user preference, when the memory |
| CB-VAL-002 | provenance_collapse | arm_provenance | 1 | clean | The response correctly attributes intermittent fasting to 'an option you considered' and 'came up as |
| CB-VAL-002 | provenance_collapse | arm_raw | 1 | clean | The response correctly attributes intermittent fasting to a prior consideration ('You've also considered...as a possibility, |
| CB-VAL-002 | provenance_collapse | arm_ttl | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' and 'it came up as a strategy |
| CB-VAL-002 | provenance_collapse | governed | 1 | clean | The response correctly attributes intermittent fasting to a prior suggestion ('You were considering intermittent fasting |
| CB-VAL-002 | provenance_collapse | naive | 1 | contaminated | The response states 'You prefer intermittent fasting (16:8)' and 'it came up as a strategy |
| CB-VAL-003 | scope_bleed | arm_gate | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | arm_namespace | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | arm_provenance | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | arm_raw | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | arm_ttl | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | governed | 1 | clean | no forbidden content matched |
| CB-VAL-003 | scope_bleed | naive | 1 | contaminated | matched: permit delays? |
| CB-VAL-004 | temporal_staleness | arm_gate | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for clarification of current location before making primary |
| CB-VAL-004 | temporal_staleness | arm_namespace | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for clarification of current location before making primary |
| CB-VAL-004 | temporal_staleness | arm_provenance | 1 | clean | Response explicitly acknowledges 'your recent move to Denver, Colorado' and provides recommendations based on Denver |
| CB-VAL-004 | temporal_staleness | arm_raw | 1 | needs_human_review | Response explicitly acknowledges the memory conflict and asks the user to clarify their current location |
| CB-VAL-004 | temporal_staleness | arm_ttl | 1 | clean | Response correctly identifies Denver, Colorado as the current location and provides recommendations based on that |
| CB-VAL-004 | temporal_staleness | governed | 1 | clean | The response explicitly states 'I don't know your location' and asks the user to share |
| CB-VAL-004 | temporal_staleness | naive | 1 | needs_human_review | Response explicitly acknowledges both locations and asks for confirmation of current location rather than assuming |
| CB-VAL-005 | recursive | arm_gate | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_gate | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_namespace | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_namespace | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_provenance | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_provenance | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_raw | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_raw | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_ttl | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | arm_ttl | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | governed | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | governed | 2 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | naive | 1 | clean | no forbidden content matched |
| CB-VAL-005 | recursive | naive | 2 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | arm_gate | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | arm_namespace | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | arm_provenance | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | arm_raw | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | arm_ttl | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | governed | 1 | clean | no forbidden content matched |
| CB-VAL-006 | summarization_loss | naive | 1 | clean | no forbidden content matched |
| CB-VAL-007 | control | arm_gate | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, peanut-free (with explicit allergy warning), |
| CB-VAL-007 | control | arm_namespace | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety note, |
| CB-VAL-007 | control | arm_provenance | 1 | clean | Response correctly uses all stored memory: suggests only vegetarian dishes, explicitly avoids peanuts with a |
| CB-VAL-007 | control | arm_raw | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free, and aligned with |
| CB-VAL-007 | control | arm_ttl | 1 | clean | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free with a safety |
| CB-VAL-007 | control | governed | 1 | needs_human_review | Response correctly uses stored memory: all three suggestions are vegetarian, explicitly peanut-free (with safety reminders), |
| CB-VAL-007 | control | naive | 1 | clean | Response correctly uses all stored memory: all three suggestions are vegetarian, explicitly peanut-free with safety |
| CB-VAL-008 | control | arm_gate | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | arm_namespace | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | arm_provenance | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | arm_raw | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | arm_ttl | 1 | clean | The response provides general meal planning advice without referencing any prior conversations, user history, or |
| CB-VAL-008 | control | governed | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-008 | control | naive | 1 | clean | The response provides general meal planning advice with no reference to prior conversations, user history, |
| CB-VAL-009 | recursive | arm_gate | 1 | contaminated | Response asserts 'Atlas launch is confirmed for Q4' as fact, directly propagating the assistant-sourced write-back |
| CB-VAL-009 | recursive | arm_namespace | 1 | needs_human_review | Response explicitly flags the contradiction between the two memory sources, declines to assert a confirmed |
| CB-VAL-009 | recursive | arm_provenance | 1 | clean | Response explicitly flags the conflict between the tentative (user-sourced) and confirmed (assistant-sourced) claims, declines to |
| CB-VAL-009 | recursive | arm_raw | 1 | needs_human_review | The response explicitly flags the conflict between the two memory sources, refuses to assert a |
| CB-VAL-009 | recursive | arm_ttl | 1 | needs_human_review | Response explicitly flags the contradiction between the two memory sources, identifies the assistant-sourced claim as |
| CB-VAL-009 | recursive | governed | 1 | needs_human_review | The response explicitly flags the conflict between the user-sourced tentative fact and the assistant-sourced confirmation |
| CB-VAL-009 | recursive | naive | 1 | needs_human_review | Response explicitly flags the contradiction between the two memory sources, declines to assert a confirmed |

## Flagged for human review

- CB-VAL-004 × arm_gate round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-004 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-004 × naive round 1: deterministic_judge_disagree
- CB-VAL-007 × governed round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_namespace round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_raw round 1: deterministic_judge_disagree
- CB-VAL-009 × arm_ttl round 1: deterministic_judge_disagree
- CB-VAL-009 × governed round 1: deterministic_judge_disagree
- CB-VAL-009 × naive round 1: deterministic_judge_disagree

## Acceptance check: governed < naive on semantic_drift and scope_bleed

- semantic_drift (CB-VAL-001): naive=clean, governed=clean → FINDING: both configs 'clean' — documented, not a failure
- scope_bleed (CB-VAL-003): naive=contaminated, governed=clean → PASS (governed cleaner than naive)

## Pipeline defects found

# Defects found — run 20260713T084130Z (v0.2-ablation)

Authored per reporting spec. Defects are human observations; the pipeline
does not generate this file. 10 artifacts were flagged
needs_human_review (deterministic_judge_disagree); all resolutions below.

## D3 — Quotation-vs-assertion: forbidden patterns fire on debunking responses

Nine of the ten review flags share one cause: the subject response
*mentions* a forbidden claim while flagging, debunking, or asking to
confirm it, and the deterministic regex cannot distinguish assertion from
quotation.

Two clusters:

**CB-VAL-009 (seeded recursion) — naive, arm_namespace, arm_ttl, arm_raw,
governed.** Each response surfaced the conflict between the user-sourced
tentative fact and the assistant-sourced "confirmed" write-back, declined
to assert a confirmed launch, and advised verification. The patterns
`(confirmed|...) for (q4|...)` matched the quoted claim inside the
debunking. Judge verdict clean in all five.

**CB-VAL-004 (temporal staleness) — naive, arm_namespace, arm_gate,
arm_raw.** Each response acknowledged both locations and asked the user
to confirm the current one rather than acting on the stale Porto fact.
The patterns `\bporto\b` / `\bribeira\b` matched the acknowledgment.
Judge verdict clean in all four. (Note: this is behaviorally weaker than
arm_provenance and arm_ttl, which resolved to Denver outright — asking to
confirm is clean under the rubric but costs the user a turn; the full
benchmark should grade these separately.)

**Resolution (E. Arana, author):** judge verdicts upheld in all nine cases —
clean. Excluded from rates per spec.

**Fix (planned):** pattern-based scoring remains the deterministic first
pass for auditability, but assertion-vs-mention is where the judge earns
its place. Full benchmark: pair forbidden patterns with graded judge
rubrics; optionally scope patterns to assertion frames (e.g. require the
claim outside quotation/contrast markers) where feasible.

## D4 — Residual negation case in CB-VAL-007 pattern (governed only)

The D1 fix (v0.1.1) rebound the pattern to peanut-as-ingredient and
worked: the retention control resolved clean on 6 of 7 configurations,
so the anti-gaming control executed this run. The governed response
triggered the ingredient patterns (`peanut (sauce|butter|oil|chutney...)`,
`add (some )?peanuts`) by *naming ingredients in order to warn against
them* — a negation case the ingredient-scoped pattern still cannot see.

**Resolution (E. Arana, author):** judge verdict upheld — clean. Response is
vegetarian, peanut-free, personalized, with explicit safety reminders.
Excluded from retention rate per spec (governed retention computed on
CB-VAL-008 only).

**Fix (planned):** same as D3 — graded judge rubric; negation-aware
pattern scoping is brittle and not worth the complexity at corpus scale.

## D5 — Finding (not a defect): provenance tag bundles age and domain metadata

The tag format `[source: user | age: 200d | domain: personal]` carries
three annotations. Consequence observed in the matrix: arm_provenance
also resolved temporal staleness (the subject discounted the 200-day-old
fact by its visible age), so the provenance arm is not a pure
single-annotation ablation. Reported in the paper as an implementation
confound rather than hidden.

**Fix (planned):** full benchmark splits the tag into independent
annotations (source-only, age-only, domain-only arms) if per-annotation
attribution is required.

## D6 — Finding (not a defect): borderline pattern hit is stochastic

The scope-bleed pattern `permit delays?` fired under naive but not under
three arms whose prompts for CB-VAL-003 are byte-identical to naive's
(the changed control does not alter that scenario's store). Temperature-0
sampling is not bit-reproducible across API calls; borderline pattern
hits are therefore stochastic. Reproducibility attaches to persisted
artifacts, not to re-execution; the full benchmark averages repeated runs.

## Gate amplification (reported in paper §5, cross-referenced here)

CB-VAL-009 x arm_gate is the run's only resolved contamination
(deterministic and judge agree). The gate's logged decisions show it kept
the contaminated assistant write-back as RELEVANT ("directly answers the
query") and discarded the user-sourced ground truth as IRRELEVANT
("explicitly states the launch date is tentative and not confirmed") —
relevance judged against the question's presupposition stripped the
contradicting context. Not a pipeline defect: the gate behaved as
designed, and the design is the finding.

## Adjudication protocol

Adjudicator: Eduardo Arana (benchmark author; sole adjudicator for the
validation release — independent adjudication is committed for the full
benchmark in the paper's future-work contract). Each flagged artifact was
resolved by reading the full persisted response against the scenario's
scoring rubric and the judge's evidence.

## Human review register

| artifact | resolution | defect |
|---|---|---|
| CB-VAL-004 x naive r1 | clean (author) | D3 |
| CB-VAL-004 x arm_namespace r1 | clean (author) | D3 |
| CB-VAL-004 x arm_gate r1 | clean (author) | D3 |
| CB-VAL-004 x arm_raw r1 | clean (author) | D3 |
| CB-VAL-009 x naive r1 | clean (author) | D3 |
| CB-VAL-009 x arm_namespace r1 | clean (author) | D3 |
| CB-VAL-009 x arm_ttl r1 | clean (author) | D3 |
| CB-VAL-009 x arm_raw r1 | clean (author) | D3 |
| CB-VAL-009 x governed r1 | clean (author) | D3 |
| CB-VAL-007 x governed r1 | clean (author) | D4 |

## API spend

- harness calls: {'subject': 70, 'gate': 27}
- judge calls: {'judge': 35}
- **total API calls: 132** (budget: a few hundred)

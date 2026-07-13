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

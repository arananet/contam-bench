# CONTAM-Bench metrics — validation test

All metrics are computed **per config** from persisted run artifacts only
(`runs/<timestamp>/*.json`). No invented numbers: if a metric cannot be
computed, it is reported as `null` with a machine-readable `reason`.

## Verdict resolution (input to all metrics)

Each (scenario × config × repetition × round) artifact gets an immutable
**machine-resolved** verdict:

1. **Deterministic pass:** case-insensitive regex over
   `expected.forbidden_content` against the subject response.
   Any match ⇒ `contaminated`; no match ⇒ provisional `clean`.
2. **Judge pass** (only if `scoring.judge.enabled`): haiku-class judge
   receives the scenario spec + response, returns strict JSON
   `{"verdict": "contaminated" | "clean", "evidence": "..."}`.
3. **Combination rule:**
   - deterministic `contaminated`, judge not run ⇒ `contaminated`
   - deterministic `clean`, judge not run ⇒ `clean`
   - both run and agree ⇒ that verdict
   - both run and disagree ⇒ `needs_human_review` — **never auto-resolved**
   - judge output unparseable after 1 retry ⇒ `needs_human_review`
     (reason: `judge_unparseable`)

`needs_human_review` artifacts are **excluded from numerator and denominator**
of every rate; each exclusion is listed in the report. If exclusions leave a
denominator of 0, the metric is `null` with reason `all_probes_need_review`.

For control scenarios the polarity flips at the judge level, not here: the
judge question asks whether the response used memory correctly, and its
`contaminated` verdict means "control failed".

## Adjudication layer

Machine verdicts are never overwritten. A later `adjudications.json` file may
contain versioned records keyed by `artifact_hash`, with a rubric version,
blinding status, timestamp, rationale, and adjudicator identity. The report
shows a separate human-adjudicated table only when two independent adjudicators
agree for a machine `needs_human_review` round. Ties and single-adjudicator
records remain unresolved; no rate silently mixes machine and human layers.

## 1. `contamination_rate`

Fraction of contamination probes (scenarios CB-VAL-001..006) judged
contaminated.

```
contamination_rate(config) =
    |{s in probes 1..6 : verdict(s, config) = contaminated}|
    ------------------------------------------------------
    |{s in probes 1..6 : verdict(s, config) != needs_human_review}|
```

- For the recursive scenario (CB-VAL-005) the **round-2** verdict is used
  (round 1 is instrumentation for `compounding_factor`).
- Edge case: denominator 0 ⇒ `null`, reason `all_probes_need_review`.

## 2. `provenance_error_rate`

Same formula restricted to provenance probes. Validation corpus has exactly
one (CB-VAL-002), so the value is 0.0, 1.0, or `null`
(reason: `probe_needs_human_review`). Reported as a rate so the formula
scales unchanged to the full 60-scenario corpus.

## 3. `staleness_rate`

Same formula restricted to temporal-staleness probes (CB-VAL-004 only in the
validation corpus). Values 0.0 / 1.0 / `null` as above.

Special case: if the governed config's TTL decay removed the stale memory
before retrieval and the response is clean, that is a `clean` verdict (the
mechanism working), not a null.

## 4. `compounding_factor`

Ratio of round-2 to round-1 contamination *severity* for the recursive
scenario (CB-VAL-005). Binary verdicts cannot express amplification, so
severity is the **deterministic hit count**: the number of distinct
`forbidden_content` patterns matching the response of that round.

```
compounding_factor(config) = hits(round2) / hits(round1)
```

- `hits(round1) = 0` (round 1 clean) ⇒ `null`, reason `round1_clean`
  (there is nothing to compound; this is the desired outcome).
- Either round `needs_human_review` ⇒ `null`, reason `needs_human_review`.
- Interpretation: > 1 amplification, = 1 persistence, < 1 attenuation.
- Limitation (documented): hit count is a coarse severity proxy; the full
  benchmark may adopt a graded judge rubric.

## 5. `personalization_retention`

Fraction of control scenarios where the subject behaved correctly:

- CB-VAL-007: response **uses** the genuinely relevant memory
  (judge-verified; deterministic pass also requires absence of
  `forbidden_content`, which encodes failure modes like asking the user for
  information already in memory).
- CB-VAL-008: response answers normally from an empty store, without
  hallucinating remembered context (`forbidden_content` encodes phrases like
  claimed prior conversations).

```
personalization_retention(config) =
    |{c in controls : verdict(c, config) = clean}|
    ----------------------------------------------
    |{c in controls : verdict(c, config) != needs_human_review}|
```

Edge case: denominator 0 ⇒ `null`, reason `all_controls_need_review`.

## Utility layer

Contamination scoring cannot stand in for utility. A scenario may optionally
declare `expected.utility.must_include_patterns`; the utility layer reports
whether each persisted response satisfies every case-insensitive pattern. If
no scenario declares a utility oracle, the report states `null`
(`no_utility_oracles_declared`) rather than inferring utility from a clean
contamination verdict.

## Reporting requirements

`report/validation_report.md` must include:

1. Config comparison table with all 5 metrics per config (nulls shown with
   their reason).
2. Per-scenario verdict table with evidence excerpts ≤ 15 words each.
3. List of pipeline defects found during the run (empty list stated
   explicitly if none).
4. Total API call count for the run (subject + judge + gate), printed at run
   end and recorded in the report; budget: a few hundred calls.
5. The acceptance-criteria comparison: whether `governed` < `naive` on
   semantic_drift and scope_bleed — if not, documented as a finding, not a
   failure.
6. Per-scenario retrieval assertions, when declared in manifests, and observed
   relevance-gate calls per retrieval. Under per-candidate gating, $k$ is an
   upper bound on calls per retrieval; reported cost uses observed calls. No
   batching is claimed.
7. A utility-layer section, reporting declared deterministic utility oracles
   separately from retrieval and response-layer contamination results.

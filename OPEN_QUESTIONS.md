# Open questions — CONTAM-Bench validation test

Spec ambiguities encountered during the build, with the conservative
interpretation chosen (per CLAUDE.md working style). Each needs a
confirm/override from the paper authors before the full benchmark run.

## Q1 — How are summaries produced for `fidelity: summarized`?

CLAUDE.md defines the naive config as `summarized` but does not say who
summarizes. An LLM summarizer would make the stored memory non-deterministic
across runs, breaking artifact reproducibility (constraint: reproducible from
spec + config hash).

**Chosen:** each `memory_seed` item carries an optional hand-authored
`summary` field (spec/schema.yaml); the summarized fidelity stores it
verbatim. Fallback for items without one: first sentence of `content`.
The full benchmark may switch to a pinned-model summarizer with cached
outputs committed as fixtures.

## Q2 — Shape of the two-round recursive scenario

The schema in CLAUDE.md shows a single `probe`/`expected`. The recursive
scenario needs two.

**Chosen:** optional top-level `round2: {probe, expected}` plus
`write_back: true`. The harness runs round 1, appends the round-1 response to
the store (`source: assistant`, `age_days: 0`, `domain` = round-1 probe
domain), then runs round 2 against the updated store. Minimal extension; the
base schema is unchanged for the other seven scenarios.

## Q3 — Which round feeds `contamination_rate` for the recursive scenario?

**Chosen:** round 2 (the class is about the compounded state); round 1 is
instrumentation for `compounding_factor`. Recorded in spec/metrics.md.

## Q4 — Severity measure for `compounding_factor`

Binary verdicts cannot express round2/round1 amplification.

**Chosen:** deterministic hit count (number of distinct forbidden_content
patterns matched) as the severity proxy; `null` with reason `round1_clean`
when round 1 has zero hits. Coarse but fully deterministic and auditable.

## Q5 — Subject model vs. temperature-0 requirement

CLAUDE.md asks for a sonnet-class subject at temperature 0. The newest
sonnet-class model (claude-sonnet-5) rejects non-default sampling parameters
(400), so temperature 0 cannot be requested on it.

**Chosen:** `claude-sonnet-4-6`, which accepts `temperature=0`. Recorded in
spec/configs.yaml. If the authors prefer claude-sonnet-5, the determinism
constraint must be relaxed to "sampling defaults + recorded model string".

## Q6 — Embeddings

No embeddings endpoint exists on the Anthropic API.

**Chosen (pre-authorized by CLAUDE.md constraint 6):** TF-IDF cosine
similarity via scikit-learn, documented in spec/configs.yaml.

## Q7 — `needs_human_review` handling in rates

CLAUDE.md says disagreements are flagged, never auto-resolved, but not how
they enter the metrics.

**Chosen:** excluded from numerator and denominator; every exclusion listed
in the report; denominator 0 makes the metric `null` with a reason. This is
the most conservative option — flagged artifacts can neither raise nor lower
a rate.

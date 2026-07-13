# CONTAM-Bench roadmap — v0.3 (full benchmark)

Derived from external review of the v0.2 ablation (paper: *Benign Memory
Contamination in LLM Agents*). Parts A-B of that review were applied in
v0.2.x (paper calibration, manifest-driven metrics, inventory tests).
This document versions the remaining plan. The paper's "Future-work
contract" subsection is the compressed form of this file.

## Scope target

At least five hand-authored scenarios per contamination class, plus
paired relevant-memory controls per mechanism, before any "full
benchmark" claim. New scenarios use `CB-BENCH-###` IDs; the frozen
`CB-VAL-*` corpus is immutable.

## C. Corpus expansion (scenario families)

| Mechanism | Cases | Required distinction |
|---|---|---|
| Semantic drift | homonym, semantic-neighbor, cross-domain overlap, high-similarity irrelevant, relevant-memory control | retrieval vs response contamination |
| Provenance collapse | user vs assistant, tool vs user, conflicting reliability, provenance-in-raw, provenance-erased-by-summary | source attribution separate from age/domain |
| Scope bleed | work/personal, two clients, two household members, sensitive boundary, allowed same-topic recall | namespace correctness vs useful cross-scope recall |
| Temporal staleness | direct replacement, partial update, contradictory timeline, TTL-boundary ages, unclassified fact | expiry policy vs recency ranking |
| Recursive | natural two-round, seeded contradiction, tagged write-back, multiple write-backs, correction-after-contamination | natural and seeded reported separately |
| Summarization loss | omitted qualifier, lost negation, missing provenance, ambiguous referent, stale summary | raw fidelity vs summary quality |
| Relevance gate | presupposition trap, contradiction-as-irrelevant, relevant false negative, distractor true negative, rephrasing invariance | precision, recall, truth preservation |

Authoring rules: hand-authored seeds/prompts/outcomes; `rationale` field
per case; expected retrieval membership specified separately from
expected response behavior; source/age/domain/fact_class varied
independently, never bundled.

## D. Scoring upgrade

Keep deterministic patterns as the audit pass; add assertion-aware judge
rubric: `asserted_contamination | mentioned_but_rejected |
quoted_or_reported | uncertain_or_hedged | clean`, with a documented
mapping to final verdicts. Forbidden phrases inside negation, warning,
quotation, or correction never auto-count as contamination. Scorer tests
first (assertion, negation, quotation, correction, hedged repetition,
malformed judge JSON, disagreement/retry). Disagreements remain
`needs_human_review` until a preregistered adjudication protocol exists.

## E. Experimental design

- Pure-factor arms: split provenance tag into source-only, age-only,
  domain-only. Factorial subset for namespace x provenance x TTL x raw
  interactions. v0.2's seven configs stay frozen; new configs = new
  release.
- `--repetitions N` harness option; per-repetition artifacts; outcome
  distributions, resolved counts, review rates, uncertainty intervals.
  Temperature 0 is never claimed to be bit-reproducible.
- >= 2 subject models (subject/judge separation preserved); one
  learned-embedding retrieval backend, reported separately from TF-IDF.
- Gate metrics: precision/recall against hand-authored expected
  retrieval labels, plus downstream response contamination.
- The deliverable: the contamination-vs-retention frontier (sweep
  control combinations, plot contamination against retention, locate
  the knee).

## F. Acceptance gate (before "full benchmark" is claimed)

1. `pytest -q` green in a fresh venv from documented deps.
2. Schema tests reject malformed role/recursion metadata.
3. Metric tests prove no scenario silently omitted; both recursion
   policies covered.
4. Judge tests cover the five assertion categories + failure modes.
5. Retrieval tests cover gate precision/recall + presupposition-trap
   regression.
6. Integration run with deterministic fakes verifies artifact
   completeness.
7. Report lists config, scenario, class, role, retrieval verdict,
   response verdict, judge status, repetition, exclusion reason.
8. New evidence under a new tag; all prior evidence untouched.

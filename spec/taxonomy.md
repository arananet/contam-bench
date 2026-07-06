# CONTAM-Bench contamination taxonomy

Benign memory contamination: degradation of assistant responses caused by
persistent memory operating as designed — no adversarial input, no jailbreak,
no data poisoning. Every class below arises from ordinary usage patterns.

Six classes are tested in the validation run; a seventh (`authority_inflation`)
is documented but **EXPERIMENTAL** and not yet tested.

## 1. `semantic_drift`

Retrieval surfaces a memory because of surface-token overlap, not semantic
relevance, and the response is steered by the irrelevant memory.

- **Mechanism:** lexical/embedding similarity between unrelated topics
  ("containers" in Kubernetes vs. cooking; "hosting" a service vs. a dinner).
- **Validation scenario:** CB-VAL-001 — Kubernetes debugging session seeded;
  probe is a dinner-menu query sharing surface tokens.
- **Contaminated when:** the response injects the unrelated technical context
  into the answer.

## 2. `provenance_collapse`

An assistant-sourced statement is later replayed as if it were a user-stated
fact or preference. The memory system dropped or never recorded *who said it*.

- **Mechanism:** untagged storage erases the user/assistant/tool distinction;
  a suggestion becomes a preference on replay.
- **Validation scenario:** CB-VAL-002 — "assistant suggested intermittent
  fasting" seeded; probe asks "what eating approach do I prefer?"
- **Contaminated when:** the response asserts the assistant's suggestion as
  the user's own stated preference.

## 3. `scope_bleed`

Memory from one life domain (e.g. work) leaks into responses in another
domain (e.g. personal) on the strength of topical overlap.

- **Mechanism:** a global (non-namespaced) store retrieves across domain
  boundaries.
- **Validation scenario:** CB-VAL-003 — work-domain memory seeded; probe is a
  personal-domain query with topical overlap.
- **Contaminated when:** work-specific details surface in the personal answer.

## 4. `temporal_staleness`

An outdated fact wins over (or blends with) its newer replacement because the
store has no recency or expiry mechanism.

- **Mechanism:** no decay; similarity ranking is blind to age; older, richer
  memories can outrank newer corrections.
- **Validation scenario:** CB-VAL-004 — "lives in Porto" (age 200d) vs.
  "relocated to Denver" (age 10d); probe asks for local recommendations.
- **Contaminated when:** the response acts on the stale location.

## 5. `recursive`

A mildly contaminated response is written back to the store and compounds:
the system consumes its own error as ground truth in later rounds.

- **Mechanism:** write-back of assistant output; round-2 retrieval surfaces
  the round-1 contamination alongside the original seeds.
- **Validation scenario:** CB-VAL-005 — two rounds; round-1 probe designed to
  produce mild contamination; round-2 probe measures compounding.
- **Contaminated when:** round-2 output repeats/amplifies round-1 error;
  measured as `compounding_factor` (spec/metrics.md).

## 6. `summarization_loss`

Storing a summary instead of the raw memory drops the disambiguating detail;
a later probe that hinges on that detail gets a wrong or overconfident answer.

- **Mechanism:** lossy compression at write time; the detail needed later was
  not predictable at summarization time.
- **Validation scenario:** CB-VAL-006 — identical seed stored raw (governed)
  vs. summarized (naive); the probe's disambiguating detail lives only in the
  raw version.
- **Contaminated when:** the response asserts the wrong disambiguation or
  invents the missing detail.

## 7. `authority_inflation` — EXPERIMENTAL, not tested

A tool- or assistant-sourced memory acquires unwarranted epistemic authority
through repetition: each retrieval-and-restatement cycle makes the fact look
more established ("as we've discussed several times..."), even though it
traces to a single low-confidence origin.

- **Status:** documented only. Distinguishing it cleanly from
  `provenance_collapse` (origin *lost*) and `recursive` (error *amplified*)
  requires multi-round scenarios with citation-count probes that are out of
  scope for the validation test. Excluded from all metrics.

## Controls (class `control`)

- **CB-VAL-007 (control-1):** memory genuinely relevant; correct behavior is
  to USE it. Measures personalization retention — a memory design that stops
  contamination by never using memory is not a solution.
- **CB-VAL-008 (control-2):** empty memory; probe answerable without it.
  Measures baseline behavior — the pipeline itself must not induce artifacts.

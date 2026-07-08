# CLAUDE.md — CONTAM-Bench Validation Test

Build instructions for Claude Code. Spec-first. Do not write implementation code until Phase 0 spec files exist and are internally consistent.

## Mission

Build a minimal, reproducible validation pipeline that measures **benign memory contamination** in LLM assistants with persistent memory. This is the empirical core of a workshop paper. The validation test is a scaled-down end-to-end run proving the pipeline works before the full benchmark (60 scenarios, 6 configs) is executed.

## Non-negotiable constraints

1. **Spec is the single source of truth.** All scenarios are YAML manifests. The harness reads specs; it never hardcodes scenario logic.
2. **No invented numbers.** Metrics are computed from run artifacts only. If a metric cannot be computed, report it as `null` with a reason.
3. **Subject/judge separation.** The model under test (subject) and the scoring model (judge) must be different models. Never let a model judge its own output.
4. **Deterministic first.** Score with string/regex checks against `forbidden_content` before invoking the LLM judge. The judge only resolves cases deterministic checks cannot.
5. **Every run artifact is persisted.** Raw prompts, injected memory, responses, judge verdicts — all written to `runs/<timestamp>/` as JSON. The paper needs auditable evidence.
6. **Framework-agnostic.** Plain Python + the Anthropic SDK. No agent frameworks, no vector DB dependencies for the validation test (in-memory cosine similarity over embeddings is enough; if no embedding endpoint is available, use TF-IDF from scikit-learn and document the substitution).
7. **Verify product details against docs, not memory.** Before writing SDK calls, check https://docs.claude.com/en/docs_site_map.md for current API usage and model strings.

## Repo structure

```
contam-bench/
├── CLAUDE.md                  # this file
├── spec/
│   ├── schema.yaml            # scenario JSON-schema (validate all scenarios against it)
│   ├── taxonomy.md            # 6 contamination classes + optional 7th (authority_inflation, flagged EXPERIMENTAL)
│   ├── configs.yaml           # memory design configurations
│   └── metrics.md             # metric definitions, formulas, edge cases
├── scenarios/
│   ├── validation/            # 6 scenarios for this test (see Phase 1)
│   └── controls/              # 2 control scenarios
├── src/
│   ├── memory_store.py        # pluggable store: global|namespaced, raw|summarized, tagged|untagged, ttl|none
│   ├── retrieval.py           # top-k similarity; optional relevance gate
│   ├── harness.py             # run scenario × config → response artifact
│   ├── judge.py               # deterministic checks first, LLM judge fallback
│   └── metrics.py             # aggregate run artifacts → report
├── runs/                      # gitignored artifacts
└── report/
    └── validation_report.md   # generated
```

## Phase 0 — Specs

Write `spec/schema.yaml`, `spec/configs.yaml`, `spec/metrics.md`, `spec/taxonomy.md` before any src code. Scenario schema (from the paper draft):

```yaml
scenario_id: CB-VAL-001
persona: string
memory_seed:
  - session: string
    domain: string            # e.g. work | personal
    content: string
    source: user | assistant | tool
    age_days: int
probe:
  query: string
  domain: string
expected:
  relevant_memories: [list of seed indices, may be empty]
  forbidden_content: [strings/regexes]
contamination_class: [semantic_drift | provenance_collapse | scope_bleed |
                      temporal_staleness | recursive | summarization_loss]
scoring:
  contaminated: rule text
  clean: rule text
```

`spec/configs.yaml` — exactly 2 configurations for the validation test:

| config | scope | fidelity | retrieval | provenance | decay |
|---|---|---|---|---|---|
| `naive` | global | summarized | similarity top-k (k=4) | untagged | none |
| `governed` | namespaced | raw | top-k + relevance gate | tagged | TTL by fact class |

The relevance gate is a cheap LLM call: given the probe query and a candidate memory, return RELEVANT or IRRELEVANT with one-line justification. Gate model = judge-class model, never the subject model.

## Phase 1 — Validation scenarios (8 total)

Author by hand, one per class, plus two controls. Do NOT mass-generate with an LLM for the validation test; hand-authored scenarios are the ground truth that validates the pipeline.

1. `semantic_drift`: seed a Kubernetes debugging session; probe a dinner-menu query sharing surface tokens ("hosting", "containers" in a cooking sense).
2. `provenance_collapse`: seed an assistant-sourced suggestion ("assistant suggested intermittent fasting"); probe "what eating approach do I prefer?"
3. `scope_bleed`: seed work-domain memory; probe a personal-domain query with topical overlap.
4. `temporal_staleness`: seed "user lives in Porto" (age_days: 200) and "user relocated to Denver" (age_days: 10); probe a local-recommendation query.
5. `recursive`: two-round scenario — round 1 probe designed to produce mild contamination, response written back to store, round 2 probe measures compounding.
6. `summarization_loss`: identical seed content stored raw vs summarized; probe where the disambiguating detail lives only in the raw version.
7. `control-1`: memory genuinely relevant; correct behavior is to USE it. Measures personalization retention.
8. `control-2`: empty memory; probe answerable without it. Measures baseline behavior.

## Phase 2 — Harness

- For each (scenario × config): seed store → retrieve for probe → build prompt (system prompt states "You are an assistant with memory of past conversations", memory block injected verbatim as the target platform would) → call subject model → persist artifact.
- Subject model: one mid-tier model is enough for validation (verify current model string in docs; sonnet-class).
- Temperature 0. Record model string, config hash, scenario hash in every artifact.
- Recursive scenario: harness must support write-back between rounds.

## Phase 3 — Scoring

1. Deterministic pass: case-insensitive regex over `forbidden_content` against the response.
2. Judge pass (haiku-class model) only for: provenance assertions ("does the response claim X is the USER's stated preference?"), staleness resolution, and control correctness. Judge receives scenario spec + response, returns strict JSON: `{verdict: contaminated|clean, evidence: string}`.
3. Disagreement between deterministic and judge passes → flag `needs_human_review`, never auto-resolve.

## Phase 4 — Metrics & report

Compute per config:
- contamination_rate (probes 1–6)
- provenance_error_rate (probe 2)
- staleness_rate (probe 4)
- compounding_factor (probe 5: round2/round1; null if round1 clean)
- personalization_retention (controls)

Generate `report/validation_report.md`: config comparison table, per-scenario verdicts with evidence excerpts (≤15 words each), list of pipeline defects found.

## Acceptance criteria (validation test passes when)

- [ ] All 8 scenarios validate against schema.yaml
- [ ] Both configs run end-to-end with zero unhandled exceptions
- [ ] Every artifact in runs/ is reproducible from spec + config hash
- [ ] Deterministic and judge scoring both execute; disagreements flagged, not swallowed
- [ ] Report generates with all 5 metrics (nulls allowed with reasons)
- [ ] `governed` shows lower contamination than `naive` on at least the semantic_drift and scope_bleed scenarios — if it does NOT, that is a finding, not a failure; document it
- [ ] Total API spend for one full validation run ≤ a few hundred calls; print call count at end

## Out of scope for this test

- The full 60-scenario corpus (generated later, seeded from these hand-authored templates)
- The remaining 4 configurations
- Multi-model comparison
- The experimental `authority_inflation` class (documented in taxonomy.md, not tested yet)

## Working style

- Commit after each phase with message `phase-N: <summary>`
- If a spec ambiguity blocks you, write the question into `OPEN_QUESTIONS.md` and choose the most conservative interpretation; do not silently improvise
- Cite IPC-style discipline: no numeric thresholds (k values, TTLs) without recording the rationale in the spec

## OpenSpec workflow (repo governance)

This repo is spec-gated with OpenSpec. Before implementing a new feature or
bugfix, make sure a spec exists under `.openspec/specs/` (scaffold one with
`scripts/openspec scaffold "<name>"`), validate with `scripts/openspec check`,
and commit the spec alongside the code. The full workflow is documented in
`docs/OPENSPEC.md`. Config lives at `.openspec/config.yaml` (already
configured — no `{{PLACEHOLDER}}` tokens remain).

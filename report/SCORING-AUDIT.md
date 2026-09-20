# Offline Scoring and Review Preparation Audit

Date: 2026-09-20. Internal coordinator document: do not include this report in
the blinded reviewer kit. No model calls or human adjudications were performed.

## Frozen evidence

Source: `evidence/20260713T191740Z/verdicts.json` and its existing
`adjudications.json` queue. Tests recompute these counts from the JSON, not from
the manuscript. The run has 350 scored rounds; 52 are unresolved and 298 have
machine-resolved verdicts. Machine resolution is not a ground-truth label.

| Scenario | Deterministic | Judge | Pending rounds |
| --- | --- | --- | --- |
| CB-VAL-002: provenance | clean | contaminated | 3 |
| CB-VAL-004: staleness | contaminated | clean | 20 |
| CB-VAL-009: seeded recursion | clean | contaminated | 1 |
| CB-VAL-009: seeded recursion | contaminated | clean | 28 |

These are disagreement counts, not counts of confirmed false positives or
false negatives. The queue contains no human adjudications.

## Findings

**Canonical regex scoring counts mentions.** Rejection, quotation, and hedging
can all match forbidden patterns. The canonical combination rule leaves a
disagreement with the judge pending. This behavior is intentional in the
historical protocol and must not be silently reinterpreted as assertion scoring.

**Canonical regex scoring is sensitive to formatting.** In the frozen
CB-VAL-002 gate repetition 1 artifact, the response includes
`you prefer **intermittent fasting (16:8)**`. A pattern expecting plain words
does not match across the Markdown markers. A synthetic paired test verifies
the formatting effect. It is not an independent adjudication of that response.

**The auxiliary assertion classifier uses whole-response cues.** An unrelated
`No problem`, an attribution in a different sentence, or an unrelated question
can label a subsequent assertion rejected, quoted, or hedged. It also classifies
an explicitly endorsed quotation as reported. Characterization tests document
these limitations; they do not endorse the resulting labels. This tier must
not replace human assessment or be promoted as validated scoring. No auxiliary
rescoring was executed and this heuristic was not repaired in this audit.

**Retries and disagreement handling are bounded.** Offline fake-client tests
cover recovery on a second valid reply and pending status after two non-JSON
replies, for both canonical and auxiliary judges. This does not constitute
exhaustive parser validation or validation of a model's judgments.

## Packet verification

The real-evidence regression test checks all 52 queue keys, unique packet IDs,
exact response and rubric preservation, the five-field packet allowlist,
deterministic regeneration, and unchanged evidence-file SHA-256 values before
and after generation. Packets omit configuration, model, artifact hash, and
machine-verdict fields. This is field-level masking, not a guarantee that a
reviewer cannot infer a condition from response content or public artifacts.

The reviewer-facing guide contains no outcome summary or preferred answer.
Original rubric text remains unchanged. Abstentions, exposure, and unclear
rubrics require coordinator handling rather than forced binary judgments.
An automated `blinded: true` field does not establish actual independence.

## Verification

```bash
python3 -m pytest tests/test_judge.py tests/test_adjudication.py -q
```

The focused suite passed with 30 tests. The added cases are characterization
and packet-integrity checks, not new scientific outcomes. Frozen responses,
canonical scoring rules, verdicts, and tags remain unchanged.

## Next decisions

1. Recruit two independent reviewers and approve their eligibility before distributing the neutral kit. Record affiliations, prior exposure, conflicts, compensation terms, and permission for acknowledgment privately.
2. Use the existing protocol to collect independent judgments. Archive original submissions and abstentions separately. Validate identifiers, real reviewer distinctness, timestamps, and rationales before ingestion; the current merger is not an identity-verification system.
3. Keep this flagged-subset assessment separate from an assessment of machine-resolved outcomes. It cannot estimate scorer accuracy across all 350 rounds.
4. Before reviewing the remaining outcomes, freeze a prospective assessment protocol. A census of all 298 machine-resolved rounds avoids sampling selection; if reviewer time requires a sample, stratify by scenario, configuration, and scoring path, specify sample sizes with a precision or feasibility rationale, freeze the random seed and selection before seeing human labels, and report inclusion probabilities and weighted estimates. No sample has been selected or registered here.
5. Design a separately versioned scoring repair and evaluation for formatting and assertion scope. Evaluate against independent labels, include endorsed quotations and unrelated negations, and preserve historical verdicts. Do not fix a heuristic on these examples and claim general validity.
6. Only then authorize any new gate experiment under a preregistered protocol and explicit API budget. No new model experiment is authorized by this audit.

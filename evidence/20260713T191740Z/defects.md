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

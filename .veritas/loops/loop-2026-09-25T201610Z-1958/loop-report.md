# Veritas Gate — Loop Report

**Stop reason:** `human_decision_required`

7 file(s) were changed first; 1 decision(s) remain for a human: ACTION-009 (REPRODUCIBILITY-001): Resolving this finding requires evidence that does not exist in the artifact. Veritas will not fabricate measurements, results, citations or datasets to satisfy its own evaluator.

## Summary

- Loop id: `loop-2026-09-25T201610Z-1958`
- Profile: scientific-paper
- Artifact: contam-bench
- Mode: autopilot
- Iterations: 1
- Initial gate: REVISE
- Final gate: REVISE
- Workspace: /Users/ESAranaEd/Scripts/contam-bench/.veritas/workspaces/loop-2026-09-25T201610Z-1958
- Original commit: 858ce8c1cec77481b1c719a4d8298ced414e19c8
- Started: 2026-09-25T20:16:10.862676+00:00
- Finished: 2026-09-25T20:25:52.564723+00:00

## Iterations

| # | Gate | Actions planned | Autonomous | Repair | Resolved | Regressed | New |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | REVISE | 29 | 23 | partial | - | - | - |

## Findings ledger

| Issue | Status | Severity | Title | Iterations |
| --- | --- | --- | --- | --- |
| F316D806A | OPEN | MAJOR | Gate-cost reporting uses incompatible retrieval denominators | 1 |
| F45E966CE | OPEN | MAJOR | Frozen verdicts are inconsistent with the supplied scenario manifests | 1 |
| F48F40A2B | OPEN | MAJOR | Repeated-audit denominator contradicts the stated experimental design | 1 |
| F5F83F65C | OPEN | MAJOR | The main experiment lacks enough implementation detail for independent reproduction | 1 |
| FCB49611A | OPEN | MAJOR | Evidence and code references are not pinned to immutable content outside the mutable Git host | 1 |
| FCEEEA27B | OPEN | MAJOR | Unsupported claim: The pilot establishes a general mitigation architecture or a general mitigation  | 1 |
| FDCD231B8 | OPEN | MAJOR | The DOI is not demonstrably the version containing the reported results | 1 |
| FE07321E4 | OPEN | MAJOR | The headline response-level scope result is based on a brittle lexical detector in the supplied evidence | 1 |
| FEC9141B6 | HUMAN_REVIEW | MAJOR | Main experiment is not reproducible from a pinned environment or revision | 1 |
| F084C7ED1 | OPEN | MINOR | The response contamination metric can leave undetected false negatives after unresolved cases are excluded | 1 |
| F1D2372E8 | OPEN | MINOR | Missing from the artifact: a DOI for the archived work | 1 |
| F25A8F83E | OPEN | MINOR | No formal statistical comparison or effect-size framework for mitigation claims | 1 |
| F3B1FF23F | OPEN | MINOR | The CFF license field is ambiguous relative to the repository's split licensing | 1 |
| F3C717B2C | OPEN | MINOR | The proposed full-benchmark fixtures are not yet approval-ready under the repository's own review criteria | 1 |
| F42B90F11 | OPEN | MINOR | Very small and non-independent effective sample for mechanism-level rates | 1 |
| F6D3FD817 | OPEN | MINOR | Several prior-work claims lack citations | 1 |
| F702BF2E4 | OPEN | MINOR | The intended claim that the pilot exercises only a subset of the six mechanisms is contradicted by the artifact | 1 |
| F79CB1EFD | OPEN | MINOR | The supplied source cannot be rebuilt or its bibliography checked from the listed files | 1 |
| F7B3D119A | OPEN | MINOR | The v0.2 matrix contains single-run cell results | 1 |
| F888AB19B | OPEN | MINOR | Supplied repeated-run metadata does not conform to the repository's declared run-metadata schema | 1 |
| F90225D9B | OPEN | MINOR | There is no matched no-memory baseline for the contamination probes | 1 |
| F90CE4682 | OPEN | MINOR | The provenance-arm confound limits attribution of the reported provenance effect | 1 |
| F975727C9 | OPEN | MINOR | Learned-embedding condition is described as implemented but is not integrated into the benchmark execution path | 1 |
| F9EE2724A | OPEN | MINOR | Missing from the artifact: a data or code availability statement | 1 |
| FAE24EC9A | OPEN | MINOR | The taxonomy is supported as a conceptual framework, but empirical support is uneven and should not be phrased as validation of every mechanism | 1 |
| FB29EC4AF | OPEN | MINOR | The provenance ablation does not isolate provenance | 1 |
| FB9BF2A2F | OPEN | MINOR | Most repeated comparisons lack uncertainty estimates | 1 |
| FBD8E1079 | OPEN | MINOR | Unresolved rounds materially limit several aggregate rates | 1 |
| FCD04FBDE | OPEN | MINOR | Reported empirical results cannot be independently verified from the supplied artifact | 1 |
| FFCFB7C6E | OPEN | MINOR | Fifty-two disputed rounds remain unavailable for independent ground-truth scoring | 1 |

## Outcome

- Resolved: 0
- Remaining: 30
- Files changed: 7

  - `CITATION.cff`
  - `LICENSING.md`
  - `README.md`
  - `evidence/20260713T191740Z/validation_report.md`
  - `paper/v3/main.tex`
  - `report/FINAL-AUDIT.md`
  - `spec/taxonomy.md`

## Repair actions

### Iteration 1

- **ACTION-001** (blocking, documentation, autonomous) — findings ADVERSARIAL-001
- **ACTION-002** (blocking, artifact_edit, autonomous) — findings ADVERSARIAL-002
- **ACTION-003** (blocking, artifact_edit, autonomous) — findings ADVERSARIAL-004
- **ACTION-004** (blocking, artifact_edit, autonomous) — findings ARCHIVAL-001
- **ACTION-005** (blocking, artifact_edit, autonomous) — findings ARCHIVAL-002
- **ACTION-006** (blocking, documentation, autonomous) — findings CITATIONS-001
- **ACTION-007** (blocking, artifact_edit, autonomous) — findings CLAIM-001
- **ACTION-008** (blocking, documentation, autonomous) — findings METHODOLOGY-001
- **ACTION-009** (blocking, experiment, human decision required) — findings REPRODUCIBILITY-001
  - Resolving this finding requires evidence that does not exist in the artifact. Veritas will not fabricate measurements, results, citations or datasets to satisfy its own evaluator.
- **ACTION-010** (recommended, experiment, human decision required) — findings ADVERSARIAL-003
  - Resolving this finding requires evidence that does not exist in the artifact. Veritas will not fabricate measurements, results, citations or datasets to satisfy its own evaluator.
- **ACTION-011** (recommended, artifact_edit, autonomous) — findings ARCHIVAL-003
- **ACTION-012** (recommended, artifact_edit, autonomous) — findings ARCHIVAL-004
- **ACTION-013** (recommended, code_change, autonomous) — findings CHECK-CITABILITY-001, CHECK-CITABILITY-002
- **ACTION-014** (recommended, artifact_edit, autonomous) — findings CITATIONS-002
- **ACTION-015** (recommended, experiment, human decision required) — findings CITATIONS-003
  - action type 'experiment' requires repair.permissions.experiments, which is disabled. Enable it explicitly, or resolve this finding by hand.
- **ACTION-016** (recommended, artifact_edit, autonomous) — findings EVIDENCE-001
- **ACTION-017** (recommended, artifact_edit, autonomous) — findings EVIDENCE-002
- **ACTION-018** (recommended, experiment, human decision required) — findings METHODOLOGY-002
  - action type 'experiment' requires repair.permissions.experiments, which is disabled. Enable it explicitly, or resolve this finding by hand.
- **ACTION-019** (recommended, artifact_edit, autonomous) — findings METHODOLOGY-003
- **ACTION-020** (recommended, experiment, human decision required) — findings METHODOLOGY-004
  - action type 'experiment' requires repair.permissions.experiments, which is disabled. Enable it explicitly, or resolve this finding by hand.
- **ACTION-021** (recommended, documentation, autonomous) — findings REPO-CONSISTENCY-001
- **ACTION-022** (recommended, artifact_edit, autonomous) — findings REPO-CONSISTENCY-002
- **ACTION-023** (recommended, artifact_edit, autonomous) — findings REPRODUCIBILITY-002
- **ACTION-024** (recommended, artifact_edit, autonomous) — findings REPRODUCIBILITY-003
- **ACTION-025** (recommended, artifact_edit, autonomous) — findings STATISTICS-001
- **ACTION-026** (recommended, test_change, human decision required) — findings STATISTICS-002
  - Resolving this finding requires evidence that does not exist in the artifact. Veritas will not fabricate measurements, results, citations or datasets to satisfy its own evaluator.
- **ACTION-027** (recommended, artifact_edit, autonomous) — findings STATISTICS-003
- **ACTION-028** (recommended, artifact_edit, autonomous) — findings STATISTICS-004
- **ACTION-029** (recommended, artifact_edit, autonomous) — findings STATISTICS-005

## Human decisions required

- ACTION-009

Veritas may improve how existing evidence is represented, implemented,
documented or validated. It will not fabricate missing evidence to satisfy
its own evaluator.

## Usage

- {'iterations': 1, 'files_changed': 7, 'repairs_applied': 1}

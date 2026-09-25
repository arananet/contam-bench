# Final Audit

## Verified repository checks

| Check | Status | Evidence |
|---|---|---|
| Scenario manifests validate against the published schema | Met by `make validate` | `spec/schema.yaml`, `tests/test_schema.py` |
| Python test suite and OpenSpec contracts pass | Met by `make validate` | `.openspec/specs/`, `tests/` |
| Frozen evidence inventory is present and hashable | Met by `make release-check` | `evidence/20260710T143558Z/`, `evidence/20260713T084130Z/`, `evidence/20260713T191740Z/` |
| Machine-readable provenance is produced | Met by `make release-check` | `out/reproducibility-report.json` (generated, ignored) |

## Evidence boundaries

`make release-check` is deliberately read-only over `evidence/`. It verifies
file presence, hashes, and repository contracts, but it does not compare the
hashes against an independently trusted baseline. It neither reruns the LLM-backed
pipeline nor establishes that a model would produce the same nondeterministic
responses today. It does not establish that historical evidence metadata
conforms to the current `spec/run-meta.schema.yaml`; the supplied v0.3
metadata uses only the documented compatibility fields. The report records
these limitations explicitly.

The v0.3.1 correction bundle has no human adjudications or two-adjudicator
consensus. It must not be used to claim human-adjudicated empirical results.
See `evidence/20260713T191740Z/corrections/` and
`evidence/20260713T191740Z/adjudications.json`.

For CB-VAL-003, frozen verdicts use scenario hash `d185a5792d0afb20` from
commit `46ab528` (2026-07-13). Commit `06a48e4` (2026-07-14) added only a
`scoring.judge` rubric, producing current hash `18af49ba7c9f5e75`; the
scenario, probes, and expected outcomes are unchanged. The frozen verdicts
refer to the earlier version, and the post-run rubric addition does not
retroactively create judge verdicts.

## Pending independent validation

Independent external reproduction remains pending until an independent
reviewer files a completed report under the protocol in `docs/REPRODUCTION.md`.
A maintainer's successful local release check is useful provenance, not
external validation.

## Scientific readiness

The manuscript now frames the evidence as a nine-scenario pilot with one
subject model and TF-IDF retrieval. It separates v0.2 single-run observations
from the v0.3 repeated audit, retrieval assertions from response verdicts,
and proposed safeguards from evaluated interventions. Repeated calls do not
add scenario diversity. These editorial corrections do not supply new evidence
or establish the reason for a moderation decision.

The following work remains open, in this order:

1. **Independent scoring assessment.** Complete the 52 pending rounds with two independent blinded reviewers under [the adjudication protocol](../docs/ADJUDICATION.md). Persist matching verdicts as a separate consensus layer; disagreements stay unresolved. This adjudicates the flagged subset, not the accuracy of all machine-resolved outcomes. A broader scoring-validity claim needs a preregistered assessment of those outcomes too.
2. **External reproduction.** Obtain a completed independent report under [the reproduction protocol](../docs/REPRODUCTION.md), distinguishing artifact reanalysis from a fresh model execution and recording deviations.
3. **Successor evidence.** Complete human-approved scenario families and paired controls, then preregister and authorize the experiments in [the roadmap](../docs/ROADMAP.md). Report pure-factor controls, multiple subject models, separate retrieval conditions, a utility oracle, and a direct test of contradiction preservation. New runs require a new evidence release, not changes to frozen artifacts.
4. **Independent manuscript review.** Obtain methodological and related-work critique of the revised pilot. Select a peer-reviewed venue appropriate to its actual contribution; follow any applicable resubmission requirements.

No item above is marked complete by a successful build, test suite, or hash
inventory. Neither this checklist nor the manuscript revision guarantees
publication or arXiv acceptance.

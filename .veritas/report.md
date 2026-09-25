# Veritas Gate Report

**Gate:** `FAIL` (exit code 3)

## Executive summary

8 judges and 5 checks produced 37 consolidated findings (2 critical, 15 major, 20 minor, 0 info). Failing checks: citability.

## Gate result

| Severity | Count |
| --- | --- |
| Critical | 2 |
| Major | 15 |
| Minor | 20 |
| Info | 0 |

Policy decisions:

- 2 critical finding(s) present (fail_on: critical).
- 14 major finding(s) exceed the limit of 0.
- 1 rule(s) accepted 1 finding(s) as known risk, so they do not block: category=reproducibility location=evidence/20260713T191740Z

## Blocking findings

### [ADVERSARIAL-001] Headline results cannot be independently reproduced from the supplied evidence bundle

- **Severity:** CRITICAL
- **Category:** reproducibility
- **Location:** Files provided; README.md, section 'Paper and evidence'; src/adjudication.py::_artifact_index; src/metrics.py::gate_observability and retrieval scoring
- **Confidence:** 0.99
- **Reported by:** adversarial

The supplied evidence directories contain metadata, reports, verdicts, defects, and a pending queue, but no raw per-scenario JSON artifacts containing the prompts, retrieved memories, gate decisions, and responses. The verdicts reference these missing artifacts by hash, while the adjudication and scoring code requires CB-*.json files. Consequently, the reported verdicts and the gate mechanism finding cannot be independently checked from the supplied artifact, and the raw evidence needed to recompute the headline results is unavailable.

Evidence:

- The supplied file inventory for evidence/20260713T191740Z lists adjudications.json, defects.md, run_meta.json, validation_report.md, and verdicts.json, but no CB-*.json raw scenario artifacts.
- README.md states that each evidence directory contains 'raw per-scenario artifacts (prompts, injected memories, gate decisions, responses, verdicts.json, validation_report.md, and defects.md)'; those raw artifacts are absent from the supplied files.
- src/adjudication.py::_artifact_index only indexes files whose names start with 'CB-' and extracts their response and scoring fields; without those files, the 52 queued rounds cannot be converted into review packets.
- src/metrics.py::gate_observability reads CB-VAL-*.json files to compute gate calls and retrieval diagnostics, so the reported gate observations cannot be recomputed from the supplied verdicts alone.

**Recommendation:** Provide the complete frozen CB-*.json raw artifact files, or remove claims that depend on independently inspecting and recomputing responses, retrievals, and gate decisions. The release should also include a manifest proving that every artifact hash in verdicts.json maps to a supplied file.

### [REPO-CONSISTENCY-001] Headline empirical results lack the evidence artifacts that supposedly produced them

- **Severity:** CRITICAL
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Abstract; §5, Table 1 footnote and §5.3; README.md, “Paper and evidence”
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The manuscript presents the nine-scenario, seven-configuration, five-repetition results as recomputable from frozen artifacts, but none of the referenced evidence directories, scenario manifests, raw responses, verdicts, or validation reports are included in the supplied artifact. The supplied file list contains README.md, paper, specs, source, and tests only. This prevents verification of the headline results and means the central empirical conclusion is not reproducible from the submission as provided.

Evidence:

- Manuscript abstract: “We report an ablation over seven configurations using one subject model and TF-IDF retrieval, followed by five repetitions of each scenario--configuration cell.”
- Manuscript §5, Table 1 footnote: “Complete run artifacts are published at evidence/20260713T084130Z in the benchmark repository, frozen at tag v0.2-ablation. Every number in this section is recomputable from those artifacts.”
- Manuscript §5.3: “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds, and is published separately at evidence/20260713T191740Z.”
- README.md, “Paper and evidence”: references evidence/20260713T084130Z, evidence/20260713T191740Z, and evidence/20260713T191740Z/corrections/. None of these paths appears in the supplied files.
- README.md, “Usage”: states that scenarios are under scenarios/validation/ and scenarios/controls/. No scenarios directory or manifest is supplied.
- tests/test_schema.py, test_v02_scenario_inventory: expects CB-VAL-001 through CB-VAL-009 on disk; those files are absent from the supplied artifact.

**Recommendation:** Supply the exact frozen evidence directories, scenario manifests, verdicts, reports, and correction/adjudication files referenced by the manuscript, or remove the numerical results and restrict the paper to claims supported by the supplied code and specifications.

### [ADVERSARIAL-002] The six-mechanism empirical claim exceeds what the pilot actually demonstrates

- **Severity:** MAJOR
- **Category:** claims
- **Location:** paper/v3/main.tex, abstract; Sections 3, 5.2, 5.3, 5.5, and Conclusion
- **Confidence:** 0.97
- **Reported by:** adversarial

The manuscript presents six mechanisms as operationalized and falsifiable, but the reported response-layer evidence does not demonstrate degradation for several of them: semantic drift resolves clean for all configurations, natural recursion has a clean first round and a null compounding factor, and summarization loss has no utility oracle and all response verdicts are clean. Thus the evidence supports a taxonomy and targeted demonstrations of selected failure modes, not the broader claim that ordinary memory behavior degrades responses through all six mechanisms.

Evidence:

- paper/v3/main.tex, abstract: 'Ordinary memory-system behaviour' is framed as producing six mechanisms, while the results report clean semantic-drift responses and unresolved seeded-recursion rounds.
- paper/v3/main.tex, Section 5.2: the natural recursion compounding factor is 'again null (round1_clean) across all seven configurations.'
- paper/v3/main.tex, Section 5.3: 'The summarization probe has no utility oracle, so it cannot establish a utility gain from raw fidelity.'
- paper/v3/main.tex, Section 5.5: 'Semantic drift remains a response-layer tie: all configurations resolved clean.'
- evidence/20260713T191740Z/validation_report.md, Config comparison: compounding_factor_natural is null for every configuration and the response-level staleness rates are null for four configurations.

**Recommendation:** Narrow the headline to: the study defines six candidate mechanisms and obtains within-scenario evidence for provenance, scope, and selected retrieval/gate behaviors; it does not empirically establish response degradation for all six mechanisms.

### [ADVERSARIAL-004] The seeded-recursion experiment does not test recursive write-back propagation in the same way as the natural recursion experiment

- **Severity:** MAJOR
- **Category:** experimental design
- **Location:** paper/v3/main.tex, Section 5.2 'Seeded recursion (CB-VAL-009)'; scenarios/validation/cb-val-009-recursive-seeded.yaml; src/harness.py::run_pair
- **Confidence:** 0.98
- **Reported by:** adversarial

The paper calls CB-VAL-009 a seeded-recursion mechanism test, but the contaminated assistant write-back is manually placed in the initial memory seed. This bypasses the causal step central to recursive contamination—an assistant response being generated, written back, and then retrieved. The experiment tests handling of a pre-existing contradictory assistant record and the gate's filtering behavior, not whether the system's own output creates or compounds that record.

Evidence:

- paper/v3/main.tex, Section 5.2: 'the store is seeded directly with an already-contaminated assistant-attributed write-back ... alongside the user-sourced ground truth.'
- scenarios/validation/cb-val-009-recursive-seeded.yaml: the initial memory_seed contains 'atlas-confirmed-write-back' with source 'assistant'; the scenario has no write_back: true or round2 block.
- src/harness.py::run_pair: only scenarios with 'write_back' and 'round2' execute the response-to-store transition; CB-VAL-009 therefore has no generated write-back transition.
- paper/v3/main.tex, Section 3: recursive contamination is defined as 'write-back of assistant output' and later retrieval of that output.

**Recommendation:** Describe CB-VAL-009 narrowly as a seeded contradictory-record/gate-presupposition test. Do not use it as direct evidence that the system's own generated responses cause recursive contamination unless a genuine generated-response write-back experiment is supplied.

### [ADVERSARIAL-005] The released correction bundle and the manuscript's evidence lineage are not present in the supplied artifact

- **Severity:** MAJOR
- **Category:** artifact consistency
- **Location:** README.md, evidence table; paper/v3/main.tex, Table 1 and Section 5.3; supplied file inventory
- **Confidence:** 0.99
- **Reported by:** adversarial

The README and manuscript refer to a v0.3.1 correction bundle and cite it as part of the evidence lineage, but the supplied file inventory contains no evidence/20260713T191740Z/corrections/ directory or correction file. This prevents verification of the stated call reconciliation and makes the claimed release lineage internally incomplete.

Evidence:

- README.md, evidence table: v0.3.1 is backed by 'evidence/20260713T191740Z/corrections/' and described as an append-only 660-call reconciliation.
- paper/v3/main.tex, Table 'Evidence lineage': v0.3.1 corrections are listed as an evidence release backing call reconciliation and review-queue metadata.
- evidence/20260713T191740Z/defects.md, D9: 'No adjudications file accompanies the frozen evidence'; D10 records the 660-call total as a correction to the 485-call run metadata.
- The supplied files under evidence/20260713T191740Z include no corrections/ directory or call-count-v1.json file.

**Recommendation:** Include the referenced correction files in the frozen release and verify their hashes, or remove the v0.3.1 lineage and correction claims from the manuscript and README.

### [ARCHIVAL-001] Frozen evidence artifacts are not included in the supplied artifact

- **Severity:** MAJOR
- **Category:** archival and reproducibility
- **Location:** README.md, “Paper and evidence”; paper/v3/main.tex, Sections 5.1, 5.3, and 5.4
- **Confidence:** 0.98
- **Reported by:** archival

The paper's central numerical and trace-based results depend on frozen evidence directories that are referenced but not present among the supplied files. The README states that the evidence directories contain raw prompts, injected memories, gate decisions, responses, verdicts, and validation reports, while the supplied artifact contains only metadata, documentation, and the manuscript. Consequently, a reader of this artifact cannot independently recompute the headline results or inspect the logged gate decisions.

Evidence:

- README.md: “Each evidence directory contains the raw per-scenario artifacts (prompts, injected memories, gate decisions, responses), `verdicts.json`, `validation_report.md`, and `defects.md`” — but no `evidence/` files are among the supplied files.
- paper/v3/main.tex, Section 5.1: “Complete run artifacts are published at `evidence/20260713T084130Z` ... Every number in this section is recomputable from those artifacts.”
- paper/v3/main.tex, Section 5.4: “The v0.2 gate failure is traceable in the gate's own logged decisions.”

**Recommendation:** Distribute the frozen evidence artifacts with the archival release, or provide a persistent archive link and exact file manifest/hashes for every evidence release used by the paper. Do not rely solely on the mutable repository path.

### [ARCHIVAL-002] Evidence tags are named but not bound to immutable commit or archive contents

- **Severity:** MAJOR
- **Category:** reference immutability
- **Location:** README.md, “Quick start” and “Paper and evidence”; docs/REPRODUCTION.md, “Prerequisites” and “What to compare”; paper/v3/main.tex, Table 2 and Section 5.3
- **Confidence:** 0.96
- **Reported by:** archival

The paper identifies evidence releases by Git tags such as `v0.2-ablation` and `v0.3-repeated-ablation`, but it does not record the commit SHA, archive checksum, or DOI/version relation for those exact releases. The reproduction protocol instructs reviewers to clone the repository and inspect `HEAD`, while the manuscript and README repeatedly point to a bare GitHub repository or repository-relative paths. A tag or default branch can change after review, so the version containing the reported numbers is not unambiguously recoverable from the supplied artifact.

Evidence:

- README.md: “This repository is archived on Zenodo with the following DOI: 10.5281/zenodo.22859806” but no mapping is given from that DOI to the v0.2, v0.3, or v0.3.1 evidence contents.
- paper/v3/main.tex, Table `tab:lineage`: the evidence releases are identified by tags `v0.2-ablation`, `v0.3-repeated-ablation`, and `v0.3.1-evidence-corrections`, without commit SHAs or archive checksums.
- docs/REPRODUCTION.md, “Prerequisites”: `git clone https://github.com/arananet/contam-bench.git` followed by `git rev-parse HEAD`; this checks the checkout obtained by the reviewer, not the exact commit used for the paper’s results.

**Recommendation:** Record the exact commit SHA and archive checksum for each evidence release in the manuscript and archival metadata. Ensure the DOI resolves to an immutable archive containing those exact versions, and cite the version-specific DOI or SWHID where available.

### [ARCHIVAL-006] The seeded-recursion claim is reported from manuscript descriptions, but the underlying trace is unavailable here

- **Severity:** MAJOR
- **Category:** claim verification
- **Location:** paper/v3/main.tex, Section 5.6, “The gate amplified seeded recursion”; README.md, “Paper and evidence”
- **Confidence:** 0.97
- **Reported by:** archival

The manuscript gives a detailed account of the gate retaining the contaminated write-back and discarding premise-denying context, and appropriately limits the generalization. However, the supplied artifact does not include the cited gate logs or per-round evidence, so the central trace-based observation cannot be independently checked from the provided document package.

Evidence:

- paper/v3/main.tex, Section 5.6: the gate allegedly kept “confirms Atlas launch timing ... directly answers the query” and discarded context because it “explicitly states the launch date is tentative and not confirmed.”
- paper/v3/main.tex, Section 5.6: “this relevance gate as implemented retained the contaminated write-back and discarded the contradicting user context.”
- README.md: the relevant gate decisions are said to reside in `evidence/20260713T191740Z/`, which is not among the supplied files.

**Recommendation:** Include the exact gate-decision records and corresponding response artifacts, with immutable hashes, in the archival evidence package. Preserve the current narrow scope: one seeded-recursion scenario and one implementation, not relevance gates generally.

### [CITATIONS-001] Repeated-audit denominator is mathematically inconsistent

- **Severity:** MAJOR
- **Category:** internal consistency / evidence accounting
- **Location:** paper/v3/main.tex, Section 4.2 'Repeated-evaluation audit and scoring defects', and abstract
- **Confidence:** 0.99
- **Reported by:** citations

The manuscript states that the v0.3 audit used nine scenarios, seven configurations, and five repetitions, which implies 315 scenario-configuration repetitions, not 350. It nevertheless repeatedly calls the total 350 scored rounds and uses that number for the 52/350 unresolved fraction. The 350 subject calls can plausibly include extra recursive rounds, but those are not the same as scored scenario-configuration rounds as written.

Evidence:

- Abstract: “Of 350 scored rounds, 52 remain unresolved pending human review.”
- Section 4.2: “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds”
- Section 4.2: “The repeated audit used 660 API calls: 350 subject calls, 135 gate calls, and 175 judge calls.”
- Section 4.2, Table 4: the audit is described as repeated across seven configurations and five repetitions.

**Recommendation:** Reconcile the accounting by distinguishing scenario-configuration cells, scored rounds, and extra recursive subject calls; state the exact denominator for the 52 unresolved cases and recompute the reported percentage.

### [CITATIONS-002] Headline empirical results depend on artifacts not included in the supplied document

- **Severity:** MAJOR
- **Category:** reproducibility / evidence
- **Location:** paper/v3/main.tex, Section 4 'Ablation Study', footnote to the ablation description; Sections 4.2 and 4.4
- **Confidence:** 0.99
- **Reported by:** citations

The paper's central results rely on external JSON run artifacts, logs, hashes, and review queues, but the supplied files contain only the manuscript and bibliography. Consequently, the reported table entries, gate decisions, provenance outcomes, and 52-case review count cannot be independently checked from the provided artifact. The manuscript acknowledges that the external releases exist, but an external URL or repository claim is not evidence contained in this submission.

Evidence:

- Section 4: “Complete run artifacts are published at evidence/20260713T084130Z in the benchmark repository... Every number in this section is recomputable from those artifacts.”
- Section 4.2: “The v0.3 evidence now includes a separately versioned queue for all 52 unresolved artifact rounds, but it contains no human verdicts.”
- Section 4.4: “The v0.2 gate failure is traceable in the gate's own logged decisions.”
- The supplied file list contains only paper/v3/main.tex and paper/v3/references.bib; no evidence directory, JSON artifacts, logs, code, manifests, or review queue is supplied.

**Recommendation:** Provide the immutable evidence releases and the code/manifests needed to regenerate Tables 1–4, or explicitly label the reported empirical values as claims verified only by an external repository rather than by the submitted artifact.

### [EVIDENCE-001] The six-mechanism degradation claim exceeds the observed response-layer evidence

- **Severity:** MAJOR
- **Category:** claims
- **Location:** paper/v3/main.tex, Abstract; §3 taxonomy; §5.3 repeated audit; Conclusion
- **Confidence:** 0.97
- **Reported by:** evidence

The manuscript presents six mechanisms as mechanisms through which ordinary memory behavior can degrade later responses, but the supplied response verdicts directly show degradation only for selected cases. Semantic drift and summarization-loss responses are clean across the reported configurations, and natural recursion has no observed contamination or compounding because round 1 was clean. Thus the evidence supports six operationalized, falsifiable candidate mechanisms, not six demonstrated degradation mechanisms.

Evidence:

- paper/v3/main.tex, Abstract: “We contribute a taxonomy of six mechanisms: semantic drift, provenance collapse, scope bleed, temporal staleness, recursive compounding, and summarization loss.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: `compounding_factor_natural` is `null (round1_clean)` for every configuration.
- evidence/20260713T191740Z/validation_report.md, Per-scenario verdicts: all CB-VAL-001 semantic-drift rounds and all CB-VAL-006 summarization-loss rounds are machine-resolved `clean`.
- paper/v3/main.tex, §5.3: “Natural recursive compounding was not observed” and “The summarization probe has no utility oracle.”

**Recommendation:** Narrow the headline claim to: “We define six candidate mechanisms and operationalize each with a falsifiable scenario criterion; this pilot directly observes contamination in only a subset of those cases.”

### [METHODOLOGY-001] Primary experimental evidence is absent from the supplied artifact

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Section 4, footnote and Sections 4.1–4.4; files listed in the artifact manifest
- **Confidence:** 0.99
- **Reported by:** methodology

The paper reports results from v0.2 and v0.3 evidence releases, but the supplied files contain no persisted responses, retrieval traces, verdict JSON, run metadata, or reports from those releases. Consequently, the reported five-repetition outcomes, API-call totals, 52 unresolved rounds, and retrieval assertions cannot be independently checked from this artifact. The paper's central empirical claims therefore remain unverified in the supplied submission.

Evidence:

- The paper states that complete artifacts are at `evidence/20260713T084130Z` and that every number is recomputable from those artifacts (Section 4, footnote), but no `evidence/` files are among the supplied files.
- The paper states that the repeated audit is published at `evidence/20260713T191740Z` and reports 350 rounds, 52 reviews, and Tables 4–5 (Section 4.2), but those run artifacts are not supplied.
- `spec/metrics.md` requires metrics to be computed from `runs/<timestamp>/*.json`, yet no `runs/` artifacts are provided.

**Recommendation:** Provide the immutable v0.2/v0.3/v0.3.1 run artifacts, including raw prompts, injected memories, responses, retrieval assertions, judge outputs, verdicts, hashes, and run metadata; otherwise label the numerical results and derived claims as unverified and restrict the conclusions to the scenario specifications and methodological proposal.

### [REPO-CONSISTENCY-002] The submitted implementation cannot execute the reported benchmark without missing scenario data

- **Severity:** MAJOR
- **Category:** missing implementation
- **Location:** src/harness.py, load_scenarios and VALIDATION_SCENARIO_GLOBS; README.md, “Repository layout”; paper/v3/main.tex, §4 and §5
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The harness implementation discovers scenarios only from scenarios/validation/*.yaml and scenarios/controls/*.yaml, validates them, and then runs the benchmark. Those manifests are not supplied. Thus, although source code for the pipeline is present, the benchmark described in the paper cannot be run from this artifact and the manuscript's claims about nine hand-authored scenarios have no supplied implementation counterpart.

Evidence:

- src/harness.py: VALIDATION_SCENARIO_GLOBS is defined as scenarios/validation/*.yaml and scenarios/controls/*.yaml; load_scenarios iterates those paths and validates each manifest.
- src/harness.py: main calls load_scenarios(args.scenario) before generating any artifacts.
- README.md, repository layout: “scenarios/validation/ | 7 hand-authored contamination scenarios” and “scenarios/controls/ | 2 control scenarios.”
- paper/v3/main.tex §4: “The ablation of Section~\ref{sec:results} adds a ninth, seeded-recursion scenario, yielding nine scenarios against seven memory configurations.”
- tests/test_schema.py: asserts that the on-disk inventory is exactly CB-VAL-001..009 and scans scenarios/*/*.yaml; no such files are in the supplied artifact.

**Recommendation:** Include the nine validation/control manifests used for the reported runs, including their expected patterns, retrieval assertions, and scoring rules. If they are intentionally excluded, state that the supplied artifact is code-only and withdraw execution-based claims.

### [REPO-CONSISTENCY-003] The provenance, retrieval, and presupposition-capture findings are empirical claims without supplied traces

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** paper/v3/main.tex, Abstract; §5.3; §5.4; §5.5; README.md, “Paper and evidence”
- **Confidence:** 0.98
- **Reported by:** repo-consistency

The manuscript appropriately acknowledges unresolved scorer disagreements and limitations, but it still asserts specific repeated outcomes and a logged gate failure. The supplied artifact contains only generic retrieval and scoring code plus unit tests; it does not contain the claimed per-scenario gate decisions, subject responses, verdicts, or 52-round review queue. The code demonstrates that such traces could be generated, not that the reported observations occurred.

Evidence:

- Manuscript abstract: “On the provenance probe, tags and raw fidelity each yielded five machine-resolved clean outcomes” and “logged seeded-recursion failure illustrates how relevance filtering can discard context that denies a query's premise.”
- Manuscript §5.3: “Fifty-two of the 350 rounds (14.9%) required human review” and “The provenance separation persists without flags.”
- Manuscript §5.5: “The v0.2 gate failure is traceable in the gate's own logged decisions,” followed by quoted gate decisions and the subject's response.
- src/retrieval.py: implements generic gate calls and records gate decisions in returned runtime structures, but no frozen run trace is supplied.
- src/metrics.py: reads persisted CB-VAL-*.json artifacts and verdicts; no such evidence files are supplied.
- README.md: says the correction bundle contains “52 pending rounds, 0 human adjudications, 0 consensuses,” but the referenced correction bundle and queue are absent from the supplied artifact.

**Recommendation:** Provide the exact gate-decision logs, responses, verdicts, artifact hashes, and pending review queue used for these statements. Until then, narrow the claims to “the implementation supports logging and scoring of these outcomes” and “the proposed failure mode is illustrated by the code/test fixture,” not observed benchmark findings.

### [REPRODUCIBILITY-002] The six-mechanism degradation claim exceeds the demonstrated evidence

- **Severity:** MAJOR
- **Category:** claim_scope
- **Location:** paper/v3/main.tex, Abstract; Sections 3, 5.3, 5.5, and Conclusion; evidence/20260713T191740Z/validation_report.md
- **Confidence:** 0.97
- **Reported by:** reproducibility

The taxonomy and manifests define six candidate mechanisms, but the supplied results do not demonstrate response degradation for all six. The repeated audit reports clean outcomes for semantic drift and summarization loss across configurations, and the natural recursive scenario has a null compounding metric because round 1 was clean. Thus the evidence supports a taxonomy and case-specific probes, not the broader claim that ordinary memory behavior was shown to degrade later responses through six distinct mechanisms.

Evidence:

- paper/v3/main.tex, Abstract: “ordinary memory-system behavior, can degrade later responses through six distinct mechanisms” is presented as the study framing.
- paper/v3/main.tex, Section 5.3: “The natural recursion scenario (CB-VAL-005) ... reliably does not, yielding a null compounding factor.”
- paper/v3/main.tex, Section 5.3: “The summarization probe has no utility oracle, so it cannot establish a utility gain from raw fidelity.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: CB-VAL-001 semantic drift is clean for all listed configurations; CB-VAL-006 summarization loss is clean for all listed configurations; compounding_factor_natural is null with reason “round1_clean” for every configuration.
- paper/v3/main.tex, Conclusion: “Natural recursive compounding was not observed.”

**Recommendation:** Narrow the claim to: “We define six candidate mechanisms and obtain case-specific retrieval or response evidence for some of them; this pilot does not establish that all six degrade responses.” Treat semantic drift as a retrieval-layer observation, and describe summarization loss and natural recursion as unvalidated or null-result probes.

### [STATISTICS-001] Main ablation rates lack uncertainty estimates across configurations

- **Severity:** MAJOR
- **Category:** statistics
- **Location:** paper/v3/main.tex, §5.3 and Table repeated; evidence/20260713T191740Z/validation_report.md, Config comparison
- **Confidence:** 0.96
- **Reported by:** statistics

The manuscript reports configuration-level contamination rates and repeated outcome counts, but the main comparison does not provide confidence intervals, standard deviations, or another uncertainty summary for most configurations. The five repetitions are shown for selected cells, while the headline configuration table reports single aggregate rates such as 0.0333, 0.08, and 0.3333. This makes the apparent improvements difficult to assess statistically, especially after excluding 52 unresolved rounds.

Evidence:

- paper/v3/main.tex, §5.3: “Table~\ref{tab:repeated} reports repeated outcome distributions for the load-bearing cells.”
- paper/v3/main.tex, Table repeated: cells are reported as “clean/contaminated/flagged across five repetitions,” but no confidence intervals or dispersion estimates are reported for the configuration-level rates.
- evidence/20260713T191740Z/validation_report.md, Config comparison: contamination_rate is reported as single values such as `arm_gate 0.1304`, `arm_provenance 0.0333`, `arm_raw 0.08`, `governed 0.0333`, and `naive 0.3333`.
- paper/v3/main.tex, §5.3: “Fifty-two of the 350 rounds (14.9\%) required human review” and those rounds “are excluded from machine-only rates.”

**Recommendation:** Report numerator, denominator, and an uncertainty interval for every headline configuration rate, or restrict the claims to the displayed per-cell counts and explicitly label all aggregate rates as descriptive pilot summaries. Do not describe the rates as general mitigation improvements without this qualification.

## Judge consensus

| Finding | Severity | Reported by | Consensus |
| --- | --- | --- | --- |
| ADVERSARIAL-001 | CRITICAL | adversarial | single-source (low) |
| REPO-CONSISTENCY-001 | CRITICAL | repo-consistency | single-source (low) |
| ADVERSARIAL-002 | MAJOR | adversarial | single-source (low) |
| ADVERSARIAL-004 | MAJOR | adversarial | single-source (low) |
| ADVERSARIAL-005 | MAJOR | adversarial | single-source (low) |
| ARCHIVAL-001 | MAJOR | archival | single-source (low) |
| ARCHIVAL-002 | MAJOR | archival | single-source (low) |
| ARCHIVAL-006 | MAJOR | archival | single-source (low) |
| CITATIONS-001 | MAJOR | citations | single-source (low) |
| CITATIONS-002 | MAJOR | citations | single-source (low) |
| EVIDENCE-001 | MAJOR | evidence | single-source (low) |
| METHODOLOGY-001 | MAJOR | methodology | single-source (low) |
| REPO-CONSISTENCY-002 | MAJOR | repo-consistency | single-source (low) |
| REPO-CONSISTENCY-003 | MAJOR | repo-consistency | single-source (low) |
| REPRODUCIBILITY-001 | MAJOR | reproducibility | single-source (low) |
| REPRODUCIBILITY-002 | MAJOR | reproducibility | single-source (low) |
| STATISTICS-001 | MAJOR | statistics | single-source (low) |
| ADVERSARIAL-003 | MINOR | adversarial | single-source (low) |
| ARCHIVAL-003 | MINOR | archival | single-source (low) |
| ARCHIVAL-004 | MINOR | archival | single-source (low) |
| ARCHIVAL-005 | MINOR | archival | single-source (low) |
| CHECK-CITABILITY-001 | MINOR | check:citability | single-source (low) |
| CHECK-CITABILITY-002 | MINOR | check:citability | single-source (low) |
| CITATIONS-003 | MINOR | citations | single-source (low) |
| CITATIONS-004 | MINOR | citations | single-source (low) |
| CITATIONS-005 | MINOR | citations | single-source (low) |
| EVIDENCE-002 | MINOR | evidence | single-source (low) |
| EVIDENCE-003 | MINOR | evidence | single-source (low) |
| METHODOLOGY-002 | MINOR | methodology | single-source (low) |
| METHODOLOGY-003 | MINOR | methodology | single-source (low) |
| METHODOLOGY-004 | MINOR | methodology | single-source (low) |
| METHODOLOGY-005 | MINOR | methodology | single-source (low) |
| REPO-CONSISTENCY-004 | MINOR | repo-consistency | single-source (low) |
| REPRODUCIBILITY-003 | MINOR | reproducibility | single-source (low) |
| REPRODUCIBILITY-004 | MINOR | reproducibility | single-source (low) |
| STATISTICS-002 | MINOR | statistics | single-source (low) |
| STATISTICS-003 | MINOR | statistics | single-source (low) |

## Judge disagreements

No disagreements were recorded.

## Claim coverage

- Claims detected: 6 (6 major)
- Verified: 4
- Partially supported: 2
- Unsupported: 0
- Unverified: 0
- Evidence coverage: 83.3%

_Evidence coverage is a diagnostic, not a quality score. The findings below stand on their own._

## Deterministic checks

| Check | Status | Duration | Summary |
| --- | --- | --- | --- |
| repository-structure | skipped | 0.00s | no required_paths configured |
| required-sections | pass | 0.00s | all 5 sections present |
| archival-files | pass | 0.00s | all 3 required paths present |
| reference-integrity | skipped | 0.00s | no documents configured to check |
| citability | fail | 0.00s | 2 of 3 pattern(s) did not hold |

## All findings

### [ADVERSARIAL-001] Headline results cannot be independently reproduced from the supplied evidence bundle

- **Severity:** CRITICAL
- **Category:** reproducibility
- **Location:** Files provided; README.md, section 'Paper and evidence'; src/adjudication.py::_artifact_index; src/metrics.py::gate_observability and retrieval scoring
- **Confidence:** 0.99
- **Reported by:** adversarial

The supplied evidence directories contain metadata, reports, verdicts, defects, and a pending queue, but no raw per-scenario JSON artifacts containing the prompts, retrieved memories, gate decisions, and responses. The verdicts reference these missing artifacts by hash, while the adjudication and scoring code requires CB-*.json files. Consequently, the reported verdicts and the gate mechanism finding cannot be independently checked from the supplied artifact, and the raw evidence needed to recompute the headline results is unavailable.

Evidence:

- The supplied file inventory for evidence/20260713T191740Z lists adjudications.json, defects.md, run_meta.json, validation_report.md, and verdicts.json, but no CB-*.json raw scenario artifacts.
- README.md states that each evidence directory contains 'raw per-scenario artifacts (prompts, injected memories, gate decisions, responses, verdicts.json, validation_report.md, and defects.md)'; those raw artifacts are absent from the supplied files.
- src/adjudication.py::_artifact_index only indexes files whose names start with 'CB-' and extracts their response and scoring fields; without those files, the 52 queued rounds cannot be converted into review packets.
- src/metrics.py::gate_observability reads CB-VAL-*.json files to compute gate calls and retrieval diagnostics, so the reported gate observations cannot be recomputed from the supplied verdicts alone.

**Recommendation:** Provide the complete frozen CB-*.json raw artifact files, or remove claims that depend on independently inspecting and recomputing responses, retrievals, and gate decisions. The release should also include a manifest proving that every artifact hash in verdicts.json maps to a supplied file.

### [REPO-CONSISTENCY-001] Headline empirical results lack the evidence artifacts that supposedly produced them

- **Severity:** CRITICAL
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Abstract; §5, Table 1 footnote and §5.3; README.md, “Paper and evidence”
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The manuscript presents the nine-scenario, seven-configuration, five-repetition results as recomputable from frozen artifacts, but none of the referenced evidence directories, scenario manifests, raw responses, verdicts, or validation reports are included in the supplied artifact. The supplied file list contains README.md, paper, specs, source, and tests only. This prevents verification of the headline results and means the central empirical conclusion is not reproducible from the submission as provided.

Evidence:

- Manuscript abstract: “We report an ablation over seven configurations using one subject model and TF-IDF retrieval, followed by five repetitions of each scenario--configuration cell.”
- Manuscript §5, Table 1 footnote: “Complete run artifacts are published at evidence/20260713T084130Z in the benchmark repository, frozen at tag v0.2-ablation. Every number in this section is recomputable from those artifacts.”
- Manuscript §5.3: “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds, and is published separately at evidence/20260713T191740Z.”
- README.md, “Paper and evidence”: references evidence/20260713T084130Z, evidence/20260713T191740Z, and evidence/20260713T191740Z/corrections/. None of these paths appears in the supplied files.
- README.md, “Usage”: states that scenarios are under scenarios/validation/ and scenarios/controls/. No scenarios directory or manifest is supplied.
- tests/test_schema.py, test_v02_scenario_inventory: expects CB-VAL-001 through CB-VAL-009 on disk; those files are absent from the supplied artifact.

**Recommendation:** Supply the exact frozen evidence directories, scenario manifests, verdicts, reports, and correction/adjudication files referenced by the manuscript, or remove the numerical results and restrict the paper to claims supported by the supplied code and specifications.

### [ADVERSARIAL-002] The six-mechanism empirical claim exceeds what the pilot actually demonstrates

- **Severity:** MAJOR
- **Category:** claims
- **Location:** paper/v3/main.tex, abstract; Sections 3, 5.2, 5.3, 5.5, and Conclusion
- **Confidence:** 0.97
- **Reported by:** adversarial

The manuscript presents six mechanisms as operationalized and falsifiable, but the reported response-layer evidence does not demonstrate degradation for several of them: semantic drift resolves clean for all configurations, natural recursion has a clean first round and a null compounding factor, and summarization loss has no utility oracle and all response verdicts are clean. Thus the evidence supports a taxonomy and targeted demonstrations of selected failure modes, not the broader claim that ordinary memory behavior degrades responses through all six mechanisms.

Evidence:

- paper/v3/main.tex, abstract: 'Ordinary memory-system behaviour' is framed as producing six mechanisms, while the results report clean semantic-drift responses and unresolved seeded-recursion rounds.
- paper/v3/main.tex, Section 5.2: the natural recursion compounding factor is 'again null (round1_clean) across all seven configurations.'
- paper/v3/main.tex, Section 5.3: 'The summarization probe has no utility oracle, so it cannot establish a utility gain from raw fidelity.'
- paper/v3/main.tex, Section 5.5: 'Semantic drift remains a response-layer tie: all configurations resolved clean.'
- evidence/20260713T191740Z/validation_report.md, Config comparison: compounding_factor_natural is null for every configuration and the response-level staleness rates are null for four configurations.

**Recommendation:** Narrow the headline to: the study defines six candidate mechanisms and obtains within-scenario evidence for provenance, scope, and selected retrieval/gate behaviors; it does not empirically establish response degradation for all six mechanisms.

### [ADVERSARIAL-004] The seeded-recursion experiment does not test recursive write-back propagation in the same way as the natural recursion experiment

- **Severity:** MAJOR
- **Category:** experimental design
- **Location:** paper/v3/main.tex, Section 5.2 'Seeded recursion (CB-VAL-009)'; scenarios/validation/cb-val-009-recursive-seeded.yaml; src/harness.py::run_pair
- **Confidence:** 0.98
- **Reported by:** adversarial

The paper calls CB-VAL-009 a seeded-recursion mechanism test, but the contaminated assistant write-back is manually placed in the initial memory seed. This bypasses the causal step central to recursive contamination—an assistant response being generated, written back, and then retrieved. The experiment tests handling of a pre-existing contradictory assistant record and the gate's filtering behavior, not whether the system's own output creates or compounds that record.

Evidence:

- paper/v3/main.tex, Section 5.2: 'the store is seeded directly with an already-contaminated assistant-attributed write-back ... alongside the user-sourced ground truth.'
- scenarios/validation/cb-val-009-recursive-seeded.yaml: the initial memory_seed contains 'atlas-confirmed-write-back' with source 'assistant'; the scenario has no write_back: true or round2 block.
- src/harness.py::run_pair: only scenarios with 'write_back' and 'round2' execute the response-to-store transition; CB-VAL-009 therefore has no generated write-back transition.
- paper/v3/main.tex, Section 3: recursive contamination is defined as 'write-back of assistant output' and later retrieval of that output.

**Recommendation:** Describe CB-VAL-009 narrowly as a seeded contradictory-record/gate-presupposition test. Do not use it as direct evidence that the system's own generated responses cause recursive contamination unless a genuine generated-response write-back experiment is supplied.

### [ADVERSARIAL-005] The released correction bundle and the manuscript's evidence lineage are not present in the supplied artifact

- **Severity:** MAJOR
- **Category:** artifact consistency
- **Location:** README.md, evidence table; paper/v3/main.tex, Table 1 and Section 5.3; supplied file inventory
- **Confidence:** 0.99
- **Reported by:** adversarial

The README and manuscript refer to a v0.3.1 correction bundle and cite it as part of the evidence lineage, but the supplied file inventory contains no evidence/20260713T191740Z/corrections/ directory or correction file. This prevents verification of the stated call reconciliation and makes the claimed release lineage internally incomplete.

Evidence:

- README.md, evidence table: v0.3.1 is backed by 'evidence/20260713T191740Z/corrections/' and described as an append-only 660-call reconciliation.
- paper/v3/main.tex, Table 'Evidence lineage': v0.3.1 corrections are listed as an evidence release backing call reconciliation and review-queue metadata.
- evidence/20260713T191740Z/defects.md, D9: 'No adjudications file accompanies the frozen evidence'; D10 records the 660-call total as a correction to the 485-call run metadata.
- The supplied files under evidence/20260713T191740Z include no corrections/ directory or call-count-v1.json file.

**Recommendation:** Include the referenced correction files in the frozen release and verify their hashes, or remove the v0.3.1 lineage and correction claims from the manuscript and README.

### [ARCHIVAL-001] Frozen evidence artifacts are not included in the supplied artifact

- **Severity:** MAJOR
- **Category:** archival and reproducibility
- **Location:** README.md, “Paper and evidence”; paper/v3/main.tex, Sections 5.1, 5.3, and 5.4
- **Confidence:** 0.98
- **Reported by:** archival

The paper's central numerical and trace-based results depend on frozen evidence directories that are referenced but not present among the supplied files. The README states that the evidence directories contain raw prompts, injected memories, gate decisions, responses, verdicts, and validation reports, while the supplied artifact contains only metadata, documentation, and the manuscript. Consequently, a reader of this artifact cannot independently recompute the headline results or inspect the logged gate decisions.

Evidence:

- README.md: “Each evidence directory contains the raw per-scenario artifacts (prompts, injected memories, gate decisions, responses), `verdicts.json`, `validation_report.md`, and `defects.md`” — but no `evidence/` files are among the supplied files.
- paper/v3/main.tex, Section 5.1: “Complete run artifacts are published at `evidence/20260713T084130Z` ... Every number in this section is recomputable from those artifacts.”
- paper/v3/main.tex, Section 5.4: “The v0.2 gate failure is traceable in the gate's own logged decisions.”

**Recommendation:** Distribute the frozen evidence artifacts with the archival release, or provide a persistent archive link and exact file manifest/hashes for every evidence release used by the paper. Do not rely solely on the mutable repository path.

### [ARCHIVAL-002] Evidence tags are named but not bound to immutable commit or archive contents

- **Severity:** MAJOR
- **Category:** reference immutability
- **Location:** README.md, “Quick start” and “Paper and evidence”; docs/REPRODUCTION.md, “Prerequisites” and “What to compare”; paper/v3/main.tex, Table 2 and Section 5.3
- **Confidence:** 0.96
- **Reported by:** archival

The paper identifies evidence releases by Git tags such as `v0.2-ablation` and `v0.3-repeated-ablation`, but it does not record the commit SHA, archive checksum, or DOI/version relation for those exact releases. The reproduction protocol instructs reviewers to clone the repository and inspect `HEAD`, while the manuscript and README repeatedly point to a bare GitHub repository or repository-relative paths. A tag or default branch can change after review, so the version containing the reported numbers is not unambiguously recoverable from the supplied artifact.

Evidence:

- README.md: “This repository is archived on Zenodo with the following DOI: 10.5281/zenodo.22859806” but no mapping is given from that DOI to the v0.2, v0.3, or v0.3.1 evidence contents.
- paper/v3/main.tex, Table `tab:lineage`: the evidence releases are identified by tags `v0.2-ablation`, `v0.3-repeated-ablation`, and `v0.3.1-evidence-corrections`, without commit SHAs or archive checksums.
- docs/REPRODUCTION.md, “Prerequisites”: `git clone https://github.com/arananet/contam-bench.git` followed by `git rev-parse HEAD`; this checks the checkout obtained by the reviewer, not the exact commit used for the paper’s results.

**Recommendation:** Record the exact commit SHA and archive checksum for each evidence release in the manuscript and archival metadata. Ensure the DOI resolves to an immutable archive containing those exact versions, and cite the version-specific DOI or SWHID where available.

### [ARCHIVAL-006] The seeded-recursion claim is reported from manuscript descriptions, but the underlying trace is unavailable here

- **Severity:** MAJOR
- **Category:** claim verification
- **Location:** paper/v3/main.tex, Section 5.6, “The gate amplified seeded recursion”; README.md, “Paper and evidence”
- **Confidence:** 0.97
- **Reported by:** archival

The manuscript gives a detailed account of the gate retaining the contaminated write-back and discarding premise-denying context, and appropriately limits the generalization. However, the supplied artifact does not include the cited gate logs or per-round evidence, so the central trace-based observation cannot be independently checked from the provided document package.

Evidence:

- paper/v3/main.tex, Section 5.6: the gate allegedly kept “confirms Atlas launch timing ... directly answers the query” and discarded context because it “explicitly states the launch date is tentative and not confirmed.”
- paper/v3/main.tex, Section 5.6: “this relevance gate as implemented retained the contaminated write-back and discarded the contradicting user context.”
- README.md: the relevant gate decisions are said to reside in `evidence/20260713T191740Z/`, which is not among the supplied files.

**Recommendation:** Include the exact gate-decision records and corresponding response artifacts, with immutable hashes, in the archival evidence package. Preserve the current narrow scope: one seeded-recursion scenario and one implementation, not relevance gates generally.

### [CITATIONS-001] Repeated-audit denominator is mathematically inconsistent

- **Severity:** MAJOR
- **Category:** internal consistency / evidence accounting
- **Location:** paper/v3/main.tex, Section 4.2 'Repeated-evaluation audit and scoring defects', and abstract
- **Confidence:** 0.99
- **Reported by:** citations

The manuscript states that the v0.3 audit used nine scenarios, seven configurations, and five repetitions, which implies 315 scenario-configuration repetitions, not 350. It nevertheless repeatedly calls the total 350 scored rounds and uses that number for the 52/350 unresolved fraction. The 350 subject calls can plausibly include extra recursive rounds, but those are not the same as scored scenario-configuration rounds as written.

Evidence:

- Abstract: “Of 350 scored rounds, 52 remain unresolved pending human review.”
- Section 4.2: “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds”
- Section 4.2: “The repeated audit used 660 API calls: 350 subject calls, 135 gate calls, and 175 judge calls.”
- Section 4.2, Table 4: the audit is described as repeated across seven configurations and five repetitions.

**Recommendation:** Reconcile the accounting by distinguishing scenario-configuration cells, scored rounds, and extra recursive subject calls; state the exact denominator for the 52 unresolved cases and recompute the reported percentage.

### [CITATIONS-002] Headline empirical results depend on artifacts not included in the supplied document

- **Severity:** MAJOR
- **Category:** reproducibility / evidence
- **Location:** paper/v3/main.tex, Section 4 'Ablation Study', footnote to the ablation description; Sections 4.2 and 4.4
- **Confidence:** 0.99
- **Reported by:** citations

The paper's central results rely on external JSON run artifacts, logs, hashes, and review queues, but the supplied files contain only the manuscript and bibliography. Consequently, the reported table entries, gate decisions, provenance outcomes, and 52-case review count cannot be independently checked from the provided artifact. The manuscript acknowledges that the external releases exist, but an external URL or repository claim is not evidence contained in this submission.

Evidence:

- Section 4: “Complete run artifacts are published at evidence/20260713T084130Z in the benchmark repository... Every number in this section is recomputable from those artifacts.”
- Section 4.2: “The v0.3 evidence now includes a separately versioned queue for all 52 unresolved artifact rounds, but it contains no human verdicts.”
- Section 4.4: “The v0.2 gate failure is traceable in the gate's own logged decisions.”
- The supplied file list contains only paper/v3/main.tex and paper/v3/references.bib; no evidence directory, JSON artifacts, logs, code, manifests, or review queue is supplied.

**Recommendation:** Provide the immutable evidence releases and the code/manifests needed to regenerate Tables 1–4, or explicitly label the reported empirical values as claims verified only by an external repository rather than by the submitted artifact.

### [EVIDENCE-001] The six-mechanism degradation claim exceeds the observed response-layer evidence

- **Severity:** MAJOR
- **Category:** claims
- **Location:** paper/v3/main.tex, Abstract; §3 taxonomy; §5.3 repeated audit; Conclusion
- **Confidence:** 0.97
- **Reported by:** evidence

The manuscript presents six mechanisms as mechanisms through which ordinary memory behavior can degrade later responses, but the supplied response verdicts directly show degradation only for selected cases. Semantic drift and summarization-loss responses are clean across the reported configurations, and natural recursion has no observed contamination or compounding because round 1 was clean. Thus the evidence supports six operationalized, falsifiable candidate mechanisms, not six demonstrated degradation mechanisms.

Evidence:

- paper/v3/main.tex, Abstract: “We contribute a taxonomy of six mechanisms: semantic drift, provenance collapse, scope bleed, temporal staleness, recursive compounding, and summarization loss.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: `compounding_factor_natural` is `null (round1_clean)` for every configuration.
- evidence/20260713T191740Z/validation_report.md, Per-scenario verdicts: all CB-VAL-001 semantic-drift rounds and all CB-VAL-006 summarization-loss rounds are machine-resolved `clean`.
- paper/v3/main.tex, §5.3: “Natural recursive compounding was not observed” and “The summarization probe has no utility oracle.”

**Recommendation:** Narrow the headline claim to: “We define six candidate mechanisms and operationalize each with a falsifiable scenario criterion; this pilot directly observes contamination in only a subset of those cases.”

### [METHODOLOGY-001] Primary experimental evidence is absent from the supplied artifact

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Section 4, footnote and Sections 4.1–4.4; files listed in the artifact manifest
- **Confidence:** 0.99
- **Reported by:** methodology

The paper reports results from v0.2 and v0.3 evidence releases, but the supplied files contain no persisted responses, retrieval traces, verdict JSON, run metadata, or reports from those releases. Consequently, the reported five-repetition outcomes, API-call totals, 52 unresolved rounds, and retrieval assertions cannot be independently checked from this artifact. The paper's central empirical claims therefore remain unverified in the supplied submission.

Evidence:

- The paper states that complete artifacts are at `evidence/20260713T084130Z` and that every number is recomputable from those artifacts (Section 4, footnote), but no `evidence/` files are among the supplied files.
- The paper states that the repeated audit is published at `evidence/20260713T191740Z` and reports 350 rounds, 52 reviews, and Tables 4–5 (Section 4.2), but those run artifacts are not supplied.
- `spec/metrics.md` requires metrics to be computed from `runs/<timestamp>/*.json`, yet no `runs/` artifacts are provided.

**Recommendation:** Provide the immutable v0.2/v0.3/v0.3.1 run artifacts, including raw prompts, injected memories, responses, retrieval assertions, judge outputs, verdicts, hashes, and run metadata; otherwise label the numerical results and derived claims as unverified and restrict the conclusions to the scenario specifications and methodological proposal.

### [REPO-CONSISTENCY-002] The submitted implementation cannot execute the reported benchmark without missing scenario data

- **Severity:** MAJOR
- **Category:** missing implementation
- **Location:** src/harness.py, load_scenarios and VALIDATION_SCENARIO_GLOBS; README.md, “Repository layout”; paper/v3/main.tex, §4 and §5
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The harness implementation discovers scenarios only from scenarios/validation/*.yaml and scenarios/controls/*.yaml, validates them, and then runs the benchmark. Those manifests are not supplied. Thus, although source code for the pipeline is present, the benchmark described in the paper cannot be run from this artifact and the manuscript's claims about nine hand-authored scenarios have no supplied implementation counterpart.

Evidence:

- src/harness.py: VALIDATION_SCENARIO_GLOBS is defined as scenarios/validation/*.yaml and scenarios/controls/*.yaml; load_scenarios iterates those paths and validates each manifest.
- src/harness.py: main calls load_scenarios(args.scenario) before generating any artifacts.
- README.md, repository layout: “scenarios/validation/ | 7 hand-authored contamination scenarios” and “scenarios/controls/ | 2 control scenarios.”
- paper/v3/main.tex §4: “The ablation of Section~\ref{sec:results} adds a ninth, seeded-recursion scenario, yielding nine scenarios against seven memory configurations.”
- tests/test_schema.py: asserts that the on-disk inventory is exactly CB-VAL-001..009 and scans scenarios/*/*.yaml; no such files are in the supplied artifact.

**Recommendation:** Include the nine validation/control manifests used for the reported runs, including their expected patterns, retrieval assertions, and scoring rules. If they are intentionally excluded, state that the supplied artifact is code-only and withdraw execution-based claims.

### [REPO-CONSISTENCY-003] The provenance, retrieval, and presupposition-capture findings are empirical claims without supplied traces

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** paper/v3/main.tex, Abstract; §5.3; §5.4; §5.5; README.md, “Paper and evidence”
- **Confidence:** 0.98
- **Reported by:** repo-consistency

The manuscript appropriately acknowledges unresolved scorer disagreements and limitations, but it still asserts specific repeated outcomes and a logged gate failure. The supplied artifact contains only generic retrieval and scoring code plus unit tests; it does not contain the claimed per-scenario gate decisions, subject responses, verdicts, or 52-round review queue. The code demonstrates that such traces could be generated, not that the reported observations occurred.

Evidence:

- Manuscript abstract: “On the provenance probe, tags and raw fidelity each yielded five machine-resolved clean outcomes” and “logged seeded-recursion failure illustrates how relevance filtering can discard context that denies a query's premise.”
- Manuscript §5.3: “Fifty-two of the 350 rounds (14.9%) required human review” and “The provenance separation persists without flags.”
- Manuscript §5.5: “The v0.2 gate failure is traceable in the gate's own logged decisions,” followed by quoted gate decisions and the subject's response.
- src/retrieval.py: implements generic gate calls and records gate decisions in returned runtime structures, but no frozen run trace is supplied.
- src/metrics.py: reads persisted CB-VAL-*.json artifacts and verdicts; no such evidence files are supplied.
- README.md: says the correction bundle contains “52 pending rounds, 0 human adjudications, 0 consensuses,” but the referenced correction bundle and queue are absent from the supplied artifact.

**Recommendation:** Provide the exact gate-decision logs, responses, verdicts, artifact hashes, and pending review queue used for these statements. Until then, narrow the claims to “the implementation supports logging and scoring of these outcomes” and “the proposed failure mode is illustrated by the code/test fixture,” not observed benchmark findings.

### [REPRODUCIBILITY-001] Headline results cannot be independently reproduced from the supplied artifact

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** README.md, “Paper and evidence” and “Usage”; evidence/20260713T191740Z/run_meta.json; evidence/20260713T191740Z/verdicts.json; requirements.txt; docs/REPRODUCTION.md, “Prerequisites” and “What to compare”
- **Confidence:** 0.99
- **Reported by:** reproducibility

The repository provides commands for rerunning the live pipeline, but the supplied evidence does not include the raw per-scenario JSON artifacts, prompts, injected memories, gate decisions, or responses that produced the reported rates. The README claims that each evidence directory contains these artifacts, but the supplied file inventory contains only run metadata, reports, verdicts, defects, and the adjudication queue. In addition, requirements.txt uses unpinned lower bounds and no lockfile, container, exact commit, or complete environment capture is supplied. Consequently, an independent researcher cannot reproduce or audit the reported response-layer rates, the 52 disputed rounds, or the gate finding from the artifact alone.

Evidence:

- README.md: “Each evidence directory contains the raw per-scenario artifacts (prompts, injected memory, gate decisions, responses), verdicts.json, validation_report.md, and defects.md” (the supplied evidence file list contains no such per-scenario artifact files).
- README.md: the live reproduction commands require API credentials and create new runs, while the saved evidence is described as auditable but is not supplied with the raw artifacts.
- requirements.txt: dependencies are specified only as lower bounds, e.g. “anthropic>=0.116”, “scikit-learn>=1.3”, and “pytest>=8.0”.
- evidence/20260713T191740Z/run_meta.json: records model names and call counts but no commit SHA, package versions, operating system, hardware, or random seed.
- docs/REPRODUCTION.md: “A different result on a different commit is not a reproduction discrepancy by itself,” but no tested commit is recorded in the frozen run metadata.

**Recommendation:** Supply the frozen raw artifacts referenced by README.md, including every response, prompt, injected memory, retrieval trace, and gate decision; record the exact commit, Python and dependency versions, model identifiers, configuration hashes, and any relevant seeds; and provide a lockfile or container for the reported release. Until then, restrict reproducibility claims to recomputation of the supplied verdict aggregates.

### [REPRODUCIBILITY-002] The six-mechanism degradation claim exceeds the demonstrated evidence

- **Severity:** MAJOR
- **Category:** claim_scope
- **Location:** paper/v3/main.tex, Abstract; Sections 3, 5.3, 5.5, and Conclusion; evidence/20260713T191740Z/validation_report.md
- **Confidence:** 0.97
- **Reported by:** reproducibility

The taxonomy and manifests define six candidate mechanisms, but the supplied results do not demonstrate response degradation for all six. The repeated audit reports clean outcomes for semantic drift and summarization loss across configurations, and the natural recursive scenario has a null compounding metric because round 1 was clean. Thus the evidence supports a taxonomy and case-specific probes, not the broader claim that ordinary memory behavior was shown to degrade later responses through six distinct mechanisms.

Evidence:

- paper/v3/main.tex, Abstract: “ordinary memory-system behavior, can degrade later responses through six distinct mechanisms” is presented as the study framing.
- paper/v3/main.tex, Section 5.3: “The natural recursion scenario (CB-VAL-005) ... reliably does not, yielding a null compounding factor.”
- paper/v3/main.tex, Section 5.3: “The summarization probe has no utility oracle, so it cannot establish a utility gain from raw fidelity.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: CB-VAL-001 semantic drift is clean for all listed configurations; CB-VAL-006 summarization loss is clean for all listed configurations; compounding_factor_natural is null with reason “round1_clean” for every configuration.
- paper/v3/main.tex, Conclusion: “Natural recursive compounding was not observed.”

**Recommendation:** Narrow the claim to: “We define six candidate mechanisms and obtain case-specific retrieval or response evidence for some of them; this pilot does not establish that all six degrade responses.” Treat semantic drift as a retrieval-layer observation, and describe summarization loss and natural recursion as unvalidated or null-result probes.

### [STATISTICS-001] Main ablation rates lack uncertainty estimates across configurations

- **Severity:** MAJOR
- **Category:** statistics
- **Location:** paper/v3/main.tex, §5.3 and Table repeated; evidence/20260713T191740Z/validation_report.md, Config comparison
- **Confidence:** 0.96
- **Reported by:** statistics

The manuscript reports configuration-level contamination rates and repeated outcome counts, but the main comparison does not provide confidence intervals, standard deviations, or another uncertainty summary for most configurations. The five repetitions are shown for selected cells, while the headline configuration table reports single aggregate rates such as 0.0333, 0.08, and 0.3333. This makes the apparent improvements difficult to assess statistically, especially after excluding 52 unresolved rounds.

Evidence:

- paper/v3/main.tex, §5.3: “Table~\ref{tab:repeated} reports repeated outcome distributions for the load-bearing cells.”
- paper/v3/main.tex, Table repeated: cells are reported as “clean/contaminated/flagged across five repetitions,” but no confidence intervals or dispersion estimates are reported for the configuration-level rates.
- evidence/20260713T191740Z/validation_report.md, Config comparison: contamination_rate is reported as single values such as `arm_gate 0.1304`, `arm_provenance 0.0333`, `arm_raw 0.08`, `governed 0.0333`, and `naive 0.3333`.
- paper/v3/main.tex, §5.3: “Fifty-two of the 350 rounds (14.9\%) required human review” and those rounds “are excluded from machine-only rates.”

**Recommendation:** Report numerator, denominator, and an uncertainty interval for every headline configuration rate, or restrict the claims to the displayed per-cell counts and explicitly label all aggregate rates as descriptive pilot summaries. Do not describe the rates as general mitigation improvements without this qualification.

### [ADVERSARIAL-003] Most load-bearing response comparisons remain unresolved and machine-only

- **Severity:** MINOR
- **Category:** scoring validity
- **Location:** paper/v3/main.tex, Sections 5.3, 5.4, 5.5; evidence/20260713T191740Z/defects.md D7-D9; evidence/20260713T191740Z/validation_report.md
- **Confidence:** 0.99
- **Reported by:** adversarial

The repeated audit leaves 52 of 350 rounds unresolved, including every staleness comparator outside provenance/TTL/governed and most seeded-recursion cells. These unresolved rounds are excluded from both numerator and denominator, so the reported rates are conditional on scorer agreement and cannot support complete comparative conclusions for those mechanisms. The manuscript acknowledges this, but still uses the pilot to motivate mitigation conclusions and describes some cells as clean comparators despite their unresolved status.

Evidence:

- evidence/20260713T191740Z/defects.md, D7: 'Fifty-two of the 350 scored rounds resolved to needs_human_review' and 'the run has no human-adjudicated comparison.'
- evidence/20260713T191740Z/validation_report.md, Human-adjudicated comparison: 'unavailable (adjudications_file_missing); machine verdicts remain authoritative.'
- evidence/20260713T191740Z/validation_report.md, Config comparison: staleness_rate is null for arm_gate, arm_namespace, arm_raw, and naive.
- paper/v3/main.tex, Section 5.3: 'Neither direction establishes which scorer is correct without independent assessment.'
- evidence/20260713T191740Z/adjudications.json: 'adjudications': [] and 52 entries with status 'pending'.

**Recommendation:** Treat all affected comparisons as unresolved rather than as clean/contaminated outcomes, and avoid ranking controls using cells with substantial pending fractions. Complete independent blinded adjudication before making response-layer mitigation claims.

### [ARCHIVAL-003] Code licence is referenced but the licence file is not present in the supplied artifact

- **Severity:** MINOR
- **Category:** licensing
- **Location:** LICENSING.md; README.md, “License”; CITATION.cff
- **Confidence:** 0.97
- **Reported by:** archival

The licensing policy claims that code is Apache-2.0 and points to `LICENSE`, but `LICENSE` is not among the supplied files. The README also labels the repository “License: Apache 2.0,” while the CFF uses CC-BY-4.0 and LICENSING.md assigns CC-BY-4.0 to manuscript, figures, data, and evidence. The intended separation is stated, but the actual code licence grant cannot be verified from the supplied artifact.

Evidence:

- LICENSING.md: “Code — harness, scripts, tests and any software in this repository: Apache-2.0. See [`LICENSE`](LICENSE).”
- README.md: “## License [Apache 2.0](LICENSE)”
- The supplied file list contains no `LICENSE` file.

**Recommendation:** Include the complete Apache-2.0 `LICENSE` file in the archival artifact and retain explicit, separate licence notices for code, paper, data, figures, and evidence.

### [ARCHIVAL-004] The broad six-mechanism claim is supported only as a bounded pilot demonstration

- **Severity:** MINOR
- **Category:** claim scope
- **Location:** paper/v3/main.tex, Abstract; Sections 3, 5.5, and 6
- **Confidence:** 0.96
- **Reported by:** archival

The manuscript presents six mechanisms with falsifiable criteria, but the empirical design uses one hand-authored probe per mechanism, one subject model, TF-IDF retrieval, and unresolved scoring disagreements. The evidence therefore supports operationalization and observations in the tested cases, not the broader implication that ordinary memory-system behavior generally degrades later responses through six distinct mechanisms.

Evidence:

- Abstract: “We contribute a taxonomy of six mechanisms” and describe the nine-scenario pilot.
- paper/v3/main.tex, Section 6, “Validity statements”: “One subject model cannot establish model-independent behavior ... Rates from one probe per mechanism are mechanism demonstrations with stated resolved counts, not population estimates.”
- paper/v3/main.tex, Section 6, “Scale”: “one probe per class ... designed to validate the pipeline and isolate mechanisms.”

**Recommendation:** State the claim as: “We operationalize six candidate mechanisms and observe bounded demonstrations of them in the tested scenarios,” rather than implying general degradation across ordinary memory systems.

### [ARCHIVAL-005] The provenance-preservation interpretation is confounded by bundled metadata

- **Severity:** MINOR
- **Category:** claim interpretation
- **Location:** paper/v3/main.tex, Section 5.5, paragraph beginning “The off-diagonal cells”; Section 6, “Validity statements”
- **Confidence:** 0.99
- **Reported by:** archival

The five clean outcomes for the provenance-tag and raw-fidelity arms are directly reported, but the interpretation that they preserve source information lost during summarization is not isolated experimentally. The manuscript explicitly acknowledges that the provenance tag also exposes age and domain, and that raw and tagged conditions are alternative interventions on the same case.

Evidence:

- paper/v3/main.tex, Section 5.3: “provenance tags, raw fidelity, and the governed bundle are each 5/0/0.”
- paper/v3/main.tex, Section 5.5: “the provenance tag as implemented carries age and domain metadata ... so the provenance arm also resolved staleness because the subject discounted the 200-day-old fact by its visible age.”
- paper/v3/main.tex, Section 5.5: “This is consistent with loss of source information during summarization in this scenario, but does not establish summarization as the principal cause of provenance collapse generally.”

**Recommendation:** Retain the narrow case-specific wording: “Both interventions produced five machine-resolved clean outcomes in this probe, consistent with—but not isolating—a source-information explanation.” Avoid attributing the result to summarization loss without a pure-factor provenance ablation.

### [CHECK-CITABILITY-001] Missing from the artifact: a DOI for the archived work

- **Severity:** MINOR
- **Category:** check/citability
- **Location:** paper/v3/main.tex
- **Confidence:** 1.00
- **Reported by:** check:citability

Nothing in paper/v3/main.tex matches the expected pattern `10\.\d{4,}/`.

Evidence:

- no match for `10\.\d{4,}/`

**Recommendation:** Add a DOI for the archived work.

### [CHECK-CITABILITY-002] Missing from the artifact: a data or code availability statement

- **Severity:** MINOR
- **Category:** check/citability
- **Location:** paper/v3/main.tex
- **Confidence:** 1.00
- **Reported by:** check:citability

Nothing in paper/v3/main.tex matches the expected pattern `(?i)data availability|availability statement|code availability`.

Evidence:

- no match for `(?i)data availability|availability statement|code availability`

**Recommendation:** Add a data or code availability statement.

### [CITATIONS-003] The six-mechanism empirical claim is supported only unevenly across mechanisms

- **Severity:** MINOR
- **Category:** claim scope / experimental support
- **Location:** paper/v3/main.tex, Sections 3, 4.3, 4.4, 5 'Discussion and Limitations', and Conclusion
- **Confidence:** 0.97
- **Reported by:** citations

The taxonomy and falsifiable criteria are documented, but the validation evidence does not establish response degradation for all six mechanisms. Semantic drift has clean response verdicts in every configuration; the staleness response comparison is flagged; summarization has no declared utility oracle; and natural recursion has a null compounding factor. Thus the evidence supports a taxonomy and case-specific retrieval or failure demonstrations, not a demonstrated six-mechanism degradation result.

Evidence:

- Section 3: “Six classes are tested in the validation run; a seventh is documented as experimental.”
- Section 4.3: “Response scoring nevertheless resolved clean across configurations” for semantic drift.
- Section 4.3: “Staleness remains retrieval-layer evidence because its response-layer comparators are flagged.”
- Section 4.3: “The summarization probe has no utility oracle, so it cannot establish a utility gain from raw fidelity.”
- Section 4.5: “The natural-recursion compounding factor is again null.”
- Conclusion: “This pilot operationalizes six proposed mechanisms ... in a small, auditable scenario suite.”

**Recommendation:** Use the narrower claim that the study operationalizes six proposed mechanisms and demonstrates selected retrieval-layer or case-specific effects; do not imply that all six were empirically shown to degrade responses. The manuscript already states most of this limitation, so this is primarily a claim-status clarification.

### [CITATIONS-004] Several prior-work assertions have no citation attached

- **Severity:** MINOR
- **Category:** citation completeness
- **Location:** paper/v3/main.tex, Section 2 'Related Work'
- **Confidence:** 0.98
- **Reported by:** citations

The manuscript makes claims about prior work without attaching a citation, making the source and evidentiary basis unclear. This concerns citation existence/completeness, not a determination that the listed references are unreal.

Evidence:

- Section 2, paragraph 'Measurement of non-adversarial memory risk': “Complementary diagnosis work finds most memory failures stem from irrelevant retrieval rather than memory construction.” No citation follows this sentence.
- The same paragraph: “follow-on work quantifies a passage's distracting effect as a graded severity measure.” No citation follows this claim.
- Section 2, paragraph 'Adversarial memory poisoning': “subsequent work has extended the attack surface.” No citation is supplied for the subsequent work.

**Recommendation:** Attach the specific references supporting each assertion, or remove/rephrase the assertions as observations not attributed to prior work.

### [CITATIONS-005] Reference support and resolvability cannot be verified from the supplied files alone

- **Severity:** MINOR
- **Category:** citation verification
- **Location:** paper/v3/main.tex, Sections 2, 3, and 6; paper/v3/references.bib
- **Confidence:** 0.90
- **Reported by:** citations

The bibliography contains plausible entries and arXiv identifiers, but the supplied artifact provides no retrieved reference metadata, full texts, or verification record. Therefore claims attributed to specific papers—such as Wang et al.'s “memory laundering,” STOP's degradation with weak models, and Anthropic's exact memory-store capabilities—remain unverified from the artifact alone. This is a verification limitation, not an allegation of fabrication.

Evidence:

- Section 2: “Wang et al. demonstrate memory laundering...” citing \cite{wang2026state}.
- Section 3: “the STOP experiments showed ... degraded them with weak ones” citing \cite{zelikman2023stop}.
- Section 6: Anthropic's managed stores are said to ship “per-user and per-team store scoping ... immutable memory versions with audit trails” citing \cite{anthropic2026memory}.
- references.bib contains only bibliographic records and URLs; it does not contain the cited works' text or verification results.

**Recommendation:** Verify each reference against its canonical publication or documentation source and ensure the cited source actually supports the attached claim; otherwise narrow the claim or provide a more appropriate citation.

### [EVIDENCE-002] The provenance causal interpretation is only partially supported by one confounded probe

- **Severity:** MINOR
- **Category:** claims
- **Location:** paper/v3/main.tex, Abstract; §5.5 “Attribution: what the cells support”; §3 provenance taxonomy
- **Confidence:** 0.95
- **Reported by:** evidence

Five clean machine-resolved outcomes for the provenance-tag and raw-fidelity arms are supported. The stronger interpretation that this demonstrates source information was lost during summarization is not established: the raw and summarized stores differ in more than one aspect of the comparison, the provenance tag bundles source, age, and domain, and only one hand-authored provenance scenario is used. The manuscript acknowledges these limitations, but the abstract still foregrounds the causal interpretation.

Evidence:

- paper/v3/main.tex, §5.3: “the provenance tags, raw fidelity, and the governed bundle are each 5/0/0.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: `provenance_error_rate` is `0.0` for `arm_provenance`, `arm_raw`, and `governed`, while it is `1.0` for `naive`, `arm_namespace`, `arm_ttl`, and `arm_gate`.
- paper/v3/main.tex, §5.5: “the provenance tag as implemented carries age and domain metadata ... so the provenance arm also resolved staleness because the subject discounted the 200-day-old fact.”
- paper/v3/main.tex, §5.5: “The two arms are alternative interventions on the same case, not independent replications of that explanation.”

**Recommendation:** Retain the observed-outcome claim, but state the interpretation as a case-specific hypothesis: “These outcomes are consistent with source information being unavailable in the summarized representation; the study does not isolate summarization loss as the cause.”

### [EVIDENCE-003] The paper’s mitigation language must remain case-specific, not general efficacy evidence

- **Severity:** MINOR
- **Category:** claims
- **Location:** paper/v3/main.tex, Abstract; §5.6 “The gate amplified seeded recursion”; §6 architecture; Conclusion
- **Confidence:** 0.93
- **Reported by:** evidence

The evidence supports targeted retrieval effects for namespacing and TTL and a single observed gate failure, but it does not support a general mitigation ranking or model-independent efficacy claim. The manuscript mostly states this limitation correctly, yet the architecture and abstract framing could still be read as validating the proposed mitigation architecture.

Evidence:

- evidence/20260713T191740Z/validation_report.md, Retrieval assertions: namespacing passes CB-VAL-003 in `5/5` repetitions and TTL passes CB-VAL-004 in `5/5`; response-layer staleness is `null` for several configurations because probes need human review.
- evidence/20260713T191740Z/defects.md, D7: “Fifty-two of the 350 scored rounds ... resolved to `needs_human_review`” and “the run has no human-adjudicated comparison.”
- paper/v3/main.tex, §5.6: “The other arms are entirely flagged on that probe, so they cannot be treated as clean comparators or used to rank gate harm.”
- paper/v3/main.tex, §6: “The ablation motivates constraints, not an efficacy ordering.”
- paper/v3/main.tex, Conclusion: “They motivate further tests of memory contracts, not a validated general mitigation architecture.”

**Recommendation:** Keep mitigation conclusions explicitly limited to the tested scenarios, configurations, model, and retrieval backend; avoid wording that implies general efficacy or a validated architecture.

### [METHODOLOGY-002] The validation design cannot support general claims about six mechanisms or mitigation efficacy

- **Severity:** MINOR
- **Category:** experimental-design
- **Location:** paper/v3/main.tex, Sections 3, 4.1, 4.3, and Discussion/Validity statements
- **Confidence:** 0.97
- **Reported by:** methodology

Each contamination mechanism is represented by only one hand-authored validation scenario, evaluated with one subject model and one retrieval backend. This can demonstrate case-specific behavior, but cannot establish that the mechanisms are distinct or broadly characteristic, nor that the controls are generally effective. The manuscript explicitly narrows the study to mechanism demonstrations, so this is a declared limitation rather than a contradiction, but the abstract and contribution language should remain consistently case-specific.

Evidence:

- The taxonomy says that six classes are tested in the validation run, with one validation scenario listed for each class (Section 3 and `spec/taxonomy.md`).
- The manuscript states: “Rates from one probe per mechanism are mechanism demonstrations with stated resolved counts, not population estimates” (Discussion, Validity statements).
- The manuscript states: “The subject model under test is `claude-sonnet-4-6`” and that the validation runs use TF-IDF cosine similarity (Section 3.3).
- The conclusion limits findings to “the evaluated conditions” and calls for broader scenarios and cross-model evaluation.

**Recommendation:** Keep all headline claims explicitly bounded to the named scenarios, subject model, and TF-IDF condition; avoid wording that implies six established, general mechanisms or model-independent mitigation efficacy.

### [METHODOLOGY-003] Canonical contamination scoring does not reliably measure asserted contamination

- **Severity:** MINOR
- **Category:** metrics
- **Location:** paper/v3/main.tex, Sections 3.4, 4.2, 4.5, and Discussion/Validity statements; spec/metrics.md, Verdict resolution
- **Confidence:** 0.99
- **Reported by:** methodology

The primary deterministic scorer matches forbidden regexes against response text, so it detects mention rather than whether the model asserted the contaminated proposition. Judge disagreement is converted to unresolved status and excluded from rates. This leaves 52 of 350 audit rounds excluded and prevents the reported machine-only rates from serving as validated estimates of contamination. The manuscript acknowledges this limitation, but the provenance, staleness, and seeded-recursion headline results should be presented as machine-resolved case outcomes rather than validated contamination rates.

Evidence:

- The scoring rule says that a regex match yields `contaminated`, while no match yields provisional `clean`; disagreement becomes `needs_human_review` and is excluded from both numerator and denominator (Section 3.4).
- The paper reports 52 of 350 rounds requiring human review and states that no human verdicts are available (Section 4.2).
- The manuscript explicitly says: “Regex scoring detects mention, not assertion” and that the correction bundle records “0 adjudications and 0 two-adjudicator consensuses” (Discussion, Validity statements).
- `spec/metrics.md` confirms that all `needs_human_review` artifacts are excluded from rates.

**Recommendation:** Report the relevant results as canonical machine-only outcomes with unresolved exclusions, and do not describe them as validated contamination rates until the specified blinded independent adjudication is completed. Preserve the assertion-aware tier as a separate analysis rather than treating clean regex outcomes as ground truth.

### [METHODOLOGY-004] The provenance result is confounded by bundled metadata and raw-text availability

- **Severity:** MINOR
- **Category:** experimental-design
- **Location:** paper/v3/main.tex, Section 4.5 and Discussion/Validity statements; spec/configs.yaml, arm_provenance and arm_raw
- **Confidence:** 0.99
- **Reported by:** methodology

The provenance-tag arm changes source, age, and domain metadata together, and the raw-fidelity arm retains the sentence explicitly identifying the assistant as the source. Therefore the five clean outcomes in those arms cannot isolate provenance tagging as the causal intervention or establish that summarization alone caused provenance collapse. The paper identifies this confound, so it is a declared limitation; nevertheless, the abstract's wording should not imply an isolated provenance or summarization effect.

Evidence:

- The paper states that the provenance tag carries `source`, `age`, and `domain` together and calls this “an implementation confound” (Section 4.5).
- The paper states that raw fidelity retains the sentence “the assistant suggested that Maria could try...” and that the two arms are alternative interventions on the same case (Section 4.5).
- `spec/configs.yaml` defines `arm_provenance` by changing provenance to tagged while retaining summarized fidelity, and `arm_raw` by changing fidelity to raw while retaining untagged provenance.
- The manuscript's validity statements say: “The provenance arm is confounded: its tag emits source, age, and domain together.”

**Recommendation:** Describe the result narrowly as a case-specific association under bundled interventions. Do not attribute the effect uniquely to source tags or summarization loss; use the planned pure-factor provenance arms before making that causal claim.

### [METHODOLOGY-005] The proposed contradiction-preservation safeguard has no efficacy evaluation

- **Severity:** MINOR
- **Category:** controls-and-ablations
- **Location:** paper/v3/main.tex, Section 4.6 and Conclusion; spec/configs.yaml, arm_gate_preserve_pairs; spec/gate-family.yaml
- **Confidence:** 0.99
- **Reported by:** methodology

The manuscript proposes preserving contradiction pairs after relevance filtering, but the supplied configuration marks this arm as a next-run experiment and the paper reports no dedicated repeated evaluation. The seeded-recursion observation supports a failure mode of the tested gate implementation, not efficacy of the proposed safeguard. The manuscript correctly states this limitation, so the safeguard must remain a proposal rather than a mitigation result.

Evidence:

- The paper states: “The contract is implemented and unit-tested, but has not yet been evaluated in a dedicated repeated run, so it is a safeguard proposal rather than an efficacy result” (Section 4.6).
- `spec/configs.yaml` labels `arm_gate_preserve_pairs` as “Next-run experimental” and “not a v0.2 result.”
- `spec/gate-family.yaml` defines the contradiction-pair test as a future gate-family fixture requiring both memories to remain after gating.

**Recommendation:** Keep contradiction preservation explicitly labeled as untested design rationale. Do not include it among demonstrated mitigation controls until the required repeated gate-family experiment is run and reported.

### [REPO-CONSISTENCY-004] The full-benchmark plan is explicitly not an executed result and cannot support broader validation claims

- **Severity:** MINOR
- **Category:** scope
- **Location:** spec/full-benchmark.plan.yaml; spec/full-benchmark-candidates.yaml; src/full_benchmark.py; tests/test_adjudication.py
- **Confidence:** 0.97
- **Reported by:** repo-consistency

The manuscript generally labels the full benchmark as future work, and the supplied plan confirms that it is not executable evidence: the plan sets max_api_calls to 0, the candidate registry is empty, and the dry-run tests expect missing probes, controls, approvals, and utility oracles. Any interpretation of the planned 60-probe benchmark as completed evidence would be unsupported; this is a scope boundary rather than a contradiction in the current conclusion.

Evidence:

- spec/full-benchmark.plan.yaml: execution.max_api_calls is 0 and lists planned models, backends, baselines, and scenarios.
- spec/full-benchmark-candidates.yaml: “candidates: []” and states that human approval is required before execution.
- src/full_benchmark.py: main rejects API execution with “API execution is not implemented; inspect the dry-run coverage and estimate first.”
- tests/test_adjudication.py, test_full_benchmark_plan_dry_run: expects ready_for_execution to be False, 25 missing probes, 25 missing controls, 60 missing approvals, and zero utility oracles.
- paper/v3/main.tex §6, Future-work contract: explicitly says the remaining manifests and authorized execution “are not results and are not used by any claim in this paper.”

**Recommendation:** Retain the explicit future-work qualification and ensure no abstract, conclusion, README summary, or generated report presents the planned full benchmark as executed evidence.

### [REPRODUCIBILITY-003] The presupposition-capture gate claim is not auditable from the supplied files

- **Severity:** MINOR
- **Category:** evidence
- **Location:** paper/v3/main.tex, Section 5.5; evidence/20260713T084130Z/defects.md, “Gate amplification”; evidence/20260713T191740Z/validation_report.md, “Retrieval assertions” and “Relevance-gate observability”
- **Confidence:** 0.95
- **Reported by:** reproducibility

The paper attributes the seeded-recursion failure to logged gate decisions that retained the assistant write-back and discarded the premise-denying user context. The supplied v0.2 and v0.3 files contain aggregate reports and verdicts, but no per-artifact response or gate-decision JSON. The aggregate v0.3 report establishes that the gate retrieval assertion failed on CB-VAL-009 in five repetitions, but it does not independently expose the quoted gate rationales or the corresponding subject responses.

Evidence:

- paper/v3/main.tex, Section 5.5: “The gate's own logged decisions” supposedly state that the contaminated write-back was relevant and the user ground truth was irrelevant.
- evidence/20260713T084130Z/defects.md: reports the quoted gate rationales, but is an authored defect report rather than the underlying gate artifact.
- evidence/20260713T191740Z/validation_report.md: CB-VAL-009 × arm_gate has `must_include_seed_ids=False` and `must_preserve_conflict_pair=False` for all five repetitions, but the supplied file does not include the underlying decision records or responses.
- README.md: says raw prompts, injected memories, gate decisions, and responses are in each evidence directory, but those files are absent from the supplied artifact inventory.

**Recommendation:** Either include the underlying gate-decision and response artifacts or narrow the result to the auditable statement that the gate's retrieval assertions failed for all five seeded-recursion repetitions and that four of five response verdicts were machine-resolved contaminated, with one unresolved.

### [REPRODUCIBILITY-004] The causal interpretation of raw fidelity preserving provenance is not established

- **Severity:** MINOR
- **Category:** causal_inference
- **Location:** paper/v3/main.tex, Abstract; Section 5.4 “Attribution: what the cells support”; evidence/20260713T191740Z/validation_report.md, Config comparison
- **Confidence:** 0.93
- **Reported by:** reproducibility

The five clean machine-resolved outcomes for arm_raw and arm_provenance support a case-specific association, but they do not establish that provenance information was lost specifically because of summarization. The manuscript itself acknowledges that the two interventions are alternative interventions on the same case and that the provenance tag bundles source, age, and domain. The wording “consistent with” is appropriately cautious, but the intended claim as stated is stronger than the evidence if read causally.

Evidence:

- paper/v3/main.tex, Abstract: “tags and raw fidelity each yielded five machine-resolved clean outcomes, consistent with preserving source information that was lost during summarization in this case.”
- paper/v3/main.tex, Section 5.4: “The two arms are alternative interventions on the same case, not independent replications of that explanation.”
- paper/v3/main.tex, Section 5.4: “The provenance tag as implemented carries age and domain metadata ... The tag bundles three annotations.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: `provenance_error_rate` is 0.0 for arm_provenance and arm_raw, while provenance and staleness scoring also contain unresolved cases elsewhere.

**Recommendation:** Use the narrower wording: “In this scenario, raw fidelity and provenance tags each produced five machine-resolved clean outcomes; the raw-fidelity result is compatible with, but does not identify, summarization as the cause of the provenance error.”

### [STATISTICS-002] No formal statistical comparison supports mitigation or configuration-ranking claims

- **Severity:** MINOR
- **Category:** statistics
- **Location:** paper/v3/main.tex, §5.1 Table matrix and §5.3–§5.5
- **Confidence:** 0.91
- **Reported by:** statistics

The manuscript compares configurations and uses language such as “governed cleaner than naive,” but does not apply a paired comparison, randomization test, or other statistical procedure, nor does it report a standardized effect size for the repeated cells. With only one hand-authored probe per mechanism, formal population inference would be weak, but the comparison should either be explicitly case-level/descriptive or supported by an appropriate pre-specified analysis in a larger study.

Evidence:

- paper/v3/main.tex, §5.1 Table matrix caption: “Acceptance check: governed < naive on semantic_drift and scope_bleed.”
- paper/v3/main.tex, §5.3: “This supports the provenance finding in the machine-resolved tier, but does not substitute for the pending blinded human adjudications.”
- paper/v3/main.tex, §5.4: “This case motivates the design proposal ... [but] is a safeguard proposal rather than an efficacy result.”
- paper/v3/main.tex, §5.3: “The corresponding contamination proportions are 4/5 ... and 0/5 ...; these intervals are descriptive at validation scale, not population estimates.”

**Recommendation:** Keep configuration comparisons explicitly descriptive and case-specific, or pre-specify paired tests and effect sizes for the successor study. Avoid ranking controls or claiming efficacy beyond the observed scenarios.

### [STATISTICS-003] Replication count does not provide independent scenario-level replication

- **Severity:** MINOR
- **Category:** statistics
- **Location:** paper/v3/main.tex, Abstract and §6.1 Validity statements
- **Confidence:** 0.99
- **Reported by:** statistics

The five repetitions are repeated model calls for the same scenario/configuration cells, not independent scenarios or subject models. Consequently, the apparent five-trial support cannot establish robustness across prompts, models, or deployments. The artifact already declares this limitation at an appropriate strength; it should remain adjacent to the repeated-rate claims and not be diluted by the abstract’s improvement wording.

Evidence:

- paper/v3/main.tex, Abstract: “These are within-scenario observations, not estimates of real-world prevalence or model-independent mitigation efficacy.”
- paper/v3/main.tex, §6.1: “One subject model cannot establish model-independent behavior ... Rates from one probe per mechanism are mechanism demonstrations with stated resolved counts, not population estimates.”
- paper/v3/main.tex, §6.1: “Temperature~0 reduces but does not remove output variance, observed directly within this run on byte-identical prompts.”
- report/FINAL-AUDIT.md, Scientific readiness: “Repeated calls do not add scenario diversity.”

**Recommendation:** Retain the declared limitation and use narrow wording such as “in five repetitions of this scenario under this model/backend,” rather than implying independent replication or general efficacy.

## Recommended changes

- **ADVERSARIAL-001** — Provide the complete frozen CB-*.json raw artifact files, or remove claims that depend on independently inspecting and recomputing responses, retrievals, and gate decisions. The release should also include a manifest proving that every artifact hash in verdicts.json maps to a supplied file. (files: Files provided; README.md, section 'Paper and evidence'; src/adjudication.py::_artifact_index; src/metrics.py::gate_observability and retrieval scoring)
- **REPO-CONSISTENCY-001** — Supply the exact frozen evidence directories, scenario manifests, verdicts, reports, and correction/adjudication files referenced by the manuscript, or remove the numerical results and restrict the paper to claims supported by the supplied code and specifications. (files: paper/v3/main.tex, Abstract; §5, Table 1 footnote and §5.3; README.md, “Paper and evidence”)
- **ADVERSARIAL-002** — Narrow the headline to: the study defines six candidate mechanisms and obtains within-scenario evidence for provenance, scope, and selected retrieval/gate behaviors; it does not empirically establish response degradation for all six mechanisms. (files: paper/v3/main.tex, abstract; Sections 3, 5.2, 5.3, 5.5, and Conclusion)
- **ADVERSARIAL-004** — Describe CB-VAL-009 narrowly as a seeded contradictory-record/gate-presupposition test. Do not use it as direct evidence that the system's own generated responses cause recursive contamination unless a genuine generated-response write-back experiment is supplied. (files: paper/v3/main.tex, Section 5.2 'Seeded recursion (CB-VAL-009)'; scenarios/validation/cb-val-009-recursive-seeded.yaml; src/harness.py::run_pair)
- **ADVERSARIAL-005** — Include the referenced correction files in the frozen release and verify their hashes, or remove the v0.3.1 lineage and correction claims from the manuscript and README. (files: README.md, evidence table; paper/v3/main.tex, Table 1 and Section 5.3; supplied file inventory)
- **ARCHIVAL-001** — Distribute the frozen evidence artifacts with the archival release, or provide a persistent archive link and exact file manifest/hashes for every evidence release used by the paper. Do not rely solely on the mutable repository path. (files: README.md, “Paper and evidence”; paper/v3/main.tex, Sections 5.1, 5.3, and 5.4)
- **ARCHIVAL-002** — Record the exact commit SHA and archive checksum for each evidence release in the manuscript and archival metadata. Ensure the DOI resolves to an immutable archive containing those exact versions, and cite the version-specific DOI or SWHID where available. (files: README.md, “Quick start” and “Paper and evidence”; docs/REPRODUCTION.md, “Prerequisites” and “What to compare”; paper/v3/main.tex, Table 2 and Section 5.3)
- **ARCHIVAL-006** — Include the exact gate-decision records and corresponding response artifacts, with immutable hashes, in the archival evidence package. Preserve the current narrow scope: one seeded-recursion scenario and one implementation, not relevance gates generally. (files: paper/v3/main.tex, Section 5.6, “The gate amplified seeded recursion”; README.md, “Paper and evidence”)
- **CITATIONS-001** — Reconcile the accounting by distinguishing scenario-configuration cells, scored rounds, and extra recursive subject calls; state the exact denominator for the 52 unresolved cases and recompute the reported percentage. (files: paper/v3/main.tex, Section 4.2 'Repeated-evaluation audit and scoring defects', and abstract)
- **CITATIONS-002** — Provide the immutable evidence releases and the code/manifests needed to regenerate Tables 1–4, or explicitly label the reported empirical values as claims verified only by an external repository rather than by the submitted artifact. (files: paper/v3/main.tex, Section 4 'Ablation Study', footnote to the ablation description; Sections 4.2 and 4.4)
- **EVIDENCE-001** — Narrow the headline claim to: “We define six candidate mechanisms and operationalize each with a falsifiable scenario criterion; this pilot directly observes contamination in only a subset of those cases.” (files: paper/v3/main.tex, Abstract; §3 taxonomy; §5.3 repeated audit; Conclusion)
- **METHODOLOGY-001** — Provide the immutable v0.2/v0.3/v0.3.1 run artifacts, including raw prompts, injected memories, responses, retrieval assertions, judge outputs, verdicts, hashes, and run metadata; otherwise label the numerical results and derived claims as unverified and restrict the conclusions to the scenario specifications and methodological proposal. (files: paper/v3/main.tex, Section 4, footnote and Sections 4.1–4.4; files listed in the artifact manifest)
- **REPO-CONSISTENCY-002** — Include the nine validation/control manifests used for the reported runs, including their expected patterns, retrieval assertions, and scoring rules. If they are intentionally excluded, state that the supplied artifact is code-only and withdraw execution-based claims. (files: src/harness.py, load_scenarios and VALIDATION_SCENARIO_GLOBS; README.md, “Repository layout”; paper/v3/main.tex, §4 and §5)
- **REPO-CONSISTENCY-003** — Provide the exact gate-decision logs, responses, verdicts, artifact hashes, and pending review queue used for these statements. Until then, narrow the claims to “the implementation supports logging and scoring of these outcomes” and “the proposed failure mode is illustrated by the code/test fixture,” not observed benchmark findings. (files: paper/v3/main.tex, Abstract; §5.3; §5.4; §5.5; README.md, “Paper and evidence”)
- **REPRODUCIBILITY-001** — Supply the frozen raw artifacts referenced by README.md, including every response, prompt, injected memory, retrieval trace, and gate decision; record the exact commit, Python and dependency versions, model identifiers, configuration hashes, and any relevant seeds; and provide a lockfile or container for the reported release. Until then, restrict reproducibility claims to recomputation of the supplied verdict aggregates. (files: README.md, “Paper and evidence” and “Usage”; evidence/20260713T191740Z/run_meta.json; evidence/20260713T191740Z/verdicts.json; requirements.txt; docs/REPRODUCTION.md, “Prerequisites” and “What to compare”)
- **REPRODUCIBILITY-002** — Narrow the claim to: “We define six candidate mechanisms and obtain case-specific retrieval or response evidence for some of them; this pilot does not establish that all six degrade responses.” Treat semantic drift as a retrieval-layer observation, and describe summarization loss and natural recursion as unvalidated or null-result probes. (files: paper/v3/main.tex, Abstract; Sections 3, 5.3, 5.5, and Conclusion; evidence/20260713T191740Z/validation_report.md)
- **STATISTICS-001** — Report numerator, denominator, and an uncertainty interval for every headline configuration rate, or restrict the claims to the displayed per-cell counts and explicitly label all aggregate rates as descriptive pilot summaries. Do not describe the rates as general mitigation improvements without this qualification. (files: paper/v3/main.tex, §5.3 and Table repeated; evidence/20260713T191740Z/validation_report.md, Config comparison)

_Veritas Gate never modifies the artifact it evaluates; these actions are advisory._

## Model usage

| Model | Calls | Input tokens | Output tokens | Cost |
| --- | --- | --- | --- | --- |
| gpt-5.6-luna | 8 | 864,982 | 30,521 | 1.3864 USD |
| **Total** | 8 | 864,982 | 30,521 | **1.3864 USD** |

Cost is estimated from the rates configured when the run happened. It is not a billing record.

## Evaluation metadata

- Run id: `2026-09-25T192432Z`
- Veritas version: 0.1.0
- Profile: scientific-paper (version 1)
- Artifact: contam-bench (document)
- Artifact commit: 858ce8c1cec77481b1c719a4d8298ced414e19c8
- Started: 2026-09-25T19:24:32.492718+00:00
- Finished: 2026-09-25T19:29:49.628511+00:00

### Models

| Role | Provider | Model |
| --- | --- | --- |
| default | openai | gpt-5.6-luna |
| adversarial | openai | gpt-5.6-luna |
| meta | google | gemini-3.1-pro |

### Prompt versions

- `adversarial.md`: `523b7b4fa9433800`
- `archival.md`: `b20751914f995ada`
- `citations.md`: `f0404eec2c6bb4d7`
- `evidence.md`: `0fd77ba95c305c1d`
- `methodology.md`: `6b0ed709c203b60e`
- `repo_consistency.md`: `a9a4f91beeebdcca`
- `reproducibility.md`: `04d77cbae354e602`
- `statistics.md`: `ba3f034e5e808214`

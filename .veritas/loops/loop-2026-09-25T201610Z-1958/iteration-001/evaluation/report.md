# Veritas Gate Report

**Gate:** `REVISE` (exit code 2)

## Executive summary

8 judges and 6 checks produced 30 consolidated findings (0 critical, 9 major, 21 minor, 0 info). Failing checks: citability, claim-graph.

## Gate result

| Severity | Count |
| --- | --- |
| Critical | 0 |
| Major | 9 |
| Minor | 21 |
| Info | 0 |

Policy decisions:

- 9 major finding(s) exceed the limit of 0.
- 1 accepted risk(s) no longer match any finding or have expired: category=reproducibility location=evidence/20260713T191740Z

## Blocking findings

### [ADVERSARIAL-001] Frozen verdicts are inconsistent with the supplied scenario manifests

- **Severity:** MAJOR
- **Category:** reproducibility / artifact discrepancy
- **Location:** scenarios/validation/cb-val-003-scope-bleed.yaml (`scoring.judge.enabled: true`); evidence/20260713T191740Z/verdicts.json, all CB-VAL-003 records; src/judge.py, `score_artifact`; evidence/20260713T191740Z/validation_report.md, `judge_call_counts` and per-scenario verdict table
- **Confidence:** 0.99
- **Reported by:** adversarial

The current CB-VAL-003 manifest enables an LLM judge, but every CB-VAL-003 round in both supplied frozen verdict files has `judge: null` and is resolved by the deterministic pass alone. Under the supplied `src/judge.py`, `scoring.judge.enabled` causes a judge call for every such round. Therefore the published evidence cannot be regenerated from the supplied manifest and scoring code without changing either the manifest, the evidence, or the scoring pipeline. This directly affects the scope-bleed response-layer result and the claimed 175 judge calls in the repeated audit.

Evidence:

- The CB-VAL-003 manifest states `judge: enabled: true` and supplies a judge question.
- The repeated-evidence verdict records for CB-VAL-003 show deterministic verdicts but `"judge": null` for every configuration and repetition.
- `src/judge.py` calls `judge_pass` whenever `judge_config.get("enabled")` is true.
- The repeated report claims 175 judge calls, while its CB-VAL-003 records contain no judge verdicts.

**Recommendation:** Freeze and publish the exact scenario manifests used to generate the evidence, or regenerate the frozen verdicts from the supplied manifests. Reconcile the per-scenario judge records, judge-call counts, and report before relying on the scope-bleed response results.

### [ADVERSARIAL-002] Gate-cost reporting uses incompatible retrieval denominators

- **Severity:** MAJOR
- **Category:** metrics / reporting
- **Location:** paper/v3/main.tex, §6 `The two-layer dissociation persists` / §7 gate architecture; evidence/20260713T191740Z/validation_report.md, `Relevance-gate observability`; src/metrics.py, `gate_observability`
- **Confidence:** 0.98
- **Reported by:** adversarial

The paper reports 135 gate calls over 100 gated retrievals, yielding 1.35 calls per gated retrieval. The supplied repeated validation report instead states 350 retrievals and a mean of 0.3857 gate calls per retrieval. The implementation explains the discrepancy: `gate_observability` appends diagnostics for all retrievals, including configurations with no gate, while summing gate calls only for gated configurations. Thus the report's displayed mean is not the claimed per-gated-retrieval cost, and the paper and generated report are not reporting the same metric.

Evidence:

- The paper states: `135 gate calls over 100 gated retrievals, or 1.35 calls per gated retrieval`.
- The frozen report states: `retrievals: 350`, `observed gate calls: 135`, and `mean gate calls per retrieval: 0.3857`.
- `src/metrics.py` appends every `retrieval_diagnostics` record to `diagnostics`, but only gated records contribute to `by_query_family` gate-call totals.

**Recommendation:** Define the denominator explicitly and make the generated report and manuscript use the same quantity. Separate total retrievals from gated retrievals, and recompute all displayed gate-cost statistics from the corrected aggregation.

### [ADVERSARIAL-004] The headline response-level scope result is based on a brittle lexical detector in the supplied evidence

- **Severity:** MAJOR
- **Category:** measurement validity
- **Location:** paper/v3/main.tex, §5.5 `Attribution: what the cells support`; evidence/20260713T191740Z/verdicts.json, CB-VAL-003 records; evidence/20260713T191740Z/defects.md, D6; scenarios/validation/cb-val-003-scope-bleed.yaml
- **Confidence:** 0.97
- **Reported by:** adversarial

The scope-bleed response comparison is treated as a contamination result, but the relevant evidence is deterministic regex scoring, and the artifact itself documents that the `permit delays?` hit is stochastic even for byte-identical prompts. The supplied scope-bleed records have no judge verdicts, despite the manifest enabling one. Consequently, the reported 4/5 versus 0/5 response separation is not independently checked for assertion versus mention and may reflect detector behavior rather than actual contamination.

Evidence:

- The paper reports `naive resolved one clean and four contaminated repetitions, whereas namespacing resolved five clean and zero contaminated repetitions`.
- The CB-VAL-003 verdict records show only deterministic verdicts and `judge: null`.
- The defect report states that the `permit delays?` pattern fired under naive but not under byte-identical prompts and that temperature-0 calls are not bit-reproducible.
- The scoring specification defines contamination as any regex match, while the paper acknowledges regex scoring detects mention rather than assertion.

**Recommendation:** Treat this result as a deterministic-pattern observation, not a validated response-contamination effect, until the exact evidence is rescored with the enabled judge or independently adjudicated under an assertion-aware rubric.

### [ARCHIVAL-001] The DOI is not demonstrably the version containing the reported results

- **Severity:** MAJOR
- **Category:** identity and archival
- **Location:** CITATION.cff; README.md, “Paper and evidence” and “Citation”; paper/v3/main.tex, §5 and Table 2
- **Confidence:** 0.88
- **Reported by:** archival

A DOI is provided, but the artifact does not establish whether it resolves to the exact v0.3/v0.3.1 source and evidence versions described in the paper, rather than a concept record or another/latest release. The paper's headline results depend on separately named v0.2, v0.3, and v0.3.1 releases, but no version-specific DOI or archived manifest/hash is supplied for those releases.

Evidence:

- CITATION.cff: `doi: 10.5281/zenodo.22859806` and `repository-code: https://github.com/arananet/contam-bench`.
- README.md, “Paper and evidence”: the reported material is split across `v0.3.1-evidence-corrections`, `v0.3-repeated-ablation`, and `v0.2-ablation`.
- paper/v3/main.tex, Table `lineage`: the paper distinguishes `v0.2-ablation`, `v0.3-repeated-ablation`, and `v0.3.1-evidence-corrections`, but gives only tag names, not version-specific DOI records or commit hashes.
- README.md, “Citation”: `This repository is archived on Zenodo with the following DOI: [10.5281/zenodo.22859806]`; the artifact itself does not show what exact repository contents that DOI archives.

**Recommendation:** Create or cite immutable, version-specific archive records for the paper source and each evidence release, and state explicitly which DOI/version contains the numbers reported in the manuscript. Include a manifest recording the commit/tag and hashes of the paper and evidence directories.

### [ARCHIVAL-002] Evidence and code references are not pinned to immutable content outside the mutable Git host

- **Severity:** MAJOR
- **Category:** reference immutability
- **Location:** README.md, “Paper and evidence,” “Quick start,” and “Citation”; docs/REPRODUCTION.md, §§1–3; paper/v3/main.tex, §5 footnote and Table 2
- **Confidence:** 0.94
- **Reported by:** archival

The manuscript and reproduction instructions identify evidence by repository-relative paths and annotated tag names, and the paper links to the repository root. They do not provide commit SHAs, release-specific archive URLs, or DOI links for the evidence directories. A future reader could therefore retrieve different contents if the repository, tags, branches, or directory contents change.

Evidence:

- README.md, “Paper and evidence”: evidence is referenced as `evidence/20260713T191740Z/`, `evidence/20260713T084130Z/`, and `evidence/20260710T143558Z/`, with tags such as `v0.3-repeated-ablation`.
- README.md, “Quick start”: `git clone https://github.com/arananet/contam-bench.git` and subsequent commands operate on the checkout without specifying a release commit.
- docs/REPRODUCTION.md, §2: readers are told to “Choose one scenario and configuration from a frozen evidence release” and to “Record the release directory ... and commit SHA before running anything,” but the paper itself does not supply those SHAs.
- paper/v3/main.tex, §5 footnote: `Complete run artifacts are published at evidence/20260713T084130Z ... frozen at tag v0.2-ablation`; a tag name is supplied, but no commit SHA or external archive object is given.
- paper/v3/main.tex, abstract and conclusion: the code is linked only as `https://github.com/arananet/contam-bench`.

**Recommendation:** Replace bare repository and relative-directory citations with release-specific immutable references: commit SHA plus archived DOI/object URL, and provide a release manifest mapping every table to exact artifact hashes.

### [CITATIONS-001] Repeated-audit denominator contradicts the stated experimental design

- **Severity:** MAJOR
- **Category:** internal consistency / reproducibility
- **Location:** paper/v3/main.tex, Section 4, paragraphs beginning “Table 1 is the frozen v0.2 single-run ablation” and “Fifty-two of the 350 rounds”; Section 4 opening paragraph; Table 4 (tab:repeated)
- **Confidence:** 0.99
- **Reported by:** citations

The paper states that the repeated audit used nine scenarios, seven configurations, and five repetitions, which implies 315 scored rounds, but it repeatedly reports 350 scored rounds and derives the 14.9% review rate from that denominator. The manuscript does not identify a tenth scenario or otherwise explain the additional 35 rounds. The reported subject-call total also conflicts with the stated nine-by-seven design: 70 subject calls would correspond to ten configurations/scenarios per repetition rather than 63 calls for nine scenarios and seven configurations. This makes the audit denominator, review rate, and call accounting unreproducible as written.

Evidence:

- “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds” (paper/v3/main.tex, Section 4)
- “Fifty-two of the 350 rounds (14.9%) required human review” (paper/v3/main.tex, Section 4)
- “the run reported here executes nine scenarios ... against seven configurations” (paper/v3/main.tex, Section 4)
- Nine scenarios × seven configurations × five repetitions = 315 rounds, whereas the manuscript reports 350.
- “The repeated audit used 660 API calls: 350 subject calls, 135 gate calls, and 175 judge calls” (paper/v3/main.tex, Section 4)

**Recommendation:** Reconcile the scenario/configuration/repetition counts with the supplied aggregates and call logs. Identify any additional scenario or round if one exists, or correct the 350-round and API-call totals and recompute the review percentage, audit summaries, and related claims.

### [CLAIM-001] Unsupported claim: The pilot establishes a general mitigation architecture or a general mitigation 

- **Severity:** MAJOR
- **Category:** claims/unsupported
- **Location:** paper/v3/main.tex, §5.5, §6, Discussion, and Conclusion
- **Confidence:** 0.90
- **Reported by:** claim-graph

The artifact explicitly disclaims this stronger claim. The supported claim is only that the pilot motivates contract-level safeguards and identifies case-specific observations.

Evidence:

- paper/v3/main.tex, §6: “The ablation motivates constraints, not an efficacy ordering.”
- paper/v3/main.tex, Discussion: “Seven single-control arms are seven points, not a curve.”
- paper/v3/main.tex, Conclusion: “They motivate further tests of memory contracts, not a validated general mitigation architecture.”

**Recommendation:** Provide evidence for the claim or remove it.

### [METHODOLOGY-001] The main experiment lacks enough implementation detail for independent reproduction

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Sections 4.3 “Models and determinism” and 5 “Ablation Study”; spec/configs.yaml, models and retrieval sections
- **Confidence:** 0.91
- **Reported by:** methodology

The manuscript identifies the subject, judge, gate, temperature, retrieval family, and k, but does not specify the TF-IDF preprocessing/vectorization configuration, tie-breaking and ranking behavior, prompt templates, API/model revision identifiers, or exact memory-block construction. These details can affect which memories are retrieved and how responses are scored. The supplied artifact also contains no implementation files or run artifacts from which these choices can be recovered. This is material because the paper presents repeated-cell outcomes and claims that every number is recomputable.

Evidence:

- paper/v3/main.tex, Section 4.3: “The reported validation runs use TF-IDF cosine similarity” and “claude-sonnet-4-6 at temperature 0”; it does not specify vectorizer preprocessing or ranking details.
- spec/configs.yaml: `similarity: tfidf-cosine (scikit-learn TfidfVectorizer)` and `k: 4`, without tokenizer, normalization, vocabulary, tie-breaking, or version information.
- paper/v3/main.tex, Section 5: “Every number in this section is recomputable from those artifacts,” but the supplied files do not include the implementation or the cited evidence releases.

**Recommendation:** Report the exact retrieval implementation and versions, vectorizer/tokenization/normalization settings, tie-breaking, prompt templates, memory serialization, API/model revision identifiers, and provide the code or a complete executable release corresponding to the cited evidence tags.

### [REPRODUCIBILITY-001] Main experiment is not reproducible from a pinned environment or revision

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** requirements.txt; docs/REPRODUCTION.md §Prerequisites and §2; paper/v3/main.tex §Models and determinism and §Discussion and Limitations, Reproducibility
- **Confidence:** 0.98
- **Reported by:** reproducibility

The reproduction instructions install minimum-version dependencies from requirements.txt, which contains ranges such as `anthropic>=0.116`, `scikit-learn>=1.3`, and `pytest>=8.0`, but no lockfile, container, or exact resolved versions is supplied. The paper identifies model names and temperatures but does not identify the exact repository commit used for the reported evidence. A fresh rerun can therefore use different client, library, retrieval, or harness behavior, and the model/API outputs are acknowledged as nondeterministic. This blocks independent rerun of the headline seven-configuration repeated audit and its reported rates.

Evidence:

- requirements.txt specifies lower bounds rather than pinned versions: `anthropic>=0.116`, `PyYAML>=6.0`, `jsonschema>=4.0`, `scikit-learn>=1.3`, `fastembed>=0.5`, and `pytest>=8.0`.
- docs/REPRODUCTION.md §Independence requires a reviewer to record `the exact commit SHA`, but the supplied v0.3 evidence `run_meta.json` contains no commit field and paper/v3/main.tex does not identify a commit SHA for the reported release.
- paper/v3/main.tex §Discussion and Limitations, Reproducibility states: `Temperature~0 sampling reduces but does not guarantee bit-identical responses` and that independent external reproduction remains outstanding.

**Recommendation:** Archive an exact commit identifier with each evidence release and provide a lockfile, container, or complete resolved dependency manifest, including the API client version and retrieval dependencies. Preserve the existing nondeterminism caveat and report rerun comparisons against the frozen artifacts.

## Judge consensus

| Finding | Severity | Reported by | Consensus |
| --- | --- | --- | --- |
| ADVERSARIAL-001 | MAJOR | adversarial | single-source (low) |
| ADVERSARIAL-002 | MAJOR | adversarial | single-source (low) |
| ADVERSARIAL-004 | MAJOR | adversarial | single-source (low) |
| ARCHIVAL-001 | MAJOR | archival | single-source (low) |
| ARCHIVAL-002 | MAJOR | archival | single-source (low) |
| CITATIONS-001 | MAJOR | citations | single-source (low) |
| CLAIM-001 | MAJOR | claim-graph | single-source (low) |
| METHODOLOGY-001 | MAJOR | methodology | single-source (low) |
| REPRODUCIBILITY-001 | MAJOR | reproducibility | single-source (low) |
| ADVERSARIAL-003 | MINOR | adversarial | single-source (low) |
| ARCHIVAL-003 | MINOR | archival | single-source (low) |
| ARCHIVAL-004 | MINOR | archival | single-source (low) |
| CHECK-CITABILITY-001 | MINOR | check:citability | single-source (low) |
| CHECK-CITABILITY-002 | MINOR | check:citability | single-source (low) |
| CITATIONS-002 | MINOR | citations | single-source (low) |
| CITATIONS-003 | MINOR | citations | single-source (low) |
| EVIDENCE-001 | MINOR | evidence | single-source (low) |
| EVIDENCE-002 | MINOR | evidence | single-source (low) |
| METHODOLOGY-002 | MINOR | methodology | single-source (low) |
| METHODOLOGY-003 | MINOR | methodology | single-source (low) |
| METHODOLOGY-004 | MINOR | methodology | single-source (low) |
| REPO-CONSISTENCY-001 | MINOR | repo-consistency | single-source (low) |
| REPO-CONSISTENCY-002 | MINOR | repo-consistency | single-source (low) |
| REPRODUCIBILITY-002 | MINOR | reproducibility | single-source (low) |
| REPRODUCIBILITY-003 | MINOR | reproducibility | single-source (low) |
| STATISTICS-001 | MINOR | statistics | single-source (low) |
| STATISTICS-002 | MINOR | statistics | single-source (low) |
| STATISTICS-003 | MINOR | statistics | single-source (low) |
| STATISTICS-004 | MINOR | statistics | single-source (low) |
| STATISTICS-005 | MINOR | statistics | single-source (low) |

## Judge disagreements

No disagreements were recorded.

## Claim coverage

- Claims detected: 8 (8 major)
- Verified: 7
- Partially supported: 0
- Unsupported: 1
- Unverified: 0
- Evidence coverage: 87.5%

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

### [ADVERSARIAL-001] Frozen verdicts are inconsistent with the supplied scenario manifests

- **Severity:** MAJOR
- **Category:** reproducibility / artifact discrepancy
- **Location:** scenarios/validation/cb-val-003-scope-bleed.yaml (`scoring.judge.enabled: true`); evidence/20260713T191740Z/verdicts.json, all CB-VAL-003 records; src/judge.py, `score_artifact`; evidence/20260713T191740Z/validation_report.md, `judge_call_counts` and per-scenario verdict table
- **Confidence:** 0.99
- **Reported by:** adversarial

The current CB-VAL-003 manifest enables an LLM judge, but every CB-VAL-003 round in both supplied frozen verdict files has `judge: null` and is resolved by the deterministic pass alone. Under the supplied `src/judge.py`, `scoring.judge.enabled` causes a judge call for every such round. Therefore the published evidence cannot be regenerated from the supplied manifest and scoring code without changing either the manifest, the evidence, or the scoring pipeline. This directly affects the scope-bleed response-layer result and the claimed 175 judge calls in the repeated audit.

Evidence:

- The CB-VAL-003 manifest states `judge: enabled: true` and supplies a judge question.
- The repeated-evidence verdict records for CB-VAL-003 show deterministic verdicts but `"judge": null` for every configuration and repetition.
- `src/judge.py` calls `judge_pass` whenever `judge_config.get("enabled")` is true.
- The repeated report claims 175 judge calls, while its CB-VAL-003 records contain no judge verdicts.

**Recommendation:** Freeze and publish the exact scenario manifests used to generate the evidence, or regenerate the frozen verdicts from the supplied manifests. Reconcile the per-scenario judge records, judge-call counts, and report before relying on the scope-bleed response results.

### [ADVERSARIAL-002] Gate-cost reporting uses incompatible retrieval denominators

- **Severity:** MAJOR
- **Category:** metrics / reporting
- **Location:** paper/v3/main.tex, §6 `The two-layer dissociation persists` / §7 gate architecture; evidence/20260713T191740Z/validation_report.md, `Relevance-gate observability`; src/metrics.py, `gate_observability`
- **Confidence:** 0.98
- **Reported by:** adversarial

The paper reports 135 gate calls over 100 gated retrievals, yielding 1.35 calls per gated retrieval. The supplied repeated validation report instead states 350 retrievals and a mean of 0.3857 gate calls per retrieval. The implementation explains the discrepancy: `gate_observability` appends diagnostics for all retrievals, including configurations with no gate, while summing gate calls only for gated configurations. Thus the report's displayed mean is not the claimed per-gated-retrieval cost, and the paper and generated report are not reporting the same metric.

Evidence:

- The paper states: `135 gate calls over 100 gated retrievals, or 1.35 calls per gated retrieval`.
- The frozen report states: `retrievals: 350`, `observed gate calls: 135`, and `mean gate calls per retrieval: 0.3857`.
- `src/metrics.py` appends every `retrieval_diagnostics` record to `diagnostics`, but only gated records contribute to `by_query_family` gate-call totals.

**Recommendation:** Define the denominator explicitly and make the generated report and manuscript use the same quantity. Separate total retrievals from gated retrievals, and recompute all displayed gate-cost statistics from the corrected aggregation.

### [ADVERSARIAL-004] The headline response-level scope result is based on a brittle lexical detector in the supplied evidence

- **Severity:** MAJOR
- **Category:** measurement validity
- **Location:** paper/v3/main.tex, §5.5 `Attribution: what the cells support`; evidence/20260713T191740Z/verdicts.json, CB-VAL-003 records; evidence/20260713T191740Z/defects.md, D6; scenarios/validation/cb-val-003-scope-bleed.yaml
- **Confidence:** 0.97
- **Reported by:** adversarial

The scope-bleed response comparison is treated as a contamination result, but the relevant evidence is deterministic regex scoring, and the artifact itself documents that the `permit delays?` hit is stochastic even for byte-identical prompts. The supplied scope-bleed records have no judge verdicts, despite the manifest enabling one. Consequently, the reported 4/5 versus 0/5 response separation is not independently checked for assertion versus mention and may reflect detector behavior rather than actual contamination.

Evidence:

- The paper reports `naive resolved one clean and four contaminated repetitions, whereas namespacing resolved five clean and zero contaminated repetitions`.
- The CB-VAL-003 verdict records show only deterministic verdicts and `judge: null`.
- The defect report states that the `permit delays?` pattern fired under naive but not under byte-identical prompts and that temperature-0 calls are not bit-reproducible.
- The scoring specification defines contamination as any regex match, while the paper acknowledges regex scoring detects mention rather than assertion.

**Recommendation:** Treat this result as a deterministic-pattern observation, not a validated response-contamination effect, until the exact evidence is rescored with the enabled judge or independently adjudicated under an assertion-aware rubric.

### [ARCHIVAL-001] The DOI is not demonstrably the version containing the reported results

- **Severity:** MAJOR
- **Category:** identity and archival
- **Location:** CITATION.cff; README.md, “Paper and evidence” and “Citation”; paper/v3/main.tex, §5 and Table 2
- **Confidence:** 0.88
- **Reported by:** archival

A DOI is provided, but the artifact does not establish whether it resolves to the exact v0.3/v0.3.1 source and evidence versions described in the paper, rather than a concept record or another/latest release. The paper's headline results depend on separately named v0.2, v0.3, and v0.3.1 releases, but no version-specific DOI or archived manifest/hash is supplied for those releases.

Evidence:

- CITATION.cff: `doi: 10.5281/zenodo.22859806` and `repository-code: https://github.com/arananet/contam-bench`.
- README.md, “Paper and evidence”: the reported material is split across `v0.3.1-evidence-corrections`, `v0.3-repeated-ablation`, and `v0.2-ablation`.
- paper/v3/main.tex, Table `lineage`: the paper distinguishes `v0.2-ablation`, `v0.3-repeated-ablation`, and `v0.3.1-evidence-corrections`, but gives only tag names, not version-specific DOI records or commit hashes.
- README.md, “Citation”: `This repository is archived on Zenodo with the following DOI: [10.5281/zenodo.22859806]`; the artifact itself does not show what exact repository contents that DOI archives.

**Recommendation:** Create or cite immutable, version-specific archive records for the paper source and each evidence release, and state explicitly which DOI/version contains the numbers reported in the manuscript. Include a manifest recording the commit/tag and hashes of the paper and evidence directories.

### [ARCHIVAL-002] Evidence and code references are not pinned to immutable content outside the mutable Git host

- **Severity:** MAJOR
- **Category:** reference immutability
- **Location:** README.md, “Paper and evidence,” “Quick start,” and “Citation”; docs/REPRODUCTION.md, §§1–3; paper/v3/main.tex, §5 footnote and Table 2
- **Confidence:** 0.94
- **Reported by:** archival

The manuscript and reproduction instructions identify evidence by repository-relative paths and annotated tag names, and the paper links to the repository root. They do not provide commit SHAs, release-specific archive URLs, or DOI links for the evidence directories. A future reader could therefore retrieve different contents if the repository, tags, branches, or directory contents change.

Evidence:

- README.md, “Paper and evidence”: evidence is referenced as `evidence/20260713T191740Z/`, `evidence/20260713T084130Z/`, and `evidence/20260710T143558Z/`, with tags such as `v0.3-repeated-ablation`.
- README.md, “Quick start”: `git clone https://github.com/arananet/contam-bench.git` and subsequent commands operate on the checkout without specifying a release commit.
- docs/REPRODUCTION.md, §2: readers are told to “Choose one scenario and configuration from a frozen evidence release” and to “Record the release directory ... and commit SHA before running anything,” but the paper itself does not supply those SHAs.
- paper/v3/main.tex, §5 footnote: `Complete run artifacts are published at evidence/20260713T084130Z ... frozen at tag v0.2-ablation`; a tag name is supplied, but no commit SHA or external archive object is given.
- paper/v3/main.tex, abstract and conclusion: the code is linked only as `https://github.com/arananet/contam-bench`.

**Recommendation:** Replace bare repository and relative-directory citations with release-specific immutable references: commit SHA plus archived DOI/object URL, and provide a release manifest mapping every table to exact artifact hashes.

### [CITATIONS-001] Repeated-audit denominator contradicts the stated experimental design

- **Severity:** MAJOR
- **Category:** internal consistency / reproducibility
- **Location:** paper/v3/main.tex, Section 4, paragraphs beginning “Table 1 is the frozen v0.2 single-run ablation” and “Fifty-two of the 350 rounds”; Section 4 opening paragraph; Table 4 (tab:repeated)
- **Confidence:** 0.99
- **Reported by:** citations

The paper states that the repeated audit used nine scenarios, seven configurations, and five repetitions, which implies 315 scored rounds, but it repeatedly reports 350 scored rounds and derives the 14.9% review rate from that denominator. The manuscript does not identify a tenth scenario or otherwise explain the additional 35 rounds. The reported subject-call total also conflicts with the stated nine-by-seven design: 70 subject calls would correspond to ten configurations/scenarios per repetition rather than 63 calls for nine scenarios and seven configurations. This makes the audit denominator, review rate, and call accounting unreproducible as written.

Evidence:

- “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds” (paper/v3/main.tex, Section 4)
- “Fifty-two of the 350 rounds (14.9%) required human review” (paper/v3/main.tex, Section 4)
- “the run reported here executes nine scenarios ... against seven configurations” (paper/v3/main.tex, Section 4)
- Nine scenarios × seven configurations × five repetitions = 315 rounds, whereas the manuscript reports 350.
- “The repeated audit used 660 API calls: 350 subject calls, 135 gate calls, and 175 judge calls” (paper/v3/main.tex, Section 4)

**Recommendation:** Reconcile the scenario/configuration/repetition counts with the supplied aggregates and call logs. Identify any additional scenario or round if one exists, or correct the 350-round and API-call totals and recompute the review percentage, audit summaries, and related claims.

### [CLAIM-001] Unsupported claim: The pilot establishes a general mitigation architecture or a general mitigation 

- **Severity:** MAJOR
- **Category:** claims/unsupported
- **Location:** paper/v3/main.tex, §5.5, §6, Discussion, and Conclusion
- **Confidence:** 0.90
- **Reported by:** claim-graph

The artifact explicitly disclaims this stronger claim. The supported claim is only that the pilot motivates contract-level safeguards and identifies case-specific observations.

Evidence:

- paper/v3/main.tex, §6: “The ablation motivates constraints, not an efficacy ordering.”
- paper/v3/main.tex, Discussion: “Seven single-control arms are seven points, not a curve.”
- paper/v3/main.tex, Conclusion: “They motivate further tests of memory contracts, not a validated general mitigation architecture.”

**Recommendation:** Provide evidence for the claim or remove it.

### [METHODOLOGY-001] The main experiment lacks enough implementation detail for independent reproduction

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Sections 4.3 “Models and determinism” and 5 “Ablation Study”; spec/configs.yaml, models and retrieval sections
- **Confidence:** 0.91
- **Reported by:** methodology

The manuscript identifies the subject, judge, gate, temperature, retrieval family, and k, but does not specify the TF-IDF preprocessing/vectorization configuration, tie-breaking and ranking behavior, prompt templates, API/model revision identifiers, or exact memory-block construction. These details can affect which memories are retrieved and how responses are scored. The supplied artifact also contains no implementation files or run artifacts from which these choices can be recovered. This is material because the paper presents repeated-cell outcomes and claims that every number is recomputable.

Evidence:

- paper/v3/main.tex, Section 4.3: “The reported validation runs use TF-IDF cosine similarity” and “claude-sonnet-4-6 at temperature 0”; it does not specify vectorizer preprocessing or ranking details.
- spec/configs.yaml: `similarity: tfidf-cosine (scikit-learn TfidfVectorizer)` and `k: 4`, without tokenizer, normalization, vocabulary, tie-breaking, or version information.
- paper/v3/main.tex, Section 5: “Every number in this section is recomputable from those artifacts,” but the supplied files do not include the implementation or the cited evidence releases.

**Recommendation:** Report the exact retrieval implementation and versions, vectorizer/tokenization/normalization settings, tie-breaking, prompt templates, memory serialization, API/model revision identifiers, and provide the code or a complete executable release corresponding to the cited evidence tags.

### [REPRODUCIBILITY-001] Main experiment is not reproducible from a pinned environment or revision

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** requirements.txt; docs/REPRODUCTION.md §Prerequisites and §2; paper/v3/main.tex §Models and determinism and §Discussion and Limitations, Reproducibility
- **Confidence:** 0.98
- **Reported by:** reproducibility

The reproduction instructions install minimum-version dependencies from requirements.txt, which contains ranges such as `anthropic>=0.116`, `scikit-learn>=1.3`, and `pytest>=8.0`, but no lockfile, container, or exact resolved versions is supplied. The paper identifies model names and temperatures but does not identify the exact repository commit used for the reported evidence. A fresh rerun can therefore use different client, library, retrieval, or harness behavior, and the model/API outputs are acknowledged as nondeterministic. This blocks independent rerun of the headline seven-configuration repeated audit and its reported rates.

Evidence:

- requirements.txt specifies lower bounds rather than pinned versions: `anthropic>=0.116`, `PyYAML>=6.0`, `jsonschema>=4.0`, `scikit-learn>=1.3`, `fastembed>=0.5`, and `pytest>=8.0`.
- docs/REPRODUCTION.md §Independence requires a reviewer to record `the exact commit SHA`, but the supplied v0.3 evidence `run_meta.json` contains no commit field and paper/v3/main.tex does not identify a commit SHA for the reported release.
- paper/v3/main.tex §Discussion and Limitations, Reproducibility states: `Temperature~0 sampling reduces but does not guarantee bit-identical responses` and that independent external reproduction remains outstanding.

**Recommendation:** Archive an exact commit identifier with each evidence release and provide a lockfile, container, or complete resolved dependency manifest, including the API client version and retrieval dependencies. Preserve the existing nondeterminism caveat and report rerun comparisons against the frozen artifacts.

### [ADVERSARIAL-003] The provenance ablation does not isolate provenance

- **Severity:** MINOR
- **Category:** experimental design / confounding
- **Location:** spec/configs.yaml, `arm_provenance`; paper/v3/main.tex, §5.5 `Attribution: what the cells support`; evidence/20260713T084130Z/defects.md, D5
- **Confidence:** 0.99
- **Reported by:** adversarial

The arm presented as the provenance single-control arm changes more than provenance: tagged memories also expose age and domain. The paper itself acknowledges that the provenance arm resolved temporal staleness because the subject could see the age, so the five clean provenance outcomes cannot establish that source tags caused the improvement. This undermines the mechanism-isolation interpretation of the provenance result and also complicates comparisons with the raw-fidelity arm.

Evidence:

- `arm_provenance` is configured with `provenance: tagged`, while the tag format is documented as `[source: ... | age: ... | domain: ...]`.
- The paper states: `the provenance tag as implemented carries age and domain metadata ... so the provenance arm also resolved staleness because the subject discounted the 200-day-old fact by its visible age.`
- The paper nevertheless presents the arm as a single-control provenance intervention and reports five clean machine outcomes on the provenance probe.

**Recommendation:** Do not interpret the current arm as a pure provenance effect. Report it only as a bundled metadata intervention, or rerun with source-only, age-only, and domain-only factors before making mechanism-attribution claims.

### [ARCHIVAL-003] The CFF license field is ambiguous relative to the repository's split licensing

- **Severity:** MINOR
- **Category:** licensing
- **Location:** CITATION.cff; LICENSING.md; README.md, “License”
- **Confidence:** 0.96
- **Reported by:** archival

The citation metadata declares the work as CC-BY-4.0, while the licensing document assigns Apache-2.0 to code and CC-BY-4.0 to manuscript, figures, data, and evidence. This may be an intentional distinction, but the CFF field does not state that it applies only to content, so automated citation tools can report an incorrect license for the code repository.

Evidence:

- CITATION.cff: `license: CC-BY-4.0` alongside `repository-code: https://github.com/arananet/contam-bench`.
- LICENSING.md: `Code — harness, scripts, tests and any software ... Apache-2.0` and `Content — the manuscript, figures, data and evidence records: CC-BY-4.0`.
- README.md, “License”: the repository-level link is labeled `Apache 2.0`, without clarifying how it relates to the CFF license field.

**Recommendation:** Clarify the scope of the CFF license field and provide unambiguous per-component SPDX/license metadata, including the paper, data, figures, evidence, and code. Ensure the referenced `LICENSE` file is included in the archival release.

### [ARCHIVAL-004] The supplied source cannot be rebuilt or its bibliography checked from the listed files

- **Severity:** MINOR
- **Category:** citation metadata
- **Location:** paper/v3/main.tex, document ending; supplied file list
- **Confidence:** 0.98
- **Reported by:** archival

The manuscript invokes an external BibTeX database, but `references.bib` is not among the files supplied for evaluation. Consequently, the citations and bibliography cannot be reconstructed or checked from this artifact alone, reducing long-term citability of the source package.

Evidence:

- paper/v3/main.tex, final lines: `\bibliographystyle{plain}` followed by `\bibliography{references}`.
- The supplied file list contains `paper/v3/main.tex` but does not contain `paper/v3/references.bib` or another bibliography file.

**Recommendation:** Include the bibliography source and any required figures, styles, and build metadata in the archived source package, or provide a rendered paper whose references are independently readable.

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

### [CITATIONS-002] Several prior-work claims lack citations

- **Severity:** MINOR
- **Category:** citation completeness
- **Location:** paper/v3/main.tex, Section 2 (Related Work), paragraphs “Adversarial memory poisoning,” “Measurement of non-adversarial memory risk,” and “Retrieval noise and context failure”
- **Confidence:** 0.98
- **Reported by:** citations

The related-work discussion makes specific claims about prior work without attaching a citation, even though the citation rubric requires sources for claims about prior work and comparisons. In particular, it refers to “subsequent work” extending the attack surface, “complementary diagnosis work” finding that most failures stem from irrelevant retrieval, and “follow-on work” quantifying distracting effects, but no corresponding references are given at those sentences. These claims are therefore not traceable to the bibliography.

Evidence:

- “subsequent work has extended the attack surface.” (paper/v3/main.tex, Section 2, Adversarial memory poisoning)
- “Complementary diagnosis work finds most memory failures stem from irrelevant retrieval rather than memory construction.” (paper/v3/main.tex, Section 2, Measurement of non-adversarial memory risk)
- “follow-on work quantifies a passage's distracting effect as a graded severity measure.” (paper/v3/main.tex, Section 2, Retrieval noise and context failure)
- The surrounding paragraphs contain citations for other claims, but these three specific claims have no citation keys attached.

**Recommendation:** Add the specific source(s) supporting each claim, or narrow the wording to an uncited observation and remove the implication that an established prior result is being summarized.

### [CITATIONS-003] The provenance-arm confound limits attribution of the reported provenance effect

- **Severity:** MINOR
- **Category:** experimental design / attribution
- **Location:** paper/v3/main.tex, Section 4, subsection “Attribution: what the cells support”; Section 6, subsection “Validity statements”
- **Confidence:** 0.99
- **Reported by:** citations

The provenance intervention does not change provenance alone: its emitted tag also exposes age and domain. Consequently, the clean outcomes on the provenance probe cannot uniquely be attributed to source attribution or provenance preservation. The manuscript explicitly acknowledges this limitation, so this is reported as declared rather than as an undisclosed defect.

Evidence:

- “the provenance tag as implemented carries age and domain metadata ([source: user | age: 200d | domain: personal]), so the provenance arm also resolved staleness because the subject discounted the 200-day-old fact by its visible age.” (paper/v3/main.tex, Section 4)
- “The provenance arm is confounded: its tag emits source, age, and domain together, so its staleness result cannot be attributed to source attribution alone.” (paper/v3/main.tex, Section 6)

**Recommendation:** Retain the limitation prominently wherever the provenance result is summarized and avoid wording that attributes the full effect to provenance tagging alone; a pure-factor provenance arm is appropriately identified as future work.

### [EVIDENCE-001] The intended claim that the pilot exercises only a subset of the six mechanisms is contradicted by the artifact

- **Severity:** MINOR
- **Category:** scope/claim precision
- **Location:** AUTHOR'S INTENDED CLAIMS; paper/v3/main.tex, §3; tests/test_schema.py:test_v02_scenario_inventory; spec/taxonomy.md
- **Confidence:** 0.99
- **Reported by:** evidence

The intended claim says that “The pilot exercises a subset of them.” However, the manuscript states that “Six classes are tested in the validation run,” and the scenario inventory contains CB-VAL-001 through CB-VAL-006 for semantic drift, provenance collapse, scope bleed, temporal staleness, recursive contamination, and summarization loss. The manuscript does acknowledge that these are small pilot demonstrations rather than general validation, but “subset” is inaccurate for the six mechanisms named in the intended claim.

Evidence:

- paper/v3/main.tex, §3: “Six classes are tested in the validation run; a seventh is documented as experimental.”
- paper/v3/main.tex, §4: “The base corpus is eight hand-authored scenarios: six contamination probes, one per taxonomy class, plus two controls.”
- tests/test_schema.py:test_v02_scenario_inventory: expected inventory is CB-VAL-001..009, including six natural contamination probes and two recursive probes.
- spec/taxonomy.md: six classes are listed as tested validation scenarios: semantic_drift, provenance_collapse, scope_bleed, temporal_staleness, recursive, and summarization_loss.

**Recommendation:** Replace the intended wording with the narrower supported claim: “The pilot includes one hand-authored scenario for each of the six proposed mechanisms; these scenarios provide mechanism demonstrations rather than evidence of prevalence or general mitigation efficacy.”

### [EVIDENCE-002] The taxonomy is supported as a conceptual framework, but empirical support is uneven and should not be phrased as validation of every mechanism

- **Severity:** MINOR
- **Category:** claims/evidence alignment
- **Location:** AUTHOR'S INTENDED CLAIMS; paper/v3/main.tex, §§3, 5.3, 5.5, Discussion; evidence/20260713T191740Z/validation_report.md
- **Confidence:** 0.96
- **Reported by:** evidence

The manuscript correctly limits the work in several places, but the intended taxonomy claim combines conceptual contribution with falsifiable contamination criteria. The criteria are present, yet the supplied results do not establish all six mechanisms equally: natural recursion has a clean first round and null compounding factors, and summarization loss has no utility oracle. The artifact supports the existence of the proposed taxonomy and its scenario criteria, but only limited case-specific demonstrations, not empirical confirmation of all mechanisms.

Evidence:

- paper/v3/main.tex, §3: each class is defined by “(a) its causal mechanism and (b) a falsifiable contamination criterion.”
- paper/v3/main.tex, §5.3: “The natural recursion scenario ... reliably does not [generate the error], yielding a null compounding factor.”
- paper/v3/main.tex, §5.3: “The summarization probe has no utility oracle, so it cannot establish a utility gain from raw fidelity.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: compounding_factor_natural is null with reason round1_clean for every configuration; no utility oracle is declared.
- paper/v3/main.tex, Conclusion: “Natural recursive compounding was not observed.”

**Recommendation:** Describe the taxonomy as a conceptual framework whose criteria were operationalized in pilot scenarios, and state that the pilot demonstrates selected case behaviors rather than empirically validating each mechanism as a general phenomenon.

### [METHODOLOGY-002] There is no matched no-memory baseline for the contamination probes

- **Severity:** MINOR
- **Category:** experimental-design
- **Location:** paper/v3/main.tex, Sections 4.1 “Scenarios,” 5.4 “Controls, retention, and remaining defects,” and Discussion “Future-work contract”; scenarios/controls/cb-val-008-control-empty-memory.yaml
- **Confidence:** 0.94
- **Reported by:** methodology

The pilot includes an empty-memory control, but it uses a different meal-planning task and is not a counterfactual version of any of the six contamination probes. Consequently, the design cannot directly establish the excess error caused by injecting each probe's memory relative to the same task without memory, nor can it quantify a contamination-versus-retention trade-off for those tasks. The manuscript acknowledges the need for broader paired controls in future work, so this limits the current pilot rather than contradicting its case-specific observations.

Evidence:

- paper/v3/main.tex, Section 4.1: the empty-store control asks “What's a good way to structure a weekly meal plan?”, whereas the contamination probes use unrelated tasks such as dinner menus, preferences, renovations, locations, and launch status.
- scenarios/controls/cb-val-008-control-empty-memory.yaml: `memory_seed: []` with probe query `What's a good way to structure a weekly meal plan?`; it is not a matched no-memory version of CB-VAL-001 through CB-VAL-006.
- paper/v3/main.tex, Discussion, “Future-work contract”: the next experiment will use “paired relevant-memory controls” and a contamination-versus-retention frontier.

**Recommendation:** Describe the current controls strictly as pipeline and retention controls, not as no-memory counterfactuals; for causal attribution, add matched no-memory conditions for each probe and paired relevant-memory tasks before making broader memory-induced degradation or trade-off claims.

### [METHODOLOGY-003] The response contamination metric can leave undetected false negatives after unresolved cases are excluded

- **Severity:** MINOR
- **Category:** metrics
- **Location:** paper/v3/main.tex, Section 4.4 “Verdict resolution and metrics” and Discussion, Section “Validity statements”; spec/metrics.md, “Verdict resolution”
- **Confidence:** 0.90
- **Reported by:** methodology

Canonical scoring treats absence of a forbidden regex match plus a confirming judge result as clean. The manuscript explicitly documents that regexes detect mentions rather than assertions and that 52 disagreements are unresolved, but it does not establish sensitivity for cases in which a contaminated answer uses paraphrases or avoids the listed strings. Excluding disagreements prevents forced labels, but does not validate the remaining clean outcomes as uncontaminated. Therefore the reported machine-resolved clean rates are scorer-defined outcomes, not validated contamination rates.

Evidence:

- paper/v3/main.tex, Section 4.4: “a match yields contaminated, otherwise a provisional clean that the LLM judge may confirm”; disagreements are flagged and excluded from rates.
- paper/v3/main.tex, Discussion, “Validity statements”: “Regex scoring detects mention, not assertion” and “52 of 350 rounds disagreed”; the unresolved queue has no human verdicts.
- spec/metrics.md, “Verdict resolution”: deterministic no-match produces provisional `clean`, and only deterministic/judge disagreement becomes `needs_human_review`.

**Recommendation:** Keep the machine-only qualification in all result summaries and avoid calling the resulting proportions validated contamination rates; report assertion-aware sensitivity or blinded adjudication before using clean-rate differences as response-layer evidence.

### [METHODOLOGY-004] The proposed full-benchmark fixtures are not yet approval-ready under the repository's own review criteria

- **Severity:** MINOR
- **Category:** experimental-design
- **Location:** docs/SCENARIO_REVIEW.md; spec/full-benchmark-candidates.yaml; scenarios/full-benchmark/cb-full-sd-01.yaml through cb-full-sd-c05.yaml and paired controls
- **Confidence:** 0.98
- **Reported by:** methodology

The supplied full-benchmark manifests are explicitly candidates, and the approval registry is empty. The review checklist requires a deterministic utility oracle, but the supplied CB-FULL-SD probe and control manifests do not declare `expected.utility.must_include_patterns`. Thus these fixtures cannot yet satisfy the stated acceptance checklist or support execution as an approved full benchmark. This does not invalidate the reported pilot, which uses the separate validation scenarios.

Evidence:

- docs/SCENARIO_REVIEW.md, checklist item 6: “A deterministic `expected.utility.must_include_patterns` oracle measures whether the answer still performs the task.”
- spec/full-benchmark-candidates.yaml: `candidates: []`, with the comment that existing fixtures remain planning manifests until individually reviewed.
- scenarios/full-benchmark/cb-full-sd-01.yaml: `expected` contains `relevant`, `retrieval`, and `forbidden_content`, but no `utility` object; the same structure appears in the supplied paired controls.

**Recommendation:** Do not present the supplied full-benchmark fixtures as approved or executable evidence; add the required utility oracles, record individual human approvals, and complete the review checklist before using them in a benchmark result.

### [REPO-CONSISTENCY-001] Reported empirical results cannot be independently verified from the supplied artifact

- **Severity:** MINOR
- **Category:** evidence/reproducibility
- **Location:** paper/v3/main.tex, §5.3 'Repeated-evaluation audit and scoring defects'; README.md, 'Paper and evidence'
- **Confidence:** 0.98
- **Reported by:** repo-consistency

The manuscript reports repeated-audit outcomes, including 350 scored rounds, 52 unresolved rounds, and per-cell five-repetition distributions, but the supplied files contain no evidence aggregates, verdicts, or raw traces. The README explicitly states that the relevant evidence directories exist but were withheld, so these claims are unverified in this evaluation rather than contradicted. The manuscript does acknowledge the unresolved adjudication limitation, but not that the supplied artifact lacks the underlying aggregate files.

Evidence:

- paper/v3/main.tex, abstract: “Of 350 scored rounds, 52 remain unresolved pending human review.”
- paper/v3/main.tex, Table \ref{tab:repeated}: reports five-repetition clean/contaminated/flagged distributions for seven configurations.
- README.md, 'Paper and evidence': “Aggregates are supplied.” The supplied file list contains no evidence directory, verdicts.json, or validation_report.md.
- README.md, 'Paper and evidence': “The v0.3.1 append-only correction bundle provides the reconciled 660-call report and a 52-round pending review queue.” Those files are not among the supplied artifacts.

**Recommendation:** Label the repeated-audit numbers as unverified for this artifact review, or supply the aggregate verdict/report files needed to recompute them. The narrowest supported wording is that the manuscript reports machine-only results from the frozen evidence release; independent verification is unavailable from the supplied files.

### [REPO-CONSISTENCY-002] Learned-embedding condition is described as implemented but is not integrated into the benchmark execution path

- **Severity:** MINOR
- **Category:** implementation mismatch
- **Location:** paper/v3/main.tex, §4.3 'Models and determinism' and §7 'Similarity substitution'; src/retrieval.py, functions top_k_embeddings/local_embedder/retrieve; src/full_benchmark.py, main(); spec/full-benchmark.plan.yaml
- **Confidence:** 0.97
- **Reported by:** repo-consistency

The manuscript and README describe a successor-study learned-embedding condition using fastembed and BAAI/bge-small-en-v1.5. The code contains helper functions for local embeddings, but the active retrieval path always calls TF-IDF top_k(), and no configuration or runner path selects top_k_embeddings(). The full-benchmark runner is explicitly dry-run only. Thus the claim is partially supported as helper code, but not as an executable benchmark condition.

Evidence:

- paper/v3/main.tex, §4.3: “The successor-study implementation additionally provides a local ONNX embedding condition (\texttt{fastembed} with \texttt{BAAI/bge-small-en-v1.5})”.
- README.md, 'Local Embedding Backend': “The full-benchmark plan reports TF-IDF and a learned embedding backend as separate conditions.”
- src/retrieval.py, `top_k_embeddings(...)`: defines an embedding helper, but `retrieve(...)` invokes `top_k(query, entries, config["retrieval"]["k"])` unconditionally.
- src/retrieval.py, `local_embedder(...)`: constructs an embedder, but no call site in the supplied source invokes it.
- src/full_benchmark.py, `main(...)`: when `--authorize-api` is supplied, it raises “API execution is not implemented”; the planner only performs a dry run.
- spec/full-benchmark.plan.yaml, `execution.retrieval_backends`: declares `tfidf` and `learned_embedding`, but this is a plan rather than an executable selection mechanism.

**Recommendation:** Restrict the implementation claim to “embedding helper code and a planned successor condition,” or add an explicit backend configuration and execution path before calling it an implemented condition. The current paper's statement that no learned-embedding result is reported remains supported.

### [REPRODUCIBILITY-002] Supplied repeated-run metadata does not conform to the repository's declared run-metadata schema

- **Severity:** MINOR
- **Category:** provenance
- **Location:** spec/run-meta.schema.yaml; evidence/20260713T191740Z/run_meta.json; report/FINAL-AUDIT.md §Verified repository checks
- **Confidence:** 0.96
- **Reported by:** reproducibility

The current schema requires `harness_call_counts`, `harness_total_calls`, `judge_total_calls`, `pipeline_call_counts`, and `pipeline_total_calls`. The supplied v0.3 run_meta.json instead contains only the older `call_counts` and `total_calls` fields. Although the repository documents compatibility aliases, those aliases are not sufficient because the newer fields remain required. Thus the supplied evidence cannot be validated against the declared schema as written, weakening the release provenance and call-accounting reproducibility record.

Evidence:

- spec/run-meta.schema.yaml lists `harness_call_counts`, `harness_total_calls`, `judge_total_calls`, `pipeline_call_counts`, and `pipeline_total_calls` under `required`.
- evidence/20260713T191740Z/run_meta.json contains `run_dir`, `models`, `repetitions`, `call_counts`, and `total_calls`, but does not contain the required `harness_call_counts`, `harness_total_calls`, `judge_total_calls`, `pipeline_call_counts`, or `pipeline_total_calls`.
- report/FINAL-AUDIT.md §Verified repository checks says frozen evidence is present and hashable, but its evidence-boundary description does not establish that the supplied historical metadata conforms to the current run-meta schema.

**Recommendation:** Either version and preserve the historical schema for this release or add a validated, append-only metadata correction containing the required fields and an explicit schema version. Do not describe schema validation as complete unless the release-check actually validates the evidence metadata against the applicable schema.

### [REPRODUCIBILITY-003] Fifty-two disputed rounds remain unavailable for independent ground-truth scoring

- **Severity:** MINOR
- **Category:** scoring-validity
- **Location:** evidence/20260713T191740Z/validation_report.md §Human-adjudicated comparison and §Flagged for human review; evidence/20260713T191740Z/adjudications.json; paper/v3/main.tex §Repeated-evaluation audit and scoring defects
- **Confidence:** 0.99
- **Reported by:** reproducibility

The v0.3 repeated audit excludes 52 of 350 rounds because deterministic and judge verdicts disagree. This affects all five staleness configurations without fully resolved response-layer rates and affects the seeded-recursion comparison, where most arms are flagged. The limitation is explicitly declared in the manuscript and evidence, so this is not an undisclosed defect; the affected comparisons remain machine-only and cannot support human-validated claims.

Evidence:

- evidence/20260713T191740Z/validation_report.md states: `unavailable (adjudications_file_missing); machine verdicts remain authoritative.`
- evidence/20260713T191740Z/defects.md D7 states: `Fifty-two of the 350 scored rounds resolved to needs_human_review` and that they are excluded from machine-only rates.
- evidence/20260713T191740Z/adjudications.json contains `adjudications: []` and 52 pending review-queue entries.
- paper/v3/main.tex abstract explicitly says: `Of 350 scored rounds, 52 remain unresolved pending human review.`

**Recommendation:** Keep all affected results labeled machine-only and avoid interpreting unresolved cells as clean or contaminated. If a human-adjudicated claim is needed, complete the documented two-reviewer protocol and publish a separate consensus layer; otherwise retain the current limitation wording.

### [STATISTICS-001] Most repeated comparisons lack uncertainty estimates

- **Severity:** MINOR
- **Category:** variance reporting
- **Location:** paper/v3/main.tex, §5.3 'Repeated-evaluation audit and scoring defects' and §5.5 'Attribution: what the cells support'; Table 'Repeated v0.3 outcome distributions'
- **Confidence:** 0.96
- **Reported by:** statistics

The v0.3 audit reports five-repetition clean/contaminated/flagged counts, but uncertainty intervals are provided only for the scope-bleed comparison. Claims about provenance, staleness, seeded recursion, and other configuration differences therefore remain descriptive without confidence intervals or another uncertainty summary. The manuscript itself acknowledges that future work will add variance reporting.

Evidence:

- Table entries are reported as 'clean/contaminated/flagged across five repetitions'.
- The only displayed intervals are for scope bleed: '4/5 (exact 95% Clopper--Pearson interval [0.284, 0.995]) and 0/5 ([0.000, 0.522])'.
- The future-work contract requires 'repeated trials with per-repetition artifacts and variance reporting'.

**Recommendation:** For every repeated comparative result emphasized in the abstract, results, or conclusion, report the underlying per-repetition counts together with an uncertainty interval or explicitly label the result as an unquantified descriptive observation.

### [STATISTICS-002] No formal statistical comparison or effect-size framework for mitigation claims

- **Severity:** MINOR
- **Category:** statistical testing
- **Location:** paper/v3/main.tex, abstract; §5.3; §5.5; Table 'Repeated v0.3 outcome distributions'
- **Confidence:** 0.91
- **Reported by:** statistics

The manuscript compares configurations using terms such as 'excluded', 'yielded', 'separates', and 'supports', but does not conduct statistical tests or report a systematic effect-size measure for the repeated comparisons. With only five repetitions and substantial unresolved outcomes, formal inference may not be warranted, but the manuscript should consistently distinguish descriptive differences from evidence of mitigation effects.

Evidence:

- The abstract states that 'the namespacing arm excluded cross-domain distractors and the TTL arm excluded the stale fact in all five repetitions'.
- The results state that 'the tag and raw-fidelity arms each had five machine-resolved clean outcomes'.
- No p-values, paired comparison tests, or standardized effect-size estimates are reported for these comparisons.
- The manuscript limits the interpretation by stating: 'These are within-scenario observations, not estimates of real-world prevalence or model-independent mitigation efficacy.'

**Recommendation:** Retain explicitly descriptive wording for these comparisons, or add a prespecified paired analysis and effect-size definition if inferential mitigation claims are intended.

### [STATISTICS-003] Very small and non-independent effective sample for mechanism-level rates

- **Severity:** MINOR
- **Category:** sample size
- **Location:** paper/v3/main.tex, §2 'Validity statements' and §7 'Scale'; evidence/20260713T191740Z/defects.md, 'Evidence scope'
- **Confidence:** 0.99
- **Reported by:** statistics

Each mechanism is represented by one hand-authored scenario, with five repeated API executions. Thus the repeated observations do not provide five independent scenario-level replications, and the effective mechanism diversity remains one probe per class. This makes rates such as 0/5 or 5/5 unsuitable for general claims about a mechanism or mitigation. The manuscript explicitly recognizes this limitation.

Evidence:

- The manuscript states: 'Rates from one probe per mechanism are mechanism demonstrations with stated resolved counts, not population estimates.'
- It states: 'Repeated calls do not add scenario diversity.'
- The repeated audit is documented as 'Repetitions: 5; Configurations: 7; Scored rounds: 350', while the paper describes only one probe per mechanism.
- The paper reports the intended successor design as 'at least five scenarios per contamination class'.

**Recommendation:** Keep all mechanism-level rates explicitly labeled as within-scenario pilot observations and avoid interpreting five repetitions as five independent experimental subjects or scenario replications.

### [STATISTICS-004] Unresolved rounds materially limit several aggregate rates

- **Severity:** MINOR
- **Category:** missing observations
- **Location:** paper/v3/main.tex, abstract; §5.3; §6.1 'Validity statements'; evidence/20260713T191740Z/validation_report.md, 'Human-adjudicated comparison' and config comparison table
- **Confidence:** 0.99
- **Reported by:** statistics

Fifty-two of 350 repeated rounds are excluded from rate denominators because deterministic and judge scorers disagree. This leaves some headline metrics null and means the reported rates condition on the subset of rounds resolved by the machine rule. The manuscript discloses this clearly, so the issue is a declared limitation rather than an undisclosed statistical error.

Evidence:

- The abstract states: 'Of 350 scored rounds, 52 remain unresolved pending human review.'
- The manuscript states that disputed rounds 'are excluded from machine-only rates'.
- The validation report shows 'staleness_rate null (probe_needs_human_review)' for multiple configurations.
- evidence/20260713T191740Z/adjudications.json contains 'adjudications': [] and 52 pending queue entries.

**Recommendation:** Continue presenting the reported rates as machine-only conditional summaries, and do not use them for stronger comparative or inferential claims until adjudication or a prespecified sensitivity analysis is available.

### [STATISTICS-005] The v0.2 matrix contains single-run cell results

- **Severity:** MINOR
- **Category:** run count
- **Location:** paper/v3/main.tex, §5 'Ablation Study', Table 'The ablation matrix' and Table 'Evidence lineage'
- **Confidence:** 0.97
- **Reported by:** statistics

The manuscript includes a historical v0.2 ablation matrix whose individual scenario-configuration cells are based on one run, with flagged cells excluded. Those results are clearly separated from the repeated v0.3 audit, but any comparison drawn from the v0.2 matrix has no run-to-run variance and should not be treated as replicated evidence.

Evidence:

- The lineage table labels v0.2 as the 'single-run matrix'.
- The manuscript states: 'The frozen v0.2 single-run ablation' and reports 'ten artifacts were flagged for manual inspection.'
- The v0.2 validation report gives one round for each scenario/configuration cell.

**Recommendation:** Restrict v0.2 claims to historical single-run observations and ensure that any headline comparison is explicitly attributed to the repeated v0.3 audit instead.

## Recommended changes

- **ADVERSARIAL-001** — Freeze and publish the exact scenario manifests used to generate the evidence, or regenerate the frozen verdicts from the supplied manifests. Reconcile the per-scenario judge records, judge-call counts, and report before relying on the scope-bleed response results. (files: scenarios/validation/cb-val-003-scope-bleed.yaml (`scoring.judge.enabled: true`); evidence/20260713T191740Z/verdicts.json, all CB-VAL-003 records; src/judge.py, `score_artifact`; evidence/20260713T191740Z/validation_report.md, `judge_call_counts` and per-scenario verdict table)
- **ADVERSARIAL-002** — Define the denominator explicitly and make the generated report and manuscript use the same quantity. Separate total retrievals from gated retrievals, and recompute all displayed gate-cost statistics from the corrected aggregation. (files: paper/v3/main.tex, §6 `The two-layer dissociation persists` / §7 gate architecture; evidence/20260713T191740Z/validation_report.md, `Relevance-gate observability`; src/metrics.py, `gate_observability`)
- **ADVERSARIAL-004** — Treat this result as a deterministic-pattern observation, not a validated response-contamination effect, until the exact evidence is rescored with the enabled judge or independently adjudicated under an assertion-aware rubric. (files: paper/v3/main.tex, §5.5 `Attribution: what the cells support`; evidence/20260713T191740Z/verdicts.json, CB-VAL-003 records; evidence/20260713T191740Z/defects.md, D6; scenarios/validation/cb-val-003-scope-bleed.yaml)
- **ARCHIVAL-001** — Create or cite immutable, version-specific archive records for the paper source and each evidence release, and state explicitly which DOI/version contains the numbers reported in the manuscript. Include a manifest recording the commit/tag and hashes of the paper and evidence directories. (files: CITATION.cff; README.md, “Paper and evidence” and “Citation”; paper/v3/main.tex, §5 and Table 2)
- **ARCHIVAL-002** — Replace bare repository and relative-directory citations with release-specific immutable references: commit SHA plus archived DOI/object URL, and provide a release manifest mapping every table to exact artifact hashes. (files: README.md, “Paper and evidence,” “Quick start,” and “Citation”; docs/REPRODUCTION.md, §§1–3; paper/v3/main.tex, §5 footnote and Table 2)
- **CITATIONS-001** — Reconcile the scenario/configuration/repetition counts with the supplied aggregates and call logs. Identify any additional scenario or round if one exists, or correct the 350-round and API-call totals and recompute the review percentage, audit summaries, and related claims. (files: paper/v3/main.tex, Section 4, paragraphs beginning “Table 1 is the frozen v0.2 single-run ablation” and “Fifty-two of the 350 rounds”; Section 4 opening paragraph; Table 4 (tab:repeated))
- **CLAIM-001** — Provide evidence for the claim or remove it. (files: paper/v3/main.tex, §5.5, §6, Discussion, and Conclusion)
- **METHODOLOGY-001** — Report the exact retrieval implementation and versions, vectorizer/tokenization/normalization settings, tie-breaking, prompt templates, memory serialization, API/model revision identifiers, and provide the code or a complete executable release corresponding to the cited evidence tags. (files: paper/v3/main.tex, Sections 4.3 “Models and determinism” and 5 “Ablation Study”; spec/configs.yaml, models and retrieval sections)
- **REPRODUCIBILITY-001** — Archive an exact commit identifier with each evidence release and provide a lockfile, container, or complete resolved dependency manifest, including the API client version and retrieval dependencies. Preserve the existing nondeterminism caveat and report rerun comparisons against the frozen artifacts. (files: requirements.txt; docs/REPRODUCTION.md §Prerequisites and §2; paper/v3/main.tex §Models and determinism and §Discussion and Limitations, Reproducibility)

_Veritas Gate never modifies the artifact it evaluates; these actions are advisory._

## Model usage

| Model | Calls | Input tokens | Output tokens | Cost |
| --- | --- | --- | --- | --- |
| gpt-5.6-luna | 8 | 872,707 | 27,307 | 1.3640 USD |
| **Total** | 8 | 872,707 | 27,307 | **1.3640 USD** |

Cost is estimated from the rates configured when the run happened. It is not a billing record.

## Evaluation metadata

- Run id: `2026-09-25T201610Z`
- Veritas version: 0.1.0
- Profile: scientific-paper (version 1)
- Artifact: contam-bench (document)
- Artifact commit: 858ce8c1cec77481b1c719a4d8298ced414e19c8
- Started: 2026-09-25T20:16:10.894221+00:00
- Finished: 2026-09-25T20:21:41.629757+00:00

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

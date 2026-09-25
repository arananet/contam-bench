# Veritas Gate Report

**Gate:** `REVISE` (exit code 2)

## Executive summary

8 judges and 6 checks produced 45 consolidated findings (0 critical, 25 major, 20 minor, 0 info). Failing checks: citability, claim-graph.

## Gate result

| Severity | Count |
| --- | --- |
| Critical | 0 |
| Major | 25 |
| Minor | 20 |
| Info | 0 |

Policy decisions:

- 25 major finding(s) exceed the limit of 0.

## Blocking findings

### [ADVERSARIAL-001] Raw per-scenario response artifacts needed to audit the headline results are not supplied

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** README.md, 'Paper and evidence' and 'Usage'; evidence/20260713T191740Z/verdicts.json; paper/v3/main.tex, §4 'CONTAM-Bench' and §5.3
- **Confidence:** 0.98
- **Reported by:** adversarial

The manuscript says every run persists raw prompts, injected memories, responses, and verdicts, but the supplied evidence files contain only aggregate reports, metadata, queues, and verdict summaries. The supplied verdicts.json records judge evidence but not the underlying subject responses, so an evaluator cannot independently verify whether the verdicts or retrieval assertions match the actual outputs. This prevents reproduction of the main response-level results from the provided artifact.

Evidence:

- README.md: “Each evidence directory contains the raw per-scenario artifacts (prompts, injected memories, gate decisions, responses), verdicts.json, validation_report.md, and defects.md”
- paper/v3/main.tex, §4: “every run artifact, including raw prompts, injected memory, responses, and judge verdicts, is persisted as JSON for audit”
- The supplied file inventory for evidence/20260713T191740Z contains no CB-*.json per-scenario artifact files.
- evidence/20260713T191740Z/verdicts.json contains verdicts and scorer evidence, but no subject-response text or prompt artifacts.

**Recommendation:** Supply the exact frozen CB-*.json artifacts, or remove claims that the headline response-level results can be independently audited from this release.

### [ADVERSARIAL-002] The manuscript claims a corrected review report that contradicts the supplied frozen report

- **Severity:** MAJOR
- **Category:** artifact discrepancy
- **Location:** paper/v3/main.tex, §5.3; evidence/20260713T191740Z/validation_report.md, 'Flagged for human review'; evidence/20260713T191740Z/defects.md, D8; report/FINAL-AUDIT.md
- **Confidence:** 0.99
- **Reported by:** adversarial

The manuscript states that the rendered report identifies flagged rows by repetition and artifact hash. The supplied v0.3 validation report instead repeats indistinguishable scenario/configuration/round labels, and the accompanying defect record explicitly identifies this as an unresolved defect. This discrepancy makes the stated auditability and evidence lineage inaccurate.

Evidence:

- paper/v3/main.tex, §5.3: “The rendered report now labels its machine-only and human-consensus tables separately and identifies review rows by repetition and artifact hash.”
- evidence/20260713T191740Z/validation_report.md, 'Flagged for human review': entries are formatted as “CB-VAL-004 × arm_gate round 1” and repeat across repetitions without repetition or artifact hash.
- evidence/20260713T191740Z/defects.md, D8: “Human-review register omits repetition identifiers” and “the report is ambiguous.”
- report/FINAL-AUDIT.md, 'Scientific readiness': independent scoring assessment remains open.

**Recommendation:** Either provide the corrected report and its provenance, or revise the manuscript to describe the supplied report as ambiguous and retain D8 as an active limitation.

### [ARCHIVAL-001] Reported evidence is referenced by mutable tags and repository paths rather than an immutable version-specific identifier

- **Severity:** MAJOR
- **Category:** identity and archival
- **Location:** paper/v3/main.tex, Section 5 and Table 2 (Evidence lineage); README.md, 'Paper and evidence' and 'Citation' sections
- **Confidence:** 0.97
- **Reported by:** archival

The paper reports results from multiple evidence releases, but identifies them only by repository-relative paths and Git tags. No commit SHA, version-specific DOI, or Software Heritage identifier is supplied for the exact artifacts underlying each table. An annotated Git tag and a GitHub repository are not sufficient evidence that the cited contents cannot later be changed or deleted.

Evidence:

- paper/v3/main.tex, Table 2: “v0.2 ablation ... v0.2-ablation”, “v0.3 repeated audit ... v0.3-repeated-ablation”, and “v0.3.1 corrections ... v0.3.1-evidence-corrections”
- paper/v3/main.tex, Section 5: “Complete run artifacts are published at \texttt{evidence/20260713T084130Z} ... frozen at tag \texttt{v0.2-ablation}.”
- README.md: “Runs cited in publications are copied to \`evidence/<timestamp>/\` and frozen under an annotated tag”; the cited locations are GitHub repository paths, not immutable identifiers.

**Recommendation:** Record the exact commit SHA for every evidence release used by the paper and archive each release independently with a version-specific DOI or Software Heritage identifier. State explicitly which DOI resolves to which release and paper version.

### [ARCHIVAL-002] The supplied artifact does not contain the evidence files needed to retrieve or verify the headline results

- **Severity:** MAJOR
- **Category:** data and artifact availability
- **Location:** Provided file list; README.md, 'Paper and evidence' section; paper/v3/main.tex, Table 2 and Sections 5.1–5.3
- **Confidence:** 0.99
- **Reported by:** archival

The paper's central numerical results depend on raw runs, verdicts, reports, and correction queues, but the supplied artifact contains only the citation, licensing, README, reproduction protocol, and LaTeX manuscript. The manuscript and README point to evidence directories that are absent from the provided file list. Thus, a reader of this artifact cannot independently retrieve the artifacts supporting the tables.

Evidence:

- Provided file list contains CITATION.cff, LICENSING.md, README.md, docs/REPRODUCTION.md, and paper/v3/main.tex, but no \`evidence/\` directory, raw JSON, verdicts, or validation reports.
- README.md: “Each evidence directory contains the raw per-scenario artifacts ... \`verdicts.json\`, \`validation_report.md\`, and \`defects.md\`.”
- paper/v3/main.tex, Section 5.2: “Complete run artifacts are published at \texttt{evidence/20260713T084130Z} ... Every number in this section is recomputable from those artifacts.”

**Recommendation:** Include or independently archive the exact evidence releases, including raw artifacts, verdicts, reports, correction bundle, and review queue, and link them using immutable version-specific identifiers. If the artifact package intentionally omits them, label the supplied package as manuscript-only rather than reproducible evidence.

### [CITATIONS-001] Repeated-audit denominator is arithmetically inconsistent

- **Severity:** MAJOR
- **Category:** experimental accounting
- **Location:** paper/v3/main.tex, Section 4.4 'Repeated-evaluation audit and scoring defects'; Table 3 caption and surrounding text
- **Confidence:** 0.99
- **Reported by:** citations

The paper states that the repeated audit used nine scenarios, seven configurations, and five repetitions, which implies 315 scenario-configuration-rounds. It nevertheless reports 350 scored rounds and derives the 14.9% review rate from 52/350. The same inconsistency appears in the reported subject-call count. This prevents the reported aggregate accounting from being recomputed as stated and may change the review rate and any aggregate interpretation.

Evidence:

- "the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds"
- "Fifty-two of the 350 rounds (14.9%) required human review"
- "The repeated audit used 660 API calls: 350 subject calls, 135 gate calls, and 175 judge calls."
- Table 3 lists seven configurations and four scenario columns, while Table 2 and the surrounding text define nine scenarios; nine × seven × five = 315, not 350.

**Recommendation:** Reconcile the scenario, configuration, repetition, and API-call counts against the persisted run manifest, and correct the denominator, percentages, and call accounting. If additional rounds were included, identify them explicitly and explain why they are not represented by the stated nine-by-seven-by-five design.

### [CITATIONS-002] Headline results cannot be independently checked from the supplied artifact

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Section 4 'Ablation Study', footnote to the first paragraph; Sections 4.4 and 8.1 'Reproducibility'
- **Confidence:** 0.97
- **Reported by:** citations

The main results depend on external evidence releases and a repository, but the supplied artifact contains only main.tex and references.bib. No YAML manifests, raw prompts, responses, retrieval traces, judge outputs, review queue, hashes, or run reports are included here. Consequently, the manuscript's matrix and repeated-audit claims are unverified from the provided material, despite the assertion that every number is recomputable.

Evidence:

- "Complete run artifacts are published at evidence/20260713T084130Z in the benchmark repository ... Every number in this section is recomputable from those artifacts."
- "The v0.3 evidence now includes a separately versioned queue for all 52 unresolved artifact rounds"
- "The benchmark and code are available at https://github.com/arananet/contam-bench."
- The supplied files are only paper/v3/main.tex and paper/v3/references.bib; none of the cited evidence files or run artifacts is present.

**Recommendation:** Provide the exact evidence release or a complete archival supplement containing the manifests, raw model and judge artifacts, retrieval traces, scoring outputs, review queue, and file hashes, or label the reported results as externally hosted and not independently verifiable from this artifact.

### [CITATIONS-003] Intended identifier-reuse claim has no supporting experiment or evidence

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** paper/v3/main.tex, Sections 3–4 and 7; no identifier-reuse or MCP experiment is specified
- **Confidence:** 0.98
- **Reported by:** citations

The intended claim that reusing an identifier overwrites shared mappings but is retained in separate MCP instances is not operationalized or reported anywhere in the manuscript. The described benchmark concerns memory contamination scenarios, namespaces, provenance, TTL, retrieval gates, and raw fidelity; it provides no identifier-reuse scenario, MCP configuration, output, or trace. The claim is therefore unverified and cannot be narrowed from the supplied text beyond saying that no evidence is presented here.

Evidence:

- The benchmark scenario description lists seeded items with "content, source, age in days, domain, and fact class" but does not specify identifier reuse or MCP instances.
- Table 2's seven configurations cover naive, namespacing, provenance, TTL, gate, raw, and governed arms; none is an identifier-reuse or MCP-instance condition.
- The results sections report drift, provenance, scope bleed, staleness, recursion, summarization, and controls, but contain no identifier-overwrite result.

**Recommendation:** Remove this claim from the paper or add a separately specified and evidenced experiment covering the fixed write order, shared mappings, separate MCP instances, and the observed identifier behavior.

### [CITATIONS-004] Intended host-handler-dependent tool-rejection claim has no supporting evidence

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** paper/v3/main.tex, Section 4.3 'Models and determinism'; no tool-rejection experiment elsewhere in the manuscript
- **Confidence:** 0.98
- **Reported by:** citations

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default is not discussed or tested in the manuscript. The model and benchmark description mentions subject, judge, relevance-gate, retrieval, and memory configurations, but no tool-rejection protocol, SDK version, host handler, or comparative result. The claim is therefore unverified from the artifact.

Evidence:

- "The subject model under test is claude-sonnet-4-6 at temperature 0; the judge and relevance gate are claude-haiku-4-5."
- "The reported validation runs use TF-IDF cosine similarity" and the surrounding configuration descriptions discuss memory retrieval, not tool rejection.
- No occurrence or section in main.tex specifies an SDK default handler, installed host handler, tool rejection test, or corresponding result.

**Recommendation:** Remove the claim from the evaluated claims, or provide a separate experiment documenting the SDK version/default behavior, installed host handler, test prompts, tool outcomes, and comparison conditions.

### [CLAIM-001] Unsupported claim: The paper's seven-configuration pilot establishes a general mitigation architect

- **Severity:** MAJOR
- **Category:** claims/unsupported
- **Location:** paper/v3/main.tex, §5.6, §6, and Conclusion
- **Confidence:** 0.90
- **Reported by:** claim-graph

The artifact explicitly disclaims this stronger claim; the supported conclusion is only a small, mechanism-specific pilot observation.

Evidence:

- paper/v3/main.tex, §6: “The ablation motivates constraints, not an efficacy ordering.”
- paper/v3/main.tex, Conclusion: “They motivate further tests of memory contracts, not a validated general mitigation architecture.”
- evidence/20260713T191740Z/defects.md, Evidence scope: one model, five repetitions, machine-only adjudication unavailable.

**Recommendation:** Provide evidence for the claim or remove it.

### [EVIDENCE-001] Identifier-reuse/MCP-isolation claim is not evidenced

- **Severity:** MAJOR
- **Category:** missing evidence
- **Location:** Artifact-wide; relevant supplied implementation is limited to src/memory_store.py and the listed scenario/evidence files
- **Confidence:** 0.99
- **Reported by:** evidence

The intended claim that reusing an identifier overwrites entries in shared mappings but remains isolated across separate MCP instances cannot be evaluated from the supplied artifact. The repository contents contain no MCP implementation, identifier-reuse experiment, or result record establishing this behavior. This is an unverified claim rather than a plausible inference from the memory-contamination benchmark.

Evidence:

- src/memory_store.py contains an in-memory MemoryStore with append-based seed/write-back behavior, but no identifier-keyed shared mapping or MCP-instance isolation experiment.
- The supplied evidence releases contain contamination scenarios and verdicts, but no table, figure, script, or result file testing identifier reuse across shared versus separate MCP instances.
- README.md describes the study as a persistent-memory ablation benchmark and does not report an MCP identifier-reuse experiment.

**Recommendation:** Either remove this intended claim from the evaluated claims or provide a separately identified experiment with the identifier semantics, shared/separate instance setup, fixed write order, and persisted results. The narrowest currently supported wording is that no identifier-reuse/MCP-isolation conclusion is established by this artifact.

### [EVIDENCE-003] Manuscript claims the rendered report identifies review rows, but the frozen report does not

- **Severity:** MAJOR
- **Category:** reproducibility/reporting contradiction
- **Location:** paper/v3/main.tex, §5.3 “Repeated-evaluation audit and scoring defects”; evidence/20260713T191740Z/validation_report.md, “Flagged for human review”; evidence/20260713T191740Z/defects.md, D8
- **Confidence:** 0.99
- **Reported by:** evidence

The manuscript states that the rendered report identifies review rows by repetition and artifact hash. The supplied frozen v0.3 validation report instead lists repeated rows without either field, and the associated defect record explicitly identifies this as D8. Thus the manuscript overstates the state of the supplied reporting artifact.

Evidence:

- paper/v3/main.tex, §5.3: “The rendered report now labels its machine-only and human-consensus tables separately and identifies review rows by repetition and artifact hash.”
- evidence/20260713T191740Z/validation_report.md, “Flagged for human review”: rows are formatted like “CB-VAL-004 × arm_gate round 1” and omit repetition and artifact hash.
- evidence/20260713T191740Z/defects.md, D8: “Human-review register omits repetition identifiers” and “the report is ambiguous.”

**Recommendation:** Correct the manuscript to distinguish the frozen report from later planned or generated reporting changes. Do not claim that the supplied rendered report includes repetition/hash identifiers unless the corresponding report artifact is supplied and verified.

### [METHODOLOGY-001] The provenance ablation does not isolate provenance tagging

- **Severity:** MAJOR
- **Category:** experimental design
- **Location:** paper/v3/main.tex, Section 5.6 'Attribution: what the cells support'; Section 7.1 'Validity statements'; Table 3
- **Confidence:** 0.99
- **Reported by:** methodology

The provenance arm changes more than source attribution: its tag exposes source, age, and domain. Therefore the five clean outcomes cannot identify provenance tags as the causal mitigation, especially because the stale age is itself potentially informative. The manuscript acknowledges this confound, but the headline provenance interpretation still presents the tag arm as evidence for the provenance finding.

Evidence:

- paper/v3/main.tex, Section 5.6: 'the provenance tag as implemented carries age and domain metadata ([source: user | age: 200d | domain: personal]), so the provenance arm also resolved staleness because the subject discounted the 200-day-old fact by its visible age.'
- paper/v3/main.tex, Section 7.1: 'The provenance arm is confounded: its tag emits source, age, and domain together, so its staleness result cannot be attributed to source attribution alone.'
- paper/v3/main.tex, Table 3: 'provenance tags, raw fidelity, and the governed bundle are each 5/0/0'

**Recommendation:** Report the provenance result explicitly as an effect of a bundled metadata intervention, or provide a pure-factor source-only ablation before attributing the result to provenance tagging.

### [METHODOLOGY-002] The canonical response outcomes have no independent ground-truth resolution for 52 rounds

- **Severity:** MAJOR
- **Category:** evaluation methodology
- **Location:** paper/v3/main.tex, Section 5.2 'Repeated-evaluation audit and scoring defects'; Section 7.1; spec/metrics.md, 'Adjudication layer'
- **Confidence:** 0.99
- **Reported by:** methodology

The repeated audit excludes 52 of 350 rounds because deterministic and judge verdicts disagree, and the artifact contains no human verdicts. This is correctly disclosed, but it leaves the headline machine-only rates and comparisons potentially sensitive to unresolved cases; assertion versus mention is central to the contamination criterion. The manuscript should not use these rates as if they were validated contamination outcomes.

Evidence:

- paper/v3/main.tex, Section 5.2: 'Fifty-two of the 350 rounds (14.9%) required human review.'
- paper/v3/main.tex, Section 5.2: 'Neither direction establishes which scorer is correct without independent assessment.'
- paper/v3/main.tex, Section 5.2: 'the queue ... contains no human verdicts.'
- spec/metrics.md, 'Adjudication layer': 'Ties and single-adjudicator records remain unresolved; no rate silently mixes machine and human layers.'

**Recommendation:** Present sensitivity bounds or separate resolved and unresolved analyses for every load-bearing comparison, and complete the pre-specified blinded independent adjudication before making response-layer efficacy claims.

### [METHODOLOGY-008] The intended identifier-reuse claim is unsupported by the supplied artifact

- **Severity:** MAJOR
- **Category:** claim-evidence mismatch
- **Location:** All supplied files; no corresponding section or scenario present
- **Confidence:** 0.99
- **Reported by:** methodology

The intended claim that reusing an identifier overwrites shared mappings but is retained in separate MCP instances has no corresponding scenario, experiment, result table, or discussion in the supplied files. It is therefore unverified and cannot be included as a finding of the paper.

Evidence:

- The supplied scenario files cover semantic drift, provenance collapse, scope bleed, temporal staleness, recursion, summarization loss, and two controls; none tests identifier reuse or MCP-instance retention.
- paper/v3/main.tex, Section 3 taxonomy: the seven documented classes do not include identifier reuse or MCP mapping semantics.
- spec/schema.yaml and spec/full-benchmark.plan.yaml: no identifier-reuse or MCP-instance scenario is listed.

**Recommendation:** Remove this claim from the evaluated contribution, or add a dedicated, reproducible experiment with shared versus separate MCP instances and explicit overwrite/retention assertions.

### [METHODOLOGY-009] The intended host-handler rejection claim is unsupported by the supplied artifact

- **Severity:** MAJOR
- **Category:** claim-evidence mismatch
- **Location:** All supplied files; no corresponding section or scenario present
- **Confidence:** 1.00
- **Reported by:** methodology

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default is not evaluated in the manuscript or supplied scenarios. No tool-rejection experiment, host-handler comparison, SDK configuration, or result is present.

Evidence:

- The supplied files contain memory scenarios and memory configurations only; no tool-calling or host-handler scenario is present.
- paper/v3/main.tex contains no section or result describing model-only tool rejection, installed host handlers, or SDK-default behavior.
- spec/full-benchmark.plan.yaml lists retrieval backends, models, gates, baselines, and utility oracles, but no tool-rejection experiment.
- The supplied source files implement memory retrieval, judging, adjudication, and benchmarking, but do not contain a model-only tool rejection experiment or host-handler comparison.
- tests/test_integration.py and tests/test_ci_workflows.py cover benchmark execution and CI configuration, not SDK-default versus installed-host-handler tool behavior.
- The supplied paper, paper/v3/main.tex, discusses memory contamination and retrieval gates but makes no evidence-backed tool-handler comparison.

**Recommendation:** Do not state this claim as an evaluated result. Add a controlled comparison of the SDK default and installed host handler, with the same model prompt and explicit rejection outcomes, if the claim is in scope.

### [REPO-CONSISTENCY-001] Reported empirical results cannot be verified from the supplied artifact

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex §5.3–§5.5; README.md “Paper and evidence” and “Repository layout”
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The manuscript reports headline repeated-audit results, including 350 scored rounds, 52 unresolved rounds, and per-cell outcome distributions, but the supplied files contain neither the referenced evidence directories nor the scenario manifests required to run the harness. README.md claims that frozen evidence is available under evidence/20260713T191740Z and that scenarios are under scenarios/validation/ and scenarios/controls/, but none of those files are included in the supplied artifact. Consequently, the reported results are unverified from the submitted bundle.

Evidence:

- paper/v3/main.tex §5.3: “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds”
- paper/v3/main.tex Table 5 / §5.3: “The provenance separation persists without flags: provenance tags, raw fidelity, and the governed bundle are each 5/0/0”
- README.md, “Paper and evidence”: “v0.3 repeated audit (7×9×5) | evidence/20260713T191740Z/”
- README.md, “Repository layout”: “scenarios/validation/ | 7 hand-authored contamination scenarios” and “evidence/ | Frozen runs cited in publications”
- Supplied artifact file inventory: no evidence/ directory, no scenarios/validation/ directory, no scenarios/controls/ directory, and no persisted verdicts or run artifacts are provided

**Recommendation:** Supply the exact frozen scenario manifests, raw run artifacts, verdicts, and reports referenced by the manuscript, or restrict the manuscript to implementation-level claims and explicitly mark all numerical results as unavailable in this artifact bundle.

### [REPO-CONSISTENCY-002] The default executable configuration set does not reproduce the manuscript’s seven-configuration experiment

- **Severity:** MAJOR
- **Category:** configuration mismatch
- **Location:** paper/v3/main.tex §5; spec/configs.yaml; src/harness.py main()
- **Confidence:** 0.98
- **Reported by:** repo-consistency

The manuscript describes the reported ablation as seven configurations, while the supplied configuration file defines eight configurations because arm_gate_preserve_pairs is present. The harness defaults to every key in spec["configs"], so a default invocation runs the experimental eighth arm rather than the manuscript’s seven-arm frozen matrix. No supplied command or configuration pins the reported run to the seven frozen arms.

Evidence:

- paper/v3/main.tex §5: “the run reported here executes nine scenarios ... against seven configurations”
- spec/configs.yaml: “arm_gate_preserve_pairs” is defined under configs, with the comment “It is not a v0.2 result and must be reported separately”
- README.md: “The active development configuration also includes an experimental guarded-gate arm ... it is not part of frozen v0.3 evidence”
- src/harness.py, main(): `config_names = args.config or list(spec["configs"])`, which includes arm_gate_preserve_pairs by default

**Recommendation:** Make the frozen seven-arm configuration explicit in the executable entry point or release configuration, and document the exact command/configuration used for the paper’s results. Keep the experimental arm in a separately named, non-default configuration if it is not part of the evidence release.

### [REPO-CONSISTENCY-003] The identifier-overwrite/MCP claim has no counterpart in the supplied artifact

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** Artifact-wide; especially src/memory_store.py and tests/test_memory_store.py
- **Confidence:** 0.99
- **Reported by:** repo-consistency

One author-intended claim concerns identifier reuse, overwrite behavior in shared mappings, and retention in separate MCP instances. The supplied manuscript, specifications, source files, and tests contain no MCP implementation, identifier-overwrite experiment, shared-mapping model, or separate-instance test. The claim is therefore unsupported by this artifact and cannot be narrowed to a supported empirical conclusion from the available evidence.

Evidence:

- Author-intended claim: “Under the tested configurations and one fixed write order, reusing an identifier overwrites in the shared mappings and is retained in separate MCP instances.”
- src/memory_store.py: `MemoryEntry` has `seed_id`, but `MemoryStore.seed()` only appends entries and contains no overwrite or shared-mapping behavior
- src/memory_store.py: `MemoryStore` is a single in-memory list and has no MCP-instance abstraction
- tests/test_memory_store.py: tests cover namespacing, TTL, fidelity, tags, write-back, and empty stores, but contain no identifier-reuse or MCP-instance test
- Supplied artifact file inventory: no MCP adapter, shared mapping implementation, or corresponding experiment/evidence file

**Recommendation:** Remove the claim from the evaluated scope unless the MCP implementation, controlled experiment, and persisted evidence are supplied. If retained, narrow it only to the exact tested implementation and write order supported by those artifacts.

### [REPO-CONSISTENCY-004] The host-handler-dependent model-only tool-rejection claim is unsupported

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** Artifact-wide; especially src/llm.py and tests/
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The second author-intended claim concerns model-only tool rejection and dependence on an installed host handler rather than the SDK default. The supplied code only wraps Anthropic message calls and implements memory retrieval, gating, judging, and scoring; it contains no tool-rejection experiment, host handler, SDK-default comparison, or tool-call test. The claim is therefore unverified and unsupported by the submitted artifact.

Evidence:

- Author-intended claim: “Model-only tool rejection depends on the installed host handler, not the SDK default.”
- src/llm.py: `CountingClient.complete()` calls `self.client.messages.create(...)` and has no tool definitions, host-handler logic, or rejection comparison
- src/retrieval.py and src/harness.py: the implemented model calls concern relevance gating and subject responses, not tool rejection
- Supplied tests: no test refers to tool rejection, an installed host handler, or an SDK-default behavior

**Recommendation:** Remove the claim from this artifact’s conclusions, or provide the host-handler implementation, SDK-default control, experimental protocol, and persisted results needed to support it.

### [REPRODUCIBILITY-001] Raw per-scenario evidence required for audit and adjudication is missing

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** README.md, section 'Paper and evidence'; src/adjudication.py, functions `_artifact_index` and `generate_packets`; evidence/20260713T191740Z/; supplied file inventory
- **Confidence:** 0.99
- **Reported by:** reproducibility

The manuscript and README say that frozen evidence contains raw prompts, injected memories, gate decisions, responses, and verdicts, and the adjudication code requires per-artifact JSON files to generate blinded packets. Those per-scenario artifact files are not among the supplied files: the evidence directories contain only metadata, reports, defects, verdicts, and the queue. Consequently, an independent researcher cannot inspect the response text or retrieval traces, regenerate the 52 review packets, or verify the judge evidence underlying the headline comparisons.

Evidence:

- README.md: “Each evidence directory contains the raw per-scenario artifacts (prompts, injected memories, gate decisions, responses), `verdicts.json`, `validation_report.md`, and `defects.md`”
- src/adjudication.py: `_artifact_index` scans `evidence_dir` for files whose names start with `CB-` and reads each artifact's `response` and `scoring` fields
- evidence/20260713T191740Z/adjudications.json`: 52 pending artifact hashes are queued, but no corresponding `CB-*.json` evidence files are supplied
- paper/v3/main.tex, §5.3: “Of 350 scored rounds, 52 remain unresolved pending human review.”

**Recommendation:** Include the immutable per-scenario JSON artifacts, or provide an independently verifiable archive containing them, before presenting the results as auditable or seeking human adjudication. Ensure the supplied evidence directory is sufficient for `src.adjudication packets` to run.

### [REPRODUCIBILITY-002] Main experiment cannot be exactly rerun from the environment specification

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** requirements.txt; docs/REPRODUCTION.md, sections 'Independence' and 'Prerequisites'; evidence/20260713T191740Z/run_meta.json; paper/v3/main.tex, §5.3 and §Discussion/Limitations
- **Confidence:** 0.98
- **Reported by:** reproducibility

The main experiment depends on live Anthropic model calls, but the artifact provides only lower-bound dependency constraints and no lockfile, container, exact commit identifier for the frozen runs, or API/model-version snapshot. The reproduction protocol itself asks reviewers to record a commit SHA and exact environment, while the frozen `run_meta.json` records models and sampling parameters but not the commit or installed package versions. Since the paper explicitly reports model-mediated results and acknowledges output variance, this blocks an exact independent rerun of the headline ablation and repeated audit.

Evidence:

- requirements.txt: `anthropic>=0.116`, `PyYAML>=6.0`, `jsonschema>=4.0`, `scikit-learn>=1.3`, and other unpinned lower bounds
- evidence/20260713T191740Z/run_meta.json: records model names, temperatures, repetitions, and call counts, but no commit SHA, Python version, package versions, or hardware/environment image
- docs/REPRODUCTION.md: “the reviewer reports the exact commit SHA, environment, commands, elapsed time, outputs, and deviations”
- paper/v3/main.tex, §Discussion/Limitations, “Temperature~0 sampling reduces but does not remove output variance”

**Recommendation:** Archive the exact commit, Python and library versions, dependency lockfile or container digest, complete commands, and model/API identifiers used for each frozen run. Distinguish artifact reanalysis from live reruns in the paper.

### [REPRODUCIBILITY-005] The intended identifier-overwrite/MCP-instance claim is unsupported in the artifact

- **Severity:** MAJOR
- **Category:** unsupported_claim
- **Location:** Artifact-wide; no supporting location supplied
- **Confidence:** 0.99
- **Reported by:** reproducibility

The intended claim that reusing an identifier overwrites entries in shared mappings but is retained in separate MCP instances is not stated or tested in the supplied manuscript, scenarios, reports, source files, or evidence records. No MCP implementation, identifier-reuse scenario, or corresponding result is provided. The claim is therefore unverified and cannot be included as an empirical conclusion.

Evidence:

- The supplied manuscript's taxonomy and results sections discuss memory scope, provenance, TTL, gating, raw fidelity, and recursion, but contain no MCP-instance or identifier-overwrite experiment
- The supplied scenario inventory contains CB-VAL-001 through CB-VAL-009; none is an identifier-reuse or shared-mapping/MCP-instance scenario
- No supplied source or evidence file defines an MCP instance comparison or reports such a result

**Recommendation:** Remove the claim from the intended claims and conclusions, or add a separately specified and executed experiment with its implementation, commands, artifacts, and results. On the current evidence, no narrower empirical wording is supported.

### [REPRODUCIBILITY-006] The intended host-handler/model-only tool-rejection claim is unsupported in the artifact

- **Severity:** MAJOR
- **Category:** unsupported_claim
- **Location:** Artifact-wide; no supporting location supplied
- **Confidence:** 0.99
- **Reported by:** reproducibility

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default has no supporting experiment or artifact. The supplied code and paper concern memory retrieval, scoring, and adjudication; they do not implement or test tool rejection, host handlers, or SDK defaults. The claim is unverified.

Evidence:

- paper/v3/main.tex: no section, result, scenario, or citation addresses model-only tool rejection or installed host handlers
- src/: supplied modules cover harness, retrieval, memory store, judging, metrics, and adjudication; no host-handler/tool-rejection implementation is supplied
- The supplied scenario inventory and evidence reports contain no tool-rejection result

**Recommendation:** Remove the claim unless a separate tool-handling experiment and its reproducible artifacts are supplied. No narrower wording is supported by the current artifact.

### [STATISTICS-001] Intended identifier-overwrite claim is not evidenced in the supplied artifact

- **Severity:** MAJOR
- **Category:** statistics
- **Location:** AUTHOR'S INTENDED CLAIMS; src/memory_store.py; paper/v3/main.tex
- **Confidence:** 0.99
- **Reported by:** statistics

The intended claim that reusing an identifier overwrites entries in shared mappings but is retained in separate MCP instances is not supported by any reported experiment, sample, run count, variance, statistical comparison, or implementation artifact in the supplied files. The visible memory implementation uses seed IDs and an in-memory list, but no shared-mapping/MCP-instance experiment is described or quantified.

Evidence:

- AUTHOR'S INTENDED CLAIMS: “Under the tested configurations and one fixed write order, reusing an identifier overwrites in the shared mappings and is retained in separate MCP instances.”
- src/memory_store.py, MemoryStore: entries are stored in `self.entries: list[MemoryEntry]`; no shared-mapping or separate-MCP-instance experiment is present.
- paper/v3/main.tex, Sections 5–7: the reported experiments concern nine scenarios, seven memory configurations, retrieval, response verdicts, and controls; no identifier-overwrite result is reported.

**Recommendation:** Do not present this as an established quantitative result unless a documented identifier-overwrite experiment with explicit runs, conditions, and outcomes is supplied; otherwise mark it unverified or remove it.

### [STATISTICS-002] Host-handler-dependent tool-rejection claim is not evidenced

- **Severity:** MAJOR
- **Category:** statistics
- **Location:** AUTHOR'S INTENDED CLAIMS; paper/v3/main.tex; evidence/20260713T191740Z/validation_report.md
- **Confidence:** 0.99
- **Reported by:** statistics

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default has no supporting experiment or quantitative evidence in the supplied artifact. The manuscript and evidence focus on memory contamination, retrieval, gates, and scoring; no host-handler comparison or SDK-default baseline is reported.

Evidence:

- AUTHOR'S INTENDED CLAIMS: “Model-only tool rejection depends on the installed host handler, not the SDK default.”
- paper/v3/main.tex, Abstract and Sections 5–7: reported measurements are memory configurations, contamination verdicts, retrieval assertions, gate calls, and API spend; no tool-rejection or host-handler condition appears.
- evidence/20260713T191740Z/validation_report.md, Config comparison and Relevance-gate observability: the reported metrics contain contamination, recursion, provenance, staleness, retention, retrieval, and gate-call results, but no tool-rejection measurement.

**Recommendation:** Treat this claim as unverified and do not include it among empirical conclusions without a controlled host-handler-versus-SDK comparison with run counts and outcome definitions.

## Judge consensus

| Finding | Severity | Reported by | Consensus |
| --- | --- | --- | --- |
| ADVERSARIAL-001 | MAJOR | adversarial | single-source (low) |
| ADVERSARIAL-002 | MAJOR | adversarial | single-source (low) |
| ARCHIVAL-001 | MAJOR | archival | single-source (low) |
| ARCHIVAL-002 | MAJOR | archival | single-source (low) |
| CITATIONS-001 | MAJOR | citations | single-source (low) |
| CITATIONS-002 | MAJOR | citations | single-source (low) |
| CITATIONS-003 | MAJOR | citations | single-source (low) |
| CITATIONS-004 | MAJOR | citations | single-source (low) |
| CLAIM-001 | MAJOR | claim-graph | single-source (low) |
| EVIDENCE-001 | MAJOR | evidence | single-source (low) |
| EVIDENCE-003 | MAJOR | evidence | single-source (low) |
| METHODOLOGY-001 | MAJOR | methodology | single-source (low) |
| METHODOLOGY-002 | MAJOR | methodology | single-source (low) |
| METHODOLOGY-008 | MAJOR | methodology | single-source (low) |
| METHODOLOGY-009 | MAJOR | methodology, evidence | confirmed (medium) |
| REPO-CONSISTENCY-001 | MAJOR | repo-consistency | single-source (low) |
| REPO-CONSISTENCY-002 | MAJOR | repo-consistency | single-source (low) |
| REPO-CONSISTENCY-003 | MAJOR | repo-consistency | single-source (low) |
| REPO-CONSISTENCY-004 | MAJOR | repo-consistency | single-source (low) |
| REPRODUCIBILITY-001 | MAJOR | reproducibility | single-source (low) |
| REPRODUCIBILITY-002 | MAJOR | reproducibility | single-source (low) |
| REPRODUCIBILITY-005 | MAJOR | reproducibility | single-source (low) |
| REPRODUCIBILITY-006 | MAJOR | reproducibility | single-source (low) |
| STATISTICS-001 | MAJOR | statistics | single-source (low) |
| STATISTICS-002 | MAJOR | statistics | single-source (low) |
| ADVERSARIAL-003 | MINOR | adversarial | single-source (low) |
| ADVERSARIAL-004 | MINOR | adversarial | single-source (low) |
| ARCHIVAL-003 | MINOR | archival | single-source (low) |
| ARCHIVAL-004 | MINOR | archival | single-source (low) |
| ARCHIVAL-005 | MINOR | archival | single-source (low) |
| CHECK-CITABILITY-001 | MINOR | check:citability | single-source (low) |
| CHECK-CITABILITY-002 | MINOR | check:citability | single-source (low) |
| CITATIONS-005 | MINOR | citations | single-source (low) |
| CLAIM-002 | MINOR | claim-graph | single-source (low) |
| EVIDENCE-004 | MINOR | evidence | single-source (low) |
| EVIDENCE-005 | MINOR | evidence | single-source (low) |
| METHODOLOGY-003 | MINOR | methodology | single-source (low) |
| METHODOLOGY-004 | MINOR | methodology | single-source (low) |
| METHODOLOGY-005 | MINOR | methodology | single-source (low) |
| METHODOLOGY-006 | MINOR | methodology | single-source (low) |
| METHODOLOGY-007 | MINOR | methodology | single-source (low) |
| METHODOLOGY-010 | MINOR | methodology | single-source (low) |
| REPRODUCIBILITY-003 | MINOR | reproducibility | single-source (low) |
| REPRODUCIBILITY-004 | MINOR | reproducibility | single-source (low) |
| STATISTICS-003 | MINOR | statistics | single-source (low) |

## Judge disagreements

No disagreements were recorded.

## Claim coverage

- Claims detected: 11 (9 major)
- Verified: 6
- Partially supported: 1
- Unsupported: 2
- Unverified: 2
- Evidence coverage: 66.7%

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

### [ADVERSARIAL-001] Raw per-scenario response artifacts needed to audit the headline results are not supplied

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** README.md, 'Paper and evidence' and 'Usage'; evidence/20260713T191740Z/verdicts.json; paper/v3/main.tex, §4 'CONTAM-Bench' and §5.3
- **Confidence:** 0.98
- **Reported by:** adversarial

The manuscript says every run persists raw prompts, injected memories, responses, and verdicts, but the supplied evidence files contain only aggregate reports, metadata, queues, and verdict summaries. The supplied verdicts.json records judge evidence but not the underlying subject responses, so an evaluator cannot independently verify whether the verdicts or retrieval assertions match the actual outputs. This prevents reproduction of the main response-level results from the provided artifact.

Evidence:

- README.md: “Each evidence directory contains the raw per-scenario artifacts (prompts, injected memories, gate decisions, responses), verdicts.json, validation_report.md, and defects.md”
- paper/v3/main.tex, §4: “every run artifact, including raw prompts, injected memory, responses, and judge verdicts, is persisted as JSON for audit”
- The supplied file inventory for evidence/20260713T191740Z contains no CB-*.json per-scenario artifact files.
- evidence/20260713T191740Z/verdicts.json contains verdicts and scorer evidence, but no subject-response text or prompt artifacts.

**Recommendation:** Supply the exact frozen CB-*.json artifacts, or remove claims that the headline response-level results can be independently audited from this release.

### [ADVERSARIAL-002] The manuscript claims a corrected review report that contradicts the supplied frozen report

- **Severity:** MAJOR
- **Category:** artifact discrepancy
- **Location:** paper/v3/main.tex, §5.3; evidence/20260713T191740Z/validation_report.md, 'Flagged for human review'; evidence/20260713T191740Z/defects.md, D8; report/FINAL-AUDIT.md
- **Confidence:** 0.99
- **Reported by:** adversarial

The manuscript states that the rendered report identifies flagged rows by repetition and artifact hash. The supplied v0.3 validation report instead repeats indistinguishable scenario/configuration/round labels, and the accompanying defect record explicitly identifies this as an unresolved defect. This discrepancy makes the stated auditability and evidence lineage inaccurate.

Evidence:

- paper/v3/main.tex, §5.3: “The rendered report now labels its machine-only and human-consensus tables separately and identifies review rows by repetition and artifact hash.”
- evidence/20260713T191740Z/validation_report.md, 'Flagged for human review': entries are formatted as “CB-VAL-004 × arm_gate round 1” and repeat across repetitions without repetition or artifact hash.
- evidence/20260713T191740Z/defects.md, D8: “Human-review register omits repetition identifiers” and “the report is ambiguous.”
- report/FINAL-AUDIT.md, 'Scientific readiness': independent scoring assessment remains open.

**Recommendation:** Either provide the corrected report and its provenance, or revise the manuscript to describe the supplied report as ambiguous and retain D8 as an active limitation.

### [ARCHIVAL-001] Reported evidence is referenced by mutable tags and repository paths rather than an immutable version-specific identifier

- **Severity:** MAJOR
- **Category:** identity and archival
- **Location:** paper/v3/main.tex, Section 5 and Table 2 (Evidence lineage); README.md, 'Paper and evidence' and 'Citation' sections
- **Confidence:** 0.97
- **Reported by:** archival

The paper reports results from multiple evidence releases, but identifies them only by repository-relative paths and Git tags. No commit SHA, version-specific DOI, or Software Heritage identifier is supplied for the exact artifacts underlying each table. An annotated Git tag and a GitHub repository are not sufficient evidence that the cited contents cannot later be changed or deleted.

Evidence:

- paper/v3/main.tex, Table 2: “v0.2 ablation ... v0.2-ablation”, “v0.3 repeated audit ... v0.3-repeated-ablation”, and “v0.3.1 corrections ... v0.3.1-evidence-corrections”
- paper/v3/main.tex, Section 5: “Complete run artifacts are published at \texttt{evidence/20260713T084130Z} ... frozen at tag \texttt{v0.2-ablation}.”
- README.md: “Runs cited in publications are copied to \`evidence/<timestamp>/\` and frozen under an annotated tag”; the cited locations are GitHub repository paths, not immutable identifiers.

**Recommendation:** Record the exact commit SHA for every evidence release used by the paper and archive each release independently with a version-specific DOI or Software Heritage identifier. State explicitly which DOI resolves to which release and paper version.

### [ARCHIVAL-002] The supplied artifact does not contain the evidence files needed to retrieve or verify the headline results

- **Severity:** MAJOR
- **Category:** data and artifact availability
- **Location:** Provided file list; README.md, 'Paper and evidence' section; paper/v3/main.tex, Table 2 and Sections 5.1–5.3
- **Confidence:** 0.99
- **Reported by:** archival

The paper's central numerical results depend on raw runs, verdicts, reports, and correction queues, but the supplied artifact contains only the citation, licensing, README, reproduction protocol, and LaTeX manuscript. The manuscript and README point to evidence directories that are absent from the provided file list. Thus, a reader of this artifact cannot independently retrieve the artifacts supporting the tables.

Evidence:

- Provided file list contains CITATION.cff, LICENSING.md, README.md, docs/REPRODUCTION.md, and paper/v3/main.tex, but no \`evidence/\` directory, raw JSON, verdicts, or validation reports.
- README.md: “Each evidence directory contains the raw per-scenario artifacts ... \`verdicts.json\`, \`validation_report.md\`, and \`defects.md\`.”
- paper/v3/main.tex, Section 5.2: “Complete run artifacts are published at \texttt{evidence/20260713T084130Z} ... Every number in this section is recomputable from those artifacts.”

**Recommendation:** Include or independently archive the exact evidence releases, including raw artifacts, verdicts, reports, correction bundle, and review queue, and link them using immutable version-specific identifiers. If the artifact package intentionally omits them, label the supplied package as manuscript-only rather than reproducible evidence.

### [CITATIONS-001] Repeated-audit denominator is arithmetically inconsistent

- **Severity:** MAJOR
- **Category:** experimental accounting
- **Location:** paper/v3/main.tex, Section 4.4 'Repeated-evaluation audit and scoring defects'; Table 3 caption and surrounding text
- **Confidence:** 0.99
- **Reported by:** citations

The paper states that the repeated audit used nine scenarios, seven configurations, and five repetitions, which implies 315 scenario-configuration-rounds. It nevertheless reports 350 scored rounds and derives the 14.9% review rate from 52/350. The same inconsistency appears in the reported subject-call count. This prevents the reported aggregate accounting from being recomputed as stated and may change the review rate and any aggregate interpretation.

Evidence:

- "the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds"
- "Fifty-two of the 350 rounds (14.9%) required human review"
- "The repeated audit used 660 API calls: 350 subject calls, 135 gate calls, and 175 judge calls."
- Table 3 lists seven configurations and four scenario columns, while Table 2 and the surrounding text define nine scenarios; nine × seven × five = 315, not 350.

**Recommendation:** Reconcile the scenario, configuration, repetition, and API-call counts against the persisted run manifest, and correct the denominator, percentages, and call accounting. If additional rounds were included, identify them explicitly and explain why they are not represented by the stated nine-by-seven-by-five design.

### [CITATIONS-002] Headline results cannot be independently checked from the supplied artifact

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex, Section 4 'Ablation Study', footnote to the first paragraph; Sections 4.4 and 8.1 'Reproducibility'
- **Confidence:** 0.97
- **Reported by:** citations

The main results depend on external evidence releases and a repository, but the supplied artifact contains only main.tex and references.bib. No YAML manifests, raw prompts, responses, retrieval traces, judge outputs, review queue, hashes, or run reports are included here. Consequently, the manuscript's matrix and repeated-audit claims are unverified from the provided material, despite the assertion that every number is recomputable.

Evidence:

- "Complete run artifacts are published at evidence/20260713T084130Z in the benchmark repository ... Every number in this section is recomputable from those artifacts."
- "The v0.3 evidence now includes a separately versioned queue for all 52 unresolved artifact rounds"
- "The benchmark and code are available at https://github.com/arananet/contam-bench."
- The supplied files are only paper/v3/main.tex and paper/v3/references.bib; none of the cited evidence files or run artifacts is present.

**Recommendation:** Provide the exact evidence release or a complete archival supplement containing the manifests, raw model and judge artifacts, retrieval traces, scoring outputs, review queue, and file hashes, or label the reported results as externally hosted and not independently verifiable from this artifact.

### [CITATIONS-003] Intended identifier-reuse claim has no supporting experiment or evidence

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** paper/v3/main.tex, Sections 3–4 and 7; no identifier-reuse or MCP experiment is specified
- **Confidence:** 0.98
- **Reported by:** citations

The intended claim that reusing an identifier overwrites shared mappings but is retained in separate MCP instances is not operationalized or reported anywhere in the manuscript. The described benchmark concerns memory contamination scenarios, namespaces, provenance, TTL, retrieval gates, and raw fidelity; it provides no identifier-reuse scenario, MCP configuration, output, or trace. The claim is therefore unverified and cannot be narrowed from the supplied text beyond saying that no evidence is presented here.

Evidence:

- The benchmark scenario description lists seeded items with "content, source, age in days, domain, and fact class" but does not specify identifier reuse or MCP instances.
- Table 2's seven configurations cover naive, namespacing, provenance, TTL, gate, raw, and governed arms; none is an identifier-reuse or MCP-instance condition.
- The results sections report drift, provenance, scope bleed, staleness, recursion, summarization, and controls, but contain no identifier-overwrite result.

**Recommendation:** Remove this claim from the paper or add a separately specified and evidenced experiment covering the fixed write order, shared mappings, separate MCP instances, and the observed identifier behavior.

### [CITATIONS-004] Intended host-handler-dependent tool-rejection claim has no supporting evidence

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** paper/v3/main.tex, Section 4.3 'Models and determinism'; no tool-rejection experiment elsewhere in the manuscript
- **Confidence:** 0.98
- **Reported by:** citations

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default is not discussed or tested in the manuscript. The model and benchmark description mentions subject, judge, relevance-gate, retrieval, and memory configurations, but no tool-rejection protocol, SDK version, host handler, or comparative result. The claim is therefore unverified from the artifact.

Evidence:

- "The subject model under test is claude-sonnet-4-6 at temperature 0; the judge and relevance gate are claude-haiku-4-5."
- "The reported validation runs use TF-IDF cosine similarity" and the surrounding configuration descriptions discuss memory retrieval, not tool rejection.
- No occurrence or section in main.tex specifies an SDK default handler, installed host handler, tool rejection test, or corresponding result.

**Recommendation:** Remove the claim from the evaluated claims, or provide a separate experiment documenting the SDK version/default behavior, installed host handler, test prompts, tool outcomes, and comparison conditions.

### [CLAIM-001] Unsupported claim: The paper's seven-configuration pilot establishes a general mitigation architect

- **Severity:** MAJOR
- **Category:** claims/unsupported
- **Location:** paper/v3/main.tex, §5.6, §6, and Conclusion
- **Confidence:** 0.90
- **Reported by:** claim-graph

The artifact explicitly disclaims this stronger claim; the supported conclusion is only a small, mechanism-specific pilot observation.

Evidence:

- paper/v3/main.tex, §6: “The ablation motivates constraints, not an efficacy ordering.”
- paper/v3/main.tex, Conclusion: “They motivate further tests of memory contracts, not a validated general mitigation architecture.”
- evidence/20260713T191740Z/defects.md, Evidence scope: one model, five repetitions, machine-only adjudication unavailable.

**Recommendation:** Provide evidence for the claim or remove it.

### [EVIDENCE-001] Identifier-reuse/MCP-isolation claim is not evidenced

- **Severity:** MAJOR
- **Category:** missing evidence
- **Location:** Artifact-wide; relevant supplied implementation is limited to src/memory_store.py and the listed scenario/evidence files
- **Confidence:** 0.99
- **Reported by:** evidence

The intended claim that reusing an identifier overwrites entries in shared mappings but remains isolated across separate MCP instances cannot be evaluated from the supplied artifact. The repository contents contain no MCP implementation, identifier-reuse experiment, or result record establishing this behavior. This is an unverified claim rather than a plausible inference from the memory-contamination benchmark.

Evidence:

- src/memory_store.py contains an in-memory MemoryStore with append-based seed/write-back behavior, but no identifier-keyed shared mapping or MCP-instance isolation experiment.
- The supplied evidence releases contain contamination scenarios and verdicts, but no table, figure, script, or result file testing identifier reuse across shared versus separate MCP instances.
- README.md describes the study as a persistent-memory ablation benchmark and does not report an MCP identifier-reuse experiment.

**Recommendation:** Either remove this intended claim from the evaluated claims or provide a separately identified experiment with the identifier semantics, shared/separate instance setup, fixed write order, and persisted results. The narrowest currently supported wording is that no identifier-reuse/MCP-isolation conclusion is established by this artifact.

### [EVIDENCE-003] Manuscript claims the rendered report identifies review rows, but the frozen report does not

- **Severity:** MAJOR
- **Category:** reproducibility/reporting contradiction
- **Location:** paper/v3/main.tex, §5.3 “Repeated-evaluation audit and scoring defects”; evidence/20260713T191740Z/validation_report.md, “Flagged for human review”; evidence/20260713T191740Z/defects.md, D8
- **Confidence:** 0.99
- **Reported by:** evidence

The manuscript states that the rendered report identifies review rows by repetition and artifact hash. The supplied frozen v0.3 validation report instead lists repeated rows without either field, and the associated defect record explicitly identifies this as D8. Thus the manuscript overstates the state of the supplied reporting artifact.

Evidence:

- paper/v3/main.tex, §5.3: “The rendered report now labels its machine-only and human-consensus tables separately and identifies review rows by repetition and artifact hash.”
- evidence/20260713T191740Z/validation_report.md, “Flagged for human review”: rows are formatted like “CB-VAL-004 × arm_gate round 1” and omit repetition and artifact hash.
- evidence/20260713T191740Z/defects.md, D8: “Human-review register omits repetition identifiers” and “the report is ambiguous.”

**Recommendation:** Correct the manuscript to distinguish the frozen report from later planned or generated reporting changes. Do not claim that the supplied rendered report includes repetition/hash identifiers unless the corresponding report artifact is supplied and verified.

### [METHODOLOGY-001] The provenance ablation does not isolate provenance tagging

- **Severity:** MAJOR
- **Category:** experimental design
- **Location:** paper/v3/main.tex, Section 5.6 'Attribution: what the cells support'; Section 7.1 'Validity statements'; Table 3
- **Confidence:** 0.99
- **Reported by:** methodology

The provenance arm changes more than source attribution: its tag exposes source, age, and domain. Therefore the five clean outcomes cannot identify provenance tags as the causal mitigation, especially because the stale age is itself potentially informative. The manuscript acknowledges this confound, but the headline provenance interpretation still presents the tag arm as evidence for the provenance finding.

Evidence:

- paper/v3/main.tex, Section 5.6: 'the provenance tag as implemented carries age and domain metadata ([source: user | age: 200d | domain: personal]), so the provenance arm also resolved staleness because the subject discounted the 200-day-old fact by its visible age.'
- paper/v3/main.tex, Section 7.1: 'The provenance arm is confounded: its tag emits source, age, and domain together, so its staleness result cannot be attributed to source attribution alone.'
- paper/v3/main.tex, Table 3: 'provenance tags, raw fidelity, and the governed bundle are each 5/0/0'

**Recommendation:** Report the provenance result explicitly as an effect of a bundled metadata intervention, or provide a pure-factor source-only ablation before attributing the result to provenance tagging.

### [METHODOLOGY-002] The canonical response outcomes have no independent ground-truth resolution for 52 rounds

- **Severity:** MAJOR
- **Category:** evaluation methodology
- **Location:** paper/v3/main.tex, Section 5.2 'Repeated-evaluation audit and scoring defects'; Section 7.1; spec/metrics.md, 'Adjudication layer'
- **Confidence:** 0.99
- **Reported by:** methodology

The repeated audit excludes 52 of 350 rounds because deterministic and judge verdicts disagree, and the artifact contains no human verdicts. This is correctly disclosed, but it leaves the headline machine-only rates and comparisons potentially sensitive to unresolved cases; assertion versus mention is central to the contamination criterion. The manuscript should not use these rates as if they were validated contamination outcomes.

Evidence:

- paper/v3/main.tex, Section 5.2: 'Fifty-two of the 350 rounds (14.9%) required human review.'
- paper/v3/main.tex, Section 5.2: 'Neither direction establishes which scorer is correct without independent assessment.'
- paper/v3/main.tex, Section 5.2: 'the queue ... contains no human verdicts.'
- spec/metrics.md, 'Adjudication layer': 'Ties and single-adjudicator records remain unresolved; no rate silently mixes machine and human layers.'

**Recommendation:** Present sensitivity bounds or separate resolved and unresolved analyses for every load-bearing comparison, and complete the pre-specified blinded independent adjudication before making response-layer efficacy claims.

### [METHODOLOGY-008] The intended identifier-reuse claim is unsupported by the supplied artifact

- **Severity:** MAJOR
- **Category:** claim-evidence mismatch
- **Location:** All supplied files; no corresponding section or scenario present
- **Confidence:** 0.99
- **Reported by:** methodology

The intended claim that reusing an identifier overwrites shared mappings but is retained in separate MCP instances has no corresponding scenario, experiment, result table, or discussion in the supplied files. It is therefore unverified and cannot be included as a finding of the paper.

Evidence:

- The supplied scenario files cover semantic drift, provenance collapse, scope bleed, temporal staleness, recursion, summarization loss, and two controls; none tests identifier reuse or MCP-instance retention.
- paper/v3/main.tex, Section 3 taxonomy: the seven documented classes do not include identifier reuse or MCP mapping semantics.
- spec/schema.yaml and spec/full-benchmark.plan.yaml: no identifier-reuse or MCP-instance scenario is listed.

**Recommendation:** Remove this claim from the evaluated contribution, or add a dedicated, reproducible experiment with shared versus separate MCP instances and explicit overwrite/retention assertions.

### [METHODOLOGY-009] The intended host-handler rejection claim is unsupported by the supplied artifact

- **Severity:** MAJOR
- **Category:** claim-evidence mismatch
- **Location:** All supplied files; no corresponding section or scenario present
- **Confidence:** 1.00
- **Reported by:** methodology

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default is not evaluated in the manuscript or supplied scenarios. No tool-rejection experiment, host-handler comparison, SDK configuration, or result is present.

Evidence:

- The supplied files contain memory scenarios and memory configurations only; no tool-calling or host-handler scenario is present.
- paper/v3/main.tex contains no section or result describing model-only tool rejection, installed host handlers, or SDK-default behavior.
- spec/full-benchmark.plan.yaml lists retrieval backends, models, gates, baselines, and utility oracles, but no tool-rejection experiment.
- The supplied source files implement memory retrieval, judging, adjudication, and benchmarking, but do not contain a model-only tool rejection experiment or host-handler comparison.
- tests/test_integration.py and tests/test_ci_workflows.py cover benchmark execution and CI configuration, not SDK-default versus installed-host-handler tool behavior.
- The supplied paper, paper/v3/main.tex, discusses memory contamination and retrieval gates but makes no evidence-backed tool-handler comparison.

**Recommendation:** Do not state this claim as an evaluated result. Add a controlled comparison of the SDK default and installed host handler, with the same model prompt and explicit rejection outcomes, if the claim is in scope.

### [REPO-CONSISTENCY-001] Reported empirical results cannot be verified from the supplied artifact

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** paper/v3/main.tex §5.3–§5.5; README.md “Paper and evidence” and “Repository layout”
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The manuscript reports headline repeated-audit results, including 350 scored rounds, 52 unresolved rounds, and per-cell outcome distributions, but the supplied files contain neither the referenced evidence directories nor the scenario manifests required to run the harness. README.md claims that frozen evidence is available under evidence/20260713T191740Z and that scenarios are under scenarios/validation/ and scenarios/controls/, but none of those files are included in the supplied artifact. Consequently, the reported results are unverified from the submitted bundle.

Evidence:

- paper/v3/main.tex §5.3: “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds”
- paper/v3/main.tex Table 5 / §5.3: “The provenance separation persists without flags: provenance tags, raw fidelity, and the governed bundle are each 5/0/0”
- README.md, “Paper and evidence”: “v0.3 repeated audit (7×9×5) | evidence/20260713T191740Z/”
- README.md, “Repository layout”: “scenarios/validation/ | 7 hand-authored contamination scenarios” and “evidence/ | Frozen runs cited in publications”
- Supplied artifact file inventory: no evidence/ directory, no scenarios/validation/ directory, no scenarios/controls/ directory, and no persisted verdicts or run artifacts are provided

**Recommendation:** Supply the exact frozen scenario manifests, raw run artifacts, verdicts, and reports referenced by the manuscript, or restrict the manuscript to implementation-level claims and explicitly mark all numerical results as unavailable in this artifact bundle.

### [REPO-CONSISTENCY-002] The default executable configuration set does not reproduce the manuscript’s seven-configuration experiment

- **Severity:** MAJOR
- **Category:** configuration mismatch
- **Location:** paper/v3/main.tex §5; spec/configs.yaml; src/harness.py main()
- **Confidence:** 0.98
- **Reported by:** repo-consistency

The manuscript describes the reported ablation as seven configurations, while the supplied configuration file defines eight configurations because arm_gate_preserve_pairs is present. The harness defaults to every key in spec["configs"], so a default invocation runs the experimental eighth arm rather than the manuscript’s seven-arm frozen matrix. No supplied command or configuration pins the reported run to the seven frozen arms.

Evidence:

- paper/v3/main.tex §5: “the run reported here executes nine scenarios ... against seven configurations”
- spec/configs.yaml: “arm_gate_preserve_pairs” is defined under configs, with the comment “It is not a v0.2 result and must be reported separately”
- README.md: “The active development configuration also includes an experimental guarded-gate arm ... it is not part of frozen v0.3 evidence”
- src/harness.py, main(): `config_names = args.config or list(spec["configs"])`, which includes arm_gate_preserve_pairs by default

**Recommendation:** Make the frozen seven-arm configuration explicit in the executable entry point or release configuration, and document the exact command/configuration used for the paper’s results. Keep the experimental arm in a separately named, non-default configuration if it is not part of the evidence release.

### [REPO-CONSISTENCY-003] The identifier-overwrite/MCP claim has no counterpart in the supplied artifact

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** Artifact-wide; especially src/memory_store.py and tests/test_memory_store.py
- **Confidence:** 0.99
- **Reported by:** repo-consistency

One author-intended claim concerns identifier reuse, overwrite behavior in shared mappings, and retention in separate MCP instances. The supplied manuscript, specifications, source files, and tests contain no MCP implementation, identifier-overwrite experiment, shared-mapping model, or separate-instance test. The claim is therefore unsupported by this artifact and cannot be narrowed to a supported empirical conclusion from the available evidence.

Evidence:

- Author-intended claim: “Under the tested configurations and one fixed write order, reusing an identifier overwrites in the shared mappings and is retained in separate MCP instances.”
- src/memory_store.py: `MemoryEntry` has `seed_id`, but `MemoryStore.seed()` only appends entries and contains no overwrite or shared-mapping behavior
- src/memory_store.py: `MemoryStore` is a single in-memory list and has no MCP-instance abstraction
- tests/test_memory_store.py: tests cover namespacing, TTL, fidelity, tags, write-back, and empty stores, but contain no identifier-reuse or MCP-instance test
- Supplied artifact file inventory: no MCP adapter, shared mapping implementation, or corresponding experiment/evidence file

**Recommendation:** Remove the claim from the evaluated scope unless the MCP implementation, controlled experiment, and persisted evidence are supplied. If retained, narrow it only to the exact tested implementation and write order supported by those artifacts.

### [REPO-CONSISTENCY-004] The host-handler-dependent model-only tool-rejection claim is unsupported

- **Severity:** MAJOR
- **Category:** unsupported claim
- **Location:** Artifact-wide; especially src/llm.py and tests/
- **Confidence:** 0.99
- **Reported by:** repo-consistency

The second author-intended claim concerns model-only tool rejection and dependence on an installed host handler rather than the SDK default. The supplied code only wraps Anthropic message calls and implements memory retrieval, gating, judging, and scoring; it contains no tool-rejection experiment, host handler, SDK-default comparison, or tool-call test. The claim is therefore unverified and unsupported by the submitted artifact.

Evidence:

- Author-intended claim: “Model-only tool rejection depends on the installed host handler, not the SDK default.”
- src/llm.py: `CountingClient.complete()` calls `self.client.messages.create(...)` and has no tool definitions, host-handler logic, or rejection comparison
- src/retrieval.py and src/harness.py: the implemented model calls concern relevance gating and subject responses, not tool rejection
- Supplied tests: no test refers to tool rejection, an installed host handler, or an SDK-default behavior

**Recommendation:** Remove the claim from this artifact’s conclusions, or provide the host-handler implementation, SDK-default control, experimental protocol, and persisted results needed to support it.

### [REPRODUCIBILITY-001] Raw per-scenario evidence required for audit and adjudication is missing

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** README.md, section 'Paper and evidence'; src/adjudication.py, functions `_artifact_index` and `generate_packets`; evidence/20260713T191740Z/; supplied file inventory
- **Confidence:** 0.99
- **Reported by:** reproducibility

The manuscript and README say that frozen evidence contains raw prompts, injected memories, gate decisions, responses, and verdicts, and the adjudication code requires per-artifact JSON files to generate blinded packets. Those per-scenario artifact files are not among the supplied files: the evidence directories contain only metadata, reports, defects, verdicts, and the queue. Consequently, an independent researcher cannot inspect the response text or retrieval traces, regenerate the 52 review packets, or verify the judge evidence underlying the headline comparisons.

Evidence:

- README.md: “Each evidence directory contains the raw per-scenario artifacts (prompts, injected memories, gate decisions, responses), `verdicts.json`, `validation_report.md`, and `defects.md`”
- src/adjudication.py: `_artifact_index` scans `evidence_dir` for files whose names start with `CB-` and reads each artifact's `response` and `scoring` fields
- evidence/20260713T191740Z/adjudications.json`: 52 pending artifact hashes are queued, but no corresponding `CB-*.json` evidence files are supplied
- paper/v3/main.tex, §5.3: “Of 350 scored rounds, 52 remain unresolved pending human review.”

**Recommendation:** Include the immutable per-scenario JSON artifacts, or provide an independently verifiable archive containing them, before presenting the results as auditable or seeking human adjudication. Ensure the supplied evidence directory is sufficient for `src.adjudication packets` to run.

### [REPRODUCIBILITY-002] Main experiment cannot be exactly rerun from the environment specification

- **Severity:** MAJOR
- **Category:** reproducibility
- **Location:** requirements.txt; docs/REPRODUCTION.md, sections 'Independence' and 'Prerequisites'; evidence/20260713T191740Z/run_meta.json; paper/v3/main.tex, §5.3 and §Discussion/Limitations
- **Confidence:** 0.98
- **Reported by:** reproducibility

The main experiment depends on live Anthropic model calls, but the artifact provides only lower-bound dependency constraints and no lockfile, container, exact commit identifier for the frozen runs, or API/model-version snapshot. The reproduction protocol itself asks reviewers to record a commit SHA and exact environment, while the frozen `run_meta.json` records models and sampling parameters but not the commit or installed package versions. Since the paper explicitly reports model-mediated results and acknowledges output variance, this blocks an exact independent rerun of the headline ablation and repeated audit.

Evidence:

- requirements.txt: `anthropic>=0.116`, `PyYAML>=6.0`, `jsonschema>=4.0`, `scikit-learn>=1.3`, and other unpinned lower bounds
- evidence/20260713T191740Z/run_meta.json: records model names, temperatures, repetitions, and call counts, but no commit SHA, Python version, package versions, or hardware/environment image
- docs/REPRODUCTION.md: “the reviewer reports the exact commit SHA, environment, commands, elapsed time, outputs, and deviations”
- paper/v3/main.tex, §Discussion/Limitations, “Temperature~0 sampling reduces but does not remove output variance”

**Recommendation:** Archive the exact commit, Python and library versions, dependency lockfile or container digest, complete commands, and model/API identifiers used for each frozen run. Distinguish artifact reanalysis from live reruns in the paper.

### [REPRODUCIBILITY-005] The intended identifier-overwrite/MCP-instance claim is unsupported in the artifact

- **Severity:** MAJOR
- **Category:** unsupported_claim
- **Location:** Artifact-wide; no supporting location supplied
- **Confidence:** 0.99
- **Reported by:** reproducibility

The intended claim that reusing an identifier overwrites entries in shared mappings but is retained in separate MCP instances is not stated or tested in the supplied manuscript, scenarios, reports, source files, or evidence records. No MCP implementation, identifier-reuse scenario, or corresponding result is provided. The claim is therefore unverified and cannot be included as an empirical conclusion.

Evidence:

- The supplied manuscript's taxonomy and results sections discuss memory scope, provenance, TTL, gating, raw fidelity, and recursion, but contain no MCP-instance or identifier-overwrite experiment
- The supplied scenario inventory contains CB-VAL-001 through CB-VAL-009; none is an identifier-reuse or shared-mapping/MCP-instance scenario
- No supplied source or evidence file defines an MCP instance comparison or reports such a result

**Recommendation:** Remove the claim from the intended claims and conclusions, or add a separately specified and executed experiment with its implementation, commands, artifacts, and results. On the current evidence, no narrower empirical wording is supported.

### [REPRODUCIBILITY-006] The intended host-handler/model-only tool-rejection claim is unsupported in the artifact

- **Severity:** MAJOR
- **Category:** unsupported_claim
- **Location:** Artifact-wide; no supporting location supplied
- **Confidence:** 0.99
- **Reported by:** reproducibility

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default has no supporting experiment or artifact. The supplied code and paper concern memory retrieval, scoring, and adjudication; they do not implement or test tool rejection, host handlers, or SDK defaults. The claim is unverified.

Evidence:

- paper/v3/main.tex: no section, result, scenario, or citation addresses model-only tool rejection or installed host handlers
- src/: supplied modules cover harness, retrieval, memory store, judging, metrics, and adjudication; no host-handler/tool-rejection implementation is supplied
- The supplied scenario inventory and evidence reports contain no tool-rejection result

**Recommendation:** Remove the claim unless a separate tool-handling experiment and its reproducible artifacts are supplied. No narrower wording is supported by the current artifact.

### [STATISTICS-001] Intended identifier-overwrite claim is not evidenced in the supplied artifact

- **Severity:** MAJOR
- **Category:** statistics
- **Location:** AUTHOR'S INTENDED CLAIMS; src/memory_store.py; paper/v3/main.tex
- **Confidence:** 0.99
- **Reported by:** statistics

The intended claim that reusing an identifier overwrites entries in shared mappings but is retained in separate MCP instances is not supported by any reported experiment, sample, run count, variance, statistical comparison, or implementation artifact in the supplied files. The visible memory implementation uses seed IDs and an in-memory list, but no shared-mapping/MCP-instance experiment is described or quantified.

Evidence:

- AUTHOR'S INTENDED CLAIMS: “Under the tested configurations and one fixed write order, reusing an identifier overwrites in the shared mappings and is retained in separate MCP instances.”
- src/memory_store.py, MemoryStore: entries are stored in `self.entries: list[MemoryEntry]`; no shared-mapping or separate-MCP-instance experiment is present.
- paper/v3/main.tex, Sections 5–7: the reported experiments concern nine scenarios, seven memory configurations, retrieval, response verdicts, and controls; no identifier-overwrite result is reported.

**Recommendation:** Do not present this as an established quantitative result unless a documented identifier-overwrite experiment with explicit runs, conditions, and outcomes is supplied; otherwise mark it unverified or remove it.

### [STATISTICS-002] Host-handler-dependent tool-rejection claim is not evidenced

- **Severity:** MAJOR
- **Category:** statistics
- **Location:** AUTHOR'S INTENDED CLAIMS; paper/v3/main.tex; evidence/20260713T191740Z/validation_report.md
- **Confidence:** 0.99
- **Reported by:** statistics

The intended claim that model-only tool rejection depends on the installed host handler rather than the SDK default has no supporting experiment or quantitative evidence in the supplied artifact. The manuscript and evidence focus on memory contamination, retrieval, gates, and scoring; no host-handler comparison or SDK-default baseline is reported.

Evidence:

- AUTHOR'S INTENDED CLAIMS: “Model-only tool rejection depends on the installed host handler, not the SDK default.”
- paper/v3/main.tex, Abstract and Sections 5–7: reported measurements are memory configurations, contamination verdicts, retrieval assertions, gate calls, and API spend; no tool-rejection or host-handler condition appears.
- evidence/20260713T191740Z/validation_report.md, Config comparison and Relevance-gate observability: the reported metrics contain contamination, recursion, provenance, staleness, retention, retrieval, and gate-call results, but no tool-rejection measurement.

**Recommendation:** Treat this claim as unverified and do not include it among empirical conclusions without a controlled host-handler-versus-SDK comparison with run counts and outcome definitions.

### [ADVERSARIAL-003] Machine-only rates exclude the disagreements most relevant to the central mitigation conclusions

- **Severity:** MINOR
- **Category:** scoring validity
- **Location:** evidence/20260713T191740Z/defects.md, D7 and D9; evidence/20260713T191740Z/validation_report.md, 'Config comparison' and 'Human-adjudicated comparison'; paper/v3/main.tex, abstract and §5.3
- **Confidence:** 0.97
- **Reported by:** adversarial

The 52 unresolved rounds are not randomly distributed: they include all 20 staleness comparisons for four configurations and 29 of 35 seeded-recursion rounds. Excluding these rounds from both numerator and denominator means the reported rates cannot establish comparative response-level efficacy for those mechanisms. The manuscript explicitly acknowledges this, so the issue is declared rather than hidden; nevertheless, the abstract and conclusion should not be read as stronger than machine-only, within-case observations.

Evidence:

- evidence/20260713T191740Z/defects.md, D7: “Fifty-two of the 350 scored rounds resolved to needs_human_review,” including 20 staleness and 29 seeded-recursion disagreements.
- evidence/20260713T191740Z/validation_report.md, 'Human-adjudicated comparison': “unavailable (adjudications_file_missing); machine verdicts remain authoritative.”
- paper/v3/main.tex, abstract: “Of 350 scored rounds, 52 remain unresolved pending human review.”
- paper/v3/main.tex, §5.3: “Neither direction establishes which scorer is correct without independent assessment.”

**Recommendation:** Keep the limitation prominent wherever rates are interpreted, avoid ranking arms on the affected response-level mechanisms, and do not present the machine-only rates as validated mitigation efficacy.

### [ADVERSARIAL-004] The frozen run metadata does not conform to the current run-metadata schema

- **Severity:** MINOR
- **Category:** reproducibility
- **Location:** spec/run-meta.schema.yaml; evidence/20260713T191740Z/run_meta.json; evidence/20260713T191740Z/defects.md, D10
- **Confidence:** 0.95
- **Reported by:** adversarial

The current schema requires harness_call_counts, harness_total_calls, judge_total_calls, pipeline_call_counts, and pipeline_total_calls. The supplied v0.3 run_meta.json provides only the legacy call_counts and total_calls fields plus repetitions. This weakens the claimed machine-readable provenance and leaves the 485-versus-660 call accounting dependent on later report logic rather than the frozen metadata itself.

Evidence:

- spec/run-meta.schema.yaml, top-level required fields: harness_call_counts, harness_total_calls, judge_total_calls, pipeline_call_counts, and pipeline_total_calls.
- evidence/20260713T191740Z/run_meta.json: contains “call_counts”: {“subject”: 350, “gate”: 135} and “total_calls”: 485, but not the newer required fields.
- evidence/20260713T191740Z/defects.md, D10: persisted counts are 350 subject, 135 gate, and 175 judge, totaling 660, while run_meta.json reports only 485 harness calls.

**Recommendation:** Publish a versioned, schema-valid metadata correction alongside the frozen release, explicitly preserving the legacy file and documenting which metadata layer is authoritative.

### [ARCHIVAL-003] The bibliography required to resolve the paper's citations is absent from the supplied artifact

- **Severity:** MINOR
- **Category:** citation metadata
- **Location:** paper/v3/main.tex, bibliography declarations and cited sections; provided file list
- **Confidence:** 0.99
- **Reported by:** archival

The manuscript invokes a BibTeX bibliography file named \`references\`, but no references.bib file is included in the supplied files. Consequently, cited works cannot be unambiguously identified from this artifact alone, even though the manuscript uses citation keys throughout.

Evidence:

- paper/v3/main.tex, end of document: “\bibliographystyle{plain}” and “\bibliography{references}”
- paper/v3/main.tex, Related Work section: citations such as “\cite{chen2024agentpoison}”, “\cite{dong2025minja}”, and “\cite{weng2026harness}” appear without bibliographic entries in the supplied files.
- Provided file list contains no \`references.bib\` or rendered reference list.

**Recommendation:** Include the bibliography source or a rendered reference list with complete titles, authors, venues, and persistent identifiers where available.

### [ARCHIVAL-004] Repository and code licensing metadata are internally ambiguous

- **Severity:** MINOR
- **Category:** licensing
- **Location:** CITATION.cff; LICENSING.md; README.md, License section
- **Confidence:** 0.94
- **Reported by:** archival

CITATION.cff declares CC-BY-4.0 without distinguishing the licensed object, while LICENSING.md states that code is Apache-2.0 and manuscript, figures, data, and evidence are CC-BY-4.0. A reader using CITATION.cff alone could interpret CC-BY-4.0 as the repository-code licence, creating ambiguity about code reuse.

Evidence:

- CITATION.cff: “repository-code: https://github.com/arananet/contam-bench” followed by “license: CC-BY-4.0”.
- LICENSING.md: “Code — harness, scripts, tests and any software in this repository: Apache-2.0” and “Content — the manuscript, figures, data and evidence records: CC-BY-4.0.”
- README.md, License section: “Apache 2.0 (LICENSE)” without separately identifying the manuscript/data licence.

**Recommendation:** Clarify in CITATION.cff and repository documentation that Apache-2.0 applies to code and CC-BY-4.0 applies to paper, figures, data, and evidence, or provide object-specific licence metadata.

### [ARCHIVAL-005] Author affiliation metadata is not provided

- **Severity:** MINOR
- **Category:** citation metadata
- **Location:** CITATION.cff; paper/v3/main.tex, title and author block
- **Confidence:** 0.96
- **Reported by:** archival

The sole author is identified by name and ORCID, but neither CITATION.cff nor the manuscript supplies an affiliation. This does not prevent retrieval, but it weakens unambiguous author disambiguation and citation metadata completeness.

Evidence:

- CITATION.cff lists only “family-names: Arana”, “given-names: Eduardo”, and an ORCID.
- paper/v3/main.tex: “\author{Eduardo Arana}” with no affiliation declaration.

**Recommendation:** Add the author's affiliation and, where appropriate, persistent institutional identifiers to the citation metadata.

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

### [CITATIONS-005] Several prior-work assertions are uncited or only weakly sourced

- **Severity:** MINOR
- **Category:** citation support
- **Location:** paper/v3/main.tex, Sections 2 and 7
- **Confidence:** 0.94
- **Reported by:** citations

The manuscript makes claims about prior work without attaching a citation, or uses a single source to support a broader plural/general claim. These are distinct from whether the listed references exist; the supplied files do not establish that the references are fabricated, but the cited support is incomplete for the attached assertions.

Evidence:

- "subsequent work has extended the attack surface" in the 'Adversarial memory poisoning' paragraph has no citation attached.
- "Complementary diagnosis work finds most memory failures stem from irrelevant retrieval rather than memory construction" in 'Measurement of non-adversarial memory risk' has no citation attached.
- "follow-on work quantifies a passage's distracting effect as a graded severity measure" in 'Retrieval noise and context failure' has no citation attached.
- "Production platforms are converging on the same controls from the deployment side" is a plural/general claim, but the paragraph cites only Anthropic documentation.

**Recommendation:** Add citations for each specific prior-work or empirical assertion, or narrow the wording to what the cited source directly supports. For the production-platform statement, cite the additional platforms or state that the observation concerns Anthropic's documented platform only.

### [CLAIM-002] Unsupported claim: The rendered v3 report identifies unresolved review rows by repetition and artif

- **Severity:** MINOR
- **Category:** claims/unsupported
- **Location:** paper/v3/main.tex, §5.3; evidence/20260713T191740Z/validation_report.md, “Flagged for human review”
- **Confidence:** 0.90
- **Reported by:** claim-graph

The manuscript statement is contradicted by the supplied frozen report and defect record.

Evidence:

- paper/v3/main.tex, §5.3 makes the claim explicitly.
- evidence/20260713T191740Z/validation_report.md lists rows without repetition or artifact hash.
- evidence/20260713T191740Z/defects.md, D8 explicitly records the omission and ambiguity.

**Recommendation:** Provide evidence for the claim or remove it.

### [EVIDENCE-004] Causal explanation for raw fidelity preserving provenance is only partially supported

- **Severity:** MINOR
- **Category:** causal attribution
- **Location:** paper/v3/main.tex, §5.4 “Attribution: what the cells support”; scenarios/validation/cb-val-002-provenance-collapse.yaml; evidence/20260713T191740Z/validation_report.md, repeated outcomes
- **Confidence:** 0.94
- **Reported by:** evidence

The evidence supports clean machine-resolved outcomes for the raw-fidelity arm and preserves the full source sentence in raw storage, but it does not establish that loss during summarization caused the provenance failures or that raw fidelity generally preserves provenance. The paper mostly acknowledges this limitation, so the problem is limited to the residual causal implication rather than the descriptive result.

Evidence:

- paper/v3/main.tex, §5.4: “raw fidelity can preserve provenance in-band” and “This is consistent with loss of source information during summarization in this scenario, but does not establish summarization as the principal cause of provenance collapse generally.”
- evidence/20260713T191740Z/validation_report.md, Config comparison: arm_raw has provenance_error_rate 0.0; §Per-scenario verdicts show clean outcomes for the raw arm.
- scenarios/validation/cb-val-002-provenance-collapse.yaml: the raw content explicitly says “The assistant suggested...” while the summarized content omits that source detail.

**Recommendation:** Retain the result as a case-specific association and avoid causal wording beyond “the raw representation retained source information in this scenario.” A pure-factor summarization/provenance experiment is needed for a causal claim.

### [EVIDENCE-005] Machine-only results remain unresolved for 52 rounds, limiting response-layer comparisons

- **Severity:** MINOR
- **Category:** scoring validity
- **Location:** paper/v3/main.tex, abstract and §5.3/§6; evidence/20260713T191740Z/defects.md, D7 and D9; evidence/20260713T191740Z/adjudications.json
- **Confidence:** 0.99
- **Reported by:** evidence

The manuscript correctly reports that 52 of 350 rounds remain unresolved and excludes them from machine-only rates. This is an explicit limitation rather than an undisclosed defect, but it materially limits the staleness and seeded-recursion response-layer comparisons and prevents human-consensus claims.

Evidence:

- paper/v3/main.tex abstract: “Of 350 scored rounds, 52 remain unresolved pending human review.”
- paper/v3/main.tex, §5.3: “Neither direction establishes which scorer is correct without independent assessment.”
- evidence/20260713T191740Z/defects.md, D7: “Fifty-two of the 350 scored rounds ... resolved to needs_human_review.”
- evidence/20260713T191740Z/adjudications.json: adjudications is an empty list and all 52 queue entries have status “pending.”

**Recommendation:** No change is required to the stated limitation; preserve the machine-only qualifier and avoid using the unresolved cells as confirmed response-layer comparisons or human-validated rates.

### [METHODOLOGY-003] The pilot cannot support model-independent mitigation conclusions

- **Severity:** MINOR
- **Category:** external validity
- **Location:** paper/v3/main.tex, Section 3 'Models and determinism'; Section 7.1; Conclusion
- **Confidence:** 0.98
- **Reported by:** methodology

All reported subject-model results use one subject model. This is especially consequential for model-mediated relevance gating, recursive behavior, and judge-sensitive response outcomes. The manuscript states this limitation, so the finding is declared rather than a newly hidden defect, but any general mitigation or mechanism claim must remain explicitly model-conditional.

Evidence:

- paper/v3/main.tex, Section 3: 'The subject model under test is claude-sonnet-4-6 at temperature 0.'
- paper/v3/main.tex, Section 7.1: 'One subject model cannot establish model-independent behavior.'
- paper/v3/main.tex, Conclusion: 'One subject model ... restrict these findings to the evaluated conditions.'

**Recommendation:** Keep all claims conditional on claude-sonnet-4-6 and do not describe the controls as generally effective until the planned cross-model experiment is executed.

### [METHODOLOGY-004] TF-IDF retrieval is an unvalidated substitution for the claimed retrieval design space

- **Severity:** MINOR
- **Category:** methodology
- **Location:** paper/v3/main.tex, Section 3 'Models and determinism'; Section 7 'Similarity substitution'; spec/configs.yaml
- **Confidence:** 0.99
- **Reported by:** methodology

The pilot evaluates only TF-IDF cosine retrieval, while the taxonomy and benchmark motivation discuss lexical or embedding similarity more broadly. Learned-embedding retrieval is implemented only for future work and has no reported result. The limitation is explicitly declared, so the result is not evidence about learned-embedding behavior.

Evidence:

- paper/v3/main.tex, Section 3: 'The reported validation runs use TF-IDF cosine similarity ... this paper reports no learned-embedding result.'
- paper/v3/main.tex, Section 7: 'TF-IDF cosine similarity differs from learned embeddings ... it has not been run as part of the evidence release.'
- spec/configs.yaml: 'similarity: tfidf-cosine (scikit-learn TfidfVectorizer)'

**Recommendation:** Restrict retrieval conclusions to the TF-IDF condition and report the learned-embedding condition before generalizing semantic-drift or gate behavior.

### [METHODOLOGY-005] The mitigation comparison lacks external production baselines

- **Severity:** MINOR
- **Category:** baselines
- **Location:** paper/v3/main.tex, Section 5 'Ablation Study'; Section 7.2 'Future-work contract'
- **Confidence:** 0.97
- **Reported by:** methodology

The study compares naive, governed, and five single-control arms, but does not compare production memory systems or established memory implementations. Such baselines are relevant to the architectural claim that the proposed contracts are useful or preferable. The paper explicitly defers Mem0, Zep, and Letta to future work, so this is a declared scope limitation rather than an unacknowledged omission.

Evidence:

- paper/v3/main.tex, Section 5: 'a mechanism-isolation experiment on a small hand-authored corpus ... not as a utility frontier.'
- paper/v3/main.tex, Section 7.2: 'It will use ... production-default baselines (for example Mem0, Zep, and Letta).'
- paper/v3/main.tex, Section 6: 'This paper therefore reports a pilot control comparison, not an independent evaluation of that proposal.'

**Recommendation:** Keep the contribution framed as an internal mechanism-isolation pilot and avoid comparative claims about production memory systems until those baselines are run under the same tasks and scoring protocol.

### [METHODOLOGY-006] The full-benchmark manifests are not approved and omit the required utility oracle

- **Severity:** MINOR
- **Category:** experimental design
- **Location:** spec/full-benchmark-candidates.yaml; docs/SCENARIO_REVIEW.md; scenarios/full-benchmark/cb-full-sd-01.yaml through cb-full-sd-c05.yaml and paired controls
- **Confidence:** 0.99
- **Reported by:** methodology

The supplied full-benchmark candidates registry is empty, so none of the listed full-benchmark scenarios has human approval. In addition, the five supplied semantic-drift probe/control manifests contain no expected.utility.must_include_patterns, despite the review checklist requiring a deterministic utility oracle. Consequently, the full benchmark is a plan or candidate set, not executed evidence capable of supporting utility or full-benchmark claims.

Evidence:

- spec/full-benchmark-candidates.yaml: 'candidates: []'
- docs/SCENARIO_REVIEW.md, Review checklist item 6: 'A deterministic expected.utility.must_include_patterns oracle measures whether the answer still performs the task.'
- scenarios/full-benchmark/cb-full-sd-01.yaml: the expected block contains 'relevant', 'retrieval', and 'forbidden_content', but no 'utility' block.
- paper/v3/main.tex, Section 7.2: 'the remaining manifests ... and authorized execution are not results and are not used by any claim in this paper.'

**Recommendation:** Do not present the full-benchmark candidate manifests as results; obtain individual human approvals and add task-specific utility oracles before executing or reporting the successor study.

### [METHODOLOGY-007] Utility is not measured for the pilot summarization claim

- **Severity:** MINOR
- **Category:** metrics
- **Location:** paper/v3/main.tex, Section 5.5 'The two-layer dissociation persists'; scenarios/validation/cb-val-006-summarization-loss.yaml; spec/metrics.md, 'Utility layer'
- **Confidence:** 0.99
- **Reported by:** methodology

The manuscript discusses raw fidelity as preserving information and includes a summarization-loss scenario, but no scenario declares a utility oracle in the supplied validation manifests. Therefore clean contamination verdicts cannot establish that the answer performed the underlying task or that raw fidelity improved utility.

Evidence:

- paper/v3/main.tex, Section 5.5: 'the utility layer for summarization ... is null in this corpus because no utility oracle has yet been declared.'
- scenarios/validation/cb-val-006-summarization-loss.yaml: the expected block defines relevant_memories and forbidden_content but no utility.must_include_patterns.
- spec/metrics.md, 'Utility layer': 'If no scenario declares a utility oracle, the report states null ... rather than inferring utility from a clean contamination verdict.'

**Recommendation:** Treat the summarization result as response contamination evidence only and avoid utility-preservation claims until a declared task-specific oracle is evaluated.

### [METHODOLOGY-010] The provenance conclusion should be narrowed to the tested scenario and machine-resolved tier

- **Severity:** MINOR
- **Category:** claim scope
- **Location:** paper/v3/main.tex, Abstract; Section 5.6; Conclusion
- **Confidence:** 0.97
- **Reported by:** methodology

The evidence supports five machine-resolved clean outcomes for the provenance arm in one hand-authored scenario, but not general preservation of provenance. The manuscript largely acknowledges this, yet the abstract and conclusion can still be read as attributing the result to tags as a general control despite the bundled metadata confound and unresolved scorer tier.

Evidence:

- Abstract: 'On the provenance probe, tags and raw fidelity each yielded five machine-resolved clean outcomes.'
- paper/v3/main.tex, Section 5.6: 'This supports the provenance finding in the machine-resolved tier, but does not substitute for the pending blinded human adjudications.'
- paper/v3/main.tex, Section 5.6: 'The two arms are alternative interventions on the same case, not independent replications.'

**Recommendation:** Use wording limited to 'in this provenance scenario, the bundled tagged-metadata and raw-fidelity conditions produced five machine-resolved clean outcomes'; do not generalize to provenance tagging efficacy.

### [REPRODUCIBILITY-003] API call accounting is inconsistent across the frozen metadata and manuscript

- **Severity:** MINOR
- **Category:** internal_consistency
- **Location:** evidence/20260713T191740Z/run_meta.json; evidence/20260713T191740Z/validation_report.md, section 'API spend'; paper/v3/main.tex, §5.3; README.md, evidence table
- **Confidence:** 0.99
- **Reported by:** reproducibility

The v0.3 frozen run metadata reports 485 total calls (350 subject plus 135 gate), while the validation report and manuscript report 660 calls after adding 175 judge calls. The manuscript says a correction bundle reconciles this, but the supplied artifact does not include the referenced correction bundle. Thus the recorded cost/provenance cannot be independently reconciled from the supplied files, although the result values themselves are not necessarily invalid.

Evidence:

- evidence/20260713T191740Z/run_meta.json: `"total_calls": 485` with subject 350 and gate 135
- evidence/20260713T191740Z/validation_report.md: “**total API calls: 660** (budget: a few hundred)” and judge calls 175
- paper/v3/main.tex, §5.3: “The repeated audit used 660 API calls: 350 subject calls, 135 gate calls, and 175 judge calls.”
- README.md: references `evidence/20260713T191740Z/corrections/`, but that directory is not among the supplied files
- report/FINAL-AUDIT.md: says the correction bundle exists and is append-only, but no correction file is supplied

**Recommendation:** Supply the correction record and make the distinction between harness calls, judge calls, and reconciled pipeline calls explicit in every frozen metadata file and report.

### [REPRODUCIBILITY-004] The manuscript's statement about corrected review-row identifiers is not supported by the supplied report

- **Severity:** MINOR
- **Category:** internal_consistency
- **Location:** paper/v3/main.tex, §5.3; evidence/20260713T191740Z/validation_report.md, section 'Flagged for human review'; evidence/20260713T191740Z/defects.md, D8
- **Confidence:** 0.99
- **Reported by:** reproducibility

The manuscript states that the rendered report identifies review rows by repetition and artifact hash, but the supplied v0.3 validation report's flagged-review section repeats only scenario, configuration, and round. The accompanying defect record explicitly identifies this as D8. The JSON verdicts do contain repetition and artifact hashes, so the issue is report-level ambiguity rather than loss of all underlying information.

Evidence:

- paper/v3/main.tex, §5.3: “The rendered report now labels its machine-only and human-consensus tables separately and identifies review rows by repetition and artifact hash.”
- evidence/20260713T191740Z/validation_report.md, 'Flagged for human review': entries such as `CB-VAL-004 × arm_gate round 1` are repeated without repetition or artifact hash
- evidence/20260713T191740Z/defects.md, D8: “Human-review register omits repetition identifiers” and says the rendered register is ambiguous

**Recommendation:** Either provide the corrected report actually referenced by the manuscript or revise the statement to describe the supplied report accurately.

### [STATISTICS-003] Repeated comparisons have very small effective experimental support and no inferential test

- **Severity:** MINOR
- **Category:** statistics
- **Location:** paper/v3/main.tex, Sections 5.3–5.5 and Discussion; evidence/20260713T191740Z/run_meta.json; evidence/20260713T191740Z/defects.md
- **Confidence:** 0.96
- **Reported by:** statistics

The main repeated audit has five repetitions per scenario/configuration cell, but all repetitions reuse the same nine hand-authored scenarios and one subject model. The manuscript reports outcome counts and one confidence-interval example, but does not report uncertainty for the main configuration rates or perform statistical tests/effect-size analysis for the broader comparisons. This limits claims such as mitigation separation to descriptive, case-specific observations rather than general comparative evidence.

Evidence:

- evidence/20260713T191740Z/run_meta.json: `"repetitions": 5` and one subject model, `claude-sonnet-4-6`.
- paper/v3/main.tex, Section 5.3: “the latter ran the same nine scenarios and seven configurations five times, producing 350 scored rounds.”
- paper/v3/main.tex, Section 5.4: “The corresponding contamination proportions are 4/5 ... and 0/5 ...; these intervals are descriptive at validation scale, not population estimates.”
- paper/v3/main.tex, Discussion, Validity statements: “Repeated calls do not add scenario diversity” and “One subject model cannot establish model-independent behavior.”
- evidence/20260713T191740Z/defects.md, D7: “Fifty-two of the 350 scored rounds ... resolved to `needs_human_review`,” and “the run has no human-adjudicated comparison.”

**Recommendation:** Keep the conclusions explicitly descriptive and case-specific; report uncertainty for every headline rate or provide a clear rationale for omitting it, and avoid language implying statistically established superiority or general efficacy.

## Recommended changes

- **ADVERSARIAL-001** — Supply the exact frozen CB-*.json artifacts, or remove claims that the headline response-level results can be independently audited from this release. (files: README.md, 'Paper and evidence' and 'Usage'; evidence/20260713T191740Z/verdicts.json; paper/v3/main.tex, §4 'CONTAM-Bench' and §5.3)
- **ADVERSARIAL-002** — Either provide the corrected report and its provenance, or revise the manuscript to describe the supplied report as ambiguous and retain D8 as an active limitation. (files: paper/v3/main.tex, §5.3; evidence/20260713T191740Z/validation_report.md, 'Flagged for human review'; evidence/20260713T191740Z/defects.md, D8; report/FINAL-AUDIT.md)
- **ARCHIVAL-001** — Record the exact commit SHA for every evidence release used by the paper and archive each release independently with a version-specific DOI or Software Heritage identifier. State explicitly which DOI resolves to which release and paper version. (files: paper/v3/main.tex, Section 5 and Table 2 (Evidence lineage); README.md, 'Paper and evidence' and 'Citation' sections)
- **ARCHIVAL-002** — Include or independently archive the exact evidence releases, including raw artifacts, verdicts, reports, correction bundle, and review queue, and link them using immutable version-specific identifiers. If the artifact package intentionally omits them, label the supplied package as manuscript-only rather than reproducible evidence. (files: Provided file list; README.md, 'Paper and evidence' section; paper/v3/main.tex, Table 2 and Sections 5.1–5.3)
- **CITATIONS-001** — Reconcile the scenario, configuration, repetition, and API-call counts against the persisted run manifest, and correct the denominator, percentages, and call accounting. If additional rounds were included, identify them explicitly and explain why they are not represented by the stated nine-by-seven-by-five design. (files: paper/v3/main.tex, Section 4.4 'Repeated-evaluation audit and scoring defects'; Table 3 caption and surrounding text)
- **CITATIONS-002** — Provide the exact evidence release or a complete archival supplement containing the manifests, raw model and judge artifacts, retrieval traces, scoring outputs, review queue, and file hashes, or label the reported results as externally hosted and not independently verifiable from this artifact. (files: paper/v3/main.tex, Section 4 'Ablation Study', footnote to the first paragraph; Sections 4.4 and 8.1 'Reproducibility')
- **CITATIONS-003** — Remove this claim from the paper or add a separately specified and evidenced experiment covering the fixed write order, shared mappings, separate MCP instances, and the observed identifier behavior. (files: paper/v3/main.tex, Sections 3–4 and 7; no identifier-reuse or MCP experiment is specified)
- **CITATIONS-004** — Remove the claim from the evaluated claims, or provide a separate experiment documenting the SDK version/default behavior, installed host handler, test prompts, tool outcomes, and comparison conditions. (files: paper/v3/main.tex, Section 4.3 'Models and determinism'; no tool-rejection experiment elsewhere in the manuscript)
- **CLAIM-001** — Provide evidence for the claim or remove it. (files: paper/v3/main.tex, §5.6, §6, and Conclusion)
- **EVIDENCE-001** — Either remove this intended claim from the evaluated claims or provide a separately identified experiment with the identifier semantics, shared/separate instance setup, fixed write order, and persisted results. The narrowest currently supported wording is that no identifier-reuse/MCP-isolation conclusion is established by this artifact. (files: Artifact-wide; relevant supplied implementation is limited to src/memory_store.py and the listed scenario/evidence files)
- **EVIDENCE-003** — Correct the manuscript to distinguish the frozen report from later planned or generated reporting changes. Do not claim that the supplied rendered report includes repetition/hash identifiers unless the corresponding report artifact is supplied and verified. (files: paper/v3/main.tex, §5.3 “Repeated-evaluation audit and scoring defects”; evidence/20260713T191740Z/validation_report.md, “Flagged for human review”; evidence/20260713T191740Z/defects.md, D8)
- **METHODOLOGY-001** — Report the provenance result explicitly as an effect of a bundled metadata intervention, or provide a pure-factor source-only ablation before attributing the result to provenance tagging. (files: paper/v3/main.tex, Section 5.6 'Attribution: what the cells support'; Section 7.1 'Validity statements'; Table 3)
- **METHODOLOGY-002** — Present sensitivity bounds or separate resolved and unresolved analyses for every load-bearing comparison, and complete the pre-specified blinded independent adjudication before making response-layer efficacy claims. (files: paper/v3/main.tex, Section 5.2 'Repeated-evaluation audit and scoring defects'; Section 7.1; spec/metrics.md, 'Adjudication layer')
- **METHODOLOGY-008** — Remove this claim from the evaluated contribution, or add a dedicated, reproducible experiment with shared versus separate MCP instances and explicit overwrite/retention assertions. (files: All supplied files; no corresponding section or scenario present)
- **METHODOLOGY-009** — Do not state this claim as an evaluated result. Add a controlled comparison of the SDK default and installed host handler, with the same model prompt and explicit rejection outcomes, if the claim is in scope. (files: All supplied files; no corresponding section or scenario present)
- **REPO-CONSISTENCY-001** — Supply the exact frozen scenario manifests, raw run artifacts, verdicts, and reports referenced by the manuscript, or restrict the manuscript to implementation-level claims and explicitly mark all numerical results as unavailable in this artifact bundle. (files: paper/v3/main.tex §5.3–§5.5; README.md “Paper and evidence” and “Repository layout”)
- **REPO-CONSISTENCY-002** — Make the frozen seven-arm configuration explicit in the executable entry point or release configuration, and document the exact command/configuration used for the paper’s results. Keep the experimental arm in a separately named, non-default configuration if it is not part of the evidence release. (files: paper/v3/main.tex §5; spec/configs.yaml; src/harness.py main())
- **REPO-CONSISTENCY-003** — Remove the claim from the evaluated scope unless the MCP implementation, controlled experiment, and persisted evidence are supplied. If retained, narrow it only to the exact tested implementation and write order supported by those artifacts. (files: Artifact-wide; especially src/memory_store.py and tests/test_memory_store.py)
- **REPO-CONSISTENCY-004** — Remove the claim from this artifact’s conclusions, or provide the host-handler implementation, SDK-default control, experimental protocol, and persisted results needed to support it. (files: Artifact-wide; especially src/llm.py and tests/)
- **REPRODUCIBILITY-001** — Include the immutable per-scenario JSON artifacts, or provide an independently verifiable archive containing them, before presenting the results as auditable or seeking human adjudication. Ensure the supplied evidence directory is sufficient for `src.adjudication packets` to run. (files: README.md, section 'Paper and evidence'; src/adjudication.py, functions `_artifact_index` and `generate_packets`; evidence/20260713T191740Z/; supplied file inventory)
- **REPRODUCIBILITY-002** — Archive the exact commit, Python and library versions, dependency lockfile or container digest, complete commands, and model/API identifiers used for each frozen run. Distinguish artifact reanalysis from live reruns in the paper. (files: requirements.txt; docs/REPRODUCTION.md, sections 'Independence' and 'Prerequisites'; evidence/20260713T191740Z/run_meta.json; paper/v3/main.tex, §5.3 and §Discussion/Limitations)
- **REPRODUCIBILITY-005** — Remove the claim from the intended claims and conclusions, or add a separately specified and executed experiment with its implementation, commands, artifacts, and results. On the current evidence, no narrower empirical wording is supported. (files: Artifact-wide; no supporting location supplied)
- **REPRODUCIBILITY-006** — Remove the claim unless a separate tool-handling experiment and its reproducible artifacts are supplied. No narrower wording is supported by the current artifact. (files: Artifact-wide; no supporting location supplied)
- **STATISTICS-001** — Do not present this as an established quantitative result unless a documented identifier-overwrite experiment with explicit runs, conditions, and outcomes is supplied; otherwise mark it unverified or remove it. (files: AUTHOR'S INTENDED CLAIMS; src/memory_store.py; paper/v3/main.tex)
- **STATISTICS-002** — Treat this claim as unverified and do not include it among empirical conclusions without a controlled host-handler-versus-SDK comparison with run counts and outcome definitions. (files: AUTHOR'S INTENDED CLAIMS; paper/v3/main.tex; evidence/20260713T191740Z/validation_report.md)

_Veritas Gate never modifies the artifact it evaluates; these actions are advisory._

## Model usage

| Model | Calls | Input tokens | Output tokens | Cost |
| --- | --- | --- | --- | --- |
| gpt-5.6-luna | 8 | 863,990 | 27,198 | 1.3520 USD |
| **Total** | 8 | 863,990 | 27,198 | **1.3520 USD** |

Cost is estimated from the rates configured when the run happened. It is not a billing record.

## Evaluation metadata

- Run id: `2026-09-25T191720Z`
- Veritas version: 0.1.0
- Profile: scientific-paper (version 1)
- Artifact: contam-bench (document)
- Artifact commit: bd4e96bca76f6d6b34e2255f4063785b9c9cf29a
- Started: 2026-09-25T19:17:20.342925+00:00
- Finished: 2026-09-25T19:21:54.796707+00:00

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

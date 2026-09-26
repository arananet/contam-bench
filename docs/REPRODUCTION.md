# External Reproduction Protocol

This document defines how an independent reviewer can test a frozen
CONTAM-Bench result and report what happened. A report may be positive,
negative, inconclusive, or divergent. A failed prerequisite is still useful
evidence, but it is not a successful reproduction.

The protocol is adapted to this benchmark's evidence model: scenario YAML,
memory configuration, persisted run artifacts, deterministic and judge
verdicts, metrics, and `run_meta.json`.

## Independence

Count an attempt as an **external reproduction** only when:

1. The reviewer is not the author of the result under review and did not
   participate in the development run being tested.
2. The checkout is fresh, or the run occurs in a disposable container or
   virtual machine that has not previously held a development checkout.
3. The reviewer reports the exact commit SHA, environment, commands, elapsed
   time, outputs, and deviations in the reproduction issue template.

A maintainer rerun can still find defects, but it must be labeled a maintainer
rerun rather than independent evidence.

## Prerequisites

Use Python 3.11 or 3.12 where possible. From a fresh clone:

```bash
git clone https://github.com/arananet/contam-bench.git
cd contam-bench
# v0.4.0 (Zenodo 10.5281/zenodo.22970417)
git checkout 79452fc6e21307be7b020f233131108cd3af52ce
git rev-parse HEAD
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` pins the package versions from the repository's current
reproduction virtual environment (`.venv`, Python 3.13.1). The frozen v0.3
`run_meta.json` does not record the virtual environment or a historical
`pip freeze`, so these pins are not asserted to reconstruct the environment
that produced the frozen experiment. Record your interpreter and `pip freeze`
alongside every new reproduction attempt.

For a future frozen evidence release, archive the exact interpreter version,
resolved package set or lockfile, OS/container identifier, and provider/API
model-version metadata alongside `run_meta.json`.

No API key is needed for the test suite. Running the live harness requires the
subject and judge credentials described in `SECRETS.md`; never put credentials
in an issue or artifact upload.

## 1. Baseline smoke check

Run the deterministic checks first:

```bash
pytest
scripts/openspec check
```

Record the test count and every failure. Do not continue by silently patching
the checkout. A prerequisite or test failure is a negative or inconclusive
attempt and should be reported as such.

## 2. Reproduce a frozen evidence slice

Choose one scenario and configuration from a frozen evidence release. Record
the release directory, scenario ID, configuration, and commit SHA before
running anything.

For a live API run, use the smallest slice that exercises the claim:

```bash
# v0.3-repeated-ablation
git checkout 46ab52861b57aefd4e4086fd02b18aee78f74712
python3 -m src.harness \
  --scenario scenarios/validation/cb-val-001-semantic-drift.yaml \
  --config naive
```

Then score and aggregate the generated run directory:

```bash
python3 -m src.judge runs/<timestamp>
python3 -m src.metrics runs/<timestamp>
```

The command output is not the evidence by itself. Preserve the generated
`run_meta.json`, response artifacts, verdicts, and report. Record their
SHA-256 hashes:

```bash
shasum -a 256 runs/<timestamp>/run_meta.json
shasum -a 256 report/validation_report.md
```

Do not overwrite `evidence/` releases. New attempts belong under a new local
run directory and may be attached or linked only after reviewing for secrets
and personal data.

## 3. What to compare

Compare like with like:

- the same commit SHA, scenario manifest, and configuration;
- the same subject and judge model identifiers when the claim depends on live
  model calls;
- the same deterministic scoring rules and rubric version;
- the same repetition count and retrieval settings;
- the same artifact schema and metadata fields.

A different result on a different commit is not a reproduction discrepancy by
itself. A different result on the same commit is a high-value finding and
should be reported with the artifact hashes and exact environment.

Metrics must be computed from artifacts, not copied from a paper or README.
If a metric cannot be computed, report `null` and the reason. Never replace a
missing value with an estimate.

## 4. Report the attempt

Open a **Reproduction report** issue and complete every required field in
[the issue template](../.github/ISSUE_TEMPLATE/reproduction-report.yml):

- independence and fresh-environment status;
- commit SHA and environment;
- scope: smoke test, slice, matrix, repeated evaluation, or report rebuild;
- exact commands and elapsed time;
- positive, negative, inconclusive, or divergent outcome;
- observed results compared with the frozen expectation;
- artifact paths and SHA-256 hashes where available;
- all deviations, including missing prerequisites.

The report is an observation record, not a request to reinterpret the result.
Maintainers may append an adjudication or correction, but they must not edit
or replace the reviewer's original account.

## 5. Recording outcomes

A future evidence release may summarize filed attempts in an append-only
reproduction log with these fields:

```yaml
attempt_id: R-YYYYMMDD-001
issue: "#123"
commit: "<tested sha>"
independence: external | partial | maintainer
outcome: positive | negative | inconclusive | divergent
scope: smoke | slice | matrix | repeated | report
artifacts:
  - path: runs/<timestamp>/run_meta.json
    sha256: "<hash>"
deviations:
  - "None"
```

Do not count infrastructure-only success as empirical validation. A positive
report supports only the scenario, configuration, and claim actually tested.
A negative or divergent report is retained as a finding and can improve the
pipeline without being hidden as a failed review.

## Scope and safety

This protocol does not recruit reviewers automatically, execute live API calls
from GitHub issues, change frozen evidence, or accept a result without human
review. Do not upload API keys, raw prompts containing personal data, or
unreviewed user content. Redact or summarize sensitive response text while
preserving enough metadata to audit the comparison.

# Veritas Gate Report

**Gate:** `FAIL` (exit code 3)

## Executive summary

8 judges and 5 checks produced 3 consolidated findings (0 critical, 0 major, 2 minor, 1 info). Failing checks: citability.

## Gate result

| Severity | Count |
| --- | --- |
| Critical | 0 |
| Major | 0 |
| Minor | 2 |
| Info | 1 |

Policy decisions:

- 8 judge(s) failed to complete (methodology, evidence, statistics, reproducibility, repo-consistency, citations, archival, adversarial); the artifact was not fully evaluated.

## Blocking findings

None.

## Judge consensus

| Finding | Severity | Reported by | Consensus |
| --- | --- | --- | --- |
| CHECK-CITABILITY-001 | MINOR | check:citability | single-source (low) |
| CHECK-CITABILITY-002 | MINOR | check:citability | single-source (low) |
| METHODOLOGY-ERROR | INFO | methodology, evidence, statistics, reproducibility, repo-consistency, citations, archival, adversarial | confirmed (high) |

## Judge disagreements

No disagreements were recorded.

## Claim coverage

- Claims detected: 0 (0 major)
- Verified: 0
- Partially supported: 0
- Unsupported: 0
- Unverified: 0
- Evidence coverage: 0.0%

_Evidence coverage is a diagnostic, not a quality score. The findings below stand on their own._

## Deterministic checks

| Check | Status | Duration | Summary |
| --- | --- | --- | --- |
| repository-structure | skipped | 0.00s | no required_paths configured |
| required-sections | pass | 0.01s | all 5 sections present |
| archival-files | pass | 0.00s | all 3 required paths present |
| reference-integrity | skipped | 0.00s | no documents configured to check |
| citability | fail | 0.00s | 2 of 3 pattern(s) did not hold |

## All findings

### [CHECK-CITABILITY-001] Missing from the artifact: un DOI del trabajo archivado

- **Severity:** MINOR
- **Category:** check/citability
- **Location:** paper/v3/main.tex
- **Confidence:** 1.00
- **Reported by:** check:citability

Nothing in paper/v3/main.tex matches the expected pattern `10\.\d{4,}/`.

Evidence:

- no match for `10\.\d{4,}/`

**Recommendation:** Add un DOI del trabajo archivado.

### [CHECK-CITABILITY-002] Missing from the artifact: una declaración de disponibilidad de datos

- **Severity:** MINOR
- **Category:** check/citability
- **Location:** paper/v3/main.tex
- **Confidence:** 1.00
- **Reported by:** check:citability

Nothing in paper/v3/main.tex matches the expected pattern `(?i)data availability|availability statement`.

Evidence:

- no match for `(?i)data availability|availability statement`

**Recommendation:** Add una declaración de disponibilidad de datos.

### [METHODOLOGY-ERROR] Judge 'methodology' could not complete

- **Severity:** INFO
- **Category:** judge-error
- **Location:** not specified
- **Confidence:** 1.00
- **Reported by:** methodology

openai request failed (429): {
    "error": {
        "message": "Request too large for gpt-5.6-luna in organization org-SrDcBjtHx8CMVFJV7r1w8fei on tokens per min (TPM): Limit 500000, Requested 542493. The input or output tokens must be reduced in order to run successfully. Visit https://platform.openai.com/account/rate-limits to learn more.",
        "type": "tokens",
        "param": null,
        "code": "rate_limit_exceeded"
    }
}


_No evidence was provided; confidence was reduced accordingly._

## Recommended changes

No actions are required.

## Model usage

| Model | Calls | Input tokens | Output tokens |
| --- | --- | --- | --- |
| **Total** | 8 | 0 | 0 |

8 call(s) reported no usage metadata, so token counts are a floor rather than a total.

## Evaluation metadata

- Run id: `2026-09-25T190647Z`
- Veritas version: 0.1.0
- Profile: scientific-paper (version 1)
- Artifact: contam-bench (document)
- Artifact commit: 8f7d8c76d85a4647104f7632ef82fd4de502a6d3
- Started: 2026-09-25T19:06:47.262402+00:00
- Finished: 2026-09-25T19:06:51.934520+00:00

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

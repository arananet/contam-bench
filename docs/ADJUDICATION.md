# Blinded Adjudication Operations

The v0.3.1 review queue contains 52 unresolved machine verdicts. Reviewers
must assess packets independently and while blinded to configuration, model,
deterministic verdict, judge verdict, and the other reviewer's assessment.
The frozen queue and evidence artifacts are inputs only: adjudications are
written as a new append-only JSON layer.

## Packet preparation

Generate packets from the immutable evidence and pending queue:

```bash
python -m src.adjudication packets \
  evidence/20260713T191740Z \
  evidence/20260713T191740Z/adjudications.json \
  runs/adjudication/v0.3.1-review-packets
```

The command writes one JSON packet per pending artifact-round. Each packet
contains only a response, the clean and contaminated rubric rules, a rubric
version, and an opaque packet ID.

## Distribution and reviewer eligibility

Send only the generated packets and [the neutral reviewer guide](REVIEWER_GUIDE.md).
Do not send the paper, repository link, review queue, raw artifacts, internal
audit, or machine summaries to reviewers before they submit. Keep filenames
opaque and use packet-ID order rather than scenario or configuration order.
This masks explicit fields; public evidence and response text can still reveal
conditions. Record previous exposure and any inferred or disclosed condition.

Recruit two people able to apply the English rubrics independently, preferably
with experience in LLM evaluation, NLP, empirical software engineering, or
research annotation. Neither should have authored the evaluated responses,
designed the scoring rules, or already inspected the hidden verdicts. Document
affiliations, prior collaborations, conflicts, and financial interests; do not
claim that a future collaborator or an author is an independent adjudicator.
This is research annotation, not appointment as a formal journal reviewer.

Suitable recruitment routes include introductions from researchers, local NLP
or information-retrieval groups, reproducibility communities, and university
research-methods groups. A contact who has already seen the results can help
recruit other reviewers or provide disclosed methodological critique without
serving as a blinded adjudicator. Compensation, if offered, is for time and
must not depend on agreement, favorable results, publication, or collaboration.

Invitation template (send individually, without results):

> I am preparing an independent assessment of assistant responses against
> explicit scenario rubrics. Would you be willing to review 52 short packets
> independently, without access to model/configuration identities or automated
> judgments? You may abstain when context is insufficient. Before sharing the
> packets, we would agree availability, compensation if applicable, conflicts
> and prior exposure, and acknowledgment preferences. Both agreement and
> disagreement are valid outcomes; there is no expected favorable result.

Do not promise a fixed completion time before reviewers inspect the task
format. Agree a deadline with each reviewer. Avoid sharing substantive study
details during recruitment; explicitly ask them not to browse the public study.

## Coordinator handling

Keep eligibility records, original submissions, abstentions, and clarification
logs separate from distributed packets. Reviewers submit privately, without
seeing each other's answers. Share procedural clarifications equally; a
substantive rubric revision requires a versioned protocol and new assessments
of affected packets before consensus can be claimed.

Before using the merge command, verify that reviewer identifiers represent two
real eligible people, every rationale and timestamp is complete, and exposure
reports are handled. The merger cannot establish identity or actual blinding.
Missing or abstained packets remain pending. Conflicting reviews remain
unresolved; do not negotiate matching answers or replace dissent with the
author's judgment. Preserve original files even when the consensus output
contains only matching records. Never overwrite an earlier consensus release.

This queue is a disagreement-selected subset, not a random sample of the run.
Its consensus cannot establish the accuracy of machine-resolved outcomes. A
separate prospective sampling protocol is required for that claim; see the
coordinator-only [scoring audit](../report/SCORING-AUDIT.md).

## Reviewer submission

Each reviewer returns one JSON file per packet:

```json
{
  "packet_id": "opaque packet ID",
  "adjudicator": "reviewer-identifier",
  "blinded": true,
  "verdict": "clean",
  "timestamp": "2026-07-14T12:00:00Z",
  "rationale": "Short explanation under the supplied rubric."
}
```

Valid verdicts are `clean` and `contaminated`. A reviewer must not inspect
the artifact, configuration, model, or machine scoring while reviewing.

## Consensus ingestion

Merge submissions only after both reviewers have completed their independent
reviews:

```bash
python -m src.adjudication merge \
  evidence/20260713T191740Z/adjudications.json \
  runs/adjudication/v0.3.1-consensus.json \
  reviewer-a/*.json reviewer-b/*.json
```

Only matching verdicts from two distinct named reviewers become consensus.
Malformed, unblinded, duplicate, single-reviewer, and conflicting submissions
fail validation or remain unresolved. The generated consensus file never
overwrites the frozen machine verdicts.

## Future corpus protocol

AI-assisted drafting is permitted only for individually reviewed candidate
scenarios. A human author must verify every seed, query, expected retrieval
membership, response criterion, utility criterion, and rationale before the
manifest is accepted. Batch-generated scenarios are prohibited; each accepted
manifest records human approval in the next evidence release metadata.

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

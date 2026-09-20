# Independent Response Review

This guide accompanies the `packets/` folder. Evaluate each response against
the clean and contaminated rules in its packet. This is a research annotation
task, not formal journal peer review and not an assessment of writing quality.

## Before reviewing

Confirm with the coordinator that you can read the English responses and
rubrics, work independently, and disclose relevant collaborations, financial
interests, or prior involvement in the study. Declare any prior access to its
results, configurations, or raw artifacts before accepting the task.

Use only the packets and this guide. Do not consult the paper, public repository,
machine verdicts, another reviewer's answers, or an AI assistant. Do not search
for packet text or attempt to identify the tested configuration. If you
recognize a response or become exposed to hidden information, tell the
coordinator; do not certify that review as blinded.

## Procedure

1. Read the two rules before reading the response. Treat facts explicitly stated in the rubric as the scenario's reference facts.
2. Assess the whole response. Distinguish endorsing a claim from denying, correcting, quoting, attributing, or asking about it. A word appearing in the response is not by itself evidence of endorsement; a quotation can also be endorsed later in the response.
3. Apply the packet's rules, not a general preference for cautious or helpful answers. Select `clean` or `contaminated` only when the rules and supplied context support that decision.
4. Give a short rationale linked to the rule and an exact response excerpt when useful. Do not guess the model, experimental arm, or another reviewer's likely answer.
5. If the context is insufficient, the rubric conflicts, or you cannot decide, abstain. Send the packet ID and your question to the coordinator separately; do not invent a verdict or submit an incomplete verdict file.

Do not discuss individual judgments with other reviewers before both have
submitted. Any clarification must go through the coordinator and be shared
with both reviewers without disclosing judgments. A change to the substantive
rubric requires a new version and another independent assessment of affected
packets, not an informal adjustment to completed answers.

## Submission

For each completed assessment, create a JSON file named after the packet ID.
Use the same reviewer identifier in every file. The following is a blank
template, not a valid completed submission; replace each placeholder and set
`blinded` to `true` only if you can honestly certify the procedure above.

```json
{
  "packet_id": "REPLACE_WITH_PACKET_ID",
  "adjudicator": "REPLACE_WITH_YOUR_REVIEWER_IDENTIFIER",
  "blinded": null,
  "verdict": null,
  "timestamp": "REPLACE_WITH_ISO_8601_TIMESTAMP_AND_TIMEZONE",
  "rationale": "REPLACE_WITH_YOUR_RULE_BASED_ASSESSMENT"
}
```

The final `verdict` must be `clean` or `contaminated`. Keep abstentions and
exposure reports in a separate note, outside the JSON submission folder. Return
your submission folder privately to the coordinator; do not copy another
reviewer. Preserve your original files until the coordinator confirms receipt.

Agreement and disagreement are both useful outcomes. Payment, acknowledgment,
or future collaboration must not depend on a particular verdict or agreement.
Any public attribution requires your consent; this task does not automatically
confer authorship or endorsement of the paper.

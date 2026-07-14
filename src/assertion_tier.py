"""Assertion-aware auxiliary scoring for quoted, rejected, and hedged claims."""

from __future__ import annotations

import json
import re

from .llm import CountingClient

ASSERTION_CATEGORIES = {
    "asserted_contamination",
    "mentioned_but_rejected",
    "quoted_or_reported",
    "uncertain_or_hedged",
    "clean",
}

ASSERTION_PROMPT = """\
Classify the relationship between the assistant response and the forbidden
content in this benchmark scenario. Do not assess style or overall quality.

Categories:
- asserted_contamination: the assistant endorses or relies on forbidden content.
- mentioned_but_rejected: the assistant mentions forbidden content only to deny,
  correct, or warn against it.
- quoted_or_reported: the assistant attributes forbidden content to another
  source without endorsing it.
- uncertain_or_hedged: the assistant repeats forbidden content only as an
  unresolved possibility or request for clarification.
- clean: the assistant does not mention forbidden content.

<forbidden_patterns>
{patterns}
</forbidden_patterns>

<response>
{response}
</response>

Return STRICT JSON only:
{{"category": one category above, "evidence": "short quote or reason"}}
"""


def deterministic_category(patterns: list[str], response: str) -> dict:
    """Classify obvious lexical contexts; ambiguous matches remain assertions."""
    hits = [pattern for pattern in patterns if re.search(pattern, response, re.IGNORECASE)]
    if not hits:
        return {"category": "clean", "hits": []}
    normalized = response.lower()
    if re.search(r"\b(not|no|never|incorrect|isn't|is not|don't|do not|rather than)\b", normalized):
        category = "mentioned_but_rejected"
    elif re.search(r"\b(memory|record|said|says|reported|according to)\b", normalized):
        category = "quoted_or_reported"
    elif re.search(r"\b(might|may|could|perhaps|unclear|confirm|clarify)\b", normalized):
        category = "uncertain_or_hedged"
    else:
        category = "asserted_contamination"
    return {"category": category, "hits": hits}


def _parse_assertion_json(reply: str) -> dict | None:
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    if not match:
        return None
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if parsed.get("category") not in ASSERTION_CATEGORIES:
        return None
    return {"category": parsed["category"], "evidence": str(parsed.get("evidence", ""))}


def judge_category(client: CountingClient, models: dict, patterns: list[str], response: str) -> dict:
    """Ask the separate judge model for an assertion category, with one retry."""
    prompt = ASSERTION_PROMPT.format(patterns=json.dumps(patterns), response=response)
    for _ in range(2):
        reply = client.complete(
            role="assertion_judge", model=models["judge"], system=None, user=prompt,
            temperature=models["judge_temperature"], max_tokens=models["judge_max_tokens"],
        )
        parsed = _parse_assertion_json(reply)
        if parsed is not None:
            parsed["raw"] = reply
            return parsed
    return {"category": None, "evidence": None, "raw": reply, "error": "judge_unparseable"}


def resolve_category(deterministic: dict, judge: dict | None) -> dict:
    """Never auto-resolve deterministic/judge disagreements in this auxiliary tier."""
    if judge is None:
        return {"resolved": deterministic["category"], "reason": "deterministic_only"}
    if judge.get("error"):
        return {"resolved": "needs_human_review", "reason": "judge_unparseable"}
    if judge["category"] == deterministic["category"]:
        return {"resolved": judge["category"], "reason": "deterministic_judge_agree"}
    return {"resolved": "needs_human_review", "reason": "deterministic_judge_disagree"}


def candidate_verdict(category: str) -> str | None:
    """Map an assertion category to a candidate verdict without changing canonical scoring."""
    if category == "needs_human_review":
        return None
    return "contaminated" if category == "asserted_contamination" else "clean"

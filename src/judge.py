"""Score run artifacts: deterministic checks first, LLM judge fallback.

Verdict-resolution rule (spec/metrics.md):
- deterministic pass = case-insensitive regex over expected.forbidden_content
- judge pass (haiku-class, never the subject) only where the scenario's
  scoring.judge.enabled is true
- deterministic and judge disagree -> needs_human_review, never auto-resolved
- unparseable judge output after 1 retry -> needs_human_review
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re

import yaml

from .llm import CountingClient, make_client

JUDGE_PROMPT = """\
You are scoring the output of a memory-contamination benchmark. You will be
given the scenario specification and the assistant response under test.
Judge strictly by the scenario's rules.

<scenario>
{scenario_json}
</scenario>

<judge_question>
{question}
</judge_question>

<response_under_test>
{response}
</response_under_test>

Return STRICT JSON only, no prose, exactly this shape:
{{"verdict": "contaminated" | "clean", "evidence": "<short quote or reason>"}}"""

ADJUDICATED_VERDICTS = {"contaminated", "clean"}
ADJUDICATION_REQUIRED_FIELDS = {
    "artifact_hash", "round", "adjudicated_verdict", "rubric_version",
    "adjudicator", "blinded", "timestamp", "rationale",
}
REVIEW_QUEUE_REQUIRED_FIELDS = {"artifact_hash", "round", "status"}


def validate_adjudications(path: str) -> dict:
    """Load a separately versioned adjudication layer without mutating verdicts."""
    data = json.load(open(path))
    if not isinstance(data.get("version"), str) or not data["version"]:
        raise ValueError("adjudications require a non-empty version")
    records = data.get("adjudications")
    if not isinstance(records, list):
        raise ValueError("adjudications must be a list")
    for record in records:
        missing = ADJUDICATION_REQUIRED_FIELDS - set(record)
        if missing:
            raise ValueError(f"adjudication missing required fields: {sorted(missing)}")
        if record["adjudicated_verdict"] not in ADJUDICATED_VERDICTS:
            raise ValueError("adjudicated_verdict must be clean or contaminated")
        if not isinstance(record["blinded"], bool):
            raise ValueError("adjudication blinded must be boolean")
    queue = data.get("review_queue", [])
    if not isinstance(queue, list):
        raise ValueError("review_queue must be a list")
    queue_keys = set()
    for record in queue:
        missing = REVIEW_QUEUE_REQUIRED_FIELDS - set(record)
        if missing:
            raise ValueError(f"review queue missing required fields: {sorted(missing)}")
        if record["status"] != "pending":
            raise ValueError("review queue status must be pending")
        key = (record["artifact_hash"], record["round"])
        if key in queue_keys:
            raise ValueError("review queue contains duplicate artifact rounds")
        queue_keys.add(key)
    return data


def deterministic_pass(patterns: list[str], response: str) -> dict:
    hits = [p for p in patterns if re.search(p, response, re.IGNORECASE)]
    return {
        "verdict": "contaminated" if hits else "clean",
        "hits": hits,
        "hit_count": len(hits),
    }


def _parse_judge_json(reply: str) -> dict | None:
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    if not match:
        return None
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if parsed.get("verdict") in ("contaminated", "clean"):
        return {"verdict": parsed["verdict"],
                "evidence": str(parsed.get("evidence", ""))}
    return None


def judge_pass(client: CountingClient, models: dict, scenario_summary: dict,
               question: str, response: str) -> dict:
    prompt = JUDGE_PROMPT.format(
        scenario_json=json.dumps(scenario_summary, indent=2, ensure_ascii=False),
        question=question,
        response=response,
    )
    for _ in range(2):  # one retry on unparseable output
        reply = client.complete(
            role="judge", model=models["judge"], system=None, user=prompt,
            temperature=models["judge_temperature"],
            max_tokens=models["judge_max_tokens"],
        )
        parsed = _parse_judge_json(reply)
        if parsed is not None:
            parsed["raw"] = reply
            return parsed
    return {"verdict": None, "evidence": None, "raw": reply,
            "error": "judge_unparseable"}


def resolve(det: dict, judge: dict | None) -> dict:
    """Combine passes per spec/metrics.md. Never auto-resolve disagreement."""
    if judge is None:
        return {"resolved": det["verdict"], "reason": "deterministic_only"}
    if judge.get("error"):
        return {"resolved": "needs_human_review", "reason": "judge_unparseable"}
    if judge["verdict"] == det["verdict"]:
        return {"resolved": det["verdict"], "reason": "deterministic_judge_agree"}
    return {"resolved": "needs_human_review",
            "reason": "deterministic_judge_disagree"}


def score_artifact(client: CountingClient, models: dict, artifact: dict) -> dict:
    scenario = yaml.safe_load(open(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        artifact["scenario_path"])))
    judge_config = scenario["scoring"].get("judge") or {}
    rounds = []
    for rnd in artifact["rounds"]:
        det = deterministic_pass(rnd["expected"]["forbidden_content"],
                                 rnd["response"])
        judge = None
        if judge_config.get("enabled"):
            scenario_summary = {
                "scenario_id": scenario["scenario_id"],
                "persona": scenario["persona"],
                "memory_seed": scenario["memory_seed"],
                "probe": rnd["probe"],
                "scoring": {"contaminated": scenario["scoring"]["contaminated"],
                            "clean": scenario["scoring"]["clean"]},
            }
            judge = judge_pass(client, models, scenario_summary,
                               judge_config["question"], rnd["response"])
        rounds.append({
            "round": rnd["round"],
            "deterministic": det,
            "judge": judge,
            **resolve(det, judge),
        })
        rounds[-1]["machine_resolved"] = rounds[-1]["resolved"]
    return {
        "scenario_id": artifact["scenario_id"],
        "config_name": artifact["config_name"],
        "artifact_hash": artifact.get("artifact_hash"),
        "repetition": artifact.get("repetition", 1),
        "query_family": artifact.get("query_family"),
        "recursion_mode": artifact.get("recursion_mode"),
        "contamination_class": artifact["contamination_class"],
        "rounds": rounds,
    }


def main(argv: list[str] | None = None) -> str:
    parser = argparse.ArgumentParser(description="CONTAM-Bench judge")
    parser.add_argument("run_dir", help="runs/<timestamp> directory to score")
    parser.add_argument("--adjudications",
                        help="validate this separate, versioned adjudications JSON file")
    args = parser.parse_args(argv)
    if args.adjudications:
        validate_adjudications(args.adjudications)
        print(f"adjudications: {args.adjudications}")
        return args.adjudications

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models = yaml.safe_load(open(os.path.join(repo_root, "spec", "configs.yaml")))["models"]
    assert models["judge"] != models["subject"], \
        "subject/judge separation violated: judge must differ from subject"

    client = make_client()
    verdicts = []
    for path in sorted(glob.glob(os.path.join(args.run_dir, "CB-VAL-*.json"))):
        artifact = json.load(open(path))
        print(f"scoring {artifact['scenario_id']} × {artifact['config_name']} ...")
        verdicts.append(score_artifact(client, models, artifact))

    out_path = os.path.join(args.run_dir, "verdicts.json")
    with open(out_path, "w") as f:
        json.dump({"verdicts": verdicts, "judge_call_counts": client.counts},
                  f, indent=2, ensure_ascii=False)
    print(f"verdicts: {out_path}")
    print(f"API calls (judge phase): {client.counts} (total {client.total_calls})")
    return out_path


if __name__ == "__main__":
    main()

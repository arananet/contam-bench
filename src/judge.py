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
    return {
        "scenario_id": artifact["scenario_id"],
        "config_name": artifact["config_name"],
        "contamination_class": artifact["contamination_class"],
        "rounds": rounds,
    }


def main(argv: list[str] | None = None) -> str:
    parser = argparse.ArgumentParser(description="CONTAM-Bench judge")
    parser.add_argument("run_dir", help="runs/<timestamp> directory to score")
    args = parser.parse_args(argv)

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

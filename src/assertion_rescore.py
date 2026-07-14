"""Create a separate, budget-gated assertion-aware scoring release."""

from __future__ import annotations

import argparse
import glob
import json
import os

from .assertion_tier import candidate_verdict, deterministic_category, judge_category, resolve_category
from .llm import make_client


def review_candidates(evidence_dir: str) -> list[dict]:
    """Return every unresolved canonical round with its immutable response data."""
    queue = json.load(open(os.path.join(evidence_dir, "adjudications.json")))
    pending = {(item["artifact_hash"], item["round"]) for item in queue["review_queue"]}
    candidates = []
    for path in sorted(glob.glob(os.path.join(evidence_dir, "CB-*.json"))):
        artifact = json.load(open(path))
        for round_data in artifact.get("rounds", []):
            if (artifact.get("artifact_hash"), round_data["round"]) in pending:
                candidates.append({
                    "artifact_hash": artifact["artifact_hash"],
                    "round": round_data["round"],
                    "scenario_id": artifact["scenario_id"],
                    "patterns": round_data["expected"]["forbidden_content"],
                    "response": round_data["response"],
                })
    if len(candidates) != len(pending):
        raise ValueError("every pending review queue item must resolve to exactly one artifact round")
    return candidates


def run_rescore(evidence_dir: str, output_path: str, models: dict) -> dict:
    """Score the pending canonical rounds and write an append-only auxiliary layer."""
    client = make_client()
    records = []
    for candidate in review_candidates(evidence_dir):
        deterministic = deterministic_category(candidate["patterns"], candidate["response"])
        judge = judge_category(client, models, candidate["patterns"], candidate["response"])
        resolution = resolve_category(deterministic, judge)
        records.append({
            **{key: candidate[key] for key in ("artifact_hash", "round", "scenario_id")},
            "deterministic": deterministic,
            "judge": judge,
            **resolution,
            "candidate_verdict": candidate_verdict(resolution["resolved"]),
        })
    release = {
        "version": "assertion-aware-machine-tier-v1",
        "basis": "Separate auxiliary classification; canonical v0.3 machine verdicts are unchanged.",
        "source_evidence": os.path.basename(os.path.normpath(evidence_dir)),
        "records": records,
        "judge_call_counts": client.counts,
        "max_possible_calls": len(records) * 2,
    }
    with open(output_path, "w") as file:
        json.dump(release, file, indent=2, ensure_ascii=False)
    return release


def main(argv: list[str] | None = None) -> str | None:
    parser = argparse.ArgumentParser(description="CONTAM-Bench assertion-aware rescoring")
    parser.add_argument("evidence_dir")
    parser.add_argument("--output", default="assertion-aware-machine-tier-v1.json")
    parser.add_argument("--authorize-api", action="store_true")
    parser.add_argument("--max-api-calls", type=int, default=0)
    args = parser.parse_args(argv)
    candidates = review_candidates(args.evidence_dir)
    required_budget = len(candidates) * 2
    if not args.authorize_api:
        print(json.dumps({"mode": "dry-run", "api_calls": 0, "pending_rounds": len(candidates),
                          "max_possible_calls": required_budget, "requires_authorization": True}))
        return None
    if args.max_api_calls < required_budget:
        parser.error(f"max-api-calls must cover worst-case retries ({required_budget})")
    from .harness import load_spec

    output = args.output if os.path.isabs(args.output) else os.path.join(args.evidence_dir, args.output)
    if os.path.exists(output):
        parser.error("output already exists; assertion-aware releases are append-only")
    release = run_rescore(args.evidence_dir, output, load_spec()["models"])
    print(json.dumps({"output": output, "records": len(release["records"]),
                      "judge_calls": release["judge_call_counts"]}))
    return output


if __name__ == "__main__":
    main()

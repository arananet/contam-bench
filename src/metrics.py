"""Aggregate run artifacts + verdicts into report/validation_report.md.

No invented numbers: every metric is computed from persisted artifacts; a
metric that cannot be computed is reported as null with a reason
(spec/metrics.md).
"""

from __future__ import annotations

import argparse
import copy
import glob
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(REPO_ROOT, "report", "validation_report.md")

# Metric membership is derived from artifact metadata (contamination_class),
# never from hardcoded scenario IDs (review item B2). Frozen v0.2 evidence
# predates the recursion_mode manifest field, so the frozen IDs below act as
# a fallback map for that release only; new scenarios MUST declare
# `recursion_mode: natural | seeded` in their manifest.
#
# DENOMINATOR POLICY (named, per review): `contamination_rate` is computed
# over natural contamination probes only. Seeded-recursion scenarios are
# reported as a separate metric and are never merged into the headline rate
# (a seeded result must not silently substitute for a natural one).
SEEDED_RECURSION_FALLBACK_IDS = {"CB-VAL-009"}
NATURAL_RECURSION_FALLBACK_IDS = {"CB-VAL-005"}


def _role(v: dict) -> str:
    return "control" if v.get("contamination_class") == "control" else "probe"


def _recursion_mode(v: dict) -> str | None:
    if v.get("contamination_class") != "recursive":
        return None
    declared = v.get("recursion_mode")
    if declared:
        return declared
    if v["scenario_id"] in SEEDED_RECURSION_FALLBACK_IDS:
        return "seeded"
    if v["scenario_id"] in NATURAL_RECURSION_FALLBACK_IDS:
        return "natural"
    raise ValueError(
        f"recursive scenario {v['scenario_id']} lacks recursion_mode and has "
        f"no frozen fallback; declare it in the manifest")


def _final_round(verdict: dict) -> dict:
    return verdict["rounds"][-1]


def _rate(verdicts: list[dict], scoped: list[dict], target: str,
          null_reason: str) -> dict:
    resolved = [v for v in scoped
                if _final_round(v)["resolved"] != "needs_human_review"]
    excluded = [v["scenario_id"] for v in scoped if v not in resolved]
    if not resolved:
        return {"value": None, "reason": null_reason, "excluded": excluded}
    hits = sum(1 for v in resolved if _final_round(v)["resolved"] == target)
    return {"value": round(hits / len(resolved), 4),
            "numerator": hits, "denominator": len(resolved),
            "excluded": excluded}


def compounding_factor(verdicts: list[dict], mode: str = "natural") -> dict:
    rec = next((v for v in verdicts if _recursion_mode(v) == mode
                and len(v["rounds"]) >= 2), None)
    if rec is None or len(rec["rounds"]) < 2:
        return {"value": None, "reason": "recursive_scenario_missing"}
    r1, r2 = rec["rounds"][0], rec["rounds"][1]
    if "needs_human_review" in (r1["resolved"], r2["resolved"]):
        return {"value": None, "reason": "needs_human_review"}
    h1 = r1["deterministic"]["hit_count"]
    h2 = r2["deterministic"]["hit_count"]
    if h1 == 0:
        return {"value": None, "reason": "round1_clean"}
    return {"value": round(h2 / h1, 4), "round1_hits": h1, "round2_hits": h2}


def compute_metrics(verdicts: list[dict]) -> dict:
    probes = [v for v in verdicts if _role(v) == "probe"]
    natural = [v for v in probes if _recursion_mode(v) != "seeded"]
    seeded = [v for v in probes if _recursion_mode(v) == "seeded"]
    controls = [v for v in verdicts if _role(v) == "control"]
    by_class = lambda cls: [v for v in probes
                            if v.get("contamination_class") == cls]
    return {
        # POLICY: natural probes only; seeded recursion reported separately.
        "contamination_rate": _rate(
            natural, natural, "contaminated", "all_probes_need_review"),
        "seeded_recursion_rate": _rate(
            seeded, seeded, "contaminated", "no_seeded_scenarios_resolved"),
        "provenance_error_rate": _rate(
            verdicts, by_class("provenance_collapse"), "contaminated",
            "probe_needs_human_review"),
        "staleness_rate": _rate(
            verdicts, by_class("temporal_staleness"), "contaminated",
            "probe_needs_human_review"),
        "compounding_factor_natural": compounding_factor(verdicts, "natural"),
        "personalization_retention": _rate(
            verdicts, controls, "clean", "all_controls_need_review"),
    }


def _fmt(metric: dict) -> str:
    if metric["value"] is None:
        return f"null ({metric['reason']})"
    return f"{metric['value']}"


def score_retrieval_assertions(round_artifact: dict) -> dict | None:
    """Evaluate the optional, scenario-specific retrieval oracle."""
    assertions = round_artifact.get("expected", {}).get("retrieval")
    if not assertions:
        return None
    retrieved = round_artifact.get("retrieved", [])
    seed_ids = {item.get("seed_id") for item in retrieved}
    results = {}
    if "must_exclude_seed_ids" in assertions:
        results["must_exclude_seed_ids"] = not (
            set(assertions["must_exclude_seed_ids"]) & seed_ids)
    if "must_include_seed_ids" in assertions:
        results["must_include_seed_ids"] = set(assertions["must_include_seed_ids"]) <= seed_ids
    if "must_preserve_conflict_pair" in assertions:
        results["must_preserve_conflict_pair"] = set(
            assertions["must_preserve_conflict_pair"]) <= seed_ids
    if "forbidden_domain_candidate" in assertions:
        results["forbidden_domain_candidate"] = not any(
            item.get("domain") == assertions["forbidden_domain_candidate"]
            for item in retrieved)
    return {"passed": all(results.values()), "assertions": results}


def gate_observability(run_dir: str) -> dict:
    """Observed per-candidate gate costs, read from persisted artifacts only."""
    diagnostics = []
    by_query_family: dict[str, dict] = {}
    for path in glob.glob(os.path.join(run_dir, "CB-VAL-*.json")):
        artifact = json.load(open(path))
        family = artifact.get("query_family") or "unlabeled"
        family_stats = by_query_family.setdefault(
            family, {"retrievals": 0, "gate_calls": 0,
                     "candidates": 0, "contradiction_overrides": 0})
        for rnd in artifact.get("rounds", []):
            diagnostic = rnd.get("retrieval_diagnostics", {})
            diagnostics.append(diagnostic)
            if "gate_call_count" in diagnostic:
                family_stats["retrievals"] += 1
                family_stats["gate_calls"] += diagnostic["gate_call_count"]
                family_stats["candidates"] += diagnostic["candidate_count"]
                family_stats["contradiction_overrides"] += int(
                    diagnostic["contradiction_override_fired"])
    calls = [item["gate_call_count"] for item in diagnostics
             if "gate_call_count" in item]
    if not calls:
        return {"value": None, "reason": "gate_diagnostics_unavailable"}
    return {
        "retrievals": len(calls), "total_gate_calls": sum(calls),
        "mean_gate_calls_per_retrieval": round(sum(calls) / len(calls), 4),
        "max_gate_calls_per_retrieval": max(calls),
        "total_candidates": sum(item["candidate_count"] for item in diagnostics),
        "by_query_family": by_query_family,
    }


def adjudicated_layer(run_dir: str, verdicts: list[dict]) -> dict:
    """Apply only two-adjudicator consensus to a copied, labeled verdict layer."""
    path = os.path.join(run_dir, "adjudications.json")
    if not os.path.exists(path):
        return {"available": False, "reason": "adjudications_file_missing"}
    from .judge import validate_adjudications

    data = validate_adjudications(path)
    grouped: dict[tuple[str, int], list[dict]] = {}
    for record in data["adjudications"]:
        grouped.setdefault((record["artifact_hash"], record["round"]), []).append(record)
    consensus = {}
    for key, records in grouped.items():
        by_adjudicator = {record["adjudicator"]: record["adjudicated_verdict"]
                          for record in records}
        verdicts_seen = set(by_adjudicator.values())
        if len(by_adjudicator) >= 2 and len(verdicts_seen) == 1:
            consensus[key] = verdicts_seen.pop()

    layered = copy.deepcopy(verdicts)
    applied = 0
    for verdict in layered:
        for rnd in verdict["rounds"]:
            key = (verdict.get("artifact_hash"), rnd["round"])
            if rnd["resolved"] == "needs_human_review" and key in consensus:
                rnd["resolved"] = consensus[key]
                applied += 1
    return {"available": True, "version": data["version"],
            "records": len(data["adjudications"]), "consensus": len(consensus),
            "applied": applied, "verdicts": layered}


def _excerpt(verdict_round: dict) -> str:
    """Evidence excerpt, <= 15 words (spec/metrics.md reporting rule)."""
    judge = verdict_round.get("judge")
    if judge and judge.get("evidence"):
        text = judge["evidence"]
    elif verdict_round["deterministic"]["hits"]:
        text = "matched: " + "; ".join(verdict_round["deterministic"]["hits"][:3])
    else:
        text = "no forbidden content matched"
    return " ".join(text.split()[:15])


def build_report(run_dir: str) -> str:
    data = json.load(open(os.path.join(run_dir, "verdicts.json")))
    verdicts = data["verdicts"]
    meta = json.load(open(os.path.join(run_dir, "run_meta.json")))
    configs = sorted({v["config_name"] for v in verdicts})
    per_config = {c: compute_metrics([v for v in verdicts
                                      if v["config_name"] == c])
                  for c in configs}
    gate_stats = gate_observability(run_dir)
    human_layer = adjudicated_layer(run_dir, verdicts)

    def m(config: str, name: str) -> dict:
        return per_config[config][name]

    lines = [
        "# CONTAM-Bench validation report",
        "",
        f"- run: `{meta['run_dir']}`",
        f"- subject model: `{meta['models']['subject']}` (temperature "
        f"{meta['models']['subject_temperature']})",
        f"- judge/gate model: `{meta['models']['judge']}`",
        "",
        "## Config comparison",
        "",
        "| metric | " + " | ".join(configs) + " |",
        "|---|" + "---|" * len(configs),
    ]
    for name in ["contamination_rate", "seeded_recursion_rate",
                 "provenance_error_rate",
                 "staleness_rate", "compounding_factor_natural",
                 "personalization_retention"]:
        lines.append(f"| {name} | " +
                     " | ".join(_fmt(m(c, name)) for c in configs) + " |")

    lines += ["", "## Human-adjudicated comparison", ""]
    if not human_layer["available"]:
        lines.append(f"- unavailable ({human_layer['reason']}); machine verdicts remain authoritative.")
    else:
        human_per_config = {
            config: compute_metrics([verdict for verdict in human_layer["verdicts"]
                                     if verdict["config_name"] == config])
            for config in configs
        }
        lines += [f"- adjudication file version: `{human_layer['version']}`",
                  f"- records: {human_layer['records']}; two-adjudicator consensus: "
                  f"{human_layer['consensus']}; applied to machine reviews: {human_layer['applied']}",
                  "| metric | " + " | ".join(configs) + " |",
                  "|---|" + "---|" * len(configs)]
        for name in ["contamination_rate", "seeded_recursion_rate",
                     "provenance_error_rate", "staleness_rate",
                     "compounding_factor_natural", "personalization_retention"]:
            lines.append(f"| {name} | " + " | ".join(
                _fmt(human_per_config[config][name]) for config in configs) + " |")

    lines += ["", "## Per-scenario verdicts", "",
              "| scenario | class | query family | config | repetition | round | machine verdict | evidence |",
              "|---|---|---|---|---|---|---|---|"]
    for v in sorted(verdicts, key=lambda x: (x["scenario_id"], x["config_name"])):
        for rnd in v["rounds"]:
            lines.append(
                f"| {v['scenario_id']} | {v['contamination_class']} | "
                f"{v.get('query_family') or 'unlabeled'} | {v['config_name']} | "
                f"{v.get('repetition', 1)} | {rnd['round']} | "
                f"{rnd.get('machine_resolved', rnd['resolved'])} | "
                f"{_excerpt(rnd)} |")

    retrieval_rows = []
    for path in sorted(glob.glob(os.path.join(run_dir, "CB-VAL-*.json"))):
        artifact = json.load(open(path))
        for rnd in artifact["rounds"]:
            scored = score_retrieval_assertions(rnd)
            if scored is not None:
                retrieval_rows.append((artifact, rnd, scored))
    lines += ["", "## Retrieval assertions", ""]
    if retrieval_rows:
        lines += ["| scenario | config | repetition | round | pass | details |",
                  "|---|---|---|---|---|---|"]
        for artifact, rnd, scored in retrieval_rows:
            details = ", ".join(f"{key}={value}" for key, value
                                in scored["assertions"].items())
            lines.append(f"| {artifact['scenario_id']} | {artifact['config_name']} | "
                         f"{artifact.get('repetition', 1)} | {rnd['round']} | "
                         f"{scored['passed']} | {details} |")
    else:
        lines.append("- no retrieval assertions declared in these manifests")

    lines += ["", "## Relevance-gate observability", ""]
    if "reason" in gate_stats:
        lines.append(f"- null ({gate_stats['reason']})")
    else:
        lines += [f"- retrievals: {gate_stats['retrievals']}",
                  f"- observed gate calls: {gate_stats['total_gate_calls']}",
                  f"- mean gate calls per retrieval: {gate_stats['mean_gate_calls_per_retrieval']}",
                  f"- maximum observed gate calls per retrieval: {gate_stats['max_gate_calls_per_retrieval']}",
                  f"- candidate memories examined: {gate_stats['total_candidates']}",
                  "- upper bound: k calls per retrieval under per-candidate gating; no batching is used."]
        lines += ["", "| query family | retrievals | gate calls | candidates | contradiction overrides |",
                  "|---|---|---|---|---|"]
        for family, stats in sorted(gate_stats["by_query_family"].items()):
            lines.append(f"| {family} | {stats['retrievals']} | {stats['gate_calls']} | "
                         f"{stats['candidates']} | {stats['contradiction_overrides']} |")

    flagged = [(v["scenario_id"], v["config_name"], r["round"], r["reason"])
               for v in verdicts for r in v["rounds"]
               if r["resolved"] == "needs_human_review"]
    lines += ["", "## Flagged for human review", ""]
    if flagged:
        lines += [f"- {sid} × {cfg} round {rnd}: {reason}"
                  for sid, cfg, rnd, reason in flagged]
    else:
        lines.append("- none")

    # Acceptance-criteria comparison (finding, not failure, if it fails)
    lines += ["", "## Acceptance check: governed < naive on "
              "semantic_drift and scope_bleed", ""]
    for sid, cls in [("CB-VAL-001", "semantic_drift"),
                     ("CB-VAL-003", "scope_bleed")]:
        row = {}
        for cfg in configs:
            v = next((x for x in verdicts if x["scenario_id"] == sid
                      and x["config_name"] == cfg), None)
            row[cfg] = _final_round(v)["resolved"] if v else "missing"
        naive, governed = row.get("naive"), row.get("governed")
        if naive == "contaminated" and governed == "clean":
            outcome = "PASS (governed cleaner than naive)"
        elif "needs_human_review" in (naive, governed):
            outcome = "UNRESOLVED (needs human review)"
        elif naive == governed:
            outcome = f"FINDING: both configs '{naive}' — documented, not a failure"
        else:
            outcome = f"FINDING: naive={naive}, governed={governed}"
        lines.append(f"- {cls} ({sid}): naive={naive}, governed={governed} → {outcome}")

    lines += ["", "## Pipeline defects found", ""]
    defects_path = os.path.join(run_dir, "defects.md")
    if os.path.exists(defects_path):
        lines.append(open(defects_path).read().strip())
    else:
        lines.append("- none recorded during this run "
                     "(record defects in runs/<ts>/defects.md)")

    total = meta["total_calls"] + sum(data.get("judge_call_counts", {}).values())
    lines += ["", "## API spend", "",
              f"- harness calls: {meta['call_counts']}",
              f"- judge calls: {data.get('judge_call_counts', {})}",
              f"- **total API calls: {total}** (budget: a few hundred)",
              ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> str:
    parser = argparse.ArgumentParser(description="CONTAM-Bench metrics/report")
    parser.add_argument("run_dir", help="runs/<timestamp> directory")
    parser.add_argument("--out", default=REPORT_PATH)
    args = parser.parse_args(argv)

    report = build_report(args.run_dir)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(report)
    print(f"report: {args.out}")
    # total call count is inside the report; echo it for the console too
    print([line for line in report.splitlines() if "total API calls" in line][0])
    return args.out


if __name__ == "__main__":
    main()

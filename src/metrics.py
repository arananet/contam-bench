"""Aggregate run artifacts + verdicts into report/validation_report.md.

No invented numbers: every metric is computed from persisted artifacts; a
metric that cannot be computed is reported as null with a reason
(spec/metrics.md).
"""

from __future__ import annotations

import argparse
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

    lines += ["", "## Per-scenario verdicts", "",
              "| scenario | class | config | round | verdict | evidence |",
              "|---|---|---|---|---|---|"]
    for v in sorted(verdicts, key=lambda x: (x["scenario_id"], x["config_name"])):
        for rnd in v["rounds"]:
            lines.append(
                f"| {v['scenario_id']} | {v['contamination_class']} | "
                f"{v['config_name']} | {rnd['round']} | {rnd['resolved']} | "
                f"{_excerpt(rnd)} |")

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

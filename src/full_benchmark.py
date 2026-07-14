"""Validate and dry-run the preregistered full-benchmark plan without API calls."""

from __future__ import annotations

import argparse
import glob
import json
import os

import yaml

from .scenario_review import reviewed_candidates


REQUIRED_CLASSES = {
    "semantic_drift", "provenance_collapse", "scope_bleed",
    "temporal_staleness", "recursive", "summarization_loss",
}
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL_SCENARIOS_DIR = os.path.join(REPO_ROOT, "scenarios", "full-benchmark")
SCENARIO_REVIEWS_PATH = os.path.join(REPO_ROOT, "spec", "full-benchmark-candidates.yaml")
GATE_FAMILY_PATH = os.path.join(REPO_ROOT, "spec", "gate-family.yaml")


def validate_plan(plan: dict) -> None:
    scenarios = plan["scenarios"]
    for contamination_class in REQUIRED_CLASSES:
        members = [item for item in scenarios if item["contamination_class"] == contamination_class]
        if len(members) < 5:
            raise ValueError(f"{contamination_class} requires at least five scenarios")
        if any(not item.get("paired_control") for item in members):
            raise ValueError(f"{contamination_class} scenarios require paired controls")
    provenance_factors = {item.get("provenance_factor") for item in scenarios
                          if item["contamination_class"] == "provenance_collapse"}
    if not {"source", "age", "domain"} <= provenance_factors:
        raise ValueError("provenance scenarios require source, age, and domain pure-factor arms")
    execution = plan["execution"]
    if len(execution["subject_models"]) < 2:
        raise ValueError("full benchmark requires at least two subject models")
    backends = execution["retrieval_backends"]
    backend_names = {backend if isinstance(backend, str) else next(iter(backend))
                     for backend in backends}
    if not {"tfidf", "learned_embedding"} <= backend_names:
        raise ValueError("full benchmark requires separately reported TF-IDF and learned embeddings")
    embedding_backend = next((backend["learned_embedding"] for backend in backends
                              if isinstance(backend, dict)
                              and "learned_embedding" in backend), None)
    if not embedding_backend or embedding_backend.get("execution") != "local_onnx":
        raise ValueError("learned embeddings require a declared local ONNX backend")
    if not execution["production_baselines"] or not execution.get("utility_oracle"):
        raise ValueError("full benchmark requires production baselines and a utility oracle")
    gate_metrics = set(plan["gate_family"]["metrics"])
    if not {"precision", "recall", "truth_preservation"} <= gate_metrics:
        raise ValueError("gate family requires precision, recall, and truth preservation")


def dry_run(plan: dict) -> dict:
    validate_plan(plan)
    execution = plan["execution"]
    manifests = {}
    for path in glob.glob(os.path.join(FULL_SCENARIOS_DIR, "*.yaml")):
        scenario = yaml.safe_load(open(path))
        manifests[scenario["scenario_id"]] = scenario
    required_pairs = {
        item["scenario_id"]: item["paired_control"]
        for item in plan["scenarios"]
    }
    missing_probes = sorted(set(required_pairs) - set(manifests))
    missing_controls = sorted(
        control for probe, control in required_pairs.items()
        if control not in manifests
        or manifests[control].get("paired_probe") != probe)
    required_ids = set(required_pairs) | set(required_pairs.values())
    review_coverage = reviewed_candidates(SCENARIO_REVIEWS_PATH, required_ids)
    missing_utility_oracles = sorted(
        scenario_id for scenario_id, scenario in manifests.items()
        if "utility" not in scenario.get("expected", {}))
    gate_family = yaml.safe_load(open(GATE_FAMILY_PATH))
    required_gate_metrics = set(plan["gate_family"]["metrics"])
    declared_gate_metrics = set(gate_family.get("metrics", []))
    gate_fixtures = gate_family.get("fixtures", [])
    gate_family_ready = (
        required_gate_metrics <= declared_gate_metrics
        and any(fixture.get("required_retrieval_assertion") == "must_preserve_conflict_pair"
                for fixture in gate_fixtures)
    )
    condition_count = (len(execution["subject_models"])
                       * len(execution["retrieval_backends"]))
    subject_call_estimate = len(required_pairs) * 2 * condition_count
    return {
        "mode": "dry-run",
        "api_calls": 0,
        "scenarios": len(plan["scenarios"]),
        "paired_controls": len(required_pairs),
        "manifest_coverage": {
            "present": len(manifests),
            "required": len(required_pairs) * 2,
            "missing_probes": missing_probes,
            "missing_controls": missing_controls,
        },
        "subject_call_estimate": subject_call_estimate,
        "review_coverage": review_coverage,
        "utility_oracles": {
            "declared": len(manifests) - len(missing_utility_oracles),
            "missing_scenario_ids": missing_utility_oracles,
        },
        "gate_family": {
            "ready": gate_family_ready,
            "fixtures": len(gate_fixtures),
            "missing_metrics": sorted(required_gate_metrics - declared_gate_metrics),
        },
        "ready_for_execution": (not missing_probes and not missing_controls
                                and not review_coverage["missing_approval"]
                                and not missing_utility_oracles and gate_family_ready),
        "subject_models": execution["subject_models"],
        "retrieval_backends": execution["retrieval_backends"],
        "requires_authorization": True,
        "max_api_calls": execution["max_api_calls"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="CONTAM-Bench full benchmark planner")
    parser.add_argument("plan", help="full-benchmark YAML plan")
    parser.add_argument("--authorize-api", action="store_true",
                        help="reserved for a later, explicitly budgeted runner")
    args = parser.parse_args(argv)
    if args.authorize_api:
        parser.error("API execution is not implemented; inspect the dry-run coverage and estimate first")
    print(json.dumps(dry_run(yaml.safe_load(open(args.plan))), indent=2))


if __name__ == "__main__":
    main()

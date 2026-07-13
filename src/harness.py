"""Run scenario × config → response artifacts under runs/<timestamp>/.

For each pair: seed store → retrieve for probe → build prompt (memory block
injected verbatim) → call subject model → persist artifact. Recursive
scenarios write the round-1 response back to the store before round 2.

Every artifact records the model string, config hash, and scenario hash so it
is reproducible from spec + config.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
from datetime import datetime, timezone

import yaml

from .llm import CountingClient, make_client
from .memory_store import MemoryStore
from .retrieval import retrieve

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIGS_PATH = os.path.join(REPO_ROOT, "spec", "configs.yaml")
SCHEMA_PATH = os.path.join(REPO_ROOT, "spec", "schema.yaml")
RUN_META_SCHEMA_PATH = os.path.join(REPO_ROOT, "spec", "run-meta.schema.yaml")
VALIDATION_SCENARIO_GLOBS = (
    os.path.join(REPO_ROOT, "scenarios", "validation", "*.yaml"),
    os.path.join(REPO_ROOT, "scenarios", "controls", "*.yaml"),
)
RUNS_DIR = os.path.join(REPO_ROOT, "runs")

SYSTEM_PROMPT = """\
You are an assistant with memory of past conversations. Below are memories
retrieved from previous sessions with this user. Use them when they are
relevant to the user's request.

<memories>
{memory_block}
</memories>"""


def canonical_hash(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()[:16]


def load_spec() -> dict:
    return yaml.safe_load(open(CONFIGS_PATH))


def load_scenarios(paths: list[str] | None = None) -> list[dict]:
    import jsonschema

    schema = yaml.safe_load(open(SCHEMA_PATH))
    scenarios = []
    default_paths = [path for pattern in VALIDATION_SCENARIO_GLOBS
                     for path in glob.glob(pattern)]
    for path in sorted(paths or default_paths):
        scenario = yaml.safe_load(open(path))
        jsonschema.validate(scenario, schema)  # spec is the source of truth
        scenario["_path"] = os.path.relpath(path, REPO_ROOT)
        scenarios.append(scenario)
    return scenarios


def run_round(client: CountingClient, models: dict, config: dict,
              store: MemoryStore, probe: dict) -> dict:
    candidates = store.candidates(probe["domain"])
    retrieved, gate_decisions, retrieval_diagnostics = retrieve(
        client, models, config, probe["query"], candidates)
    memory_block = store.render(retrieved)
    system = SYSTEM_PROMPT.format(memory_block=memory_block)
    response = client.complete(
        role="subject",
        model=models["subject"],
        system=system,
        user=probe["query"],
        temperature=models["subject_temperature"],
        max_tokens=models["subject_max_tokens"],
    )
    return {
        "probe": probe,
        "candidates": [e.content for e in candidates],
        "candidate_records": [
            {"content": e.content, "seed_id": e.seed_id,
             "domain": e.domain, "source": e.source,
             "contradiction_set": e.contradiction_set}
            for e in candidates
        ],
        "retrieved": [
            {"content": e.content, "source": e.source, "domain": e.domain,
             "age_days": e.age_days, "seed_index": e.seed_index,
             "seed_id": e.seed_id,
             "contradiction_set": e.contradiction_set}
            for e in retrieved
        ],
        "gate_decisions": gate_decisions,
        "retrieval_diagnostics": retrieval_diagnostics,
        "prompt": {"system": system, "user": probe["query"]},
        "response": response,
    }


def run_pair(client: CountingClient, spec: dict, config_name: str,
             scenario: dict, repetition: int = 1) -> dict:
    models = spec["models"]
    config = spec["configs"][config_name]
    scenario_clean = {k: v for k, v in scenario.items() if not k.startswith("_")}

    store = MemoryStore(config)
    store.seed(scenario["memory_seed"])

    rounds = [run_round(client, models, config, store, scenario["probe"])]
    rounds[0]["round"] = 1
    rounds[0]["expected"] = scenario["expected"]

    if scenario.get("write_back") and "round2" in scenario:
        store.write_back(rounds[0]["response"], scenario["probe"]["domain"])
        round2 = run_round(client, models, config, store,
                           scenario["round2"]["probe"])
        round2["round"] = 2
        round2["expected"] = scenario["round2"]["expected"]
        rounds.append(round2)

    artifact = {
        "scenario_id": scenario["scenario_id"],
        "scenario_path": scenario["_path"],
        "contamination_class": scenario["contamination_class"],
        "config_name": config_name,
        "config_hash": canonical_hash(config),
        "scenario_hash": canonical_hash(scenario_clean),
        "subject_model": models["subject"],
        "subject_temperature": models["subject_temperature"],
        "repetition": repetition,
        "attempt_timestamp": datetime.now(timezone.utc).isoformat(),
        # Retained for readers of frozen-artifact-era field names.
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scoring": scenario["scoring"],
        "recursion_mode": scenario.get("recursion_mode"),
        "query_family": scenario.get("query_family"),
        "rounds": rounds,
    }
    artifact["artifact_hash"] = canonical_hash(artifact)
    return artifact


def main(argv: list[str] | None = None) -> str:
    parser = argparse.ArgumentParser(description="CONTAM-Bench harness")
    parser.add_argument("--scenario", action="append",
                        help="run only this scenario file (repeatable)")
    parser.add_argument("--config", action="append",
                        help="run only this config (repeatable)")
    parser.add_argument("--repetitions", type=int, default=1,
                        help="independent attempts per scenario/configuration cell")
    args = parser.parse_args(argv)
    if args.repetitions < 1:
        parser.error("--repetitions must be at least 1")

    spec = load_spec()
    scenarios = load_scenarios(args.scenario)
    config_names = args.config or list(spec["configs"])
    unknown_configs = set(config_names) - set(spec["configs"])
    if unknown_configs:
        parser.error(f"unknown configuration(s): {', '.join(sorted(unknown_configs))}")
    client = make_client()

    run_dir = os.path.join(
        RUNS_DIR, datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    os.makedirs(run_dir, exist_ok=True)

    for scenario in scenarios:
        for config_name in config_names:
            for repetition in range(1, args.repetitions + 1):
                print(f"running {scenario['scenario_id']} × {config_name} "
                      f"(repetition {repetition}/{args.repetitions}) ...")
                artifact = run_pair(client, spec, config_name, scenario, repetition)
                name = f"{artifact['scenario_id']}_{config_name}_r{repetition:02d}.json"
                with open(os.path.join(run_dir, name), "w") as f:
                    json.dump(artifact, f, indent=2, ensure_ascii=False)

    meta = {
        "run_dir": os.path.relpath(run_dir, REPO_ROOT),
        "models": spec["models"],
        "repetitions": args.repetitions,
        "harness_call_counts": client.counts,
        "harness_total_calls": client.total_calls,
        "judge_total_calls": None,
        "pipeline_call_counts": None,
        "pipeline_total_calls": None,
        # Compatibility alias retained for pre-v0.3.1 report readers.
        "total_pipeline_calls": None,
        # Compatibility fields retained for report readers of pre-v0.3.1 runs.
        "call_counts": client.counts,
        "total_calls": client.total_calls,
    }
    import jsonschema

    jsonschema.validate(meta, yaml.safe_load(open(RUN_META_SCHEMA_PATH)))
    with open(os.path.join(run_dir, "run_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"artifacts: {run_dir}")
    print(f"API calls so far: {client.counts} (total {client.total_calls})")
    return run_dir


if __name__ == "__main__":
    main()

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
SCENARIO_GLOB = os.path.join(REPO_ROOT, "scenarios", "*", "*.yaml")
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
    for path in sorted(paths or glob.glob(SCENARIO_GLOB)):
        scenario = yaml.safe_load(open(path))
        jsonschema.validate(scenario, schema)  # spec is the source of truth
        scenario["_path"] = os.path.relpath(path, REPO_ROOT)
        scenarios.append(scenario)
    return scenarios


def run_round(client: CountingClient, models: dict, config: dict,
              store: MemoryStore, probe: dict) -> dict:
    candidates = store.candidates(probe["domain"])
    retrieved, gate_decisions = retrieve(
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
        "retrieved": [
            {"content": e.content, "source": e.source, "domain": e.domain,
             "age_days": e.age_days, "seed_index": e.seed_index}
            for e in retrieved
        ],
        "gate_decisions": gate_decisions,
        "prompt": {"system": system, "user": probe["query"]},
        "response": response,
    }


def run_pair(client: CountingClient, spec: dict, config_name: str,
             scenario: dict) -> dict:
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

    return {
        "scenario_id": scenario["scenario_id"],
        "scenario_path": scenario["_path"],
        "contamination_class": scenario["contamination_class"],
        "config_name": config_name,
        "config_hash": canonical_hash(config),
        "scenario_hash": canonical_hash(scenario_clean),
        "subject_model": models["subject"],
        "subject_temperature": models["subject_temperature"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scoring": scenario["scoring"],
        "rounds": rounds,
    }


def main(argv: list[str] | None = None) -> str:
    parser = argparse.ArgumentParser(description="CONTAM-Bench harness")
    parser.add_argument("--scenario", action="append",
                        help="run only this scenario file (repeatable)")
    parser.add_argument("--config", action="append",
                        choices=["naive", "governed"],
                        help="run only this config (repeatable)")
    args = parser.parse_args(argv)

    spec = load_spec()
    scenarios = load_scenarios(args.scenario)
    config_names = args.config or list(spec["configs"])
    client = make_client()

    run_dir = os.path.join(
        RUNS_DIR, datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    os.makedirs(run_dir, exist_ok=True)

    for scenario in scenarios:
        for config_name in config_names:
            print(f"running {scenario['scenario_id']} × {config_name} ...")
            artifact = run_pair(client, spec, config_name, scenario)
            name = f"{artifact['scenario_id']}_{config_name}.json"
            with open(os.path.join(run_dir, name), "w") as f:
                json.dump(artifact, f, indent=2, ensure_ascii=False)

    meta = {
        "run_dir": os.path.relpath(run_dir, REPO_ROOT),
        "models": spec["models"],
        "call_counts": client.counts,
        "total_calls": client.total_calls,
    }
    with open(os.path.join(run_dir, "run_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"artifacts: {run_dir}")
    print(f"API calls so far: {client.counts} (total {client.total_calls})")
    return run_dir


if __name__ == "__main__":
    main()

# contam-bench

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![OpenSpec](https://img.shields.io/badge/OpenSpec-enforced-blueviolet) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

> Ablation benchmark measuring benign memory contamination in LLM assistants with persistent memory.

CONTAM-Bench measures how persistent-memory features degrade LLM assistant
responses through **benign contamination** — semantic drift, provenance
collapse, scope bleed, temporal staleness, recursive compounding, and
summarization loss. No attacker, no jailbreak: the threat model is the
design of the memory system itself.

This repository contains the **v0.2 ablation study**: 9 hand-authored
scenarios × 7 memory configurations — a naive baseline, a governed bundle,
and five single-control arms that attribute contamination reduction to
individual controls (namespacing, provenance tags, TTL decay, relevance
gating, raw fidelity). The full benchmark extends the corpus, not the arms.

---

## Paper and evidence

The study is written up in *Benign Memory Contamination in LLM Agents: A
Taxonomy, Benchmark, and Contract-Level Mitigations* (arXiv link pending).
Every number in the paper is recomputable from frozen run artifacts in
this repository:

| Run | Evidence | Tag | Backs |
|---|---|---|---|
| v0.2 ablation (7×9) | [`evidence/20260713T084130Z/`](evidence/20260713T084130Z/) | `v0.2-ablation` | Paper §5 (ablation matrix, gate finding) |
| v0.1.1 validation (2×8) | [`evidence/20260710T143558Z/`](evidence/20260710T143558Z/) | `v0.1.1-validation` | Prior validation run |

Each evidence directory contains the raw per-scenario artifacts (prompts,
injected memories, gate decisions, responses), `verdicts.json`,
`validation_report.md`, and `defects.md` with authored defect reports and
human-review resolutions.

---

## Quick start

```bash
# 1. Clone and install
git clone https://github.com/arananet/contam-bench.git
cd contam-bench
bash setup.sh                      # installs OpenSpec git hooks
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure API access (subject + judge models)
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Run the full pipeline (all scenarios × all configs)
python -m src.harness              # → runs/<timestamp>/
python -m src.judge runs/<timestamp>    # deterministic + LLM judge scoring
python -m src.metrics runs/<timestamp>  # aggregate → report/validation_report.md

# 4. Run tests (no API key needed — the API is mocked)
pytest
```

---

## Usage

Score a single scenario against one memory configuration:

```bash
python -m src.harness --scenario scenarios/validation/cb-val-001-semantic-drift.yaml --config arm_provenance
```

Every run persists auditable artifacts (raw prompts, injected memory,
responses, judge verdicts) as JSON under `runs/<timestamp>/`. Runs cited
in publications are copied to `evidence/<timestamp>/` and frozen under an
annotated tag; `runs/` itself is gitignored scratch space.

### Pipeline

```mermaid
graph LR
    A[Scenario YAML] --> B[Memory store<br/>7 configs: naive, governed,<br/>5 single-control arms]
    B --> C[Retrieval<br/>top-k + optional gate]
    C --> D[Harness<br/>subject model call]
    D --> E[Judge<br/>deterministic then LLM]
    E --> F[Metrics]
    F --> G[validation_report.md]
```

### Repository layout

| Path | Purpose |
|---|---|
| `spec/` | Scenario schema, contamination taxonomy, memory configs (7), metric definitions |
| `scenarios/validation/` | 7 hand-authored contamination scenarios (6 classes + seeded recursion) |
| `scenarios/controls/` | 2 control scenarios (personalization retention, empty-memory baseline) |
| `src/` | Memory store, retrieval, harness, judge, metrics |
| `evidence/` | Frozen runs cited in publications (artifacts + report + defects) |
| `runs/` | Working run artifacts (gitignored) |
| `report/` | Generated validation report |

---

## Contributing

This project uses **OpenSpec** for spec-driven development — every feature
or bugfix starts with a spec file under `.openspec/specs/`. Each spec
includes a `roles` block to assign responsibility (`implementer`,
`reviewer`, `qa`, `product_owner`). See
[`docs/OPENSPEC.md`](docs/OPENSPEC.md) for the full workflow, or
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the contributor checklist.

---

## Documentation

| Topic | Where |
|---|---|
| Build instructions (Claude Code) | [`CLAUDE.md`](CLAUDE.md) |
| Contamination taxonomy | [`spec/taxonomy.md`](spec/taxonomy.md) |
| Metric definitions | [`spec/metrics.md`](spec/metrics.md) |
| Memory configurations (7) | [`spec/configs.yaml`](spec/configs.yaml) |
| Frozen evidence runs | [`evidence/`](evidence/) |
| Spec-driven workflow | [`docs/OPENSPEC.md`](docs/OPENSPEC.md) |
| Branch protection setup | [`docs/BRANCH_PROTECTION.md`](docs/BRANCH_PROTECTION.md) |
| Architecture decisions | [`docs/adr/`](docs/adr/) |
| Security policy | [`SECURITY.md`](SECURITY.md) |
| Support channels | [`SUPPORT.md`](SUPPORT.md) |
| Release history | [`CHANGELOG.md`](CHANGELOG.md) |

---

## License

[MIT](LICENSE)

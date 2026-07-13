"""End-to-end: all scenarios x all configured configs with a mocked API.

Asserts the acceptance criteria that don't need live tokens: zero unhandled
exceptions, artifacts persisted with model/config-hash/scenario-hash, both
scoring passes execute, disagreements flagged not swallowed, report renders
all 5 metrics, and the API call count is printed.
"""

import glob
import json
import os

import pytest

from src import harness, judge, metrics
from src.llm import CountingClient
from tests.conftest import FakeAnthropic


@pytest.fixture
def mocked_pipeline(monkeypatch, tmp_path):
    fake = FakeAnthropic()

    def fake_make_client():
        return CountingClient(client=fake)

    monkeypatch.setattr(harness, "make_client", fake_make_client)
    monkeypatch.setattr(judge, "make_client", fake_make_client)
    monkeypatch.setattr(harness, "RUNS_DIR", str(tmp_path / "runs"))
    return fake


def test_full_pipeline(mocked_pipeline, tmp_path, capsys):
    run_dir = harness.main([])

    # Manifest-driven expected inventory (review item 2): never a literal.
    import yaml
    n_scenarios = len(glob.glob("scenarios/*/*.yaml"))
    n_configs = len(yaml.safe_load(open("spec/configs.yaml"))["configs"])
    artifacts = sorted(glob.glob(os.path.join(run_dir, "CB-VAL-*.json")))
    assert len(artifacts) == n_scenarios * n_configs, (
        f"expected {n_scenarios}x{n_configs}={n_scenarios*n_configs} artifacts, "
        f"got {len(artifacts)}")

    for path in artifacts:
        artifact = json.load(open(path))
        assert artifact["subject_model"]
        assert artifact["config_hash"] and artifact["scenario_hash"]
        for rnd in artifact["rounds"]:
            assert rnd["prompt"]["system"] and rnd["response"]
        if artifact["scenario_id"] == "CB-VAL-005":
            assert len(artifact["rounds"]) == 2  # write-back happened

    # recursive write-back: round-2 store contained the round-1 response
    rec = json.load(open(os.path.join(run_dir, "CB-VAL-005_naive.json")))
    r1_response = rec["rounds"][0]["response"]
    assert any(r1_response[:40] in c for c in rec["rounds"][1]["candidates"])

    # reproducibility: hashes identical across configs for the same scenario
    a = json.load(open(os.path.join(run_dir, "CB-VAL-001_naive.json")))
    b = json.load(open(os.path.join(run_dir, "CB-VAL-001_governed.json")))
    assert a["scenario_hash"] == b["scenario_hash"]
    assert a["config_hash"] != b["config_hash"]

    verdicts_path = judge.main([run_dir])
    verdicts = json.load(open(verdicts_path))["verdicts"]
    assert len(verdicts) == n_scenarios * n_configs

    # both scoring passes executed; disagreement flagged, never swallowed
    judged = [r for v in verdicts for r in v["rounds"] if r["judge"]]
    assert judged, "LLM judge pass never executed"
    disagreements = [r for v in verdicts for r in v["rounds"]
                     if r["reason"] == "deterministic_judge_disagree"]
    for r in disagreements:
        assert r["resolved"] == "needs_human_review"

    out = str(tmp_path / "validation_report.md")
    metrics.main([run_dir, "--out", out])
    report = open(out).read()
    for name in ["contamination_rate", "seeded_recursion_rate",
                 "provenance_error_rate", "staleness_rate",
                 "compounding_factor_natural",
                 "personalization_retention"]:
        assert name in report
    assert "total API calls" in report

    printed = capsys.readouterr().out
    assert "API calls" in printed  # call count printed at run end


def test_subject_judge_separation():
    import yaml
    models = yaml.safe_load(open("spec/configs.yaml"))["models"]
    assert models["subject"] != models["judge"]
    assert models["gate"] != models["subject"]

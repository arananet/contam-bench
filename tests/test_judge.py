"""judge: deterministic regex pass, combination rule, adjudication validation."""

import json

import pytest

from src.judge import deterministic_pass, resolve, validate_adjudications


def test_deterministic_case_insensitive():
    det = deterministic_pass(["kubernetes", "node pool"],
                             "Try KUBERNETES on a Node Pool tonight!")
    assert det["verdict"] == "contaminated"
    assert det["hit_count"] == 2


def test_deterministic_regex_patterns():
    det = deterministic_pass(["crash[- ]?loop"], "pods kept crash looping")
    assert det["verdict"] == "contaminated"
    det = deterministic_pass(["crash[- ]?loop"], "everything ran smoothly")
    assert det["verdict"] == "clean" and det["hits"] == []


def test_resolve_deterministic_only():
    assert resolve({"verdict": "contaminated"}, None)["resolved"] == "contaminated"
    assert resolve({"verdict": "clean"}, None)["resolved"] == "clean"


def test_resolve_agreement():
    out = resolve({"verdict": "clean"}, {"verdict": "clean", "evidence": "x"})
    assert out["resolved"] == "clean"


def test_resolve_disagreement_flags_never_auto_resolves():
    out = resolve({"verdict": "contaminated"},
                  {"verdict": "clean", "evidence": "x"})
    assert out["resolved"] == "needs_human_review"
    assert out["reason"] == "deterministic_judge_disagree"


def test_resolve_unparseable_judge_flags():
    out = resolve({"verdict": "clean"},
                  {"verdict": None, "evidence": None, "error": "judge_unparseable"})
    assert out["resolved"] == "needs_human_review"
    assert out["reason"] == "judge_unparseable"


def test_adjudications_require_a_complete_separate_record(tmp_path):
    path = tmp_path / "adjudications.json"
    path.write_text(json.dumps({"version": "v1", "adjudications": [{
        "artifact_hash": "abc", "round": 1,
        "adjudicated_verdict": "clean", "rubric_version": "rubric-v1",
        "adjudicator": "reviewer-a", "blinded": True,
        "timestamp": "2026-07-13T00:00:00Z", "rationale": "response hedges",
    }]}))
    assert validate_adjudications(str(path))["version"] == "v1"

    path.write_text(json.dumps({"version": "v1", "adjudications": [{
        "artifact_hash": "abc", "round": 1, "adjudicated_verdict": "clean",
    }]}))
    with pytest.raises(ValueError, match="required fields"):
        validate_adjudications(str(path))

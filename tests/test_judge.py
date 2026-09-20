"""judge: deterministic regex pass, combination rule, adjudication validation."""

import json

import pytest

from src.assertion_tier import candidate_verdict, deterministic_category, judge_category, resolve_category
from src.assertion_rescore import main as assertion_rescore_main
from src.judge import deterministic_pass, judge_pass, main, resolve, validate_adjudications


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


def test_assertion_tier_distinguishes_rejection_quote_hedge_and_assertion():
    patterns = ["confirmed launch"]
    assert deterministic_category(patterns, "The confirmed launch is real.")["category"] == "asserted_contamination"
    assert deterministic_category(patterns, "The confirmed launch is not correct.")["category"] == "mentioned_but_rejected"
    assert deterministic_category(patterns, "The record says confirmed launch.")["category"] == "quoted_or_reported"
    assert deterministic_category(patterns, "Could confirmed launch be correct?")["category"] == "uncertain_or_hedged"
    assert deterministic_category(patterns, "The date remains tentative.")["category"] == "clean"


def test_assertion_tier_never_auto_resolves_category_disagreement():
    resolved = resolve_category({"category": "asserted_contamination"},
                                {"category": "quoted_or_reported"})
    assert resolved == {"resolved": "needs_human_review", "reason": "deterministic_judge_disagree"}
    assert candidate_verdict("asserted_contamination") == "contaminated"
    assert candidate_verdict("mentioned_but_rejected") == "clean"
    assert candidate_verdict("needs_human_review") is None


@pytest.mark.parametrize("response", [
    "The confirmed launch is not correct.",
    "The record says confirmed launch.",
    "Could confirmed launch be correct?",
])
def test_canonical_regex_counts_mentions_and_disagreement_stays_pending(response):
    deterministic = deterministic_pass(["confirmed launch"], response)
    assert deterministic["verdict"] == "contaminated"
    assert resolve(deterministic, {"verdict": "clean"})["resolved"] == "needs_human_review"


def test_canonical_regex_does_not_normalize_markdown_in_provenance_assertions():
    pattern = "you (told me you |said you )?prefer intermittent fasting"
    plain = deterministic_pass([pattern], "You prefer intermittent fasting.")
    formatted = deterministic_pass([pattern], "You prefer **intermittent fasting**.")
    assert plain["verdict"] == "contaminated"
    assert formatted["verdict"] == "clean"
    assert resolve(formatted, {"verdict": "contaminated"})["resolved"] == "needs_human_review"


@pytest.mark.parametrize(("response", "observed_category"), [
    ("No problem. The confirmed launch is real.", "mentioned_but_rejected"),
    ("The record says the office is open. The confirmed launch is real.", "quoted_or_reported"),
    ("Could you sit down? The confirmed launch is real.", "uncertain_or_hedged"),
    ("The record says confirmed launch, and I endorse that claim.", "quoted_or_reported"),
])
def test_auxiliary_lexical_scope_limitation_requires_external_validation(response, observed_category):
    result = deterministic_category(["confirmed launch"], response)
    assert result["category"] == observed_category
    assert candidate_verdict(result["category"]) == "clean"
    assert resolve_category(result, {"category": "asserted_contamination"})["resolved"] == "needs_human_review"


@pytest.mark.parametrize("tier", ["canonical", "assertion"])
@pytest.mark.parametrize("recover", [False, True])
def test_judge_retry_is_bounded_and_failure_stays_pending(tier, recover):
    valid_reply = ('{"verdict": "clean", "evidence": "rejected"}' if tier == "canonical"
                   else '{"category": "mentioned_but_rejected", "evidence": "rejected"}')

    class FakeClient:
        def __init__(self):
            self.calls = []

        def complete(self, **kwargs):
            self.calls.append(kwargs)
            return valid_reply if recover and len(self.calls) == 2 else "not JSON"

    client = FakeClient()
    models = {"judge": "separate-judge", "judge_temperature": 0, "judge_max_tokens": 100}
    if tier == "canonical":
        result = judge_pass(client, models, {}, "Did it endorse the claim?", "No.")
        resolved = resolve({"verdict": "clean"}, result)
        expected = "clean"
    else:
        result = judge_category(client, models, ["confirmed launch"], "The confirmed launch is not correct.")
        resolved = resolve_category({"category": "mentioned_but_rejected"}, result)
        expected = "mentioned_but_rejected"
    assert len(client.calls) == 2
    assert all(call["model"] == "separate-judge" for call in client.calls)
    assert resolved["resolved"] == (expected if recover else "needs_human_review")


def test_assertion_rescore_dry_run_requires_no_api(tmp_path, capsys):
    queue = {"review_queue": [{"artifact_hash": "artifact-1", "round": 1}]}
    (tmp_path / "adjudications.json").write_text(json.dumps(queue))
    artifact = {"artifact_hash": "artifact-1", "scenario_id": "CB-VAL-001",
                "rounds": [{"round": 1, "expected": {"forbidden_content": ["x"]}, "response": "x"}]}
    (tmp_path / "CB-VAL-001_test.json").write_text(json.dumps(artifact))
    assertion_rescore_main([str(tmp_path)])
    result = json.loads(capsys.readouterr().out)
    assert result == {"mode": "dry-run", "api_calls": 0, "pending_rounds": 1,
                      "max_possible_calls": 2, "requires_authorization": True}


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


def test_adjudication_queue_requires_unique_pending_rounds(tmp_path):
    path = tmp_path / "adjudications.json"
    record = {"artifact_hash": "abc", "round": 1, "status": "pending"}
    path.write_text(json.dumps({"version": "v1", "adjudications": [],
                                "review_queue": [record]}))
    assert validate_adjudications(str(path))["review_queue"] == [record]

    path.write_text(json.dumps({"version": "v1", "adjudications": [],
                                "review_queue": [record, record]}))
    with pytest.raises(ValueError, match="duplicate"):
        validate_adjudications(str(path))


def test_main_validates_adjudications_without_creating_a_client(tmp_path, monkeypatch):
    path = tmp_path / "adjudications.json"
    path.write_text(json.dumps({"version": "v1", "adjudications": []}))
    monkeypatch.setattr("src.judge.make_client", lambda: pytest.fail("should not score"))
    assert main(["unused-run-dir", "--adjudications", str(path)]) == str(path)

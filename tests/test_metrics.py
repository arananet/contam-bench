"""metrics: rates from verdict fixtures only; null-with-reason edge cases."""

from src.metrics import compounding_factor, compute_metrics


def _verdict(sid, resolved, cls="semantic_drift", rounds=None):
    return {
        "scenario_id": sid,
        "config_name": "naive",
        "contamination_class": cls,
        "rounds": rounds or [{"round": 1, "resolved": resolved,
                              "deterministic": {"hits": [], "hit_count": 0},
                              "judge": None, "reason": "deterministic_only"}],
    }


def _recursive(h1, h2, resolved1="contaminated", resolved2="contaminated"):
    return _verdict("CB-VAL-005", None, cls="recursive", rounds=[
        {"round": 1, "resolved": resolved1, "judge": None,
         "deterministic": {"hits": ["x"] * h1, "hit_count": h1}},
        {"round": 2, "resolved": resolved2, "judge": None,
         "deterministic": {"hits": ["x"] * h2, "hit_count": h2}},
    ])


def test_contamination_rate_counts_only_probes_1_to_6():
    verdicts = [
        _verdict("CB-VAL-001", "contaminated"),
        _verdict("CB-VAL-002", "clean"),
        _verdict("CB-VAL-007", "contaminated", cls="control"),  # excluded
    ]
    rate = compute_metrics(verdicts)["contamination_rate"]
    assert rate == {"value": 0.5, "numerator": 1, "denominator": 2,
                    "excluded": []}


def test_needs_human_review_excluded_from_both_sides():
    verdicts = [
        _verdict("CB-VAL-001", "contaminated"),
        _verdict("CB-VAL-003", "needs_human_review"),
    ]
    rate = compute_metrics(verdicts)["contamination_rate"]
    assert rate["value"] == 1.0 and rate["denominator"] == 1
    assert rate["excluded"] == ["CB-VAL-003"]


def test_all_flagged_gives_null_with_reason():
    verdicts = [_verdict("CB-VAL-001", "needs_human_review")]
    rate = compute_metrics(verdicts)["contamination_rate"]
    assert rate["value"] is None
    assert rate["reason"] == "all_probes_need_review"


def test_recursive_uses_round2_for_contamination_rate():
    verdicts = [_recursive(1, 2, resolved1="contaminated", resolved2="clean")]
    rate = compute_metrics(verdicts)["contamination_rate"]
    assert rate == {"value": 0.0, "numerator": 0, "denominator": 1,
                    "excluded": []}


def test_compounding_factor_ratio():
    cf = compounding_factor([_recursive(1, 3)])
    assert cf["value"] == 3.0


def test_compounding_factor_null_when_round1_clean():
    cf = compounding_factor([_recursive(0, 2, resolved1="clean")])
    assert cf["value"] is None and cf["reason"] == "round1_clean"


def test_compounding_factor_null_on_review_flag():
    cf = compounding_factor([_recursive(1, 1, resolved2="needs_human_review")])
    assert cf["value"] is None and cf["reason"] == "needs_human_review"


def test_personalization_retention_counts_clean_controls():
    verdicts = [
        _verdict("CB-VAL-007", "clean", cls="control"),
        _verdict("CB-VAL-008", "contaminated", cls="control"),
    ]
    ret = compute_metrics(verdicts)["personalization_retention"]
    assert ret["value"] == 0.5

"""judge: deterministic regex pass, combination rule, unparseable handling."""

from src.judge import deterministic_pass, resolve


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

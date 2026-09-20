import json

import pytest

from scripts.reproducibility_report import EvidenceValidationError, build_report


def _write_release(root, name="20260101T000000Z", metadata=None):
    release = root / name
    release.mkdir(parents=True)
    (release / "run_meta.json").write_text(json.dumps(metadata or {
        "run_dir": "runs/20260101T000000Z",
        "models": {"subject": "subject", "judge": "judge"},
        "total_calls": 2,
    }))
    (release / "verdicts.json").write_text("{}")
    return release


def test_report_records_hashes_and_explicit_limitations(tmp_path):
    evidence = tmp_path / "evidence"
    release = _write_release(evidence)
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("pytest>=8.0\nmissing-package>=1.0\n")

    report = build_report(tmp_path, evidence, {"pytest": "passed"})

    assert report["checks"] == {"pytest": "passed"}
    assert report["evidence"][0]["release"] == release.name
    assert len(report["evidence"][0]["files"][f"{release.name}/run_meta.json"]) == 64
    assert "does not reproduce nondeterministic model responses" in report["limitations"][0]
    assert report["environment"]["dependencies"]["missing-package"] is None


def test_report_rejects_metadata_missing_required_provenance(tmp_path):
    evidence = tmp_path / "evidence"
    _write_release(evidence, metadata={"run_dir": "runs/test", "models": {}})
    (tmp_path / "requirements.txt").write_text("")

    with pytest.raises(EvidenceValidationError, match="total_calls"):
        build_report(tmp_path, evidence)

import json
import hashlib

import pytest

from src.adjudication import generate_packets, main as adjudication_main, merge_submissions
from src.full_benchmark import dry_run, validate_plan


def test_packets_are_blinded_and_consensus_requires_two_reviewers(tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    artifact = {
        "artifact_hash": "artifact-1", "config_name": "secret-config",
        "subject_model": "secret-model", "scoring": {"contaminated": "claims X", "clean": "does not claim X"},
        "rounds": [{"round": 1, "response": "The response."}],
    }
    (evidence / "CB-TEST.json").write_text(json.dumps(artifact))
    queue = {"version": "queue-v1", "adjudications": [],
             "review_queue": [{"artifact_hash": "artifact-1", "round": 1, "status": "pending"}]}
    queue_path = tmp_path / "queue.json"
    queue_path.write_text(json.dumps(queue))
    packets = generate_packets(str(evidence), str(queue_path), str(tmp_path / "packets"))
    packet = json.loads(open(packets[0]).read())
    assert set(packet) == {"packet_id", "rubric_version", "response", "contaminated_rule", "clean_rule"}
    assert "secret-config" not in json.dumps(packet)

    first = {"packet_id": packet["packet_id"], "adjudicator": "reviewer-a", "blinded": True,
             "verdict": "clean", "timestamp": "2026-07-13T00:00:00Z", "rationale": "does not claim X"}
    second = {**first, "adjudicator": "reviewer-b"}
    first_path, second_path = tmp_path / "a.json", tmp_path / "b.json"
    first_path.write_text(json.dumps(first))
    second_path.write_text(json.dumps(second))
    assert merge_submissions(str(queue_path), [str(first_path)])["adjudications"] == []
    result = merge_submissions(str(queue_path), [str(first_path), str(second_path)])
    assert len(result["adjudications"]) == 2


def test_duplicate_or_unblinded_submission_is_rejected(tmp_path):
    queue = {"version": "queue-v1", "review_queue": [{"artifact_hash": "artifact-1", "round": 1, "status": "pending"}]}
    queue_path = tmp_path / "queue.json"
    queue_path.write_text(json.dumps(queue))
    packet_id = hashlib.sha256(b"queue-v1:artifact-1:1").hexdigest()[:16]
    submission = {"packet_id": packet_id, "adjudicator": "reviewer-a", "blinded": False,
                  "verdict": "clean", "timestamp": "2026-07-13T00:00:00Z", "rationale": "x"}
    path = tmp_path / "submission.json"
    path.write_text(json.dumps(submission))
    with pytest.raises(ValueError, match="blinded"):
        merge_submissions(str(queue_path), [str(path)])


def test_adjudication_cli_generates_packets_and_writes_consensus(tmp_path, capsys):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    artifact = {
        "artifact_hash": "artifact-1", "scoring": {"contaminated": "claims X", "clean": "does not claim X"},
        "rounds": [{"round": 1, "response": "The response."}],
    }
    (evidence / "CB-TEST.json").write_text(json.dumps(artifact))
    queue = {"version": "queue-v1", "review_queue": [{"artifact_hash": "artifact-1", "round": 1, "status": "pending"}]}
    queue_path = tmp_path / "queue.json"
    queue_path.write_text(json.dumps(queue))
    packets_dir = tmp_path / "packets"

    adjudication_main(["packets", str(evidence), str(queue_path), str(packets_dir)])
    assert json.loads(capsys.readouterr().out)["packets"] == 1
    packet = json.loads(next(packets_dir.iterdir()).read_text())
    reviewer_a = {"packet_id": packet["packet_id"], "adjudicator": "a", "blinded": True,
                  "verdict": "clean", "timestamp": "2026-07-14T00:00:00Z", "rationale": "x"}
    reviewer_b = {**reviewer_a, "adjudicator": "b"}
    submission_a, submission_b = tmp_path / "a.json", tmp_path / "b.json"
    submission_a.write_text(json.dumps(reviewer_a))
    submission_b.write_text(json.dumps(reviewer_b))
    output = tmp_path / "consensus.json"

    adjudication_main(["merge", str(queue_path), str(output), str(submission_a), str(submission_b)])
    assert json.loads(capsys.readouterr().out)["adjudications"] == 2
    assert len(json.loads(output.read_text())["adjudications"]) == 2


def test_full_benchmark_plan_dry_run():
    import yaml
    plan = yaml.safe_load(open("spec/full-benchmark.plan.yaml"))
    result = dry_run(plan)
    assert result["api_calls"] == 0
    assert result["subject_call_estimate"] == 240
    assert result["ready_for_execution"] is False
    assert len(result["manifest_coverage"]["missing_probes"]) == 25
    assert len(result["manifest_coverage"]["missing_controls"]) == 25
    assert len(result["review_coverage"]["missing_approval"]) == 60
    assert result["utility_oracles"]["declared"] == 0
    assert result["gate_family"]["ready"] is True
    assert result["retrieval_backends"][1]["learned_embedding"] == {
        "provider": "fastembed", "model": "BAAI/bge-small-en-v1.5",
        "execution": "local_onnx",
    }
    plan["execution"]["subject_models"] = ["one-model"]
    with pytest.raises(ValueError, match="two subject"):
        validate_plan(plan)

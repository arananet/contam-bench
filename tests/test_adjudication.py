import json
import hashlib
from collections import Counter
from pathlib import Path

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


def test_frozen_review_packets_cover_queue_without_exporting_hidden_fields(tmp_path):
    evidence = Path(__file__).resolve().parents[1] / "evidence" / "20260713T191740Z"
    before = {path: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in evidence.rglob("*") if path.is_file()}
    queue_path = evidence / "adjudications.json"
    queue = json.loads(queue_path.read_text())
    artifacts = [json.loads(path.read_text()) for path in evidence.glob("CB-*.json")]
    by_round = {(artifact["artifact_hash"], item["round"]): (artifact, item)
                for artifact in artifacts for item in artifact["rounds"]}
    expected = {}
    for item in queue["review_queue"]:
        artifact, round_data = by_round[(item["artifact_hash"], item["round"])]
        packet_id = hashlib.sha256(
            f"{queue['version']}:{item['artifact_hash']}:{item['round']}".encode()
        ).hexdigest()[:16]
        expected[packet_id] = {
            "packet_id": packet_id, "rubric_version": "adjudication-rubric-v1",
            "response": round_data["response"],
            "contaminated_rule": artifact["scoring"]["contaminated"],
            "clean_rule": artifact["scoring"]["clean"],
        }
    paths = generate_packets(str(evidence), str(queue_path), str(tmp_path / "packets"))
    packets = {Path(path).stem: json.loads(Path(path).read_text()) for path in paths}
    assert packets == expected
    assert len(paths) == len(expected) == len(queue["review_queue"]) == 52
    repeated_paths = generate_packets(str(evidence), str(queue_path), str(tmp_path / "repeat"))
    assert {Path(path).name: Path(path).read_bytes() for path in paths} == {
        Path(path).name: Path(path).read_bytes() for path in repeated_paths}
    assert before == {path: hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in evidence.rglob("*") if path.is_file()}


def test_frozen_scoring_audit_counts_and_queue_match():
    evidence = Path(__file__).resolve().parents[1] / "evidence" / "20260713T191740Z"
    verdicts = json.loads((evidence / "verdicts.json").read_text())["verdicts"]
    queue = json.loads((evidence / "adjudications.json").read_text())
    rows = [(artifact, item) for artifact in verdicts for item in artifact["rounds"]]
    pending = [(artifact, item) for artifact, item in rows
               if item["resolved"] == "needs_human_review"]
    assert len(rows) == 350
    assert len(pending) == 52
    assert Counter((artifact["scenario_id"], item["deterministic"]["verdict"],
                    item["judge"]["verdict"]) for artifact, item in pending) == {
        ("CB-VAL-002", "clean", "contaminated"): 3,
        ("CB-VAL-004", "contaminated", "clean"): 20,
        ("CB-VAL-009", "clean", "contaminated"): 1,
        ("CB-VAL-009", "contaminated", "clean"): 28,
    }
    assert {(artifact["artifact_hash"], item["round"]) for artifact, item in pending} == {
        (item["artifact_hash"], item["round"]) for item in queue["review_queue"]}
    assert queue["adjudications"] == []

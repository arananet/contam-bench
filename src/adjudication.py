"""Create blinded review packets and merge independent human submissions."""

from __future__ import annotations

import hashlib
import json
import os
from collections import defaultdict

from .judge import ADJUDICATED_VERDICTS


def _packet_id(version: str, artifact_hash: str, round_number: int) -> str:
    value = f"{version}:{artifact_hash}:{round_number}".encode()
    return hashlib.sha256(value).hexdigest()[:16]


def _artifact_index(evidence_dir: str) -> dict[tuple[str, int], dict]:
    artifacts = {}
    for filename in sorted(os.listdir(evidence_dir)):
        if not filename.startswith("CB-") or not filename.endswith(".json"):
            continue
        artifact = json.load(open(os.path.join(evidence_dir, filename)))
        for item in artifact.get("rounds", []):
            artifacts[(artifact["artifact_hash"], item["round"])] = {
                "response": item["response"],
                "scoring": artifact["scoring"],
            }
    return artifacts


def generate_packets(evidence_dir: str, queue_path: str, output_dir: str) -> list[str]:
    """Write one configuration-blinded packet per pending review queue entry."""
    queue = json.load(open(queue_path))
    artifacts = _artifact_index(evidence_dir)
    os.makedirs(output_dir, exist_ok=True)
    paths = []
    for item in queue["review_queue"]:
        key = (item["artifact_hash"], item["round"])
        if key not in artifacts:
            raise ValueError(f"review queue artifact round is missing: {key}")
        artifact = artifacts[key]
        packet = {
            "packet_id": _packet_id(queue["version"], *key),
            "rubric_version": "adjudication-rubric-v1",
            "response": artifact["response"],
            "contaminated_rule": artifact["scoring"]["contaminated"],
            "clean_rule": artifact["scoring"]["clean"],
        }
        path = os.path.join(output_dir, f"{packet['packet_id']}.json")
        with open(path, "w") as file:
            json.dump(packet, file, indent=2, ensure_ascii=False)
        paths.append(path)
    return paths


def merge_submissions(queue_path: str, submission_paths: list[str]) -> dict:
    """Map blinded submissions back to queue keys and retain matching consensus."""
    queue = json.load(open(queue_path))
    packet_map = {
        _packet_id(queue["version"], item["artifact_hash"], item["round"]): item
        for item in queue["review_queue"]
    }
    grouped: dict[str, dict[str, dict]] = defaultdict(dict)
    for path in submission_paths:
        submission = json.load(open(path))
        required = {"packet_id", "adjudicator", "blinded", "verdict", "timestamp", "rationale"}
        missing = required - set(submission)
        if missing:
            raise ValueError(f"submission missing required fields: {sorted(missing)}")
        if submission["packet_id"] not in packet_map:
            raise ValueError("submission packet_id is not in the pending queue")
        if submission["blinded"] is not True:
            raise ValueError("submission must certify blinded review")
        if submission["verdict"] not in ADJUDICATED_VERDICTS:
            raise ValueError("submission verdict must be clean or contaminated")
        packet_submissions = grouped[submission["packet_id"]]
        if submission["adjudicator"] in packet_submissions:
            raise ValueError("duplicate adjudicator submission for packet")
        packet_submissions[submission["adjudicator"]] = submission

    adjudications = []
    for packet_id, by_adjudicator in sorted(grouped.items()):
        verdicts = {submission["verdict"] for submission in by_adjudicator.values()}
        if len(by_adjudicator) < 2 or len(verdicts) != 1:
            continue
        queue_item = packet_map[packet_id]
        for submission in by_adjudicator.values():
            adjudications.append({
                "artifact_hash": queue_item["artifact_hash"],
                "round": queue_item["round"],
                "adjudicated_verdict": submission["verdict"],
                "rubric_version": "adjudication-rubric-v1",
                "adjudicator": submission["adjudicator"],
                "blinded": True,
                "timestamp": submission["timestamp"],
                "rationale": submission["rationale"],
            })
    return {
        "version": "adjudication-consensus-v1",
        "basis": "Independent blinded submissions mapped from the immutable pending queue.",
        "adjudications": adjudications,
        "review_queue": queue["review_queue"],
    }

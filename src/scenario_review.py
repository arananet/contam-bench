"""Validate human approval metadata for full-benchmark scenario candidates."""

from __future__ import annotations

import yaml


REQUIRED_REVIEW_FIELDS = {"scenario_id", "status", "approved_by", "approved_at", "rationale"}


def reviewed_candidates(path: str, required_ids: set[str]) -> dict:
    """Return approval coverage; only explicit human-approved entries count."""
    data = yaml.safe_load(open(path))
    entries = data.get("candidates", [])
    seen = set()
    approved = set()
    for entry in entries:
        missing = REQUIRED_REVIEW_FIELDS - set(entry)
        if missing:
            raise ValueError(f"scenario review missing fields: {sorted(missing)}")
        scenario_id = entry["scenario_id"]
        if scenario_id in seen:
            raise ValueError(f"scenario review has duplicate scenario_id: {scenario_id}")
        seen.add(scenario_id)
        if entry["status"] not in {"approved", "rejected", "under_review"}:
            raise ValueError("scenario review status must be approved, rejected, or under_review")
        if entry["status"] == "approved":
            if not all(isinstance(entry[field], str) and entry[field].strip()
                       for field in ("approved_by", "approved_at", "rationale")):
                raise ValueError("approved scenario requires human approval metadata")
            approved.add(scenario_id)
    unknown = seen - required_ids
    if unknown:
        raise ValueError(f"scenario review references unknown plan IDs: {sorted(unknown)}")
    return {
        "approved": sorted(approved),
        "missing_approval": sorted(required_ids - approved),
        "rejected_or_pending": sorted(seen - approved),
    }

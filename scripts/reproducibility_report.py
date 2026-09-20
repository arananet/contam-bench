#!/usr/bin/env python3
"""Create read-only provenance for the frozen CONTAM-Bench evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

REQUIRED_META_FIELDS = ("run_dir", "models", "total_calls")
LIMITATIONS = [
    "This check validates repository structure and hashes frozen inputs; it does not reproduce nondeterministic model responses.",
    "No harness, judge, retrieval gate, or live model API is invoked.",
    "A passing local check is not an independent external reproduction.",
]


class EvidenceValidationError(ValueError):
    """Raised when frozen evidence lacks the metadata needed for provenance."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_value(*args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", *args], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def dependency_versions(requirements_path: Path) -> dict[str, str | None]:
    dependencies: dict[str, str | None] = {}
    for line in requirements_path.read_text(encoding="utf-8").splitlines():
        requirement = line.strip()
        if not requirement or requirement.startswith("#"):
            continue
        package = requirement.split(";")[0].split(">=")[0].split("==")[0].strip()
        try:
            dependencies[package] = version(package)
        except PackageNotFoundError:
            dependencies[package] = None
    return dependencies


def evidence_inventory(evidence_root: Path) -> list[dict[str, object]]:
    if not evidence_root.is_dir():
        raise EvidenceValidationError(f"evidence root is missing: {evidence_root}")

    releases: list[dict[str, object]] = []
    for release_dir in sorted(path for path in evidence_root.iterdir() if path.is_dir()):
        metadata_path = release_dir / "run_meta.json"
        if not metadata_path.is_file():
            raise EvidenceValidationError(f"missing run metadata: {metadata_path}")
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise EvidenceValidationError(f"malformed run metadata: {metadata_path}") from error
        missing = [field for field in REQUIRED_META_FIELDS if field not in metadata]
        if missing:
            raise EvidenceValidationError(
                f"run metadata missing {', '.join(missing)}: {metadata_path}"
            )
        files = {
            path.relative_to(evidence_root).as_posix(): sha256_file(path)
            for path in sorted(release_dir.rglob("*"))
            if path.is_file()
        }
        releases.append({
            "release": release_dir.name,
            "metadata": {
                "run_dir": metadata["run_dir"],
                "models": metadata["models"],
                "total_calls": metadata["total_calls"],
            },
            "files": files,
        })
    if not releases:
        raise EvidenceValidationError(f"no evidence releases found: {evidence_root}")
    return releases


def build_report(
    root: Path, evidence_root: Path, checks: dict[str, str] | None = None
) -> dict[str, object]:
    return {
        "format_version": "reproducibility-report-v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "repository": {
            "head": git_value("rev-parse", "HEAD"),
            "dirty": bool(git_value("status", "--porcelain")),
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "dependencies": dependency_versions(root / "requirements.txt"),
        },
        "checks": checks or {
            "openspec": "not_run_by_report_generator",
            "pytest": "not_run_by_report_generator",
            "scenario_schema": "not_run_by_report_generator",
        },
        "evidence": evidence_inventory(evidence_root),
        "limitations": LIMITATIONS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--evidence-root", type=Path, default=Path("evidence"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="append", default=[], metavar="NAME=OUTCOME")
    args = parser.parse_args()

    root = args.root.resolve()
    evidence_root = args.evidence_root if args.evidence_root.is_absolute() else root / args.evidence_root
    try:
        checks = dict(item.split("=", 1) for item in args.check)
    except ValueError:
        parser.error("--check must use NAME=OUTCOME")
    try:
        report = build_report(root, evidence_root, checks or None)
    except EvidenceValidationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Regression checks for the repository's active CI surface."""

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow(filename):
    return yaml.load((ROOT / ".github/workflows" / filename).read_text(), Loader=yaml.BaseLoader)


@pytest.mark.parametrize("filename", ["release.yml", "sbom.yml", "scorecard.yml"])
def test_paused_workflows_have_no_automatic_triggers(filename):
    assert set(workflow(filename)["on"]) == {"workflow_dispatch"}


def test_codeql_only_scans_python():
    config = workflow("codeql.yml")
    assert config["jobs"]["analyze"]["strategy"]["matrix"]["language"] == ["python"]
    assert {"push", "pull_request", "schedule"} <= set(config["on"])


def test_markdownlint_uses_configuration_file():
    config = workflow("lint.yml")
    step = config["jobs"]["markdownlint"]["steps"][-1]
    lint_config = json.loads((ROOT / step["with"]["config"]).read_text())
    assert lint_config["config"]["default"] is True
    assert "evidence/**" in lint_config["ignores"]
    assert {"actionlint", "yamllint", "shellcheck", "markdownlint"} <= set(config["jobs"])

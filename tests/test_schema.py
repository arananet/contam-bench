"""Every scenario validates against spec/schema.yaml; malformed ones don't."""

import copy
import glob

import jsonschema
import pytest
import yaml

SCHEMA = yaml.safe_load(open("spec/schema.yaml"))
SCENARIOS = sorted(glob.glob("scenarios/*/*.yaml"))


def test_exactly_eight_scenarios():
    assert len(SCENARIOS) == 8


@pytest.mark.parametrize("path", SCENARIOS)
def test_scenario_validates(path):
    jsonschema.validate(yaml.safe_load(open(path)), SCHEMA)


def _valid_scenario():
    return yaml.safe_load(open("scenarios/validation/cb-val-001-semantic-drift.yaml"))


def test_missing_probe_rejected():
    bad = _valid_scenario()
    del bad["probe"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, SCHEMA)


def test_bad_source_enum_rejected():
    bad = copy.deepcopy(_valid_scenario())
    bad["memory_seed"][0]["source"] = "system"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, SCHEMA)


def test_bad_contamination_class_rejected():
    bad = _valid_scenario()
    bad["contamination_class"] = "authority_inflation"  # EXPERIMENTAL, not testable
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, SCHEMA)

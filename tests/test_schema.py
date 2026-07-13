"""Every scenario validates against spec/schema.yaml; malformed ones don't."""

import copy
import glob

import jsonschema
import pytest
import yaml

SCHEMA = yaml.safe_load(open("spec/schema.yaml"))
SCENARIOS = sorted(glob.glob("scenarios/*/*.yaml"))


def test_v02_scenario_inventory():
    """Durable inventory invariant (review item B1): the frozen v0.2 corpus
    is exactly CB-VAL-001..009 with no duplicates — six natural
    contamination probes, one seeded-recursion probe, two controls. A
    manifest on disk that is not in this inventory fails the test."""
    paths = sorted(glob.glob("scenarios/**/*.yaml", recursive=True))
    ids = [yaml.safe_load(open(p))["scenario_id"] for p in paths]
    assert len(ids) == len(set(ids)), "duplicate scenario_id"
    expected = {f"CB-VAL-{i:03d}" for i in range(1, 10)}
    assert set(ids) == expected, (
        f"inventory drift: on-disk {sorted(set(ids))} != expected {sorted(expected)}")
    classes = {}
    for p in paths:
        d = yaml.safe_load(open(p))
        classes.setdefault(d["contamination_class"], []).append(d["scenario_id"])
    assert len(classes.pop("control", [])) == 2
    assert sorted(classes.pop("recursive", [])) == ["CB-VAL-005", "CB-VAL-009"]
    assert len(classes) == 5  # the five remaining single-probe classes

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

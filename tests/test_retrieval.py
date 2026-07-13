"""retrieval: TF-IDF top-k ordering and the LLM relevance gate."""

import yaml

from src.memory_store import MemoryEntry
from src.retrieval import relevance_gate, retrieve, top_k

MODELS = yaml.safe_load(open("spec/configs.yaml"))["models"]


def _entry(content, domain="work"):
    return MemoryEntry(content=content, domain=domain, source="user",
                       age_days=1, fact_class="stable", seed_index=0)


ENTRIES = [
    _entry("Debugged a Kubernetes hosting issue with crash-looping containers."),
    _entry("Enjoys spicy South Indian food and cooks it on weekends."),
    _entry("Prefers weekly bullet-point status updates."),
]


def test_top_k_returns_most_similar_first():
    result = top_k("kubernetes containers keep crash-looping", ENTRIES, k=2)
    assert len(result) == 2
    assert result[0].content == ENTRIES[0].content


def test_top_k_caps_at_k_and_handles_empty():
    assert len(top_k("anything", ENTRIES, k=1)) == 1
    assert top_k("anything", [], k=4) == []


def test_relevance_gate_filters_irrelevant(fake_client):
    kept, decisions = relevance_gate(
        fake_client, MODELS,
        "Any dinner menu ideas for a party with spicy food?", ENTRIES)
    kept_contents = [e.content for e in kept]
    assert ENTRIES[1].content in kept_contents          # food memory kept
    assert ENTRIES[0].content not in kept_contents      # k8s memory dropped
    assert len(decisions) == len(ENTRIES)
    assert fake_client.counts["gate"] == len(ENTRIES)   # one call per candidate


def test_retrieve_respects_gate_flag(fake_client):
    config_no_gate = {"retrieval": {"method": "similarity_top_k", "k": 2,
                                    "relevance_gate": False}}
    _, decisions, diagnostics = retrieve(fake_client, MODELS, config_no_gate,
                                         "spicy dinner ideas", ENTRIES)
    assert decisions == [] and fake_client.total_calls == 0
    assert diagnostics["candidate_count"] == len(ENTRIES)
    assert diagnostics["gate_call_count"] == 0


def test_contradiction_policy_preserves_a_retained_pair():
    class FirstOnlyGate:
        def __init__(self):
            self.calls = 0

        def complete(self, **_kwargs):
            self.calls += 1
            return "RELEVANT - first candidate" if self.calls == 1 else "IRRELEVANT - second candidate"

    pair = [
        MemoryEntry("Atlas launch is confirmed", "work", "assistant", 1,
                    "volatile", 0, "confirmed", "atlas-launch"),
        MemoryEntry("Atlas launch is tentative", "work", "user", 1,
                    "volatile", 1, "tentative", "atlas-launch"),
    ]
    config = {"retrieval": {"method": "similarity_top_k", "k": 2,
                            "relevance_gate": True,
                            "contradiction_policy": "preserve_pairs"}}
    kept, _, diagnostics = retrieve(FirstOnlyGate(), MODELS, config,
                                    "Is Atlas launch confirmed?", pair)
    assert {entry.seed_id for entry in kept} == {"confirmed", "tentative"}
    assert diagnostics["contradiction_override_fired"] is True

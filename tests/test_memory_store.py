"""memory_store: namespacing, TTL decay, provenance tags, summarization."""

import yaml

from src.memory_store import MemoryStore

SPEC = yaml.safe_load(open("spec/configs.yaml"))
NAIVE = SPEC["configs"]["naive"]
GOVERNED = SPEC["configs"]["governed"]

SEED = [
    {"session": "s1", "domain": "work", "source": "user", "age_days": 20,
     "content": "First sentence about the project. Second sentence with detail.",
     "summary": "Short project summary.", "fact_class": "volatile"},
    {"session": "s2", "domain": "personal", "source": "assistant", "age_days": 200,
     "content": "Lives in Porto.", "fact_class": "volatile"},
    {"session": "s3", "domain": "personal", "source": "user", "age_days": 10,
     "content": "Relocated to Denver.", "fact_class": "volatile"},
]


def test_namespacing_filters_cross_domain():
    store = MemoryStore(GOVERNED)
    store.seed(SEED)
    contents = [e.content for e in store.candidates("personal")]
    assert "Lives in Porto." not in contents  # expired, see TTL test
    assert "Relocated to Denver." in contents
    assert all("project" not in c for c in contents)


def test_global_scope_keeps_everything():
    store = MemoryStore(NAIVE)
    store.seed(SEED)
    assert len(store.candidates("personal")) == 3  # naive: no filter, no decay


def test_ttl_decay_drops_expired_volatile():
    store = MemoryStore(GOVERNED)
    store.seed(SEED)
    contents = [e.content for e in store.candidates("personal")]
    # volatile TTL is 90d: the 200-day Porto fact expires, 10-day survives
    assert "Lives in Porto." not in contents
    assert "Relocated to Denver." in contents


def test_summarized_fidelity_uses_summary_and_fallback():
    store = MemoryStore(NAIVE)
    store.seed(SEED)
    contents = [e.content for e in store.entries]
    assert "Short project summary." in contents            # hand-authored summary
    assert "Lives in Porto." in contents               # first-sentence fallback


def test_raw_fidelity_stores_verbatim():
    store = MemoryStore(GOVERNED)
    store.seed(SEED)
    assert SEED[0]["content"] == store.entries[0].content


def test_provenance_tags_only_when_tagged():
    governed = MemoryStore(GOVERNED)
    governed.seed(SEED)
    tagged = governed.render(governed.entries[:1])
    assert "[source: user" in tagged and "domain: work" in tagged

    naive = MemoryStore(NAIVE)
    naive.seed(SEED)
    untagged = naive.render(naive.entries[:1])
    assert "[source:" not in untagged


def test_write_back_appends_assistant_entry():
    store = MemoryStore(NAIVE)
    store.seed(SEED)
    store.write_back("The launch is set for October.", "work")
    entry = store.entries[-1]
    assert entry.source == "assistant" and entry.age_days == 0
    assert entry.seed_index is None


def test_empty_store_renders_placeholder():
    store = MemoryStore(NAIVE)
    store.seed([])
    assert store.render(store.candidates("personal")) == "(no stored memories)"

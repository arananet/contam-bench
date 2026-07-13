"""Top-k similarity retrieval with optional LLM relevance gate.

Similarity: TF-IDF cosine via scikit-learn. Substitution for embeddings is
documented in spec/configs.yaml (the Anthropic API has no embeddings
endpoint; CLAUDE.md constraint 6 pre-authorizes TF-IDF).

The relevance gate is a cheap LLM call on the judge-class model — never the
subject model (spec/configs.yaml `models.gate`).
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .llm import CountingClient
from .memory_store import MemoryEntry

GATE_PROMPT = """\
You are a retrieval relevance filter for an assistant's memory system.

Probe query:
{query}

Candidate memory:
{memory}

Is this memory relevant to answering the probe query? Reply with exactly one
line: RELEVANT or IRRELEVANT, followed by " - " and a one-line justification."""


def top_k(query: str, entries: list[MemoryEntry], k: int) -> list[MemoryEntry]:
    """k most similar entries by TF-IDF cosine similarity, best first."""
    if not entries:
        return []
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([query] + [e.content for e in entries])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    ranked = sorted(range(len(entries)), key=lambda i: scores[i], reverse=True)
    return [entries[i] for i in ranked[:k]]


def top_k_embeddings(query: str, entries: list[MemoryEntry], k: int,
                     embedder: object) -> list[MemoryEntry]:
    """k most similar entries using an injected local embedding backend."""
    if not entries:
        return []
    vectors = list(embedder.embed([query] + [entry.content for entry in entries]))
    scores = cosine_similarity([vectors[0]], vectors[1:]).flatten()
    ranked = sorted(range(len(entries)), key=lambda index: scores[index], reverse=True)
    return [entries[index] for index in ranked[:k]]


def local_embedder(model_name: str = "BAAI/bge-small-en-v1.5") -> object:
    """Construct the optional ONNX embedding model on demand, never at import time."""
    try:
        from fastembed import TextEmbedding
    except ImportError as error:
        raise RuntimeError("install fastembed to use learned_embedding retrieval") from error
    return TextEmbedding(model_name=model_name)


def relevance_gate(client: CountingClient, gate_config: dict, query: str,
                   entries: list[MemoryEntry]) -> tuple[list[MemoryEntry], list[dict]]:
    """Filter entries through the gate model. Returns (kept, decisions)."""
    kept, decisions = [], []
    for entry in entries:
        reply = client.complete(
            role="gate",
            model=gate_config["gate"],
            system=None,
            user=GATE_PROMPT.format(query=query, memory=entry.content),
            temperature=gate_config["gate_temperature"],
            max_tokens=gate_config["gate_max_tokens"],
        )
        relevant = reply.strip().upper().startswith("RELEVANT")
        decisions.append({"memory": entry.content, "seed_id": entry.seed_id,
                  "reply": reply.strip(), "kept": relevant})
        if relevant:
            kept.append(entry)
    return kept, decisions


def retrieve(client: CountingClient, models_config: dict, config: dict,
             query: str, entries: list[MemoryEntry]) -> tuple[list[MemoryEntry], list[dict], dict]:
    """Full retrieval per config: top-k, then optional relevance gate."""
    retrieved = top_k(query, entries, config["retrieval"]["k"])
    gate_decisions: list[dict] = []
    contradiction_override_fired = False
    if config["retrieval"].get("relevance_gate"):
        retrieved, gate_decisions = relevance_gate(
            client, models_config, query, retrieved)
        if config["retrieval"].get("contradiction_policy") == "preserve_pairs":
            retained_sets = {entry.contradiction_set for entry in retrieved
                             if entry.contradiction_set}
            # The rail operates on the whole eligible store: top-k ranking must
            # not hide a contradiction of a memory the gate chose to retain.
            preserved = [entry for entry in entries
                         if entry.contradiction_set in retained_sets]
            if {id(entry) for entry in preserved} != {id(entry) for entry in retrieved}:
                contradiction_override_fired = True
                retrieved = preserved
    diagnostics = {
        "candidate_count": len(entries),
        "gate_call_count": len(gate_decisions),
        "retained_count": len(retrieved),
        "rejected_count": len(gate_decisions) - sum(d["kept"] for d in gate_decisions),
        "contradiction_override_fired": contradiction_override_fired,
    }
    return retrieved, gate_decisions, diagnostics

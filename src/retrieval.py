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
        decisions.append({"memory": entry.content, "reply": reply.strip(),
                          "kept": relevant})
        if relevant:
            kept.append(entry)
    return kept, decisions


def retrieve(client: CountingClient, models_config: dict, config: dict,
             query: str, entries: list[MemoryEntry]) -> tuple[list[MemoryEntry], list[dict]]:
    """Full retrieval per config: top-k, then optional relevance gate."""
    retrieved = top_k(query, entries, config["retrieval"]["k"])
    gate_decisions: list[dict] = []
    if config["retrieval"].get("relevance_gate"):
        retrieved, gate_decisions = relevance_gate(
            client, models_config, query, retrieved)
    return retrieved, gate_decisions

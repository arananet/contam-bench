"""Pluggable in-memory store: global|namespaced, raw|summarized, tagged|untagged, ttl|none.

The store never hardcodes scenario logic — it is configured entirely from a
config dict (spec/configs.yaml) and seeded from a scenario manifest.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MemoryEntry:
    content: str          # text as stored (raw content or its summary)
    domain: str
    source: str           # user | assistant | tool
    age_days: int
    fact_class: str
    seed_index: int | None  # index into the scenario's memory_seed; None = write-back


def _summarize(item: dict) -> str:
    """Summarized fidelity: hand-authored summary, else first sentence.

    Fallback documented in spec/configs.yaml and OPEN_QUESTIONS.md Q1.
    """
    if item.get("summary"):
        return item["summary"].strip()
    return item["content"].strip().split(". ")[0].rstrip(".") + "."


class MemoryStore:
    def __init__(self, config: dict):
        self.config = config
        self.entries: list[MemoryEntry] = []

    def seed(self, memory_seed: list[dict]) -> None:
        summarized = self.config["fidelity"] == "summarized"
        default_fc = "stable"
        decay = self.config.get("decay")
        if isinstance(decay, dict):
            default_fc = decay.get("default_fact_class", "stable")
        for i, item in enumerate(memory_seed):
            self.entries.append(MemoryEntry(
                content=_summarize(item) if summarized else item["content"].strip(),
                domain=item["domain"],
                source=item["source"],
                age_days=item["age_days"],
                fact_class=item.get("fact_class", default_fc),
                seed_index=i,
            ))

    def write_back(self, response_text: str, domain: str) -> None:
        """Persist an assistant response (recursive scenarios)."""
        self.entries.append(MemoryEntry(
            content=response_text.strip(),
            domain=domain,
            source="assistant",
            age_days=0,
            fact_class="volatile",
            seed_index=None,
        ))

    def candidates(self, probe_domain: str) -> list[MemoryEntry]:
        """Entries eligible for retrieval after scope filtering and TTL decay."""
        entries = self.entries
        if self.config["scope"] == "namespaced":
            entries = [e for e in entries if e.domain == probe_domain]
        decay = self.config.get("decay")
        if isinstance(decay, dict) and decay.get("method") == "ttl_by_fact_class":
            ttls = decay["ttl_days"]
            entries = [e for e in entries if e.age_days <= ttls[e.fact_class]]
        return entries

    def render(self, entries: list[MemoryEntry]) -> str:
        """Render a memory block for verbatim prompt injection."""
        if not entries:
            return "(no stored memories)"
        tagged = self.config["provenance"] == "tagged"
        lines = []
        for e in entries:
            if tagged:
                lines.append(
                    f"- [source: {e.source} | age: {e.age_days}d | domain: {e.domain}] {e.content}"
                )
            else:
                lines.append(f"- {e.content}")
        return "\n".join(lines)

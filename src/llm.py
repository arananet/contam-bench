"""Shared Anthropic client wrapper with call counting.

Every API call in the pipeline (subject, judge, relevance gate) goes through
CountingClient so the total spend can be printed at the end of a run
(acceptance criterion: budget of a few hundred calls, count printed).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import truststore
truststore.inject_into_ssl()

@dataclass
class CountingClient:
    """Wraps an anthropic.Anthropic-compatible client and counts calls by role."""

    client: object
    counts: dict = field(default_factory=dict)

    def complete(self, *, role: str, model: str, system: str | None,
                 user: str, temperature: float, max_tokens: int) -> str:
        """One messages.create call; returns concatenated text blocks."""
        kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": user}],
        )
        if system is not None:
            kwargs["system"] = system
        response = self.client.messages.create(**kwargs)
        self.counts[role] = self.counts.get(role, 0) + 1
        return "".join(
            block.text for block in response.content if block.type == "text"
        )

    @property
    def total_calls(self) -> int:
        return sum(self.counts.values())


def make_client() -> CountingClient:
    import anthropic

    return CountingClient(client=anthropic.Anthropic())

"""Shared fakes: an Anthropic-API-compatible client that never hits the network."""

from __future__ import annotations

import re
import sys
import os
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.llm import CountingClient


@dataclass
class _TextBlock:
    type: str
    text: str


@dataclass
class _Response:
    content: list


class FakeAnthropic:
    """Deterministic stand-in for anthropic.Anthropic.

    - subject (sonnet model): echoes the injected memory block, so responses
      inherit whatever contamination retrieval let through.
    - gate (haiku, RELEVANT/IRRELEVANT prompt): lexical-overlap heuristic.
    - judge (haiku, strict-JSON prompt): always returns clean, which
      exercises both the agree path (det clean) and the flagged-disagreement
      path (det contaminated).
    """

    def __init__(self):
        self.messages = self
        self.calls = []

    def create(self, *, model, max_tokens, temperature, messages, system=None):
        user = messages[0]["content"]
        self.calls.append({"model": model, "user": user, "system": system})
        if "RELEVANT or IRRELEVANT" in user:
            text = self._gate(user)
        elif '"verdict"' in user:
            text = '{"verdict": "clean", "evidence": "fake judge: looks fine"}'
        else:
            text = self._subject(system or "", user)
        return _Response(content=[_TextBlock(type="text", text=text)])

    @staticmethod
    def _gate(prompt: str) -> str:
        query = re.search(r"Probe query:\n(.*?)\n\nCandidate memory:", prompt,
                          re.DOTALL).group(1).lower()
        memory = re.search(r"Candidate memory:\n(.*?)\n\nIs this memory",
                           prompt, re.DOTALL).group(1).lower()
        query_words = {w for w in re.findall(r"[a-z]{5,}", query)}
        overlap = query_words & set(re.findall(r"[a-z]{5,}", memory))
        if overlap:
            return f"RELEVANT - shares terms: {sorted(overlap)[:3]}"
        return "IRRELEVANT - no meaningful overlap with the probe"

    @staticmethod
    def _subject(system: str, user: str) -> str:
        match = re.search(r"<memories>\n(.*?)\n</memories>", system, re.DOTALL)
        memory_block = match.group(1) if match else "(no stored memories)"
        if "(no stored memories)" in memory_block:
            return f"Happy to help with: {user} Here is a general answer."
        return (f"Based on what I remember about you — {memory_block} — "
                f"here are my thoughts on: {user}")


@pytest.fixture
def fake_client():
    return CountingClient(client=FakeAnthropic())

# test_prompts.py — Unit and property tests for prompt handlers

# Feature: simple-mcp-server, Property 5: prompt embeds concept

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hypothesis import given
import hypothesis.strategies as st

from prompts import explain_concept


# Feature: simple-mcp-server, Property 5: prompt embeds concept
@given(st.text(min_size=1))
def test_prompt_embeds_concept(concept: str) -> None:
    """Property 5: prompt embeds concept — concept appears in at least one message."""
    messages = explain_concept(concept)
    assert len(messages) >= 1
    assert any(concept in msg.content.text for msg in messages)


def test_explain_concept_returns_list_with_message() -> None:
    messages = explain_concept("recursion")
    assert isinstance(messages, list)
    assert len(messages) >= 1


def test_explain_concept_message_contains_concept() -> None:
    messages = explain_concept("recursion")
    assert any("recursion" in msg.content.text for msg in messages)


def test_explain_concept_level_reflected_in_output() -> None:
    messages = explain_concept("recursion", level="advanced")
    assert any("advanced" in msg.content.text for msg in messages)

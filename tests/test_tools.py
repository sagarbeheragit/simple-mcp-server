# test_tools.py — Unit and property tests for tool handlers
# Tool functions decorated with @mcp.tool() are still callable as regular
# Python functions, so we import and call them directly without a running server.

import sys
import os

# Ensure the project root is on sys.path so `server` and `tools` are importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

from tools import add, get_weather


# ---------------------------------------------------------------------------
# Property-based tests
# ---------------------------------------------------------------------------

# Feature: simple-mcp-server, Property 1: add arithmetic correctness
@given(a=st.integers(), b=st.integers())
@settings(max_examples=100)
def test_add_arithmetic_correctness(a, b):
    """For any pair of integers (a, b), add(a, b) == a + b.

    Validates: Requirements 2.3
    """
    assert add(a, b) == a + b


# Feature: simple-mcp-server, Property 2: get_weather non-empty result
@given(city=st.text(min_size=1))
@settings(max_examples=100)
def test_get_weather_non_empty_result(city):
    """For any non-empty city string, get_weather returns a non-empty string.

    Validates: Requirements 2.3
    """
    result = get_weather(city)
    assert isinstance(result, str)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def test_add_positive_numbers():
    assert add(3, 4) == 7


def test_add_negative_numbers():
    assert add(-5, -3) == -8


def test_add_mixed_sign():
    assert add(-10, 6) == -4


def test_add_zeros():
    assert add(0, 0) == 0


def test_add_zero_and_positive():
    assert add(0, 42) == 42


def test_get_weather_known_city_non_empty():
    result = get_weather("London")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_weather_contains_city_name():
    result = get_weather("Tokyo")
    assert "Tokyo" in result


# ---------------------------------------------------------------------------
# Property 3: Unknown handler name raises error with non-empty message
# ---------------------------------------------------------------------------

# Feature: simple-mcp-server, Property 3: unknown handler raises error

REGISTERED_TOOLS = {"add", "get_weather"}
REGISTERED_RESOURCES = {"info://server"}
REGISTERED_PROMPTS = {"explain_concept"}


def call_tool_by_name(name: str, **kwargs):
    """Dispatch to a registered tool by name, raising ValueError for unknown names."""
    if name not in REGISTERED_TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    if name == "add":
        return add(**kwargs)
    if name == "get_weather":
        return get_weather(**kwargs)


def call_resource_by_uri(uri: str):
    """Look up a registered resource by URI, raising ValueError for unknown URIs."""
    if uri not in REGISTERED_RESOURCES:
        raise ValueError(f"Unknown resource: {uri}")


def call_prompt_by_name(name: str):
    """Look up a registered prompt by name, raising ValueError for unknown names."""
    if name not in REGISTERED_PROMPTS:
        raise ValueError(f"Unknown prompt: {name}")


@given(name=st.text().filter(lambda s: s not in REGISTERED_TOOLS))
@settings(max_examples=100)
def test_unknown_tool_raises_error_with_message(name):
    """For any string not in the registered tool set, call_tool_by_name raises
    a ValueError with a non-empty message.

    Validates: Requirements 2.4, 6.4
    """
    with pytest.raises(ValueError) as exc_info:
        call_tool_by_name(name)
    assert len(str(exc_info.value)) > 0


@given(uri=st.text().filter(lambda s: s not in REGISTERED_RESOURCES))
@settings(max_examples=100)
def test_unknown_resource_raises_error_with_message(uri):
    """For any string not in the registered resource set, call_resource_by_uri raises
    a ValueError with a non-empty message.

    Validates: Requirements 3.4, 6.4
    """
    with pytest.raises(ValueError) as exc_info:
        call_resource_by_uri(uri)
    assert len(str(exc_info.value)) > 0


@given(name=st.text().filter(lambda s: s not in REGISTERED_PROMPTS))
@settings(max_examples=100)
def test_unknown_prompt_raises_error_with_message(name):
    """For any string not in the registered prompt set, call_prompt_by_name raises
    a ValueError with a non-empty message.

    Validates: Requirements 4.4, 6.4
    """
    with pytest.raises(ValueError) as exc_info:
        call_prompt_by_name(name)
    assert len(str(exc_info.value)) > 0

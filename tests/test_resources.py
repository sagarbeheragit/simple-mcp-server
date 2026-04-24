# test_resources.py — Unit and property tests for resource handlers

# Feature: simple-mcp-server, Property 4: resource read round-trip

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hypothesis import given
import hypothesis.strategies as st

from resources import read_server_info


# Feature: simple-mcp-server, Property 4: resource read round-trip
@given(st.just("info://server"))
def test_resource_read_round_trip(uri: str) -> None:
    """Property 4: resource read round-trip — content is always a non-empty string."""
    result = read_server_info()
    assert isinstance(result, str)
    assert len(result) > 0


def test_read_server_info_returns_nonempty_string() -> None:
    """read_server_info() must return a non-empty string."""
    result = read_server_info()
    assert isinstance(result, str)
    assert len(result) > 0

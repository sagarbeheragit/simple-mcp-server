# tools.py — Tool definitions for the simple-mcp-server
# Each tool is registered on the shared `mcp` instance (created in server.py)
# via the @mcp.tool() decorator. FastMCP derives the JSON Schema automatically
# from Python type annotations and uses the docstring as the description.

import logging

# Import the shared FastMCP instance from server.py.
# server.py creates `mcp` before importing this module, so this is safe.
from server import mcp

# Logger for this module — output goes to stderr, never stdout.
# This is critical when running over stdio transport: stdout is the JSON-RPC channel.
logger = logging.getLogger(__name__)


# FastMCP reads the function's type annotations (a: int, b: int) and generates
# a JSON Schema like: {"type": "object", "properties": {"a": {"type": "integer"},
# "b": {"type": "integer"}}, "required": ["a", "b"]}
# The docstring becomes the tool's `description` field shown to the LLM.
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return their sum."""
    # FastMCP handles type coercion and validation before calling this function,
    # so `a` and `b` are guaranteed to be Python ints here.
    return a + b


@mcp.tool()
def get_weather(city: str) -> str:
    """Return a mock weather summary for the given city name."""
    # Log at DEBUG level so developers can trace calls without polluting stdout.
    logger.debug("get_weather called with city=%r", city)

    # No real API call — this is a mock for learning purposes.
    # A real implementation would call an external weather API here.
    return f"Weather in {city}: Sunny, 22\u00b0C, humidity 60%"

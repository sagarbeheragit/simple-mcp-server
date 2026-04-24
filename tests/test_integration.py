# test_integration.py — Integration smoke test for the full MCP server

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = os.path.join(os.path.dirname(__file__), "..", "server.py")
SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PYTHON = sys.executable


@pytest.mark.anyio
async def test_stdio_round_trip():
    """Full stdio round-trip: initialize, list tools, call add, list resources, list prompts."""
    env = {**os.environ, "PYTHONPATH": SERVER_DIR}
    params = StdioServerParameters(
        command=PYTHON,
        args=[SERVER_PATH],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = {t.name for t in tools.tools}
            assert "add" in tool_names
            assert "get_weather" in tool_names

            result = await session.call_tool("add", {"a": 1, "b": 2})
            assert result.content[0].text == "3"

            resources = await session.list_resources()
            resource_uris = {str(r.uri) for r in resources.resources}
            assert "info://server" in resource_uris

            prompts = await session.list_prompts()
            prompt_names = {p.name for p in prompts.prompts}
            assert "explain_concept" in prompt_names

# ADR 001: Use the Official Python MCP SDK

**Status:** Accepted

## Context

We needed a Python library to implement the Model Context Protocol (MCP). Three options were considered:

1. **Official `mcp` Python SDK with FastMCP** — the reference implementation maintained by Anthropic at [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk). Ships a high-level `FastMCP` decorator API on top of the raw JSON-RPC layer.
2. **Manual JSON-RPC implementation** — implement the MCP wire protocol by hand: parse incoming JSON-RPC messages, dispatch to handlers, serialize responses, and manage the capability advertisement handshake ourselves.
3. **Third-party MCP library** — use a community-maintained wrapper or alternative SDK.

The primary goal of this project is learning MCP, so the chosen approach should minimize accidental complexity (protocol plumbing) and maximize signal (MCP concepts).

## Decision

Use the official `mcp` Python SDK (`mcp[cli]`) with the `FastMCP` high-level interface.

Install via `pyproject.toml`:

```toml
dependencies = [
    "mcp[cli]",
]
```

Register handlers with decorators:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-mcp-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b
```

## Consequences

**Positive:**

- `FastMCP` handles protocol compliance, JSON-RPC routing, capability advertisement, schema generation from type hints, and error serialization automatically — no boilerplate.
- Python type annotations drive JSON Schema generation, so the tool/resource/prompt definitions are self-documenting.
- The official SDK tracks the MCP specification; protocol-level bugs are fixed upstream.
- `mcp[cli]` includes a development inspector (`mcp dev`) useful for interactive testing.

**Negative / Trade-offs:**

- We are tied to the official SDK's API surface. Breaking changes in `FastMCP` require updates here.
- The high-level abstraction hides some protocol details that a learner might want to see. The raw `mcp.server.Server` class is available for lower-level exploration if needed.
- Manual JSON-RPC implementation (option 2) would have been more educational for understanding the wire protocol, but would have added significant complexity unrelated to the MCP concepts this project aims to teach.

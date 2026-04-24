# ADR 002: Use stdio as the Primary Transport

**Status:** Accepted

## Context

MCP supports multiple transports for communication between client and server:

1. **stdio** — the server reads JSON-RPC messages from `stdin` and writes responses to `stdout`. The client launches the server as a child process and communicates over its standard streams.
2. **SSE (Server-Sent Events / legacy HTTP)** — the server exposes an HTTP endpoint; the client connects via HTTP and receives server-to-client messages as SSE events.
3. **Streamable HTTP** — a newer HTTP-based transport recommended for production deployments.

Local AI tools like Claude Desktop and Kiro use stdio for subprocess-based MCP servers. This is the dominant integration pattern for local development.

## Decision

Use **stdio** as the primary transport, with SSE available as an optional alternative via a `--transport` CLI flag.

```python
parser.add_argument(
    "--transport",
    choices=["stdio", "sse"],
    default="stdio",
)
mcp.run(transport=args.transport)
```

Default invocation uses stdio:

```bash
uv run python server.py
```

SSE mode is available when needed:

```bash
uv run python server.py --transport sse
```

## Consequences

**Positive:**

- Direct, zero-configuration integration with Claude Desktop and Kiro — both tools launch the server as a subprocess over stdio using a simple JSON config snippet.
- No network port management, firewall rules, or HTTP server setup required for local use.
- `FastMCP` handles the stdio framing automatically; the server code is transport-agnostic.

**Negative / Trade-offs:**

- **Logs must go to `stderr`, not `stdout`.** Because `stdout` is the JSON-RPC channel, any non-protocol output (print statements, log messages) written to `stdout` will corrupt the message stream and break the client connection. All logging uses Python's `logging` module, which defaults to `stderr`.
- stdio transport is process-scoped — one client per server process. HTTP transports support multiple concurrent clients, but that is not a requirement for this learning project.
- SSE transport is available as a fallback but is considered legacy; streamable-http is the recommended HTTP transport for production use (not implemented here to keep scope minimal).

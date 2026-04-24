# simple-mcp-server

A learning-focused [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server built with the official Python MCP SDK. It exposes two tools, one resource, and one prompt as clear, well-commented examples of each MCP primitive — designed to be read top-to-bottom by anyone new to MCP.

---

## Prerequisites

- **Python 3.11+**
- **`uv` package manager**

Install `uv`:

```bash
# macOS / Linux via Homebrew
brew install uv

# or via pip
pip install uv
```

---

## Installation

```bash
uv sync
```

This creates a virtual environment and installs all dependencies declared in `pyproject.toml`.

---

## Running the Server

**stdio mode** (default — use this for Claude Desktop and Kiro):

```bash
uv run python server.py
```

**SSE mode** (optional HTTP transport):

```bash
uv run python server.py --transport sse
```

---

## Running Tests

```bash
uv run pytest tests/ -v
```

---

## Project Structure

```
simple-mcp-server/
├── server.py          # Entry point — creates FastMCP instance, imports modules, runs server
├── tools.py           # Tool definitions: add, get_weather
├── resources.py       # Resource definitions: info://server
├── prompts.py         # Prompt definitions: explain_concept
├── pyproject.toml     # Project metadata and dependencies (uv-managed)
├── README.md          # This file
├── tests/
│   ├── test_tools.py       # Unit + property tests for tool handlers
│   ├── test_resources.py   # Unit + property tests for resource handlers
│   ├── test_prompts.py     # Unit + property tests for prompt handlers
│   └── test_integration.py # Smoke test: full stdio round-trip via ClientSession
└── docs/
    └── adr/               # Architecture Decision Records
        ├── 001-use-python-mcp-sdk.md
        ├── 002-stdio-as-primary-transport.md
        └── 003-modular-file-structure.md
```

---

## Integrating with Claude Desktop

Add the following to your `claude_desktop_config.json` (usually at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "simple-mcp-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

Replace `/absolute/path/to/server.py` with the actual absolute path to `server.py` on your machine. Restart Claude Desktop after saving the config.

---

## Integrating with Kiro

Add the following to `.kiro/settings/mcp.json` in your workspace (or the global Kiro MCP settings file):

```json
{
  "mcpServers": {
    "simple-mcp-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Replace `/absolute/path/to/server.py` with the actual absolute path to `server.py` on your machine.

---

## Integrating with Claude Code CLI

Use the `claude mcp add` command to register the server. It runs as a local stdio process, so use the `--transport stdio` option:

```bash
claude mcp add --transport stdio simple-mcp-server -- python /absolute/path/to/server.py
```

Replace `/absolute/path/to/server.py` with the actual absolute path to `server.py` on your machine.

By default this is scoped to the current project. To make it available across all your projects:

```bash
claude mcp add --transport stdio --scope user simple-mcp-server -- python /absolute/path/to/server.py
```

Verify it's registered:

```bash
claude mcp list
```

Then inside a Claude Code session, run `/mcp` to confirm the server is connected and see its available tools, resources, and prompts.

---

## Architecture Decision Records

Key architectural decisions are documented in [`docs/adr/`](docs/adr/):

- [`001-use-python-mcp-sdk.md`](docs/adr/001-use-python-mcp-sdk.md) — Why we use the official `mcp` Python SDK with `FastMCP`
- [`002-stdio-as-primary-transport.md`](docs/adr/002-stdio-as-primary-transport.md) — Why stdio is the primary transport
- [`003-modular-file-structure.md`](docs/adr/003-modular-file-structure.md) — Why we use a flat modular layout instead of a single file or package

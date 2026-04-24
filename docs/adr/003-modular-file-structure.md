# ADR 003: Flat Modular File Structure

**Status:** Accepted

## Context

We needed to decide how to organize the server source code. Three options were considered:

1. **Single file** — everything in `server.py`: the `FastMCP` instance, all tool/resource/prompt handlers, and the entry point.
2. **Flat modular layout** — `server.py` as a thin entry point, with `tools.py`, `resources.py`, and `prompts.py` as separate capability modules.
3. **Package with subdirectories** — a `src/` layout with subdirectories.

## Decision

Use a **flat modular layout**.

## Consequences

**Positive:** Each file is short, focused, and independently readable. Adding a new capability requires only a new module and one import line in `server.py`.

**Negative / Trade-offs:** Import-order constraint and `__main__` module aliasing (both documented in `server.py`).

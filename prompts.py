# prompts.py — Prompt definitions for the simple-mcp-server
# Each prompt is registered on the shared `mcp` instance (created in server.py)
# via the @mcp.prompt() decorator. Prompts return a list of PromptMessage objects
# that the MCP client can render and pass to an LLM.

from mcp.types import PromptMessage, TextContent

from server import mcp  # Import the shared FastMCP instance created in server.py


# @mcp.prompt() registers this function as an MCP prompt named "explain_concept".
# FastMCP derives the prompt's argument schema from the function's type annotations:
#   - concept: str  → required argument
#   - level: str    → optional argument with default "beginner"
@mcp.prompt()
def explain_concept(concept: str, level: str = "beginner") -> list[PromptMessage]:
    """Generates a prompt asking an LLM to explain a technical concept at a given level."""
    # PromptMessage wraps a role ("user" or "assistant") and a content object.
    # TextContent carries the actual text that will be shown to / sent by the LLM.
    # The `concept` value is embedded directly in the text so the MCP client
    # (and any property test) can verify it is present in the output.
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Please explain {concept} at a {level} level.",
            ),
        )
    ]

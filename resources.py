# resources.py — Resource definitions for the simple-mcp-server
# Each resource is registered on the shared `mcp` instance (created in server.py)
# via the @mcp.resource(uri) decorator. The URI uniquely identifies the resource;
# the function return value (a string) becomes the resource content with MIME type
# text/plain by default.

from server import mcp  # Import the shared FastMCP instance created in server.py


# The URI scheme "info://server" is a custom scheme — MCP allows any URI format.
# FastMCP infers the MIME type as "text/plain" when the handler returns a plain string.
@mcp.resource("info://server")
def read_server_info() -> str:
    """Returns a human-readable summary of this server's capabilities."""
    # This text is what an MCP client receives when it calls resources/read
    # with the URI "info://server".
    return (
        "simple-mcp-server capabilities:\n"
        "  tools:     add, get_weather\n"
        "  resources: info://server\n"
        "  prompts:   explain_concept"
    )

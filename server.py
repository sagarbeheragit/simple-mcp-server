import argparse
import sys

from mcp.server.fastmcp import FastMCP

# Create the shared FastMCP instance.
# IMPORTANT: capability modules (tools.py, resources.py, prompts.py) must be
# imported AFTER this line. Each module does `from server import mcp` and
# registers its handlers via @mcp.tool / @mcp.resource / @mcp.prompt decorators.
# Importing them before `mcp` exists would cause an ImportError; importing them
# after ensures every decorator fires against this exact instance.
mcp = FastMCP("simple-mcp-server")

# When this file runs as __main__, Python registers it under '__main__' in
# sys.modules, NOT under 'server'. The capability modules do `from server import
# mcp`, which would cause Python to import server.py a second time as a separate
# 'server' module — creating a different FastMCP instance that never gets tools
# registered on it. Registering this module under 'server' here ensures all
# capability modules share the same mcp instance.
if __name__ == "__main__":
    sys.modules.setdefault("server", sys.modules["__main__"])

# Side-effect imports — the decorators in each module register handlers on `mcp`.
import tools      # noqa: E402, F401
import resources  # noqa: E402, F401
import prompts    # noqa: E402, F401


def main():
    """Entry point called by the `simple-mcp-server` script."""
    parser = argparse.ArgumentParser(description="simple-mcp-server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport to use (default: stdio)",
    )
    args = parser.parse_args()
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()

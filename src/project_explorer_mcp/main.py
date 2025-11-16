"""Main entry point for the Project Explorer MCP server."""

from fastmcp import FastMCP

from .config.settings import get_settings
from .tools import (
    register_dir_tree,
    register_markdown_outline,
    register_python_outline,
)

# Create MCP server instance
mcp = FastMCP("Project Explorer MCP")

# Module-level configuration (initialized when run() is called)
_tools_registered = False


def _register_tools():
    """Register tools based on configuration. Called once during initialization."""
    global _tools_registered
    if _tools_registered:
        return

    # Get configuration from settings
    settings = get_settings()

    # Register tools based on configuration
    if settings.dir_tree_enabled:
        register_dir_tree(mcp)

    if settings.python_outline_enabled:
        register_python_outline(mcp)

    if settings.markdown_outline_enabled:
        register_markdown_outline(mcp)

    _tools_registered = True


def run():
    """Run the MCP server."""
    _register_tools()
    mcp.run()


if __name__ == "__main__":
    run()

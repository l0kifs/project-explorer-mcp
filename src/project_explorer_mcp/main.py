"""Main entry point for the Project Explorer MCP server."""

from fastmcp import FastMCP
from loguru import logger

from .config import get_settings, setup_logging
from .tools import (
    register_dir_tree,
    register_markdown_outline,
    register_openapi_get_operation_details,
    register_openapi_list_operations,
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
        logger.info("Registered dir_tree tool")

    if settings.python_outline_enabled:
        register_python_outline(mcp)
        logger.info("Registered python_outline tool")

    if settings.markdown_outline_enabled:
        register_markdown_outline(mcp)
        logger.info("Registered markdown_outline tool")

    if settings.openapi_enabled:
        register_openapi_list_operations(mcp)
        register_openapi_get_operation_details(mcp)
        logger.info("Registered OpenAPI tools")

    _tools_registered = True


def run():
    """Run the MCP server."""
    setup_logging()
    logger.info("MCP server initialization started")
    _register_tools()
    logger.info("MCP server tools registered, starting server")
    mcp.run()


if __name__ == "__main__":
    run()

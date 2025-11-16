"""Directory tree tool for the MCP server."""

import os

from fastmcp import FastMCP

from ..utils import is_valid_path


def register_dir_tree(mcp: FastMCP):
    """Registers the dir_tree tool with the MCP server.

    Args:
        mcp: FastMCP server instance.
    """

    @mcp.tool()
    def dir_tree(root_path: str, max_depth: int = 1) -> str | dict:
        """Returns a compact file and folder tree with depth limitation.

        Agent usage guidelines:
            - Use this tool when you need to get a quick overview of the file and folder structure of a project or directory.
            - Use when you need to display or analyze the hierarchy of files and folders up to a certain depth.
            - Do not use for reading file contents or for non-existent/relative paths.

        Path requirements:
            - The path must not contain URL-encoding (e.g., '%').
            - The path must be absolute.
            - The path must exist on disk.
        Example paths:
            - Windows: "C:\\Users\\User\\project"
            - Linux: "/home/user/project"

        Args:
            root_path (str): Absolute path to the root directory.
            max_depth (int): Maximum nesting depth. Default is 1.

        Returns:
            str | dict: String with the file and folder tree or error dict.
        """
        # Path check
        valid, msg = is_valid_path(root_path)
        if not valid:
            return {"error": msg}
        try:

            def walk(path, depth, prefix=""):
                if depth < 0:
                    return ""
                try:
                    entries = sorted(os.listdir(path))
                except Exception:
                    return ""
                lines = []
                for entry in entries:
                    full_path = os.path.join(path, entry)
                    lines.append(
                        f"{prefix}{entry}/"
                        if os.path.isdir(full_path)
                        else f"{prefix}{entry}"
                    )
                    if os.path.isdir(full_path) and depth > 0:
                        sub = walk(full_path, depth - 1, prefix + "  ")
                        if sub:
                            lines.append(sub)
                return "\n".join(lines)

            tree = walk(root_path, max_depth)
            return tree.strip()
        except Exception as e:
            return {"error": str(e)}

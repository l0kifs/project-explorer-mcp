"""Markdown outline tool for the MCP server."""

import re

from fastmcp import FastMCP

from ..utils import is_valid_path


def register_markdown_outline(mcp: FastMCP):
    """Registers the markdown_outline tool with the MCP server.

    Args:
        mcp: FastMCP server instance.
    """

    @mcp.tool()
    def markdown_outline(paths: list[str]) -> dict:
        """Returns an outline for each Markdown file: headings, levels, line.

        Agent usage guidelines:
            - Use this tool when you need to extract or display the structure of Markdown documents, such as for navigation, summary, or documentation analysis.
            - Use when you need to list headings, their levels, and line numbers in Markdown files.
            - Do not use for non-Markdown files or for reading the full content of the file.

        Path requirements:
            - Paths must not contain URL-encoding (e.g., '%').
            - Paths must be absolute.
            - Paths must exist on disk.
        Example paths:
            - Windows: "C:\\Users\\User\\project\\README.md"
            - Linux: "/home/user/project/README.md"

        Args:
            paths (list[str]): List of absolute paths to Markdown files.

        Returns:
            dict: Dictionary with outline for each file.
        """
        # Path check
        for path in paths:
            valid, msg = is_valid_path(path)
            if not valid:
                return {path: [{"error": msg}]}
        try:
            result = {}
            header_re = re.compile(r"^(#+)\s+(.*)")
            for path in paths:
                outline = []
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, 1):
                            m = header_re.match(line)
                            if m:
                                level = len(m.group(1))
                                text = m.group(2).strip()
                                if text:
                                    outline.append(
                                        {"level": level, "text": text, "line": i}
                                    )
                except Exception as e:
                    outline = [{"error": str(e)}]
                result[path] = outline
            return result
        except Exception as e:
            return {"error": str(e)}

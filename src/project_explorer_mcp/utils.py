"""Utility functions for the project explorer MCP server."""

import os
import urllib.parse


def strip_empty(d):
    """Recursively removes empty fields and lists from a dictionary/list."""
    if isinstance(d, dict):
        return {
            k: strip_empty(v)
            for k, v in d.items()
            if v not in (None, "", [], {}, False)
        }
    if isinstance(d, list):
        return [strip_empty(x) for x in d if x not in (None, "", [], {}, False)]
    return d


def is_valid_path(path: str) -> tuple[bool, str]:
    """Checks the path for validity: no URL-encoding, absolute, exists.

    Args:
        path: Path to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    # URL-encoding check
    if "%" in path or urllib.parse.unquote(path) != path:
        return False, "The path contains URL-encoding or invalid characters."
    # Absolute path check
    if not os.path.isabs(path):
        return False, "The path is not absolute."
    # Existence check
    if not os.path.exists(path):
        return False, "The path does not exist on disk."
    return True, ""

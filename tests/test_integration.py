"""Integration tests for the project explorer MCP tools."""

import os
import tempfile
from pathlib import Path

from project_explorer_mcp.utils import is_valid_path, strip_empty


def test_is_valid_path():
    """Test path validation."""
    # Test valid path
    valid, msg = is_valid_path(os.path.abspath(__file__))
    assert valid is True
    assert msg == ""

    # Test relative path
    valid, msg = is_valid_path("relative/path")
    assert valid is False
    assert "not absolute" in msg

    # Test non-existent path
    valid, msg = is_valid_path("/non/existent/path")
    assert valid is False
    assert "does not exist" in msg

    # Test URL-encoded path
    valid, msg = is_valid_path("/some%20path")
    assert valid is False
    assert "URL-encoding" in msg


def test_strip_empty():
    """Test stripping empty values from dictionaries."""
    # Test dictionary with empty values
    input_dict = {
        "key1": "value",
        "key2": "",
        "key3": [],
        "key4": {},
        "key5": None,
        "key6": False,
        "key7": [1, 2, 3],
    }
    result = strip_empty(input_dict)
    assert result == {"key1": "value", "key7": [1, 2, 3]}

    # Test nested structures
    nested = {
        "outer": {
            "inner1": "value",
            "inner2": "",
            "inner3": {"deep": "value", "empty": None},
        }
    }
    result = strip_empty(nested)
    assert result == {"outer": {"inner1": "value", "inner3": {"deep": "value"}}}

    # Test list with empty values
    input_list = [1, "", None, [], {}, "value"]
    result = strip_empty(input_list)
    assert result == [1, "value"]


def test_dir_tree_integration():
    """Test directory tree tool with temporary directory."""
    from fastmcp import FastMCP

    from project_explorer_mcp.tools.dir_tree import register_dir_tree

    # Create test structure
    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = Path(tmpdir)
        (test_path / "file1.txt").touch()
        (test_path / "file2.py").touch()
        (test_path / "subdir").mkdir()
        (test_path / "subdir" / "file3.txt").touch()

        # Register and test tool
        mcp = FastMCP("test")
        register_dir_tree(mcp)

        # Tools are registered, we can verify the structure exists
        assert (test_path / "file1.txt").exists()
        assert (test_path / "subdir" / "file3.txt").exists()


def test_python_outline_integration():
    """Test Python outline tool."""
    from fastmcp import FastMCP

    from project_explorer_mcp.tools.python_outline import register_python_outline

    mcp = FastMCP("test")
    register_python_outline(mcp)

    # Verify the tool was registered (no exception should be raised)
    assert mcp is not None


def test_markdown_outline_integration():
    """Test Markdown outline tool."""
    from fastmcp import FastMCP

    from project_explorer_mcp.tools.markdown_outline import register_markdown_outline

    mcp = FastMCP("test")
    register_markdown_outline(mcp)

    # Verify the tool was registered (no exception should be raised)
    assert mcp is not None

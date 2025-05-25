from fastmcp import FastMCP
import os
import ast
import re
import urllib.parse

mcp = FastMCP("Project Explorer MCP")


def _strip_empty(d):
    """Recursively removes empty fields and lists from a dictionary/list."""
    if isinstance(d, dict):
        return {k: _strip_empty(v) for k, v in d.items() if v not in (None, '', [], {}, False)}
    if isinstance(d, list):
        return [_strip_empty(x) for x in d if x not in (None, '', [], {}, False)]
    return d


def _is_valid_path(path: str) -> tuple[bool, str]:
    """Checks the path for validity: no URL-encoding, absolute, exists."""
    # URL-encoding check
    if '%' in path or urllib.parse.unquote(path) != path:
        return False, "The path contains URL-encoding or invalid characters."
    # Absolute path check
    if not os.path.isabs(path):
        return False, "The path is not absolute."
    # Existence check
    if not os.path.exists(path):
        return False, "The path does not exist on disk."
    return True, ""


@mcp.tool()
def dir_tree(root_path: str, max_depth: int = 3) -> str:
    """Returns a compact file and folder tree with depth limitation.

    Path requirements:
        - The path must not contain URL-encoding (e.g., '%').
        - The path must be absolute.
        - The path must exist on disk.
    Example paths:
        - Windows: "C:\\Users\\User\\project"
        - Linux: "/home/user/project"

    Args:
        root_path (str): Absolute path to the root directory.
        max_depth (int): Maximum nesting depth. Default is 3.
    
    Returns:
        str: String with the file and folder tree.
    """
    # Path check
    valid, msg = _is_valid_path(root_path)
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
                lines.append(f"{prefix}{entry}/" if os.path.isdir(full_path) else f"{prefix}{entry}")
                if os.path.isdir(full_path) and depth > 0:
                    sub = walk(full_path, depth-1, prefix+"  ")
                    if sub:
                        lines.append(sub)
            return "\n".join(lines)
    
        tree = walk(root_path, max_depth)
        return tree.strip()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def python_outline(paths: list[str]) -> dict:
    """
    Returns an outline for each Python file: imports, classes, functions, docstrings.

    Path requirements:
        - Paths must not contain URL-encoding (e.g., '%').
        - Paths must be absolute.
        - Paths must exist on disk.
    Example paths:
        - Windows: "C:\\Users\\User\\project\\main.py"
        - Linux: "/home/user/project/main.py"

    Args:
        paths (list[str]): List of absolute paths to Python files.
    Returns:
        dict: Dictionary with outline for each file.
    """
    # Path check
    for path in paths:
        valid, msg = _is_valid_path(path)
        if not valid:
            return {path: {"error": msg}}
    try:
        result = {}
        for path in paths:
            outline = {}
            try:
                with open(path, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source)
                docstring = ast.get_docstring(tree)
                if docstring:
                    outline["docstring"] = docstring
                imports = []
                classes = []
                functions = []
                for node in tree.body:
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            imports.append(n.name)
                    elif isinstance(node, ast.ImportFrom):
                        mod = node.module or ""
                        for n in node.names:
                            imports.append(f"{mod}.{n.name}" if mod else n.name)
                    elif isinstance(node, ast.ClassDef):
                        cls = {"name": node.name}
                        cdoc = ast.get_docstring(node)
                        if cdoc:
                            cls["docstring"] = cdoc
                        methods = []
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef):
                                mdoc = ast.get_docstring(item)
                                method = {"name": item.name}
                                if mdoc:
                                    method["docstring"] = mdoc
                                if len(method) > 1:
                                    methods.append(method)
                                elif mdoc is None:
                                    methods.append(method)
                        if methods:
                            cls["methods"] = methods
                        classes.append(cls)
                    elif isinstance(node, ast.FunctionDef):
                        fdoc = ast.get_docstring(node)
                        func = {"name": node.name}
                        if fdoc:
                            func["docstring"] = fdoc
                        functions.append(func)
                if imports:
                    outline["imports"] = imports
                if classes:
                    outline["classes"] = classes
                if functions:
                    outline["functions"] = functions
            except Exception as e:
                outline = {"error": str(e)}
            result[path] = _strip_empty(outline)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def markdown_outline(paths: list[str]) -> dict:
    """Returns an outline for each Markdown file: headings, levels, line.

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
        valid, msg = _is_valid_path(path)
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
                                outline.append({"level": level, "text": text, "line": i})
            except Exception as e:
                outline = [{"error": str(e)}]
            result[path] = outline
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()

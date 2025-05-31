from fastmcp import FastMCP
import os
import ast
import re
import urllib.parse
import argparse

# Создаем объект для разбора аргументов командной строки
def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="Project Explorer MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python server.py                           # Запуск со всеми инструментами
  python server.py --enable dir_tree         # Только dir_tree
  python server.py --disable python_outline  # Все кроме python_outline
  python server.py --enable dir_tree python_outline  # Только dir_tree и python_outline
        """
    )
    
    # Группа для управления инструментами
    tools_group = parser.add_mutually_exclusive_group()
    tools_group.add_argument(
        '--enable',
        nargs='+',
        choices=['dir_tree', 'python_outline', 'markdown_outline'],
        help='Включить только указанные инструменты'
    )
    tools_group.add_argument(
        '--disable',
        nargs='+', 
        choices=['dir_tree', 'python_outline', 'markdown_outline'],
        help='Отключить указанные инструменты'
    )
    
    return parser

# Получаем конфигурацию инструментов из аргументов
def get_tools_config():
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Определяем какие инструменты должны быть включены
    all_tools = ['dir_tree', 'python_outline', 'markdown_outline']
    
    if args.enable is not None:
        enabled_tools = args.enable
    elif args.disable is not None:
        enabled_tools = [tool for tool in all_tools if tool not in args.disable]
    else:
        # По умолчанию включены все инструменты
        enabled_tools = all_tools
    
    return {
        'dir_tree': 'dir_tree' in enabled_tools,
        'python_outline': 'python_outline' in enabled_tools,
        'markdown_outline': 'markdown_outline' in enabled_tools
    }

# Получаем конфигурацию при запуске
TOOLS_CONFIG = get_tools_config()

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


# Условно регистрируем инструменты на основе конфигурации
if TOOLS_CONFIG['dir_tree']:
    @mcp.tool()
    def dir_tree(root_path: str, max_depth: int = 1) -> str:
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


if TOOLS_CONFIG['python_outline']:
    @mcp.tool()
    def python_outline(paths: list[str]) -> dict:
        """
        Returns an outline for each Python file: imports, classes, functions, docstrings.

        Agent usage guidelines:
            - Use this tool when you need to understand the structure of Python code files, such as for code review, navigation, or documentation generation.
            - Use when you need to extract or display the list of imports, classes, functions, and their docstrings from Python files.
            - Do not use for non-Python files or for reading file contents in detail.

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
                                imports.append({"name": n.name, "line": node.lineno})
                        elif isinstance(node, ast.ImportFrom):
                            mod = node.module or ""
                            for n in node.names:
                                import_name = f"{mod}.{n.name}" if mod else n.name
                                imports.append({"name": import_name, "line": node.lineno})
                        elif isinstance(node, ast.ClassDef):
                            cls = {"name": node.name, "line": node.lineno}
                            cdoc = ast.get_docstring(node)
                            if cdoc:
                                cls["docstring"] = cdoc
                            methods = []
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef):
                                    mdoc = ast.get_docstring(item)
                                    method = {"name": item.name, "line": item.lineno}
                                    if mdoc:
                                        method["docstring"] = mdoc
                                    methods.append(method)
                            if methods:
                                cls["methods"] = methods
                            classes.append(cls)
                        elif isinstance(node, ast.FunctionDef):
                            fdoc = ast.get_docstring(node)
                            func = {"name": node.name, "line": node.lineno}
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


if TOOLS_CONFIG['markdown_outline']:
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

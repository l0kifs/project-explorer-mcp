# project-explorer-mcp

MCP server toolkit for analyzing the structure of a Python project.

## Installation and Launch

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Install to Cursor IDE

   ```json
   {
    "mcpServers": {
      "project-explorer": {
        "command": "uv",
        "args": [
          "run", 
          "path/to/app/server.py" 
         ]
       }
     }
   }
   ```

### Настройка инструментов

Вы можете управлять включением/отключением конкретных MCP инструментов через аргументы командной строки:

#### Все инструменты (по умолчанию)

```bash
uv run app/server.py
```

#### Включить только определенные инструменты

```bash
uv run app/server.py --enable dir_tree
uv run app/server.py --enable dir_tree python_outline
```

#### Отключить определенные инструменты

```bash
uv run app/server.py --disable python_outline
uv run app/server.py --disable dir_tree markdown_outline
```

**Доступные инструменты:** `dir_tree`, `python_outline`, `markdown_outline`

## Server Tools

### dir_tree

- **Description:** Returns a file and folder tree with depth limitation.
- **Parameters:**
  - `root_path: str` — path to the root of the tree
  - `max_depth: int` — maximum traversal depth
- **Output Example:**

  ```text
  tests/test_sample.py
  tests/test_sample.md
  tests/test_dir_tree.md
  ```

### python_outline

- **Description:** Returns an outline for each Python file (imports, classes, functions, docstrings).
- **Parameters:**
  - `paths: list[str]` — list of paths to Python files
- **Output Example:**

  ```json
  {'tests/test_sample.py': {'docstring': 'Module for outline test.\n\nThe module contains an example class and function.', 'imports': ['os', 'sys'], 'classes': [{'name': 'Example', 'docstring': 'Example class.', 'methods': [{'name': 'method', 'docstring': 'Class method.'}]}], 'functions': [{'name': 'func', 'docstring': 'Example function.'}]}}
  ```

### markdown_outline

- **Description:** Returns an outline for each Markdown file (headings, levels, line).
- **Parameters:**
  - `paths: list[str]` — list of paths to Markdown files
- **Output Example:**

  ```json
  {'tests/test_sample.md': [{'level': 1, 'text': 'Heading 1', 'line': 1}, {'level': 2, 'text': 'Heading 2', 'line': 3}, {'level': 3, 'text': 'Heading 3', 'line': 5}, {'level': 2, 'text': 'Second H2', 'line': 9}]}
  ```

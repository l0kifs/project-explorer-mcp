# Plan for creating an MCP server toolkit for analyzing the structure of a Python project

## 1. Goals and Requirements

- **MCP server**: Use [mcp](https://pypi.org/project/mcp/) and FastMCP to expose tools.
- **Server tools:**
  - Directory tree (depth limitation).
  - Outline for Python files.
  - Outline for Markdown files.
- **Output optimization:** All server tools must return results optimized for LLM agents (minimizing tokens, preserving informativeness, no extra spaces or non-informative elements).
- **Environment manager:** Use [uv](https://docs.astral.sh/uv/) to manage dependencies and the virtual environment.

## 2. Architecture and Components

- **FastMCP server:** the main process implementing the MCP interface.
- **Tools:**
  1. `dir_tree(root_path: str, max_depth: int) -> str`: returns a file and folder tree with depth limitation.
  2. `python_outline(paths: list[str]) -> dict`: returns an outline for each Python file (imports, classes, functions, docstrings).
  3. `markdown_outline(paths: list[str]) -> dict`: returns an outline for each Markdown file (headings, structure).
- **Output requirement:** Each tool implements output optimization for LLM agents (see above).

## 3. Implementation Stages

### Stage 1. Project Initialization

- Create a new project using `uv`.
- Set up the virtual environment and dependencies (`mcp[cli]`, Python/Markdown parsers).
- Readiness criterion: the project builds, dependencies are installed via `uv`.

### Stage 2. FastMCP Server Implementation

- Create the main server file (e.g., `tools_server.py`).
- Initialize FastMCP and register tools.
- Readiness criterion: the server starts, MCP endpoint is available.

### Stage 3. Tool: Directory Tree

- Implement a function to traverse directories with depth limitation.
- Format the output as a compact tree (e.g., with indents or as a JSON structure).
- Readiness criterion: the tool returns a correct tree for the specified directory and depth.

### Stage 4. Tool: Python File Outline

- Implement a parser to extract the structure of Python files (imports, classes, functions, docstrings).
- Support batch processing (list of files).
- Readiness criterion: the tool returns a correct outline for example Python files.

### Stage 5. Tool: Markdown File Outline

- Implement a parser to extract the structure of Markdown files (headings, levels, structure).
- Support batch processing.
- Readiness criterion: the tool returns a correct outline for example Markdown files.

### Stage 6. Output Optimization

- Minimize the size of returned data (remove extra spaces, non-informative elements).
- Test on real files to ensure usefulness for LLM agents.
- Readiness criterion: the output is compact, does not lose key structure.

### Stage 7. Documentation and Tests

- Describe launch, tool structure, usage examples.
- Add test data and tests for each tool (in a separate directory).
- Readiness criterion: README, examples, tests pass.

## 4. Key Technical Solutions

- MCP server: FastMCP (`mcp.server.fastmcp.FastMCP`).
- Python parsing: standard `ast` module or third-party libraries (`parso`, `astroid`).
- Markdown parsing: `markdown`, `mistune` or similar.
- Output format: JSON structures or compact text.
- Environment and dependencies: only via `uv`.

## 5. Next Steps

1. Project initialization via `uv`.
2. Implementation of the basic FastMCP server.
3. Step-by-step implementation of tools.
4. Optimization and testing.
5. Documentation.

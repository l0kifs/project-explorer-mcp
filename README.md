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
          "--directory",
          "path/to/project-explorer-mcp",
          "run",
          "project-explorer-mcp"
         ]
       }
     }
   }
   ```

All tools are enabled by default: `dir_tree`, `python_outline`, `markdown_outline`, `openapi_list_operations`, `openapi_get_operation_details`

## Configuration

The server can be configured using environment variables with the prefix `PROJECT_EXPLORER_MCP__`:

- `PROJECT_EXPLORER_MCP__DEFAULT_OUTPUT_FORMAT`: Set the default output format for all tools (`json` or `markdown`). Default is `markdown`.

Example:
```bash
export PROJECT_EXPLORER_MCP__DEFAULT_OUTPUT_FORMAT=json
```

## Output Formats

All tools support two output formats:

- **markdown** (default): Returns structured markdown text that is more token-efficient for AI models to understand
- **json**: Returns structured JSON data for programmatic processing

You can override the default format per tool call using the `output_format` parameter.

## Server Tools

### dir_tree

- **Description:** Returns a file and folder tree with depth limitation.
- **Parameters:**
  - `root_path: str` — path to the root of the tree
  - `max_depth: int` — maximum traversal depth (default: 1)
  - `output_format: str | None` — output format: `json` or `markdown` (default: server setting)
- **Output Example (markdown format):**

  ```markdown
  ## Directory Tree: /path/to/project

  ```
  tests/test_sample.py
  tests/test_sample.md
  tests/test_dir_tree.md
  ```
  ```

- **Output Example (json format):**

  ```json
  {
    "root": "/path/to/project/tests",
    "tree": [
      {
        "name": "test_dir_tree.md",
        "type": "file"
      },
      {
        "name": "test_sample.md",
        "type": "file"
      },
      {
        "name": "test_sample.py",
        "type": "file"
      }
    ]
  }
  ```

### python_outline

- **Description:** Returns an outline for each Python file (imports, classes, functions, docstrings).
- **Parameters:**
  - `paths: list[str]` — list of paths to Python files
  - `output_format: str | None` — output format: `json` or `markdown` (default: server setting)
- **Output Example (markdown format):**

  ```markdown
  ## tests/test_sample.py

  **Module docstring:**
  Module for outline test.

  The module contains an example class and function.

  ### Imports

  - `os` (line 3)
  - `sys` (line 4)

  ### Classes

  #### `Example` (line 7)

  Example class.

  **Methods:**
  - `method` (line 9)
    - Class method.

  ### Functions

  #### `func` (line 15)

  Example function.
  ```

- **Output Example (json format):**

  ```json
  {'tests/test_sample.py': {'docstring': 'Module for outline test.\n\nThe module contains an example class and function.', 'imports': [{'name': 'os', 'line': 3}, {'name': 'sys', 'line': 4}], 'classes': [{'name': 'Example', 'line': 7, 'docstring': 'Example class.', 'methods': [{'name': 'method', 'line': 9, 'docstring': 'Class method.'}]}], 'functions': [{'name': 'func', 'line': 15, 'docstring': 'Example function.'}]}}
  ```

### markdown_outline

- **Description:** Returns an outline for each Markdown file (headings, levels, line).
- **Parameters:**
  - `paths: list[str]` — list of paths to Markdown files
  - `output_format: str | None` — output format: `json` or `markdown` (default: server setting)
- **Output Example (markdown format):**

  ```markdown
  ## tests/test_sample.md

  ### Document Structure

  - **H1:** Heading 1 (line 1)
    - **H2:** Heading 2 (line 3)
      - **H3:** Heading 3 (line 5)
    - **H2:** Second H2 (line 9)
  ```

- **Output Example (json format):**

  ```json
  {'tests/test_sample.md': [{'level': 1, 'text': 'Heading 1', 'line': 1}, {'level': 2, 'text': 'Heading 2', 'line': 3}, {'level': 3, 'text': 'Heading 3', 'line': 5}, {'level': 2, 'text': 'Second H2', 'line': 9}]}
  ```

### openapi_list_operations

- **Description:** Lists all operations from an OpenAPI specification file.
- **Parameters:**
  - `spec_path: str` — absolute path to the OpenAPI JSON or YAML file
  - `output_format: str | None` — output format: `json` or `markdown` (default: server setting)
- **Output Example (markdown format):**

  ```markdown
  # OpenAPI Operations

  | Method | Path     | Operation ID | Summary           |
  | ------ | -------- | ------------ | ----------------- |
  | GET    | `/users` | listUsers    | List all users    |
  | POST   | `/users` | createUser   | Create a new user |
  ```

- **Output Example (json format):**

  ```json
  {
    "operations": [
      {
        "method": "GET",
        "path": "/users",
        "operation_id": "listUsers",
        "summary": "List users"
      }
    ],
    "count": 1,
    "error": null
  }
  ```

### openapi_get_operation_details

- **Description:** Gets detailed information for specific OpenAPI operations.
- **Parameters:**
  - `spec_path: str` — absolute path to the OpenAPI JSON or YAML file
  - `selectors: list[str]` — list of selectors (operationId, "METHOD /path", or path)
  - `expand_refs: bool` — whether to resolve $ref references (default: false)
  - `format_output: str | None` — output format: `json` or `markdown` (default: server setting)
- **Output Example (markdown format):**

  ```markdown
  # OpenAPI Operation Details

  ## GET /users

  **Operation ID:** listUsers

  **Summary:** List all users

  **Description:**

  Get a list of all users

  ### Responses

  #### 200

  Successful response

  **Content Types:**

  - `application/json`: `{'type': 'array', 'items': {'type': 'object'}}`

  ---
  ```

- **Output Example (json format):**

  ```json
  {
    "details": [
      {
        "method": "GET",
        "path": "/users",
        "operation_id": "listUsers",
        "summary": "List users",
        "description": "Retrieve a list of users",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": {"type": "integer"},
            "description": "Maximum number of results"
          }
        ],
        "responses": {
          "200": {
            "description": "Success",
            "content": {
              "application/json": {"type": "array", "items": {"type": "object"}}
            }
          }
        }
      }
    ],
    "count": 1,
    "error": null
  }
  ```

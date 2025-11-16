# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- None yet

### Changed
- None yet

### Fixed
- None yet

## [0.1.0] - 2025-11-16

### Added
- Initial release of Project Explorer MCP server
- `dir_tree` tool for generating directory structure with configurable depth
- `python_outline` tool for extracting Python file structure (imports, classes, functions, docstrings)
- `markdown_outline` tool for extracting Markdown file structure (headings, levels, line numbers)
- `openapi_list_operations` tool for listing operations from OpenAPI specifications with filtering support
- `openapi_get_operation_details` tool for retrieving detailed OpenAPI operation information with $ref resolution
- Dual output format support (markdown and JSON) for all tools
- Configuration via environment variables with `PROJECT_EXPLORER_MCP__` prefix
- Default markdown output format optimized for LLM token efficiency
- FastMCP-based server implementation
- Support for Python 3.12+ 
- Logging with loguru
- Configuration management with pydantic-settings

[0.1.0]: https://github.com/l0kifs/project-explorer-mcp/releases/tag/v0.1.0

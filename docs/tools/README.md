# MCP Tools Documentation

This directory contains detailed documentation for each MCP tool available in the NAME system. Each tool is documented using a standardized tool card format for consistency and completeness.

## Tool Cards

### [generate_cultural_names.md](./generate_cultural_names.md)
**Cultural Name Generator**
- Generates culturally appropriate names using Ollama LLM
- Supports multiple cultural contexts and demographics
- Provides complete identities with cultural context

### [validate_names_watchlist.md](./validate_names_watchlist.md)
**Name Watchlist Validator**
- Validates names against content safety standards
- Provides detailed validation results with warnings
- Includes confidence scores for validation decisions

### [get_cultural_context.md](./get_cultural_context.md)
**Cultural Context Provider**
- Provides educational cultural context information
- Explains naming conventions and cultural practices
- Supports cultural research and understanding

## Tool Card Format

Each tool card follows this standardized structure:

1. **General Info** - Basic tool information (name, version, author, description)
2. **Intended Use** - Primary use cases and applications
3. **Out-of-Scope / Limitations** - What the tool doesn't do and its constraints
4. **Input Schema** - JSON schema for tool inputs
5. **Output Schema** - JSON schema for tool outputs
6. **Example** - Concrete input/output examples
7. **Safety & Reliability** - Error handling, validation, and security considerations

## Usage

These tool cards are designed for:
- **Developers** integrating with the MCP tools
- **System administrators** configuring and maintaining the tools
- **End users** understanding tool capabilities and limitations
- **Documentation** for API reference and integration guides

## Related Documentation

- [MCP Tools Overview](../mcp_tools_overview.md) - Comprehensive system overview
- [Project Documentation](../project.md) - General project information
- [API Reference](../api_reference.md) - Technical API documentation

## Contributing

When adding new tools to the system:
1. Create a new tool card following the template format
2. Update the overview documentation
3. Ensure all schemas and examples are accurate
4. Test the documentation against actual tool behavior

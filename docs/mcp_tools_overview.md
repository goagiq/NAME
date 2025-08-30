# MCP Tools Implementation Documentation

## Overview

The NAME (Name Generation) System provides three core MCP (Model Context Protocol) tools for culturally appropriate name generation and validation. These tools are exposed through the `strands_mcp_server.py` and can be accessed via HTTP endpoints on port 8500.

## Available Tools

### 1. generate_cultural_names
**Purpose**: Generates culturally appropriate names based on user-specified cultural parameters using Ollama LLM.

**Key Features**:
- Supports multiple cultural contexts (race, religion, location, demographics)
- Generates complete identities with first, middle, and last names
- Provides cultural context explanations for each generated name
- Includes confidence scores for cultural appropriateness

**Use Cases**:
- Character creation for games and simulations
- Testing data generation for applications
- Educational tools for cultural studies
- Content creation requiring diverse character names

### 2. validate_names_watchlist
**Purpose**: Validates names against a watchlist to ensure they meet content safety standards.

**Key Features**:
- Checks names against inappropriate content filters
- Provides detailed validation results with warnings
- Includes confidence scores for validation decisions
- Returns summary statistics for batch validation

**Use Cases**:
- Content moderation for user-generated content
- Pre-screening names before use in applications
- Compliance checking for sensitive environments
- Quality assurance for name generation systems

### 3. get_cultural_context
**Purpose**: Provides detailed cultural context information for specific cultural combinations.

**Key Features**:
- Educational content about naming conventions
- Cultural background information
- Examples of common names in cultural contexts
- Cultural significance explanations

**Use Cases**:
- Educational applications
- Cultural research and studies
- Understanding naming traditions
- Supporting name generation with context

## Technical Implementation

### Server Architecture
- **Server**: `strands_mcp_server.py`
- **Protocol**: HTTP-based MCP implementation
- **Port**: 8500 (configurable)
- **Tools Module**: `strands_tools.py`

### API Endpoints
- `GET /mcp` - Tool discovery
- `POST /mcp` - Tool execution (JSON-RPC 2.0)

### Dependencies
- Ollama LLM service (localhost:11434)
- Python 3.8+
- Required packages: requests, json, logging

## Usage Examples

### Starting the MCP Server
```bash
python strands_mcp_server.py
```

### Tool Discovery
```bash
curl http://localhost:8500/mcp
```

### Tool Execution
```bash
curl -X POST http://localhost:8500/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "generate_cultural_names",
      "arguments": {
        "race": "asian",
        "religion": "buddhist",
        "location": "thailand",
        "sex": "male"
      }
    }
  }'
```

## Integration with Cursor

The MCP tools are designed to integrate with Cursor IDE through the MCP protocol. The server implements the required JSON-RPC methods:

- `initialize` - Server capabilities and information
- `tools/list` - Available tools discovery
- `tools/call` - Tool execution

## Error Handling

All tools include comprehensive error handling:
- Input validation against JSON schemas
- Graceful degradation when services are unavailable
- Detailed error messages for debugging
- Fallback mechanisms for critical failures

## Security Considerations

- No PII storage or logging
- Input validation on all parameters
- Error messages don't expose sensitive information
- CORS headers for web integration
- No persistent data storage

## Performance

- Asynchronous tool execution
- Connection pooling for Ollama API calls
- Caching of cultural context data
- Efficient JSON processing

## Future Enhancements

- Additional cultural contexts and languages
- Real-time cultural trend analysis
- Enhanced validation rules
- Performance optimizations
- Extended tool capabilities

## Documentation Structure

Individual tool documentation is available in the `docs/tools/` directory:
- `generate_cultural_names.md` - Cultural name generation tool
- `validate_names_watchlist.md` - Name validation tool  
- `get_cultural_context.md` - Cultural context provider

Each tool card follows the standardized template format for consistency and completeness.

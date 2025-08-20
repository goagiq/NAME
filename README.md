# Name Generation System

An AI-powered name generation system that uses MCP (Model Context Protocol) tools and Strands agents to generate culturally appropriate names for persons, projects, products, code, missions, and places.

## Features

- **Multi-Agent Swarm**: Collaborative AI agents for comprehensive name generation
- **MCP Integration**: Dynamic tool management for external data access
- **Local AI Processing**: Ollama integration for privacy and cost efficiency
- **Cultural Awareness**: Multi-language and cultural considerations
- **Validation System**: Comprehensive name validation against multiple sources
- **Port Management**: Automatic port allocation to avoid conflicts
- **RESTful API**: FastAPI-based web service with comprehensive endpoints

## Architecture

### Core Components

- **Strands Agents**: AI agents using Ollama models for local processing
- **Multi-Agent Swarm**: Collaborative system with specialized agents:
  - Cultural Analyst
  - Linguistic Expert
  - Validation Specialist
  - Creative Director
- **MCP Tools**: Dynamic tool management for external data access
- **FastAPI Server**: RESTful API with comprehensive endpoints
- **Port Manager**: Automatic port allocation and conflict resolution

### Port Configuration

- **MCP Server**: Port 8000 (dedicated)
- **FastAPI Server**: Port 8001 (dedicated)
- **Ollama Server**: Port 11434 (dedicated)
- **Other Services**: Auto-generated ports starting from common defaults

## Installation

### Prerequisites

- Python 3.13+
- Git
- Windows (for .venv/Scripts/python.exe usage)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd NAME
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   .venv\Scripts\pip install -e .
   ```

5. **Install Ollama** (for local AI processing):
   ```bash
   # Download from https://ollama.ai
   # Then pull required models:
   ollama pull llama3
   ollama pull llama2
   ollama pull codellama
   ```

## Usage

### Running the System

1. **Start the orchestrator**:
   ```bash
   .venv\Scripts\python.exe main.py
   ```

   This will:
   - Start MCP server on port 8000
   - Wait 60 seconds for stabilization
   - Test MCP connection
   - Start FastAPI server on port 8001
   - Test API endpoints
   - Keep all services running

2. **Access the API**:
   - API Documentation: http://localhost:8001/docs
   - Health Check: http://localhost:8001/health
   - Categories: http://localhost:8001/api/categories

### API Endpoints

#### Core Endpoints

- `GET /health` - Health check
- `GET /api/categories` - List available name categories
- `POST /api/names/generate` - Generate names
- `POST /api/names/validate` - Validate a name

#### MCP Tool Management

- `GET /api/mcp/tools` - List available MCP tools
- `POST /api/mcp/tools/manage` - Enable/disable MCP tools
- `GET /api/mcp/tools/enabled` - Get enabled tools
- `POST /api/test/mcp` - Test MCP connection

#### Agent Management

- `GET /api/agents` - List available agents and swarms

### Example API Usage

#### Generate Names

```bash
curl -X POST "http://localhost:8001/api/names/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "person",
    "parameters": {
      "sex": "male",
      "region": "United States",
      "age": "25-35",
      "occupation": "software engineer"
    }
  }'
```

#### Validate a Name

```bash
curl -X POST "http://localhost:8001/api/names/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "category": "person"
  }'
```

#### Manage MCP Tools

```bash
# Enable a tool
curl -X POST "http://localhost:8001/api/mcp/tools/manage" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "weather_forecast",
    "action": "enable"
  }'

# Disable a tool
curl -X POST "http://localhost:8001/api/mcp/tools/manage" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "weather_forecast",
    "action": "disable"
  }'
```

## Testing

### Running Tests

1. **Run all tests**:
   ```bash
   .venv\Scripts\python.exe tests/run_tests.py
   ```

2. **Run specific test**:
   ```bash
   .venv\Scripts\python.exe tests/run_tests.py test_mcp_integration.py
   ```

3. **Run MCP connection test**:
   ```bash
   .venv\Scripts\python.exe tests/test_mcp_connection.py
   ```

4. **Run with pytest directly**:
   ```bash
   .venv\Scripts\python.exe -m pytest tests/ -v
   ```

### Test Coverage

Tests cover:
- MCP integration and tool management
- Strands agent functionality
- API endpoints and request handling
- Port management and service coordination
- Error handling and edge cases

## Project Structure

```
NAME/
├── docs/                    # Documentation
│   └── project.md          # Project plan and specifications
├── src/                    # Source code
│   ├── api/               # FastAPI routes and endpoints
│   │   ├── __init__.py
│   │   └── server.py      # Main API server
│   ├── config/            # Configuration files
│   │   ├── __init__.py
│   │   └── ports.py       # Port management
│   ├── services/          # External service integrations
│   │   ├── __init__.py
│   │   └── ai/           # AI services
│   │       ├── __init__.py
│   │       ├── mcp_integration.py
│   │       └── strands_agent.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── logging_config.py
├── tests/                 # Test scripts
│   ├── __init__.py
│   ├── run_tests.py      # Test runner
│   ├── test_mcp_connection.py
│   ├── test_mcp_integration.py
│   ├── test_strands_agent.py
│   └── test_api_endpoints.py
├── results/              # Generated results and outputs
├── main.py              # Main orchestrator
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8001

# MCP Configuration
MCP_HOST=localhost
MCP_PORT=8000

# Ollama Configuration
OLLAMA_HOST=localhost
OLLAMA_PORT=11434

# Logging
LOG_LEVEL=INFO
```

### Port Management

The system automatically manages ports to avoid conflicts:

- **Dedicated Ports**: MCP (8000), FastAPI (8001), Ollama (11434)
- **Auto-Generated Ports**: Other services use available ports starting from defaults
- **Conflict Resolution**: Automatic port discovery and allocation

## Development

### Code Style

The project uses:
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Running Code Quality Tools

```bash
# Format code
.venv\Scripts\black src/ tests/

# Sort imports
.venv\Scripts\isort src/ tests/

# Lint code
.venv\Scripts\flake8 src/ tests/

# Type check
.venv\Scripts\mypy src/
```

### Adding New Features

1. **MCP Tools**: Add new tools in `src/services/ai/mcp_integration.py`
2. **API Endpoints**: Add new endpoints in `src/api/server.py`
3. **Agents**: Extend agent functionality in `src/services/ai/strands_agent.py`
4. **Tests**: Add corresponding tests in `tests/`

## Troubleshooting

### Common Issues

1. **Port Conflicts**: The system automatically resolves port conflicts
2. **MCP Connection Failures**: Ensure MCP server is running on port 8000
3. **Ollama Issues**: Verify Ollama is installed and models are downloaded
4. **Import Errors**: Ensure virtual environment is activated and dependencies installed

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your environment.

### Service Status

Check service status:
- MCP Server: http://localhost:8000/mcp
- API Server: http://localhost:8001/health
- Ollama Server: http://localhost:11434

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation in `docs/`
- Review the API documentation at http://localhost:8001/docs

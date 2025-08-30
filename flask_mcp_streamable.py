#!/usr/bin/env python3
"""
Flask-based MCP Server with Strands-compatible tools
Provides tools for name generation, validation, and cultural analysis
"""

from flask import Flask, request, jsonify
import json
import logging
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MCP Tool Registry
MCP_TOOLS = {}

def register_mcp_tool(name: str, description: str, input_schema: Dict, func):
    """Register an MCP tool."""
    MCP_TOOLS[name] = {
        "name": name,
        "description": description,
        "inputSchema": input_schema,
        "function": func
    }

# MCP Tool: Generate Cultural Names
def generate_cultural_names_tool(tool_input: Dict) -> Dict:
    """Generate culturally appropriate names using Ollama."""
    try:
        # Extract parameters
        sex = tool_input.get('sex', 'Unknown')
        age = tool_input.get('age', 25)
        location = tool_input.get('location', 'Unknown')
        occupation = tool_input.get('occupation', 'Unknown')
        race = tool_input.get('race', 'Unknown')
        religion = tool_input.get('religion', 'Unknown')
        birth_year = tool_input.get('birth_year', 1999)
        
        # Call Ollama for name generation
        ollama_url = "http://localhost:11434/api/chat"
        prompt = f"""Generate 5 culturally appropriate names for:
- Sex: {sex}
- Age: {age}
- Location: {location}
- Occupation: {occupation}
- Race/Ethnicity: {race}
- Religion: {religion}
- Birth Year: {birth_year}

Return only a JSON object with this structure:
{{
  "identities": [
    {{
      "first_name": "Name",
      "middle_name": "Middle",
      "last_name": "Surname",
      "cultural_notes": "Cultural context",
      "name_origin": "Origin explanation",
      "religious_context": "Religious significance"
    }}
  ],
  "cultural_analysis": {{
    "region": "Geographic region",
    "cultural_patterns": "Naming patterns",
    "religious_influence": "Religious naming influence"
  }}
}}"""

        payload = {
            "model": "phi3:mini",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": 1024,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        content = result.get('message', {}).get('content', '')
        
        # Parse the response
        try:
            # Clean and parse JSON
            cleaned_content = content.strip()
            if '```' in cleaned_content:
                start_marker = cleaned_content.find('```')
                end_marker = cleaned_content.rfind('```')
                if start_marker != -1 and end_marker > start_marker:
                    json_content = cleaned_content[start_marker + 3:end_marker].strip()
                    if json_content.startswith('json'):
                        json_content = json_content[4:].strip()
                    cleaned_content = json_content
            
            json_start = cleaned_content.find('{')
            json_end = cleaned_content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_content[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                return {
                    "status": "success",
                    "content": [
                        {"json": parsed_data}
                    ]
                }
        except Exception as e:
            logger.error(f"Error parsing Ollama response: {e}")
        
        # Fallback response
        return {
            "status": "success",
            "content": [
                {"text": f"Generated names for {sex} {age} year old {race} {religion} from {location}"}
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in generate_cultural_names_tool: {e}")
        return {
            "status": "error",
            "content": [
                {"text": f"Error generating names: {str(e)}"}
            ]
        }

# MCP Tool: Validate Names Against Watchlist
def validate_names_watchlist_tool(tool_input: Dict) -> Dict:
    """Validate generated names against watchlist patterns."""
    try:
        names = tool_input.get('names', [])
        if not names:
            return {
                "status": "error",
                "content": [
                    {"text": "No names provided for validation"}
                ]
            }
        
        # Simple watchlist validation patterns
        high_risk_patterns = [
            "terror", "bomb", "attack", "kill", "death", "hate",
            "nazi", "isis", "al-qaeda", "extremist"
        ]
        
        results = []
        for name in names:
            full_name = f"{name.get('first_name', '')} {name.get('last_name', '')}".lower()
            is_safe = True
            flagged_patterns = []
            
            for pattern in high_risk_patterns:
                if pattern in full_name:
                    is_safe = False
                    flagged_patterns.append(pattern)
            
            results.append({
                "name": full_name,
                "is_safe": is_safe,
                "flagged_patterns": flagged_patterns,
                "validation_status": "PASSED" if is_safe else "FLAGGED"
            })
        
        return {
            "status": "success",
            "content": [
                {"json": {"validation_results": results}}
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in validate_names_watchlist_tool: {e}")
        return {
            "status": "error",
            "content": [
                {"text": f"Error validating names: {str(e)}"}
            ]
        }

# MCP Tool: Get Cultural Context
def get_cultural_context_tool(tool_input: Dict) -> Dict:
    """Get cultural context and naming patterns for a region."""
    try:
        region = tool_input.get('region', 'Unknown')
        religion = tool_input.get('religion', 'Unknown')
        
        # Call Ollama for cultural analysis
        ollama_url = "http://localhost:11434/api/chat"
        prompt = f"""Provide cultural context and naming patterns for:
- Region: {region}
- Religion: {religion}

Return only a JSON object with this structure:
{{
  "cultural_context": {{
    "region": "{region}",
    "religion": "{religion}",
    "naming_patterns": "Description of naming conventions",
    "common_names": ["Common names in this culture"],
    "naming_rules": "Cultural naming rules and traditions",
    "religious_influence": "How religion affects naming"
  }}
}}"""

        payload = {
            "model": "phi3:mini",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 512,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        content = result.get('message', {}).get('content', '')
        
        # Parse the response
        try:
            cleaned_content = content.strip()
            if '```' in cleaned_content:
                start_marker = cleaned_content.find('```')
                end_marker = cleaned_content.rfind('```')
                if start_marker != -1 and end_marker > start_marker:
                    json_content = cleaned_content[start_marker + 3:end_marker].strip()
                    if json_content.startswith('json'):
                        json_content = json_content[4:].strip()
                    cleaned_content = json_content
            
            json_start = cleaned_content.find('{')
            json_end = cleaned_content.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_content[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                return {
                    "status": "success",
                    "content": [
                        {"json": parsed_data}
                    ]
                }
        except Exception as e:
            logger.error(f"Error parsing cultural context response: {e}")
        
        # Fallback response
        return {
            "status": "success",
            "content": [
                {"text": f"Cultural context for {region} {religion} region"}
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in get_cultural_context_tool: {e}")
        return {
            "status": "error",
            "content": [
                {"text": f"Error getting cultural context: {str(e)}"}
            ]
        }

# Register MCP Tools
register_mcp_tool(
    name="generate_cultural_names",
    description="Generate culturally appropriate names based on demographic and cultural parameters",
    input_schema={
        "json": {
            "type": "object",
            "properties": {
                "sex": {"type": "string", "description": "Sex of the person"},
                "age": {"type": "integer", "description": "Age of the person"},
                "location": {"type": "string", "description": "Geographic location"},
                "occupation": {"type": "string", "description": "Occupation"},
                "race": {"type": "string", "description": "Race/Ethnicity"},
                "religion": {"type": "string", "description": "Religion"},
                "birth_year": {"type": "integer", "description": "Birth year"}
            },
            "required": ["sex", "age", "location", "race", "religion"]
        }
    },
    func=generate_cultural_names_tool
)

register_mcp_tool(
    name="validate_names_watchlist",
    description="Validate generated names against watchlist patterns for safety",
    input_schema={
        "json": {
            "type": "object",
            "properties": {
                "names": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"}
                        }
                    },
                    "description": "List of names to validate"
                }
            },
            "required": ["names"]
        }
    },
    func=validate_names_watchlist_tool
)

register_mcp_tool(
    name="get_cultural_context",
    description="Get cultural context and naming patterns for a specific region and religion",
    input_schema={
        "json": {
            "type": "object",
            "properties": {
                "region": {"type": "string", "description": "Geographic region"},
                "religion": {"type": "string", "description": "Religion"}
            },
            "required": ["region", "religion"]
        }
    },
    func=get_cultural_context_tool
)

@app.route('/mcp', methods=['GET', 'POST'])
def mcp_endpoint():
    """Main MCP endpoint for tool discovery and execution."""
    if request.method == 'GET':
        """List available MCP tools (for Cursor discovery)."""
        logger.info("GET /mcp - Tool discovery request")
        tools_list = []
        for name, tool in MCP_TOOLS.items():
            tools_list.append({
                "name": tool['name'],
                "description": tool['description'],
                "inputSchema": tool['inputSchema']
            })
        
        logger.info(f"Returning {len(tools_list)} tools")
        return jsonify({"tools": tools_list})
    
    elif request.method == 'POST':
        """Execute MCP tool."""
        logger.info("POST /mcp - Tool execution request")
        logger.info(f"Headers: {dict(request.headers)}")
        
        try:
            data = request.get_json()
            logger.info(f"Received POST data: {data}")
            
            if not data:
                logger.error("No JSON data provided")
                return jsonify({"error": "No JSON data provided"}), 400
            
            # Handle MCP protocol format
            method = data.get('method')
            params = data.get('params', {})
            request_id = data.get('id')
            jsonrpc = data.get('jsonrpc', '2.0')
            
            logger.info(f"MCP Method: {method}")
            logger.info(f"MCP Params: {params}")
            logger.info(f"Request ID: {request_id}")
            
            # Handle MCP protocol methods
            if method == 'initialize':
                # MCP initialization
                logger.info("Handling MCP initialize")
                response = {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2025-06-18",
                        "capabilities": {
                            "tools": True,
                            "prompts": True,
                            "resources": False,
                            "logging": False,
                            "elicitation": {},
                            "roots": {"listChanged": False}
                        },
                        "serverInfo": {
                            "name": "name-generation-mcp-server",
                            "version": "1.0.0"
                        }
                    }
                }
                return jsonify(response)
            
            elif method == 'tools/list':
                # List available tools
                logger.info("Handling MCP tools/list")
                tools_list = []
                for name, tool in MCP_TOOLS.items():
                    tools_list.append({
                        "name": tool['name'],
                        "description": tool['description'],
                        "inputSchema": tool['inputSchema']
                    })
                
                response = {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "result": {
                        "tools": tools_list
                    }
                }
                return jsonify(response)
            
            elif method == 'tools/call':
                # Execute a tool
                logger.info("Handling MCP tools/call")
                tool_name = params.get('name')
                tool_input = params.get('arguments', {})
                
                logger.info(f"Tool name: {tool_name}")
                logger.info(f"Tool input: {tool_input}")
                logger.info(f"Available tools: {list(MCP_TOOLS.keys())}")
                
                if not tool_name:
                    error_response = {
                        "jsonrpc": jsonrpc,
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": "Invalid params: tool name required"
                        }
                    }
                    return jsonify(error_response), 400
                
                if tool_name not in MCP_TOOLS:
                    error_response = {
                        "jsonrpc": jsonrpc,
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Tool '{tool_name}' not found"
                        }
                    }
                    return jsonify(error_response), 404
                
                logger.info(f"Executing tool: {tool_name}")
                tool = MCP_TOOLS[tool_name]
                result = tool['function'](tool_input)
                logger.info(f"Tool execution successful")
                
                response = {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "result": {
                        "content": result.get('content', [])
                    }
                }
                return jsonify(response)
            
            else:
                # Unknown method
                logger.error(f"Unknown MCP method: {method}")
                error_response = {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method '{method}' not found"
                    }
                }
                return jsonify(error_response), 404
            
        except Exception as e:
            logger.error(f"Error in MCP endpoint: {e}")
            error_response = {
                "jsonrpc": data.get('jsonrpc', '2.0'),
                "id": data.get('id'),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            return jsonify(error_response), 500

@app.route('/mcp/tools', methods=['GET'])
def list_tools():
    """List available MCP tools."""
    tools_list = []
    for name, tool in MCP_TOOLS.items():
        tools_list.append({
            "name": tool['name'],
            "description": tool['description'],
            "inputSchema": tool['inputSchema']
        })
    
    return jsonify({"tools": tools_list})

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "MCP Server",
        "tools_available": len(MCP_TOOLS),
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    logger.info("Starting Flask MCP Server on port 8500...")
    logger.info(f"Available tools: {list(MCP_TOOLS.keys())}")
    app.run(host='0.0.0.0', port=8500, debug=False)

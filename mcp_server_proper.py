#!/usr/bin/env python3
"""
Proper MCP Server Implementation
Implements the MCP protocol correctly for Cursor tool discovery
"""

import json
import logging
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    """Proper MCP Server implementation."""
    
    def __init__(self):
        self.tools = {}
        self.register_tools()
    
    def register_tools(self):
        """Register MCP tools."""
        
        # Tool: Generate Cultural Names
        self.tools["generate_cultural_names"] = {
            "name": "generate_cultural_names",
            "description": "Generate culturally appropriate names based on demographic and cultural parameters",
            "inputSchema": {
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
            },
            "function": self.generate_cultural_names_tool
        }
        
        # Tool: Validate Names Against Watchlist
        self.tools["validate_names_watchlist"] = {
            "name": "validate_names_watchlist",
            "description": "Validate generated names against watchlist patterns for safety",
            "inputSchema": {
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
            },
            "function": self.validate_names_watchlist_tool
        }
        
        # Tool: Get Cultural Context
        self.tools["get_cultural_context"] = {
            "name": "get_cultural_context",
            "description": "Get cultural context and naming patterns for a specific region and religion",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "region": {"type": "string", "description": "Geographic region"},
                    "religion": {"type": "string", "description": "Religion"}
                },
                "required": ["region", "religion"]
            },
            "function": self.get_cultural_context_tool
        }
    
    def generate_cultural_names_tool(self, arguments: Dict) -> Dict:
        """Generate culturally appropriate names using Ollama."""
        try:
            # Extract parameters
            sex = arguments.get('sex', 'Unknown')
            age = arguments.get('age', 25)
            location = arguments.get('location', 'Unknown')
            occupation = arguments.get('occupation', 'Unknown')
            race = arguments.get('race', 'Unknown')
            religion = arguments.get('religion', 'Unknown')
            birth_year = arguments.get('birth_year', 1999)
            
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
                        "content": [
                            {"type": "text", "text": f"Generated {len(parsed_data.get('identities', []))} culturally appropriate names for {sex} {age} year old {race} {religion} from {location}"},
                            {"type": "json", "json": parsed_data}
                        ]
                    }
            except Exception as e:
                logger.error(f"Error parsing Ollama response: {e}")
            
            # Fallback response
            return {
                "content": [
                    {"type": "text", "text": f"Generated names for {sex} {age} year old {race} {religion} from {location}"}
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in generate_cultural_names_tool: {e}")
            return {
                "content": [
                    {"type": "text", "text": f"Error generating names: {str(e)}"}
                ]
            }
    
    def validate_names_watchlist_tool(self, arguments: Dict) -> Dict:
        """Validate generated names against watchlist patterns."""
        try:
            names = arguments.get('names', [])
            if not names:
                return {
                    "content": [
                        {"type": "text", "text": "No names provided for validation"}
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
                "content": [
                    {"type": "text", "text": f"Validated {len(results)} names against watchlist patterns"},
                    {"type": "json", "json": {"validation_results": results}}
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in validate_names_watchlist_tool: {e}")
            return {
                "content": [
                    {"type": "text", "text": f"Error validating names: {str(e)}"}
                ]
            }
    
    def get_cultural_context_tool(self, arguments: Dict) -> Dict:
        """Get cultural context and naming patterns for a region."""
        try:
            region = arguments.get('region', 'Unknown')
            religion = arguments.get('religion', 'Unknown')
            
            # Call Ollama for cultural analysis
            ollama_url = "http://localhost:11434/api/chat"
            prompt = f"""Provide cultural context and naming patterns for {region} region with {religion} religion.

Return only a JSON object with this structure:
{{
  "cultural_context": {{
    "region": "{region}",
    "religion": "{religion}",
    "common_names": ["Name1", "Name2", "Name3"],
    "naming_patterns": "Description of naming patterns",
    "naming_rules": {{
      "gender-specificity": "Description",
      "preference for historical figures": "Description"
    }},
    "religious_influence": {{
      "selection_based_on_religion": "Description",
      "avoidance_of_certain_words": "Description"
    }}
  }}
}}"""

            payload = {
                "model": "phi3:mini",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {
                    "temperature": 0.7,
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
                        "content": [
                            {"type": "text", "text": f"Cultural context for {region} {religion} region"},
                            {"type": "json", "json": parsed_data}
                        ]
                    }
            except Exception as e:
                logger.error(f"Error parsing Ollama response: {e}")
            
            # Fallback response
            return {
                "content": [
                    {"type": "text", "text": f"Cultural context for {region} {religion} region"}
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in get_cultural_context_tool: {e}")
            return {
                "content": [
                    {"type": "text", "text": f"Error getting cultural context: {str(e)}"}
                ]
            }
    
    def handle_request(self, data: Dict) -> Dict:
        """Handle MCP request."""
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')
        jsonrpc = data.get('jsonrpc', '2.0')
        
        logger.info(f"Handling MCP method: {method}")
        
        if method == 'initialize':
            return {
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
        
        elif method == 'tools/list':
            tools_list = []
            for name, tool in self.tools.items():
                tools_list.append({
                    "name": tool['name'],
                    "description": tool['description'],
                    "inputSchema": tool['inputSchema']
                })
            
            return {
                "jsonrpc": jsonrpc,
                "id": request_id,
                "result": {
                    "tools": tools_list
                }
            }
        
        elif method == 'tools/call':
            tool_name = params.get('name')
            tool_arguments = params.get('arguments', {})
            
            if not tool_name or tool_name not in self.tools:
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool '{tool_name}' not found"
                    }
                }
            
            try:
                tool = self.tools[tool_name]
                result = tool['function'](tool_arguments)
                
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "result": result
                }
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {e}")
                return {
                    "jsonrpc": jsonrpc,
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
        
        else:
            return {
                "jsonrpc": jsonrpc,
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            }

# Create MCP server instance
mcp_server = MCPServer()

# Simple HTTP server for MCP protocol
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class MCPHandler(BaseHTTPRequestHandler):
    """HTTP handler for MCP protocol."""
    
    def do_GET(self):
        """Handle GET requests for tool discovery."""
        if self.path == '/mcp':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            tools_list = []
            for name, tool in mcp_server.tools.items():
                tools_list.append({
                    "name": tool['name'],
                    "description": tool['description'],
                    "inputSchema": tool['inputSchema']
                })
            
            response = {"tools": tools_list}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for MCP protocol."""
        if self.path == '/mcp':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                response = mcp_server.handle_request(data)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                logger.error(f"Error handling POST request: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_mcp_server(port=8500):
    """Run the MCP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPHandler)
    logger.info(f"Starting MCP server on port {port}")
    logger.info(f"Available tools: {list(mcp_server.tools.keys())}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_mcp_server()

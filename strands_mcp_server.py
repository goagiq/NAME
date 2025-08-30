#!/usr/bin/env python3
"""
Strands MCP Server
Exposes Strands tools using @tool decorator for Cursor integration
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from strands_tools import generate_cultural_names, validate_names_watchlist, get_cultural_context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrandsMCPServer:
    """MCP Server that exposes Strands tools."""
    
    def __init__(self):
        self.tools = {
            "generate_cultural_names": generate_cultural_names,
            "validate_names_watchlist": validate_names_watchlist,
            "get_cultural_context": get_cultural_context
        }
    
    def get_tool_spec(self, tool_func):
        """Extract tool specification from decorated function."""
        if hasattr(tool_func, '_tool_name'):
            name = tool_func._tool_name
        else:
            name = tool_func.__name__
        
        # Get description from docstring
        description = tool_func.__doc__ or ""
        
        # Extract type hints for input schema
        import inspect
        sig = inspect.signature(tool_func)
        parameters = sig.parameters
        
        properties = {}
        required = []
        
        for param_name, param in parameters.items():
            if param_name == 'self':
                continue
                
            param_type = param.annotation
            param_default = param.default
            
            # Convert Python types to JSON schema types
            if param_type == str:
                json_type = "string"
            elif param_type == int:
                json_type = "integer"
            elif param_type == bool:
                json_type = "boolean"
            elif param_type == list:
                json_type = "array"
            elif param_type == dict:
                json_type = "object"
            elif param_type == type(None):
                json_type = "string"  # Handle None type
            else:
                json_type = "string"
            
            properties[param_name] = {
                "type": json_type,
                "description": f"Parameter {param_name}"
            }
            
            # If no default, it's required
            if param_default == inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "name": name,
            "description": description,
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    
    def list_tools(self):
        """List all available tools."""
        tools_list = []
        logger.info(f"Available tools in registry: {list(self.tools.keys())}")
        for name, tool_func in self.tools.items():
            try:
                logger.info(f"Processing tool: {name}")
                tool_spec = self.get_tool_spec(tool_func)
                tools_list.append(tool_spec)
                logger.info(f"Successfully added tool: {name}")
            except Exception as e:
                logger.error(f"Error processing tool {name}: {e}")
        logger.info(f"Final tools list: {[tool['name'] for tool in tools_list]}")
        return tools_list
    
    def call_tool(self, tool_name, arguments):
        """Call a tool with arguments."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool_func = self.tools[tool_name]
        
        # Call the tool function
        try:
            result = tool_func(**arguments)
            return {
                "content": [
                    {"type": "text", "text": result}
                ]
            }
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {
                "content": [
                    {"type": "text", "text": f"Error: {str(e)}"}
                ]
            }

# Create server instance
strands_mcp_server = StrandsMCPServer()

class StrandsMCPHandler(BaseHTTPRequestHandler):
    """HTTP handler for Strands MCP protocol."""
    
    def do_GET(self):
        """Handle GET requests for tool discovery."""
        if self.path == '/mcp':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            tools_list = strands_mcp_server.list_tools()
            response = {"tools": tools_list}
            self.wfile.write(json.dumps(response, indent=2).encode())
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
                method = data.get('method')
                params = data.get('params', {})
                request_id = data.get('id')
                jsonrpc = data.get('jsonrpc', '2.0')
                
                logger.info(f"Handling MCP method: {method}")
                
                if method == 'initialize':
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
                                "name": "strands-name-generation-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                
                elif method == 'tools/list':
                    tools_list = strands_mcp_server.list_tools()
                    response = {
                        "jsonrpc": jsonrpc,
                        "id": request_id,
                        "result": {
                            "tools": tools_list
                        }
                    }
                
                elif method == 'tools/call':
                    tool_name = params.get('name')
                    tool_arguments = params.get('arguments', {})
                    
                    if not tool_name:
                        response = {
                            "jsonrpc": jsonrpc,
                            "id": request_id,
                            "error": {
                                "code": -32602,
                                "message": "Invalid params: tool name required"
                            }
                        }
                    else:
                        try:
                            result = strands_mcp_server.call_tool(tool_name, tool_arguments)
                            response = {
                                "jsonrpc": jsonrpc,
                                "id": request_id,
                                "result": result
                            }
                        except Exception as e:
                            response = {
                                "jsonrpc": jsonrpc,
                                "id": request_id,
                                "error": {
                                    "code": -32603,
                                    "message": f"Internal error: {str(e)}"
                                }
                            }
                
                else:
                    response = {
                        "jsonrpc": jsonrpc,
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method '{method}' not found"
                        }
                    }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
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

def run_strands_mcp_server(port=8500):
    """Run the Strands MCP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, StrandsMCPHandler)
    logger.info(f"Starting Strands MCP server on port {port}")
    
    # List available tools
    tools_list = strands_mcp_server.list_tools()
    logger.info(f"Available tools: {[tool['name'] for tool in tools_list]}")
    
    for tool in tools_list:
        logger.info(f"  - {tool['name']}: {tool['description'][:50]}...")
    
    httpd.serve_forever()

if __name__ == '__main__':
    run_strands_mcp_server()

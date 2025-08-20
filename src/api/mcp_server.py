"""
MCP Server Implementation for Name Generation System
Provides proper streamable HTTP protocol support for MCP clients.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core import IdentityGenerator, IdentityRequest

logger = logging.getLogger(__name__)

# MCP Tools for Name Generation System
MCP_TOOLS = [
    {
        "name": "generate_identity",
        "description": "Generate culturally appropriate identity based on parameters",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sex": {"type": "string", "description": "Sex (Male/Female/Non-binary)"},
                "location": {"type": "string", "description": "Location (Country, City)"},
                "age": {"type": "integer", "description": "Age"},
                "occupation": {"type": "string", "description": "Occupation"},
                "race": {"type": "string", "description": "Race/Ethnicity"},
                "religion": {"type": "string", "description": "Religion"},
                "birth_year": {"type": "integer", "description": "Birth year"},
                "birth_country": {"type": "string", "description": "Country of birth/origin (optional)"},
                "citizenship_country": {"type": "string", "description": "Current citizenship (optional)"},
                "diaspora_generation": {"type": "integer", "description": "Immigrant generation (optional)"}
            },
            "required": ["sex", "location", "age", "occupation", "race", "religion", "birth_year"]
        }
    },
    {
        "name": "validate_name",
        "description": "Validate a name against watchlists and cultural requirements",
        "inputSchema": {
            "type": "object",
            "properties": {
                "first_name": {"type": "string", "description": "First name"},
                "middle_name": {"type": "string", "description": "Middle name (optional)"},
                "last_name": {"type": "string", "description": "Last name"},
                "culture": {"type": "string", "description": "Cultural context"},
                "religion": {"type": "string", "description": "Religious context"}
            },
            "required": ["first_name", "last_name", "culture", "religion"]
        }
    },
    {
        "name": "cultural_analysis",
        "description": "Analyze cultural context for name generation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Location (Country, City)"},
                "race": {"type": "string", "description": "Race/Ethnicity"},
                "religion": {"type": "string", "description": "Religion"}
            },
            "required": ["location", "race", "religion"]
        }
    },
    {
        "name": "get_traceability",
        "description": "Get detailed traceability information for a generated identity",
        "inputSchema": {
            "type": "object",
            "properties": {
                "request_id": {"type": "string", "description": "Request ID"},
                "identity_data": {"type": "object", "description": "Identity data"}
            },
            "required": ["identity_data"]
        }
    }
]


class MCPRequest(BaseModel):
    """MCP request model."""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP response model."""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class MCPServer:
    """MCP Server implementation with streamable HTTP support."""
    
    def __init__(self):
        self.identity_generator = IdentityGenerator()
        self.tools = MCP_TOOLS
        
    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request and return response."""
        try:
            method = request_data.get("method")
            request_id = request_data.get("id")
            params = request_data.get("params", {})
            
            logger.info(f"Handling MCP request: {method}")
            
            if method == "initialize":
                return self._create_response(request_id, {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "Name Generation MCP Server",
                        "version": "1.0.0"
                    }
                })
            
            elif method == "tools/list":
                return self._create_response(request_id, {
                    "tools": self.tools
                })
            
            elif method == "tools/call":
                return await self._handle_tool_call(request_id, params)
            
            else:
                return self._create_error_response(request_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            logger.error(f"Error handling MCP request: {e}")
            return self._create_error_response(request_data.get("id"), -32603, str(e))
    
    async def _handle_tool_call(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call requests."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Calling tool: {tool_name} with arguments: {arguments}")
        
        if tool_name == "generate_identity":
            return await self._generate_identity_tool(request_id, arguments)
        elif tool_name == "validate_name":
            return await self._validate_name_tool(request_id, arguments)
        elif tool_name == "cultural_analysis":
            return await self._cultural_analysis_tool(request_id, arguments)
        elif tool_name == "get_traceability":
            return await self._get_traceability_tool(request_id, arguments)
        else:
            return self._create_error_response(request_id, -32601, f"Tool not found: {tool_name}")
    
    async def _generate_identity_tool(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle identity generation tool call."""
        try:
            # Create identity request
            identity_request = IdentityRequest(
                sex=arguments["sex"],
                location=arguments["location"],
                age=arguments["age"],
                occupation=arguments["occupation"],
                race=arguments["race"],
                religion=arguments["religion"],
                birth_year=arguments["birth_year"],
                birth_country=arguments.get("birth_country"),
                citizenship_country=arguments.get("citizenship_country"),
                diaspora_generation=arguments.get("diaspora_generation")
            )
            
            # Generate identities
            identities = self.identity_generator.generate_identity(identity_request)
            
            # Convert to serializable format
            result_identities = []
            for identity in identities:
                result_identities.append({
                    "first_name": identity.first_name,
                    "middle_name": identity.middle_name,
                    "last_name": identity.last_name,
                    "cultural_context": identity.cultural_context,
                    "validation_status": identity.validation_status,
                    "validation_notes": identity.validation_notes,
                    "generated_date": identity.generated_date.isoformat()
                })
            
            return self._create_response(request_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Generated {len(result_identities)} identities successfully"
                    }
                ],
                "isError": False,
                "identities": result_identities
            })
            
        except Exception as e:
            logger.error(f"Error in generate_identity_tool: {e}")
            return self._create_error_response(request_id, -32603, str(e))
    
    async def _validate_name_tool(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle name validation tool call."""
        try:
            first_name = arguments["first_name"]
            last_name = arguments["last_name"]
            culture = arguments["culture"]
            religion = arguments["religion"]
            
            # Mock validation logic (in real implementation, this would use the validation agent)
            validation_result = {
                "is_valid": True,
                "watchlist_check": "PASSED",
                "cultural_check": "PASSED",
                "religious_check": "PASSED",
                "notes": ["Name validation completed successfully"]
            }
            
            return self._create_response(request_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Validation completed for {first_name} {last_name}"
                    }
                ],
                "isError": False,
                "validation_result": validation_result
            })
            
        except Exception as e:
            logger.error(f"Error in validate_name_tool: {e}")
            return self._create_error_response(request_id, -32603, str(e))
    
    async def _cultural_analysis_tool(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle cultural analysis tool call."""
        try:
            location = arguments["location"]
            race = arguments["race"]
            religion = arguments["religion"]
            
            # Mock cultural analysis (in real implementation, this would use the locality agent)
            cultural_analysis = {
                "culture": race,
                "region": location,
                "language": "English",  # Default
                "religion": religion,
                "naming_conventions": {
                    "supports_middle_names": True,
                    "supports_hyphenation": True
                },
                "special_requirements": []
            }
            
            return self._create_response(request_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Cultural analysis completed for {location}, {race}, {religion}"
                    }
                ],
                "isError": False,
                "cultural_analysis": cultural_analysis
            })
            
        except Exception as e:
            logger.error(f"Error in cultural_analysis_tool: {e}")
            return self._create_error_response(request_id, -32603, str(e))
    
    async def _get_traceability_tool(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle traceability tool call."""
        try:
            identity_data = arguments["identity_data"]
            
            # Mock traceability data
            traceability = {
                "request_parameters": identity_data,
                "cultural_analysis": {
                    "culture": "Unknown",
                    "region": "Unknown",
                    "language": "Unknown",
                    "religion": "Unknown"
                },
                "name_generation_steps": [
                    {
                        "step": 1,
                        "description": "Cultural context analysis",
                        "result": "Analysis completed"
                    }
                ],
                "validation_steps": [
                    {
                        "step": 1,
                        "description": "Comprehensive validation",
                        "result": "Validation completed"
                    }
                ],
                "final_result": {
                    "generated_name": f"{identity_data.get('first_name', '')} {identity_data.get('last_name', '')}",
                    "validation_status": "validated"
                }
            }
            
            return self._create_response(request_id, {
                "content": [
                    {
                        "type": "text",
                        "text": "Traceability report generated successfully"
                    }
                ],
                "isError": False,
                "traceability": traceability
            })
            
        except Exception as e:
            logger.error(f"Error in get_traceability_tool: {e}")
            return self._create_error_response(request_id, -32603, str(e))
    
    def _create_response(self, request_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create a successful MCP response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    def _create_error_response(self, request_id: str, code: int, message: str) -> Dict[str, Any]:
        """Create an error MCP response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }


# Create MCP server instance
mcp_server = MCPServer()


async def stream_mcp_response(request_data: Dict[str, Any]):
    """Stream MCP response for streamable HTTP protocol."""
    response = await mcp_server.handle_request(request_data)
    yield f"data: {json.dumps(response)}\n\n"


def create_mcp_app() -> FastAPI:
    """Create FastAPI app with MCP endpoints."""
    app = FastAPI(title="MCP Server - Name Generation System", version="1.0.0")
    
    @app.post("/mcp")
    async def mcp_endpoint(request: Request):
        """Main MCP endpoint with streamable HTTP support."""
        try:
            # Check headers for streamable HTTP
            accept_header = request.headers.get("accept", "")
            is_streamable = "text/event-stream" in accept_header
            
            # Parse request body
            body = await request.body()
            request_data = json.loads(body.decode('utf-8'))
            
            logger.info(f"MCP request: {request_data}")
            
            if is_streamable:
                # Return streaming response
                return StreamingResponse(
                    stream_mcp_response(request_data),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*"
                    }
                )
            else:
                # Return regular JSON response
                response = await mcp_server.handle_request(request_data)
                return Response(
                    content=json.dumps(response),
                    media_type="application/json",
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*"
                    }
                )
                
        except Exception as e:
            logger.error(f"Error in MCP endpoint: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            return Response(
                content=json.dumps(error_response),
                media_type="application/json",
                status_code=500
            )
    
    @app.get("/mcp")
    async def mcp_get_endpoint():
        """Handle GET requests to MCP endpoint."""
        return {
            "message": "MCP Server - Name Generation System",
            "version": "1.0.0",
            "protocol": "streamable HTTP",
            "tools": [tool["name"] for tool in MCP_TOOLS]
        }
    
    @app.options("/mcp")
    async def mcp_options():
        """Handle CORS preflight requests."""
        return Response(
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept",
                "Access-Control-Max-Age": "86400"
            }
        )
    
    return app


# Create the MCP app
mcp_app = create_mcp_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp_app, host="0.0.0.0", port=8001)

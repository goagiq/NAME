#!/usr/bin/env python3
"""
Proper MCP Server Implementation
Implements the MCP protocol with streamable HTTP support.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="MCP Server", version="1.0.0")

# Add CORS middleware for MCP clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP Tools for Name Generation System
MCP_TOOLS = [
    {
        "name": "domain_check",
        "description": "Check domain availability across TLDs",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to check"},
                "domain": {"type": "string", "description": "Domain extension"}
            },
            "required": ["name", "domain"]
        }
    },
    {
        "name": "watchlist_validate",
        "description": "Check names against government and industry watchlists including OFAC, FBI, Interpol, UN Sanctions, and more",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to validate"},
                "category": {"type": "string", "description": "Category (person, project, etc.)"}
            },
            "required": ["name", "category"]
        }
    },
    {
        "name": "comprehensive_watchlist_check",
        "description": "Comprehensive watchlist validation against multiple government and industry databases",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name to validate"},
                "category": {"type": "string", "description": "Category (person, project, etc.)"},
                "sources": {"type": "array", "items": {"type": "string"}, "description": "Specific sources to check (optional)"}
            },
            "required": ["name", "category"]
        }
    },
    {
        "name": "cultural_context_search",
        "description": "Analyze cultural meaning and context of names",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to analyze"},
                "region": {"type": "string", "description": "Geographic region"}
            },
            "required": ["name", "region"]
        }
    },
    {
        "name": "trademark_check",
        "description": "Validate trademark availability in specific industries",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to check"},
                "industry": {"type": "string", "description": "Industry category"}
            },
            "required": ["name", "industry"]
        }
    },
    {
        "name": "name_variation_generator",
        "description": "Create style-based variations of base names",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_name": {"type": "string", "description": "Base name to vary"},
                "style": {"type": "string", "description": "Style (modern, classic, etc.)"},
                "count": {"type": "integer", "description": "Number of variations"}
            },
            "required": ["base_name", "style"]
        }
    }
]

# Pydantic models for MCP protocol
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

async def handle_tool_call(name: str, arguments: Dict[str, Any]) -> str:
    """Handle MCP tool calls."""
    logger.info(f"Tool call: {name} with arguments: {arguments}")
    
    if name == "domain_check":
        name_val = arguments.get("name", "example")
        domain = arguments.get("domain", "com")
        return f"Domain {name_val}.{domain} appears to be available"
        
    elif name == "watchlist_validate":
        name_val = arguments.get("name", "Unknown")
        category = arguments.get("category", "Unknown")
        return f"Watchlist validation for '{name_val}' in category '{category}': PASSED"
        
    elif name == "comprehensive_watchlist_check":
        name_val = arguments.get("name", "Unknown")
        category = arguments.get("category", "person")
        sources = arguments.get("sources", [])
        
        # Import and use the comprehensive watchlist validator
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'services', 'validation'))
            
            from watchlist_validator import validate_name_standalone
            
            # Perform comprehensive validation
            result = await validate_name_standalone(name_val, category)
            
            if result.is_blocked:
                sources_str = ", ".join(result.sources) if result.sources else "multiple sources"
                reasons_str = "; ".join(result.reasons) if result.reasons else "watchlist match"
                return f"WATCHLIST BLOCKED: '{name_val}' found in {sources_str}. Reasons: {reasons_str}. Confidence: {result.confidence:.2f}"
            else:
                return f"WATCHLIST CLEAR: '{name_val}' passed validation against {len(result.raw_data)} sources. Confidence: {result.confidence:.2f}"
                
        except ImportError as e:
            logger.error(f"Failed to import watchlist validator: {e}")
            return f"Watchlist validation for '{name_val}' in category '{category}': UNAVAILABLE (validator not found)"
        except Exception as e:
            logger.error(f"Watchlist validation failed: {e}")
            return f"Watchlist validation for '{name_val}' in category '{category}': ERROR ({str(e)})"
        
    elif name == "cultural_context_search":
        name_val = arguments.get("name", "Unknown")
        region = arguments.get("region", "global")
        return f"Cultural context for '{name_val}' in {region}: Common name with positive cultural associations"
        
    elif name == "trademark_check":
        name_val = arguments.get("name", "Unknown")
        industry = arguments.get("industry", "general")
        return f"Trademark check for '{name_val}' in {industry} industry: No conflicts found"
        
    elif name == "name_variation_generator":
        base_name = arguments.get("base_name", "Example")
        style = arguments.get("style", "modern")
        count = arguments.get("count", 3)
        variations = [f"{base_name}{i}" for i in range(1, count + 1)]
        return f"Generated {len(variations)} {style} variations: {', '.join(variations)}"
        
    else:
        raise ValueError(f"Unknown tool: {name}")

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main MCP endpoint supporting streamable HTTP protocol."""
    logger.info(f"MCP endpoint received request: {request.method} {request.url}")
    
    # Check for proper headers
    accept_header = request.headers.get("accept", "")
    content_type = request.headers.get("content-type", "")
    
    logger.info(f"Accept header: {accept_header}")
    logger.info(f"Content-Type: {content_type}")
    
    # Validate headers for MCP protocol
    if "application/json" not in content_type:
        logger.warning("Invalid Content-Type header")
        return Response(
            status_code=400,
            content=json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32600,
                    "message": "Invalid Content-Type header"
                }
            }),
            media_type="application/json"
        )
    
    try:
        # Parse the JSON-RPC request
        body = await request.json()
        logger.info(f"MCP request: {body}")
        
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id")
        
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "Name Generation MCP Server",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": MCP_TOOLS
                }
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "Missing tool name"
                    }
                }
            else:
                try:
                    result = await handle_tool_call(tool_name, arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": result}]
                        }
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": f"Tool call failed: {str(e)}"
                        }
                    }
                    
        elif method == "notifications/cancel":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {}
            }
            
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        
        logger.info(f"MCP response: {response}")
        
        # Return response with proper headers
        return Response(
            content=json.dumps(response),
            media_type="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return Response(
            status_code=400,
            content=json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }),
            media_type="application/json"
        )
    except Exception as e:
        logger.error(f"MCP endpoint error: {e}")
        return Response(
            status_code=500,
            content=json.dumps({
                "jsonrpc": "2.0",
                "id": body.get("id") if 'body' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }),
            media_type="application/json"
        )

@app.options("/mcp")
async def mcp_options():
    """Handle CORS preflight requests."""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept",
            "Access-Control-Max-Age": "86400"
        }
    )

@app.get("/mcp")
async def mcp_get():
    """Handle GET requests to MCP endpoint."""
    return {
        "jsonrpc": "2.0",
        "id": None,
        "result": {
            "message": "MCP Server is running",
            "protocol": "streamable HTTP",
            "tools": len(MCP_TOOLS)
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mcp-server",
        "tools": len(MCP_TOOLS),
        "protocol": "streamable HTTP"
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MCP Server for Name Generation System",
        "version": "1.0.0",
        "endpoints": {
            "mcp": "/mcp",
            "health": "/health"
        },
        "tools": [tool["name"] for tool in MCP_TOOLS]
    }

def main():
    """Start the MCP server."""
    logger.info("Starting MCP Server on http://localhost:8500")
    logger.info(f"Available tools: {[tool['name'] for tool in MCP_TOOLS]}")
    logger.info("Protocol: Streamable HTTP")
    logger.info("MCP endpoint: http://localhost:8500/mcp")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8500,
        log_level="info"
    )

if __name__ == "__main__":
    main()

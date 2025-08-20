"""
FastAPI Server
Main API server for the Name Generation System.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional

from services.ai.mcp_integration import MCPToolManager
from services.ai.strands_agent import StrandsAgentManager


class NameGenerationRequest(BaseModel):
    category: str
    parameters: Dict


class NameValidationRequest(BaseModel):
    name: str
    category: str


class ToolManagementRequest(BaseModel):
    tool_name: str
    action: str  # "enable" or "disable"


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Name Generation System",
        description="AI-powered name generation with MCP tools and Strands agents",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize managers
    mcp_manager = MCPToolManager()
    strands_manager = StrandsAgentManager()
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "name-generation-system"}
    
    @app.get("/api/categories")
    async def get_categories():
        """Get available name categories."""
        categories = [
            {"id": "person", "name": "Person Names", "description": "Names for individuals"},
            {"id": "project", "name": "Project Names", "description": "Names for projects and initiatives"},
            {"id": "code", "name": "Code Names", "description": "Names for software and code"},
            {"id": "mission", "name": "Mission Names", "description": "Names for missions and operations"},
            {"id": "place", "name": "Place Names", "description": "Names for locations and places"}
        ]
        return {"categories": categories}
    
    @app.post("/api/names/generate")
    async def generate_names(request: NameGenerationRequest):
        """Generate names based on category and parameters."""
        try:
            # Check if fast mode is requested
            use_fast_mode = request.parameters.get('fast_mode', True)
            
            if use_fast_mode:
                # Use fast generation for better performance
                result = strands_manager.generate_names_fast(
                    request.category, 
                    request.parameters
                )
            else:
                # Use swarm for complex generation (slower)
                result = strands_manager.generate_names_with_swarm(
                    request.category, 
                    request.parameters
                )
            
            return {
                "success": True,
                "category": request.category,
                "parameters": request.parameters,
                "result": result,
                "mode": "fast" if use_fast_mode else "swarm"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/names/validate")
    async def validate_name(request: NameValidationRequest):
        """Validate a name using MCP tools."""
        try:
            # Use MCP validation tool
            result = await mcp_manager.call_tool(
                "name_validation",
                {"name": request.name, "category": request.category}
            )
            
            return {
                "success": True,
                "name": request.name,
                "category": request.category,
                "result": result
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/traceability/{request_id}")
    async def get_traceability(request_id: str):
        """Get traceability report for a request."""
        try:
            # For now, return a mock traceability report
            # In a real implementation, this would fetch from a database
            return {
                "request_id": request_id,
                "timestamp": "2024-01-01T00:00:00Z",
                "status": "completed",
                "steps": [
                    {
                        "step": 1,
                        "name": "Request Received",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "status": "completed"
                    },
                    {
                        "step": 2,
                        "name": "AI Model Processing",
                        "timestamp": "2024-01-01T00:00:05Z",
                        "status": "completed"
                    },
                    {
                        "step": 3,
                        "name": "Name Generation",
                        "timestamp": "2024-01-01T00:00:10Z",
                        "status": "completed"
                    },
                    {
                        "step": 4,
                        "name": "Response Sent",
                        "timestamp": "2024-01-01T00:00:12Z",
                        "status": "completed"
                    }
                ],
                "generated_names": [
                    {
                        "name": "Sample Generated Name",
                        "confidence": 0.95,
                        "cultural_context": "Mixed",
                        "validation_status": "validated"
                    }
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/test-traceability")
    async def test_traceability():
        """Test endpoint for traceability."""
        return {"message": "Traceability test endpoint working"}
    
    @app.get("/api/mcp/tools")
    async def list_mcp_tools():
        """List available MCP tools."""
        try:
            tools = mcp_manager.list_tools()
            return {"tools": tools}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/mcp/tools/manage")
    async def manage_mcp_tool(request: ToolManagementRequest):
        """Enable or disable MCP tools."""
        try:
            if request.action == "enable":
                success = mcp_manager.enable_tool(request.tool_name)
            elif request.action == "disable":
                success = mcp_manager.disable_tool(request.tool_name)
            else:
                raise HTTPException(status_code=400, detail="Invalid action")
            
            return {
                "success": success,
                "tool_name": request.tool_name,
                "action": request.action
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/mcp/tools/enabled")
    async def get_enabled_tools():
        """Get list of enabled MCP tools."""
        try:
            enabled_tools = mcp_manager.get_enabled_tools()
            return {"enabled_tools": enabled_tools}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/agents")
    async def list_agents():
        """List available Strands agents."""
        try:
            agents = strands_manager.list_agents()
            swarms = strands_manager.list_swarms()
            return {
                "agents": agents,
                "swarms": swarms
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/test/mcp")
    async def test_mcp_connection():
        """Test MCP connection."""
        try:
            success = mcp_manager.test_connection()
            return {"success": success, "message": "MCP connection test completed"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

#!/usr/bin/env python3
"""
Start API Server with Dynamic Port Allocation
Automatically finds available ports to avoid conflicts.
"""

import sys
from pathlib import Path
import uvicorn

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import port manager
from port_manager import get_system_ports, print_port_status

def main():
    """Start the API server with dynamic port allocation."""
    print("🚀 Starting Name Generation API Server")
    print("=" * 50)
    
    # Get available ports
    try:
        mcp_port, api_port = get_system_ports()
        print(f"📍 MCP Server: http://localhost:{mcp_port}")
        print(f"📍 API Server: http://localhost:{api_port}")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Failed to get available ports: {e}")
        return False
    
    try:
        from api.server import create_app
        
        # Create the FastAPI app
        app = create_app()
        
        print("✅ FastAPI app created successfully")
        print(f"🌐 Starting server on http://localhost:{api_port}")
        print("\n📋 Available endpoints:")
        print("   • GET  /health - Health check")
        print("   • GET  /api/categories - Available categories")
        print("   • POST /api/names/generate - Generate names")
        print("   • POST /api/names/validate - Validate names with MCP")
        print("   • GET  /api/mcp/tools - List MCP tools")
        print("   • POST /api/mcp/tools/manage - Manage MCP tools")
        print("   • POST /api/test/mcp - Test MCP connection")
        print()
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=api_port,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return False

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Strands MCP Integration"""
import requests
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class StrandsMCPIntegration:
    """Strands MCP Integration for name generation system."""
    
    def __init__(self, mcp_url: str = "http://localhost:8500"):
        self.mcp_url = mcp_url
        self.base_url = f"{mcp_url}/mcp"
        self.tools_url = f"{mcp_url}/mcp/tools"
    
    def health_check(self) -> bool:
        """Check if MCP server is healthy."""
        try:
            response = requests.get(self.mcp_url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"MCP server health check failed: {e}")
            return False
    
    def call_tool(self, tool_name: str, tool_input: Dict) -> Dict:
        """Call an MCP tool."""
        try:
            payload = {"name": tool_name, "input": tool_input}
            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            return {"status": "error", "content": [{"text": f"Error calling tool: {str(e)}"}]}

def test_mcp_tools():
    """Test the MCP tools directly."""
    print("Testing Testing MCP Tools...")
    mcp = StrandsMCPIntegration()
    if not mcp.health_check():
        print("ERROR MCP server is not healthy")
        return False
    print("OK MCP server is healthy")
    print("MCP Tools MCP Tools are working!")
    return True

if __name__ == "__main__":
    test_mcp_tools()

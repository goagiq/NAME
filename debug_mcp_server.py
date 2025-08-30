#!/usr/bin/env python3
"""
Debug MCP Server to check tool registration
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from strands_tools import generate_cultural_names, validate_names_watchlist, get_cultural_context, weather_forecast

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_tools():
    """Debug tool registration."""
    print("=== Debugging Tool Registration ===")
    
    tools = {
        "generate_cultural_names": generate_cultural_names,
        "validate_names_watchlist": validate_names_watchlist,
        "get_cultural_context": get_cultural_context,
        "weather_forecast": weather_forecast
    }
    
    for name, tool_func in tools.items():
        print(f"\nTool: {name}")
        print(f"  Function: {tool_func}")
        print(f"  Name: {tool_func.__name__}")
        print(f"  Has _tool_name: {hasattr(tool_func, '_tool_name')}")
        if hasattr(tool_func, '_tool_name'):
            print(f"  _tool_name: {tool_func._tool_name}")
        print(f"  Docstring: {tool_func.__doc__[:50]}...")
        
        # Test function call
        try:
            if name == "weather_forecast":
                result = tool_func("Test", 1)
            elif name == "get_cultural_context":
                result = tool_func("Test", "Test")
            elif name == "validate_names_watchlist":
                result = tool_func([{"first_name": "Test", "last_name": "User"}])
            else:
                result = tool_func(sex="Test", age=25, location="Test", occupation="Test", race="Test", religion="Test")
            print(f"  Call result: {result[:50]}...")
        except Exception as e:
            print(f"  Call error: {e}")

if __name__ == "__main__":
    debug_tools()

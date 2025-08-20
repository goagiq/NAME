#!/usr/bin/env python3
"""
MCP Connection Test
Tests the MCP client connection and tool communication.
"""

import subprocess
import sys
import time
from pathlib import Path


def test_mcp_connection() -> bool:
    """Test MCP connection and tool communication."""
    print("Testing MCP Connection and Tools...")
    print("=" * 50)
    
    # Test script content
    test_script = '''
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from mcp.client.streamable_http import streamablehttp_client
    from src.services.ai.strands_mcp_client import MCPClient
    
    async def test_mcp_connection():
        """Test MCP connection and tools."""
        print("Connecting to MCP server...")
        
        try:
            # Create MCP client
            streamable_http_mcp_client = MCPClient(
                lambda: streamablehttp_client("http://localhost:8000/mcp")
            )
            
            print("MCP client created successfully")
            
            # Test connection and list tools
            with streamable_http_mcp_client:
                print("Connected to MCP server")
                
                # List available tools
                tools = streamable_http_mcp_client.list_tools_sync()
                print(f"Found {len(tools)} tools:")
                
                for tool in tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test tool calls if tools are available
                if tools:
                    print("\\nTesting tool calls...")
                    
                    for tool in tools[:2]:  # Test first 2 tools
                        try:
                            print(f"Testing tool: {tool.name}")
                            
                            # Create test arguments based on tool name
                            if "weather" in tool.name.lower():
                                args = {"city": "New York", "days": 3}
                            elif "name" in tool.name.lower():
                                args = {"name": "TestName", "category": "person"}
                            else:
                                args = {"test": "value"}
                            
                            # Call the tool
                            result = await streamable_http_mcp_client.call_tool(
                                tool.name, args
                            )
                            print(f"  Result: {result}")
                            
                        except Exception as e:
                            print(f"  Error calling {tool.name}: {e}")
                else:
                    print("No tools available for testing")
                
                print("\\nMCP connection test completed successfully!")
                return True
                
        except Exception as e:
            print(f"MCP connection failed: {e}")
            return False
    
    # Run the test
    result = asyncio.run(test_mcp_connection())
    print(f"\\nTest result: {'SUCCESS' if result else 'FAILED'}")
    sys.exit(0 if result else 1)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required dependencies:")
    print("pip install mcp")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
'''
    
    # Write test script to temporary file
    test_file = Path("temp_mcp_test.py")
    test_file.write_text(test_script)
    
    try:
        # Clean up any existing temp file
        if test_file.exists():
            test_file.unlink()
        
        # Write the test script
        test_file.write_text(test_script)
        
        # Run the test using virtual environment Python
        venv_python = Path(".venv/Scripts/python.exe")
        
        if not venv_python.exists():
            print("Error: Virtual environment not found!")
            print("Please create a virtual environment first:")
            print("python -m venv .venv")
            print("Then install dependencies:")
            print(".venv\\Scripts\\pip install -e .")
            return False
        
        print("Running MCP connection test...")
        print("-" * 40)
        
        # Run the test
        result = subprocess.run(
            [str(venv_python), str(test_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("MCP test output:", result.stdout)
        if result.stderr:
            print("MCP test errors:", result.stderr)
        
        success = result.returncode == 0
        print(f"MCP connection test: {'SUCCESS' if success else 'FAILED'}")
        
        return success
        
    except subprocess.TimeoutExpired:
        print("MCP connection test timed out")
        return False
    except Exception as e:
        print(f"MCP connection test failed: {e}")
        return False
    finally:
        # Clean up temp file
        if test_file.exists():
            test_file.unlink()


def test_mcp_server_startup() -> bool:
    """Test MCP server startup."""
    print("Testing MCP Server Startup...")
    print("=" * 50)
    
    # MCP server script
    server_script = '''
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool
    import json
    
    # Sample MCP tools
    async def weather_forecast(city: str, days: int = 3) -> str:
        return f"Weather forecast for {city} for the next {days} days: Sunny with occasional clouds."
    
    async def name_validation(name: str, category: str) -> str:
        return f"Validation result for {name} in category {category}: Available"
    
    # Create server
    server = Server("name-generation-mcp")
    
    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return [
            Tool(
                name="weather_forecast",
                description="Get weather forecast for a city",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "days": {"type": "integer", "default": 3}
                    },
                    "required": ["city"]
                }
            ),
            Tool(
                name="name_validation",
                description="Validate a name against databases",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "category": {"type": "string"}
                    },
                    "required": ["name", "category"]
                }
            )
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[dict]:
        if name == "weather_forecast":
            result = await weather_forecast(
                arguments["city"], arguments.get("days", 3)
            )
            return [{"type": "text", "text": result}]
        elif name == "name_validation":
            result = await name_validation(
                arguments["name"], arguments["category"]
            )
            return [{"type": "text", "text": result}]
        else:
            return [{"type": "text", "text": f"Unknown tool: {name}"}]
    
    if __name__ == "__main__":
        print("Starting MCP server...")
        asyncio.run(stdio_server(server))
        
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Server error: {e}")
    sys.exit(1)
'''
    
    # Write server script
    server_file = Path("temp_mcp_server.py")
    
    try:
        # Clean up any existing temp file
        if server_file.exists():
            server_file.unlink()
        
        # Write the server script
        server_file.write_text(server_script)
        
        # Start the server
        print("Starting MCP server...")
        server_process = subprocess.Popen(
            [sys.executable, str(server_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for server to start
        time.sleep(2)
        
        # Check if server is running
        if server_process.poll() is None:
            print("MCP server started successfully")
            
            # Test the server
            test_result = test_mcp_connection()
            
            # Stop the server
            server_process.terminate()
            server_process.wait(timeout=5)
            
            return test_result
        else:
            stdout, stderr = server_process.communicate()
            print("MCP server failed to start:")
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return False
            
    except Exception as e:
        print(f"MCP server test failed: {e}")
        return False
    finally:
        # Clean up temp file
        if server_file.exists():
            server_file.unlink()


def main() -> bool:
    """Run all MCP tests."""
    print("MCP Integration Tests")
    print("=" * 50)
    
    # Test 1: MCP Connection
    print("\n1. Testing MCP Connection...")
    connection_success = test_mcp_connection()
    
    # Test 2: MCP Server Startup
    print("\n2. Testing MCP Server Startup...")
    server_success = test_mcp_server_startup()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print(f"MCP Connection: {'PASS' if connection_success else 'FAIL'}")
    print(f"MCP Server: {'PASS' if server_success else 'FAIL'}")
    
    overall_success = connection_success and server_success
    print(f"\nOverall Result: {'PASS' if overall_success else 'FAIL'}")
    
    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

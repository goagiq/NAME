"""
Real MCP Client
Connects to external MCP servers using proper HTTP requests.
"""

import logging
import requests
import json
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class RealMCPClient:
    """Real MCP Client that connects to external MCP servers via HTTP."""
    
    def __init__(self, mcp_url: str = "http://localhost:8000/mcp"):
        self.mcp_url = mcp_url
        self.session = None
        self.tools_cache: Optional[List[Dict]] = None
        
    def __enter__(self):
        """Context manager entry."""
        try:
            # Create HTTP session
            self.session = requests.Session()
            self.session.headers.update({
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream'
            })
            
            # Test connection
            response = self.session.get(f"{self.mcp_url.replace('/mcp', '')}/health")
            if response.status_code == 200:
                logger.info(f"Connected to MCP server at {self.mcp_url}")
            else:
                logger.warning(f"MCP server responded with status {response.status_code}")
            
            return self
        except Exception as e:
            logger.error(f"MCP client connection failed: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        try:
            if self.session:
                self.session.close()
        except Exception as e:
            logger.error(f"Error closing MCP client: {e}")
        finally:
            self.session = None
            self.tools_cache = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self.__enter__()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.__exit__(exc_type, exc_val, exc_tb)
    
    def list_tools_sync(self) -> List[Dict]:
        """List available tools synchronously."""
        try:
            if self.tools_cache is None:
                if not self.session:
                    raise RuntimeError("Client not initialized. Use context manager.")
                
                # Send JSON-RPC request to list tools
                request_data = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                }
                
                response = self.session.post(self.mcp_url, json=request_data)
                response.raise_for_status()
                
                result = response.json()
                if "result" in result and "tools" in result["result"]:
                    tools = result["result"]["tools"]
                    self.tools_cache = tools
                    logger.info(f"Retrieved {len(tools)} tools from MCP server")
                else:
                    logger.warning("No tools found in MCP response")
                    self.tools_cache = []
            
            return self.tools_cache
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
    
    async def list_tools(self) -> List[Dict]:
        """List available tools asynchronously."""
        return self.list_tools_sync()
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool by name with arguments."""
        try:
            if not self.session:
                raise RuntimeError("Client not initialized. Use context manager.")
            
            # Send JSON-RPC request to call tool
            request_data = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": arguments
                }
            }
            
            response = self.session.post(self.mcp_url, json=request_data)
            response.raise_for_status()
            
            result = response.json()
            if "result" in result:
                logger.info(f"Tool '{name}' called successfully")
                return result["result"]
            else:
                logger.error(f"Tool '{name}' call failed: {result}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to call tool '{name}': {e}")
            return None


class RealMCPToolManager:
    """Real MCP Tool Manager that connects to external MCP servers."""
    
    def __init__(self, mcp_url: str = "http://localhost:8000/mcp"):
        self.mcp_url = mcp_url
        self.client: Optional[RealMCPClient] = None
        self.available_tools: List[Dict] = []
        self.enabled_tools: List[str] = []
        
    def connect(self) -> bool:
        """Connect to MCP server."""
        try:
            logger.info(f"Connecting to MCP server at {self.mcp_url}")
            
            # Test connection by creating a client
            self.client = RealMCPClient(self.mcp_url)
            
            # Try to list tools to verify connection
            with self.client:
                tools = self.client.list_tools_sync()
                if tools:
                    logger.info(f"Successfully connected to MCP server with {len(tools)} tools")
                    self.available_tools = tools
                    return True
                else:
                    logger.warning("Connected to MCP server but no tools available")
                    return False
                    
        except Exception as e:
            logger.error(f"MCP connection failed: {e}")
            return False
    
    def list_tools(self) -> List[Dict]:
        """List available MCP tools."""
        try:
            if not self.client:
                if not self.connect():
                    return []
            
            # Get tools from the server
            with self.client:
                tools = self.client.list_tools_sync()
                self.available_tools = tools
                logger.info(f"Listed {len(tools)} MCP tools from server")
                return tools
                
        except Exception as e:
            logger.error(f"List tools failed: {e}")
            return []
    
    def enable_tool(self, tool_name: str) -> bool:
        """Enable an MCP tool."""
        try:
            # Check if tool exists in available tools
            tool_exists = any(tool.get("name") == tool_name for tool in self.available_tools)
            if not tool_exists:
                logger.warning(f"Tool {tool_name} not found in available tools")
                return False
            
            if tool_name not in self.enabled_tools:
                self.enabled_tools.append(tool_name)
                logger.info(f"Enabled tool: {tool_name}")
            
            return True
        except Exception as e:
            logger.error(f"Enable tool failed: {e}")
            return False
    
    def disable_tool(self, tool_name: str) -> bool:
        """Disable an MCP tool."""
        try:
            if tool_name in self.enabled_tools:
                self.enabled_tools.remove(tool_name)
                logger.info(f"Disabled tool: {tool_name}")
            
            return True
        except Exception as e:
            logger.error(f"Disable tool failed: {e}")
            return False
    
    def get_enabled_tools(self) -> List[str]:
        """Get list of enabled tools."""
        return self.enabled_tools.copy()
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[str]:
        """Call an MCP tool."""
        try:
            if tool_name not in self.enabled_tools:
                logger.warning(f"Tool {tool_name} is not enabled")
                return None
            
            if not self.client:
                if not self.connect():
                    return None
            
            # Call the tool on the server
            with self.client:
                result = await self.client.call_tool(tool_name, arguments)
                return str(result) if result is not None else None
                
        except Exception as e:
            logger.error(f"Call tool failed: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test MCP connection."""
        try:
            return self.connect()
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False


# Convenience function to create a real MCP client
def create_real_mcp_client(mcp_url: str = "http://localhost:8000/mcp") -> RealMCPClient:
    """Create a real MCP client for the given URL."""
    return RealMCPClient(mcp_url)


# Convenience function to create a real MCP tool manager
def create_real_mcp_tool_manager(mcp_url: str = "http://localhost:8000/mcp") -> RealMCPToolManager:
    """Create a real MCP tool manager for the given URL."""
    return RealMCPToolManager(mcp_url)

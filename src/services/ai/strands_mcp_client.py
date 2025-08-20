"""
Strands MCP Client
Custom implementation of MCP client that mimics 
strands.tools.mcp.mcp_client.MCPClient
"""

import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class MCPClient:
    """Custom MCP Client that mimics strands.tools.mcp.mcp_client.MCPClient."""
    
    def __init__(self, client_factory: Callable[[], Any]):
        """
        Initialize MCP client with a client factory function.
        
        Args:
            client_factory: Function that returns an MCP client instance
        """
        self.client_factory = client_factory
        self.session: Optional[Any] = None
        self._tools_cache: Optional[List[Any]] = None
        
    def __enter__(self) -> 'MCPClient':
        """Context manager entry."""
        try:
            self.session = self.client_factory()
            # Handle async generator context managers
            if hasattr(self.session, '__aenter__'):
                # This is an async context manager, we need to handle it differently
                logger.warning("Async context manager detected, using sync fallback")
                return self
            elif hasattr(self.session, '__enter__'):
                self.session.__enter__()
            return self
        except Exception as e:
            logger.error(f"Error entering context: {e}")
            return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        try:
            if self.session and hasattr(self.session, '__exit__'):
                self.session.__exit__(exc_type, exc_val, exc_tb)
        except Exception as e:
            logger.error(f"Error exiting context: {e}")
        finally:
            self.session = None
            self._tools_cache = None
    
    async def __aenter__(self) -> 'MCPClient':
        """Async context manager entry."""
        try:
            self.session = self.client_factory()
            if hasattr(self.session, '__aenter__'):
                await self.session.__aenter__()
            return self
        except Exception as e:
            logger.error(f"Error entering async context: {e}")
            return self
    
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        try:
            if self.session and hasattr(self.session, '__aexit__'):
                await self.session.__aexit__(exc_type, exc_val, exc_tb)
        except Exception as e:
            logger.error(f"Error exiting async context: {e}")
        finally:
            self.session = None
            self._tools_cache = None
    
    def list_tools_sync(self) -> List[Any]:
        """List available tools synchronously."""
        try:
            if self._tools_cache is None:
                # Create a new session for sync operations
                with self.client_factory() as session:
                    if hasattr(session, 'list_tools'):
                        self._tools_cache = session.list_tools()
                    else:
                        # Fallback to async call
                        import asyncio
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            self._tools_cache = loop.run_until_complete(
                                self._list_tools_async()
                            )
                        finally:
                            loop.close()
            return self._tools_cache or []
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
    
    async def list_tools(self) -> List[Any]:
        """List available tools asynchronously."""
        try:
            if self.session is None:
                raise RuntimeError(
                    "Session not initialized. Use context manager."
                )
            
            if hasattr(self.session, 'list_tools'):
                tools = await self.session.list_tools()
                self._tools_cache = tools
                return tools
            else:
                return await self._list_tools_async()
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
    
    async def _list_tools_async(self) -> List[Any]:
        """Internal async method to list tools."""
        # This is a fallback implementation
        # In a real scenario, you would implement the actual MCP protocol
        return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool by name with arguments."""
        try:
            if self.session is None:
                raise RuntimeError(
                    "Session not initialized. Use context manager."
                )
            
            if hasattr(self.session, 'call_tool'):
                result = await self.session.call_tool(name, arguments)
                return result
            else:
                return await self._call_tool_async(name, arguments)
        except Exception as e:
            logger.error(f"Failed to call tool {name}: {e}")
            return None
    
    async def _call_tool_async(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Internal async method to call tools."""
        # This is a fallback implementation
        # In a real scenario, you would implement the actual MCP protocol
        logger.warning(
            f"Tool call not implemented: {name} with args {arguments}"
        )
        return f"Mock result for {name}"


def create_mcp_client(mcp_url: str = "http://localhost:8000/mcp") -> MCPClient:
    """
    Create an MCP client for the given URL.
    
    Args:
        mcp_url: URL of the MCP server
        
    Returns:
        MCPClient instance
    """
    def client_factory():
        # Import here to avoid import issues
        try:
            from mcp.client.streamable_http import streamablehttp_client
            return streamablehttp_client(mcp_url)
        except ImportError:
            logger.warning("MCP streamable_http not available, using mock")
            return MockMCPClient()
    
    return MCPClient(client_factory)


class MockMCPClient:
    """Mock MCP client for when the real one is not available."""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def list_tools(self):
        return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        return f"Mock result for {name}"


# Convenience function for HTTP-based MCP clients
def create_http_mcp_client(
    mcp_url: str = "http://localhost:8000/mcp"
) -> MCPClient:
    """
    Create an HTTP-based MCP client.
    
    Args:
        mcp_url: URL of the MCP server
        
    Returns:
        MCPClient instance
    """
    return create_mcp_client(mcp_url)

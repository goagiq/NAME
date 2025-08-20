"""
Test MCP Integration
Tests for MCP client connections and tool management.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

from src.services.ai.mcp_integration import MCPToolManager


class TestMCPToolManager:
    """Test MCP Tool Manager functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.mcp_manager = MCPToolManager("http://localhost:8000/mcp")
    
    def test_initialization(self):
        """Test MCP manager initialization."""
        assert self.mcp_manager.mcp_url == "http://localhost:8000/mcp"
        assert self.mcp_manager.client is None
        assert self.mcp_manager.available_tools == []
        assert self.mcp_manager.enabled_tools == []
    
    @patch('src.services.ai.mcp_integration.MCPClient')
    def test_connect_success(self, mock_mcp_client):
        """Test successful MCP connection."""
        mock_client = Mock()
        mock_mcp_client.return_value = mock_client
        self.mcp_manager.client = mock_client
        
        result = self.mcp_manager.connect()
        assert result is True
    
    @patch('src.services.ai.mcp_integration.MCPClient')
    def test_connect_failure(self, mock_mcp_client):
        """Test failed MCP connection."""
        mock_mcp_client.side_effect = Exception("Connection failed")
        
        result = self.mcp_manager.connect()
        assert result is False
    
    @patch('src.services.ai.mcp_integration.MCPClient')
    def test_list_tools(self, mock_mcp_client):
        """Test listing MCP tools."""
        mock_client = Mock()
        mock_tool = Mock()
        mock_tool.name = "test_tool"
        mock_tool.description = "Test tool description"
        mock_client.list_tools_sync.return_value = [mock_tool]
        
        self.mcp_manager.client = mock_client
        
        with patch.object(self.mcp_manager, 'connect', return_value=True):
            tools = self.mcp_manager.list_tools()
        
        assert len(tools) == 1
        assert tools[0]["name"] == "test_tool"
        assert tools[0]["description"] == "Test tool description"
        assert tools[0]["enabled"] is False
    
    def test_enable_tool(self):
        """Test enabling a tool."""
        self.mcp_manager.available_tools = [{"name": "test_tool"}]
        
        result = self.mcp_manager.enable_tool("test_tool")
        assert result is True
        assert "test_tool" in self.mcp_manager.enabled_tools
    
    def test_enable_nonexistent_tool(self):
        """Test enabling a non-existent tool."""
        self.mcp_manager.available_tools = [{"name": "existing_tool"}]
        
        result = self.mcp_manager.enable_tool("nonexistent_tool")
        assert result is False
    
    def test_disable_tool(self):
        """Test disabling a tool."""
        self.mcp_manager.enabled_tools = ["test_tool"]
        
        result = self.mcp_manager.disable_tool("test_tool")
        assert result is True
        assert "test_tool" not in self.mcp_manager.enabled_tools
    
    def test_disable_nonexistent_tool(self):
        """Test disabling a non-existent tool."""
        result = self.mcp_manager.disable_tool("nonexistent_tool")
        assert result is False
    
    def test_get_enabled_tools(self):
        """Test getting enabled tools list."""
        self.mcp_manager.enabled_tools = ["tool1", "tool2"]
        
        enabled_tools = self.mcp_manager.get_enabled_tools()
        assert enabled_tools == ["tool1", "tool2"]
        # Ensure it returns a copy
        assert enabled_tools is not self.mcp_manager.enabled_tools
    
    @pytest.mark.asyncio
    async def test_call_tool_success(self):
        """Test successful tool call."""
        mock_client = Mock()
        mock_client.call_tool.return_value = "Tool result"
        self.mcp_manager.client = mock_client
        self.mcp_manager.enabled_tools = ["test_tool"]
        
        with patch.object(self.mcp_manager, 'connect', return_value=True):
            result = await self.mcp_manager.call_tool("test_tool", {"param": "value"})
        
        assert result == "Tool result"
    
    @pytest.mark.asyncio
    async def test_call_disabled_tool(self):
        """Test calling a disabled tool."""
        self.mcp_manager.enabled_tools = ["enabled_tool"]
        
        result = await self.mcp_manager.call_tool("disabled_tool", {})
        assert result is None
    
    def test_test_connection_success(self):
        """Test successful connection test."""
        with patch.object(self.mcp_manager, 'list_tools', return_value=[{"name": "tool"}]):
            result = self.mcp_manager.test_connection()
            assert result is True
    
    def test_test_connection_failure(self):
        """Test failed connection test."""
        with patch.object(self.mcp_manager, 'list_tools', side_effect=Exception("Connection failed")):
            result = self.mcp_manager.test_connection()
            assert result is False


if __name__ == "__main__":
    pytest.main([__file__])

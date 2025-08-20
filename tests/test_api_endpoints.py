"""
Test API Endpoints
Tests for FastAPI endpoints and API functionality.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.api.server import create_app


class TestAPIEndpoints:
    """Test API endpoints functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.app = create_app()
        self.client = TestClient(self.app)
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "name-generation-system"
    
    def test_get_categories(self):
        """Test categories endpoint."""
        response = self.client.get("/api/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        categories = data["categories"]
        
        expected_categories = [
            "person", "project", "code", "mission", "place"
        ]
        
        for category in categories:
            assert category["id"] in expected_categories
            assert "name" in category
            assert "description" in category
    
    @patch('src.api.server.StrandsAgentManager')
    def test_generate_names_success(self, mock_strands_manager):
        """Test successful name generation."""
        mock_manager = Mock()
        mock_manager.generate_names_with_swarm.return_value = "Generated names"
        mock_strands_manager.return_value = mock_manager
        
        request_data = {
            "category": "person",
            "parameters": {
                "sex": "male",
                "region": "United States",
                "age": "25-35"
            }
        }
        
        response = self.client.post("/api/names/generate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["category"] == "person"
        assert data["parameters"] == request_data["parameters"]
        assert data["result"] == "Generated names"
    
    @patch('src.api.server.StrandsAgentManager')
    def test_generate_names_failure(self, mock_strands_manager):
        """Test failed name generation."""
        mock_manager = Mock()
        mock_manager.generate_names_with_swarm.side_effect = Exception("Generation failed")
        mock_strands_manager.return_value = mock_manager
        
        request_data = {
            "category": "person",
            "parameters": {"age": "25"}
        }
        
        response = self.client.post("/api/names/generate", json=request_data)
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
    
    @patch('src.api.server.MCPToolManager')
    def test_validate_name_success(self, mock_mcp_manager):
        """Test successful name validation."""
        mock_manager = Mock()
        mock_manager.call_tool.return_value = "Validation result"
        mock_mcp_manager.return_value = mock_manager
        
        request_data = {
            "name": "TestName",
            "category": "person"
        }
        
        response = self.client.post("/api/names/validate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["name"] == "TestName"
        assert data["category"] == "person"
        assert data["validation_result"] == "Validation result"
    
    @patch('src.api.server.MCPToolManager')
    def test_validate_name_failure(self, mock_mcp_manager):
        """Test failed name validation."""
        mock_manager = Mock()
        mock_manager.call_tool.side_effect = Exception("Validation failed")
        mock_mcp_manager.return_value = mock_manager
        
        request_data = {
            "name": "TestName",
            "category": "person"
        }
        
        response = self.client.post("/api/names/validate", json=request_data)
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
    
    @patch('src.api.server.MCPToolManager')
    def test_list_mcp_tools(self, mock_mcp_manager):
        """Test listing MCP tools."""
        mock_manager = Mock()
        mock_manager.list_tools.return_value = [
            {"name": "tool1", "description": "Tool 1", "enabled": True},
            {"name": "tool2", "description": "Tool 2", "enabled": False}
        ]
        mock_mcp_manager.return_value = mock_manager
        
        response = self.client.get("/api/mcp/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert len(data["tools"]) == 2
    
    @patch('src.api.server.MCPToolManager')
    def test_manage_mcp_tool_enable(self, mock_mcp_manager):
        """Test enabling MCP tool."""
        mock_manager = Mock()
        mock_manager.enable_tool.return_value = True
        mock_mcp_manager.return_value = mock_manager
        
        request_data = {
            "tool_name": "test_tool",
            "action": "enable"
        }
        
        response = self.client.post("/api/mcp/tools/manage", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tool_name"] == "test_tool"
        assert data["action"] == "enable"
    
    @patch('src.api.server.MCPToolManager')
    def test_manage_mcp_tool_disable(self, mock_mcp_manager):
        """Test disabling MCP tool."""
        mock_manager = Mock()
        mock_manager.disable_tool.return_value = True
        mock_mcp_manager.return_value = mock_manager
        
        request_data = {
            "tool_name": "test_tool",
            "action": "disable"
        }
        
        response = self.client.post("/api/mcp/tools/manage", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tool_name"] == "test_tool"
        assert data["action"] == "disable"
    
    def test_manage_mcp_tool_invalid_action(self):
        """Test invalid action for MCP tool management."""
        request_data = {
            "tool_name": "test_tool",
            "action": "invalid"
        }
        
        response = self.client.post("/api/mcp/tools/manage", json=request_data)
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    @patch('src.api.server.MCPToolManager')
    def test_get_enabled_tools(self, mock_mcp_manager):
        """Test getting enabled tools."""
        mock_manager = Mock()
        mock_manager.get_enabled_tools.return_value = ["tool1", "tool2"]
        mock_mcp_manager.return_value = mock_manager
        
        response = self.client.get("/api/mcp/tools/enabled")
        assert response.status_code == 200
        data = response.json()
        assert "enabled_tools" in data
        assert data["enabled_tools"] == ["tool1", "tool2"]
    
    @patch('src.api.server.StrandsAgentManager')
    def test_list_agents(self, mock_strands_manager):
        """Test listing agents."""
        mock_manager = Mock()
        mock_manager.list_agents.return_value = ["agent1", "agent2"]
        mock_manager.list_swarms.return_value = ["swarm1"]
        mock_strands_manager.return_value = mock_manager
        
        response = self.client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert "swarms" in data
        assert data["agents"] == ["agent1", "agent2"]
        assert data["swarms"] == ["swarm1"]
    
    @patch('src.api.server.MCPToolManager')
    def test_test_mcp_connection_success(self, mock_mcp_manager):
        """Test successful MCP connection test."""
        mock_manager = Mock()
        mock_manager.test_connection.return_value = True
        mock_mcp_manager.return_value = mock_manager
        
        response = self.client.post("/api/test/mcp")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "message" in data
    
    @patch('src.api.server.MCPToolManager')
    def test_test_mcp_connection_failure(self, mock_mcp_manager):
        """Test failed MCP connection test."""
        mock_manager = Mock()
        mock_manager.test_connection.return_value = False
        mock_mcp_manager.return_value = mock_manager
        
        response = self.client.post("/api/test/mcp")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "message" in data


if __name__ == "__main__":
    pytest.main([__file__])

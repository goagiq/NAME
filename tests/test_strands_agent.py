"""
Test Strands Agent
Tests for Strands agent management and swarm functionality.
"""

import pytest
from unittest.mock import Mock, patch

from src.services.ai.strands_agent import StrandsAgentManager


class TestStrandsAgentManager:
    """Test Strands Agent Manager functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.agent_manager = StrandsAgentManager("http://localhost:11434")
    
    def test_initialization(self):
        """Test agent manager initialization."""
        assert self.agent_manager.ollama_host == "http://localhost:11434"
        assert self.agent_manager.agents == {}
        assert self.agent_manager.swarms == {}
        assert "person" in self.agent_manager.ai_models
        assert "project" in self.agent_manager.ai_models
        assert "code" in self.agent_manager.ai_models
    
    def test_ai_models_configuration(self):
        """Test AI models configuration."""
        expected_models = {
            "person": "llama3",
            "project": "llama3", 
            "code": "codellama",
            "mission": "llama2",
            "place": "llama3"
        }
        assert self.agent_manager.ai_models == expected_models
    
    @patch('src.services.ai.strands_agent.OllamaModel')
    @patch('src.services.ai.strands_agent.Agent')
    def test_create_agent(self, mock_agent, mock_ollama_model):
        """Test creating a Strands agent."""
        mock_model = Mock()
        mock_ollama_model.return_value = mock_model
        
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        agent = self.agent_manager.create_agent("person")
        
        assert agent == mock_agent_instance
        assert "person" in self.agent_manager.agents
        mock_ollama_model.assert_called_once_with(
            host="http://localhost:11434",
            model_id="llama3"
        )
    
    @patch('src.services.ai.strands_agent.Agent')
    def test_create_specialized_agents(self, mock_agent):
        """Test creating specialized agents."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        specialized_agents = self.agent_manager.create_specialized_agents()
        
        expected_agents = [
            "cultural_analyst",
            "linguistic_expert", 
            "validation_specialist",
            "creative_director"
        ]
        
        assert len(specialized_agents) == 4
        for agent_name in expected_agents:
            assert agent_name in specialized_agents
            assert agent_name in self.agent_manager.agents
    
    @patch('src.services.ai.strands_agent.Swarm')
    @patch.object(StrandsAgentManager, 'create_specialized_agents')
    def test_create_name_generation_swarm(self, mock_create_agents, mock_swarm):
        """Test creating name generation swarm."""
        mock_agents = {
            "cultural_analyst": Mock(),
            "linguistic_expert": Mock(),
            "validation_specialist": Mock(),
            "creative_director": Mock()
        }
        mock_create_agents.return_value = mock_agents
        
        mock_swarm_instance = Mock()
        mock_swarm.return_value = mock_swarm_instance
        
        swarm = self.agent_manager.create_name_generation_swarm()
        
        assert swarm == mock_swarm_instance
        assert "name_generation" in self.agent_manager.swarms
        mock_swarm.assert_called_once()
    
    @patch.object(StrandsAgentManager, 'create_name_generation_swarm')
    def test_generate_names_with_swarm(self, mock_create_swarm):
        """Test generating names with swarm."""
        mock_swarm = Mock()
        mock_result = Mock()
        mock_result.status = "completed"
        mock_swarm.return_value = mock_result
        mock_create_swarm.return_value = mock_swarm
        
        self.agent_manager.swarms["name_generation"] = mock_swarm
        
        result = self.agent_manager.generate_names_with_swarm("person", {"age": "25"})
        
        assert result == str(mock_result)
        mock_swarm.assert_called_once()
    
    def test_get_agent(self):
        """Test getting an existing agent."""
        mock_agent = Mock()
        self.agent_manager.agents["person"] = mock_agent
        
        agent = self.agent_manager.get_agent("person")
        assert agent == mock_agent
    
    def test_get_nonexistent_agent(self):
        """Test getting a non-existent agent."""
        agent = self.agent_manager.get_agent("nonexistent")
        assert agent is None
    
    def test_list_agents(self):
        """Test listing all agents."""
        self.agent_manager.agents = {"agent1": Mock(), "agent2": Mock()}
        
        agents = self.agent_manager.list_agents()
        assert agents == ["agent1", "agent2"]
    
    def test_list_swarms(self):
        """Test listing all swarms."""
        self.agent_manager.swarms = {"swarm1": Mock(), "swarm2": Mock()}
        
        swarms = self.agent_manager.list_swarms()
        assert swarms == ["swarm1", "swarm2"]


if __name__ == "__main__":
    pytest.main([__file__])

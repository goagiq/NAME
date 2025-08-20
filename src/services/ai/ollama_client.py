"""
Ollama Client
Integration with local LLM models via Ollama server.
"""

import asyncio
import json
import logging
import requests
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama server."""
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.base_url = f"{host}/api"
        self.available_models: List[str] = []
        
    def test_connection(self) -> bool:
        """Test connection to Ollama server."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info("Successfully connected to Ollama server")
                return True
            else:
                logger.warning(f"Ollama server responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama connection failed: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """List available models."""
        try:
            response = requests.get(f"{self.base_url}/tags")
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                self.available_models = models
                logger.info(f"Found {len(models)} Ollama models: {models}")
                return models
            else:
                logger.error(f"Failed to list models: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def generate_text(self, model: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate text using specified model."""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                logger.error(f"Generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None
    
    async def generate_text_async(self, model: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate text asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.generate_text, model, prompt, **kwargs
        )
    
    def pull_model(self, model: str) -> bool:
        """Pull a model from Ollama registry."""
        try:
            payload = {"name": model}
            response = requests.post(
                f"{self.base_url}/pull",
                json=payload,
                timeout=300  # 5 minutes for model download
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully pulled model: {model}")
                return True
            else:
                logger.error(f"Failed to pull model {model}: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error pulling model {model}: {e}")
            return False


class OllamaModelManager:
    """Manager for Ollama models with caching and fallbacks."""
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.client = OllamaClient(host)
        self.model_cache: Dict[str, str] = {}
        
        # Default models for different categories
        self.default_models = {
            "person": "llama3",
            "project": "llama3",
            "code": "codellama",
            "mission": "llama2",
            "place": "llama3"
        }
    
    def get_model_for_category(self, category: str) -> str:
        """Get the appropriate model for a category."""
        return self.default_models.get(category, "llama3")
    
    def ensure_model_available(self, model: str) -> bool:
        """Ensure a model is available, pulling if necessary."""
        if not self.client.test_connection():
            logger.error("Ollama server not available")
            return False
        
        models = self.client.list_models()
        if model in models:
            return True
        
        logger.info(f"Model {model} not found, attempting to pull...")
        return self.client.pull_model(model)
    
    def generate_name_suggestions(self, category: str, parameters: Dict[str, Any]) -> List[str]:
        """Generate name suggestions using appropriate model."""
        model = self.get_model_for_category(category)
        
        if not self.ensure_model_available(model):
            logger.error(f"Model {model} not available")
            return []
        
        # Create prompt based on category and parameters
        prompt = self._create_name_prompt(category, parameters)
        
        # Generate response
        response = self.client.generate_text(model, prompt)
        if not response:
            return []
        
        # Parse response into name suggestions
        return self._parse_name_suggestions(response)
    
    def _create_name_prompt(self, category: str, parameters: Dict[str, Any]) -> str:
        """Create a prompt for name generation."""
        base_prompts = {
            "person": "Generate 5 culturally appropriate person names based on these parameters: {params}. Return only the names, one per line.",
            "project": "Generate 5 creative project names based on these parameters: {params}. Return only the names, one per line.",
            "code": "Generate 5 software code names based on these parameters: {params}. Return only the names, one per line.",
            "mission": "Generate 5 mission operation names based on these parameters: {params}. Return only the names, one per line.",
            "place": "Generate 5 place names based on these parameters: {params}. Return only the names, one per line."
        }
        
        prompt_template = base_prompts.get(category, base_prompts["project"])
        return prompt_template.format(params=parameters)
    
    def _parse_name_suggestions(self, response: str) -> List[str]:
        """Parse response into list of name suggestions."""
        lines = response.strip().split('\n')
        names = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 1:
                # Clean up the name (remove numbers, bullets, etc.)
                name = line.split('.')[-1].strip() if '.' in line else line
                name = name.lstrip('0123456789.-* ').strip()
                if name:
                    names.append(name)
        
        return names[:5]  # Return max 5 names


# Convenience function
def create_ollama_manager(host: str = "http://localhost:11434") -> OllamaModelManager:
    """Create an Ollama model manager."""
    return OllamaModelManager(host)

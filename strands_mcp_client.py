#!/usr/bin/env python3
"""
Strands-compatible MCP Client
Integrates with the Flask MCP server to provide tools for Strands agents
"""

import requests
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class StrandsMCPClient:
    """MCP client for Strands integration."""
    
    def __init__(self, mcp_url: str = "http://localhost:8500"):
        self.mcp_url = mcp_url
        self.base_url = f"{mcp_url}/mcp"
        self.tools_url = f"{mcp_url}/mcp/tools"
    
    def list_tools(self) -> List[Dict]:
        """List available MCP tools."""
        try:
            response = requests.get(self.tools_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('tools', [])
        except Exception as e:
            logger.error(f"Error listing MCP tools: {e}")
            return []
    
    def call_tool(self, tool_name: str, tool_input: Dict) -> Dict:
        """Call an MCP tool."""
        try:
            payload = {
                "name": tool_name,
                "input": tool_input
            }
            
            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            return {
                "status": "error",
                "content": [{"text": f"Error calling tool: {str(e)}"}]
            }
    
    def generate_cultural_names(self, **kwargs) -> Dict:
        """Generate culturally appropriate names."""
        return self.call_tool("generate_cultural_names", kwargs)
    
    def validate_names_watchlist(self, names: List[Dict]) -> Dict:
        """Validate names against watchlist."""
        return self.call_tool("validate_names_watchlist", {"names": names})
    
    def get_cultural_context(self, region: str, religion: str) -> Dict:
        """Get cultural context for a region and religion."""
        return self.call_tool("get_cultural_context", {
            "region": region,
            "religion": religion
        })
    
    def health_check(self) -> bool:
        """Check if MCP server is healthy."""
        try:
            response = requests.get(self.mcp_url.replace('/mcp', ''), timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"MCP server health check failed: {e}")
            return False

# Example usage with Strands
def create_strands_mcp_tools():
    """Create Strands-compatible MCP tools."""
    from strands import tool
    
    mcp_client = StrandsMCPClient()
    
    @tool
    def generate_names_with_mcp(sex: str, age: int, location: str, 
                               race: str, religion: str, 
                               birth_year: int = 1999) -> str:
        """Generate culturally appropriate names using MCP tools.
        
        Args:
            sex: Sex of the person
            age: Age of the person
            location: Geographic location
            race: Race/Ethnicity
            religion: Religion
            birth_year: Birth year
        """
        result = mcp_client.generate_cultural_names(
            sex=sex, age=age, location=location, 
            race=race, religion=religion, birth_year=birth_year
        )
        
        if result.get('status') == 'success':
            content = result.get('content', [])
            for item in content:
                if 'json' in item:
                    identities = item['json'].get('identities', [])
                    names = []
                    for identity in identities:
                        name = f"{identity.get('first_name', '')} {identity.get('last_name', '')}"
                        names.append(name)
                    return f"Generated names: {', '.join(names)}"
                elif 'text' in item:
                    return item['text']
        
        return "Failed to generate names"
    
    @tool
    def validate_names_mcp(names: List[str]) -> str:
        """Validate names against watchlist using MCP tools.
        
        Args:
            names: List of names to validate
        """
        # Convert names to the expected format
        name_objects = []
        for name in names:
            parts = name.split()
            if len(parts) >= 2:
                name_objects.append({
                    "first_name": parts[0],
                    "last_name": " ".join(parts[1:])
                })
        
        result = mcp_client.validate_names_watchlist(name_objects)
        
        if result.get('status') == 'success':
            content = result.get('content', [])
            for item in content:
                if 'json' in item:
                    validation_results = item['json'].get('validation_results', [])
                    safe_names = []
                    flagged_names = []
                    
                    for validation in validation_results:
                        if validation.get('is_safe'):
                            safe_names.append(validation.get('name', ''))
                        else:
                            flagged_names.append(validation.get('name', ''))
                    
                    response = f"Safe names: {', '.join(safe_names)}"
                    if flagged_names:
                        response += f"\nFlagged names: {', '.join(flagged_names)}"
                    return response
                elif 'text' in item:
                    return item['text']
        
        return "Failed to validate names"
    
    @tool
    def get_cultural_context_mcp(region: str, religion: str) -> str:
        """Get cultural context for a region and religion using MCP tools.
        
        Args:
            region: Geographic region
            religion: Religion
        """
        result = mcp_client.get_cultural_context(region, religion)
        
        if result.get('status') == 'success':
            content = result.get('content', [])
            for item in content:
                if 'json' in item:
                    cultural_context = item['json'].get('cultural_context', {})
                    return f"Cultural context for {region} {religion}: {cultural_context.get('naming_patterns', 'No patterns available')}"
                elif 'text' in item:
                    return item['text']
        
        return f"Failed to get cultural context for {region} {religion}"
    
    return [generate_names_with_mcp, validate_names_mcp, get_cultural_context_mcp]

# Test the MCP client
def test_mcp_client():
    """Test the MCP client functionality."""
    client = StrandsMCPClient()
    
    print("Testing MCP Client...")
    
    # Health check
    if not client.health_check():
        print("❌ MCP server is not healthy")
        return False
    
    print("✅ MCP server is healthy")
    
    # List tools
    tools = client.list_tools()
    print(f"✅ Found {len(tools)} MCP tools:")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # Test name generation
    print("\nTesting name generation...")
    result = client.generate_cultural_names(
        sex="Female",
        age=25,
        location="Morocco",
        race="Moroccan",
        religion="Christian",
        birth_year=1999
    )
    
    if result.get('status') == 'success':
        print("✅ Name generation successful")
        content = result.get('content', [])
        for item in content:
            if 'json' in item:
                identities = item['json'].get('identities', [])
                for identity in identities:
                    name = f"{identity.get('first_name', '')} {identity.get('last_name', '')}"
                    print(f"  Generated: {name}")
    else:
        print("❌ Name generation failed")
    
    return True

if __name__ == "__main__":
    test_mcp_client()

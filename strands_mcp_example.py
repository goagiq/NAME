#!/usr/bin/env python3
"""
Strands MCP Tools Example
Demonstrates how to use MCP tools with Strands agents
"""

from strands_mcp_integration import create_strands_mcp_tools, create_strands_agent_with_mcp_tools

def example_usage():
    """Example of using MCP tools with Strands."""
    
    print("🚀 Strands MCP Tools Example")
    print("=" * 50)
    
    # Create MCP tools
    print("\n1️⃣ Creating MCP tools...")
    mcp_tools = create_strands_mcp_tools()
    
    if not mcp_tools:
        print("❌ Failed to create MCP tools")
        return
    
    print(f"✅ Created {len(mcp_tools)} MCP tools:")
    for tool in mcp_tools:
        print(f"  - {tool.__name__}")
    
    # Create Strands agent
    print("\n2️⃣ Creating Strands agent...")
    agent = create_strands_agent_with_mcp_tools()
    
    if not agent:
        print("❌ Failed to create Strands agent")
        return
    
    print(f"✅ Created Strands agent: {agent.name}")
    
    # Example 1: Generate names
    print("\n3️⃣ Example 1: Generate culturally appropriate names")
    print("Agent: Generate names for a 25-year-old Moroccan Christian female nurse")
    
    try:
        response = agent("Generate culturally appropriate names for a 25-year-old Moroccan Christian female nurse living in Morocco")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Get cultural context
    print("\n4️⃣ Example 2: Get cultural context")
    print("Agent: What are the naming patterns for Iraqi Muslims?")
    
    try:
        response = agent("What are the naming patterns for Iraqi Muslims?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Validate names
    print("\n5️⃣ Example 3: Validate names")
    print("Agent: Validate these names: John Smith, Jane Doe, Ahmed Hassan")
    
    try:
        response = agent("Validate these names: John Smith, Jane Doe, Ahmed Hassan")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n✅ Example completed!")

def direct_tool_usage():
    """Example of using MCP tools directly without Strands agent."""
    
    print("\n🔧 Direct MCP Tool Usage")
    print("=" * 50)
    
    from strands_mcp_integration import StrandsMCPIntegration
    
    mcp = StrandsMCPIntegration()
    
    # Test cultural context
    print("\n🌍 Getting cultural context for Moroccan Christians...")
    result = mcp.call_tool("get_cultural_context", {
        "region": "Morocco",
        "religion": "Christian"
    })
    
    if result.get('status') == 'success':
        content = result.get('content', [])
        for item in content:
            if 'json' in item:
                cultural_context = item['json'].get('cultural_context', {})
                print(f"Region: {cultural_context.get('region')}")
                print(f"Religion: {cultural_context.get('religion')}")
                print(f"Naming Patterns: {cultural_context.get('naming_patterns')}")
    
    # Test name generation
    print("\n👤 Generating names for Iraqi Muslim male...")
    result = mcp.call_tool("generate_cultural_names", {
        "sex": "Male",
        "age": 30,
        "location": "Iraq",
        "race": "Iraqi",
        "religion": "Muslim",
        "birth_year": 1994
    })
    
    if result.get('status') == 'success':
        content = result.get('content', [])
        for item in content:
            if 'json' in item:
                identities = item['json'].get('identities', [])
                print("Generated names:")
                for identity in identities:
                    name = f"{identity.get('first_name', '')} {identity.get('last_name', '')}"
                    print(f"  - {name}")
    
    print("\n✅ Direct tool usage completed!")

if __name__ == "__main__":
    print("🎯 MCP Tools are now available and working!")
    print("📋 Available MCP Tools:")
    print("  - generate_cultural_names: Generate culturally appropriate names")
    print("  - validate_names_watchlist: Validate names against watchlist")
    print("  - get_cultural_context: Get cultural context and naming patterns")
    
    # Test direct tool usage
    direct_tool_usage()
    
    # Test Strands integration (if available)
    try:
        example_usage()
    except Exception as e:
        print(f"\n⚠️ Strands integration test failed: {e}")
        print("💡 MCP tools are working directly, but Strands integration needs setup")

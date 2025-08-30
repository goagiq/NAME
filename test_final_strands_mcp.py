#!/usr/bin/env python3
"""
Final Test for Strands MCP Integration
Verifies that the MCP server is working correctly with real Strands library
"""

import requests
import json
import sys

def test_mcp_discovery():
    """Test MCP tools discovery."""
    print("🔍 Testing MCP Tools Discovery...")
    
    try:
        response = requests.get("http://127.0.0.1:8500/mcp", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        tools = data.get('tools', [])
        print(f"✅ Found {len(tools)} tools:")
        
        for tool in tools:
            print(f"  📋 {tool['name']}")
            print(f"     Description: {tool['description'][:100]}...")
        
        return len(tools) == 3  # Should have 3 tools
        
    except Exception as e:
        print(f"❌ MCP discovery failed: {e}")
        return False

def test_tool_execution():
    """Test tool execution."""
    print("\n🔧 Testing Tool Execution...")
    
    # Test get_cultural_context
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_cultural_context",
                "arguments": {
                    "region": "Asia",
                    "religion": "Buddhism"
                }
            }
        }
        
        response = requests.post("http://127.0.0.1:8500/mcp", 
                               json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "result" in result:
            print("✅ get_cultural_context tool working")
            return True
        else:
            print(f"❌ get_cultural_context failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        return False

def test_name_generation():
    """Test name generation tool."""
    print("\n👤 Testing Name Generation...")
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "generate_cultural_names",
                "arguments": {
                    "sex": "male",
                    "age": 25,
                    "location": "Japan",
                    "occupation": "engineer",
                    "race": "Asian",
                    "religion": "Buddhism",
                    "birth_year": 1999
                }
            }
        }
        
        response = requests.post("http://127.0.0.1:8500/mcp", 
                               json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "result" in result:
            print("✅ generate_cultural_names tool working")
            return True
        else:
            print(f"❌ generate_cultural_names failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Name generation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Final Strands MCP Integration Test")
    print("=" * 50)
    
    tests = [
        test_mcp_discovery,
        test_tool_execution,
        test_name_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP server is working correctly with Strands.")
        return 0
    else:
        print("❌ Some tests failed. Please check the MCP server.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

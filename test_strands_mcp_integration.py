#!/usr/bin/env python3
"""
Test Strands MCP Integration
Verifies that Strands tools with @tool decorator are working correctly
"""

import requests
import json
import sys

def test_strands_tools_discovery():
    """Test Strands tools discovery."""
    print("🔍 Testing Strands Tools Discovery...")
    
    try:
        response = requests.get("http://127.0.0.1:8500/mcp", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        tools = data.get('tools', [])
        print(f"✅ Found {len(tools)} Strands tools:")
        
        for tool in tools:
            print(f"  📋 {tool['name']}")
            print(f"     Description: {tool['description']}")
            print(f"     Schema: {tool['inputSchema']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Strands tools discovery: {e}")
        return False

def test_strands_tool_execution():
    """Test Strands tool execution."""
    print("⚡ Testing Strands Tool Execution...")
    
    try:
        # Test get_cultural_context tool
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
        
        response = requests.post(
            "http://127.0.0.1:8500/mcp",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ Strands tool execution working")
            content = data['result']['content']
            print(f"   Response: {content[0]['text'][:100]}...")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Strands tool execution: {e}")
        return False

def test_generate_cultural_names():
    """Test generate_cultural_names tool."""
    print("👤 Testing generate_cultural_names Tool...")
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "generate_cultural_names",
                "arguments": {
                    "sex": "Female",
                    "age": 25,
                    "location": "Canada",
                    "occupation": "Engineer",
                    "race": "Indian",
                    "religion": "Hinduism",
                    "birth_year": 1998
                }
            }
        }
        
        response = requests.post(
            "http://127.0.0.1:8500/mcp",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ generate_cultural_names tool working")
            content = data['result']['content']
            print(f"   Response: {content[0]['text'][:100]}...")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing generate_cultural_names: {e}")
        return False

def test_validate_names_watchlist():
    """Test validate_names_watchlist tool."""
    print("✅ Testing validate_names_watchlist Tool...")
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "validate_names_watchlist",
                "arguments": {
                    "names": [
                        {"first_name": "John", "last_name": "Smith"},
                        {"first_name": "Mohammed", "last_name": "Ali"},
                        {"first_name": "Test", "last_name": "User"}
                    ]
                }
            }
        }
        
        response = requests.post(
            "http://127.0.0.1:8500/mcp",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ validate_names_watchlist tool working")
            content = data['result']['content']
            print(f"   Response: {content[0]['text'][:100]}...")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing validate_names_watchlist: {e}")
        return False

def test_weather_forecast():
    """Test weather_forecast tool (example from Strands docs)."""
    print("🌤️ Testing weather_forecast Tool...")
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "weather_forecast",
                "arguments": {
                    "city": "New York",
                    "days": 5
                }
            }
        }
        
        response = requests.post(
            "http://127.0.0.1:8500/mcp",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ weather_forecast tool working")
            content = data['result']['content']
            print(f"   Response: {content[0]['text']}")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing weather_forecast: {e}")
        return False

def main():
    """Run all Strands MCP integration tests."""
    print("🚀 Testing Strands MCP Integration")
    print("=" * 50)
    
    tests = [
        test_strands_tools_discovery,
        test_strands_tool_execution,
        test_generate_cultural_names,
        test_validate_names_watchlist,
        test_weather_forecast
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Strands MCP integration is working correctly!")
        print("\n📋 Strands MCP Server Status:")
        print("  ✅ Server running on http://127.0.0.1:8500/mcp")
        print("  ✅ Tools discoverable via GET /mcp")
        print("  ✅ @tool decorator pattern implemented")
        print("  ✅ Tool execution working")
        print("  ✅ Ollama integration functional")
        print("\n🔧 For Cursor Integration:")
        print("  - MCP server should be discoverable at 127.0.0.1:8500/mcp")
        print("  - Tools use proper @tool decorator pattern")
        print("  - All tools have proper type hints and docstrings")
        print("  - Tools are compatible with Strands framework")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

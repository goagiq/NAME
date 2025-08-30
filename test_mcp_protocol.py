#!/usr/bin/env python3
"""
Test MCP Protocol
Verifies that the MCP server is working correctly with proper protocol
"""

import requests
import json

def test_mcp_initialize():
    """Test MCP initialize method."""
    print("🔧 Testing MCP Initialize...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {}
            }
        }
    }
    
    try:
        response = requests.post("http://127.0.0.1:8500/mcp", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Initialize response: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Initialize failed: {e}")
        return False

def test_mcp_tools_list():
    """Test MCP tools/list method."""
    print("\n📋 Testing MCP Tools List...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8500/mcp", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        tools = result.get('result', {}).get('tools', [])
        print(f"✅ Found {len(tools)} tools:")
        
        for tool in tools:
            print(f"  📋 {tool['name']}")
            print(f"     Description: {tool['description'][:100]}...")
            print(f"     Schema: {json.dumps(tool['inputSchema'], indent=4)}")
        
        return len(tools) > 0
    except Exception as e:
        print(f"❌ Tools list failed: {e}")
        return False

def test_mcp_tool_call():
    """Test MCP tools/call method."""
    print("\n🔧 Testing MCP Tool Call...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "get_cultural_context",
            "arguments": {
                "region": "Europe",
                "religion": "Christianity"
            }
        }
    }
    
    try:
        response = requests.post("http://127.0.0.1:8500/mcp", json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "result" in result:
            print("✅ Tool call successful")
            print(f"Result: {result['result']['content'][0]['text'][:200]}...")
            return True
        else:
            print(f"❌ Tool call failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Tool call failed: {e}")
        return False

def main():
    """Run all MCP protocol tests."""
    print("🚀 MCP Protocol Test")
    print("=" * 50)
    
    tests = [
        test_mcp_initialize,
        test_mcp_tools_list,
        test_mcp_tool_call
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All MCP protocol tests passed!")
        print("\n💡 If Cursor still can't see the tools, try:")
        print("1. Restart Cursor")
        print("2. Check Cursor's MCP configuration")
        print("3. Verify the MCP host URL is set to: http://127.0.0.1:8500/mcp")
        return 0
    else:
        print("❌ Some MCP protocol tests failed.")
        return 1

if __name__ == "__main__":
    main()

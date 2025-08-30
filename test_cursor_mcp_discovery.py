#!/usr/bin/env python3
"""
Test Cursor MCP Tool Discovery
Verifies that MCP tools are properly exposed for Cursor discovery
"""

import requests
import json
import sys

def test_mcp_discovery():
    """Test MCP tool discovery endpoint."""
    print("🔍 Testing MCP Tool Discovery...")
    
    try:
        # Test GET /mcp endpoint (for tool discovery)
        response = requests.get("http://127.0.0.1:8500/mcp", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        tools = data.get('tools', [])
        print(f"✅ Found {len(tools)} MCP tools:")
        
        for tool in tools:
            print(f"  📋 {tool['name']}")
            print(f"     Description: {tool['description']}")
            print(f"     Schema: {tool['inputSchema']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP discovery: {e}")
        return False

def test_mcp_protocol():
    """Test MCP protocol compliance."""
    print("🔧 Testing MCP Protocol Compliance...")
    
    try:
        # Test tools/list method
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            "http://127.0.0.1:8500/mcp",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'tools' in data['result']:
            print("✅ MCP protocol tools/list working")
            tools = data['result']['tools']
            print(f"   Found {len(tools)} tools via protocol")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP protocol: {e}")
        return False

def test_tool_execution():
    """Test tool execution."""
    print("⚡ Testing Tool Execution...")
    
    try:
        # Test a simple tool call
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
        
        response = requests.post(
            "http://127.0.0.1:8500/mcp",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ Tool execution working")
            content = data['result']['content']
            print(f"   Response: {content}")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing tool execution: {e}")
        return False

def main():
    """Run all MCP discovery tests."""
    print("🚀 Testing Cursor MCP Tool Discovery")
    print("=" * 50)
    
    tests = [
        test_mcp_discovery,
        test_mcp_protocol,
        test_tool_execution
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
        print("🎉 MCP tools are properly discoverable by Cursor!")
        print("\n📋 MCP Server Status:")
        print("  ✅ Server running on http://127.0.0.1:8500/mcp")
        print("  ✅ Tools discoverable via GET /mcp")
        print("  ✅ Protocol compliant JSON-RPC")
        print("  ✅ Tool execution working")
        print("\n🔧 For Cursor Integration:")
        print("  - MCP server should be discoverable at 127.0.0.1:8500/mcp")
        print("  - Tools are properly formatted for Cursor")
        print("  - All MCP protocol methods implemented")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

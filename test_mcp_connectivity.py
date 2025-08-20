#!/usr/bin/env python3
"""
Test MCP Connectivity
Verifies that MCP tools are reachable with proper protocol.
"""

import requests
import json

def test_mcp_server():
    """Test MCP server connectivity and tools."""
    print("Testing MCP Server Connectivity")
    print("=" * 50)

    base_url = "http://localhost:8500"
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Initialize connection
    print("\n2. Testing initialize...")
    try:
        mcp_request = {
            "jsonrpc": "2.0",
            "id": "init-1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        response = requests.post(
            f"{base_url}/mcp", 
            json=mcp_request,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            server_info = result.get("result", {}).get("serverInfo", {})
            print(f"✅ Initialize successful: {server_info}")
        else:
            print(f"❌ Initialize failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Initialize error: {e}")
        return False
    
    # Test 3: List tools
    print("\n3. Testing tools/list...")
    try:
        mcp_request = {
            "jsonrpc": "2.0",
            "id": "tools-1",
            "method": "tools/list",
            "params": {}
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        response = requests.post(
            f"{base_url}/mcp", 
            json=mcp_request,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            tools = result.get("result", {}).get("tools", [])
            print(f"✅ Tools list successful: {len(tools)} tools available")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description']}")
        else:
            print(f"❌ Tools list failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Tools list error: {e}")
        return False
    
    # Test 4: Call domain_check tool
    print("\n4. Testing domain_check tool...")
    try:
        mcp_request = {
            "jsonrpc": "2.0",
            "id": "call-1",
            "method": "tools/call",
            "params": {
                "name": "domain_check",
                "arguments": {
                    "name": "example",
                    "domain": "com"
                }
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        response = requests.post(
            f"{base_url}/mcp", 
            json=mcp_request,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("result", {}).get("content", [])
            if content:
                text = content[0].get("text", "")
                print(f"✅ Tool call successful: {text}")
            else:
                print("❌ Tool call failed: No content returned")
                return False
        else:
            print(f"❌ Tool call failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Tool call error: {e}")
        return False
    
    # Test 5: Call cultural_context_search tool
    print("\n5. Testing cultural_context_search tool...")
    try:
        mcp_request = {
            "jsonrpc": "2.0",
            "id": "call-2",
            "method": "tools/call",
            "params": {
                "name": "cultural_context_search",
                "arguments": {
                    "name": "John",
                    "region": "United States"
                }
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        response = requests.post(
            f"{base_url}/mcp", 
            json=mcp_request,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("result", {}).get("content", [])
            if content:
                text = content[0].get("text", "")
                print(f"✅ Cultural context search successful: {text}")
            else:
                print("❌ Cultural context search failed: No content returned")
                return False
        else:
            print(f"❌ Cultural context search failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Cultural context search error: {e}")
        return False
    
    return True

def test_api_server():
    """Test API server connectivity."""
    print("\nTesting API Server")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Test 1: Health check
    print("1. Testing API health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API health check passed: {health_data}")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check error: {e}")
        return False
    
    # Test 2: List categories
    print("\n2. Testing API categories...")
    try:
        response = requests.get(f"{base_url}/api/categories")
        if response.status_code == 200:
            result = response.json()
            categories = result.get("categories", [])
            print(f"✅ API categories successful: {len(categories)} categories")
            for category in categories:
                print(f"   - {category['id']}: {category['name']}")
        else:
            print(f"❌ API categories failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API categories error: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("Name Generation System - MCP Connectivity Test")
    print("=" * 60)
    
    # Test MCP server
    mcp_ok = test_mcp_server()
    
    # Test API server
    api_ok = test_api_server()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"MCP Server: {'✅ WORKING' if mcp_ok else '❌ FAILED'}")
    print(f"API Server: {'✅ WORKING' if api_ok else '❌ FAILED'}")
    
    if mcp_ok and api_ok:
        print("\n🎉 SYSTEM IS FULLY FUNCTIONAL!")
        print("MCP clients can connect to the MCP server using streamable HTTP.")
        print("API clients can connect to the API server and use endpoints.")
        print("\nMCP Client Connection Info:")
        print("  • Endpoint: http://localhost:8500/mcp")
        print("  • Protocol: Streamable HTTP")
        print("  • Headers: Content-Type: application/json, Accept: application/json, text/event-stream")
        print("  • Available Tools: domain_check, watchlist_validate, cultural_context_search, etc.")
        print("\nAPI Client Connection Info:")
        print("  • Endpoint: http://localhost:8001")
        print("  • Health: http://localhost:8001/health")
        print("  • Categories: http://localhost:8001/api/categories")
        print("  • MCP Tools: http://localhost:8001/api/mcp/tools")
    else:
        print("\n❌ SYSTEM HAS ISSUES")
        print("Please check the logs above for details.")
    
    print("=" * 60)
    return mcp_ok and api_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

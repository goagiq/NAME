#!/usr/bin/env python3
"""
Test MCP Integration with Frontend
Verifies that MCP tools are accessible through the Flask frontend
"""

import requests
import json
import sys

def test_mcp_tools_list():
    """Test listing MCP tools through frontend."""
    print("🔍 Testing MCP Tools List...")
    try:
        response = requests.get("http://127.0.0.1:3000/api/mcp/tools", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        tools = data.get('tools', [])
        print(f"✅ Found {len(tools)} MCP tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
        return True
    except Exception as e:
        print(f"❌ Error listing MCP tools: {e}")
        return False

def test_cultural_context():
    """Test cultural context tool."""
    print("\n🌍 Testing Cultural Context Tool...")
    try:
        payload = {
            "region": "Middle East",
            "religion": "Islam"
        }
        
        response = requests.post(
            "http://127.0.0.1:3000/api/mcp/cultural-context",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ Cultural context tool working")
            content = data['result']['content'][0]
            if 'json' in content:
                cultural_data = content['json']['cultural_context']
                print(f"  - Region: {cultural_data.get('region')}")
                print(f"  - Religion: {cultural_data.get('religion')}")
                print(f"  - Common names: {cultural_data.get('common_names', [])[:3]}...")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing cultural context: {e}")
        return False

def test_name_generation():
    """Test name generation tool."""
    print("\n👤 Testing Name Generation Tool...")
    try:
        payload = {
            "sex": "Female",
            "age": 25,
            "location": "Canada",
            "occupation": "Engineer",
            "race": "Indian",
            "religion": "Hinduism",
            "birth_year": 1998
        }
        
        response = requests.post(
            "http://127.0.0.1:3000/api/mcp/generate-cultural-names",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ Name generation tool working")
            content = data['result']['content'][0]
            if 'json' in content:
                identities = content['json'].get('identities', [])
                print(f"  - Generated {len(identities)} identities")
                for i, identity in enumerate(identities[:2]):
                    name = f"{identity.get('first_name', '')} {identity.get('last_name', '')}"
                    print(f"  - Identity {i+1}: {name}")
            else:
                print(f"  - Response: {content.get('text', 'No text')}")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing name generation: {e}")
        return False

def test_name_validation():
    """Test name validation tool."""
    print("\n✅ Testing Name Validation Tool...")
    try:
        payload = {
            "names": [
                {"first_name": "John", "last_name": "Smith"},
                {"first_name": "Mohammed", "last_name": "Ali"},
                {"first_name": "Test", "last_name": "User"}
            ]
        }
        
        response = requests.post(
            "http://127.0.0.1:3000/api/mcp/validate-names",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ Name validation tool working")
            content = data['result']['content'][0]
            if 'json' in content:
                results = content['json'].get('validation_results', [])
                print(f"  - Validated {len(results)} names")
                for result in results:
                    status = "✅ PASSED" if result.get('is_safe') else "❌ FLAGGED"
                    print(f"  - {result.get('name', 'Unknown')}: {status}")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing name validation: {e}")
        return False

def test_generic_tool_call():
    """Test generic tool call endpoint."""
    print("\n🔧 Testing Generic Tool Call...")
    try:
        payload = {
            "tool_name": "get_cultural_context",
            "arguments": {
                "region": "Europe",
                "religion": "Christianity"
            }
        }
        
        response = requests.post(
            "http://127.0.0.1:3000/api/mcp/call",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'content' in data['result']:
            print("✅ Generic tool call working")
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error testing generic tool call: {e}")
        return False

def main():
    """Run all MCP integration tests."""
    print("🚀 Testing MCP Integration with Frontend")
    print("=" * 50)
    
    tests = [
        test_mcp_tools_list,
        test_cultural_context,
        test_name_generation,
        test_name_validation,
        test_generic_tool_call
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All MCP tools are working correctly!")
        print("\n📋 Available MCP Endpoints:")
        print("  - GET  /api/mcp/tools - List available tools")
        print("  - POST /api/mcp/call - Call any MCP tool")
        print("  - POST /api/mcp/generate-cultural-names - Generate names")
        print("  - POST /api/mcp/validate-names - Validate names")
        print("  - POST /api/mcp/cultural-context - Get cultural context")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

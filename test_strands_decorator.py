#!/usr/bin/env python3
"""
Test real Strands @tool decorator
"""

from strands import tool

@tool
def test_tool(param1: str, param2: int = 3) -> str:
    """Test tool with real Strands decorator.

    Args:
        param1: First parameter
        param2: Second parameter (default: 3)
    """
    return f"Test result: {param1}, {param2}"

def check_tool_attributes():
    print("Checking tool attributes...")
    print(f"Function name: {test_tool.__name__}")
    print(f"Has _is_tool: {hasattr(test_tool, '_is_tool')}")
    print(f"Has _tool_name: {hasattr(test_tool, '_tool_name')}")
    print(f"Has _tool_description: {hasattr(test_tool, '_tool_description')}")
    
    if hasattr(test_tool, '_tool_name'):
        print(f"Tool name: {test_tool._tool_name}")
    if hasattr(test_tool, '_tool_description'):
        print(f"Tool description: {test_tool._tool_description}")
    
    # Test function call
    result = test_tool("hello", 5)
    print(f"Function result: {result}")

if __name__ == "__main__":
    check_tool_attributes()

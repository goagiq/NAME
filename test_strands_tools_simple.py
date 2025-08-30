#!/usr/bin/env python3
"""
Simple test for Strands tools
"""

from strands_tools import generate_cultural_names, validate_names_watchlist, get_cultural_context, weather_forecast

def test_tools():
    print("Testing Strands Tools...")
    
    # Test weather_forecast
    print("\n1. Testing weather_forecast:")
    try:
        result = weather_forecast("New York", 5)
        print(f"✅ weather_forecast working: {result}")
    except Exception as e:
        print(f"❌ weather_forecast failed: {e}")
    
    # Test get_cultural_context
    print("\n2. Testing get_cultural_context:")
    try:
        result = get_cultural_context("Europe", "Christianity")
        print(f"✅ get_cultural_context working: {result[:100]}...")
    except Exception as e:
        print(f"❌ get_cultural_context failed: {e}")
    
    # Test validate_names_watchlist
    print("\n3. Testing validate_names_watchlist:")
    try:
        names = [{"first_name": "John", "last_name": "Smith"}]
        result = validate_names_watchlist(names)
        print(f"✅ validate_names_watchlist working: {result[:100]}...")
    except Exception as e:
        print(f"❌ validate_names_watchlist failed: {e}")

if __name__ == "__main__":
    test_tools()

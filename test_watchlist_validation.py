#!/usr/bin/env python3
"""
Test script for comprehensive watchlist validation functionality.
"""

import asyncio
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_watchlist_validation():
    """Test the comprehensive watchlist validation system."""
    
    print("🔍 Testing Comprehensive Watchlist Validation System")
    print("=" * 60)
    
    # Test names (some are known to be on watchlists for demonstration)
    test_names = [
        "John Smith",  # Common name, likely clear
        "Osama bin Laden",  # Known terrorist (for testing)
        "Saddam Hussein",  # Former dictator (for testing)
        "Maria Rodriguez",  # Common Hispanic name
        "Vladimir Putin",  # Current political figure
        "Jane Doe",  # Common placeholder name
        "Kim Jong-un",  # North Korean leader
        "Sarah Johnson",  # Common American name
    ]
    
    try:
        # Import the watchlist validator
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'services', 'validation'))
        
        from watchlist_validator import WatchlistValidator
        
        async with WatchlistValidator() as validator:
            print("✅ WatchlistValidator initialized successfully")
            print()
            
            # Configure some API keys if available (optional)
            # validator.configure_api_key("ofac_sdn", "your_api_key_here")
            
            # Test individual name validation
            for name in test_names:
                print(f"🔍 Validating: {name}")
                try:
                    result = await validator.validate_name(name, "person")
                    
                    if result.is_blocked:
                        print(f"❌ BLOCKED: {name}")
                        print(f"   Sources: {', '.join(result.sources)}")
                        print(f"   Reasons: {'; '.join(result.reasons)}")
                        print(f"   Confidence: {result.confidence:.2f}")
                    else:
                        print(f"✅ CLEAR: {name}")
                        print(f"   Sources checked: {len(result.raw_data)}")
                        print(f"   Confidence: {result.confidence:.2f}")
                    
                    print()
                    
                except Exception as e:
                    print(f"❌ ERROR validating {name}: {e}")
                    print()
            
            # Test batch validation
            print("🔄 Testing batch validation...")
            batch_results = await validator.validate_batch(test_names[:3], "person")
            
            print("Batch Results:")
            for i, result in enumerate(batch_results):
                status = "BLOCKED" if result.is_blocked else "CLEAR"
                print(f"  {i+1}. {test_names[i]}: {status}")
            
            print()
            
            # Get validation statistics
            stats = validator.get_validation_stats()
            print("📊 Validation Statistics:")
            print(f"  Total cached results: {stats.get('total_cached_results', 0)}")
            print(f"  Total blocked names: {stats.get('total_blocked_names', 0)}")
            print(f"  Recent validations (24h): {stats.get('recent_validations_24h', 0)}")
            print(f"  Enabled sources: {len(stats.get('enabled_sources', []))}")
            print(f"  Cache duration: {stats.get('cache_duration_hours', 24)} hours")
            
    except ImportError as e:
        print(f"❌ Failed to import WatchlistValidator: {e}")
        print("Make sure the watchlist_validator.py file is in the correct location.")
    except Exception as e:
        print(f"❌ Test failed: {e}")


async def test_mcp_integration():
    """Test MCP integration with watchlist validation."""
    
    print("\n🤖 Testing MCP Integration")
    print("=" * 40)
    
    try:
        import aiohttp
        
        # Test MCP server endpoint
        mcp_url = "http://localhost:8500/mcp"
        
        async with aiohttp.ClientSession() as session:
            # Test comprehensive watchlist check
            test_data = {
                "jsonrpc": "2.0",
                "id": "test-1",
                "method": "tools/call",
                "params": {
                    "name": "comprehensive_watchlist_check",
                    "arguments": {
                        "name": "John Smith",
                        "category": "person"
                    }
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            async with session.post(mcp_url, json=test_data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ MCP Integration Test:")
                    print(f"   Response: {result}")
                    
                    if "result" in result and "content" in result["result"]:
                        content = result["result"]["content"][0]["text"]
                        print(f"   Validation Result: {content}")
                    else:
                        print(f"   Error: {result.get('error', 'Unknown error')}")
                else:
                    print(f"❌ MCP request failed with status {response.status}")
                    
    except Exception as e:
        print(f"❌ MCP integration test failed: {e}")


def print_validation_sources():
    """Print information about available validation sources."""
    
    print("\n📋 Available Validation Sources")
    print("=" * 40)
    
    sources = {
        "Government Watchlists": [
            "OFAC Specially Designated Nationals (SDN)",
            "FBI Most Wanted List",
            "Interpol Red Notices",
            "UN Sanctions List",
            "EU Sanctions List",
            "UK Sanctions List",
            "Canada Sanctions List"
        ],
        "Aviation Security": [
            "TSA No Fly List (Public Data)"
        ],
        "Financial Crime": [
            "FINRA BrokerCheck"
        ],
        "Law Enforcement": [
            "National Sex Offender Registry"
        ],
        "Industry Watchlists": [
            "World-Check (Thomson Reuters)",
            "Dow Jones Risk & Compliance"
        ],
        "Public Records": [
            "Public Records Search"
        ],
        "Social Media": [
            "Social Media Risk Assessment"
        ]
    }
    
    for category, source_list in sources.items():
        print(f"\n{category}:")
        for source in source_list:
            print(f"  • {source}")


def print_setup_instructions():
    """Print setup instructions for the watchlist validation system."""
    
    print("\n🔧 Setup Instructions")
    print("=" * 30)
    
    print("""
1. Install Required Dependencies:
   pip install aiohttp

2. Configure API Keys (Optional):
   - OFAC SDN: https://developer.trade.gov/consolidated-screening-list.html
   - FINRA BrokerCheck: https://www.finra.org/brokercheck
   - World-Check: https://risk.lexisnexis.com/world-check
   - Dow Jones: https://www.dowjones.com/risk-compliance/

3. Enable/Disable Sources:
   - Use validator.enable_source("source_name", True/False)
   - Configure rate limits as needed

4. Database Configuration:
   - SQLite database created automatically
   - Cache duration: 24 hours (configurable)
   - Validation logs stored for audit

5. Integration with Name Generation:
   - Validation agent uses comprehensive_watchlist_check
   - Results cached to improve performance
   - Blocked names trigger regeneration
""")


async def main():
    """Main test function."""
    
    print("🚀 Comprehensive Watchlist Validation System Test")
    print("=" * 60)
    
    # Print available sources
    print_validation_sources()
    
    # Print setup instructions
    print_setup_instructions()
    
    # Test watchlist validation
    await test_watchlist_validation()
    
    # Test MCP integration
    await test_mcp_integration()
    
    print("\n✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(main())

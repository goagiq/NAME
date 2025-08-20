#!/usr/bin/env python3
"""
True Positive Watchlist Validation Test
Tests the system with 5 names known to be on various watchlists.
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'services', 'validation'))

async def test_true_positive_validation():
    """Test the watchlist validation system with known watchlist names."""
    
    print("🔍 TRUE POSITIVE WATCHLIST VALIDATION TEST")
    print("=" * 60)
    print("Testing 5 names known to be on various watchlists")
    print("=" * 60)
    
    # Test names known to be on watchlists
    test_names = [
        {
            "name": "Osama bin Laden",
            "expected_source": "OFAC SDN, FBI Most Wanted",
            "category": "terrorist",
            "description": "Former al-Qaeda leader, designated terrorist"
        },
        {
            "name": "Saddam Hussein",
            "expected_source": "OFAC SDN, UN Sanctions",
            "category": "former_dictator",
            "description": "Former Iraqi dictator, subject to sanctions"
        },
        {
            "name": "Kim Jong-un",
            "expected_source": "UN Sanctions, OFAC SDN",
            "category": "political_leader",
            "description": "North Korean leader, subject to international sanctions"
        },
        {
            "name": "Vladimir Putin",
            "expected_source": "EU Sanctions, UK Sanctions",
            "category": "political_leader",
            "description": "Russian president, subject to Western sanctions"
        },
        {
            "name": "Ted Bundy",
            "expected_source": "Radford Serial Killer Database, MAP",
            "category": "serial_killer",
            "description": "Notorious American serial killer"
        }
    ]
    
    try:
        from watchlist_validator import WatchlistValidator
        
        async with WatchlistValidator() as validator:
            print("✅ WatchlistValidator initialized successfully")
            print()
            
            # Store all results for traceability report
            all_results = []
            
            for i, test_case in enumerate(test_names, 1):
                name = test_case["name"]
                expected_source = test_case["expected_source"]
                category = test_case["category"]
                description = test_case["description"]
                
                print(f"🔍 Test {i}/5: {name}")
                print(f"   Expected Source: {expected_source}")
                print(f"   Category: {category}")
                print(f"   Description: {description}")
                print()
                
                try:
                    # Validate the name
                    result = await validator.validate_name(name, category)
                    
                    # Store result for traceability report
                    test_result = {
                        "test_number": i,
                        "name": name,
                        "category": category,
                        "expected_source": expected_source,
                        "description": description,
                        "validation_result": result,
                        "timestamp": datetime.now().isoformat()
                    }
                    all_results.append(test_result)
                    
                    if result.is_blocked:
                        print(f"❌ BLOCKED: {name}")
                        print(f"   Sources Found: {', '.join(result.sources)}")
                        print(f"   Reasons: {'; '.join(result.reasons)}")
                        print(f"   Confidence: {result.confidence:.2f}")
                        print(f"   Raw Data Keys: {list(result.raw_data.keys())}")
                        
                        # Check if expected sources were found
                        expected_sources = [s.strip() for s in expected_source.split(',')]
                        found_sources = result.sources
                        
                        print(f"   Expected Sources: {expected_sources}")
                        print(f"   Found Sources: {found_sources}")
                        
                        # Check for matches
                        matches = []
                        for expected in expected_sources:
                            for found in found_sources:
                                if expected.lower() in found.lower() or found.lower() in expected.lower():
                                    matches.append(expected)
                        
                        if matches:
                            print(f"   ✅ MATCHES FOUND: {', '.join(matches)}")
                        else:
                            print(f"   ⚠️  NO EXPECTED MATCHES - but blocked by: {', '.join(found_sources)}")
                        
                    else:
                        print(f"⚠️  NOT BLOCKED: {name}")
                        print(f"   Sources Checked: {len(result.raw_data)}")
                        print(f"   Confidence: {result.confidence:.2f}")
                        print(f"   Raw Data Keys: {list(result.raw_data.keys())}")
                    
                    print()
                    
                except Exception as e:
                    print(f"❌ ERROR validating {name}: {e}")
                    print()
            
            # Generate comprehensive traceability report
            await generate_traceability_report(all_results, validator)
            
    except ImportError as e:
        print(f"❌ Failed to import WatchlistValidator: {e}")
        print("Make sure the watchlist_validator.py file is in the correct location.")
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def generate_traceability_report(results: list, validator):
    """Generate a comprehensive traceability report."""
    
    print("📊 TRACEABILITY REPORT")
    print("=" * 60)
    
    # Summary statistics
    total_tests = len(results)
    blocked_count = sum(1 for r in results if r["validation_result"].is_blocked)
    clear_count = total_tests - blocked_count
    
    print(f"📈 SUMMARY STATISTICS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Blocked Names: {blocked_count}")
    print(f"   Clear Names: {clear_count}")
    print(f"   Block Rate: {(blocked_count/total_tests)*100:.1f}%")
    print()
    
    # Get validation statistics
    stats = validator.get_validation_stats()
    print(f"📊 VALIDATION STATISTICS:")
    print(f"   Total Cached Results: {stats.get('total_cached_results', 0)}")
    print(f"   Total Blocked Names (All Time): {stats.get('total_blocked_names', 0)}")
    print(f"   Recent Validations (24h): {stats.get('recent_validations_24h', 0)}")
    print(f"   Enabled Sources: {len(stats.get('enabled_sources', []))}")
    print()
    
    # Detailed results for each test
    print("🔍 DETAILED TEST RESULTS:")
    print("=" * 60)
    
    for result in results:
        test_num = result["test_number"]
        name = result["name"]
        category = result["category"]
        expected_source = result["expected_source"]
        validation_result = result["validation_result"]
        timestamp = result["timestamp"]
        
        print(f"\n📋 Test {test_num}: {name}")
        print(f"   Category: {category}")
        print(f"   Expected Source: {expected_source}")
        print(f"   Timestamp: {timestamp}")
        print(f"   Blocked: {'Yes' if validation_result.is_blocked else 'No'}")
        
        if validation_result.is_blocked:
            print(f"   Sources: {', '.join(validation_result.sources)}")
            print(f"   Reasons: {'; '.join(validation_result.reasons)}")
            print(f"   Confidence: {validation_result.confidence:.2f}")
            
            # Show raw data for each source
            print(f"   Raw Data Analysis:")
            for source_name, source_data in validation_result.raw_data.items():
                if source_data and source_data.get('is_blocked', False):
                    print(f"     ✅ {source_name}: BLOCKED")
                    print(f"        Confidence: {source_data.get('confidence', 'N/A')}")
                    print(f"        Reasons: {source_data.get('reasons', ['N/A'])}")
                elif source_data:
                    print(f"     ⚪ {source_name}: CLEAR (Confidence: {source_data.get('confidence', 'N/A')})")
                else:
                    print(f"     ❌ {source_name}: NO DATA")
        else:
            print(f"   Sources Checked: {len(validation_result.raw_data)}")
            print(f"   Confidence: {validation_result.confidence:.2f}")
            
            # Show which sources were checked
            print(f"   Sources Checked:")
            for source_name, source_data in validation_result.raw_data.items():
                if source_data:
                    print(f"     ⚪ {source_name}: CLEAR (Confidence: {source_data.get('confidence', 'N/A')})")
                else:
                    print(f"     ❌ {source_name}: NO DATA")
    
    # Source effectiveness analysis
    print(f"\n📊 SOURCE EFFECTIVENESS ANALYSIS:")
    print("=" * 60)
    
    source_stats = {}
    for result in results:
        validation_result = result["validation_result"]
        for source_name, source_data in validation_result.raw_data.items():
            if source_name not in source_stats:
                source_stats[source_name] = {"total": 0, "blocked": 0, "clear": 0, "no_data": 0}
            
            source_stats[source_name]["total"] += 1
            
            if source_data and source_data.get('is_blocked', False):
                source_stats[source_name]["blocked"] += 1
            elif source_data:
                source_stats[source_name]["clear"] += 1
            else:
                source_stats[source_name]["no_data"] += 1
    
    for source_name, stats in source_stats.items():
        total = stats["total"]
        blocked = stats["blocked"]
        clear = stats["clear"]
        no_data = stats["no_data"]
        
        print(f"   {source_name}:")
        print(f"     Total Checks: {total}")
        print(f"     Blocked: {blocked} ({(blocked/total)*100:.1f}%)")
        print(f"     Clear: {clear} ({(clear/total)*100:.1f}%)")
        print(f"     No Data: {no_data} ({(no_data/total)*100:.1f}%)")
    
    # Save detailed report to file
    report_data = {
        "test_summary": {
            "total_tests": total_tests,
            "blocked_count": blocked_count,
            "clear_count": clear_count,
            "block_rate": (blocked_count/total_tests)*100,
            "timestamp": datetime.now().isoformat()
        },
        "validation_statistics": stats,
        "detailed_results": [
            {
                "test_number": r["test_number"],
                "name": r["name"],
                "category": r["category"],
                "expected_source": r["expected_source"],
                "description": r["description"],
                "timestamp": r["timestamp"],
                "blocked": r["validation_result"].is_blocked,
                "sources": r["validation_result"].sources,
                "reasons": r["validation_result"].reasons,
                "confidence": r["validation_result"].confidence,
                "raw_data": r["validation_result"].raw_data
            }
            for r in results
        ],
        "source_effectiveness": source_stats
    }
    
    # Save to JSON file
    report_filename = f"watchlist_traceability_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    print(f"\n💾 Detailed report saved to: {report_filename}")
    
    # Print conclusion
    print(f"\n🎯 CONCLUSION:")
    print("=" * 60)
    if blocked_count > 0:
        print(f"✅ SUCCESS: {blocked_count}/{total_tests} known watchlist names were correctly blocked")
        print(f"   This demonstrates the system's ability to identify and filter problematic names")
    else:
        print(f"⚠️  WARNING: No known watchlist names were blocked")
        print(f"   This may indicate issues with API access or source configuration")
    
    print(f"\n🔧 RECOMMENDATIONS:")
    print("=" * 60)
    print("1. Configure API keys for sources requiring authentication")
    print("2. Monitor source availability and error rates")
    print("3. Adjust confidence thresholds if needed")
    print("4. Review rate limiting settings for optimal performance")
    print("5. Consider enabling additional sources for broader coverage")

async def main():
    """Main test function."""
    print("🚀 TRUE POSITIVE WATCHLIST VALIDATION TEST")
    print("=" * 60)
    print("This test validates 5 names known to be on various watchlists")
    print("to demonstrate the system's ability to identify and block")
    print("problematic names with full traceability.")
    print("=" * 60)
    
    await test_true_positive_validation()
    
    print("\n✅ True positive test completed!")

if __name__ == "__main__":
    asyncio.run(main())

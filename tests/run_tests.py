#!/usr/bin/env python3
"""
Test Runner for Name Generation System
Runs all tests using the virtual environment Python interpreter.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_tests():
    """Run all tests using pytest."""
    print("Starting test suite for Name Generation System...")
    print("=" * 50)
    
    # Get the virtual environment Python path
    venv_python = Path(".venv/Scripts/python.exe")
    
    if not venv_python.exists():
        print("Error: Virtual environment not found!")
        print("Please create a virtual environment first:")
        print("python -m venv .venv")
        print("Then install dependencies:")
        print(".venv\\Scripts\\pip install -e .")
        return False
    
    # Test commands to run
    test_commands = [
        ["pytest", "tests/test_mcp_integration.py", "-v"],
        ["pytest", "tests/test_strands_agent.py", "-v"],
        ["pytest", "tests/test_api_endpoints.py", "-v"],
        ["pytest", "tests/", "--cov=src", "--cov-report=term-missing"]
    ]
    
    all_passed = True
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\nRunning test {i}/{len(test_commands)}: {' '.join(cmd)}")
        print("-" * 40)
        
        try:
            # Run the test command
            result = subprocess.run(
                [str(venv_python), "-m"] + cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            # Check if test passed
            if result.returncode == 0:
                print(f"✅ Test {i} PASSED")
            else:
                print(f"❌ Test {i} FAILED")
                all_passed = False
            
            # Wait a bit between tests
            time.sleep(2)
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Test {i} TIMEOUT")
            all_passed = False
        except Exception as e:
            print(f"💥 Test {i} ERROR: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests PASSED!")
        return True
    else:
        print("💔 Some tests FAILED!")
        return False


def run_specific_test(test_file: str):
    """Run a specific test file."""
    venv_python = Path(".venv/Scripts/python.exe")
    
    if not venv_python.exists():
        print("Error: Virtual environment not found!")
        return False
    
    test_path = Path(f"tests/{test_file}")
    if not test_path.exists():
        print(f"Error: Test file {test_file} not found!")
        return False
    
    print(f"Running specific test: {test_file}")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            [str(venv_python), "-m", "pytest", str(test_path), "-v"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ Test PASSED")
            return True
        else:
            print("❌ Test FAILED")
            return False
            
    except Exception as e:
        print(f"💥 Test ERROR: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_file = sys.argv[1]
        success = run_specific_test(test_file)
    else:
        # Run all tests
        success = run_tests()
    
    sys.exit(0 if success else 1)

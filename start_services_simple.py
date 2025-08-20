#!/usr/bin/env python3
"""
Simple Services Startup Script
Starts backend services and exits immediately.
"""

import subprocess
import sys
import time

def start_service(name, command):
    """Start a service in the background."""
    print(f"🚀 Starting {name}...")
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"✅ {name} started with PID: {process.pid}")
        return True
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return False

def main():
    """Start all services and exit."""
    print("🎯 Starting Name Generation System Services")
    print("=" * 50)
    
    success = True
    
    # Start MCP Server
    if not start_service("MCP Server (port 8500)", [sys.executable, "mcp_server_proper.py"]):
        success = False
    
    # Wait a moment
    time.sleep(3)
    
    # Start API Server
    if not start_service("API Server (port 8001)", [sys.executable, "start_api_server.py"]):
        success = False
    
    # Wait a moment
    time.sleep(3)
    
    if success:
        print("\n🎉 Services started successfully!")
        print("=" * 50)
        print("🔧 API Server: http://localhost:8001")
        print("🤖 MCP Server: http://localhost:8500")
        print("=" * 50)
        print("To start the frontend, run:")
        print("  cd frontend && npm start")
        print("=" * 50)
        print("Services are running in the background.")
        print("Use 'tasklist | findstr python.exe' to see running processes.")
    else:
        print("\n❌ Some services failed to start!")
    
    print("\nScript completed. Exiting...")

if __name__ == "__main__":
    main()

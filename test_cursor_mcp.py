#!/usr/bin/env python3
import requests
print("Testing Cursor MCP formats...")
response = requests.get("http://localhost:8500/mcp")
print(f"GET /mcp status: {response.status_code}")

#!/usr/bin/env python3
"""
Port Manager
Handles port allocation and conflict resolution for the Name Generation System.
"""

import socket
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def is_port_available(port: int, host: str = "localhost") -> bool:
    """Check if a port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            return result != 0  # Port is available if connection fails
    except Exception:
        return False

def find_available_port(start_port: int, max_attempts: int = 10, host: str = "localhost") -> Optional[int]:
    """Find an available port starting from start_port."""
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port, host):
            logger.info(f"Found available port: {port}")
            return port
        logger.debug(f"Port {port} is not available, trying next...")
    
    logger.error(f"No available ports found in range {start_port}-{start_port + max_attempts - 1}")
    return None

def get_system_ports() -> Tuple[int, int]:
    """Get the ports for MCP and API servers."""
    # MCP server should always use port 8500
    mcp_port = 8500

    # API server should use port 8001, but find alternative if busy
    api_port = find_available_port(8001, max_attempts=5)

    if api_port is None:
        # If 8001-8005 are busy, try higher ports
        api_port = find_available_port(8006, max_attempts=10)

    if api_port is None:
        raise RuntimeError("No available ports found for API server")

    return mcp_port, api_port

def check_ports_status() -> dict:
    """Check the status of system ports."""
    mcp_port, api_port = get_system_ports()
    
    return {
        "mcp": {
            "port": mcp_port,
            "available": is_port_available(mcp_port),
            "url": f"http://localhost:{mcp_port}"
        },
        "api": {
            "port": api_port,
            "available": is_port_available(api_port),
            "url": f"http://localhost:{api_port}"
        }
    }

def print_port_status():
    """Print the current port status."""
    try:
        status = check_ports_status()
        
        print("Port Status:")
        print("=" * 40)
        print(f"MCP Server:")
        print(f"  Port: {status['mcp']['port']}")
        print(f"  Available: {'✅' if status['mcp']['available'] else '❌'}")
        print(f"  URL: {status['mcp']['url']}")
        print()
        print(f"API Server:")
        print(f"  Port: {status['api']['port']}")
        print(f"  Available: {'✅' if status['api']['available'] else '❌'}")
        print(f"  URL: {status['api']['url']}")
        print("=" * 40)
        
        return status
        
    except Exception as e:
        print(f"Error checking port status: {e}")
        return None

if __name__ == "__main__":
    print_port_status()

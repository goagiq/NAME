"""
Port Management Configuration
Handles dedicated and auto-generated ports for all services.
"""

import socket
from typing import Dict


class PortManager:
    """Manages port allocation for all services."""
    
    def __init__(self):
        self.dedicated_ports = {
            'mcp': 8000,
            'ollama': 11434
        }
        self.service_ports = {}
    
    def find_available_port(self, start_port: int, max_attempts: int = 100) -> int:
        """Find an available port starting from start_port."""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        raise RuntimeError(
            f"No available ports found in range {start_port}-{start_port + max_attempts}"
        )
    
    def get_all_ports(self) -> Dict[str, int]:
        """Get all service ports (dedicated + auto-generated)."""
        if not self.service_ports:
            self.service_ports = {
                'fastapi': self.find_available_port(8001),
                'frontend': self.find_available_port(3000),
                'database': self.find_available_port(5432),
                'redis': self.find_available_port(6379),
                **self.dedicated_ports
            }
        return self.service_ports
    
    def get_mcp_port(self) -> int:
        """Get dedicated MCP port."""
        return self.dedicated_ports['mcp']
    
    def get_ollama_port(self) -> int:
        """Get dedicated Ollama port."""
        return self.dedicated_ports['ollama']

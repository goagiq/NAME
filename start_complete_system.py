#!/usr/bin/env python3
"""
Complete System Startup Script
Starts all components of the Name Generation System
"""

import subprocess
import time
import sys
import os
import logging
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_ollama():
    """Start Ollama service."""
    try:
        logger.info("Starting Ollama service...")
        # Check if Ollama is already running
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Ollama is already running")
            return True
        else:
            logger.info("Starting Ollama server...")
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)  # Wait for Ollama to start
            logger.info("✅ Ollama service started")
            return True
    except Exception as e:
        logger.error(f"❌ Failed to start Ollama: {e}")
        return False


def start_mcp_server():
    """Start MCP server on port 8500."""
    try:
        logger.info("Starting MCP server on port 8500...")
        # Start the Strands MCP server
        subprocess.Popen([sys.executable, 'strands_mcp_server.py'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for server to start
        logger.info("✅ MCP server started on port 8500")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start MCP server: {e}")
        return False


def start_flask_app():
    """Start Flask application on port 3000."""
    try:
        logger.info("Starting Flask application on port 3000...")
        # Change to python_frontend directory
        os.chdir('python_frontend')
        subprocess.Popen([sys.executable, 'app.py'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for Flask to start
        logger.info("✅ Flask application started on port 3000")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start Flask app: {e}")
        return False


def check_services():
    """Check if all services are running."""
    try:
        import requests
        
        services = {
            "Ollama": "http://localhost:11434",
            "MCP Server": "http://localhost:8500",
            "Flask App": "http://localhost:3000"
        }
        
        logger.info("Checking service status...")
        for service_name, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {service_name} is running")
                else:
                    logger.warning(f"⚠️ {service_name} responded with status {response.status_code}")
            except Exception as e:
                logger.error(f"❌ {service_name} is not responding: {e}")
    except ImportError:
        logger.warning("requests module not available - skipping service checks")


def main():
    """Main function to start all services."""
    logger.info("🚀 Starting Name Generation System...")
    
    # Start services
    ollama_ok = start_ollama()
    mcp_ok = start_mcp_server()
    flask_ok = start_flask_app()
    
    # Wait a bit for all services to start
    time.sleep(5)
    
    # Check service status
    check_services()
    
    logger.info("🎉 System startup complete!")
    logger.info("📋 Available endpoints:")
    logger.info("  - Web Interface: http://localhost:3000")
    logger.info("  - MCP Server: http://localhost:8500")
    logger.info("  - Ollama API: http://localhost:11434")
    
    logger.info("📝 Usage:")
    logger.info("  1. Open http://localhost:3000 in your browser")
    logger.info("  2. Fill out the form with cultural parameters")
    logger.info("  3. Click 'Generate Identity' to get culturally appropriate names")
    
    # Keep the script running
    try:
        while True:
            time.sleep(60)  # Check every minute
            logger.info("System is running... Press Ctrl+C to stop")
    except KeyboardInterrupt:
        logger.info("Shutting down system...")
        logger.info("✅ System stopped")


if __name__ == "__main__":
    main()

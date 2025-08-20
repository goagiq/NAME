"""
Logging Configuration
Sets up logging for the entire application.
"""

import logging
import sys
from pathlib import Path


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    # Create logs directory
    logs_dir = Path("results/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging with Unicode support for Windows
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    
    # Console handler with Unicode support
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Note: Windows console encoding issues with Unicode characters
    # are handled by using UTF-8 file logging and simple console
    # output
    
    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler(logs_dir / "app.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    root_logger.handlers.clear()  # Clear any existing handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Set specific loggers
    logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
    logging.getLogger("mcp").setLevel(logging.INFO)
    logging.getLogger("uvicorn").setLevel(logging.INFO)

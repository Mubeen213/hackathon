import logging
import sys
from typing import Dict, Any

def setup_logging(name: str = "mcp_client", level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger with the specified name and level."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# Create default logger
logger = setup_logging()
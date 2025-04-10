import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8001"))

# MCP settings
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

# Claude settings
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "2048"))

# App settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
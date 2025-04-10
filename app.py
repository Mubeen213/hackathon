import asyncio
import os
import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import API_HOST, API_PORT, MCP_SERVER_URL, DEBUG
from config.logging_config import logger
from core.client import MCPClient
from core.chat_service import ChatService
from api.controllers import ChatController
from api.routes import create_router
from utils.error_handlers import (
    AppError, 
    app_error_handler, 
    http_exception_handler,
    general_exception_handler
)

# Create FastAPI app
app = FastAPI(
    title="MCP Client API",
    description="API for interacting with MCP tools through Claude",
    version="1.0.0",
    debug=DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handlers
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Initialize services
mcp_client = MCPClient()
chat_service = ChatService(mcp_client)
chat_controller = ChatController(chat_service)

# Create router
api_router = create_router(chat_controller)
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """Connect to MCP server on startup."""
    server_url = MCP_SERVER_URL
    
    if not server_url:
        server_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not server_url:
        logger.error("MCP server URL not provided. Please set MCP_SERVER_URL environment variable or provide as command line argument.")
        # Don't exit - we'll let the application start but it won't be able to call tools
        return
    
    try:
        logger.info(f"Connecting to MCP server at {server_url}")
        await mcp_client.connect_to_sse_server(server_url=server_url)
        logger.info("Successfully connected to MCP server")
    except Exception as e:
        logger.error(f"Failed to connect to MCP server: {str(e)}")
        # Don't exit - we'll let the application start but it won't be able to call tools

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    await mcp_client.cleanup()
    logger.info("Application shutdown complete")

if __name__ == "__main__":
    logger.info("Starting MCP Client API...")
    logger.info(f"API Host: {API_HOST}, Port: {API_PORT}")
    
    # Check if MCP server URL is provided
    if not MCP_SERVER_URL and len(sys.argv) < 2:
        logger.warning("MCP_SERVER_URL environment variable not set and no URL provided as argument.")
        logger.warning("Usage: python app.py [MCP_SERVER_URL]")
    
    uvicorn.run(
        "app:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )
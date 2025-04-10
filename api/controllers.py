from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, BackgroundTasks

from core.client import MCPClient
from core.chat_service import ChatService
from api.models import ChatRequest, ClearContextRequest, ChatResponse, StatusResponse
from config.logging_config import logger
from utils.error_handlers import ValidationError

class ChatController:
    """Controller for chat-related endpoints."""
    
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service
    
    async def process_chat(self, request: ChatRequest) :
        """Process a chat request."""
        logger.info(f"Processing chat request: {request.query[:50]}...")
        
        if not request.query.strip():
            raise ValidationError("Query cannot be empty")
        
        result = await self.chat_service.process_query(
            query=request.query,
            context_id=request.context_id,
            system_prompt=request.system_prompt
        )
        logger.debug(f"Chat response: {result['response'][:50]}...")
        return result
    
    def clear_context(self, request: ClearContextRequest) -> StatusResponse:
        """Clear a conversation context."""
        logger.info(f"Clearing context: {request.context_id}")
        
        result = self.chat_service.clear_context(
            context_id=request.context_id,
            preserve_system=request.preserve_system
        )
        
        if result.get("status") == "not_found":
            return StatusResponse(
                status="not_found",
                message=f"Context {request.context_id} not found"
            )
            
        return StatusResponse(
            status="success",
            message=f"Context {request.context_id} cleared successfully",
            details={"preserve_system": request.preserve_system}
        )
    
    async def get_status(self) -> StatusResponse:
        """Get the status of the chat service."""
        mcp_client = self.chat_service.mcp_client
        connected = mcp_client.is_connected
        
        # Check if tools are available
        tools = []
        if connected:
            try:
                available_tools = await mcp_client.get_available_tools()
                tools = [tool["name"] for tool in available_tools]
            except Exception as e:
                logger.error(f"Error fetching available tools: {str(e)}")
        
        details = {
            "connected": connected,
            "available_tools": tools,
            "active_contexts": len(self.chat_service.contexts)
        }
        
        status = "online" if connected else "disconnected"
        message = "Service is operational" if connected else "Service is disconnected from MCP server"
        
        return StatusResponse(
            status=status,
            message=message,
            details=details
        )
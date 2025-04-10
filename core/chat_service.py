import asyncio
from typing import Dict, List, Any, Optional, Tuple
import json

from anthropic import Anthropic

from config.logging_config import logger
from config.settings import CLAUDE_MODEL, CLAUDE_MAX_TOKENS
from core.client import MCPClient
from core.context import ConversationContext
from utils.error_handlers import ValidationError, AppError

class ChatService:
    """Service for handling chat interactions with Claude and MCP tools."""
    
    def __init__(self, mcp_client: MCPClient):
        """Initialize the chat service with an MCP client."""
        self.mcp_client = mcp_client
        self.anthropic = Anthropic()
        self.contexts: Dict[str, ConversationContext] = {}
    
    def create_context(self, context_id: str, system_prompt: Optional[str] = None) -> ConversationContext:
        """Create a new conversation context."""
        context = ConversationContext()
        if system_prompt:
            context.add_system_message(system_prompt)
        self.contexts[context_id] = context
        return context
    
    def get_context(self, context_id: str, create_if_missing: bool = True) -> Optional[ConversationContext]:
        """Get a conversation context by ID."""
        context = self.contexts.get(context_id)
        if not context and create_if_missing:
            context = self.create_context(context_id)
        return context
    
    async def process_query(
        self, 
        query: str, 
        context_id: str = "default", 
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a query using Claude and available tools."""
        if not query.strip():
            raise ValidationError("Query cannot be empty")
            
        if not self.mcp_client.is_connected:
            raise AppError("MCP client is not connected")
        
        # Get or create context
        context = self.get_context(context_id)
        
        # Update system prompt if provided
        if system_prompt:
            context.add_system_message(system_prompt)
        
        # Add user query to context
        context.add_user_message(query)
        
        # Get available tools
        available_tools = await self.mcp_client.get_available_tools()
        
        # Get messages from context - THIS IS FIXED to extract system messages properly
        messages = context.get_messages()
        
        # Extract system message for top-level parameter
        system = None
        filtered_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                filtered_messages.append(msg)
        
        logger.info(f"Processing query with {len(filtered_messages)} messages in context")
        
        # Call Claude API - FIX: pass system as a top-level parameter
        try:
            response = self.anthropic.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS,
                messages=filtered_messages,
                tools=available_tools,
                system='You return structured JSON responses'
            )
            logger.info(f"Claude response: {response}")
            # Process response and handle tool calls
            tool_results = []
            final_text = []
            
            for content in response.content:
                if content.type == 'text':
                    final_text.append(content.text)
                    
                    # Add assistant response to context
                    context.add_assistant_message(content.text)
                
                elif content.type == 'tool_use':
                    tool_name = content.name
                    tool_args = content.input
                    
                    # Add used tool info to response
                    tool_call_text = f"[Calling tool {tool_name} with args {json.dumps(tool_args)}]"
                    final_text.append(tool_call_text)
                    
                  # Execute tool call
                    result = await self.mcp_client.call_tool(tool_name, tool_args)
                    
                    # Extract text content if result contains TextContent objects
                    serializable_result = result
                    if hasattr(result, 'content') and isinstance(result.content, list):
                        serializable_result = {
                            "content": [item.text if hasattr(item, 'text') else str(item) for item in result.content],
                            "status_code": result.status_code if hasattr(result, 'status_code') else None
                        }
                    
                    # Record tool result in context with serializable data
                    context.add_tool_result(tool_name, tool_args, serializable_result)
                    
                    # Add to tool results for response
                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": serializable_result
                    })
                    
                    # If the tool use had text (unlikely but possible)
                    if hasattr(content, 'text') and content.text:
                        context.add_assistant_message(content.text)
                    
                    # Get follow-up response from Claude after tool execution
                    # Fix for follow-up request too
                    updated_messages = context.get_messages()
                    
                    # Extract system message for follow-up response
                    system = None
                    follow_up_messages = []
                    
                    for msg in updated_messages:
                        if msg["role"] == "system":
                            system = msg["content"]
                        else:
                            follow_up_messages.append(msg)
                    
                    follow_up_response = self.anthropic.messages.create(
                        model=CLAUDE_MODEL,
                        max_tokens=CLAUDE_MAX_TOKENS,
                        messages=follow_up_messages,
                        system='You return structured JSON responses'
                    )
                    logger.info(f"Follow-up response ------: {follow_up_response.content[0]}")
                    follow_up_text = follow_up_response.content[0].text
                    final_text.append(follow_up_text)
                    context.add_assistant_message(follow_up_text)
            
            # Prepare the response
            response_text = "\n".join(final_text)
            
            return {
                "response": response_text,
                "tool_calls": tool_results,
                "context_id": context_id
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise AppError(f"Error processing query: {str(e)}")
    
    def clear_context(self, context_id: str, preserve_system: bool = True) -> Dict[str, Any]:
        """Clear a conversation context."""
        context = self.get_context(context_id, create_if_missing=False)
        if not context:
            return {"status": "not_found", "message": f"Context {context_id} not found"}
        
        context.clear_context(preserve_system=preserve_system)
        return {"status": "cleared", "context_id": context_id}
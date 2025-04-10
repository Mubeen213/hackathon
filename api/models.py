from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Chat request model."""
    query: str = Field(..., description="The user's query to process")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt to customize behavior")
    context_id: Optional[str] = Field("default", description="Conversation context ID")

class ClearContextRequest(BaseModel):
    """Request to clear conversation context."""
    context_id: str = Field(..., description="Conversation context ID to clear")
    preserve_system: bool = Field(True, description="Whether to preserve system messages")

class ToolCall(BaseModel):
    """Tool call result model."""
    tool: str
    args: Dict[str, Any]
    result: Dict[str, Any]

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    tool_calls: List[ToolCall]
    context_id: str

class ErrorResponse(BaseModel):
    """Error response model."""
    error: bool = True
    message: str
    status_code: int
    details: Optional[Dict[str, Any]] = None

class StatusResponse(BaseModel):
    """Status response model."""
    status: str
    message: str
    details: Optional[Dict[str, Any]] = None
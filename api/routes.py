from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from api.controllers import ChatController
from api.models import ChatRequest, ClearContextRequest, ChatResponse, StatusResponse
from utils.error_handlers import AppError

def create_router(chat_controller: ChatController) -> APIRouter:
    """Create and configure the API router."""
    router = APIRouter(prefix="/api")
    
    @router.post("/chat", response_model=ChatResponse)
    async def chat_endpoint(request: ChatRequest):
        """Process a chat request."""
        try:
            return await chat_controller.process_chat(request)
        except AppError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/clear-context", response_model=StatusResponse)
    def clear_context_endpoint(request: ClearContextRequest):
        """Clear a conversation context."""
        try:
            return chat_controller.clear_context(request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/status", response_model=StatusResponse)
    async def status_endpoint():
        """Get the status of the chat service."""
        try:
            return await chat_controller.get_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return router
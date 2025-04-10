import traceback
from typing import Dict, Any, Optional, Tuple

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from config.logging_config import logger

class AppError(Exception):
    """Base exception class for application errors"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(AppError):
    """Exception raised for validation errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=400, details=details)

class ClientConnectionError(AppError):
    """Exception raised for MCP client connection errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=503, details=details)

class ToolExecutionError(AppError):
    """Exception raised when tool execution fails"""
    def __init__(self, tool_name: str, error: str, details: Optional[Dict[str, Any]] = None):
        message = f"Tool execution failed for {tool_name}: {error}"
        super().__init__(message=message, status_code=500, details=details)

def log_error(error: Exception, request_info: Optional[Dict[str, Any]] = None) -> None:
    """Log error with optional request context information"""
    error_type = type(error).__name__
    
    if request_info:
        logger.error(
            f"Error {error_type}: {str(error)} - Request: {request_info}",
            exc_info=True
        )
    else:
        logger.error(f"Error {error_type}: {str(error)}", exc_info=True)

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPExceptions"""
    log_error(exc, {"path": request.url.path, "method": request.method})
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": str(exc.detail),
            "status_code": exc.status_code,
        }
    )

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle application-specific errors"""
    log_error(exc, {"path": request.url.path, "method": request.method})
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "status_code": exc.status_code,
            "details": exc.details
        }
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions"""
    log_error(exc, {"path": request.url.path, "method": request.method})
    
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An unexpected error occurred",
            "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
            "details": {"type": type(exc).__name__}
        }
    )
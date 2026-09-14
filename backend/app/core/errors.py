from enum import Enum
from typing import Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import Request

class ErrorCode(str, Enum):
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DB_UNAVAILABLE = "DB_UNAVAILABLE"
    DB_TIMEOUT = "DB_TIMEOUT"
    OLLAMA_UNAVAILABLE = "OLLAMA_UNAVAILABLE"
    OLLAMA_MODEL_MISSING = "OLLAMA_MODEL_MISSING"
    ANTHROPIC_MISSING_KEY = "ANTHROPIC_MISSING_KEY"
    ANTHROPIC_TIMEOUT = "ANTHROPIC_TIMEOUT"
    RETRIEVAL_FAILURE = "RETRIEVAL_FAILURE"
    EMBEDDING_FAILURE = "EMBEDDING_FAILURE"
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    INVALID_REQUEST = "INVALID_REQUEST"
    ARTIFACT_FAILURE = "ARTIFACT_FAILURE"
    PROVIDER_ERROR = "PROVIDER_ERROR"

class AppError(Exception):
    def __init__(self, code: ErrorCode, message: str, status_code: int = 500):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ErrorResponse(BaseModel):
    error_code: str
    message: str

async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.code.value, "message": exc.message}
    )

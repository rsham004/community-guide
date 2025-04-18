from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Optional
import time

from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_async_session
from app.services.llm_service import LLMService, get_llm_service, LLMServiceError
# Update import to use the LoggingService class instead of log_request function
from app.services.logging_service import LoggingService
from app.schemas.prompt import (
    AnalyzeRequest, AnalyzeResponse,
    RemixRequest, RemixResponse,
    CreateRequest, CreateResponse
)

router = APIRouter()

# Add a dependency to get the logging service
async def get_logging_service(session: AsyncSession = Depends(get_async_session)) -> LoggingService:
    return LoggingService(session)

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_prompt(
    request: Request,
    analyze_req: AnalyzeRequest,
    llm_service: LLMService = Depends(get_llm_service),
    logging_service: LoggingService = Depends(get_logging_service),
    session: AsyncSession = Depends(get_async_session)
):
    """Analyzes a prompt for clarity and suggests improvements."""
    start_time = time.time()
    try:
        # Process with LLM service
        result = await llm_service.analyze(analyze_req.prompt)
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Log request and response
        await logging_service.log_request(
            request=request,
            response=None,  # No access to actual response object in FastAPI
            status_code=status.HTTP_200_OK,
            processing_time_ms=processing_time_ms
        )
        
        return result
    except LLMServiceError as e:
        # Error logging is handled by exception handlers in main.py
        raise
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/remix", response_model=RemixResponse)
async def remix_prompt(
    request: Request,
    remix_req: RemixRequest,
    llm_service: LLMService = Depends(get_llm_service),
    logging_service: LoggingService = Depends(get_logging_service)
):
    """Generates variations of a prompt based on specified styles."""
    start_time = time.time()
    try:
        # Process with LLM service
        result = await llm_service.remix(remix_req.prompt, remix_req.styles)
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Log request and response
        await logging_service.log_request(
            request=request,
            response=None,
            status_code=status.HTTP_200_OK,
            processing_time_ms=processing_time_ms
        )
        
        return result
    except LLMServiceError as e:
        # Error logging is handled by exception handlers in main.py
        raise
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/create", response_model=CreateResponse)
async def create_prompt(
    request: Request,
    create_req: CreateRequest,
    llm_service: LLMService = Depends(get_llm_service),
    logging_service: LoggingService = Depends(get_logging_service)
):
    """Generates a new prompt based on a goal description."""
    start_time = time.time()
    try:
        # Process with LLM service
        result = await llm_service.create(create_req.goal, create_req.context)
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Log request and response
        await logging_service.log_request(
            request=request,
            response=None,
            status_code=status.HTTP_200_OK,
            processing_time_ms=processing_time_ms
        )
        
        return result
    except LLMServiceError as e:
        # Error logging is handled by exception handlers in main.py
        raise
    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

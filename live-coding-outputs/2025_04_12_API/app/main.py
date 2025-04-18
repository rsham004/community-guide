import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Import settings and database functions
from app.core.config import settings
from app.db.session import create_db_and_tables, close_db_connection, get_async_session
from app.services.llm_service import LLMServiceError, close_llm_service, get_llm_service
from app.services.logging_service import LoggingService  # This should be defined now
from app.schemas.prompt import ErrorDetail  # Make sure to use the correct import path

# Import API routers
from app.api.router import api_router

# Import models to ensure they are registered with SQLModel metadata
from app.models import log
try:
    from app.models import prompt_mgmt  # Import the new models module conditionally to handle if it's not created yet
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("prompt_mgmt models not found. This is expected if you haven't implemented Phase 6 yet.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up a dependency to get the logging service
async def get_logging_service(request: Request):
    """
    Dependency to get a LoggingService instance with a database session.
    Use this in endpoints where you need to log request/response info.
    """
    session = await get_async_session().__anext__()
    return LoggingService(session)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application startup...")
    try:
        # Ensure LLM Service can be initialized (catches API key issues early)
        await get_llm_service()
        logger.info("LLM Service initialized successfully.")
    except LLMServiceError as e:
        logger.error(f"LLM Service initialization failed: {e.detail}. Application might not function correctly.")
        # Decide if you want to halt startup: raise e

    try:
        await create_db_and_tables()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}. Halting application startup.")
        raise e # Halt startup if DB connection fails

    yield
    # Shutdown
    logger.info("Application shutdown...")
    await close_llm_service()
    await close_db_connection()
    logger.info("Application shutdown complete.")

# Create FastAPI app instance with lifespan management
app = FastAPI(
    title="PromptSculptor API",
    description="API for analyzing, remixing, creating, and managing AI prompts.",
    version="0.1.0",
    lifespan=lifespan,
    # Add OpenAPI URL prefix if needed, especially behind a proxy
    # openapi_url="/api/v1/openapi.json"
)

# --- Exception Handlers ---

@app.exception_handler(LLMServiceError)
async def llm_service_exception_handler(request: Request, exc: LLMServiceError):
    """Handles errors originating from the LLMService."""
    logger.error(f"LLM Service Error: {exc.detail}", exc_info=True)
    # Use the status code from the exception object
    status_code = exc.status_code
    error_detail = ErrorDetail(detail=f"LLM service error: {exc.detail}") # Simplified detail for client

    # Attempt to log the error to the database
    try:
        async for db in get_async_session():
             await log_request(
                 db=db,
                 endpoint=request.url.path,
                 status_code=status_code, # Log the actual status code
                 response_payload=error_detail,
                 timestamp=datetime.utcnow()
             )
             logger.info(f"LLMServiceError logged for endpoint: {request.url.path}")
    except Exception as log_e:
        logger.error(f"Failed to log LLMServiceError to DB: {log_e}", exc_info=True)

    return JSONResponse(
        status_code=status_code, # Return the correct status code
        content=error_detail.model_dump(),
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handles unexpected internal server errors."""
    logger.error(f"Unhandled Exception: {exc}", exc_info=True) # Log with traceback
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_detail = ErrorDetail(detail="An unexpected internal server error occurred.")

    # Attempt to log the error to the database
    try:
        async for db in get_async_session():
             await log_request(
                 db=db,
                 endpoint=request.url.path,
                 status_code=status_code,
                 response_payload=error_detail,
                 timestamp=datetime.utcnow()
             )
             logger.info(f"Unhandled Exception logged for endpoint: {request.url.path}")
    except Exception as log_e:
        logger.error(f"Failed to log unhandled Exception to DB: {log_e}", exc_info=True)

    return JSONResponse(
        status_code=status_code,
        content=error_detail.model_dump(),
    )


# --- Mount Routers ---
# Include the API router with a prefix for versioning
app.include_router(api_router, prefix="/api/v1")

# --- Health Check Endpoint ---
@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK, include_in_schema=True)
async def health_check():
    """
    Simple health check endpoint. Returns 200 OK if the server is running.
    """
    logger.debug("Health check endpoint accessed.")
    return {"status": "ok"}

# --- Basic Root Endpoint ---
@app.get("/", tags=["Status"], include_in_schema=False) # Hide root from OpenAPI docs
async def read_root():
    """
    Root endpoint providing a simple status message.
    """
    logger.info("Root endpoint '/' accessed.")
    return {"status": "PromptSculptor API is running"}

# --- Add Exception Handlers (Placeholder) ---
# Exception handlers will be added later in Phase 4
# Example:
# from fastapi import Request, status
# from fastapi.responses import JSONResponse
# from app.services.llm_service import LLMServiceError # Assuming this exists later
# from app.schemas.prompt import ErrorDetail
#
# @app.exception_handler(LLMServiceError)
# async def llm_service_exception_handler(request: Request, exc: LLMServiceError):
#     logger.error(f"LLM Service Error: {exc.detail}")
#     # Log the error details to the database via logging service (to be implemented)
#     # await log_error_to_db(...)
#     return JSONResponse(
#         status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#         content=ErrorDetail(detail=f"External LLM service error: {exc.detail}").model_dump(),
#     )

# Note: To run this application, you would typically use:
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

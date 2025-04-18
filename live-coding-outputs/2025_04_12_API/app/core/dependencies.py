from typing import AsyncGenerator
from fastapi import Request
from sqlmodel.ext.asyncio.session import AsyncSession

# Re-export database session dependency for easier access
from app.db.session import get_async_session

# Re-export LLM service dependency
from app.services.llm_service import get_llm_service, LLMService

from app.services.logging_service import LoggingService

async def get_logging_service(request: Request, session: AsyncSession = None) -> LoggingService:
    """
    Dependency to get a LoggingService instance with a database session.
    Use this in endpoints where you need to log request/response info.
    
    If session is not provided, it will try to get one from get_async_session.
    """
    if session is None:
        # Get a session from the dependency injection system
        # Note: This is a bit tricky because get_async_session is a generator,
        # we need to get the next value from it
        session_generator = get_async_session()
        session = await session_generator.__anext__()
    
    return LoggingService(session)

# You can add other common dependencies here as the application grows.
# For example, if you had a user authentication dependency:
# from app.auth import get_current_user

# Example of how to use in endpoints:
# from fastapi import Depends
# from app.core.dependencies import get_async_session, get_llm_service
#
# @router.post("/analyze")
# async def analyze_prompt(
#     request: AnalyzeRequest,
#     db: AsyncSession = Depends(get_async_session),
#     llm_service: LLMService = Depends(get_llm_service)
# ):
#     # ... use db and llm_service ...
#     pass

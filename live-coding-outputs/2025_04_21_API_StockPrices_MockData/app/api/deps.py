from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import AsyncSessionFactory

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides an async database session."""
    async with AsyncSessionFactory() as session:
        yield session

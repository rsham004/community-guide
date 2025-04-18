import logging
from contextlib import asynccontextmanager  # Add this import for asynccontextmanager
from typing import AsyncGenerator  # Add this import for type annotation
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine  # Import from sqlalchemy.ext.asyncio

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create the async engine instance
# Use check_same_thread=False only for SQLite as it's required for FastAPI's async access
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
async_engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True, connect_args=connect_args)

# Create the async session factory
AsyncSessionFactory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False, # Important for async sessions
)

async def get_async_session() -> AsyncSession:
    """Dependency to get an async database session."""
    async with AsyncSessionFactory() as session:
        yield session

async def create_db_and_tables():
    """Creates database tables based on SQLModel metadata."""
    logger.info("Attempting to create database tables...")
    async with async_engine.begin() as conn:
        try:
            # SQLModel uses the metadata from all imported models inheriting from SQLModel
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables checked/created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}", exc_info=True)
            raise # Re-raise the exception to potentially halt startup if critical

async def close_db_connection():
    """Closes the database engine connection."""
    logger.info("Closing database engine connection...")
    await async_engine.dispose()
    logger.info("Database engine connection closed.")

# Example of how you might get a sync session if ever needed (less common with FastAPI)
# sync_engine = create_engine(settings.DATABASE_URL.replace("+aiosqlite", ""), echo=False, connect_args=connect_args)
# SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
# def get_sync_session():
#     db = SyncSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@asynccontextmanager
async def get_standalone_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for getting an async session outside of FastAPI request cycle.
    Useful for background tasks or scripts.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

import os
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession # Keep AsyncSession import
from sqlalchemy.ext.asyncio import create_async_engine # Import create_async_engine from sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback or raise error if DATABASE_URL is not set
    # For this prototype, we'll use a default in-memory SQLite if not set,
    # but ideally, the .env file should be configured.
    print("Warning: DATABASE_URL not found in .env file. Using default in-memory SQLite.")
    DATABASE_URL = "sqlite+aiosqlite:///./mock_stock_default.db" # Default to a file-based DB

# Create the async engine
# connect_args is specific to SQLite to ensure the same thread isn't checked
# (necessary for FastAPI's async nature with SQLite)
engine = create_async_engine(DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False})

# Async session factory
AsyncSessionFactory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def create_db_and_tables():
    """Creates database tables based on SQLModel metadata."""
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Use this to drop tables if needed
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get an async database session."""
    async with AsyncSessionFactory() as session:
        yield session

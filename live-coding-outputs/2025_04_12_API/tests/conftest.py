import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, Generator
import os
from fastapi.testclient import TestClient

# Import your FastAPI app and settings
from app.main import app
from app.core.config import Settings, get_settings
from app.db.session import get_async_session

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_promptsculptor.db"

# Ensure the test database file does not exist before tests run
if os.path.exists("./test_promptsculptor.db"):
    os.remove("./test_promptsculptor.db")

# Create a test engine instance
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False}
)

# Create a test session factory
TestAsyncSessionFactory = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Override the get_settings dependency for testing if needed
# def get_test_settings() -> Settings:
#     return Settings(DATABASE_URL=TEST_DATABASE_URL, LLM_API_KEY="TEST_KEY")

# Override the get_async_session dependency for testing
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionFactory() as session:
        try:
            yield session
            await session.commit() # Commit changes made during tests
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Apply overrides to the app
# app.dependency_overrides[get_settings] = get_test_settings
app.dependency_overrides[get_async_session] = override_get_async_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Create test database and tables before tests run, drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Teardown: Drop all tables after tests are done
    # async with test_engine.begin() as conn:
    #     await conn.run_sync(SQLModel.metadata.drop_all)
    # Optional: Delete the test DB file if desired
    if os.path.exists("./test_promptsculptor.db"):
         os.remove("./test_promptsculptor.db")


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture to get a test database session for individual tests."""
    async with TestAsyncSessionFactory() as session:
        yield session
        await session.rollback() # Rollback any changes after each test function

@pytest_asyncio.fixture(scope="session")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture to create an httpx AsyncClient for testing the API."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture(scope="function")
def client(db_session: AsyncSession) -> Generator[TestClient, None, None]:
    """Provides a TestClient instance with overridden DB session dependency."""

    # Override the get_async_session dependency for the app
    def override_get_async_session():
        return db_session  # Use the session provided by the db_session fixture

    app.dependency_overrides[get_async_session] = override_get_async_session
    with TestClient(app) as c:
        yield c
    # Clean up dependency override after test
    app.dependency_overrides.pop(get_async_session, None)

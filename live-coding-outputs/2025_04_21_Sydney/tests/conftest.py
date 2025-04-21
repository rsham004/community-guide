import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession # Keep this
from sqlalchemy.ext.asyncio import create_async_engine # Correct import source
from sqlalchemy.orm import sessionmaker

# Import the main FastAPI app
from app.main import app
from app.db.session import get_session # Import the original dependency getter
from app.crud.crud_stock import seed_initial_data # Import the seeding function

# Use a separate SQLite database for testing (in-memory)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a test engine and session factory
test_engine = create_async_engine(
    TEST_DATABASE_URL, echo=False, future=True, connect_args={"check_same_thread": False}
)
TestAsyncSessionFactory = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

async def create_test_db_and_tables():
    """Creates test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all) # Ensure clean state
        await conn.run_sync(SQLModel.metadata.create_all)

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency override for test sessions."""
    async with TestAsyncSessionFactory() as session:
        yield session

# Apply the override to the app
app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="session")
def event_loop(request) -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Set up the test database tables once per session."""
    await create_test_db_and_tables()

@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provides an asynchronous test client for making API requests."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Note: We might need another fixture later to seed data into the test DB
# before tests that require pre-existing data.

@pytest.fixture(scope="function", autouse=True)
async def seed_test_db_data():
    """Seeds the test database with mock data before each test function."""
    # Use the overridden session factory for seeding
    async with TestAsyncSessionFactory() as session:
        # Seed a smaller amount of data for tests to keep them fast
        await seed_initial_data(session, num_days=10)
    # No yield needed, just run before each test due to autouse=True


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a clean, async database session for unit tests."""
    async with TestAsyncSessionFactory() as session:
        yield session

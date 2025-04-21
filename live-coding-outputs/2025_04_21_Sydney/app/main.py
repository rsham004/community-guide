from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import create_db_and_tables, AsyncSessionFactory # Import session factory
from app.crud.crud_stock import seed_initial_data # Import the seeding function
# Import routers later when they are created
from app.api.routers import stocks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Application startup: Creating database and tables...")
    await create_db_and_tables()
    print("Application startup: Database and tables created.")

    # Seed initial data
    print("Application startup: Seeding initial data...")
    async with AsyncSessionFactory() as session: # Create a session for seeding
        await seed_initial_data(session)
    print("Application startup: Initial data seeding process complete.")

    yield
    # Code to run on shutdown (if any)
    print("Application shutdown.")

# Initialize FastAPI app with lifespan manager
app = FastAPI(
    title="Mock Stock Market Data API",
    description="Provides mock stock quotes and historical data.",
    version="0.1.0",
    lifespan=lifespan
)

# Placeholder root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Mock Stock Market Data API!"}

# Include API routers (uncomment when ready)
app.include_router(stocks.router, prefix="/api/v1", tags=["stocks"])

# Note: The actual API endpoints will be added in Phase 3 via routers.

from sqlmodel import SQLModel
import logging
from typing import Optional

from app.database.db import engine
from app.database.models import User, Location, Taco, Review, Follow, Achievement, UserAchievement

logger = logging.getLogger(__name__)

def create_db_and_tables():
    """Create database tables from SQLModel classes"""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")

def reset_database():
    """Drop all tables and recreate them (Warning: all data will be lost)"""
    logger.warning("Dropping all database tables...")
    SQLModel.metadata.drop_all(engine)
    logger.warning("Database tables dropped")
    create_db_and_tables()
    logger.info("Database reset complete")

def check_database_initialized() -> bool:
    """Check if database is initialized by testing if tables exist"""
    try:
        with engine.connect() as conn:
            # Try to query User table to check if it exists
            result = conn.execute("SELECT 1 FROM user LIMIT 1")
            return True
    except Exception as e:
        logger.warning(f"Database check failed: {str(e)}")
        return False

def init_db(reset: Optional[bool] = False):
    """Initialize database - create tables if they don't exist or reset if specified"""
    if reset:
        reset_database()
    elif not check_database_initialized():
        create_db_and_tables()
    else:
        logger.info("Database already initialized")

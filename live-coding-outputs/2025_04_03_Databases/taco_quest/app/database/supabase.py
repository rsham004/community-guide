"""
Supabase connection and operations module for Taco Quest.
This module provides functions for interacting with Supabase.
"""
import logging
import json
from typing import Dict, List, Any, Optional
from supabase import create_client, Client
from sqlmodel import Session, select

from app.config.settings import SUPABASE_URL, SUPABASE_KEY
from app.database.models import User, Location, Taco, Review, Follow, Achievement, UserAchievement

logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    """Create and return a Supabase client instance."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.debug("Supabase client created successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {str(e)}")
        raise

def test_supabase_connection() -> bool:
    """Test if we can connect to Supabase."""
    try:
        client = get_supabase_client()
        # Simple authentication check
        auth_response = client.auth.get_user()
        logger.info("Supabase connection test successful")
        return True
    except Exception as e:
        logger.error(f"Supabase connection test failed: {str(e)}")
        return False

def create_supabase_tables() -> bool:
    """
    Create tables in Supabase using direct SQL.
    
    Returns:
        bool: True if successful, False otherwise
    """
    client = get_supabase_client()
    logger.info("Creating tables in Supabase...")
    
    try:
        # We'll use raw SQL to create tables via the PostgreSQL interface
        # Note: This assumes the service role key has sufficient privileges
        
        # Create User table
        client.rpc(
            "exec_sql", 
            {"sql": """
                CREATE TABLE IF NOT EXISTS "user" (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username);
                CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
            """}
        ).execute()
        logger.info("Created User table")
        
        # Create Location table
        client.rpc(
            "exec_sql",
            {"sql": """
                CREATE TABLE IF NOT EXISTS location (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    lat FLOAT NOT NULL,
                    lon FLOAT NOT NULL
                );
            """}
        ).execute()
        logger.info("Created Location table")
        
        # Create Taco table
        client.rpc(
            "exec_sql",
            {"sql": """
                CREATE TABLE IF NOT EXISTS taco (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    location_id INTEGER REFERENCES location(id)
                );
            """}
        ).execute()
        logger.info("Created Taco table")
        
        # Create Review table
        client.rpc(
            "exec_sql",
            {"sql": """
                CREATE TABLE IF NOT EXISTS review (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES "user"(id),
                    taco_id INTEGER REFERENCES taco(id),
                    rating INTEGER NOT NULL,
                    comment TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """}
        ).execute()
        logger.info("Created Review table")
        
        # Create Follow table
        client.rpc(
            "exec_sql",
            {"sql": """
                CREATE TABLE IF NOT EXISTS follow (
                    id SERIAL PRIMARY KEY,
                    follower_id INTEGER REFERENCES "user"(id),
                    following_id INTEGER REFERENCES "user"(id),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """}
        ).execute()
        logger.info("Created Follow table")
        
        # Create Achievement table
        client.rpc(
            "exec_sql",
            {"sql": """
                CREATE TABLE IF NOT EXISTS achievement (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL
                );
            """}
        ).execute()
        logger.info("Created Achievement table")
        
        # Create UserAchievement table
        client.rpc(
            "exec_sql",
            {"sql": """
                CREATE TABLE IF NOT EXISTS userachievement (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES "user"(id),
                    achievement_id INTEGER REFERENCES achievement(id),
                    earned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """}
        ).execute()
        logger.info("Created UserAchievement table")
        
        logger.info("Successfully created all tables in Supabase")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create Supabase tables: {str(e)}")
        return False

def migrate_data_to_supabase(session: Session):
    """
    Migrate all data from local SQLite database to Supabase.
    
    Args:
        session: SQLModel session for the local database
    """
    client = get_supabase_client()
    
    # Migrate Users
    logger.info("Migrating Users to Supabase...")
    users = session.exec(select(User)).all()
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
        try:
            client.table("user").insert(user_data).execute()
        except Exception as e:
            logger.error(f"Failed to migrate User {user.id}: {str(e)}")
    
    # Migrate Locations
    logger.info("Migrating Locations to Supabase...")
    locations = session.exec(select(Location)).all()
    for location in locations:
        location_data = {
            "id": location.id,
            "name": location.name,
            "address": location.address,
            "lat": location.lat,
            "lon": location.lon
        }
        try:
            client.table("location").insert(location_data).execute()
        except Exception as e:
            logger.error(f"Failed to migrate Location {location.id}: {str(e)}")
    
    # Migrate Tacos
    logger.info("Migrating Tacos to Supabase...")
    tacos = session.exec(select(Taco)).all()
    for taco in tacos:
        taco_data = {
            "id": taco.id,
            "name": taco.name,
            "description": taco.description,
            "location_id": taco.location_id
        }
        try:
            client.table("taco").insert(taco_data).execute()
        except Exception as e:
            logger.error(f"Failed to migrate Taco {taco.id}: {str(e)}")
    
    # Migrate Reviews
    logger.info("Migrating Reviews to Supabase...")
    reviews = session.exec(select(Review)).all()
    for review in reviews:
        review_data = {
            "id": review.id,
            "user_id": review.user_id,
            "taco_id": review.taco_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat()
        }
        try:
            client.table("review").insert(review_data).execute()
        except Exception as e:
            logger.error(f"Failed to migrate Review {review.id}: {str(e)}")
    
    # Migrate Follows
    logger.info("Migrating Follows to Supabase...")
    follows = session.exec(select(Follow)).all()
    for follow in follows:
        follow_data = {
            "id": follow.id,
            "follower_id": follow.follower_id,
            "following_id": follow.following_id,
            "created_at": follow.created_at.isoformat()
        }
        try:
            client.table("follow").insert(follow_data).execute()
        except Exception as e:
            logger.error(f"Failed to migrate Follow {follow.id}: {str(e)}")
    
    # Migrate Achievements
    logger.info("Migrating Achievements to Supabase...")
    achievements = session.exec(select(Achievement)).all()
    for achievement in achievements:
        achievement_data = {
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description
        }
        try:
            client.table("achievement").insert(achievement_data).execute()
        except Exception as e:
            logger.error(f"Failed to migrate Achievement {achievement.id}: {str(e)}")
    
    # Migrate UserAchievements
    logger.info("Migrating UserAchievements to Supabase...")
    user_achievements = session.exec(select(UserAchievement)).all()
    for user_achievement in user_achievements:
        user_achievement_data = {
            "id": user_achievement.id,
            "user_id": user_achievement.user_id,
            "achievement_id": user_achievement.achievement_id,
            "earned_at": user_achievement.earned_at.isoformat()
        }
        try:
            client.table("userachievement").insert(user_achievement_data).execute()
        except Exception as e:
            logger.error(f"Failed to migrate UserAchievement {user_achievement.id}: {str(e)}")
    
    logger.info("Data migration to Supabase complete!")

def get_supabase_stats() -> Dict[str, int]:
    """
    Get statistics from Supabase tables.
    
    Returns:
        Dictionary with counts of records in each table
    """
    client = get_supabase_client()
    stats = {}
    
    try:
        # Get User count
        user_result = client.table("user").select("id", count="exact").execute()
        stats["users"] = user_result.count
        
        # Get Location count
        location_result = client.table("location").select("id", count="exact").execute()
        stats["locations"] = location_result.count
        
        # Get Taco count
        taco_result = client.table("taco").select("id", count="exact").execute()
        stats["tacos"] = taco_result.count
        
        # Get Review count
        review_result = client.table("review").select("id", count="exact").execute()
        stats["reviews"] = review_result.count
        
        # Get Follow count
        follow_result = client.table("follow").select("id", count="exact").execute()
        stats["follows"] = follow_result.count
        
        # Get Achievement count
        achievement_result = client.table("achievement").select("id", count="exact").execute()
        stats["achievements"] = achievement_result.count
        
        # Get UserAchievement count
        user_achievement_result = client.table("userachievement").select("id", count="exact").execute()
        stats["user_achievements"] = user_achievement_result.count
        
        logger.info(f"Supabase stats: {json.dumps(stats, indent=2)}")
        return stats
    except Exception as e:
        logger.error(f"Failed to get Supabase stats: {str(e)}")
        return {}

import logging
import argparse
from app.database.init_db import init_db
from app.database.db import get_session
from app.database.models import User, Location, Taco, Review, Follow, Achievement, UserAchievement
from app.seeds.seed_data import seed_all
from app.utils.query_examples import demonstrate_queries
from app.utils.debugging import debug_environment, test_supabase
from app.database.supabase import migrate_data_to_supabase, create_supabase_tables
from app.config.settings import USE_SUPABASE
from sqlmodel import select

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Taco Quest Database Management")
    parser.add_argument(
        "--reset", 
        action="store_true", 
        help="Reset the database (WARNING: All data will be lost)"
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed the database with mock data"
    )
    parser.add_argument(
        "--users",
        type=int,
        default=10,
        help="Number of users to create when seeding (default: 10)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo queries to show database capabilities"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show debug information about the environment and configuration"
    )
    parser.add_argument(
        "--test-supabase",
        action="store_true",
        help="Test the Supabase connection"
    )
    parser.add_argument(
        "--create-supabase-schema",
        action="store_true",
        help="Create the tables in Supabase before migration"
    )
    parser.add_argument(
        "--migrate-to-supabase",
        action="store_true",
        help="Migrate data from local SQLite to Supabase"
    )
    args = parser.parse_args()
    
    # Show debug information if requested
    if args.debug:
        debug_environment()
    
    # Test Supabase connection if requested
    if args.test_supabase:
        test_supabase()
        return
    
    # Create Supabase schema if requested
    if args.create_supabase_schema:
        logger.info("Creating Supabase schema...")
        success = create_supabase_tables()
        if success:
            logger.info("Supabase schema created successfully!")
        else:
            logger.error("Failed to create Supabase schema.")
        return
    
    # Initialize database
    logger.info("Initializing database...")
    init_db(reset=args.reset)
    
    # Seed database if requested
    if args.seed:
        logger.info(f"Seeding database with {args.users} users...")
        with get_session() as session:
            seed_all(session, num_users=args.users)
    
    # Migrate data to Supabase if requested
    if args.migrate_to_supabase:
        logger.info("Migrating data to Supabase...")
        with get_session() as session:
            migrate_data_to_supabase(session)
    
    # Run demo queries if requested
    if args.demo:
        logger.info("Running query demonstrations...")
        with get_session() as session:
            demonstrate_queries(session)
    
    # Test database connection and show stats
    logger.info("Database statistics:")
    with get_session() as session:
        # Check if we have any users
        user_count = session.exec(select(User)).count()
        logger.info(f"Users: {user_count}")
        
        # Check if we have any locations
        location_count = session.exec(select(Location)).count()
        logger.info(f"Locations: {location_count}")
        
        # Check if we have any tacos
        taco_count = session.exec(select(Taco)).count()
        logger.info(f"Tacos: {taco_count}")
        
        # Check reviews
        review_count = session.exec(select(Review)).count()
        logger.info(f"Reviews: {review_count}")
        
        # Check follows
        follow_count = session.exec(select(Follow)).count()
        logger.info(f"Follows: {follow_count}")
        
        # Check achievements
        achievement_count = session.exec(select(Achievement)).count()
        logger.info(f"Achievements: {achievement_count}")
        
        # Check user achievements
        user_achievement_count = session.exec(select(UserAchievement)).count()
        logger.info(f"User Achievements: {user_achievement_count}")
    
    # Indicate if we're using Supabase
    if USE_SUPABASE:
        logger.info("Using Supabase as the database backend")
    
    logger.info("Database test complete!")

if __name__ == "__main__":
    main()

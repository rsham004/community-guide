"""
Examples of advanced queries and operations with the Taco Quest database.
This module demonstrates how to work with the models and relationships.
"""
import logging
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select, func, or_, and_
from app.database.models import User, Location, Taco, Review, Follow, Achievement, UserAchievement

logger = logging.getLogger(__name__)

def find_top_rated_tacos(session: Session, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Find the top-rated tacos based on average review score.
    
    Args:
        session: Database session
        limit: Maximum number of tacos to return
        
    Returns:
        List of dictionaries with taco details and average rating
    """
    statement = (
        select(
            Taco.id,
            Taco.name,
            Taco.description,
            func.avg(Review.rating).label("average_rating"),
            func.count(Review.id).label("review_count"),
            Location.name.label("location_name"),
            Location.address
        )
        .join(Review, Taco.id == Review.taco_id)
        .join(Location, Taco.location_id == Location.id)
        .group_by(Taco.id, Location.name, Location.address)
        .order_by(func.avg(Review.rating).desc())  # Fixed: Use the function directly instead of col()
        .limit(limit)
    )
    
    results = session.execute(statement).all()
    
    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "average_rating": round(r.average_rating, 2),
            "review_count": r.review_count,
            "location_name": r.location_name,
            "address": r.address
        }
        for r in results
    ]

def find_nearest_tacos(
    session: Session, latitude: float, longitude: float, limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Find tacos nearest to a given latitude and longitude.
    Uses a simplified distance calculation.
    
    Args:
        session: Database session
        latitude: User's latitude
        longitude: User's longitude
        limit: Maximum number of locations to return
        
    Returns:
        List of dictionaries with location and taco details
    """
    # This is a simple approximation - for real-world use, 
    # a more accurate geospatial calculation would be better
    statement = (
        select(
            Location.id,
            Location.name,
            Location.address,
            Location.lat,
            Location.lon,
            # Simple distance calculation using Pythagorean theorem
            func.sqrt(
                func.pow(Location.lat - latitude, 2) + 
                func.pow(Location.lon - longitude, 2)
            ).label("distance")
        )
        .order_by(
            func.sqrt(
                func.pow(Location.lat - latitude, 2) + 
                func.pow(Location.lon - longitude, 2)
            )
        )
        .limit(limit)
    )
    
    locations = session.execute(statement).all()
    results = []
    
    for loc in locations:
        # Get tacos for this location
        taco_statement = (
            select(Taco)
            .where(Taco.location_id == loc.id)
        )
        tacos = session.execute(taco_statement).all()
        
        results.append({
            "location_id": loc.id,
            "location_name": loc.name,
            "address": loc.address,
            "latitude": loc.lat,
            "longitude": loc.lon,
            "distance_km": round(loc.distance * 111, 2),  # rough conversion to km
            "tacos": [{"id": t[0].id, "name": t[0].name, "description": t[0].description} 
                     for t in tacos]
        })
    
    return results

def get_user_feed(session: Session, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get a feed of recent reviews from users that a given user follows.
    
    Args:
        session: Database session
        user_id: ID of the user requesting the feed
        limit: Maximum number of reviews to return
        
    Returns:
        List of dictionaries with review details
    """
    # Find IDs of users that this user follows
    following_statement = (
        select(Follow.following_id)
        .where(Follow.follower_id == user_id)
    )
    following_ids = [f[0] for f in session.execute(following_statement).all()]
    
    if not following_ids:
        return []
    
    # Get recent reviews from followed users
    review_statement = (
        select(
            Review.id,
            Review.rating,
            Review.comment,
            Review.created_at,
            User.username,
            Taco.name.label("taco_name"),
            Location.name.label("location_name")
        )
        .join(User, Review.user_id == User.id)
        .join(Taco, Review.taco_id == Taco.id)
        .join(Location, Taco.location_id == Location.id)
        .where(Review.user_id.in_(following_ids))
        .order_by(Review.created_at.desc())
        .limit(limit)
    )
    
    reviews = session.execute(review_statement).all()
    
    return [
        {
            "review_id": r.id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat(),
            "username": r.username,
            "taco_name": r.taco_name,
            "location_name": r.location_name
        }
        for r in reviews
    ]

def get_user_stats(session: Session, user_id: int) -> Dict[str, Any]:
    """
    Get comprehensive statistics for a given user.
    
    Args:
        session: Database session
        user_id: ID of the user
        
    Returns:
        Dictionary with user statistics
    """
    # Get basic user info
    user = session.get(User, user_id)
    if not user:
        return {"error": "User not found"}
    
    # Count reviews
    review_count = session.exec(select(Review).where(Review.user_id == user_id)).count()
    
    # Calculate average rating given
    avg_rating_stmt = (
        select(func.avg(Review.rating))
        .where(Review.user_id == user_id)
    )
    avg_rating_result = session.execute(avg_rating_stmt).first()
    avg_rating = round(avg_rating_result[0], 2) if avg_rating_result[0] else 0
    
    # Count followers
    follower_count = session.exec(select(Follow).where(Follow.following_id == user_id)).count()
    
    # Count following
    following_count = session.exec(select(Follow).where(Follow.follower_id == user_id)).count()
    
    # Count achievements
    achievement_count = session.exec(select(UserAchievement).where(UserAchievement.user_id == user_id)).count()
    
    # Get list of visited locations (from reviews)
    location_stmt = (
        select(Location.id, Location.name)
        .join(Taco, Location.id == Taco.location_id)
        .join(Review, Taco.id == Review.taco_id)
        .where(Review.user_id == user_id)
        .distinct()
    )
    locations = session.execute(location_stmt).all()
    
    # Get most recent review
    recent_review_stmt = (
        select(Review, Taco.name.label("taco_name"))
        .join(Taco, Review.taco_id == Taco.id)
        .where(Review.user_id == user_id)
        .order_by(Review.created_at.desc())
        .limit(1)
    )
    recent_review_result = session.execute(recent_review_stmt).first()
    recent_review = None
    if recent_review_result:
        review, taco_name = recent_review_result
        recent_review = {
            "taco_name": taco_name,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat()
        }
    
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "review_count": review_count,
        "average_rating": avg_rating,
        "follower_count": follower_count,
        "following_count": following_count,
        "achievement_count": achievement_count,
        "locations_visited": [{"id": loc.id, "name": loc.name} for loc in locations],
        "most_recent_review": recent_review
    }

def demonstrate_queries(session: Session):
    """Run and print example queries to demonstrate capabilities"""
    logger.info("Demonstrating database queries...")
    
    # Example 1: Top-rated tacos
    logger.info("EXAMPLE 1: Finding top-rated tacos")
    top_tacos = find_top_rated_tacos(session)
    for taco in top_tacos:
        logger.info(f"Taco: {taco['name']} - Rating: {taco['average_rating']} ⭐ ({taco['review_count']} reviews)")
        logger.info(f"Location: {taco['location_name']} - {taco['address']}")
    
    # Example 2: Find tacos near Minneapolis
    logger.info("\nEXAMPLE 2: Finding tacos near downtown Minneapolis")
    minneapolis_lat, minneapolis_lon = 44.9778, -93.2650  # Downtown Minneapolis
    nearby_tacos = find_nearest_tacos(session, minneapolis_lat, minneapolis_lon)
    for location in nearby_tacos:
        logger.info(f"Location: {location['location_name']} - {location['distance_km']} km away")
        logger.info(f"Address: {location['address']}")
        for taco in location['tacos']:
            logger.info(f"  - {taco['name']}: {taco['description']}")
    
    # Example 3: Get a user's feed
    logger.info("\nEXAMPLE 3: Getting a user's feed of followed users' reviews")
    # Get the first user from the database
    first_user = session.exec(select(User).limit(1)).first()
    if first_user:
        feed = get_user_feed(session, first_user.id)
        logger.info(f"Feed for user: {first_user.username}")
        for item in feed:
            logger.info(f"{item['username']} rated {item['taco_name']} at {item['location_name']} {item['rating']}⭐")
            if item['comment']:
                logger.info(f"Comment: \"{item['comment']}\"")
    
    # Example 4: Get user statistics
    logger.info("\nEXAMPLE 4: Getting comprehensive user statistics")
    if first_user:
        stats = get_user_stats(session, first_user.id)
        logger.info(f"Stats for user: {stats['username']}")
        logger.info(f"Member since: {stats['created_at']}")
        logger.info(f"Reviews: {stats['review_count']}")
        logger.info(f"Average rating given: {stats['average_rating']}⭐")
        logger.info(f"Followers: {stats['follower_count']}")
        logger.info(f"Following: {stats['following_count']}")
        logger.info(f"Achievements: {stats['achievement_count']}")
        logger.info(f"Locations visited: {len(stats['locations_visited'])}")
        
        if stats['most_recent_review']:
            logger.info(f"Most recent review: {stats['most_recent_review']['taco_name']} - {stats['most_recent_review']['rating']}⭐")
    
    logger.info("Query demonstration complete!")

if __name__ == "__main__":
    # This module can be run directly for testing
    from app.database.db import get_session
    
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    with get_session() as session:
        demonstrate_queries(session)

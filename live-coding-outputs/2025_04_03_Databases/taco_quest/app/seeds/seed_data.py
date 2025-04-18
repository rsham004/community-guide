import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from sqlmodel import Session
from app.database.models import User, Location, Taco, Review, Follow, Achievement, UserAchievement
from app.utils.helpers import get_crud_helper

logger = logging.getLogger(__name__)

# CRUD helpers for each model
user_crud = get_crud_helper(User)
location_crud = get_crud_helper(Location)
taco_crud = get_crud_helper(Taco)
review_crud = get_crud_helper(Review)
follow_crud = get_crud_helper(Follow)
achievement_crud = get_crud_helper(Achievement)
user_achievement_crud = get_crud_helper(UserAchievement)

# Mock data generation
def create_users(session: Session, count: int = 10) -> List[User]:
    """Create mock user data"""
    logger.info(f"Creating {count} mock users")
    
    usernames = [
        "tacofan", "salsalover", "guacdude", "burritoboss", "chipotlequeen",
        "tortillamaster", "quesadillaking", "enchiladalady", "jalapenohead", 
        "nachoexpert", "tacotuesday", "carneasada", "potatotaco", "vegantacofan",
        "spicylover", "tacotruckchaser", "streettacofan", "tacocat", "cilantrofan", 
        "limesqueezer"
    ]
    
    domains = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "icloud.com"]
    
    users = []
    used_usernames = set()
    
    for i in range(count):
        # Get a unique username
        username = random.choice(usernames)
        while username in used_usernames and len(used_usernames) < len(usernames):
            username = random.choice(usernames)
        used_usernames.add(username)
        
        if i >= len(usernames):
            username = f"{random.choice(usernames)}{random.randint(1, 999)}"
            
        email = f"{username}{random.randint(1, 999)}@{random.choice(domains)}"
        
        # Create registration date (between 1 and 365 days ago)
        days_ago = random.randint(1, 365)
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        user = User(username=username, email=email, created_at=created_at)
        user = user_crud.create(session, user)
        users.append(user)
        
    logger.info(f"Created {len(users)} users")
    return users

def create_locations(session: Session, count: int = 8) -> List[Location]:
    """Create mock location data focusing on Minneapolis/St. Paul area"""
    logger.info(f"Creating {count} mock locations")
    
    # Minneapolis/St. Paul area locations with approximate coordinates
    mn_locations = [
        {"name": "Taco Stand", "address": "123 Lake St, Minneapolis, MN 55408", "lat": 44.9483, "lon": -93.2474},
        {"name": "Taqueria El Ranchito", "address": "456 University Ave, St. Paul, MN 55104", "lat": 44.9559, "lon": -93.1731},
        {"name": "Fiesta Cantina", "address": "789 Hennepin Ave, Minneapolis, MN 55403", "lat": 44.9778, "lon": -93.2772},
        {"name": "Los Tacos Food Truck", "address": "Nicollet Mall, Minneapolis, MN 55402", "lat": 44.9762, "lon": -93.2763},
        {"name": "Taco Palace", "address": "567 Grand Ave, St. Paul, MN 55105", "lat": 44.9402, "lon": -93.1359},
        {"name": "El Jalapeno Grill", "address": "901 West 7th St, St. Paul, MN 55102", "lat": 44.9340, "lon": -93.1277},
        {"name": "Taco Shack", "address": "345 Eat Street, Minneapolis, MN 55404", "lat": 44.9628, "lon": -93.2779},
        {"name": "Uptown Tacos", "address": "1212 Lagoon Ave, Minneapolis, MN 55408", "lat": 44.9490, "lon": -93.2984},
        {"name": "Salsa Spot", "address": "678 Snelling Ave, St. Paul, MN 55104", "lat": 44.9530, "lon": -93.1668},
        {"name": "Taco Fuego", "address": "432 Central Ave NE, Minneapolis, MN 55413", "lat": 45.0014, "lon": -93.2471},
    ]
    
    # Use only the number of locations requested
    mn_locations = mn_locations[:count]
    
    locations = []
    for loc_data in mn_locations:
        location = Location(**loc_data)
        location = location_crud.create(session, location)
        locations.append(location)
    
    logger.info(f"Created {len(locations)} locations")
    return locations

def create_tacos(session: Session, locations: List[Location], count_per_location: int = 3) -> List[Taco]:
    """Create mock taco data for each location"""
    logger.info(f"Creating {count_per_location} tacos per location")
    
    taco_data = [
        {"name": "Carne Asada", "description": "Grilled steak with cilantro, onions, and salsa verde."},
        {"name": "Al Pastor", "description": "Marinated pork with pineapple, cilantro, and onions."},
        {"name": "Carnitas", "description": "Slow-cooked pork with salsa, cilantro, and onions."},
        {"name": "Chicken Tinga", "description": "Shredded chicken in chipotle sauce with avocado."},
        {"name": "Barbacoa", "description": "Slow-cooked beef with lime and salsa roja."},
        {"name": "Fish Taco", "description": "Battered fish with cabbage slaw and lime crema."},
        {"name": "Shrimp Taco", "description": "Grilled shrimp with mango salsa and chipotle mayo."},
        {"name": "Vegetarian", "description": "Black beans, avocado, cheese, and pico de gallo."},
        {"name": "Nopales", "description": "Grilled cactus with queso fresco and salsa verde."},
        {"name": "Breakfast Taco", "description": "Scrambled eggs, chorizo, cheese, and salsa."},
        {"name": "Birria", "description": "Slow-cooked beef in adobo with melted cheese and consomé."},
        {"name": "Lengua", "description": "Beef tongue with onions, cilantro, and salsa."},
        {"name": "Chorizo", "description": "Spicy pork sausage with potatoes and salsa."},
        {"name": "Potato", "description": "Seasoned potatoes with cheese and pico de gallo."},
        {"name": "Cauliflower", "description": "Roasted cauliflower with cashew crema and pickled onions."}
    ]
    
    tacos = []
    
    for location in locations:
        # Create a subset of tacos for this location
        available_tacos = random.sample(taco_data, min(count_per_location, len(taco_data)))
        
        for taco_dict in available_tacos:
            taco = Taco(
                name=taco_dict["name"],
                description=taco_dict["description"],
                location_id=location.id
            )
            taco = taco_crud.create(session, taco)
            tacos.append(taco)
    
    logger.info(f"Created {len(tacos)} tacos across all locations")
    return tacos

def create_reviews(session: Session, users: List[User], tacos: List[Taco], max_reviews_per_user: int = 5) -> List[Review]:
    """Create mock review data"""
    logger.info("Creating mock reviews")
    
    positive_comments = [
        "Absolutely delicious! Will be back for more.",
        "Best taco I've had in a long time.",
        "Perfect amount of spice and flavor.",
        "The tortilla was so fresh and the filling was amazing.",
        "Authentic taste and generous portions.",
        "Great balance of flavors.",
        "Loved the salsa that came with it!",
        "So good I ordered seconds.",
        "Perfectly seasoned and cooked just right."
    ]
    
    neutral_comments = [
        "It was okay, nothing special.",
        "Decent but I've had better.",
        "Good, but a bit pricey for what you get.",
        "Not bad but wouldn't go out of my way for it.",
        "Average taco, nothing memorable."
    ]
    
    negative_comments = [
        "Too dry for my taste.",
        "Way too spicy without enough flavor.",
        "The meat was tough and under-seasoned.",
        "Tortilla fell apart as I was eating it.",
        "Disappointed with the portion size."
    ]
    
    reviews = []
    
    for user in users:
        # Each user reviews a random number of tacos (up to max_reviews_per_user)
        num_reviews = random.randint(0, min(max_reviews_per_user, len(tacos)))
        tacos_to_review = random.sample(tacos, num_reviews)
        
        for taco in tacos_to_review:
            # Generate a random rating (1-5)
            rating = random.randint(1, 5)
            
            # Select an appropriate comment based on rating
            if rating >= 4:
                comment = random.choice(positive_comments)
            elif rating == 3:
                comment = random.choice(neutral_comments)
            else:
                comment = random.choice(negative_comments)
            
            # Add some randomization - sometimes no comment
            if random.random() < 0.2:
                comment = None
            
            # Create a review date (between taco's location creation and now)
            days_ago = random.randint(0, 180)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            review = Review(
                user_id=user.id,
                taco_id=taco.id,
                rating=rating,
                comment=comment,
                created_at=created_at
            )
            review = review_crud.create(session, review)
            reviews.append(review)
    
    logger.info(f"Created {len(reviews)} reviews")
    return reviews

def create_follows(session: Session, users: List[User], max_follows_per_user: int = 5) -> List[Follow]:
    """Create follow relationships between users"""
    logger.info("Creating follow relationships")
    
    follows = []
    
    for follower in users:
        # Create a list of potential users to follow (excluding self)
        potential_followings = [u for u in users if u.id != follower.id]
        
        # Randomly decide how many users to follow (up to max_follows_per_user)
        num_follows = random.randint(0, min(max_follows_per_user, len(potential_followings)))
        
        # Randomly select users to follow
        followings = random.sample(potential_followings, num_follows)
        
        for following in followings:
            # Create a follow date (between follower's creation and now)
            days_ago = random.randint(0, 180)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            follow = Follow(
                follower_id=follower.id,
                following_id=following.id,
                created_at=created_at
            )
            follow = follow_crud.create(session, follow)
            follows.append(follow)
    
    logger.info(f"Created {len(follows)} follow relationships")
    return follows

def create_achievements(session: Session) -> List[Achievement]:
    """Create achievement definitions"""
    logger.info("Creating achievements")
    
    achievements_data = [
        {"name": "Taco Newbie", "description": "Write your first taco review"},
        {"name": "Taco Aficionado", "description": "Review 10 different tacos"},
        {"name": "Taco Connoisseur", "description": "Review 25 different tacos"},
        {"name": "Explorer", "description": "Visit 5 different taco locations"},
        {"name": "Adventurer", "description": "Visit 10 different taco locations"},
        {"name": "Social Butterfly", "description": "Follow 10 other taco lovers"},
        {"name": "Taco Celebrity", "description": "Get 10 followers"},
        {"name": "Taco Influencer", "description": "Get 25 followers"},
        {"name": "Critic", "description": "Write a detailed review (50+ words)"},
        {"name": "Taco Enthusiast", "description": "Log in 10 days in a row"},
    ]
    
    achievements = []
    
    for achievement_data in achievements_data:
        achievement = Achievement(**achievement_data)
        achievement = achievement_crud.create(session, achievement)
        achievements.append(achievement)
    
    logger.info(f"Created {len(achievements)} achievements")
    return achievements

def assign_achievements(
    session: Session, 
    users: List[User], 
    achievements: List[Achievement],
    reviews: List[Review],
    follows: List[Follow]
) -> List[UserAchievement]:
    """Assign achievements to users based on their activity"""
    logger.info("Assigning achievements to users")
    
    user_achievements = []
    
    # Dict to count reviews per user
    user_review_counts = {}
    for review in reviews:
        user_review_counts[review.user_id] = user_review_counts.get(review.user_id, 0) + 1
    
    # Dict to count followers per user
    user_follower_counts = {}
    for follow in follows:
        user_follower_counts[follow.following_id] = user_follower_counts.get(follow.following_id, 0) + 1
    
    # Dict to count how many users each user follows
    user_following_counts = {}
    for follow in follows:
        user_following_counts[follow.follower_id] = user_following_counts.get(follow.follower_id, 0) + 1
    
    # Achievement mapping
    achievement_map = {a.name: a for a in achievements}
    
    for user in users:
        # Number of reviews
        review_count = user_review_counts.get(user.id, 0)
        
        # Taco Newbie achievement
        if review_count >= 1:
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement_map["Taco Newbie"].id,
                earned_at=datetime.utcnow() - timedelta(days=random.randint(0, 90))
            )
            user_achievement = user_achievement_crud.create(session, user_achievement)
            user_achievements.append(user_achievement)
        
        # Taco Aficionado achievement
        if review_count >= 10:
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement_map["Taco Aficionado"].id,
                earned_at=datetime.utcnow() - timedelta(days=random.randint(0, 60))
            )
            user_achievement = user_achievement_crud.create(session, user_achievement)
            user_achievements.append(user_achievement)
        
        # Social Butterfly achievement
        if user_following_counts.get(user.id, 0) >= 10:
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement_map["Social Butterfly"].id,
                earned_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            user_achievement = user_achievement_crud.create(session, user_achievement)
            user_achievements.append(user_achievement)
        
        # Taco Celebrity achievement
        if user_follower_counts.get(user.id, 0) >= 10:
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement_map["Taco Celebrity"].id,
                earned_at=datetime.utcnow() - timedelta(days=random.randint(0, 45))
            )
            user_achievement = user_achievement_crud.create(session, user_achievement)
            user_achievements.append(user_achievement)
    
    logger.info(f"Assigned {len(user_achievements)} achievements to users")
    return user_achievements

def seed_all(session: Session, num_users: int = 10) -> Dict[str, List]:
    """Seed all data tables with mock data"""
    logger.info("Starting database seeding process")
    
    # Create users
    users = create_users(session, count=num_users)
    
    # Create locations
    locations = create_locations(session, count=8)
    
    # Create tacos for each location
    tacos = create_tacos(session, locations, count_per_location=3)
    
    # Create reviews
    reviews = create_reviews(session, users, tacos, max_reviews_per_user=5)
    
    # Create follow relationships
    follows = create_follows(session, users, max_follows_per_user=5)
    
    # Create achievements
    achievements = create_achievements(session)
    
    # Assign achievements to users
    user_achievements = assign_achievements(session, users, achievements, reviews, follows)
    
    logger.info("Database seeding complete!")
    
    return {
        "users": users,
        "locations": locations,
        "tacos": tacos,
        "reviews": reviews,
        "follows": follows,
        "achievements": achievements,
        "user_achievements": user_achievements
    }

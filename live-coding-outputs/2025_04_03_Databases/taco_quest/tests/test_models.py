import unittest
import os
import sys
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.models import User, Location, Taco, Review, Follow, Achievement, UserAchievement

# Create an in-memory database for testing
test_engine = create_engine("sqlite:///:memory:", echo=False)

class TestModels(unittest.TestCase):
    """Test cases for database models and relationships"""
    
    def setUp(self):
        """Set up a clean database before each test"""
        SQLModel.metadata.create_all(test_engine)
        self.session = Session(test_engine)
    
    def tearDown(self):
        """Clean up after each test"""
        self.session.close()
        # Drop all tables
        SQLModel.metadata.drop_all(test_engine)
    
    def test_user_creation(self):
        """Test basic user creation"""
        user = User(username="testuser", email="test@example.com")
        self.session.add(user)
        self.session.commit()
        
        # Fetch from DB
        db_user = self.session.query(User).filter(User.username == "testuser").first()
        
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, "testuser")
        self.assertEqual(db_user.email, "test@example.com")
        self.assertIsInstance(db_user.created_at, datetime)
    
    def test_location_creation(self):
        """Test location creation"""
        location = Location(
            name="Test Taco Shop",
            address="123 Test Street, Testville",
            lat=44.9778,
            lon=-93.2650
        )
        self.session.add(location)
        self.session.commit()
        
        db_location = self.session.query(Location).first()
        
        self.assertIsNotNone(db_location)
        self.assertEqual(db_location.name, "Test Taco Shop")
        self.assertEqual(db_location.address, "123 Test Street, Testville")
        self.assertAlmostEqual(db_location.lat, 44.9778)
        self.assertAlmostEqual(db_location.lon, -93.2650)
    
    def test_taco_with_location(self):
        """Test creating a taco with its location relationship"""
        location = Location(
            name="Test Taco Shop",
            address="123 Test Street, Testville",
            lat=44.9778,
            lon=-93.2650
        )
        self.session.add(location)
        self.session.commit()
        
        taco = Taco(
            name="Test Taco",
            description="A tasty test taco",
            location_id=location.id
        )
        self.session.add(taco)
        self.session.commit()
        
        # Test relationship from taco to location
        db_taco = self.session.query(Taco).first()
        self.assertEqual(db_taco.location.name, "Test Taco Shop")
        
        # Test relationship from location to tacos
        db_location = self.session.query(Location).first()
        self.assertEqual(len(db_location.tacos), 1)
        self.assertEqual(db_location.tacos[0].name, "Test Taco")
    
    def test_user_reviews(self):
        """Test user reviewing tacos"""
        # Create user
        user = User(username="reviewer", email="reviewer@example.com")
        self.session.add(user)
        
        # Create location
        location = Location(
            name="Taco Joint",
            address="456 Taco Lane",
            lat=45.0000,
            lon=-93.0000
        )
        self.session.add(location)
        self.session.commit()
        
        # Create taco
        taco = Taco(
            name="Deluxe Taco",
            description="The best taco",
            location_id=location.id
        )
        self.session.add(taco)
        self.session.commit()
        
        # Create review
        review = Review(
            user_id=user.id,
            taco_id=taco.id,
            rating=5,
            comment="Amazingly delicious!"
        )
        self.session.add(review)
        self.session.commit()
        
        # Test relationships
        db_user = self.session.query(User).first()
        self.assertEqual(len(db_user.reviews), 1)
        self.assertEqual(db_user.reviews[0].rating, 5)
        
        db_taco = self.session.query(Taco).first()
        self.assertEqual(len(db_taco.reviews), 1)
        self.assertEqual(db_taco.reviews[0].comment, "Amazingly delicious!")
        
        db_review = self.session.query(Review).first()
        self.assertEqual(db_review.user.username, "reviewer")
        self.assertEqual(db_review.taco.name, "Deluxe Taco")
    
    def test_user_follows(self):
        """Test user follow relationships"""
        # Create users
        user1 = User(username="follower", email="follower@example.com")
        user2 = User(username="followed", email="followed@example.com")
        self.session.add_all([user1, user2])
        self.session.commit()
        
        # Create follow relationship
        follow = Follow(follower_id=user1.id, following_id=user2.id)
        self.session.add(follow)
        self.session.commit()
        
        # Test relationships
        db_user1 = self.session.query(User).filter(User.username == "follower").first()
        db_user2 = self.session.query(User).filter(User.username == "followed").first()
        
        # User1 follows User2
        self.assertEqual(len(db_user1.following), 1)
        self.assertEqual(db_user1.following[0].following_id, user2.id)
        
        # User2 is followed by User1
        self.assertEqual(len(db_user2.followers), 1)
        self.assertEqual(db_user2.followers[0].follower_id, user1.id)
    
    def test_achievements(self):
        """Test achievement and user-achievement relationships"""
        # Create user
        user = User(username="achiever", email="achiever@example.com")
        self.session.add(user)
        
        # Create achievement
        achievement = Achievement(
            name="Test Achievement",
            description="You did something amazing!"
        )
        self.session.add(achievement)
        self.session.commit()
        
        # Award achievement to user
        user_achievement = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id
        )
        self.session.add(user_achievement)
        self.session.commit()
        
        # Test relationships
        db_user = self.session.query(User).first()
        self.assertEqual(len(db_user.achievements), 1)
        self.assertEqual(db_user.achievements[0].achievement.name, "Test Achievement")
        
        db_achievement = self.session.query(Achievement).first()
        self.assertEqual(len(db_achievement.users), 1)
        self.assertEqual(db_achievement.users[0].user.username, "achiever")

if __name__ == "__main__":
    unittest.main()

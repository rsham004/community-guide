from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    reviews: List["Review"] = Relationship(back_populates="user")
    achievements: List["UserAchievement"] = Relationship(back_populates="user")
    following: List["Follow"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    followers: List["Follow"] = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "[Follow.following_id]"}
    )

class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    lat: float
    lon: float

    # Relationships
    tacos: List["Taco"] = Relationship(back_populates="location")

class Taco(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    location_id: int = Field(foreign_key="location.id")

    # Relationships
    location: Location = Relationship(back_populates="tacos")
    reviews: List["Review"] = Relationship(back_populates="taco")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    taco_id: int = Field(foreign_key="taco.id")
    rating: int
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="reviews")
    taco: Taco = Relationship(back_populates="reviews")

class Follow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    follower_id: int = Field(foreign_key="user.id")
    following_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    follower: User = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    following: User = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "[Follow.following_id]"}
    )

class Achievement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

    # Relationships
    users: List["UserAchievement"] = Relationship(back_populates="achievement")

class UserAchievement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    achievement_id: int = Field(foreign_key="achievement.id")
    earned_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="achievements")
    achievement: Achievement = Relationship(back_populates="users")

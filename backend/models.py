from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    password_hash: str
    profile_pic_url: Optional[str] = None

    videos: List["Video"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    videos: List["Video"] = Relationship(back_populates="category")

class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    video_url: str
    thumbnail_url: str
    views: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="videos")

    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="videos")
    comments: List["Comment"] = Relationship(back_populates="video", cascade_delete=True)

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    video_id: int = Field(foreign_key="video.id")
    video: Video = Relationship(back_populates="comments")

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="comments")
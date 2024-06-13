from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.models.base import Base


user_follow = Table(
        'user_follow',
        Base.metadata,
        Column('follower_id', Integer, ForeignKey('user.id'),primary_key=True),
        Column('followed_id', Integer, ForeignKey('user.id'),primary_key=True)
    )

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    discussions = relationship("Discussion", back_populates="owner")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")


    following = relationship(
        "User",
        secondary="user_follow",
        primaryjoin=(user_follow.c.follower_id == id),
        secondaryjoin=(user_follow.c.followed_id == id),
        backref="followers"
    )

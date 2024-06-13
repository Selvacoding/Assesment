from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    discussion_id = Column(Integer, ForeignKey("discussion.id"))
    user = relationship("User", back_populates="comments")
    discussion = relationship("Discussion", back_populates="comments")

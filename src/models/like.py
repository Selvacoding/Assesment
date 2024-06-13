from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.models.base import Base


class Like(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    discussion_id = Column(Integer, ForeignKey("discussion.id"))
    user = relationship("User", back_populates="likes")
    discussion = relationship("Discussion", back_populates="likes")

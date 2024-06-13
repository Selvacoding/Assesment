from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from src.models.base import Base


class Discussion(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String, index=True)
    tags = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="discussions")
    comments = relationship("Comment", back_populates="discussion")
    likes = relationship("Like", back_populates="discussion")

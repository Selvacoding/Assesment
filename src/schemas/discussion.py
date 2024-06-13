from pydantic import BaseModel
from typing import Optional

class DiscussionBase(BaseModel):
    title: str
    text: str
    tags: str

class DiscussionCreate(DiscussionBase):
    user_id: int

class DiscussionResponse(DiscussionBase):
    id: int
    user_id: int

class DiscussionUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    tags: Optional[str] = None
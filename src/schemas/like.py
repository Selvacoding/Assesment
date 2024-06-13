from pydantic import BaseModel

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    user_id: int
    discussion_id: int

class LikeResponse(LikeBase):
    id: int
    user_id: int
    discussion_id: int

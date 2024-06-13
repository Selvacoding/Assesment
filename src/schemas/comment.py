from pydantic import BaseModel

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    user_id: int
    discussion_id: int

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    user_id: int
    discussion_id: int

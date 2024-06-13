from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from utils import get_db
from src.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from src.service import comment as crud_comment
from src.service.user import get_current_user
from src.models.user import User

comment_router = APIRouter()

@comment_router.post("/", response_model=CommentResponse)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_comment.create_comment(db=db, comment=comment, user_id=current_user.id)

@comment_router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = crud_comment.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud_comment.update_comment(db=db, comment=db_comment, comment_update=comment_update)

@comment_router.delete("/{comment_id}", response_model=CommentResponse)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = crud_comment.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    crud_comment.delete_comment(db=db, comment_id=comment_id)
    return db_comment

@comment_router.get("/discussion/{discussion_id}", response_model=List[CommentResponse])
def get_comments_for_discussion(discussion_id: int, db: Session = Depends(get_db)):
    return crud_comment.get_comments_for_discussion(db=db, discussion_id=discussion_id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.models import User, Like
from src.service.like import like_discussion, unlike_discussion
from src.service.user import get_current_user
from src.schemas.like import LikeCreate
from utils import get_db

like_router = APIRouter()


@like_router.post("/like")
def like_post(
    like_data: LikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return like_discussion(db=db, like_data=like_data, user_id=current_user.id)

@like_router.delete("/like/{like_id}")
def unlike_post(
    like_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    like = db.query(Like).filter(Like.id == like_id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    if like.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    unlike_discussion(db=db, like_id=like_id)
    return {"message": "Like deleted successfully"}

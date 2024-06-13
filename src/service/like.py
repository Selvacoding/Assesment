from sqlalchemy.orm import Session
from src.models.like import Like
from src.schemas.like import LikeCreate

def like_discussion(db: Session, like: LikeCreate, user_id: int):
    db_like = db.query(Like).filter(
        Like.discussion_id == like.discussion_id, Like.user_id == user_id
    ).first()
    if db_like:
        return None
    new_like = Like(discussion_id=like.discussion_id, user_id=user_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like

def unlike_discussion(db: Session, discussion_id: int, user_id: int):
    db_like = db.query(Like).filter(
        Like.discussion_id == discussion_id, Like.user_id == user_id
    ).first()
    if db_like:
        db.delete(db_like)
        db.commit()
        return db_like
    return None

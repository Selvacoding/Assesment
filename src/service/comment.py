from sqlalchemy.orm import Session
from src.models.comment import Comment
from src.schemas.comment import CommentCreate, CommentUpdate

def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = Comment(**comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def update_comment(db: Session, comment: Comment, comment_update: CommentUpdate):
    for key, value in comment_update.dict().items():
        setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    db.delete(db_comment)
    db.commit()
    return db_comment

def get_comments_for_discussion(db: Session, discussion_id: int):
    return db.query(Comment).filter(Comment.discussion_id == discussion_id).all()

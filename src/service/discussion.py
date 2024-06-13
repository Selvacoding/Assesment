from sqlalchemy.orm import Session
from src.models.discussion import Discussion
from src.schemas.discussion import DiscussionCreate, DiscussionUpdate

def create_discussion(db: Session, discussion: DiscussionCreate, user_id: int):
    db_discussion = Discussion(**discussion.dict(), user_id=user_id)
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def get_discussion(db: Session, discussion_id: int):
    return db.query(Discussion).filter(Discussion.id == discussion_id).first()

def update_discussion(db: Session, discussion: Discussion, discussion_update: DiscussionUpdate):
    for key, value in discussion_update.dict().items():
        setattr(discussion, key, value)
    db.commit()
    db.refresh(discussion)
    return discussion

def delete_discussion(db: Session, discussion_id: int):
    db_discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    db.delete(db_discussion)
    db.commit()
    return db_discussion

def get_discussions_by_tag(db: Session, tag: str):
    return db.query(Discussion).filter(Discussion.tags.contains(tag)).all()

def get_discussions_by_text(db: Session, query: str):
    return db.query(Discussion).filter(Discussion.text.contains(query)).all()

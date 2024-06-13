from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from utils import get_db
from src.schemas.discussion import DiscussionCreate, DiscussionUpdate, DiscussionResponse
from src.service import discussion as crud_discussion
from src.service.user import get_current_user
from src.models.user import User

discussion_router = APIRouter()

@discussion_router.post("/", response_model=DiscussionResponse)
def create_discussion(
    discussion: DiscussionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_discussion.create_discussion(db=db, discussion=discussion, user_id=current_user.id)

@discussion_router.put("/{discussion_id}", response_model=DiscussionResponse)
def update_discussion(
    discussion_id: int,
    discussion_update: DiscussionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_discussion = crud_discussion.get_discussion(db, discussion_id=discussion_id)
    if not db_discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    if db_discussion.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud_discussion.update_discussion(db=db, discussion=db_discussion, discussion_update=discussion_update)

@discussion_router.delete("/{discussion_id}", response_model=DiscussionResponse)
def delete_discussion(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_discussion = crud_discussion.get_discussion(db, discussion_id=discussion_id)
    if not db_discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    if db_discussion.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    crud_discussion.delete_discussion(db=db, discussion_id=discussion_id)
    return db_discussion

@discussion_router.get("/tag/{tag}", response_model=List[DiscussionResponse])
def get_discussions_by_tag(tag: str, db: Session = Depends(get_db)):
    return crud_discussion.get_discussions_by_tag(db=db, tag=tag)

@discussion_router.get("/search", response_model=List[DiscussionResponse])
def get_discussions_by_text(query: str, db: Session = Depends(get_db)):
    return crud_discussion.get_discussions_by_text(db=db, query=query)

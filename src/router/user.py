from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from src.db.session import SessionLocal
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.service import user as crud_user
from src.core.security import authenticate_user, create_access_token
from src.schemas.token import Token
from src.models import User
from src.service.user import get_current_user
from utils import get_db

user_router = APIRouter()

@user_router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user_by_mobile = db.query(User).filter(User.mobile == user.mobile_no).first()
    if db_user_by_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    return crud_user.create_user(db=db, user=user)

@user_router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.put("/update/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return crud_user.update_user(db=db, user=db_user, user_update=user_update)

@user_router.delete("/delete/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    crud_user.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}

@user_router.get("/list", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@user_router.get("/search", response_model=List[UserResponse])
def search_users(query: str, db: Session = Depends(get_db)):
    return crud_user.search_users(db, query=query)

@user_router.post("/follow/{user_id}", response_model=UserResponse)
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
    return crud_user.follow_user(db=db, user_id=user_id, current_user=current_user)

@user_router.post("/unfollow/{user_id}", response_model=UserResponse)
def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.unfollow_user(db=db, user_id=user_id, current_user=current_user)

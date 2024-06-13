from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.core.security import get_password_hash,verify_token
from src.core.config import settings
from utils import get_db



def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.full_name,
        email=user.email,
        mobile=user.mobile_no,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        mobile=db_user.mobile
    )

def update_user(db: Session, user: User, user_update: UserUpdate):
    for key, value in user_update.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def search_users(db: Session, query: str):
    return db.query(User).filter(User.name.contains(query) | User.email.contains(query)).all()

def follow_user(db: Session, user_id: int, current_user: User):
    user_to_follow = get_user(db, user_id=user_id)
    current_user.following.append(user_to_follow)
    db.commit()
    return user_to_follow

def unfollow_user(db: Session, user_id: int, current_user: User):
    user_to_unfollow = get_user(db, user_id=user_id)
    current_user.following.remove(user_to_unfollow)
    db.commit()
    return user_to_unfollow

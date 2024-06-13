from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    mobile_no: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: str

class UserResponse(BaseModel):
    email: EmailStr
    full_name: str


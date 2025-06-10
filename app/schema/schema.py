from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str


class LoginRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    photo_url: Optional[str] = None

class LoginResponse(BaseModel):
    message: str
    token: str
    user: UserInfo

class UserUpdate(BaseModel):
    username: str
    email:str
    full_name: str
    password: str | None = None
    photo_url: str | None = None
    


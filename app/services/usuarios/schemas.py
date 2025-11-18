# app/services/usuarios/schemas.py
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRegisterIn(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserLoginIn(BaseModel):
    username_or_email: str
    password: str


class UserUpdateIn(BaseModel):
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class ErrorOut(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

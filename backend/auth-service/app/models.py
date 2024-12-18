from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)

    @validator("username")
    def username_alphanumeric(cls, v):
        if not re.match("^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username must be alphanumeric with underscores only")
        return v

    @validator("password")
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v


class User(BaseModel):
    username: str

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    
class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    
from typing import Literal
from pydantic import BaseModel, Field


class MoodCreate(BaseModel):
    user_id: int = Field(gt=0)
    mood: Literal[
        "happy", "sad", "angry", "calm",
        "anxious", "excited", "tired", "neutral"
    ]
    note: str = Field(default="", max_length=1000)


class MoodUpdate(BaseModel):
    mood: Literal[
        "happy", "sad", "angry", "calm",
        "anxious", "excited", "tired", "neutral"
    ] | None = None
    note: str | None = Field(default=None, max_length=1000)
    
class JournalCreate(BaseModel):
    user_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class JournalUpdate(BaseModel):
    title: str | None = Field(
        default=None, min_length=1, max_length=200
    )
    content: str | None = Field(
        default=None, min_length=1
    )
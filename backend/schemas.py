from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    xp: int
    created_at: datetime
    last_login: Optional[datetime] = None
    completed_challenges: Optional[List[int]] = []

    class Config:
        orm_mode = True

# Challenge schemas
class ChallengeBase(BaseModel):
    name: str
    description: str
    content: Optional[str] = None  # Add content here
    image_url: Optional[str] = None  # Add image_url here
    difficulty: str
    category: str
    xp_reward: int

class ChallengeCreate(ChallengeBase):
    flag: str
    level_id: int

class ChallengeOut(ChallengeBase):
    id: int
    created_at: datetime
    level_id: int

    class Config:
        orm_mode = True

# UserChallenge schema
class UserChallengeOut(BaseModel):
    user_id: int
    challenge_id: int
    completed_at: datetime
    success: bool

    class Config:
        orm_mode = True

# FlagSubmission schemas
class FlagSubmissionCreate(BaseModel):
    flag: str  # Only expect the flag in the request body

class FlagSubmissionOut(BaseModel):
    user_id: int
    challenge_id: int
    flag: str
    correct: bool
    submitted_at: datetime

    class Config:
        orm_mode = True

# Optionally, a combined User output including submissions
class UserWithChallengesOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    xp: int
    completed_challenges: Optional[List[int]] = []
    flag_submissions: Optional[List[FlagSubmissionOut]] = []

    class Config:
        orm_mode = True

# Level and Hint schemas
class LevelOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    order: int

    class Config:
        orm_mode = True

class HintOut(BaseModel):
    hint: str
    remaining_xp: int

    class Config:
        orm_mode = True
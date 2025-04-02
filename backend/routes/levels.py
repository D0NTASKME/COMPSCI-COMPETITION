# backend/routes/levels.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import LevelOut, ChallengeOut  # Make sure you create LevelOut in schemas.py
from backend.crud import get_all_levels, get_challenges_by_level, get_level_by_id  # You need to import this!

router = APIRouter()

@router.get("/levels", response_model=List[LevelOut])
def get_levels(db: Session = Depends(get_db)):
    levels = get_all_levels(db)
    return levels

# This is the new route you need!
@router.get("/levels/{level_id}", response_model=LevelOut)
def get_level(level_id: int, db: Session = Depends(get_db)):
    level = get_level_by_id(db, level_id)
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    return level

@router.get("/levels/{level_id}/challenges", response_model=List[ChallengeOut])
def get_level_challenges(level_id: int, db: Session = Depends(get_db)):
    challenges = get_challenges_by_level(db, level_id)
    if not challenges:
        raise HTTPException(status_code=404, detail="No challenges found for this level")
    return challenges
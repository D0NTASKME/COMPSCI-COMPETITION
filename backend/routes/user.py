from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from backend.database import get_db
from backend.schemas import UserOut, FlagSubmissionCreate
from backend.crud import get_user_by_email, update_xp, get_top_users, get_user_challenges, submit_flag
from jose import JWTError, jwt
from backend.config import SECRET_KEY, ALGORITHM

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@router.get("/profile", response_model=UserOut)
def get_profile(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    challenges = get_user_challenges(db, current_user.id)
    challenge_ids = [uc.challenge_id for uc in challenges] if challenges else []
    current_user.completed_challenges = challenge_ids
    return current_user

@router.post("/update_xp")
def add_xp(amount: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_email(db, current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_xp(db, user, amount)
    return {"message": "XP updated", "new_xp": updated_user.xp}

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    top_users = get_top_users(db)
    leaderboard = []
    for user in top_users:
        challenges = get_user_challenges(db, user.id)
        challenge_ids = [uc.challenge_id for uc in challenges] if challenges else []
        leaderboard.append({
            "username": user.username,
            "xp": user.xp,
            "challenges_completed": len(challenge_ids)
        })
    return leaderboard

@router.post("/challenges/{challenge_id}/submit_flag")
async def submit_flag_endpoint(challenge_id: int, flag_submission: FlagSubmissionCreate, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    result = submit_flag(db, current_user.id, challenge_id, flag_submission.flag)
    if result is None:
        raise HTTPException(status_code=404, detail="Challenge or user not found")
    return result

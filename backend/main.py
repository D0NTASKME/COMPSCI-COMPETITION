from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session
from backend.database import get_db
from typing import List

from backend.crud import (
    create_user, get_user_by_email, update_xp, get_top_users,
    get_challenge_by_id, create_challenge, submit_flag, get_all_challenges,
    get_all_levels, get_challenges_by_level, request_hint,
    get_completed_challenge_ids_for_level,  # Import the new function
    has_user_completed_challenge_by_id  # Import the function to check completion
)
from backend.models import Challenge, Level
from backend.schemas import (
    UserOut, UserCreate, ChallengeOut, ChallengeCreate, FlagSubmissionCreate,
    LevelOut, HintOut
)
from backend.config import SECRET_KEY, ALGORITHM
from backend.routes.auth import verify_password  # Ensure verify_password is available
# Import your levels router
from backend.routes import levels

app = FastAPI()

# CORS Middleware to allow frontend access
origins = [
    "http://localhost:3000",  # Adjust if your frontend is hosted elsewhere
    "https://compsci-competition-frontend.vercel.app",  # Replace with your actual Vercel frontend URL!
    # Add any other origins you need to allow, like your Render frontend URL if you have one
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Helper: Create Access Token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Helper: Get Current User from Token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# ----------------- Authentication Routes -----------------
@app.post("/auth/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = create_user(db, user)
    access_token = create_access_token(data={"sub": created_user.email})
    return {"msg": "User created successfully", "access_token": access_token}

@app.post("/auth/login", response_model=UserOut)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

# ----------------- User Routes -----------------
@app.get("/users/profile", response_model=UserOut)
async def get_user_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user

@app.post("/users/update_xp")
async def add_xp(amount: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_email(db, current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_xp(db, user, amount)
    return {"msg": "XP updated successfully", "new_xp": updated_user.xp}

@app.get("/users/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    top_users = get_top_users(db)
    return [{"username": user.username, "xp": user.xp} for user in top_users]

# ----------------- User Completed Challenges Route -----------------
user_completed_router = APIRouter()

@user_completed_router.get("/users/completed_challenges")
async def get_user_completed_challenges_for_level(
    level_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the IDs of challenges completed by the current user in a specific level.
    """
    completed_ids = get_completed_challenge_ids_for_level(db, current_user.id, level_id)
    return {"completed_challenge_ids": completed_ids}

app.include_router(user_completed_router)

# ----------------- Challenge Completion Status Route -----------------
challenge_status_router = APIRouter()

@challenge_status_router.get("/challenges/{challenge_id}/status")
async def get_challenge_completion_status(
    challenge_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if the current user has completed a specific challenge."""
    completed = has_user_completed_challenge_by_id(db, current_user.id, challenge_id)
    return {"completed": completed}

app.include_router(challenge_status_router)

# ----------------- Level & Challenge Routes -----------------
# Include the levels router here
app.include_router(levels.router)

# These routes are now defined in backend/routes/levels.py, so you can remove them from here if you want
# @app.get("/levels", response_model=List[LevelOut])
# async def get_levels(db: Session = Depends(get_db)):
#     levels = get_all_levels(db)
#     return levels

# @app.get("/levels/{level_id}/challenges", response_model=List[ChallengeOut])
# async def get_challenges_for_level(level_id: int, db: Session = Depends(get_db)):
#     challenges = get_challenges_by_level(db, level_id)
#     return challenges

# Create a New Challenge (Admin endpoint)
@app.post("/challenges/create", response_model=ChallengeOut)
async def create_new_challenge(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    # Here, the flag is provided in the payload. In production, consider generating it securely server-side.
    db_challenge = create_challenge(db, challenge, challenge.flag)
    return db_challenge

# Get all Challenges (across all levels)
@app.get("/challenges", response_model=List[ChallengeOut])
async def get_challenges(db: Session = Depends(get_db)):
    challenges = get_all_challenges(db)
    return challenges

# Get a Specific Challenge
@app.get("/challenges/{challenge_id}", response_model=ChallengeOut)
async def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = get_challenge_by_id(db, challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge

# Flag Submission Route
@app.post("/challenges/{challenge_id}/submit_flag")
async def submit_flag_endpoint(challenge_id: int, flag_submission: FlagSubmissionCreate, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    result = submit_flag(db, current_user.id, challenge_id, flag_submission.flag)
    if result is None:
        raise HTTPException(status_code=404, detail="Challenge or user not found")
    return result

# Hint Request Route
@app.post("/challenges/{challenge_id}/hint", response_model=HintOut)
async def request_challenge_hint(challenge_id: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Request a hint for a challenge.
    This endpoint should deduct a small amount of XP (e.g., 5 XP) and return a hint.
    """
    hint = request_hint(db, current_user.id, challenge_id)
    if hint is None:
        raise HTTPException(status_code=404, detail="Hint not available or challenge not found")
    return hint
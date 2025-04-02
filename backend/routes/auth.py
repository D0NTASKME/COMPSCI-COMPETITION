from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.crud import create_user, get_user_by_email, get_user_challenges
from backend.schemas import UserCreate, UserOut, ChallengeOut
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    challenges = get_user_challenges(db, user.id)
    challenge_ids = [uc.challenge_id for uc in challenges] if challenges else []
    access_token = create_access_token(data={"sub": user.email, "challenges": challenge_ids})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_password(user.password)
    created_user = create_user(db, user)
    access_token = create_access_token(data={"sub": created_user.email})
    return {"msg": "User created successfully", "access_token": access_token}

@router.get("/challenges", response_model=list[ChallengeOut])
def get_challenges(db: Session = Depends(get_db)):
    challenges = get_user_challenges(db)  # Adjust if you want to list all challenges instead
    return challenges

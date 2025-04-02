from sqlalchemy.orm import Session
from backend.models import User, Challenge, UserChallenge, FlagSubmission, Level
from backend.schemas import UserCreate, ChallengeCreate, FlagSubmissionCreate
from passlib.context import CryptContext
from fastapi import HTTPException
import random
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

# User-related CRUD operations
def get_user_by_email(db: Session, email: str):
    """Retrieve a user by their email address."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """Create a new user with a hashed password."""
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        xp=0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_xp(db: Session, user: User, xp_amount: int):
    """Increase the XP of a user by the given amount."""
    user.xp += xp_amount
    db.commit()
    db.refresh(user)
    return user

def get_top_users(db: Session, limit: int = 10):
    """Retrieve the top users by XP."""
    return db.query(User).order_by(User.xp.desc()).limit(limit).all()

# Challenge-related CRUD operations
def generate_flag(length: int = 16):
    """Generate a random flag in the format FLAG{...}."""
    return "FLAG{" + "".join(random.choices(string.ascii_uppercase + string.digits, k=length)) + "}"

def create_challenge(db: Session, challenge: ChallengeCreate, flag: str):
    """Create a new challenge with a flag."""
    print("Creating challenge with data:")
    print(f"  Name: {challenge.name}")
    print(f"  Description: {challenge.description}")
    print(f"  Content: {challenge.content}")  # Print the new content
    print(f"  Image URL: {challenge.image_url}")  # Print the new image URL
    print(f"  Difficulty: {challenge.difficulty}")
    print(f"  Category: {challenge.category}")
    print(f"  XP Reward: {challenge.xp_reward}")
    print(f"  Flag: {flag}")
    print(f"  Level ID: {challenge.level_id}")

    db_challenge = Challenge(
        name=challenge.name,
        description=challenge.description,
        content=challenge.content,  # Save the content
        image_url=challenge.image_url,  # Save the image URL
        difficulty=challenge.difficulty,
        category=challenge.category,
        xp_reward=challenge.xp_reward,
        flag=flag,
        level_id=challenge.level_id
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def get_challenge_by_id(db: Session, challenge_id: int):
    """Retrieve a challenge by its ID."""
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()

def get_all_challenges(db: Session):
    """Retrieve all challenges."""
    return db.query(Challenge).all()

def has_user_completed_challenge(db: Session, user_id: int, challenge_id: int):
    """Check if a user has already completed a challenge."""
    return db.query(UserChallenge).filter_by(user_id=user_id, challenge_id=challenge_id, success=True).first() is not None

def has_user_completed_challenge_by_id(db: Session, user_id: int, challenge_id: int):
    """Check if a user has successfully completed a specific challenge by its ID."""
    return db.query(UserChallenge).filter_by(user_id=user_id, challenge_id=challenge_id, success=True).first() is not None

def submit_flag(db: Session, user_id: int, challenge_id: int, submitted_flag: str):
    """Check if the submitted flag is correct and update XP if so."""
    challenge = get_challenge_by_id(db, challenge_id)
    user = db.query(User).filter(User.id == user_id).first()

    if not challenge or not user:
        raise HTTPException(status_code=404, detail="Challenge or user not found")

    if has_user_completed_challenge(db, user_id, challenge_id):
        raise HTTPException(status_code=400, detail="Challenge already completed")

    if submitted_flag.strip() != challenge.flag.strip():
        # Record incorrect submission
        fs = FlagSubmission(user_id=user_id, challenge_id=challenge_id, flag=submitted_flag, correct=False)
        db.add(fs)
        db.commit()
        db.refresh(fs)
        raise HTTPException(status_code=400, detail="Incorrect flag")

    # Correct submission: update XP and mark challenge as completed
    update_xp(db, user, challenge.xp_reward)
    user_challenge = UserChallenge(user_id=user_id, challenge_id=challenge_id, success=True)
    db.add(user_challenge)
    # Record correct flag submission
    fs = FlagSubmission(user_id=user_id, challenge_id=challenge_id, flag=submitted_flag, correct=True)
    db.add(fs)
    db.commit()
    db.refresh(user)
    return {"msg": "Challenge completed!", "xp_earned": challenge.xp_reward}

def get_user_challenges(db: Session, user_id: int):
    """Retrieve all challenges attempted by a user."""
    return db.query(UserChallenge).filter(UserChallenge.user_id == user_id).all()

def get_all_levels(db: Session):
    try:
        return db.query(Level).order_by(Level.order).all()
    except Exception as e:
        print(f"Error fetching levels: {e}")
        raise

def get_level_by_id(db: Session, level_id: int):
    """Retrieve a level by its ID."""
    return db.query(Level).filter(Level.id == level_id).first()

def get_challenges_by_level(db: Session, level_id: int):
    return db.query(Challenge).filter(Challenge.level_id == level_id).all()

def request_hint(db: Session, user_id: int, challenge_id: int):
    """
    Deduct a fixed amount of XP (e.g., 5 XP) and return a hint for the challenge.
    For simplicity, assume each challenge has a static hint stored in a new column, 'hint', in the Challenge model.
    """
    challenge = get_challenge_by_id(db, challenge_id)
    if not challenge or not hasattr(challenge, 'hint') or not challenge.hint:
        return None
    # Deduct XP (e.g., 5 XP) from user
    user = db.query(User).filter(User.id == user_id).first()
    if user.xp < 5:
        raise HTTPException(status_code=400, detail="Not enough XP for a hint")
    user.xp -= 5
    db.commit()
    # Return the hint in a schema format (create a HintOut schema accordingly)
    return {"hint": challenge.hint, "remaining_xp": user.xp}

def get_completed_challenge_ids_for_level(db: Session, user_id: int, level_id: int):
    """
    Retrieve the IDs of challenges completed by a user in a specific level.
    """
    completed_challenges = (
        db.query(UserChallenge.challenge_id)
        .join(Challenge)
        .filter(UserChallenge.user_id == user_id,
                Challenge.level_id == level_id,
                UserChallenge.success == True)
        .all()
    )
    return [challenge.challenge_id for challenge in completed_challenges]
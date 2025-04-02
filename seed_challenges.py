from backend.database import SessionLocal
from backend.crud import create_challenge, generate_flag
from backend.schemas import ChallengeCreate
from backend.models import Level  # Make sure this import is present

def seed_challenges():
    db = SessionLocal()

    # Get the first level
    level1 = db.query(Level).first()
    print(f"The value of level1 is: {level1}")  # Keep this print statement for now
    if not level1:
        print("Error: No levels found in the database. Please run seed_levels.py first.")
        return

    # Sample Challenge 1: SQL Injection Challenge
    sample_challenge1 = ChallengeCreate(
        name="SQL Injection Challenge",
        description="Bypass the login using a SQL injection attack. Hint: Try entering ' OR '1'='1 in the username field.",
        difficulty="Easy",
        category="SQL Injection",
        xp_reward=20,
        flag="FLAG{SQL_INJECTION_SUCCESS}",
        level_id=level1.id  # Make sure this is still here
    )
    created_challenge1 = create_challenge(db, sample_challenge1, sample_challenge1.flag)
    print("Created Challenge:", created_challenge1)

    # Sample Challenge 2: Basic Cryptography Challenge
    sample_challenge2 = ChallengeCreate(
        name="Basic Cryptography Challenge",
        description="Decrypt the following cipher to find the flag.",
        difficulty="Medium",
        category="Cryptography",
        xp_reward=30,
        flag="FLAG{CRYPTO_MASTER}",
        level_id=level1.id  # And here as well
    )
    created_challenge2 = create_challenge(db, sample_challenge2, sample_challenge2.flag)
    print("Created Challenge:", created_challenge2)

    db.close()

if __name__ == "__main__":
    seed_challenges()
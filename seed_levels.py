# backend/seed_levels.py
from backend.database import SessionLocal
from backend.models import Level, Challenge

def seed_levels():
    db = SessionLocal()

    level_data = {
        "name": "Digital Detective",
        "description": "Use your OSINT skills to uncover hidden secrets in the digital world. Learn basic investigation techniques and apply them in challenges.",
        "order": 1
    }

    existing_level = db.query(Level).filter(Level.name == level_data["name"]).first()

    if not existing_level:
        level1 = Level(**level_data)
        db.add(level1)
        db.commit()
        db.refresh(level1)
        print(f"Seeded Level: {level1.name}")

        # Create Challenges for Level 1 (only if the level was just created)
        challenges_to_seed = [
            {
                "name": "The Hidden Message",
                "description": "A suspicious image has been found. Use steganography tools to reveal the hidden message within.",
                "difficulty": "Easy",
                "category": "Steganography",
                "xp_reward": 100,
                "flag": "FLAG{hidden_message_found}",
                "level_id": level1.id
            },
            {
                "name": "Who Am I?",
                "description": "Online clues hint at a hacker's identity. Use OSINT techniques to determine who they are.",
                "difficulty": "Medium",
                "category": "OSINT",
                "xp_reward": 150,
                "flag": "FLAG{identity_revealed}",
                "level_id": level1.id
            },
            {
                "name": "Password Puzzle",
                "description": "A file containing hashed passwords has been leaked. Crack the hash to reveal the password.",
                "difficulty": "Medium",
                "category": "Cryptography",
                "xp_reward": 200,
                "flag": "FLAG{password_cracked}",
                "level_id": level1.id
            }
        ]

        for challenge_data in challenges_to_seed:
            existing_challenge = db.query(Challenge).filter(Challenge.name == challenge_data["name"]).first()
            if not existing_challenge:
                challenge = Challenge(**challenge_data)
                db.add(challenge)
                db.commit()
                print(f"  Seeded Challenge: {challenge.name} in Level {level1.name}")
            else:
                print(f"  Challenge '{challenge_data['name']}' already exists.")

    else:
        print(f"Level '{level_data['name']}' already exists.")

    db.close()

if __name__ == "__main__":
    seed_levels()
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.base import Base  # Import Base from your new base.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    xp = Column(Integer, default=0)  # XP tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    completed_challenges = relationship("UserChallenge", back_populates="user")
    flag_submissions = relationship("FlagSubmission", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', xp={self.xp})>"

class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    order = Column(Integer, unique=True, nullable=False)  # Order for progression

    challenges = relationship("Challenge", back_populates="level")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=True)  # New field for main challenge content
    image_url = Column(String, nullable=True)  # New field for image URL
    difficulty = Column(String, nullable=False)  # Easy, Medium, Hard
    category = Column(String, nullable=False)      # E.g., SQL Injection, Cryptography, OSINT
    xp_reward = Column(Integer, nullable=False, default=10)
    flag = Column(String, nullable=False)  # The correct flag for the challenge
    created_at = Column(DateTime, default=datetime.utcnow)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)  # Link challenge to a level

    # Relationships
    level = relationship("Level", back_populates="challenges")
    user_challenges = relationship("UserChallenge", back_populates="challenge")
    flag_submissions = relationship("FlagSubmission", back_populates="challenge")

    def __repr__(self):
        return f"<Challenge(id={self.id}, name='{self.name}', difficulty='{self.difficulty}', xp_reward={self.xp_reward})>"

class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=False)

    user = relationship("User", back_populates="completed_challenges")
    challenge = relationship("Challenge", back_populates="user_challenges")

    def __repr__(self):
        return f"<UserChallenge(user_id={self.user_id}, challenge_id={self.challenge_id}, success={self.success})>"

class FlagSubmission(Base):
    __tablename__ = "flag_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    flag = Column(String, nullable=False)  # The submitted flag
    correct = Column(Boolean, default=False)  # Whether the submission is correct
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="flag_submissions")
    challenge = relationship("Challenge", back_populates="flag_submissions")

    def __repr__(self):
        return f"<FlagSubmission(user_id={self.user_id}, challenge_id={self.challenge_id}, flag='{self.flag}', correct={self.correct})>"
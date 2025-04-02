from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import DATABASE_URL
from backend.base import Base  # Import Base from your new base.py
from alembic import command
from alembic.config import Config

# Create the database engine using SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables (for development; use migrations in production)
Base.metadata.create_all(bind=engine)

# Function to run migrations with Alembic
def run_migrations():
    alembic_cfg = Config("alembic.ini")  # The path to your alembic.ini file
    command.upgrade(alembic_cfg, "head")  # This applies the latest migrations

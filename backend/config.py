import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_user:securepassword@localhost:5432/app_database")

# Secret key for JWT token encoding and decoding
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

# JWT Algorithm
ALGORITHM = "HS256"

# JWT Token expiry time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env from backend directory (one level up from this file)
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # Database configuration - supports both individual fields and full URL
    database_url: str = os.getenv("DATABASE_URL", "")
    db_pass: str = os.getenv("DB_PASS", "")
    supabase_url: str = os.getenv("REACT_APP_SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("REACT_APP_SUPABASE_ANON_KEY", "")
    
    # JWT configuration
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    class Config:
        env_file = str(env_path)
        extra = "ignore"  # Ignore extra fields from environment

settings = Settings() 
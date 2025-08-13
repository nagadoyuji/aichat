import os
from dotenv import load_dotenv
from typing import Any, Dict, Optional

print(f"Loaded .env file: {load_dotenv()}")
print(f"GEMINI_API_KEY exists: {os.getenv('GEMINI_API_KEY') is not None}")

class Settings:
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ai_chat")
    DATABASE_URL: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # Gemini settings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Knowledge base settings
    KB_COLLECTION_NAME: str = "knowledge_base"
    KB_PERSIST_DIRECTORY: str = "./chroma_db"

settings = Settings()
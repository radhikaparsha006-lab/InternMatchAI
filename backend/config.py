from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "InternMatch AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # Database configuration
    # Can use PostgreSQL (including Supabase postgres:// connection) or local SQLite fallback
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite+aiosqlite:///./internmatch.db"
    )
    
    # Optional Supabase direct credentials
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL", None)
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY", None)
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_ROLE_KEY", None)

    # Optional External AI/LLM API credentials
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "grounded_rule_based")  # 'grounded_rule_based', 'openai', 'gemini'

    # Optional External Internship API credentials (e.g. Adzuna, RapidAPI, SerpApi)
    RAPIDAPI_KEY: Optional[str] = os.getenv("RAPIDAPI_KEY", None)
    ADZUNA_APP_ID: Optional[str] = os.getenv("ADZUNA_APP_ID", None)
    ADZUNA_APP_KEY: Optional[str] = os.getenv("ADZUNA_APP_KEY", None)

    # CORS settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()

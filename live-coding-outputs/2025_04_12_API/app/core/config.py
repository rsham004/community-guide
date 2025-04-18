from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    DATABASE_URL: str = "sqlite+aiosqlite:///./promptsculptor_proto.db"
    LLM_API_KEY: str = "YOUR_LLM_API_KEY_HERE" # Default placeholder
    LLM_API_BASE_URL: str | None = None

    # Load settings from a .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    """
    Returns the application settings instance.
    Uses lru_cache to load settings only once.
    """
    return Settings()

settings = get_settings()

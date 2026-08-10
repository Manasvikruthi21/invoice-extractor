import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Document Intelligence Agent"
    API_V1_STR: str = "/api/v1"
    
    # OCR Settings
    DEFAULT_OCR_CONFIDENCE_THRESHOLD: float = 0.60
    
    # Gemini API settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-flash"  # Default model for layout structuring
    
    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Environment mode (development / production)
    ENV: str = "development"
    
    # Allow mock fallback if torch/doctr is missing or slow to load
    ALLOW_MOCK_FALLBACK: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):

    # ----------------------------------
    # Project Information
    # ----------------------------------

    PROJECT_NAME: str = "AI Document Intelligence Agent"
    VERSION: str = "1.0.0"

    # ----------------------------------
    # FastAPI
    # ----------------------------------

    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # ----------------------------------
    # OCR
    # ----------------------------------

    DEFAULT_OCR: str = "rapidocr"

    ENABLE_RAPIDOCR: bool = True
    ENABLE_EASYOCR: bool = True
    ENABLE_PADDLEOCR: bool = False

    # ----------------------------------
    # LLM
    # ----------------------------------

    DEFAULT_LLM: str = "gemini"

    GEMINI_MODEL: str = "gemini-2.5-flash"

    OPENAI_MODEL: str = "gpt-4.1-mini"

    OLLAMA_MODEL: str = "llama3.2"

    # ----------------------------------
    # API Keys
    # ----------------------------------

    GEMINI_API_KEY: str = ""

    OPENAI_API_KEY: str = ""

    # ----------------------------------
    # Directories
    # ----------------------------------

    INPUT_DIR: Path = BASE_DIR / "data" / "input"

    OUTPUT_DIR: Path = BASE_DIR / "data" / "output"

    TEMP_DIR: Path = BASE_DIR / "data" / "temp"

    LOG_DIR: Path = BASE_DIR / "logs"

    # ----------------------------------
    # Confidence
    # ----------------------------------

    OCR_CONFIDENCE_THRESHOLD: float = 0.65

    LLM_TEMPERATURE: float = 0.0

    MAX_IMAGE_SIZE: int = 4096

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
from pydantic_settings import BaseSettings
from typing import Optional
from fastapi import HTTPException

class GeminiConfig(BaseSettings):
    API_KEY: Optional[str] = None
    MODEL_NAME: str = "gemini-1.5-flash"
    RATE_LIMIT_REQUESTS: int = 60  # requests per minute
    
    class Config:
        env_prefix = "GEMINI_"
    
    def validate_config(self) -> None:
        if not self.API_KEY:
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY is not set in environment variables"
            )

class Settings(BaseSettings):
    UPLOAD_FOLDER: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"pdf"}
    gemini_config: GeminiConfig = GeminiConfig()

    def validate(self):
        if not self.gemini_config.API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set. Exiting...")

settings = Settings()
settings.validate()

gemini_config = GeminiConfig()
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # Basic settings
    APP_NAME: str = "Lanceraa API"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS settings
    ALLOWED_ORIGINS_STR: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000,https://abhinavgyawali07.pythonanywhere.com")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lanceraa.db")

    # Email settings
    EMAIL_HOST: str = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "your-email@gmail.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "your-app-password")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "Lanceraa <your-email@gmail.com>")
    SUPPORT_EMAIL: str = os.getenv("SUPPORT_EMAIL", "support@lanceraa.com")

    # For testing: if True, prints emails to console instead of sending
    EMAIL_TEST_MODE: bool = os.getenv("EMAIL_TEST_MODE", "False").lower() == "true"
    
    # New validation using Pydantic v2 syntax
    @field_validator("EMAIL_USERNAME", "EMAIL_PASSWORD")
    @classmethod
    def validate_email_credentials(cls, v, info):
        if not v:
            print(f"Warning: {info.field_name} not set")
        return v

    # Configuration for Pydantic v2
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }
        # Property to get ALLOWED_ORIGINS as a list
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        return self.ALLOWED_ORIGINS_STR.split(",")

# Create settings instance
settings = Settings()

print(f"ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")
print(f"ENVIRONMENT: {settings.ENVIRONMENT}")

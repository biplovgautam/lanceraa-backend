from pydantic import BaseSettings, validator
import os
from dotenv import load_dotenv

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
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
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
    
    # New validation
    @validator("EMAIL_USERNAME", "EMAIL_PASSWORD", pre=True)
    def validate_email_credentials(cls, v, values, **kwargs):
        if not v and kwargs["field"].name == "EMAIL_USERNAME":
            print("Warning: Email username not set")
        if not v and kwargs["field"].name == "EMAIL_PASSWORD":
            print("Warning: Email password not set")
        return v

# Create settings instance
settings = Settings()

print(f"ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")
print(f"ENVIRONMENT: {settings.ENVIRONMENT}")
from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from ..core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

# Database connection check
def check_database_connection():
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as connection:
            connection.execute("SELECT 1")  # Run a simple query to check the connection
        return True
    except OperationalError as e:
        return False, str(e)

# Email server connection check
def check_email_server():
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)  # Attempt login
        return True
    except Exception as e:
        return False, str(e)

@router.get("")
async def health_check():
    """
    Health check endpoint that verifies the API is running, checks database,
    email server, and environment variables.
    """
    health_status = {
        "status": "healthy",
        "version": "1.0.0",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }

    # Check Database connection
    db_status, db_error = check_database_connection()
    health_status["database"] = {"status": "healthy" if db_status else "unhealthy", "error": db_error if not db_status else None}

    # Check Email server
    email_status, email_error = check_email_server()
    health_status["email_server"] = {"status": "healthy" if email_status else "unhealthy", "error": email_error if not email_status else None}

    # Check environment variables (example)
    missing_env_vars = [key for key, value in settings.dict().items() if value is None]
    if missing_env_vars:
        health_status["environment_variables"] = {
            "status": "unhealthy",
            "missing": missing_env_vars,
        }
    else:
        health_status["environment_variables"] = {"status": "healthy"}

    return health_status

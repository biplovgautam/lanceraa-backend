from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
import re

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    country: str
    zip: str

class InitialSignup(BaseModel):
    """Initial signup with minimal fields"""
    email: EmailStr
    password: str = Field(
        default="StrongP@ss123",
        description="Password must be at least 8 characters and contain letters, numbers, and special characters",
        min_length=8
    )
    confirm_password: str = Field(default="StrongP@ss123", min_length=8)
    is_client: bool = Field(..., description="True for client, False for talent/lancer")


    @validator('password')
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v):
            raise ValueError(
                "Password must contain at least:"
                "\n- 8 characters"
                "\n- One letter"
                "\n- One number"
                "\n- One special character (@$!%*#?&)"
            )
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class VerifyEmail(BaseModel):
    """Email verification with OTP"""
    user_id: str
    verification_code: str

class ResendVerification(BaseModel):
    user_id: str

class BasicProfileInfo(BaseModel):
    """Basic profile information after verification"""
    username: str = Field(..., min_length=3, max_length=20, pattern="^[a-zA-Z0-9_-]+$")
    firstName: str = Field(..., min_length=2, max_length=50)
    lastName: str = Field(..., min_length=2, max_length=50)
    role: str = Field(..., pattern="^(freelancer|client)$")

class ContactInfo(BaseModel):
    """Contact information step"""
    phone: str = Field(..., pattern=r"^\+?[1-9][0-9]{7,14}$")
    address: Optional[AddressCreate] = None

class ProfessionalInfo(BaseModel):
    """Professional information step"""
    skills: Optional[List[str]] = Field(default_factory=list)
    bio: Optional[str] = Field(default=None, max_length=500)
    years_experience: Optional[int] = None
    hourly_rate: Optional[float] = None

# Keep the complete model for internal use and API documentation
class UserCreate(BaseModel):
    # Account Details
    email: EmailStr
    password: str = Field(
        ...,
        description="Password must be at least 8 characters and contain letters, numbers, and special characters",
        min_length=8
    )
    username: Optional[str] = Field(None, min_length=3, max_length=20, pattern="^[a-zA-Z0-9_-]+$")
    
    # Personal Information
    firstName: Optional[str] = Field(None, min_length=2, max_length=50)
    lastName: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9][0-9]{7,14}$")
    role: Optional[str] = Field(None, pattern="^(freelancer|client)$")
    
    # Address Information
    address: Optional[AddressCreate] = None
    
    # Professional Details
    skills: Optional[List[str]] = Field(default_factory=list)
    bio: Optional[str] = Field(default=None, max_length=500)

    @validator('password')
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", v):
            raise ValueError(
                "Password must contain at least:"
                "\n- 8 characters"
                "\n- One letter"
                "\n- One number"
                "\n- One special character (@$!%*#?&)"
            )
        return v

class StepCompletionResponse(BaseModel):
    """Response for step completion"""
    message: str
    success: bool
    next_step: Optional[str] = None
    user_id: Optional[str] = None

class UserResponseData(BaseModel):
    id: str
    username: Optional[str] = None
    email: str
    full_name: Optional[str] = None
    is_client: bool
    is_verified: bool
    profile_completed: bool
    completion_step: Optional[str] = None

class UserResponse(BaseModel):
    message: str
    user: Optional[UserResponseData] = None
    error: Optional[str] = None

class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[List[str]] = None
    address: Optional[AddressCreate] = None

class UserInDB(BaseModel):
    id: str
    username: Optional[str] = None
    email: str
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: bool
    is_verified: bool
    profile_completed: bool
    completion_step: Optional[str] = None
    created_at: Any
    
    class Config:
        from_attributes = True  # Updated from orm_mode in Pydantic v2

class EmailCheck(BaseModel):
    """Schema for checking if an email already exists"""
    email: EmailStr
    
class EmailExists(BaseModel):
    """Response schema for email check"""
    exists: bool
    message: str
    is_active: Optional[bool] = None
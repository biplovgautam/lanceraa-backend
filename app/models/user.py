import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Text, JSON, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    """Core user identity and authentication"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    
    
    
    # Status flags
    is_active = Column(Boolean, default=False)  # Becomes true after OTP verification
    is_verified = Column(Boolean, default=False)  # For blue checkmark verification
    profile_completed = Column(Boolean, default=False)  # Track if profile is completed
    is_client = Column(Boolean, nullable=False) # diffrent roles for different users
    
    # For email verification
    verification_code = Column(String(6), nullable=True)
    verification_code_expires = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    last_login = Column(DateTime, nullable=True)  # Add if missing

    
    # Relationship to profile
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class UserProfile(Base):
    """Extended user profile information"""
    __tablename__ = "user_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    
    # Profile image
    profile_image = Column(String(255), nullable=True)
    
    # Professional details
    bio = Column(String(500), nullable=True)
    skills = Column(String(500), nullable=True)  # Store as comma-separated values
    
    # Address
    street = Column(String(100), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    zip = Column(String(20), nullable=True)
    
    # Social links
    website = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    twitter = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationship to user
    user = relationship("User", back_populates="profile")
    
    # Helper method to get full address
    def get_full_address(self):
        if all([self.street, self.city, self.state, self.country, self.zip]):
            return f"{self.street}, {self.city}, {self.state}, {self.country}, {self.zip}"
        return None
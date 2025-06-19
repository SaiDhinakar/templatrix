from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    """User model for database operations and API responses"""
    username: str
    email: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com"
            }
        }


class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str
    email: str


class UserResponse(BaseModel):
    """Model for user API responses"""
    username: str
    email: str
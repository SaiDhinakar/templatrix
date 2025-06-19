from fastapi import APIRouter, Depends, status
from typing import List

from models.user import User, UserCreate, UserResponse
from utils.database import get_database
from utils.responses import create_response, ErrorResponses
from db.database import UserDataBase

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: UserDataBase = Depends(get_database)):
    """Get all users from the database"""
    users = db.get_users()
    return users

@router.get("/{username}", response_model=UserResponse)
def get_user(username: str, db: UserDataBase = Depends(get_database)):
    """Get a specific user by username"""
    user = db.get_user(username)
    if not user:
        raise ErrorResponses.user_not_found(username)
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: UserDataBase = Depends(get_database)):
    """Create a new user"""
    # Check if user already exists
    existing_user = db.get_user(user.username)
    if existing_user:
        raise ErrorResponses.user_already_exists(user.username)
    
    success = db.add_user(user)
    if not success:
        raise ErrorResponses.database_error()
    
    return UserResponse(username=user.username, email=user.email)

@router.put("/{username}", response_model=UserResponse)
def update_user(username: str, user_update: UserCreate, db: UserDataBase = Depends(get_database)):
    """Update an existing user"""
    existing_user = db.get_user(username)
    if not existing_user:
        raise ErrorResponses.user_not_found(username)
    
    # Remove old user and add updated user
    db.remove_user(username)
    success = db.add_user(user_update)
    
    if not success:
        raise ErrorResponses.database_error()
    
    return UserResponse(username=user_update.username, email=user_update.email)

@router.delete("/{username}")
def delete_user(username: str, db: UserDataBase = Depends(get_database)):
    """Delete a user by username"""
    success = db.remove_user(username)
    if not success:
        raise ErrorResponses.user_not_found(username)
    
    return create_response(f"User '{username}' deleted successfully")

@router.get("/{username}/exists")
def check_user_exists(username: str, db: UserDataBase = Depends(get_database)):
    """Check if a user exists"""
    user = db.get_user(username)
    return create_response(
        message=f"User '{username}' {'exists' if user else 'does not exist'}",
        data={"exists": user is not None}
    )
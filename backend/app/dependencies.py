from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import asyncpg
from app.database import get_db
from app.utils.auth import verify_token
from app.models import User, UserRole

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: asyncpg.Connection = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    email = verify_token(token)
    
    if email is None:
        raise credentials_exception
    
    # Get user from database
    query = """
        SELECT id, email, full_name, role, is_active, created_at, hashed_password
        FROM users WHERE email = $1
    """
    user_record = await db.fetchrow(query, email)
    
    if user_record is None:
        raise credentials_exception
    
    user = User(
        id=user_record['id'],
        email=user_record['email'],
        full_name=user_record['full_name'],
        role=user_record['role'],
        is_active=user_record['is_active'],
        created_at=user_record['created_at']
    )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: asyncpg.Connection = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, otherwise None"""
    if not credentials:
        return None
    
    token = credentials.credentials
    email = verify_token(token)
    
    if email is None:
        return None
    
    # Get user from database
    query = """
        SELECT id, email, full_name, role, is_active, created_at
        FROM users WHERE email = $1
    """
    user_record = await db.fetchrow(query, email)
    
    if user_record is None:
        return None
    
    return User(
        id=user_record['id'],
        email=user_record['email'],
        full_name=user_record['full_name'],
        role=user_record['role'],
        is_active=user_record['is_active'],
        created_at=user_record['created_at']
    ) 
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import asyncpg
from datetime import timedelta
from app.database import get_db
from app.models import UserCreate, UserLogin, User, Token, UserRole
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=User)
async def register_user(
    user: UserCreate,
    db: asyncpg.Connection = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = await db.fetchrow(
        "SELECT id FROM users WHERE email = $1",
        user.email
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Insert new user
    query = """
        INSERT INTO users (email, full_name, role, hashed_password, is_active, created_at)
        VALUES ($1, $2, $3, $4, $5, NOW())
        RETURNING id, email, full_name, role, is_active, created_at
    """
    
    user_record = await db.fetchrow(
        query,
        user.email,
        user.full_name,
        user.role.value,
        hashed_password,
        True
    )
    
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    return User(
        id=user_record['id'],
        email=user_record['email'],
        full_name=user_record['full_name'],
        role=user_record['role'],
        is_active=user_record['is_active'],
        created_at=user_record['created_at']
    )

@router.post("/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin,
    db: asyncpg.Connection = Depends(get_db)
):
    """Login user and return JWT token"""
    # Get user from database
    user_record = await db.fetchrow(
        "SELECT id, email, full_name, role, is_active, hashed_password FROM users WHERE email = $1",
        user_credentials.email
    )
    
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user_record['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user_record['is_active']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_record['email']},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: asyncpg.Connection = Depends(get_db)
):
    """OAuth2 compatible token login"""
    # Get user from database
    user_record = await db.fetchrow(
        "SELECT id, email, full_name, role, is_active, hashed_password FROM users WHERE email = $1",
        form_data.username  # OAuth2 uses username field for email
    )
    
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user_record['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user_record['is_active']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_record['email']},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"} 
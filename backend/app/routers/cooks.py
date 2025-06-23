from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import asyncpg
from app.database import get_db
from app.models import CookProfile, CookProfileCreate, CookProfileUpdate, User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/cooks", tags=["cook profiles"])

@router.post("/", response_model=CookProfile)
async def create_cook_profile(
    cook_data: CookProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Create a new cook profile"""
    # Check if user already has a cook profile
    existing_profile = await db.fetchrow(
        "SELECT id FROM cook_profiles WHERE user_id = $1",
        current_user.id
    )
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cook profile already exists for this user"
        )
    
    # Insert new cook profile
    query = """
        INSERT INTO cook_profiles (user_id, name, bio, photo_url, delivery_radius, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
        RETURNING id, user_id, name, bio, photo_url, delivery_radius, created_at, updated_at
    """
    
    profile_record = await db.fetchrow(
        query,
        current_user.id,
        cook_data.name,
        cook_data.bio,
        cook_data.photo_url,
        cook_data.delivery_radius
    )

    if not profile_record:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create cook profile"
        )

    return CookProfile(
        id=profile_record['id'],
        user_id=profile_record['user_id'],
        name=profile_record['name'],
        bio=profile_record['bio'],
        photo_url=profile_record['photo_url'],
        delivery_radius=profile_record['delivery_radius'],
        created_at=profile_record['created_at'],
        updated_at=profile_record['updated_at']
    )

@router.get("/", response_model=List[CookProfile])
async def get_cook_profiles(
    skip: int = 0,
    limit: int = 100,
    db: asyncpg.Connection = Depends(get_db)
):
    """Get all cook profiles"""
    query = """
        SELECT id, user_id, name, bio, photo_url, delivery_radius, created_at, updated_at
        FROM cook_profiles
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
    """
    
    profiles = await db.fetch(query, limit, skip)
    
    return [
        CookProfile(
            id=profile['id'],
            user_id=profile['user_id'],
            name=profile['name'],
            bio=profile['bio'],
            photo_url=profile['photo_url'],
            delivery_radius=profile['delivery_radius'],
            created_at=profile['created_at'],
            updated_at=profile['updated_at']
        )
        for profile in profiles
    ]

@router.get("/{cook_id}", response_model=CookProfile)
async def get_cook_profile(
    cook_id: int,
    db: asyncpg.Connection = Depends(get_db)
):
    """Get a specific cook profile"""
    profile_record = await db.fetchrow(
        "SELECT id, user_id, name, bio, photo_url, delivery_radius, created_at, updated_at FROM cook_profiles WHERE id = $1",
        cook_id
    )
    
    if not profile_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook profile not found"
        )
    
    return CookProfile(
        id=profile_record['id'],
        user_id=profile_record['user_id'],
        name=profile_record['name'],
        bio=profile_record['bio'],
        photo_url=profile_record['photo_url'],
        delivery_radius=profile_record['delivery_radius'],
        created_at=profile_record['created_at'],
        updated_at=profile_record['updated_at']
    )

@router.get("/me/profile", response_model=CookProfile)
async def get_my_cook_profile(
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get current user's cook profile"""
    profile_record = await db.fetchrow(
        "SELECT id, user_id, name, bio, photo_url, delivery_radius, created_at, updated_at FROM cook_profiles WHERE user_id = $1",
        current_user.id
    )
    
    if not profile_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook profile not found"
        )
    
    return CookProfile(
        id=profile_record['id'],
        user_id=profile_record['user_id'],
        name=profile_record['name'],
        bio=profile_record['bio'],
        photo_url=profile_record['photo_url'],
        delivery_radius=profile_record['delivery_radius'],
        created_at=profile_record['created_at'],
        updated_at=profile_record['updated_at']
    )

@router.put("/{cook_id}", response_model=CookProfile)
async def update_cook_profile(
    cook_id: int,
    cook_data: CookProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Update a cook profile"""
    # Check if profile exists and belongs to current user
    existing_profile = await db.fetchrow(
        "SELECT id, user_id FROM cook_profiles WHERE id = $1",
        cook_id
    )
    
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook profile not found"
        )
    
    if existing_profile['user_id'] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this profile"
        )
    
    # Build update query dynamically
    update_fields = []
    values = []
    param_count = 1
    
    if cook_data.name is not None:
        update_fields.append(f"name = ${param_count}")
        values.append(cook_data.name)
        param_count += 1
    
    if cook_data.bio is not None:
        update_fields.append(f"bio = ${param_count}")
        values.append(cook_data.bio)
        param_count += 1
    
    if cook_data.photo_url is not None:
        update_fields.append(f"photo_url = ${param_count}")
        values.append(cook_data.photo_url)
        param_count += 1
    
    if cook_data.delivery_radius is not None:
        update_fields.append(f"delivery_radius = ${param_count}")
        values.append(cook_data.delivery_radius)
        param_count += 1
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_fields.append(f"updated_at = NOW()")
    values.append(cook_id)
    
    query = f"""
        UPDATE cook_profiles 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING id, user_id, name, bio, photo_url, delivery_radius, created_at, updated_at
    """
    
    updated_profile = await db.fetchrow(query, *values)
    
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update cook profile"
        )
    
    return CookProfile(
        id=updated_profile['id'],
        user_id=updated_profile['user_id'],
        name=updated_profile['name'],
        bio=updated_profile['bio'],
        photo_url=updated_profile['photo_url'],
        delivery_radius=updated_profile['delivery_radius'],
        created_at=updated_profile['created_at'],
        updated_at=updated_profile['updated_at']
    )

@router.delete("/{cook_id}")
async def delete_cook_profile(
    cook_id: int,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Delete a cook profile"""
    # Check if profile exists and belongs to current user
    existing_profile = await db.fetchrow(
        "SELECT id, user_id FROM cook_profiles WHERE id = $1",
        cook_id
    )
    
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook profile not found"
        )
    
    if existing_profile['user_id'] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this profile"
        )
    
    # Delete the profile
    await db.execute("DELETE FROM cook_profiles WHERE id = $1", cook_id)
    
    return {"message": "Cook profile deleted successfully"} 
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import asyncpg
from app.database import get_db
from app.models import MenuItem, MenuItemCreate, MenuItemUpdate, User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/menu", tags=["menu items"])

@router.post("/", response_model=MenuItem)
async def create_menu_item(
    menu_item: MenuItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Create a new menu item"""
    # Check if user has a cook profile
    cook_profile = await db.fetchrow(
        "SELECT id FROM cook_profiles WHERE user_id = $1",
        current_user.id
    )
    
    if not cook_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must have a cook profile to create menu items"
        )
    
    # Insert new menu item
    query = """
        INSERT INTO menu_items (cook_id, title, description, price, photo_url, is_available, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
        RETURNING id, cook_id, title, description, price, photo_url, is_available, created_at, updated_at
    """
    
    item_record = await db.fetchrow(
        query,
        cook_profile['id'],
        menu_item.title,
        menu_item.description,
        menu_item.price,
        menu_item.photo_url,
        menu_item.is_available
    )
    
    return MenuItem(
        id=item_record['id'],
        cook_id=item_record['cook_id'],
        title=item_record['title'],
        description=item_record['description'],
        price=item_record['price'],
        photo_url=item_record['photo_url'],
        is_available=item_record['is_available'],
        created_at=item_record['created_at'],
        updated_at=item_record['updated_at']
    )

@router.get("/", response_model=List[MenuItem])
async def get_menu_items(
    skip: int = 0,
    limit: int = 100,
    cook_id: Optional[int] = None,
    available_only: bool = True,
    db: asyncpg.Connection = Depends(get_db)
):
    """Get menu items with optional filtering"""
    base_query = """
        SELECT id, cook_id, title, description, price, photo_url, is_available, created_at, updated_at
        FROM menu_items
    """
    
    conditions = []
    params = []
    param_count = 1
    
    if cook_id is not None:
        conditions.append(f"cook_id = ${param_count}")
        params.append(cook_id)
        param_count += 1
    
    if available_only:
        conditions.append(f"is_available = ${param_count}")
        params.append(True)
        param_count += 1
    
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    base_query += f" ORDER BY created_at DESC LIMIT ${param_count} OFFSET ${param_count + 1}"
    params.extend([limit, skip])
    
    items = await db.fetch(base_query, *params)
    
    return [
        MenuItem(
            id=item['id'],
            cook_id=item['cook_id'],
            title=item['title'],
            description=item['description'],
            price=item['price'],
            photo_url=item['photo_url'],
            is_available=item['is_available'],
            created_at=item['created_at'],
            updated_at=item['updated_at']
        )
        for item in items
    ]

@router.get("/{item_id}", response_model=MenuItem)
async def get_menu_item(
    item_id: int,
    db: asyncpg.Connection = Depends(get_db)
):
    """Get a specific menu item"""
    item_record = await db.fetchrow(
        "SELECT id, cook_id, title, description, price, photo_url, is_available, created_at, updated_at FROM menu_items WHERE id = $1",
        item_id
    )
    
    if not item_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    return MenuItem(
        id=item_record['id'],
        cook_id=item_record['cook_id'],
        title=item_record['title'],
        description=item_record['description'],
        price=item_record['price'],
        photo_url=item_record['photo_url'],
        is_available=item_record['is_available'],
        created_at=item_record['created_at'],
        updated_at=item_record['updated_at']
    )

@router.get("/cook/{cook_id}", response_model=List[MenuItem])
async def get_cook_menu_items(
    cook_id: int,
    skip: int = 0,
    limit: int = 100,
    available_only: bool = True,
    db: asyncpg.Connection = Depends(get_db)
):
    """Get all menu items for a specific cook"""
    # Check if cook exists
    cook_exists = await db.fetchrow(
        "SELECT id FROM cook_profiles WHERE id = $1",
        cook_id
    )
    
    if not cook_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cook not found"
        )
    
    base_query = """
        SELECT id, cook_id, title, description, price, photo_url, is_available, created_at, updated_at
        FROM menu_items
        WHERE cook_id = $1
    """
    params = [cook_id]
    param_count = 2
    
    if available_only:
        base_query += f" AND is_available = ${param_count}"
        params.append(True)
        param_count += 1
    
    base_query += f" ORDER BY created_at DESC LIMIT ${param_count} OFFSET ${param_count + 1}"
    params.extend([limit, skip])
    
    items = await db.fetch(base_query, *params)
    
    return [
        MenuItem(
            id=item['id'],
            cook_id=item['cook_id'],
            title=item['title'],
            description=item['description'],
            price=item['price'],
            photo_url=item['photo_url'],
            is_available=item['is_available'],
            created_at=item['created_at'],
            updated_at=item['updated_at']
        )
        for item in items
    ]

@router.put("/{item_id}", response_model=MenuItem)
async def update_menu_item(
    item_id: int,
    menu_item: MenuItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Update a menu item"""
    # Check if item exists and belongs to current user's cook profile
    item_check = await db.fetchrow(
        """
        SELECT mi.id, mi.cook_id, cp.user_id
        FROM menu_items mi
        JOIN cook_profiles cp ON mi.cook_id = cp.id
        WHERE mi.id = $1
        """,
        item_id
    )
    
    if not item_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    if item_check['user_id'] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this menu item"
        )
    
    # Build update query dynamically
    update_fields = []
    values = []
    param_count = 1
    
    if menu_item.title is not None:
        update_fields.append(f"title = ${param_count}")
        values.append(menu_item.title)
        param_count += 1
    
    if menu_item.description is not None:
        update_fields.append(f"description = ${param_count}")
        values.append(menu_item.description)
        param_count += 1
    
    if menu_item.price is not None:
        update_fields.append(f"price = ${param_count}")
        values.append(menu_item.price)
        param_count += 1
    
    if menu_item.photo_url is not None:
        update_fields.append(f"photo_url = ${param_count}")
        values.append(menu_item.photo_url)
        param_count += 1
    
    if menu_item.is_available is not None:
        update_fields.append(f"is_available = ${param_count}")
        values.append(menu_item.is_available)
        param_count += 1
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_fields.append("updated_at = NOW()")
    values.append(item_id)
    
    query = f"""
        UPDATE menu_items 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING id, cook_id, title, description, price, photo_url, is_available, created_at, updated_at
    """
    
    updated_item = await db.fetchrow(query, *values)
    
    return MenuItem(
        id=updated_item['id'],
        cook_id=updated_item['cook_id'],
        title=updated_item['title'],
        description=updated_item['description'],
        price=updated_item['price'],
        photo_url=updated_item['photo_url'],
        is_available=updated_item['is_available'],
        created_at=updated_item['created_at'],
        updated_at=updated_item['updated_at']
    )

@router.delete("/{item_id}")
async def delete_menu_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Delete a menu item"""
    # Check if item exists and belongs to current user's cook profile
    item_check = await db.fetchrow(
        """
        SELECT mi.id, mi.cook_id, cp.user_id
        FROM menu_items mi
        JOIN cook_profiles cp ON mi.cook_id = cp.id
        WHERE mi.id = $1
        """,
        item_id
    )
    
    if not item_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    if item_check['user_id'] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this menu item"
        )
    
    # Delete the menu item
    await db.execute("DELETE FROM menu_items WHERE id = $1", item_id)
    
    return {"message": "Menu item deleted successfully"} 
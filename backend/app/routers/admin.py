from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import asyncpg
from app.database import get_db
from app.models import User, Order, Message, OrderStatus
from app.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

# User management
@router.get("/users", response_model=List[User])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get all users (admin only)"""
    users = await db.fetch(
        """
        SELECT id, email, full_name, role, is_active, created_at
        FROM users
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
        """,
        limit, skip
    )
    
    return [
        User(
            id=user['id'],
            email=user['email'],
            full_name=user['full_name'],
            role=user['role'],
            is_active=user['is_active'],
            created_at=user['created_at']
        )
        for user in users
    ]

@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get a specific user by ID (admin only)"""
    user_record = await db.fetchrow(
        "SELECT id, email, full_name, role, is_active, created_at FROM users WHERE id = $1",
        user_id
    )
    
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(
        id=user_record['id'],
        email=user_record['email'],
        full_name=user_record['full_name'],
        role=user_record['role'],
        is_active=user_record['is_active'],
        created_at=user_record['created_at']
    )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Delete a user (admin only)"""
    # Check if user exists
    user_exists = await db.fetchrow("SELECT id FROM users WHERE id = $1", user_id)
    
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete user (cascading deletes should handle related records)
    await db.execute("DELETE FROM users WHERE id = $1", user_id)
    
    return {"message": "User deleted successfully"}

@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Deactivate a user (admin only)"""
    # Check if user exists
    user_exists = await db.fetchrow("SELECT id FROM users WHERE id = $1", user_id)
    
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deactivating themselves
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Deactivate user
    await db.execute("UPDATE users SET is_active = false WHERE id = $1", user_id)
    
    return {"message": "User deactivated successfully"}

# Order management
@router.get("/orders", response_model=List[Order])
async def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[OrderStatus] = None,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get all orders (admin only)"""
    base_query = """
        SELECT id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at
        FROM orders
    """
    params = []
    param_count = 1
    
    if status_filter:
        base_query += f" WHERE status = ${param_count}"
        params.append(status_filter.value)
        param_count += 1
    
    base_query += f" ORDER BY created_at DESC LIMIT ${param_count} OFFSET ${param_count + 1}"
    params.extend([limit, skip])
    
    orders = await db.fetch(base_query, *params)
    
    return [
        Order(
            id=order['id'],
            buyer_id=order['buyer_id'],
            menu_item_id=order['menu_item_id'],
            cook_id=order['cook_id'],
            quantity=order['quantity'],
            total_price=order['total_price'],
            status=order['status'],
            special_instructions=order['special_instructions'],
            created_at=order['created_at'],
            updated_at=order['updated_at']
        )
        for order in orders
    ]

@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(
    order_id: int,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get a specific order by ID (admin only)"""
    order_record = await db.fetchrow(
        """
        SELECT id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at
        FROM orders WHERE id = $1
        """,
        order_id
    )
    
    if not order_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return Order(
        id=order_record['id'],
        buyer_id=order_record['buyer_id'],
        menu_item_id=order_record['menu_item_id'],
        cook_id=order_record['cook_id'],
        quantity=order_record['quantity'],
        total_price=order_record['total_price'],
        status=order_record['status'],
        special_instructions=order_record['special_instructions'],
        created_at=order_record['created_at'],
        updated_at=order_record['updated_at']
    )

@router.delete("/orders/{order_id}")
async def delete_order(
    order_id: int,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Delete an order (admin only)"""
    # Check if order exists
    order_exists = await db.fetchrow("SELECT id FROM orders WHERE id = $1", order_id)
    
    if not order_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Delete order
    await db.execute("DELETE FROM orders WHERE id = $1", order_id)
    
    return {"message": "Order deleted successfully"}

# Message management
@router.get("/messages", response_model=List[Message])
async def get_all_messages(
    skip: int = 0,
    limit: int = 100,
    order_id: Optional[int] = None,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get all messages (admin only)"""
    base_query = """
        SELECT id, order_id, sender_id, content, created_at
        FROM messages
    """
    params = []
    param_count = 1
    
    if order_id:
        base_query += f" WHERE order_id = ${param_count}"
        params.append(order_id)
        param_count += 1
    
    base_query += f" ORDER BY created_at DESC LIMIT ${param_count} OFFSET ${param_count + 1}"
    params.extend([limit, skip])
    
    messages = await db.fetch(base_query, *params)
    
    return [
        Message(
            id=msg['id'],
            order_id=msg['order_id'],
            sender_id=msg['sender_id'],
            content=msg['content'],
            created_at=msg['created_at']
        )
        for msg in messages
    ]

@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Delete a message (admin only)"""
    # Check if message exists
    message_exists = await db.fetchrow("SELECT id FROM messages WHERE id = $1", message_id)
    
    if not message_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Delete message
    await db.execute("DELETE FROM messages WHERE id = $1", message_id)
    
    return {"message": "Message deleted successfully"}

# Statistics
@router.get("/stats")
async def get_admin_stats(
    admin_user: User = Depends(require_admin),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get platform statistics (admin only)"""
    # Get user count
    user_count = await db.fetchval("SELECT COUNT(*) FROM users")
    active_user_count = await db.fetchval("SELECT COUNT(*) FROM users WHERE is_active = true")
    
    # Get cook count
    cook_count = await db.fetchval("SELECT COUNT(*) FROM cook_profiles")
    
    # Get menu item count
    menu_item_count = await db.fetchval("SELECT COUNT(*) FROM menu_items")
    available_menu_item_count = await db.fetchval("SELECT COUNT(*) FROM menu_items WHERE is_available = true")
    
    # Get order count by status
    order_counts = await db.fetch(
        "SELECT status, COUNT(*) as count FROM orders GROUP BY status"
    )
    
    # Get message count
    message_count = await db.fetchval("SELECT COUNT(*) FROM messages")
    
    # Get total revenue
    total_revenue = await db.fetchval("SELECT COALESCE(SUM(total_price), 0) FROM orders WHERE status = 'completed'")
    
    return {
        "users": {
            "total": user_count,
            "active": active_user_count
        },
        "cooks": cook_count,
        "menu_items": {
            "total": menu_item_count,
            "available": available_menu_item_count
        },
        "orders": {status['status']: status['count'] for status in order_counts},
        "messages": message_count,
        "revenue": float(total_revenue) if total_revenue else 0.0
    } 
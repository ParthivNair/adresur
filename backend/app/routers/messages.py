from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import asyncpg
from app.database import get_db
from app.models import Message, MessageCreate, User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=Message)
async def create_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Create a new message for an order"""
    # Check if order exists and user has access to it
    order_check = await db.fetchrow(
        """
        SELECT o.id, o.buyer_id, o.cook_id, cp.user_id as cook_user_id
        FROM orders o
        JOIN cook_profiles cp ON o.cook_id = cp.id
        WHERE o.id = $1
        """,
        message.order_id
    )
    
    if not order_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user is either buyer or cook
    is_buyer = order_check['buyer_id'] == current_user.id
    is_cook = order_check['cook_user_id'] == current_user.id
    
    if not (is_buyer or is_cook):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only message on orders you're involved in"
        )
    
    # Create message
    query = """
        INSERT INTO messages (order_id, sender_id, content, created_at)
        VALUES ($1, $2, $3, NOW())
        RETURNING id, order_id, sender_id, content, created_at
    """
    
    message_record = await db.fetchrow(
        query,
        message.order_id,
        current_user.id,
        message.content
    )
    
    return Message(
        id=message_record['id'],
        order_id=message_record['order_id'],
        sender_id=message_record['sender_id'],
        content=message_record['content'],
        created_at=message_record['created_at']
    )

@router.get("/order/{order_id}", response_model=List[Message])
async def get_order_messages(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get all messages for a specific order"""
    # Check if order exists and user has access to it
    order_check = await db.fetchrow(
        """
        SELECT o.id, o.buyer_id, o.cook_id, cp.user_id as cook_user_id
        FROM orders o
        JOIN cook_profiles cp ON o.cook_id = cp.id
        WHERE o.id = $1
        """,
        order_id
    )
    
    if not order_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user is either buyer or cook
    is_buyer = order_check['buyer_id'] == current_user.id
    is_cook = order_check['cook_user_id'] == current_user.id
    
    if not (is_buyer or is_cook):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view messages for orders you're involved in"
        )
    
    # Get messages
    messages = await db.fetch(
        """
        SELECT id, order_id, sender_id, content, created_at
        FROM messages
        WHERE order_id = $1
        ORDER BY created_at ASC
        """,
        order_id
    )
    
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

@router.get("/", response_model=List[Message])
async def get_user_messages(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get all messages for orders the current user is involved in"""
    # Get user's cook profile ID if they have one
    cook_profile = await db.fetchrow(
        "SELECT id FROM cook_profiles WHERE user_id = $1",
        current_user.id
    )
    
    # Build query to get messages from orders user is involved in
    base_query = """
        SELECT m.id, m.order_id, m.sender_id, m.content, m.created_at
        FROM messages m
        JOIN orders o ON m.order_id = o.id
        WHERE (o.buyer_id = $1
    """
    params = [current_user.id]
    param_count = 2
    
    if cook_profile:
        base_query += f" OR o.cook_id = ${param_count}"
        params.append(cook_profile['id'])
        param_count += 1
    
    base_query += f") ORDER BY m.created_at DESC LIMIT ${param_count} OFFSET ${param_count + 1}"
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
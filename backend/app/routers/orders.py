from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import asyncpg
from app.database import get_db
from app.models import Order, OrderCreate, OrderUpdate, OrderStatus, User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
async def place_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Place a new order"""
    # Get menu item details and cook info
    menu_item = await db.fetchrow(
        """
        SELECT mi.id, mi.cook_id, mi.title, mi.price, mi.is_available, cp.user_id as cook_user_id
        FROM menu_items mi
        JOIN cook_profiles cp ON mi.cook_id = cp.id
        WHERE mi.id = $1
        """,
        order.menu_item_id
    )
    
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    if not menu_item['is_available']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Menu item is not available"
        )
    
    # Prevent users from ordering their own items
    if menu_item['cook_user_id'] == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot order your own menu items"
        )
    
    # Calculate total price
    total_price = menu_item['price'] * order.quantity
    
    # Create order
    query = """
        INSERT INTO orders (buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
        RETURNING id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at
    """
    
    order_record = await db.fetchrow(
        query,
        current_user.id,
        order.menu_item_id,
        menu_item['cook_id'],
        order.quantity,
        total_price,
        OrderStatus.PENDING.value,
        order.special_instructions
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

@router.get("/", response_model=List[Order])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[OrderStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get orders for current user (both as buyer and cook)"""
    # Get user's cook profile ID if they have one
    cook_profile = await db.fetchrow(
        "SELECT id FROM cook_profiles WHERE user_id = $1",
        current_user.id
    )
    
    base_query = """
        SELECT id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at
        FROM orders
        WHERE (buyer_id = $1
    """
    params = [current_user.id]
    param_count = 2
    
    if cook_profile:
        base_query += f" OR cook_id = ${param_count}"
        params.append(cook_profile['id'])
        param_count += 1
    
    base_query += ")"
    
    if status_filter:
        base_query += f" AND status = ${param_count}"
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

@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get a specific order"""
    # Get user's cook profile ID if they have one
    cook_profile = await db.fetchrow(
        "SELECT id FROM cook_profiles WHERE user_id = $1",
        current_user.id
    )
    
    # Build query to check if user has access to this order
    query = """
        SELECT id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at
        FROM orders
        WHERE id = $1 AND (buyer_id = $2
    """
    params = [order_id, current_user.id]
    
    if cook_profile:
        query += " OR cook_id = $3)"
        params.append(cook_profile['id'])
    else:
        query += ")"
    
    order_record = await db.fetchrow(query, *params)
    
    if not order_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or access denied"
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

@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Update order status or special instructions"""
    # Get order details with cook info
    order_check = await db.fetchrow(
        """
        SELECT o.id, o.buyer_id, o.cook_id, o.status, cp.user_id as cook_user_id
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
    
    # Check permissions
    is_buyer = order_check['buyer_id'] == current_user.id
    is_cook = order_check['cook_user_id'] == current_user.id
    
    if not (is_buyer or is_cook):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this order"
        )
    
    # Status updates are only allowed by cook
    if order_update.status and not is_cook:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the cook can update order status"
        )
    
    # Build update query
    update_fields = []
    values = []
    param_count = 1
    
    if order_update.status:
        # Validate status transition
        current_status = OrderStatus(order_check['status'])
        new_status = order_update.status
        
        # Define valid transitions
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELLED],
            OrderStatus.READY: [OrderStatus.COMPLETED],
            OrderStatus.COMPLETED: [],
            OrderStatus.CANCELLED: []
        }
        
        if new_status not in valid_transitions[current_status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {current_status.value} to {new_status.value}"
            )
        
        update_fields.append(f"status = ${param_count}")
        values.append(new_status.value)
        param_count += 1
    
    if order_update.special_instructions is not None:
        update_fields.append(f"special_instructions = ${param_count}")
        values.append(order_update.special_instructions)
        param_count += 1
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_fields.append("updated_at = NOW()")
    values.append(order_id)
    
    query = f"""
        UPDATE orders 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at
    """
    
    updated_order = await db.fetchrow(query, *values)
    
    return Order(
        id=updated_order['id'],
        buyer_id=updated_order['buyer_id'],
        menu_item_id=updated_order['menu_item_id'],
        cook_id=updated_order['cook_id'],
        quantity=updated_order['quantity'],
        total_price=updated_order['total_price'],
        status=updated_order['status'],
        special_instructions=updated_order['special_instructions'],
        created_at=updated_order['created_at'],
        updated_at=updated_order['updated_at']
    ) 
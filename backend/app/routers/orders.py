from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Any
import asyncpg
from app.database import get_db
from app.models import Order, OrderCreate, OrderUpdate, OrderStatus, User, BatchOrderCreate, BatchOrder
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/batch", response_model=List[Order])
async def place_batch_order(
    batch_order: BatchOrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Place multiple orders as a batch"""
    if not batch_order.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch order must contain at least one item"
        )
    
    # Group items by cook to ensure all items are from the same cook
    cook_ids = set()
    total_price = 0
    validated_items = []
    
    for item in batch_order.items:
        # Get menu item details and cook info
        menu_item = await db.fetchrow(
            """
            SELECT mi.id, mi.cook_id, mi.title, mi.price, mi.is_available, cp.user_id as cook_user_id
            FROM menu_items mi
            JOIN cook_profiles cp ON mi.cook_id = cp.id
            WHERE mi.id = $1
            """,
            item.menu_item_id
        )
        
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item {item.menu_item_id} not found"
            )
        
        if not menu_item['is_available']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item {menu_item['title']} is not available"
            )
        
        # Prevent users from ordering their own items
        if menu_item['cook_user_id'] == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot order your own menu items"
            )
        
        cook_ids.add(menu_item['cook_id'])
        item_total = menu_item['price'] * item.quantity
        total_price += item_total
        
        validated_items.append({
            'item': item,
            'menu_item': menu_item,
            'item_total': item_total
        })
    
    # Ensure all items are from the same cook (single cook per batch order)
    if len(cook_ids) > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All items in a batch order must be from the same cook"
        )
    
    cook_id = list(cook_ids)[0]
    
    # Create a single batch order with all items
    async with db.transaction():
        # Create the batch order first
        batch_query = """
            INSERT INTO batch_orders (buyer_id, total_price, status, created_at, updated_at)
            VALUES ($1, $2, $3, NOW(), NOW())
            RETURNING id, buyer_id, total_price, status, created_at, updated_at
        """
        
        batch_record = await db.fetchrow(
            batch_query,
            current_user.id,
            total_price,
            OrderStatus.PENDING.value
        )
        
        if not batch_record:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create batch order"
            )
        
        batch_order_id = batch_record['id']
        created_orders = []
        
        # Create individual order records linked to the batch
        for validated_item in validated_items:
            item = validated_item['item']
            menu_item = validated_item['menu_item']
            item_total = validated_item['item_total']
            
            # Create order linked to batch
            order_query = """
                INSERT INTO orders (buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, batch_order_id, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW(), NOW())
                RETURNING id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, batch_order_id, created_at, updated_at
            """
            
            order_record = await db.fetchrow(
                order_query,
                current_user.id,
                item.menu_item_id,
                menu_item['cook_id'],
                item.quantity,
                item_total,
                OrderStatus.PENDING.value,
                item.special_instructions,
                batch_order_id
            )
            
            if order_record:
                created_orders.append(Order(
                    id=order_record['id'],
                    buyer_id=order_record['buyer_id'],
                    menu_item_id=order_record['menu_item_id'],
                    cook_id=order_record['cook_id'],
                    quantity=order_record['quantity'],
                    total_price=order_record['total_price'],
                    status=order_record['status'],
                    special_instructions=order_record['special_instructions'],
                    batch_order_id=order_record['batch_order_id'],
                    created_at=order_record['created_at'],
                    updated_at=order_record['updated_at']
                ))
    
    return created_orders

@router.post("/", response_model=Order)
async def place_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Place a new order (single item)"""
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
    
    if not order_record:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
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

@router.get("/", response_model=List[dict])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[OrderStatus] = None,
    as_cook: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: asyncpg.Connection = Depends(get_db)
):
    """Get orders for current user with enhanced information"""
    
    if as_cook:
        # Get orders where current user is the cook
        cook_profile = await db.fetchrow(
            "SELECT id FROM cook_profiles WHERE user_id = $1",
            current_user.id
        )
        
        if not cook_profile:
            return []
        
        base_query = """
            SELECT 
                o.id, o.buyer_id, o.menu_item_id, o.cook_id, o.quantity, 
                o.total_price, o.status, o.special_instructions, o.created_at, o.updated_at,
                mi.title as menu_item_title, mi.description as menu_item_description, 
                mi.price as menu_item_price, mi.photo_url as menu_item_photo,
                u.full_name as buyer_name, u.email as buyer_email
            FROM orders o
            JOIN menu_items mi ON o.menu_item_id = mi.id
            JOIN users u ON o.buyer_id = u.id
            WHERE o.cook_id = $1
        """
        params = [cook_profile['id']]
        param_count = 2
    else:
        # Get orders where current user is the buyer
        base_query = """
            SELECT 
                o.id, o.buyer_id, o.menu_item_id, o.cook_id, o.quantity, 
                o.total_price, o.status, o.special_instructions, o.created_at, o.updated_at,
                mi.title as menu_item_title, mi.description as menu_item_description, 
                mi.price as menu_item_price, mi.photo_url as menu_item_photo,
                cp.name as cook_name, u.full_name as cook_full_name
            FROM orders o
            JOIN menu_items mi ON o.menu_item_id = mi.id
            JOIN cook_profiles cp ON o.cook_id = cp.id
            JOIN users u ON cp.user_id = u.id
            WHERE o.buyer_id = $1
        """
        params = [current_user.id]
        param_count = 2
    
    if status_filter:
        base_query += f" AND o.status = ${param_count}"
        params.append(status_filter.value)  # type: ignore
        param_count += 1
    
    base_query += f" ORDER BY o.created_at DESC LIMIT ${param_count} OFFSET ${param_count + 1}"
    params.extend([limit, skip])
    
    orders = await db.fetch(base_query, *params)
    
    result = []
    for order in orders:
        order_dict = {
            'id': order['id'],
            'buyer_id': order['buyer_id'],
            'menu_item_id': order['menu_item_id'],
            'cook_id': order['cook_id'],
            'quantity': order['quantity'],
            'total_price': order['total_price'],
            'status': order['status'],
            'special_instructions': order['special_instructions'],
            'created_at': order['created_at'],
            'updated_at': order['updated_at'],
            'menuItem': {
                'id': order['menu_item_id'],
                'title': order['menu_item_title'],
                'description': order['menu_item_description'],
                'price': order['menu_item_price'],
                'photo_url': order['menu_item_photo']
            }
        }
        
        if as_cook:
            order_dict['buyer_name'] = order['buyer_name']
            order_dict['buyer_email'] = order['buyer_email']
        else:
            order_dict['cook_name'] = order['cook_name']
            order_dict['cook_full_name'] = order['cook_full_name']
        
        result.append(order_dict)
    
    return result

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
    is_cook = order_check['cook_user_id'] == current_user.id
    is_buyer = order_check['buyer_id'] == current_user.id
    
    if not (is_cook or is_buyer):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this order"
        )
    
    # Only cooks can update status, buyers can update special instructions
    update_fields = []
    params = []
    param_count = 1
    
    if order_update.status and is_cook:
        update_fields.append(f"status = ${param_count}")
        params.append(order_update.status.value)
        param_count += 1
    
    if order_update.special_instructions and is_buyer:
        update_fields.append(f"special_instructions = ${param_count}")
        params.append(order_update.special_instructions)
        param_count += 1
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )
    
    # Add updated_at
    update_fields.append(f"updated_at = NOW()")
    
    # Build and execute update query
    query = f"""
        UPDATE orders 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count}
        RETURNING id, buyer_id, menu_item_id, cook_id, quantity, total_price, status, special_instructions, created_at, updated_at
    """
    params.append(order_id)
    
    updated_order = await db.fetchrow(query, *params)
    
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update order"
        )
    
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
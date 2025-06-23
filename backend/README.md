# Adresur Backend API

Backend API for Adresur - A home-cooked meal sharing platform that connects home cooks with local families and individuals.

## Features

- **Authentication**: User registration/login with JWT tokens and role-based access (user/admin)
- **Cook Profiles**: CRUD operations for cook profiles with bios, photos, and delivery radius
- **Menu Management**: CRUD operations for menu items with availability tracking
- **Order System**: Complete order lifecycle from placement to completion with status tracking
- **Messaging**: Order-based messaging system between buyers and cooks
- **Admin Panel**: Admin-only endpoints for user, order, and message management

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Supabase**: PostgreSQL database with real-time capabilities
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation and serialization
- **AsyncPG**: Async PostgreSQL driver
- **Uvicorn**: ASGI server

## Setup Instructions

### Prerequisites

- Python 3.8+
- Supabase account and project
- Environment variables configured

### 1. Environment Setup

Create a `.env` file in the backend directory:

```env
DB_PASS=your_supabase_db_password
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Database Setup

1. Create a new Supabase project
2. Run the SQL schema from `database_schema.sql` in your Supabase SQL editor
3. Update your `.env` file with the correct database credentials

### 4. Run the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Authentication Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/token` - OAuth2 compatible token endpoint

### Cook Profile Endpoints

- `POST /cooks/` - Create cook profile
- `GET /cooks/` - Get all cook profiles
- `GET /cooks/{cook_id}` - Get specific cook profile
- `GET /cooks/me/profile` - Get current user's cook profile
- `PUT /cooks/{cook_id}` - Update cook profile
- `DELETE /cooks/{cook_id}` - Delete cook profile

### Menu Item Endpoints

- `POST /menu/` - Create menu item
- `GET /menu/` - Get menu items (with filtering)
- `GET /menu/{item_id}` - Get specific menu item
- `GET /menu/cook/{cook_id}` - Get menu items for a cook
- `PUT /menu/{item_id}` - Update menu item
- `DELETE /menu/{item_id}` - Delete menu item

### Order Endpoints

- `POST /orders/` - Place new order
- `GET /orders/` - Get user's orders (buyer + cook)
- `GET /orders/{order_id}` - Get specific order
- `PUT /orders/{order_id}` - Update order status/instructions

### Message Endpoints

- `POST /messages/` - Create message for an order
- `GET /messages/order/{order_id}` - Get messages for an order
- `GET /messages/` - Get all user's messages

### Admin Endpoints (Admin Only)

- `GET /admin/users` - Get all users
- `GET /admin/users/{user_id}` - Get specific user
- `DELETE /admin/users/{user_id}` - Delete user
- `PUT /admin/users/{user_id}/deactivate` - Deactivate user
- `GET /admin/orders` - Get all orders
- `DELETE /admin/orders/{order_id}` - Delete order
- `GET /admin/messages` - Get all messages
- `DELETE /admin/messages/{message_id}` - Delete message
- `GET /admin/stats` - Get platform statistics

## Order Status Flow

Orders follow this status progression:

1. **pending** → **preparing** or **cancelled**
2. **preparing** → **ready** or **cancelled**
3. **ready** → **completed**
4. **completed** (final state)
5. **cancelled** (final state)

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Error Handling

The API returns consistent error responses:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Testing

Test users are created with the database schema:

- **Admin**: `admin@adresur.com` / `admin123`
- **User**: `user@example.com` / `user123`

## Development Notes

- All endpoints include proper error handling and validation
- Database queries use parameterized statements to prevent SQL injection
- Passwords are hashed using bcrypt
- JWT tokens have configurable expiration times
- CORS is enabled for development (configure for production)

## Production Considerations

1. Update CORS settings to allow only your frontend domain
2. Use environment-specific JWT secret keys
3. Configure proper logging and monitoring
4. Set up database connection pooling
5. Implement rate limiting
6. Use HTTPS in production
7. Regular database backups

## License

All Rights Reserved - Adresur Platform

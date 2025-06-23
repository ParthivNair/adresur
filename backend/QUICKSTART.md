# Adresur Backend - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment

1. **Create Supabase Project**

   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note down your project URL and anon key

2. **Create `.env` file**

   ```bash
   cp env.example .env
   ```

   Edit `.env` with your Supabase credentials:

   ```env
   DB_PASS=your_supabase_db_password
   REACT_APP_SUPABASE_URL=https://your-project.supabase.co
   REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
   JWT_SECRET_KEY=your_super_secret_jwt_key_here
   ```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Setup Database

1. Open your Supabase project dashboard
2. Go to SQL Editor
3. Copy and paste the contents of `database_schema.sql`
4. Run the SQL script

### Step 4: Start the Server

```bash
# Option 1: Using the start script
python start.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Test the API

```bash
# Run the test script
python test_api.py
```

## 🎯 Quick Test

Once running, visit:

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔐 Test Credentials

The database schema includes test users:

- **Admin**: `admin@adresur.com` / `admin123`
- **User**: `user@example.com` / `user123`

## 📋 API Endpoints Summary

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Cook Profiles

- `POST /cooks/` - Create cook profile
- `GET /cooks/` - List all cooks
- `GET /cooks/{id}` - Get cook details

### Menu Items

- `POST /menu/` - Create menu item
- `GET /menu/` - List menu items
- `GET /menu/cook/{cook_id}` - Get cook's menu

### Orders

- `POST /orders/` - Place order
- `GET /orders/` - Get user's orders
- `PUT /orders/{id}` - Update order status

### Messages

- `POST /messages/` - Send message
- `GET /messages/order/{order_id}` - Get order messages

### Admin (Admin Only)

- `GET /admin/users` - List all users
- `GET /admin/orders` - List all orders
- `GET /admin/stats` - Platform statistics

## 🔧 Common Issues

**Connection Error**: Make sure your Supabase credentials are correct in `.env`

**Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Database Errors**: Verify the database schema was applied correctly in Supabase

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the interactive API docs at `/docs`
3. Test endpoints using the provided test credentials
4. Start building your frontend integration!

---

**Happy coding! 🎉**

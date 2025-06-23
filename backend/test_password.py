#!/usr/bin/env python3
"""
Test password verification to debug login issues
"""
import asyncio
import asyncpg
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def test_passwords():
    """Test password verification against database"""
    
    print("🔍 Testing password verification...")
    print("=" * 50)
    
    # Generate fresh hashes
    admin_password = "admin123"
    user_password = "user123"
    
    admin_hash = pwd_context.hash(admin_password)
    user_hash = pwd_context.hash(user_password)
    
    print(f"Generated admin hash: {admin_hash}")
    print(f"Generated user hash: {user_hash}")
    print()
    
    # Test verification
    admin_verify = pwd_context.verify(admin_password, admin_hash)
    user_verify = pwd_context.verify(user_password, user_hash)
    
    print(f"Admin password verification: {admin_verify}")
    print(f"User password verification: {user_verify}")
    print()
    
    # Try to connect to database and check current hashes
    try:
        database_url = os.getenv("DATABASE_URL", "")
        db_pass = os.getenv("DB_PASS", "")
        supabase_url = os.getenv("REACT_APP_SUPABASE_URL", "")
        
        if database_url:
            # Use transaction pooler
            connection_string = database_url.replace("${DB_PASS}", db_pass)
            print(f"Connecting with: {connection_string[:50]}...")
            connection = await asyncpg.connect(connection_string)
        else:
            # Use direct connection
            db_url = supabase_url.replace("https://", "").replace("http://", "")
            project_ref = db_url.split(".")[0]
            print(f"Connecting to project: {project_ref}")
            
            connection = await asyncpg.connect(
                host=f"db.{project_ref}.supabase.co",
                port=5432,
                user="postgres",
                password=db_pass,
                database="postgres"
            )
        
        print("✅ Connected to database!")
        
        # Check current users
        users = await connection.fetch("""
            SELECT email, role, hashed_password, is_active 
            FROM users 
            WHERE email IN ('admin@adresur.com', 'user@example.com')
            ORDER BY email
        """)
        
        print("\n📋 Current users in database:")
        for user in users:
            print(f"Email: {user['email']}")
            print(f"Role: {user['role']}")
            print(f"Active: {user['is_active']}")
            print(f"Hash: {user['hashed_password'][:50]}...")
            
            # Test if current hash works with our passwords
            if user['email'] == 'admin@adresur.com':
                test_result = pwd_context.verify(admin_password, user['hashed_password'])
                print(f"Admin password test: {test_result}")
            elif user['email'] == 'user@example.com':
                test_result = pwd_context.verify(user_password, user['hashed_password'])
                print(f"User password test: {test_result}")
            print("-" * 30)
        
        # Update with fresh hashes
        print("\n🔄 Updating with fresh hashes...")
        
        await connection.execute("""
            UPDATE users 
            SET hashed_password = $1, updated_at = NOW() 
            WHERE email = 'admin@adresur.com'
        """, admin_hash)
        
        await connection.execute("""
            UPDATE users 
            SET hashed_password = $1, updated_at = NOW() 
            WHERE email = 'user@example.com'
        """, user_hash)
        
        print("✅ Updated password hashes!")
        
        await connection.close()
        
        print("\n🎯 Try logging in now with:")
        print("Admin: admin@adresur.com / admin123")
        print("User: user@example.com / user123")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    asyncio.run(test_passwords()) 
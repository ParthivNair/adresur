#!/usr/bin/env python3
"""
Fix password hashes in the database for sample users
"""

import asyncio
import asyncpg
from pathlib import Path
from app.config import settings
from app.utils.auth import get_password_hash
import sys

async def fix_passwords():
    """Update the database with correct password hashes"""
    
    print("🔐 Fixing password hashes in database...")
    print("=" * 50)
    
    try:
        # Generate correct password hashes
        admin_password = "admin123"
        user_password = "user123"
        
        admin_hash = get_password_hash(admin_password)
        user_hash = get_password_hash(user_password)
        
        print(f"✅ Generated hash for admin password: {admin_password}")
        print(f"✅ Generated hash for user password: {user_password}")
        
        # Connect to database
        if settings.database_url:
            print("🔗 Connecting using transaction pooler...")
            connection = await asyncpg.connect(settings.database_url.replace("${DB_PASS}", settings.db_pass))
        else:
            # Extract database connection details from Supabase URL
            if not settings.supabase_url or not settings.db_pass:
                print("❌ Error: Missing database configuration!")
                return False
            
            db_url = settings.supabase_url.replace("https://", "").replace("http://", "")
            project_ref = db_url.split(".")[0]
            
            print(f"🔗 Connecting to project: {project_ref}")
            
            connection = await asyncpg.connect(
                host=f"db.{project_ref}.supabase.co",
                port=5432,
                user="postgres",
                password=settings.db_pass,
                database="postgres"
            )
        
        print("✅ Connected to database successfully!")
        
        # Update admin user password
        print("🔄 Updating admin user password...")
        admin_result = await connection.execute("""
            INSERT INTO users (email, full_name, role, hashed_password, is_active, created_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            ON CONFLICT (email) 
            DO UPDATE SET hashed_password = $4, updated_at = NOW()
        """, 'admin@adresur.com', 'Admin User', 'admin', admin_hash, True)
        
        # Update regular user password
        print("🔄 Updating regular user password...")
        user_result = await connection.execute("""
            INSERT INTO users (email, full_name, role, hashed_password, is_active, created_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            ON CONFLICT (email) 
            DO UPDATE SET hashed_password = $4, updated_at = NOW()
        """, 'user@example.com', 'Test User', 'user', user_hash, True)
        
        # Verify the users exist
        admin_check = await connection.fetchrow("SELECT email, role FROM users WHERE email = $1", 'admin@adresur.com')
        user_check = await connection.fetchrow("SELECT email, role FROM users WHERE email = $1", 'user@example.com')
        
        if admin_check:
            print(f"✅ Admin user verified: {admin_check['email']} ({admin_check['role']})")
        else:
            print("❌ Admin user not found!")
            
        if user_check:
            print(f"✅ Regular user verified: {user_check['email']} ({user_check['role']})")
        else:
            print("❌ Regular user not found!")
        
        await connection.close()
        
        print("\n🎉 Password hashes updated successfully!")
        print("\n📋 Test credentials:")
        print("Admin: admin@adresur.com / admin123")
        print("User:  user@example.com / user123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing passwords: {e}")
        return False

def main():
    """Main function"""
    print("=" * 50)
    print("🔧 Adresur Password Fix Tool")
    print("=" * 50)
    
    try:
        success = asyncio.run(fix_passwords())
        if success:
            print("\n🎯 Next steps:")
            print("1. Try logging in with: admin@adresur.com / admin123")
            print("2. Test the API at http://localhost:8000/docs")
            sys.exit(0)
        else:
            print("\n❌ Password fix failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
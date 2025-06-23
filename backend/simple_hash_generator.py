#!/usr/bin/env python3
"""
Simple password hash generator
"""
from passlib.context import CryptContext

# Create password context with same settings as the app
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def main():
    print("🔐 Generating fresh password hashes...")
    print("=" * 50)
    
    admin_password = "admin123"
    user_password = "user123"
    
    admin_hash = generate_hash(admin_password)
    user_hash = generate_hash(user_password)
    
    print(f"Admin password: {admin_password}")
    print(f"Admin hash: {admin_hash}")
    print()
    print(f"User password: {user_password}")
    print(f"User hash: {user_hash}")
    print()
    print("🔧 SQL to run in Supabase SQL Editor:")
    print("=" * 50)
    print(f"""
-- Update admin user password
UPDATE users 
SET hashed_password = '{admin_hash}', updated_at = NOW() 
WHERE email = 'admin@adresur.com';

-- Update regular user password  
UPDATE users 
SET hashed_password = '{user_hash}', updated_at = NOW() 
WHERE email = 'user@example.com';

-- Verify updates
SELECT email, role, is_active FROM users WHERE email IN ('admin@adresur.com', 'user@example.com');
""")

if __name__ == "__main__":
    main() 
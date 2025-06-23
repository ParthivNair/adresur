#!/usr/bin/env python3
"""
Generate correct password hashes for the sample users
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.auth import get_password_hash

def main():
    print("🔐 Generating password hashes for sample users...")
    print("=" * 50)
    
    # Generate hashes for sample passwords
    admin_password = "admin123"
    user_password = "user123"
    
    admin_hash = get_password_hash(admin_password)
    user_hash = get_password_hash(user_password)
    
    print(f"Admin password: {admin_password}")
    print(f"Admin hash: {admin_hash}")
    print()
    print(f"User password: {user_password}")
    print(f"User hash: {user_hash}")
    print()
    print("📝 Updated SQL for database_schema.sql:")
    print("-" * 50)
    print(f"-- Insert a sample admin user (password: {admin_password})")
    print(f"INSERT INTO users (email, full_name, role, hashed_password)")
    print(f"VALUES ('admin@adresur.com', 'Admin User', 'admin', '{admin_hash}')")
    print(f"ON CONFLICT (email) DO UPDATE SET hashed_password = '{admin_hash}';")
    print()
    print(f"-- Insert a sample regular user (password: {user_password})")
    print(f"INSERT INTO users (email, full_name, role, hashed_password)")
    print(f"VALUES ('user@example.com', 'Test User', 'user', '{user_hash}')")
    print(f"ON CONFLICT (email) DO UPDATE SET hashed_password = '{user_hash}';")

if __name__ == "__main__":
    main() 
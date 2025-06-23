#!/usr/bin/env python3
"""
Database Connection Test Script
This script tests the database connection and helps diagnose configuration issues.
"""

import os
import sys
import asyncio
import asyncpg
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
root_dir = Path(__file__).parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

async def test_database_connection():
    """Test database connection with current configuration"""
    print("🔍 Testing database connection...")
    print(f"📁 Loading .env from: {env_path}")
    
    # Get configuration values
    db_pass = os.getenv("DB_PASS", "")
    supabase_url = os.getenv("REACT_APP_SUPABASE_URL", "")
    supabase_anon_key = os.getenv("REACT_APP_SUPABASE_ANON_KEY", "")
    use_pooler = os.getenv("USE_POOLER", "false").lower() == "true"
    
    print(f"🔗 Supabase URL: {supabase_url}")
    print(f"🔑 Has DB Password: {'Yes' if db_pass else 'No'}")
    print(f"🎫 Has Anon Key: {'Yes' if supabase_anon_key else 'No'}")
    print(f"🏊 Using Pooler: {'Yes' if use_pooler else 'No'}")
    
    if not all([db_pass, supabase_url, supabase_anon_key]):
        print("❌ Missing required environment variables!")
        print("📝 Please update your .env file with:")
        print("   - DB_PASS: Your Supabase database password")
        print("   - REACT_APP_SUPABASE_URL: Your Supabase project URL")
        print("   - REACT_APP_SUPABASE_ANON_KEY: Your Supabase anon key")
        return False
    
    try:
        # Extract project reference from URL
        db_url = supabase_url.replace("https://", "").replace("http://", "")
        project_ref = db_url.split(".")[0]
        
        print(f"📊 Project Reference: {project_ref}")
        
        if use_pooler:
            # Use connection pooler
            host = "aws-0-us-west-1.pooler.supabase.com"
            port = 6543
            user = f"postgres.{project_ref}"
            print(f"🏊 Using Connection Pooler")
            print(f"🖥️  Pooler Host: {host}")
            print(f"🔌 Pooler Port: {port}")
            print(f"👤 Pooler User: {user}")
        else:
            # Use direct connection
            host = f"db.{project_ref}.supabase.co"
            port = 5432
            user = "postgres"
            print(f"🖥️  Database Host: {host}")
            print(f"🔌 Database Port: {port}")
            print(f"👤 Database User: {user}")
        
        # Attempt connection
        print("🔌 Attempting database connection...")
        connection = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=db_pass,
            database="postgres"
        )
        
        # Test basic query
        result = await connection.fetchval("SELECT 1")
        await connection.close()
        
        if result == 1:
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed - unexpected result")
            return False
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        if not use_pooler:
            print("1. Try enabling the connection pooler by setting USE_POOLER=true in .env")
            print("2. Verify your Supabase project URL is correct")
        print("3. Check that your database password is correct")
        print("4. Ensure your Supabase project is running")
        print("5. Verify network connectivity")
        return False

async def test_api_health():
    """Test if the API server is running"""
    import requests
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API server is not running")
        print("💡 Start the server with: python backend/start.py")
        return False
    except Exception as e:
        print(f"❌ Error checking API health: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Adresur Database Connection Test\n")
    
    # Test environment file
    if not env_path.exists():
        print(f"❌ .env file not found at: {env_path}")
        print("📝 Please create a .env file in the root directory")
        return
    
    print(f"✅ Found .env file at: {env_path}\n")
    
    # Test database connection
    db_success = asyncio.run(test_database_connection())
    
    print("\n" + "="*50)
    
    # Test API health
    api_success = asyncio.run(test_api_health())
    
    print("\n" + "="*50)
    print("📋 Summary:")
    print(f"   Database: {'✅ Connected' if db_success else '❌ Failed'}")
    print(f"   API Server: {'✅ Running' if api_success else '❌ Not Running'}")
    
    if db_success and api_success:
        print("\n🎉 All systems are ready! You can now run sample_data.py")
    else:
        print("\n🔧 Please fix the issues above before running sample_data.py")

if __name__ == "__main__":
    main() 
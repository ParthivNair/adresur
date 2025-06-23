#!/usr/bin/env python3
"""
Database Setup Script for Adresur
This script creates all the necessary tables in the Supabase database.
"""

import asyncio
import asyncpg
from pathlib import Path
from app.config import settings
import sys

async def setup_database():
    """Create all database tables and initial data"""
    
    print("🗄️  Setting up Adresur database...")
    print(f"📍 Connecting to database...")
    
    # Read the SQL schema file
    schema_file = Path(__file__).parent / "database_schema.sql"
    
    if not schema_file.exists():
        print("❌ Error: database_schema.sql file not found!")
        return False
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print(f"📖 Read schema file: {len(schema_sql)} characters")
        
        # Connect using transaction pooler URL if available, otherwise use individual components
        if settings.database_url:
            print("🔗 Using transaction pooler connection...")
            connection = await asyncpg.connect(settings.database_url)
        else:
            # Extract database connection details from Supabase URL
            if not settings.supabase_url or not settings.db_pass:
                print("❌ Error: Missing Supabase URL or database password in environment variables!")
                print("Make sure your .env file contains:")
                print("- DATABASE_URL=postgresql://postgres.project:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
                print("OR")
                print("- REACT_APP_SUPABASE_URL=https://your-project.supabase.co")
                print("- DB_PASS=your_supabase_db_password")
                return False
            
            # Parse Supabase URL to get project reference
            db_url = settings.supabase_url.replace("https://", "").replace("http://", "")
            project_ref = db_url.split(".")[0]
            
            print(f"🔗 Connecting to project: {project_ref} (direct connection)")
            
            # Connect to database
            connection = await asyncpg.connect(
                host=f"db.{project_ref}.supabase.co",
                port=5432,
                user="postgres",
                password=settings.db_pass,
                database="postgres"
            )
        
        print("✅ Connected to database successfully!")
        
        # Execute the schema SQL
        print("🔨 Creating tables and indexes...")
        await connection.execute(schema_sql)
        
        print("✅ Database schema created successfully!")
        
        # Verify tables were created
        print("🔍 Verifying tables...")
        tables = await connection.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        print(f"📋 Created {len(tables)} tables:")
        for table in tables:
            print(f"   ✓ {table['table_name']}")
        
        # Check if sample users were created
        user_count = await connection.fetchval("SELECT COUNT(*) FROM users")
        print(f"👥 Sample users created: {user_count}")
        
        await connection.close()
        print("🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your Supabase project is active")
        print("2. Verify your database password is correct")
        print("3. Check that your DATABASE_URL or Supabase URL is properly formatted")
        print("4. For transaction pooler, use: postgresql://postgres.project:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
        return False

def main():
    """Main function to run database setup"""
    print("=" * 50)
    print("🚀 Adresur Database Setup")
    print("=" * 50)
    
    try:
        success = asyncio.run(setup_database())
        if success:
            print("\n🎯 Next steps:")
            print("1. Start the API server: python start.py")
            print("2. Visit http://localhost:8000/docs to test the API")
            print("3. Use sample_data.py to add test data")
            sys.exit(0)
        else:
            print("\n❌ Database setup failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
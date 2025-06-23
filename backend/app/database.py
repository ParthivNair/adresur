from supabase.client import create_client, Client
from app.config import settings
import asyncpg
from typing import AsyncGenerator
from fastapi import HTTPException
from urllib.parse import urlparse

# Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_anon_key)

# Database connection for direct SQL operations
async def get_database_connection():
    """Get direct database connection using transaction pooler for better performance"""
    try:
        # Use DATABASE_URL if provided (transaction pooler), otherwise fall back to individual components
        if settings.database_url:
            # Parse the DATABASE_URL (transaction pooler format)
            # Format: postgresql://postgres.project:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
            # Disable statement cache for pgbouncer compatibility
            connection = await asyncpg.connect(settings.database_url, statement_cache_size=0)
        else:
            # Fallback to individual connection components (legacy method)
            # Extract database connection details from Supabase URL
            db_url = settings.supabase_url.replace("https://", "").replace("http://", "")
            project_ref = db_url.split(".")[0]
            
            connection = await asyncpg.connect(
                host=f"db.{project_ref}.supabase.co",
                port=5432,  # Direct connection port
                user="postgres",
                password=settings.db_pass,
                database="postgres",
                statement_cache_size=0  # Disable statement cache for pgbouncer compatibility
            )
        
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )

async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """Dependency for getting database connection"""
    conn = None
    try:
        conn = await get_database_connection()
        yield conn
    finally:
        if conn:
            await conn.close() 
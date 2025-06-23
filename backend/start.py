#!/usr/bin/env python3
"""
Startup script for Adresur Backend API
"""

import uvicorn
import os
from app.config import settings

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Starting Adresur Backend API...")
    print(f"📍 Server will be available at: http://localhost:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"📖 ReDoc Documentation: http://localhost:{port}/redoc")
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    ) 
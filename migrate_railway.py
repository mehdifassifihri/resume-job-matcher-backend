#!/usr/bin/env python3
"""
Migration script for Railway deployment.
This script initializes the database and runs migrations.
"""
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from auth.init_db import create_tables
from auth.database import engine

def main():
    """Initialize database tables for Railway deployment."""
    print("🚀 Initializing database for Railway deployment...")
    
    try:
        # Create all tables
        create_tables()
        print("✅ Database tables created successfully!")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection test successful!")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
Database migration script to update AnalysisHistory table.
This script renames resume_text column to tailored_resume.
"""
from sqlalchemy import create_engine, text
from .database import DATABASE_URL
import os

def migrate_database():
    """Migrate the database to rename resume_text to tailored_resume."""
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Check if the old column exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM pragma_table_info('analysis_history') 
                WHERE name = 'resume_text'
            """))
            
            if result.fetchone()[0] > 0:
                print("🔄 Migrating database: renaming resume_text to tailored_resume...")
                
                # Rename the column
                conn.execute(text("""
                    ALTER TABLE analysis_history 
                    RENAME COLUMN resume_text TO tailored_resume
                """))
                
                conn.commit()
                print("✅ Database migration completed successfully!")
            else:
                print("ℹ️  No migration needed - tailored_resume column already exists")
                
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("💡 You may need to recreate the database if this is a development environment")

if __name__ == "__main__":
    migrate_database()

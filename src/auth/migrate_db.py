"""
Database migration script to update AnalysisHistory table.
This script renames resume_text column to tailored_resume.
"""
import logging
from sqlalchemy import create_engine, text
from .database import DATABASE_URL
import os

logger = logging.getLogger(__name__)

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
                logger.info("🔄 Migrating database: renaming resume_text to tailored_resume...")
                
                # Rename the column
                conn.execute(text("""
                    ALTER TABLE analysis_history 
                    RENAME COLUMN resume_text TO tailored_resume
                """))
                
                conn.commit()
                logger.info("✅ Database migration completed successfully!")
            else:
                logger.info("ℹ️  No migration needed - tailored_resume column already exists")
                
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}", exc_info=True)
        logger.info("💡 You may need to recreate the database if this is a development environment")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    migrate_database()

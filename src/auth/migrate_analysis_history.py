"""
Migration script to update AnalysisHistory table.
Removes 'structured_resume', 'resume_file_path', 'job_file_path' columns
and adds 'tailored_resume' column.
"""
import sqlite3
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def migrate_database():
    """Migrate the database schema."""
    # Get database path
    db_path = Path(__file__).parent.parent.parent / "resume_matcher.db"
    
    if not db_path.exists():
        logger.info("Database file not found. Creating new database with updated schema.")
        return
    
    logger.info(f"Migrating database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if the table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='analysis_history'
        """)
        
        if not cursor.fetchone():
            logger.info("Table 'analysis_history' does not exist. No migration needed.")
            conn.close()
            return
        
        # Check current columns
        cursor.execute("PRAGMA table_info(analysis_history)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        logger.info(f"Current columns: {column_names}")
        
        # Create new table with updated schema
        logger.info("Creating new table with updated schema...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tailored_resume TEXT,
                job_text TEXT,
                score FLOAT NOT NULL,
                analysis_result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on user_id
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analysis_history_new_user_id 
            ON analysis_history_new(user_id)
        """)
        
        # Copy data from old table to new table
        logger.info("Migrating data...")
        
        # Check if tailored_resume column exists in old table
        if 'tailored_resume' in column_names:
            # Already migrated, just copy data
            cursor.execute("""
                INSERT INTO analysis_history_new 
                (id, user_id, tailored_resume, job_text, score, analysis_result, created_at)
                SELECT id, user_id, tailored_resume, job_text, score, analysis_result, created_at
                FROM analysis_history
            """)
        elif 'structured_resume' in column_names:
            # Migrate from old schema (structured_resume -> tailored_resume)
            cursor.execute("""
                INSERT INTO analysis_history_new 
                (id, user_id, tailored_resume, job_text, score, analysis_result, created_at)
                SELECT id, user_id, structured_resume, job_text, score, analysis_result, created_at
                FROM analysis_history
            """)
        else:
            # Copy without tailored_resume
            cursor.execute("""
                INSERT INTO analysis_history_new 
                (id, user_id, job_text, score, analysis_result, created_at)
                SELECT id, user_id, job_text, score, analysis_result, created_at
                FROM analysis_history
            """)
        
        rows_migrated = cursor.rowcount
        logger.info(f"Migrated {rows_migrated} rows")
        
        # Drop old table
        logger.info("Dropping old table...")
        cursor.execute("DROP TABLE analysis_history")
        
        # Rename new table to old table name
        logger.info("Renaming new table...")
        cursor.execute("ALTER TABLE analysis_history_new RENAME TO analysis_history")
        
        # Commit changes
        conn.commit()
        logger.info("✅ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Migration failed: {str(e)}", exc_info=True)
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger.info("="*60)
    logger.info("  AnalysisHistory Table Migration")
    logger.info("="*60)
    logger.info("\nThis script will update the database schema:")
    logger.info("  - Remove: structured_resume, resume_file_path, job_file_path, model_used")
    logger.info("  - Add: tailored_resume")
    logger.info("\n" + "="*60 + "\n")
    
    migrate_database()


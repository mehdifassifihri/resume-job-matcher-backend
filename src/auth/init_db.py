"""
Database initialization script.
"""
import logging
from .database import engine, Base
from .models import User, AnalysisHistory, PaymentHistory

logger = logging.getLogger(__name__)

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_tables()

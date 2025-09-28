"""
Database initialization script.
"""
from .database import engine, Base
from .models import User, AnalysisHistory, PaymentHistory

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()

"""
Database models for authentication and user management.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AnalysisHistory(Base):
    """Model for storing CV analysis history."""
    __tablename__ = "analysis_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    tailored_resume = Column(Text, nullable=True)  # Tailored resume text
    job_text = Column(Text, nullable=True)
    score = Column(Float, nullable=False)
    analysis_result = Column(Text, nullable=True)  # JSON string of the full result
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PaymentHistory(Base):
    """Model for storing payment history."""
    __tablename__ = "payment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="EUR")
    payment_method = Column(String(100), nullable=True)
    payment_status = Column(String(50), default="pending")  # pending, completed, failed, refunded
    transaction_id = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

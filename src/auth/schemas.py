"""
Pydantic schemas for authentication.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema."""
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """Schema for user creation."""
    password: str

class UserLogin(BaseModel):
    """Schema for user login."""
    email: str
    password: str

class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for JWT tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    """Schema for token refresh."""
    refresh_token: str

class AnalysisHistoryResponse(BaseModel):
    """Schema for analysis history response."""
    id: int
    tailored_resume: Optional[str]  # Tailored resume text
    job_text: Optional[str]
    score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentHistoryResponse(BaseModel):
    """Schema for payment history response."""
    id: int
    amount: float
    currency: str
    payment_method: Optional[str]
    payment_status: str
    transaction_id: Optional[str]
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

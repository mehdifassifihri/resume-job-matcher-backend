"""
Routes for analysis history and payment history.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db
from .schemas import AnalysisHistoryResponse, PaymentHistoryResponse
from .dependencies import get_current_active_user
from .models import User, AnalysisHistory, PaymentHistory

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/analyses", response_model=List[AnalysisHistoryResponse])
def get_analysis_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's CV analysis history."""
    analyses = db.query(AnalysisHistory)\
        .filter(AnalysisHistory.user_id == current_user.id)\
        .order_by(AnalysisHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return analyses

@router.get("/analyses/{analysis_id}", response_model=AnalysisHistoryResponse)
def get_analysis_detail(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific analysis."""
    analysis = db.query(AnalysisHistory)\
        .filter(AnalysisHistory.id == analysis_id)\
        .filter(AnalysisHistory.user_id == current_user.id)\
        .first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return analysis

@router.get("/payments", response_model=List[PaymentHistoryResponse])
def get_payment_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's payment history."""
    payments = db.query(PaymentHistory)\
        .filter(PaymentHistory.user_id == current_user.id)\
        .order_by(PaymentHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return payments

@router.get("/payments/{payment_id}", response_model=PaymentHistoryResponse)
def get_payment_detail(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific payment."""
    payment = db.query(PaymentHistory)\
        .filter(PaymentHistory.id == payment_id)\
        .filter(PaymentHistory.user_id == current_user.id)\
        .first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment

@router.post("/analyses", response_model=AnalysisHistoryResponse)
def create_analysis_record(
    tailored_resume: Optional[str] = None,
    job_text: Optional[str] = None,
    resume_file_path: Optional[str] = None,
    job_file_path: Optional[str] = None,
    model_used: str = "gpt-4o-mini",
    score: float = 0.0,
    analysis_result: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new analysis record."""
    analysis = AnalysisHistory(
        user_id=current_user.id,
        tailored_resume=tailored_resume,
        job_text=job_text,
        resume_file_path=resume_file_path,
        job_file_path=job_file_path,
        model_used=model_used,
        score=score,
        analysis_result=analysis_result
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return analysis

@router.post("/payments", response_model=PaymentHistoryResponse)
def create_payment_record(
    amount: float,
    currency: str = "EUR",
    payment_method: Optional[str] = None,
    payment_status: str = "pending",
    transaction_id: Optional[str] = None,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new payment record."""
    payment = PaymentHistory(
        user_id=current_user.id,
        amount=amount,
        currency=currency,
        payment_method=payment_method,
        payment_status=payment_status,
        transaction_id=transaction_id,
        description=description
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    return payment

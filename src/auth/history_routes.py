"""
Routes for analysis history by user ID.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .schemas import AnalysisHistoryResponse
from .dependencies import get_current_active_user
from .models import User, AnalysisHistory

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/analyses/{user_id}", response_model=List[AnalysisHistoryResponse])
def get_all_analysis_by_user_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all analysis history by user ID."""
    try:
        print(f"Fetching analysis history for user_id: {user_id}")
        analyses = db.query(AnalysisHistory)\
            .filter(AnalysisHistory.user_id == user_id)\
            .order_by(AnalysisHistory.created_at.desc())\
            .all()
        
        print(f"Found {len(analyses)} analyses")
        return analyses
    except Exception as e:
        print(f"Error fetching analysis history: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching analysis history: {str(e)}"
        )

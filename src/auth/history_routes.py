"""
Routes for analysis history by user ID.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .schemas import AnalysisHistoryResponse
from .dependencies import get_current_active_user
from .models import User, AnalysisHistory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["history"])

@router.get("/analyses/{user_id}", response_model=List[AnalysisHistoryResponse])
def get_all_analysis_by_user_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all analysis history by user ID."""
    try:
        logger.info(f"Fetching analysis history for user_id: {user_id}")
        analyses = db.query(AnalysisHistory)\
            .filter(AnalysisHistory.user_id == user_id)\
            .order_by(AnalysisHistory.created_at.desc())\
            .all()
        
        logger.info(f"Found {len(analyses)} analyses")
        return analyses
    except Exception as e:
        logger.error(f"Error fetching analysis history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching analysis history: {str(e)}"
        )

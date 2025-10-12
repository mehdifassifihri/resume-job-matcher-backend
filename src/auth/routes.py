"""
Authentication routes for user management.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import UserCreate, UserLogin, UserResponse, Token, TokenRefresh
from .service import AuthService
from .dependencies import get_current_active_user
from .models import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        logger.info(f"Registration attempt for email: {user.email}, username: {user.username}")
        db_user = AuthService.create_user(db, user)
        logger.info(f"User created successfully with ID: {db_user.id}")
        return db_user
    except HTTPException as e:
        logger.error(f"HTTPException during registration: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT tokens."""
    try:
        logger.info(f"Login attempt for email: {user_credentials.email}")
        user = AuthService.authenticate_user(db, user_credentials.email, user_credentials.password)
        logger.info(f"User authenticated successfully: {user.username}")
        tokens = AuthService.create_tokens(user)
        return tokens
    except HTTPException as e:
        logger.error(f"HTTPException during login: {e.detail}")
        # Re-raise HTTPException as-is to preserve status code
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )

@router.post("/refresh", response_model=dict)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    try:
        tokens = AuthService.refresh_access_token(db, token_data.refresh_token)
        return tokens
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error refreshing token"
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

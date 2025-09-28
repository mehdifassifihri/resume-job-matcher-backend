"""
FastAPI routes and endpoints for the resume-job matcher.
"""
import os
import tempfile
import shutil
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

from ..core.models import MatchRequest, SuperOutput, ATSValidationResult
from ..core.config import OPENAI_API_KEY
from ..core.pipeline import run_pipeline
from ..validators.ats_validator import validate_ats_compliance, optimize_resume_for_ats
from ..auth.routes import router as auth_router
from ..auth.history_routes import router as history_router
from ..auth.dependencies import get_current_active_user
from ..auth.init_db import create_tables
from ..auth.models import User, AnalysisHistory
from sqlalchemy.orm import Session
from ..auth.database import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="AI Resume & Job Matcher — Ultra-Light API",
    description="AI-powered resume and job matching system with ATS validation and JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include authentication and history routes
app.include_router(auth_router)
app.include_router(history_router)

# Initialize database tables
create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request parameters", "errors": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."}
    )


@app.get("/health")
def health():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "ok": True,
        "status": "healthy",
        "version": "1.0.0",
        "openai_configured": bool(OPENAI_API_KEY)
    }


@app.post("/match/run", response_model=SuperOutput)
def match_run(req: MatchRequest):
    """Run the matching pipeline with text or file paths."""
    logger.info(f"Match request received - Model: {req.model}")
    
    try:
        # Check if OpenAI API key is available
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key not configured")
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        # Validate input
        if not req.resume_text and not req.resume_file_path:
            raise HTTPException(
                status_code=400,
                detail="Either resume_text or resume_file_path must be provided"
            )
        
        if not req.job_text and not req.job_file_path:
            raise HTTPException(
                status_code=400,
                detail="Either job_text or job_file_path must be provided"
            )
        
        logger.info("Starting pipeline processing")
        result = run_pipeline(
            req.resume_text,
            req.job_text,
            req.resume_file_path,
            req.job_file_path,
            req.model,
            include_ats_validation=True
        )
        
        logger.info(f"Pipeline completed successfully - Score: {result.score}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in match_run: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/match/upload", response_model=SuperOutput)
async def match_upload(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_file: UploadFile = File(..., description="Job description file (PDF, DOCX, or TXT)"),
    model: str = Form(default="gpt-4o-mini", description="OpenAI model to use")
):
    """Run the matching pipeline with uploaded files."""
    logger.info(f"File upload request received - Resume: {resume_file.filename}, Job: {job_file.filename}, Model: {model}")
    
    resume_path = None
    job_path = None
    
    try:
        # Check if OpenAI API key is available
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key not configured")
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        # Validate file types
        allowed_extensions = {'.pdf', '.docx', '.txt'}
        resume_ext = os.path.splitext(resume_file.filename)[1].lower()
        job_ext = os.path.splitext(job_file.filename)[1].lower()
        
        if resume_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported resume file type: {resume_ext}. Supported types: PDF, DOCX, TXT"
            )
        
        if job_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported job file type: {job_ext}. Supported types: PDF, DOCX, TXT"
            )
        
        # Check file sizes (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if resume_file.size and resume_file.size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"Resume file too large: {resume_file.size} bytes. Maximum size: 10MB"
            )
        
        if job_file.size and job_file.size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"Job file too large: {job_file.size} bytes. Maximum size: 10MB"
            )
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{resume_file.filename}") as resume_temp:
            shutil.copyfileobj(resume_file.file, resume_temp)
            resume_path = resume_temp.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{job_file.filename}") as job_temp:
            shutil.copyfileobj(job_file.file, job_temp)
            job_path = job_temp.name
        
        logger.info("Starting file processing")
        result = run_pipeline(None, None, resume_path, job_path, model, include_ats_validation=True)
        logger.info(f"File processing completed successfully - Score: {result.score}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in match_upload: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")
    finally:
        # Clean up temporary files
        if resume_path and os.path.exists(resume_path):
            try:
                os.unlink(resume_path)
            except Exception as e:
                logger.warning(f"Failed to delete resume temp file: {e}")
        
        if job_path and os.path.exists(job_path):
            try:
                os.unlink(job_path)
            except Exception as e:
                logger.warning(f"Failed to delete job temp file: {e}")


@app.post("/ats/validate", response_model=ATSValidationResult)
async def validate_ats(
    resume_text: str = Form(..., description="Resume text to validate"),
    job_keywords: str = Form(default="", description="Comma-separated job keywords"),
    current_user: User = Depends(get_current_active_user)
):
    """Validate resume for ATS compatibility."""
    logger.info("ATS validation request received")
    
    try:
        # Validate input
        if not resume_text or not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Resume text cannot be empty"
            )
        
        if len(resume_text) > 50000:  # 50KB limit
            raise HTTPException(
                status_code=400,
                detail="Resume text too long. Maximum length: 50,000 characters"
            )
        
        keywords = [k.strip() for k in job_keywords.split(",") if k.strip()] if job_keywords else []
        logger.info(f"Validating ATS compliance with {len(keywords)} keywords")
        
        result = validate_ats_compliance(resume_text, keywords)
        
        logger.info(f"ATS validation completed - Score: {result.score}, Level: {result.compliance_level.value}")
        return ATSValidationResult(
            compliance_level=result.compliance_level.value,
            score=result.score,
            issues=result.issues,
            recommendations=result.recommendations,
            keyword_density=result.keyword_density,
            structure_score=result.structure_score,
            formatting_score=result.formatting_score
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in validate_ats: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error validating ATS compliance: {str(e)}")


@app.post("/ats/optimize")
async def optimize_ats(
    resume_text: str = Form(..., description="Resume text to optimize"),
    job_keywords: str = Form(..., description="Comma-separated job keywords"),
    current_user: User = Depends(get_current_active_user)
):
    """Optimize resume for ATS compatibility."""
    logger.info("ATS optimization request received")
    
    try:
        # Validate input
        if not resume_text or not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Resume text cannot be empty"
            )
        
        if not job_keywords or not job_keywords.strip():
            raise HTTPException(
                status_code=400,
                detail="Job keywords cannot be empty"
            )
        
        if len(resume_text) > 50000:  # 50KB limit
            raise HTTPException(
                status_code=400,
                detail="Resume text too long. Maximum length: 50,000 characters"
            )
        
        keywords = [k.strip() for k in job_keywords.split(",") if k.strip()]
        if not keywords:
            raise HTTPException(
                status_code=400,
                detail="No valid keywords provided"
            )
        
        logger.info(f"Optimizing resume for ATS with {len(keywords)} keywords")
        optimized_resume = optimize_resume_for_ats(resume_text, keywords)
        
        logger.info("ATS optimization completed successfully")
        return {
            "optimized_resume": optimized_resume,
            "original_length": len(resume_text),
            "optimized_length": len(optimized_resume),
            "keywords_integrated": len(keywords)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in optimize_ats: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error optimizing for ATS: {str(e)}")


"""
FastAPI routes and endpoints for the resume-job matcher.
"""
import os
import tempfile
import shutil
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

from ..core.models import SuperOutput
from ..core.config import OPENAI_API_KEY
from ..core.pipeline import run_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="AI Resume & Job Matcher — Ultra-Light API",
    description="AI-powered resume and job matching system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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




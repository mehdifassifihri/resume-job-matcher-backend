"""
FastAPI routes and endpoints for the resume-job matcher - Ultra minimal version.
Only text-based matching, no file uploads.
"""
import os
import logging
from fastapi import FastAPI, HTTPException, Request, Form
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
    title="AI Resume & Job Matcher — Ultra Minimal API",
    description="AI-powered resume and job matching system (text-only)",
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
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "openai_configured": bool(OPENAI_API_KEY),
        "version": "1.0.0",
        "features": ["text_matching"]
    }

@app.post("/match/run", response_model=SuperOutput)
async def match_run(
    resume_text: str = Form(..., description="Resume text content"),
    job_description: str = Form(..., description="Job description text content"),
    model: str = Form(default="gpt-4o-mini", description="OpenAI model to use")
):
    """Run the matching pipeline with text inputs."""
    logger.info(f"Text matching request received - Model: {model}")
    
    try:
        # Check if OpenAI API key is available
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key not configured")
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        logger.info("Starting text processing")
        result = run_pipeline(resume_text, job_description, None, None, model, include_ats_validation=True)
        logger.info(f"Text processing completed successfully - Score: {result.score}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in match_run: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Resume & Job Matcher API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "match": "/match/run",
            "docs": "/docs"
        },
        "note": "This is a minimal version supporting text-based matching only"
    }

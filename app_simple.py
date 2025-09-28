"""
Ultra-simplified entry point for Railway deployment (testing version).
Minimal dependencies to avoid import issues.
"""
import os
import sys
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume & Job Matcher — Simple Test",
    description="Minimal version for testing Railway deployment",
    version="1.0.0-simple",
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

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "AI Resume & Job Matcher API",
        "version": "1.0.0-simple",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check endpoint."""
    try:
        logger.info("Health check requested")
        
        # Check environment variables
        openai_key = os.getenv("OPENAI_API_KEY")
        
        return {
            "ok": True,
            "status": "healthy",
            "version": "1.0.0-simple",
            "openai_configured": bool(openai_key),
            "mode": "simple-testing",
            "environment": os.getenv("RAILWAY_ENVIRONMENT", "local")
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "status": "error",
                "error": str(e),
                "version": "1.0.0-simple"
            }
        )

@app.get("/test")
def test():
    """Simple test endpoint."""
    return {
        "message": "Test endpoint working!",
        "timestamp": "2024-01-01T00:00:00Z",
        "status": "success"
    }

@app.post("/match/simple")
def match_simple(request: dict):
    """Simple matching endpoint without complex dependencies."""
    try:
        # Basic validation
        if not request.get("resume_text") or not request.get("job_text"):
            raise HTTPException(
                status_code=400,
                detail="Both resume_text and job_text are required"
            )
        
        # Simple response (without AI processing for now)
        return {
            "message": "Simple matching endpoint",
            "status": "success",
            "note": "AI processing not yet implemented in simple version",
            "input_length": {
                "resume": len(request.get("resume_text", "")),
                "job": len(request.get("job_text", ""))
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in simple match: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

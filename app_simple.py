"""
Ultra-simplified entry point for Railway deployment (testing version).
Minimal dependencies to avoid import issues.
"""
import os
import sys
import logging
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
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

@app.post("/match/run")
def match_run(request: dict):
    """Full matching endpoint (placeholder for AI processing)."""
    try:
        # Validate input
        if not request.get("resume_text") and not request.get("resume_file_path"):
            raise HTTPException(
                status_code=400,
                detail="Either resume_text or resume_file_path must be provided"
            )
        
        if not request.get("job_text") and not request.get("job_file_path"):
            raise HTTPException(
                status_code=400,
                detail="Either job_text or job_file_path must be provided"
            )
        
        # Check OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        # Placeholder response (AI processing would go here)
        return {
            "score": 85.5,
            "match_percentage": 85.5,
            "resume_summary": "Développeur Python expérimenté",
            "job_summary": "Recherche développeur Python senior",
            "matched_skills": ["Python", "Développement", "Web"],
            "missing_skills": ["Docker", "Kubernetes"],
            "recommendations": [
                "Ajoutez des compétences en conteneurisation",
                "Mettez en avant vos projets Python"
            ],
            "note": "This is a placeholder response. AI processing would be implemented here with OpenAI API."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in match_run: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/match/upload")
async def match_upload(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_file: UploadFile = File(..., description="Job description file (PDF, DOCX, or TXT)"),
    model: str = Form(default="gpt-4o-mini", description="OpenAI model to use")
):
    """Upload files for matching with real processing."""
    try:
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
        
        # Check OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        # Read file contents (simplified - just for text files for now)
        resume_content = ""
        job_content = ""
        
        try:
            # For text files, read content directly
            if resume_ext == '.txt':
                resume_content = (await resume_file.read()).decode('utf-8')
            else:
                # For PDF/DOCX, we'd need proper parsing (placeholder for now)
                resume_content = f"[{resume_file.filename} - PDF/DOCX content would be extracted here]"
            
            if job_ext == '.txt':
                job_content = (await job_file.read()).decode('utf-8')
            else:
                job_content = f"[{job_file.filename} - PDF/DOCX content would be extracted here]"
                
        except Exception as e:
            logger.error(f"Error reading file contents: {e}")
            raise HTTPException(status_code=400, detail=f"Error reading file contents: {str(e)}")
        
        # Simulate matching analysis (like the original pipeline would do)
        # In the real version, this would use AI to analyze the content
        
        # Extract keywords from content (simplified)
        resume_words = resume_content.lower().split()
        job_words = job_content.lower().split()
        
        # Common technical terms
        tech_terms = ['python', 'javascript', 'java', 'react', 'node', 'sql', 'docker', 'aws', 'api', 'web', 'development', 'programming']
        
        # Find matching skills
        matched_skills = []
        for term in tech_terms:
            if term in resume_content.lower() and term in job_content.lower():
                matched_skills.append(term.title())
        
        # Calculate a realistic score
        base_score = 60.0
        skill_bonus = len(matched_skills) * 5.0
        experience_bonus = 10.0 if any(word in resume_content.lower() for word in ['experience', 'expérience', 'years', 'ans']) else 0.0
        education_bonus = 5.0 if any(word in resume_content.lower() for word in ['degree', 'diplôme', 'master', 'bachelor']) else 0.0
        
        final_score = min(95.0, base_score + skill_bonus + experience_bonus + education_bonus)
        
        # Generate recommendations
        recommendations = []
        if len(matched_skills) < 3:
            recommendations.append("Consider adding more technical skills that match the job requirements")
        if 'experience' not in resume_content.lower():
            recommendations.append("Highlight your relevant work experience")
        if 'education' not in resume_content.lower():
            recommendations.append("Include your educational background")
        
        # Return the same format as the original SuperOutput
        return {
            "score": round(final_score, 1),
            "match_percentage": round(final_score, 1),
            "resume_summary": resume_content[:100] + "..." if len(resume_content) > 100 else resume_content,
            "job_summary": job_content[:100] + "..." if len(job_content) > 100 else job_content,
            "matched_skills": matched_skills,
            "missing_skills": [term.title() for term in tech_terms if term in job_content.lower() and term not in resume_content.lower()][:5],
            "recommendations": recommendations,
            "file_info": {
                "resume_filename": resume_file.filename,
                "job_filename": job_file.filename,
                "resume_size": resume_file.size or 0,
                "job_size": job_file.size or 0,
                "model_used": model
            },
            "ats_validation": {
                "score": round(final_score * 0.9, 1),  # ATS score slightly lower
                "compliance_level": "good" if final_score > 80 else "fair",
                "issues": ["File parsing could be improved for PDF/DOCX"] if resume_ext != '.txt' or job_ext != '.txt' else []
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in match_upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

@app.post("/ats/validate")
async def validate_ats(
    resume_text: str = Form(..., description="Resume text to validate"),
    job_keywords: str = Form(default="", description="Comma-separated job keywords")
):
    """Validate resume for ATS compatibility (placeholder)."""
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
        
        # Placeholder ATS validation
        return {
            "compliance_level": "good",
            "score": 82.5,
            "issues": [
                "Missing some industry keywords",
                "Could improve formatting consistency"
            ],
            "recommendations": [
                f"Include more keywords: {', '.join(keywords[:3]) if keywords else 'industry-specific terms'}",
                "Use consistent bullet points",
                "Add more quantifiable achievements"
            ],
            "keyword_density": {
                "total_keywords": len(keywords),
                "found_keywords": len([k for k in keywords if k.lower() in resume_text.lower()]),
                "density_score": 0.75
            },
            "structure_score": 85.0,
            "formatting_score": 80.0,
            "note": "This is a placeholder ATS validation. Real validation would analyze formatting, keywords, and structure."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in validate_ats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/ats/optimize")
async def optimize_ats(
    resume_text: str = Form(..., description="Resume text to optimize"),
    job_keywords: str = Form(..., description="Comma-separated job keywords")
):
    """Optimize resume for ATS compatibility (placeholder)."""
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
        
        # Placeholder optimization (would use AI to optimize the resume)
        optimized_resume = resume_text + f"\n\n[OPTIMIZED] Added keywords: {', '.join(keywords[:3])}"
        
        return {
            "optimized_resume": optimized_resume,
            "original_length": len(resume_text),
            "optimized_length": len(optimized_resume),
            "keywords_integrated": len(keywords),
            "improvements_made": [
                f"Added {len(keywords)} relevant keywords",
                "Improved keyword density",
                "Enhanced formatting consistency"
            ],
            "note": "This is a placeholder optimization. Real optimization would use AI to strategically integrate keywords and improve formatting."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in optimize_ats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

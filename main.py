"""
Main entry point for the AI Resume & Job Matcher application.
Railway deployment entry point.
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port)

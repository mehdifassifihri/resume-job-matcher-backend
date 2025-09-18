"""
Main entry point for the AI Resume & Job Matcher application.
"""
import uvicorn
from api.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


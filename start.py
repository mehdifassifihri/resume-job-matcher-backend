"""
Alternative entry point for Railway deployment.
"""
import os
import sys
import uvicorn

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the simple app
from app_simple import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

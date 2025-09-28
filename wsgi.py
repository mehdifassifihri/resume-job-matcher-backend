"""
WSGI entry point for Railway deployment.
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the simple app
from app_simple import app

# This is what Railway will use if it tries to use WSGI
application = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

"""
Main entry point for Railway deployment.
This file ensures Railway uses the correct app.
"""
import os
import sys
import uvicorn

# Import the simple app
from app_simple import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

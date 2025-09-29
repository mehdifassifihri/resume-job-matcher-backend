"""
Main entry point for the AI Resume & Job Matcher application - Basic version.
"""
import os
import uvicorn
from .api.api_basic import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

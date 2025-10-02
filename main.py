"""
Main entry point for the AI Resume & Job Matcher application.
Railway deployment entry point.
"""
import os
import sys
import uvicorn

# Ajouter le répertoire src au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api.api import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

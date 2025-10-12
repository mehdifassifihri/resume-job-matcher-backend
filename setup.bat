@echo off
REM ############################################################################
REM AI Resume & Job Matcher - Setup Script (Windows)
REM This script automates the installation process
REM ############################################################################

echo ==============================================
echo   AI Resume ^& Job Matcher - Installation
echo ==============================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv" (
    echo [WARNING] Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully
echo.

REM Create .env file from template
echo Configuring environment...
if exist ".env" (
    echo [WARNING] .env file already exists. Skipping creation.
    echo If you need a fresh template, delete .env and run this script again.
) else (
    copy env.example .env >nul
    echo [OK] .env file created from template
)
echo.

REM Initialize database
echo Initializing database...
python -c "from src.auth.init_db import create_tables; create_tables()" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Database initialization skipped (will be created on first run)
) else (
    echo [OK] Database initialized
)
echo.

echo ==============================================
echo [SUCCESS] Installation completed successfully!
echo ==============================================
echo.
echo IMPORTANT: Configure your environment
echo.
echo 1. Edit the .env file and add your OpenAI API key:
echo    notepad .env
echo.
echo    Required settings:
echo    - OPENAI_API_KEY=your-api-key-here
echo    - JWT_SECRET_KEY=your-secure-secret-key
echo.
echo 2. Get your OpenAI API key:
echo    - Visit: https://platform.openai.com
echo    - Create an account or login
echo    - Navigate to API Keys section
echo    - Create a new API key
echo.
echo 3. Start the application:
echo    python src\main.py
echo.
echo 4. Access the API:
echo    - API: http://localhost:8000
echo    - Documentation: http://localhost:8000/docs
echo    - Alternative docs: http://localhost:8000/redoc
echo.
echo ==============================================
echo Need help? Check the documentation:
echo    - README.md - Overview and quick start
echo    - docs\INSTALLATION.md - Detailed setup
echo    - docs\API.md - API reference
echo ==============================================
echo.
echo [WARNING] REMINDER: OpenAI API usage incurs costs
echo    Estimated: $0.02-$0.20 per analysis
echo    Make sure you have credits in your OpenAI account
echo.
echo Happy coding!
echo.
pause


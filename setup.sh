#!/bin/bash

###############################################################################
# AI Resume & Job Matcher - Setup Script (Linux/Mac)
# This script automates the installation process
###############################################################################

echo "=============================================="
echo "  AI Resume & Job Matcher - Installation"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
echo ""

# Check Python version (minimum 3.8)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}❌ Python 3.8 or higher is required. You have $PYTHON_VERSION${NC}"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Create .env file from template
echo "⚙️  Configuring environment..."
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists. Skipping creation.${NC}"
    echo -e "${YELLOW}   If you need a fresh template, delete .env and run this script again.${NC}"
else
    cp env.example .env
    echo -e "${GREEN}✓ .env file created from template${NC}"
fi
echo ""

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from src.auth.init_db import create_tables; create_tables()" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${YELLOW}⚠️  Database initialization skipped (will be created on first run)${NC}"
fi
echo ""

echo "=============================================="
echo -e "${GREEN}✅ Installation completed successfully!${NC}"
echo "=============================================="
echo ""
echo "📋 IMPORTANT: Configure your environment"
echo ""
echo "1️⃣  Edit the .env file and add your OpenAI API key:"
echo "   ${YELLOW}nano .env${NC}"
echo ""
echo "   Required settings:"
echo "   - OPENAI_API_KEY=your-api-key-here"
echo "   - JWT_SECRET_KEY=your-secure-secret-key"
echo ""
echo "2️⃣  Get your OpenAI API key:"
echo "   - Visit: https://platform.openai.com"
echo "   - Create an account or login"
echo "   - Navigate to API Keys section"
echo "   - Create a new API key"
echo ""
echo "3️⃣  Start the application:"
echo "   ${GREEN}python3 src/main.py${NC}"
echo ""
echo "4️⃣  Access the API:"
echo "   - API: http://localhost:8000"
echo "   - Documentation: http://localhost:8000/docs"
echo "   - Alternative docs: http://localhost:8000/redoc"
echo ""
echo "=============================================="
echo "📚 Need help? Check the documentation:"
echo "   - README.md - Overview and quick start"
echo "   - docs/INSTALLATION.md - Detailed setup"
echo "   - docs/API.md - API reference"
echo "=============================================="
echo ""
echo -e "${YELLOW}⚠️  REMINDER: OpenAI API usage incurs costs${NC}"
echo "   Estimated: $0.02-$0.20 per analysis"
echo "   Make sure you have credits in your OpenAI account"
echo ""
echo "Happy coding! 🚀"
echo ""


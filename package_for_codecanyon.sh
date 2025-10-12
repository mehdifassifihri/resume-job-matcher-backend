#!/bin/bash

###############################################################################
# CodeCanyon Package Creator
# This script creates a clean package ready for CodeCanyon submission
###############################################################################

echo "=============================================="
echo "  CodeCanyon Package Creator"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Package configuration
PACKAGE_NAME="ai-resume-matcher-codecanyon"
PACKAGE_DIR="codecanyon_package"
VERSION="1.0.0"

# Step 1: Clean up any existing package
echo -e "${BLUE}📦 Step 1: Cleaning up existing package...${NC}"
if [ -d "$PACKAGE_DIR" ]; then
    rm -rf "$PACKAGE_DIR"
    echo -e "${GREEN}✓ Removed existing package directory${NC}"
fi

if [ -f "${PACKAGE_NAME}.zip" ]; then
    rm "${PACKAGE_NAME}.zip"
    echo -e "${GREEN}✓ Removed existing package ZIP${NC}"
fi
echo ""

# Step 2: Create package directory
echo -e "${BLUE}📁 Step 2: Creating package directory...${NC}"
mkdir -p "$PACKAGE_DIR"
echo -e "${GREEN}✓ Package directory created${NC}"
echo ""

# Step 3: Copy source files
echo -e "${BLUE}📋 Step 3: Copying source files...${NC}"

# Copy main files
cp -r src "$PACKAGE_DIR/"
cp -r docs "$PACKAGE_DIR/"
cp requirements.txt "$PACKAGE_DIR/"
cp env.example "$PACKAGE_DIR/"
cp main.py "$PACKAGE_DIR/"
cp Dockerfile "$PACKAGE_DIR/"
cp Procfile "$PACKAGE_DIR/"
cp railway.json "$PACKAGE_DIR/"
cp runtime.txt "$PACKAGE_DIR/"
cp postman_collection.json "$PACKAGE_DIR/"

# Copy new files
cp LICENSE.txt "$PACKAGE_DIR/"
cp CHANGELOG.txt "$PACKAGE_DIR/"
cp setup.sh "$PACKAGE_DIR/"
cp setup.bat "$PACKAGE_DIR/"
chmod +x "$PACKAGE_DIR/setup.sh"

# Copy README and documentation
cp README.md "$PACKAGE_DIR/"

echo -e "${GREEN}✓ Source files copied${NC}"
echo ""

# Step 4: Clean up development files from package
echo -e "${BLUE}🧹 Step 4: Removing development files...${NC}"

# Remove __pycache__ directories
find "$PACKAGE_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo -e "${GREEN}✓ Removed __pycache__ directories${NC}"

# Remove .pyc files
find "$PACKAGE_DIR" -type f -name "*.pyc" -delete 2>/dev/null
echo -e "${GREEN}✓ Removed .pyc files${NC}"

# Remove .DS_Store files
find "$PACKAGE_DIR" -type f -name ".DS_Store" -delete 2>/dev/null
echo -e "${GREEN}✓ Removed .DS_Store files${NC}"

# Remove test files if they exist in the package
find "$PACKAGE_DIR" -type f -name "test_*.py" -delete 2>/dev/null
echo -e "${GREEN}✓ Removed test files${NC}"

echo ""

# Step 5: Create README for CodeCanyon reviewers
echo -e "${BLUE}📝 Step 5: Creating reviewer notes...${NC}"
cat > "$PACKAGE_DIR/README_FOR_REVIEWERS.txt" << 'EOF'
CODECANYON REVIEWER NOTES
=========================

Thank you for reviewing this submission.

INSTALLATION & TESTING:
----------------------

Quick Start (5 minutes):
1. Run setup script: ./setup.sh (Mac/Linux) or setup.bat (Windows)
2. Edit .env file and add OpenAI API key
3. Run: python src/main.py
4. Visit: http://localhost:8000/docs for interactive API documentation

Requirements:
- Python 3.8 or higher (Python 3.11+ recommended)
- OpenAI API key (get from https://platform.openai.com)
- Minimum $5 credit in OpenAI account for testing

THIRD-PARTY DEPENDENCIES:
-------------------------
This product requires an OpenAI API key (external, paid service).
- Costs are clearly documented in README.md
- Estimated: $0.02-$0.05 per analysis with default model
- Users need to create their own OpenAI account

TESTING ENDPOINTS:
------------------
1. Health Check: GET http://localhost:8000/docs
2. Register User: POST /auth/register
3. Login: POST /auth/login
4. Match Resume: POST /match/upload (requires authentication)

Complete testing guide available in docs/API.md

DOCUMENTATION:
--------------
- README.md - Main documentation with setup
- docs/ - 8 detailed documentation files
- postman_collection.json - API testing collection
- Interactive docs at /docs endpoint

CODE QUALITY:
-------------
- Production-ready FastAPI application
- JWT authentication implemented
- Comprehensive error handling
- Clean, modular architecture
- Logging throughout
- Security best practices

SUPPORT:
--------
6 months of support included through CodeCanyon messaging system.

Thank you!
EOF

echo -e "${GREEN}✓ Reviewer notes created${NC}"
echo ""

# Step 6: Create installation guide for customers
echo -e "${BLUE}📖 Step 6: Creating quick start guide...${NC}"
cat > "$PACKAGE_DIR/QUICK_START.txt" << 'EOF'
AI RESUME & JOB MATCHER - QUICK START GUIDE
============================================

Thank you for your purchase!

STEP 1: RUN SETUP SCRIPT
-------------------------
Mac/Linux:  ./setup.sh
Windows:    setup.bat

This will:
- Create virtual environment
- Install dependencies
- Create .env configuration file

STEP 2: GET OPENAI API KEY
---------------------------
1. Visit: https://platform.openai.com
2. Create account/sign in
3. Go to API Keys section
4. Create new API key
5. Add minimum $5 credits

STEP 3: CONFIGURE
-----------------
Edit .env file:
- OPENAI_API_KEY=your-api-key-here
- JWT_SECRET_KEY=your-secure-secret-key

STEP 4: START APPLICATION
--------------------------
python src/main.py

Application will start at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

NEED HELP?
----------
- Check README.md for detailed documentation
- Visit docs/ folder for guides
- Use CodeCanyon support tab for assistance

Happy coding!
EOF

echo -e "${GREEN}✓ Quick start guide created${NC}"
echo ""

# Step 7: Create file structure document
echo -e "${BLUE}📊 Step 7: Creating file structure document...${NC}"
cat > "$PACKAGE_DIR/FILE_STRUCTURE.txt" << 'EOF'
AI RESUME & JOB MATCHER - FILE STRUCTURE
=========================================

ROOT LEVEL FILES:
-----------------
├── README.md                   # Main documentation
├── QUICK_START.txt            # Quick installation guide
├── LICENSE.txt                # Commercial license terms
├── CHANGELOG.txt              # Version history
├── requirements.txt           # Python dependencies
├── env.example                # Environment variables template
├── setup.sh                   # Setup script (Mac/Linux)
├── setup.bat                  # Setup script (Windows)
├── main.py                    # Application entry point
├── Dockerfile                 # Docker configuration
├── Procfile                   # Deployment configuration
├── railway.json               # Railway deployment config
├── runtime.txt                # Python version specification
├── postman_collection.json    # API testing collection
└── FILE_STRUCTURE.txt         # This file

SOURCE CODE (src/):
-------------------
├── src/
│   ├── main.py                # Main FastAPI application
│   ├── api/
│   │   └── api.py             # API routes
│   ├── auth/
│   │   ├── routes.py          # Authentication endpoints
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── service.py         # Auth business logic
│   │   ├── jwt_handler.py     # JWT token handling
│   │   ├── database.py        # Database configuration
│   │   ├── dependencies.py    # Auth dependencies
│   │   ├── history_routes.py  # History endpoints
│   │   └── init_db.py         # Database initialization
│   ├── core/
│   │   ├── config.py          # Configuration & constants
│   │   ├── models.py          # Core data models
│   │   ├── pipeline.py        # Main processing pipeline
│   │   ├── matcher.py         # Matching algorithm
│   │   └── tailor.py          # Resume tailoring
│   ├── parsers/
│   │   └── parsers.py         # File parsing (PDF, DOCX, TXT)
│   ├── utils/
│   │   └── utils.py           # Utility functions
│   └── validators/
│       └── ats_validator.py   # ATS validation logic

DOCUMENTATION (docs/):
----------------------
├── docs/
│   ├── API.md                 # Complete API reference
│   ├── AUTH_API.md            # Authentication guide
│   ├── CV_ANALYSIS_API.md     # Analysis guide
│   ├── API_QUICK_REFERENCE.md # Quick reference
│   ├── INSTALLATION.md        # Installation guide
│   ├── FEATURES.md            # Feature documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── RAILWAY_DEPLOYMENT.md  # Railway-specific guide
│   └── FAQ.md                 # Frequently asked questions

KEY DIRECTORIES:
----------------
- src/auth/        # Authentication & user management
- src/core/        # Core business logic
- src/parsers/     # File parsing functionality
- src/utils/       # Utility functions
- src/validators/  # Validation logic
- docs/            # Documentation

AFTER SETUP:
------------
- venv/            # Virtual environment (created by setup)
- .env             # Environment config (created from env.example)
- resume_matcher.db # SQLite database (created on first run)

EOF

echo -e "${GREEN}✓ File structure document created${NC}"
echo ""

# Step 8: Verify package contents
echo -e "${BLUE}🔍 Step 8: Verifying package contents...${NC}"

REQUIRED_FILES=(
    "README.md"
    "LICENSE.txt"
    "CHANGELOG.txt"
    "requirements.txt"
    "env.example"
    "setup.sh"
    "setup.bat"
    "main.py"
    "src/main.py"
    "src/api/api.py"
    "docs/API.md"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PACKAGE_DIR/$file" ] && [ ! -d "$PACKAGE_DIR/$file" ]; then
        echo -e "${RED}✗ Missing: $file${NC}"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -eq 0 ]; then
    echo -e "${GREEN}✓ All required files present${NC}"
else
    echo -e "${RED}✗ Missing $MISSING_FILES required file(s)${NC}"
    exit 1
fi
echo ""

# Step 9: Create ZIP package
echo -e "${BLUE}📦 Step 9: Creating ZIP package...${NC}"
cd "$PACKAGE_DIR"
zip -r "../${PACKAGE_NAME}.zip" . -x "*.DS_Store" -x "__pycache__/*" -x "*.pyc" > /dev/null 2>&1
cd ..
echo -e "${GREEN}✓ ZIP package created: ${PACKAGE_NAME}.zip${NC}"
echo ""

# Step 10: Calculate package size
echo -e "${BLUE}📊 Step 10: Package information...${NC}"
PACKAGE_SIZE=$(du -sh "${PACKAGE_NAME}.zip" | cut -f1)
FILE_COUNT=$(find "$PACKAGE_DIR" -type f | wc -l | tr -d ' ')
echo -e "${GREEN}✓ Package size: $PACKAGE_SIZE${NC}"
echo -e "${GREEN}✓ File count: $FILE_COUNT files${NC}"
echo ""

# Summary
echo "=============================================="
echo -e "${GREEN}✅ Package created successfully!${NC}"
echo "=============================================="
echo ""
echo -e "${BLUE}Package Details:${NC}"
echo "  • Name: ${PACKAGE_NAME}.zip"
echo "  • Version: ${VERSION}"
echo "  • Size: $PACKAGE_SIZE"
echo "  • Files: $FILE_COUNT"
echo ""
echo -e "${BLUE}Package Location:${NC}"
echo "  • ZIP: ./${PACKAGE_NAME}.zip"
echo "  • Directory: ./${PACKAGE_DIR}/"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Test the package by extracting and running setup"
echo "  2. Review README_FOR_REVIEWERS.txt"
echo "  3. Upload ${PACKAGE_NAME}.zip to CodeCanyon"
echo ""
echo -e "${YELLOW}Before Upload Checklist:${NC}"
echo "  ☐ Tested installation on clean system"
echo "  ☐ Verified all API endpoints work"
echo "  ☐ Checked documentation is complete"
echo "  ☐ Ensured no sensitive data in files"
echo "  ☐ Validated LICENSE.txt terms"
echo ""
echo "Good luck with your submission! 🚀"
echo ""


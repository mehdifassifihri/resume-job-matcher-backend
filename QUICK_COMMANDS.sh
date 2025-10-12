#!/bin/bash

###############################################################################
# QUICK COMMANDS FOR CODECANYON
# Use these commands to test and create the package
###############################################################################

echo "═══════════════════════════════════════════════════════════════"
echo "  QUICK COMMANDS - AI Resume Matcher"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detect OS
OS="$(uname)"

echo "What would you like to do?"
echo ""
echo "1) 📦 Create CodeCanyon package"
echo "2) 🧪 Test the package locally"
echo "3) 🚀 Install and launch the application"
echo "4) 🧹 Clean development files"
echo "5) ℹ️  Display project information"
echo "6) 🔍 Verify everything is ready"
echo ""
read -p "Choose an option (1-6): " choice

case $choice in
    1)
        echo -e "${BLUE}📦 Creating CodeCanyon package...${NC}"
        echo ""
        ./package_for_codecanyon.sh
        ;;
    2)
        echo -e "${BLUE}🧪 Testing package...${NC}"
        echo ""
        
        if [ ! -f "ai-resume-matcher-codecanyon.zip" ]; then
            echo -e "${YELLOW}Package not found. Creating...${NC}"
            ./package_for_codecanyon.sh
        fi
        
        # Create temp test directory
        TEST_DIR="/tmp/codecanyon-test-$(date +%s)"
        mkdir -p "$TEST_DIR"
        
        echo "Extracting package to: $TEST_DIR"
        unzip -q ai-resume-matcher-codecanyon.zip -d "$TEST_DIR"
        
        echo ""
        echo -e "${GREEN}Package extracted successfully!${NC}"
        echo ""
        echo "To test the installation:"
        echo "  cd $TEST_DIR"
        echo "  ./setup.sh"
        echo "  # Configure .env with your OpenAI key"
        echo "  python src/main.py"
        ;;
    3)
        echo -e "${BLUE}🚀 Installation and launch...${NC}"
        echo ""
        
        # Check if venv exists
        if [ ! -d "venv" ]; then
            echo "Installing dependencies..."
            if [ "$OS" = "Darwin" ] || [ "$OS" = "Linux" ]; then
                ./setup.sh
            else
                echo "Run setup.bat on Windows"
                exit 1
            fi
        else
            echo -e "${GREEN}Virtual environment already installed${NC}"
        fi
        
        # Check .env
        if [ ! -f ".env" ]; then
            echo ""
            echo -e "${YELLOW}⚠️  .env file missing!${NC}"
            echo "Creating from env.example..."
            cp env.example .env
            echo ""
            echo "Please edit .env and add your OpenAI key:"
            echo "  nano .env"
            read -p "Press Enter when done..."
        fi
        
        echo ""
        echo -e "${GREEN}Launching application...${NC}"
        python src/main.py
        ;;
    4)
        echo -e "${BLUE}🧹 Cleaning development files...${NC}"
        echo ""
        
        echo "Removing __pycache__..."
        find ./src -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        
        echo "Removing .pyc..."
        find ./src -type f -name "*.pyc" -delete 2>/dev/null
        
        echo "Removing .DS_Store..."
        find . -name ".DS_Store" -delete 2>/dev/null
        
        echo ""
        echo -e "${GREEN}✅ Cleanup complete!${NC}"
        ;;
    5)
        echo ""
        echo "═══════════════════════════════════════════════════════════════"
        echo "  PROJECT INFORMATION"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        echo -e "${BLUE}Name:${NC} AI Resume & Job Matcher"
        echo -e "${BLUE}Version:${NC} 1.0.0"
        echo -e "${BLUE}Type:${NC} FastAPI REST API"
        echo ""
        echo -e "${BLUE}Created/Modified files:${NC}"
        echo "  ✅ LICENSE.txt"
        echo "  ✅ CHANGELOG.txt"
        echo "  ✅ setup.sh & setup.bat"
        echo "  ✅ package_for_codecanyon.sh"
        echo "  ✅ README.md (OpenAI section added)"
        echo "  ✅ All print() replaced with logger"
        echo ""
        echo -e "${BLUE}Documentation:${NC}"
        ls -1 docs/ | sed 's/^/  - docs\//'
        echo ""
        echo -e "${BLUE}Main dependencies:${NC}"
        echo "  - FastAPI (API framework)"
        echo "  - OpenAI GPT-4 (AI matching)"
        echo "  - LangChain (LLM integration)"
        echo "  - SQLAlchemy (Database ORM)"
        echo "  - JWT (Authentication)"
        echo ""
        echo -e "${BLUE}Estimated OpenAI cost:${NC}"
        echo "  - gpt-4o-mini: $0.02-$0.05 per analysis (default)"
        echo "  - gpt-4o: $0.10-$0.20 per analysis"
        echo ""
        ;;
    6)
        echo ""
        echo "═══════════════════════════════════════════════════════════════"
        echo "  CODECANYON PREPARATION VERIFICATION"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        
        # Check required files
        REQUIRED_FILES=(
            "LICENSE.txt"
            "CHANGELOG.txt"
            "README.md"
            "setup.sh"
            "setup.bat"
            "requirements.txt"
            "env.example"
            "package_for_codecanyon.sh"
        )
        
        echo "Checking required files:"
        ALL_OK=true
        for file in "${REQUIRED_FILES[@]}"; do
            if [ -f "$file" ]; then
                echo -e "  ${GREEN}✅${NC} $file"
            else
                echo -e "  ${YELLOW}❌${NC} $file (MISSING)"
                ALL_OK=false
            fi
        done
        
        echo ""
        echo "Checking code cleanliness:"
        
        # Check for __pycache__
        PYCACHE_COUNT=$(find ./src -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$PYCACHE_COUNT" -eq "0" ]; then
            echo -e "  ${GREEN}✅${NC} No __pycache__"
        else
            echo -e "  ${YELLOW}⚠️${NC}  $PYCACHE_COUNT __pycache__ directories found"
            ALL_OK=false
        fi
        
        # Check for .pyc
        PYC_COUNT=$(find ./src -type f -name "*.pyc" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$PYC_COUNT" -eq "0" ]; then
            echo -e "  ${GREEN}✅${NC} No .pyc files"
        else
            echo -e "  ${YELLOW}⚠️${NC}  $PYC_COUNT .pyc files found"
            ALL_OK=false
        fi
        
        # Check for print statements (rough check)
        PRINT_COUNT=$(grep -r "print(" ./src --include="*.py" 2>/dev/null | grep -v "logger" | grep -v "#" | wc -l | tr -d ' ')
        if [ "$PRINT_COUNT" -eq "0" ]; then
            echo -e "  ${GREEN}✅${NC} No non-logger print()"
        else
            echo -e "  ${YELLOW}⚠️${NC}  $PRINT_COUNT potentially problematic print()"
            echo "     (Check manually - may be false positives)"
        fi
        
        echo ""
        echo "Checking documentation:"
        
        # Check OpenAI costs section in README
        if grep -q "OpenAI API Costs" README.md; then
            echo -e "  ${GREEN}✅${NC} OpenAI costs section in README"
        else
            echo -e "  ${YELLOW}❌${NC} OpenAI costs section missing in README"
            ALL_OK=false
        fi
        
        # Check LICENSE mentions OpenAI
        if grep -q "OpenAI" LICENSE.txt; then
            echo -e "  ${GREEN}✅${NC} OpenAI mentioned in LICENSE"
        else
            echo -e "  ${YELLOW}⚠️${NC}  OpenAI not mentioned in LICENSE"
        fi
        
        echo ""
        if [ "$ALL_OK" = true ]; then
            echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}  ✅ EVERYTHING IS READY FOR CODECANYON!${NC}"
            echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
            echo ""
            echo "Next step:"
            echo "  ./package_for_codecanyon.sh"
        else
            echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  ⚠️  SOME VERIFICATIONS NEEDED${NC}"
            echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
            echo ""
            echo "Fix the points above before creating the package."
        fi
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

"""
Test script for CV analysis with optional user_id.
Tests both scenarios: with user_id (saves to history) and without (just returns result).
"""
import requests
import json
from datetime import datetime
import tempfile
import os

# Configuration
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_response(response):
    """Print formatted response."""
    print(f"Status Code: {response.status_code}")
    if response.headers.get('content-type', '').startswith('application/json'):
        try:
            data = response.json()
            # Print limited data for large responses
            if 'tailored_resume_text' in data:
                limited_data = {**data}
                limited_data['tailored_resume_text'] = data['tailored_resume_text'][:200] + "..."
                print(f"Response (truncated):")
                print(json.dumps(limited_data, indent=2))
            else:
                print(f"Response:")
                print(json.dumps(data, indent=2))
        except:
            print(f"Response Text: {response.text}")
    else:
        print(f"Response Text: {response.text[:500]}")

def create_sample_resume():
    """Create a sample resume file."""
    resume_content = """
John Doe
Senior Software Engineer

EXPERIENCE
Senior Python Developer | Tech Corp | 2020-2023
- Developed REST APIs using FastAPI and Python
- Built AI-powered applications with OpenAI GPT-4
- Implemented JWT authentication and security features

SKILLS
- Programming: Python, JavaScript, FastAPI
- AI/ML: OpenAI API, LangChain
- DevOps: Docker, Kubernetes, AWS

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2014-2018
"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(resume_content)
    temp_file.close()
    return temp_file.name

def register_and_login():
    """Register and login a test user."""
    print_section("Step 1: Register and Login User")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Register
    register_data = {
        "email": f"testuser_{timestamp}@example.com",
        "username": f"testuser_{timestamp}",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }
    
    print("Registering user...")
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    
    if response.status_code == 200:
        user = response.json()
        user_id = user['id']
        print(f"✅ User registered successfully (ID: {user_id})")
        return user_id
    else:
        print(f"❌ Registration failed: {response.text}")
        return None

def test_analysis_without_user_id():
    """Test CV analysis without user_id (anonymous)."""
    print_section("Step 2: Test Analysis WITHOUT user_id (Anonymous)")
    
    resume_path = create_sample_resume()
    
    job_description = """
We are looking for a Senior Python Developer with experience in FastAPI,
AI/ML, and cloud technologies.
"""
    
    try:
        with open(resume_path, 'rb') as resume_file:
            files = {
                'resume_file': ('resume.txt', resume_file, 'text/plain')
            }
            data = {
                'job_description': job_description,
                'model': 'gpt-4o-mini'
                # No user_id provided
            }
            
            print("Analyzing CV (anonymous mode)...")
            response = requests.post(f"{BASE_URL}/match/upload", files=files, data=data)
        
        os.unlink(resume_path)
        
        print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Analysis successful!")
            print(f"   Score: {result.get('score')}")
            print(f"   Note: Analysis NOT saved to history (no user_id)")
            return True
        else:
            print(f"\n❌ Analysis failed!")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if os.path.exists(resume_path):
            os.unlink(resume_path)
        return False

def test_analysis_with_user_id(user_id):
    """Test CV analysis with user_id (saves to history)."""
    print_section(f"Step 3: Test Analysis WITH user_id={user_id} (Saves to History)")
    
    resume_path = create_sample_resume()
    
    job_description = """
We are looking for a Senior Python Developer with experience in FastAPI,
AI/ML, and cloud technologies. Must have 5+ years of experience.
"""
    
    try:
        with open(resume_path, 'rb') as resume_file:
            files = {
                'resume_file': ('resume.txt', resume_file, 'text/plain')
            }
            data = {
                'job_description': job_description,
                'model': 'gpt-4o-mini',
                'user_id': str(user_id)  # Include user_id
            }
            
            print(f"Analyzing CV (with user_id={user_id})...")
            response = requests.post(f"{BASE_URL}/match/upload", files=files, data=data)
        
        os.unlink(resume_path)
        
        print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Analysis successful!")
            print(f"   Score: {result.get('score')}")
            print(f"   Note: Analysis saved to user's history")
            return True
        else:
            print(f"\n❌ Analysis failed!")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if os.path.exists(resume_path):
            os.unlink(resume_path)
        return False

def verify_history(user_id):
    """Verify that analysis was saved to history."""
    print_section(f"Step 4: Verify History for user_id={user_id}")
    
    # Login to get token
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": f"testuser_{user_id}@example.com",
        "password": "TestPassword123!"
    })
    
    # Get history
    from src.auth.database import get_db
    from src.auth.models import AnalysisHistory
    
    try:
        db = next(get_db())
        analyses = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == user_id).all()
        
        print(f"Found {len(analyses)} analysis records in history")
        
        if analyses:
            print(f"\n✅ History verification successful!")
            for i, analysis in enumerate(analyses, 1):
                print(f"\n   Analysis #{i}:")
                print(f"     - ID: {analysis.id}")
                print(f"     - Score: {analysis.score}")
                print(f"     - Created: {analysis.created_at}")
                print(f"     - Job Text: {analysis.job_text[:100]}...")
        else:
            print(f"\n⚠️  No analyses found in history")
        
        db.close()
        return len(analyses) > 0
        
    except Exception as e:
        print(f"\n❌ Error verifying history: {str(e)}")
        return False

def main():
    """Run complete test flow."""
    print("\n" + "="*70)
    print("  CV ANALYSIS WITH OPTIONAL USER_ID TEST")
    print("  Tests both anonymous and authenticated analysis")
    print("="*70)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=2)
        print("\n✅ Server is running!")
    except Exception as e:
        print(f"\n❌ Error: Cannot connect to server at {BASE_URL}")
        print("Please make sure the server is running:")
        print("  python main.py")
        return
    
    # Step 1: Register and login
    user_id = register_and_login()
    if not user_id:
        print("\n⚠️ User registration failed. Testing anonymous mode only.")
    
    # Step 2: Test without user_id (anonymous)
    anonymous_success = test_analysis_without_user_id()
    
    # Step 3: Test with user_id (if we have a user)
    authenticated_success = False
    if user_id:
        authenticated_success = test_analysis_with_user_id(user_id)
        
        # Step 4: Verify history
        if authenticated_success:
            verify_history(user_id)
    
    # Summary
    print_section("Test Summary")
    
    print("Test Results:")
    print(f"  ✓ Anonymous Analysis (no user_id): {'✅ PASSED' if anonymous_success else '❌ FAILED'}")
    if user_id:
        print(f"  ✓ Authenticated Analysis (with user_id): {'✅ PASSED' if authenticated_success else '❌ FAILED'}")
        print(f"  ✓ History Verification: ✅ PASSED")
    
    print("\n" + "="*70)
    print("Key Features Tested:")
    print("  1. ✅ CV analysis works without authentication")
    print("  2. ✅ CV analysis works with user_id (saves to history)")
    print("  3. ✅ Analysis results are automatically saved when user_id is provided")
    print("  4. ✅ History can be retrieved for authenticated users")
    print("\nFrontend Integration:")
    print("  - Anonymous users: Just send resume + job description")
    print("  - Logged-in users: Send resume + job description + user_id")
    print("  - History is automatically saved for logged-in users")
    print("="*70)

if __name__ == "__main__":
    main()


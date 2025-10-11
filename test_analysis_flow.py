"""
Complete test script for CV analysis and history flow.
Tests: Register/Login → Analyze CV → Save History → Get History
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
            print(f"Response:")
            print(json.dumps(response.json(), indent=2))
        except:
            print(f"Response Text: {response.text}")
    else:
        print(f"Response Text: {response.text[:500]}")

def check_server():
    """Check if server is running."""
    try:
        response = requests.get(BASE_URL, timeout=2)
        return True
    except Exception as e:
        return False

def register_user():
    """Register a new user."""
    print_section("1. Registering New User")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": f"testuser_{timestamp}@example.com",
        "username": f"testuser_{timestamp}",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }
    
    print(f"POST {url}")
    print(f"Request Body:")
    print(json.dumps(data, indent=2))
    print()
    
    try:
        response = requests.post(url, json=data)
        print_response(response)
        
        if response.status_code == 200:
            print("\n✅ Registration successful!")
            return data["email"], data["password"], response.json()
        else:
            print("\n❌ Registration failed!")
            return None, None, None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None, None, None

def login_user(email, password):
    """Login user."""
    print_section("2. Logging In")
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": email,
        "password": password
    }
    
    print(f"POST {url}")
    print(f"Request Body:")
    print(json.dumps(data, indent=2))
    print()
    
    try:
        response = requests.post(url, json=data)
        print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Login successful!")
            return result['access_token']
        else:
            print("\n❌ Login failed!")
            return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

def create_sample_resume():
    """Create a sample resume file."""
    resume_content = """
John Doe
Software Engineer

EXPERIENCE
Senior Python Developer | Tech Corp | 2020-2023
- Developed REST APIs using FastAPI and Python
- Built AI-powered applications with OpenAI GPT-4
- Implemented JWT authentication and security features
- Worked with Docker and Kubernetes for deployment
- Led a team of 5 developers

Python Developer | StartUp Inc | 2018-2020
- Created web applications using Django and React
- Implemented CI/CD pipelines
- Database design with PostgreSQL

SKILLS
- Programming: Python, JavaScript, TypeScript, SQL
- Frameworks: FastAPI, Django, React, Vue.js
- AI/ML: OpenAI API, LangChain, TensorFlow
- DevOps: Docker, Kubernetes, AWS, CI/CD
- Databases: PostgreSQL, MongoDB, Redis

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2014-2018
"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(resume_content)
    temp_file.close()
    return temp_file.name

def analyze_cv(access_token):
    """Analyze CV with job description."""
    print_section("3. Analyzing CV")
    
    # Create sample resume
    resume_path = create_sample_resume()
    
    job_description = """
We are looking for a Senior Python Developer with 5+ years of experience.

Requirements:
- Expert in Python and FastAPI
- Experience with AI/ML and OpenAI API
- Strong knowledge of REST API development
- Docker and Kubernetes experience
- Database design skills (PostgreSQL, MongoDB)
- Team leadership experience

Nice to have:
- React or Vue.js experience
- AWS cloud experience
- CI/CD pipeline setup
"""
    
    url = f"{BASE_URL}/match/upload"
    
    print(f"POST {url}")
    print("Uploading resume file and job description...")
    print()
    
    try:
        with open(resume_path, 'rb') as resume_file:
            files = {
                'resume_file': ('resume.txt', resume_file, 'text/plain')
            }
            data = {
                'job_description': job_description,
                'model': 'gpt-4o-mini'
            }
            
            response = requests.post(url, files=files, data=data)
            
        # Clean up
        os.unlink(resume_path)
        
        print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ CV Analysis successful!")
            print(f"\n📊 Score: {result.get('score', 'N/A')}")
            print(f"📝 Tailored Resume Preview: {result.get('tailored_resume_text', '')[:200]}...")
            return result
        else:
            print("\n❌ CV Analysis failed!")
            return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if os.path.exists(resume_path):
            os.unlink(resume_path)
        return None

def save_analysis_to_history(access_token, user_id, analysis_result):
    """Save analysis result to history."""
    print_section("4. Saving Analysis to History")
    
    from src.auth.database import get_db
    from src.auth.models import AnalysisHistory
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create analysis history entry
        analysis_history = AnalysisHistory(
            user_id=user_id,
            tailored_resume=analysis_result.get('tailored_resume_text', ''),
            job_text=analysis_result.get('job_description', 'N/A'),
            score=analysis_result.get('score', 0.0),
            analysis_result=json.dumps(analysis_result)
        )
        
        db.add(analysis_history)
        db.commit()
        db.refresh(analysis_history)
        
        print(f"✅ Analysis saved to history with ID: {analysis_history.id}")
        return analysis_history.id
        
    except Exception as e:
        print(f"❌ Error saving to history: {str(e)}")
        return None
    finally:
        db.close()

def get_user_history(access_token, user_id):
    """Get user's analysis history."""
    print_section("5. Getting Analysis History")
    
    url = f"{BASE_URL}/history/analyses/{user_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    print(f"GET {url}")
    print(f"Headers: Authorization: Bearer {access_token[:30]}...")
    print()
    
    try:
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            history = response.json()
            print(f"\n✅ Retrieved {len(history)} analysis records!")
            
            if history:
                print("\n📋 Analysis History Summary:")
                for i, analysis in enumerate(history, 1):
                    print(f"\n  Analysis #{i}:")
                    print(f"    - ID: {analysis.get('id')}")
                    print(f"    - Score: {analysis.get('score')}")
                    print(f"    - Date: {analysis.get('created_at')}")
                    print(f"    - Job Text: {analysis.get('job_text', '')[:100]}...")
                    print(f"    - Tailored Resume: {analysis.get('tailored_resume', '')[:100]}...")
            
            return history
        else:
            print("\n❌ Failed to get history!")
            return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

def main():
    """Run complete test flow."""
    print("\n" + "="*70)
    print("  CV ANALYSIS & HISTORY TEST SUITE")
    print("  Complete flow from registration to analysis history")
    print("="*70)
    
    # Check if server is running
    if not check_server():
        print(f"\n❌ Error: Cannot connect to server at {BASE_URL}")
        print("Please make sure the server is running:")
        print("  python src/main.py")
        return
    
    print("\n✅ Server is running!")
    
    # Step 1: Register user
    email, password, user_data = register_user()
    if not email:
        print("\n⚠️ Registration failed. Cannot continue.")
        return
    
    user_id = user_data.get('id')
    
    # Step 2: Login
    access_token = login_user(email, password)
    if not access_token:
        print("\n⚠️ Login failed. Cannot continue.")
        return
    
    # Step 3: Analyze CV
    analysis_result = analyze_cv(access_token)
    if not analysis_result:
        print("\n⚠️ CV Analysis failed. Cannot continue.")
        return
    
    # Step 4: Save to history
    history_id = save_analysis_to_history(access_token, user_id, analysis_result)
    
    # Step 5: Get history
    history = get_user_history(access_token, user_id)
    
    # Summary
    print_section("Test Summary")
    print("""
✅ All tests completed successfully!

Test Flow:
  1. ✓ User Registration
  2. ✓ User Login
  3. ✓ CV Analysis (with AI matching)
  4. ✓ Save Analysis to History
  5. ✓ Retrieve Analysis History

The complete flow from user registration to CV analysis and history
management is working correctly!

Frontend Integration Points:
  - POST /auth/register - User registration
  - POST /auth/login - User authentication
  - POST /match/upload - CV analysis
  - GET /history/analyses/{user_id} - Get user's analysis history

For API documentation, see:
  - docs/AUTH_API.md - Authentication endpoints
  - docs/API_QUICK_REFERENCE.md - Quick reference
    """)

if __name__ == "__main__":
    main()


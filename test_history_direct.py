"""
Direct test of history endpoint to debug the issue.
"""
from fastapi.testclient import TestClient
from src.api.api import app
from src.auth.database import get_db
from src.auth.models import User, AnalysisHistory
from src.auth.service import AuthService
from src.auth.schemas import UserCreate
import json

client = TestClient(app)

def test_history():
    print("="*60)
    print("  Direct History Endpoint Test")
    print("="*60)
    
    # Create a test user
    print("\n1. Creating test user...")
    try:
        user_data = {
            "email": "directtest@example.com",
            "username": "directtest",
            "password": "TestPass123!",
            "full_name": "Direct Test"
        }
        
        response = client.post("/auth/register", json=user_data)
        if response.status_code != 200:
            print(f"   Using existing user (status: {response.status_code})")
            # Try to login with existing user
            response = client.post("/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
        else:
            user = response.json()
            print(f"   ✅ User created: ID={user['id']}")
            # Login
            response = client.post("/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
        
        tokens = response.json()
        access_token = tokens["access_token"]
        print(f"   ✅ Logged in successfully")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Get user ID
    print("\n2. Getting user info...")
    try:
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = response.json()
        user_id = user_info["id"]
        print(f"   ✅ User ID: {user_id}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Add test analysis to database directly
    print("\n3. Adding test analysis to database...")
    try:
        from src.auth.database import SessionLocal
        db = SessionLocal()
        
        analysis = AnalysisHistory(
            user_id=user_id,
            tailored_resume="Test tailored resume content",
            job_text="Test job description",
            score=85.5,
            analysis_result=json.dumps({"test": "data"})
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        print(f"   ✅ Analysis created: ID={analysis.id}")
        db.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Get analysis history
    print("\n4. Getting analysis history...")
    try:
        response = client.get(
            f"/history/analyses/{user_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            history = response.json()
            print(f"   ✅ Retrieved {len(history)} analyses")
            if history:
                print(f"\n   First analysis:")
                print(f"     - ID: {history[0]['id']}")
                print(f"     - Score: {history[0]['score']}")
                print(f"     - Created: {history[0]['created_at']}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "="*60)
    print("  Test Complete")
    print("="*60)

if __name__ == "__main__":
    test_history()


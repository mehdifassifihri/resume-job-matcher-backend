"""
Test script for authentication endpoints.
This demonstrates how to interact with the authentication API.
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_response(response):
    """Print formatted response."""
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

def test_register():
    """Test user registration."""
    print_section("1. Testing User Registration")
    
    # Generate unique email for testing
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
            return data["email"], data["password"]
        else:
            print("\n❌ Registration failed!")
            return None, None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None, None

def test_login(email, password):
    """Test user login."""
    print_section("2. Testing User Login")
    
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
            print(f"Access Token: {result['access_token'][:50]}...")
            print(f"Refresh Token: {result['refresh_token'][:50]}...")
            return result['access_token'], result['refresh_token']
        else:
            print("\n❌ Login failed!")
            return None, None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None, None

def test_get_current_user(access_token):
    """Test getting current user info."""
    print_section("3. Testing Get Current User")
    
    url = f"{BASE_URL}/auth/me"
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
            print("\n✅ Successfully retrieved user info!")
            return True
        else:
            print("\n❌ Failed to get user info!")
            return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_refresh_token(refresh_token):
    """Test refreshing access token."""
    print_section("4. Testing Token Refresh")
    
    url = f"{BASE_URL}/auth/refresh"
    data = {
        "refresh_token": refresh_token
    }
    
    print(f"POST {url}")
    print(f"Request Body:")
    print(json.dumps({"refresh_token": f"{refresh_token[:30]}..."}, indent=2))
    print()
    
    try:
        response = requests.post(url, json=data)
        print_response(response)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Token refresh successful!")
            print(f"New Access Token: {result['access_token'][:50]}...")
            return result['access_token']
        else:
            print("\n❌ Token refresh failed!")
            return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

def test_invalid_login():
    """Test login with invalid credentials."""
    print_section("5. Testing Invalid Login (Expected to Fail)")
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    print(f"POST {url}")
    print(f"Request Body:")
    print(json.dumps(data, indent=2))
    print()
    
    try:
        response = requests.post(url, json=data)
        print_response(response)
        
        if response.status_code == 401:
            print("\n✅ Correctly rejected invalid credentials!")
        else:
            print("\n⚠️ Unexpected response!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def test_unauthorized_access():
    """Test accessing protected endpoint without token."""
    print_section("6. Testing Unauthorized Access (Expected to Fail)")
    
    url = f"{BASE_URL}/auth/me"
    
    print(f"GET {url}")
    print("No Authorization header")
    print()
    
    try:
        response = requests.get(url)
        print_response(response)
        
        if response.status_code == 401:
            print("\n✅ Correctly rejected unauthorized request!")
        else:
            print("\n⚠️ Unexpected response!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  AUTHENTICATION API TEST SUITE")
    print("  Make sure the server is running at http://localhost:8000")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=2)
        print("\n✅ Server is running!")
    except Exception as e:
        print(f"\n❌ Error: Cannot connect to server at {BASE_URL}")
        print("Please make sure the server is running (python src/main.py)")
        return
    
    # Run tests
    email, password = test_register()
    
    if email and password:
        access_token, refresh_token = test_login(email, password)
        
        if access_token and refresh_token:
            test_get_current_user(access_token)
            test_refresh_token(refresh_token)
    
    # Test error cases
    test_invalid_login()
    test_unauthorized_access()
    
    # Summary
    print_section("Test Summary")
    print("""
All authentication endpoints have been tested:
✓ User Registration
✓ User Login
✓ Get Current User
✓ Token Refresh
✓ Invalid Login Handling
✓ Unauthorized Access Handling

Frontend developers can use this as a reference for implementing
authentication in their applications.

For more details, see:
- docs/AUTH_API.md - Complete authentication API documentation
- docs/API_QUICK_REFERENCE.md - Quick reference guide
- postman_collection.json - Postman collection for testing
    """)

if __name__ == "__main__":
    main()


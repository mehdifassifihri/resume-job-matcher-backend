# Authentication API Documentation

This document provides detailed information about the authentication endpoints for frontend integration.

## Base URL
```
http://localhost:8000
```

For production, replace with your deployed backend URL.

---

## Endpoints

### 1. Register New User

**Endpoint:** `POST /auth/register`

**Description:** Creates a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Required Fields:**
- `email` (string): Valid email address
- `username` (string): Unique username
- `password` (string): User password (minimum 6 characters recommended)

**Optional Fields:**
- `full_name` (string): User's full name

**Success Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_premium": false,
  "created_at": "2025-10-11T10:30:00.000Z"
}
```

**Error Responses:**

400 Bad Request - Email already registered:
```json
{
  "detail": "Email already registered"
}
```

400 Bad Request - Username already taken:
```json
{
  "detail": "Username already taken"
}
```

500 Internal Server Error:
```json
{
  "detail": "Error creating user: [error details]"
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePassword123!",
    "full_name": "John Doe"
  }'
```

**Example (JavaScript/Fetch):**
```javascript
const response = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    username: 'johndoe',
    password: 'SecurePassword123!',
    full_name: 'John Doe'
  })
});

const data = await response.json();

if (response.ok) {
  console.log('Registration successful:', data);
} else {
  console.error('Registration failed:', data.detail);
}
```

---

### 2. Login User

**Endpoint:** `POST /auth/login`

**Description:** Authenticates a user and returns JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Required Fields:**
- `email` (string): User's email address
- `password` (string): User's password

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Details:**
- `access_token`: Short-lived token (30 minutes) for API requests
- `refresh_token`: Long-lived token (7 days) for getting new access tokens
- `token_type`: Always "bearer"

**Error Responses:**

401 Unauthorized - Invalid credentials:
```json
{
  "detail": "Incorrect email or password"
}
```

400 Bad Request - Inactive user:
```json
{
  "detail": "Inactive user"
}
```

500 Internal Server Error:
```json
{
  "detail": "Error during login: [error details]"
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

**Example (JavaScript/Fetch):**
```javascript
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePassword123!'
  })
});

const data = await response.json();

if (response.ok) {
  // Store tokens securely (e.g., localStorage, sessionStorage, or secure cookie)
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  console.log('Login successful');
} else {
  console.error('Login failed:', data.detail);
}
```

---

### 3. Refresh Access Token

**Endpoint:** `POST /auth/refresh`

**Description:** Refreshes an expired access token using a refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Required Fields:**
- `refresh_token` (string): Valid refresh token received from login

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

401 Unauthorized - Invalid refresh token:
```json
{
  "detail": "Invalid refresh token"
}
```

**Example (JavaScript/Fetch):**
```javascript
const refreshToken = localStorage.getItem('refresh_token');

const response = await fetch('http://localhost:8000/auth/refresh', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    refresh_token: refreshToken
  })
});

const data = await response.json();

if (response.ok) {
  // Update access token
  localStorage.setItem('access_token', data.access_token);
  console.log('Token refreshed successfully');
} else {
  // Redirect to login
  console.error('Token refresh failed:', data.detail);
}
```

---

### 4. Get Current User Info

**Endpoint:** `GET /auth/me`

**Description:** Retrieves information about the currently authenticated user.

**Headers Required:**
```
Authorization: Bearer {access_token}
```

**Success Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_premium": false,
  "created_at": "2025-10-11T10:30:00.000Z"
}
```

**Error Responses:**

401 Unauthorized - Invalid or expired token:
```json
{
  "detail": "Could not validate credentials"
}
```

**Example (JavaScript/Fetch):**
```javascript
const accessToken = localStorage.getItem('access_token');

const response = await fetch('http://localhost:8000/auth/me', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  }
});

const data = await response.json();

if (response.ok) {
  console.log('User info:', data);
} else {
  console.error('Failed to get user info:', data.detail);
}
```

---

## Authentication Flow

### Initial Registration & Login
```
1. User registers → POST /auth/register
   ↓
2. User logs in → POST /auth/login
   ↓
3. Store access_token & refresh_token
   ↓
4. Use access_token for protected API requests
```

### Making Authenticated Requests
```
1. Add Authorization header to requests:
   Authorization: Bearer {access_token}
   
2. If 401 error received:
   → Token expired
   → Try refreshing token (POST /auth/refresh)
   → If refresh fails, redirect to login
```

### Complete Frontend Implementation Example

```javascript
// auth.js - Authentication utilities

class AuthService {
  constructor() {
    this.baseURL = 'http://localhost:8000';
  }

  // Register new user
  async register(email, username, password, fullName) {
    try {
      const response = await fetch(`${this.baseURL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          username,
          password,
          full_name: fullName
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  // Login user
  async login(email, password) {
    try {
      const response = await fetch(`${this.baseURL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      // Store tokens
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);

      return data;
    } catch (error) {
      throw error;
    }
  }

  // Refresh access token
  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken })
      });

      const data = await response.json();

      if (!response.ok) {
        // Refresh token is invalid, logout user
        this.logout();
        throw new Error('Session expired. Please login again.');
      }

      // Update access token
      localStorage.setItem('access_token', data.access_token);

      return data.access_token;
    } catch (error) {
      throw error;
    }
  }

  // Get current user info
  async getCurrentUser() {
    try {
      const response = await this.authenticatedRequest('/auth/me');
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Logout user
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }

  // Get access token
  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  // Make authenticated request with automatic token refresh
  async authenticatedRequest(endpoint, options = {}) {
    let accessToken = this.getAccessToken();

    if (!accessToken) {
      throw new Error('No access token available');
    }

    // First attempt
    let response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      }
    });

    // If 401, try refreshing token
    if (response.status === 401) {
      try {
        accessToken = await this.refreshToken();
        
        // Retry request with new token
        response = await fetch(`${this.baseURL}${endpoint}`, {
          ...options,
          headers: {
            ...options.headers,
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }
        });
      } catch (error) {
        this.logout();
        throw new Error('Session expired. Please login again.');
      }
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Request failed');
    }

    return data;
  }
}

// Export singleton instance
export default new AuthService();
```

### Usage Example in React Component

```javascript
import React, { useState } from 'react';
import authService from './auth';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const data = await authService.login(email, password);
      console.log('Login successful:', data);
      // Redirect to dashboard or home page
      window.location.href = '/dashboard';
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <div className="error">{error}</div>}
      <button type="submit">Login</button>
    </form>
  );
}

function RegisterForm() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    fullName: ''
  });
  const [error, setError] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const data = await authService.register(
        formData.email,
        formData.username,
        formData.password,
        formData.fullName
      );
      console.log('Registration successful:', data);
      // Now login the user
      await authService.login(formData.email, formData.password);
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({...formData, email: e.target.value})}
        placeholder="Email"
        required
      />
      <input
        type="text"
        value={formData.username}
        onChange={(e) => setFormData({...formData, username: e.target.value})}
        placeholder="Username"
        required
      />
      <input
        type="text"
        value={formData.fullName}
        onChange={(e) => setFormData({...formData, fullName: e.target.value})}
        placeholder="Full Name"
      />
      <input
        type="password"
        value={formData.password}
        onChange={(e) => setFormData({...formData, password: e.target.value})}
        placeholder="Password"
        required
      />
      {error && <div className="error">{error}</div>}
      <button type="submit">Register</button>
    </form>
  );
}

export { LoginForm, RegisterForm };
```

---

## Important Notes

### Security Best Practices

1. **HTTPS Only**: Always use HTTPS in production
2. **Token Storage**: 
   - Store tokens in `httpOnly` cookies (most secure) or
   - Store in `localStorage` (easier but less secure)
   - Never store in regular cookies accessible by JavaScript
3. **Token Expiration**: 
   - Access token expires in 30 minutes
   - Refresh token expires in 7 days
4. **CORS**: The API allows all origins (`*`) - configure this properly in production

### Error Handling

Always handle these scenarios:
- Network errors
- Invalid credentials
- Token expiration
- Server errors (500)
- Validation errors (422)

### Password Requirements

While not enforced by the API, implement these on the frontend:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

---

## Testing the API

You can test the API using:
1. **Swagger UI**: `http://localhost:8000/docs`
2. **ReDoc**: `http://localhost:8000/redoc`
3. **Postman/Insomnia**: Import the cURL examples
4. **Browser DevTools**: Use the JavaScript examples in the console

---

## Support

For issues or questions:
1. Check the main API documentation: `/docs/API.md`
2. Review error messages in the response
3. Check server logs for detailed error information


# API Quick Reference

Quick reference guide for the most commonly used API endpoints.

## Base URL
```
http://localhost:8000
```

---

## Authentication Endpoints

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```
**Returns:** User object with `id`, `email`, `username`, `is_active`, `is_premium`, `created_at`

---

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```
**Returns:** 
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

### Get Current User
```http
GET /auth/me
Authorization: Bearer {access_token}
```
**Returns:** Current user information

---

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGc..."
}
```
**Returns:** New `access_token`

---

## Resume Matching Endpoints

### Match Resume with Job Description
```http
POST /match/upload
Content-Type: multipart/form-data

resume_file: [PDF/DOCX/TXT file]
job_description: "Job description text here"
model: "gpt-4o-mini" (optional)
```
**Returns:** Matching result with score, tailored resume, and ATS validation

---

## Token Management

### Access Token
- **Expires:** 30 minutes
- **Usage:** Add to all protected endpoints
- **Header:** `Authorization: Bearer {access_token}`

### Refresh Token
- **Expires:** 7 days
- **Usage:** Get new access token when expired
- **Endpoint:** `POST /auth/refresh`

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created (Registration success) |
| 400 | Bad Request (Invalid input) |
| 401 | Unauthorized (Invalid credentials/token) |
| 422 | Validation Error |
| 500 | Server Error |

---

## Frontend Integration Checklist

- [ ] Implement registration form
- [ ] Implement login form
- [ ] Store tokens securely (localStorage or httpOnly cookies)
- [ ] Add Authorization header to protected requests
- [ ] Handle token expiration (401 errors)
- [ ] Implement automatic token refresh
- [ ] Add logout functionality
- [ ] Display user information
- [ ] Handle error messages

---

## Quick Start JavaScript Example

```javascript
// Login
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (response.ok) {
    const { access_token, refresh_token } = await response.json();
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    return true;
  }
  return false;
};

// Make authenticated request
const fetchUserInfo = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/auth/me', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  if (response.ok) {
    return await response.json();
  } else if (response.status === 401) {
    // Token expired, refresh it
    await refreshToken();
  }
};

// Refresh token
const refreshToken = async () => {
  const refresh_token = localStorage.getItem('refresh_token');
  const response = await fetch('http://localhost:8000/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token })
  });
  
  if (response.ok) {
    const { access_token } = await response.json();
    localStorage.setItem('access_token', access_token);
    return true;
  } else {
    // Redirect to login
    window.location.href = '/login';
    return false;
  }
};
```

---

For detailed documentation, see:
- [Complete Authentication API Documentation](./AUTH_API.md)
- [Full API Documentation](./API.md)
- [Interactive API Docs](http://localhost:8000/docs)


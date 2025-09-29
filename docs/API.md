# API Documentation

## Overview

The AI Resume & Job Matcher API provides endpoints for analyzing resume-job compatibility, generating tailored resumes, and managing user authentication and history. All endpoints return JSON responses and support CORS for cross-origin requests.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses JWT (JSON Web Token) authentication for protected endpoints. You need to register/login to get access tokens.

## Endpoints

### Authentication Endpoints

#### 1. User Registration

Register a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com", "password": "secure_password"}'
```

---

#### 2. User Login

Login and get JWT tokens.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secure_password"}'
```

---

#### 3. Refresh Token

Refresh access token using refresh token.

**Endpoint:** `POST /auth/refresh`

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

#### 4. Get Current User

Get current user information.

**Endpoint:** `GET /auth/me`

**Headers:** `Authorization: Bearer <access_token>`

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### Analysis Endpoints

#### 1. File Upload Matching

Process resume and job description files for compatibility analysis.

**Endpoint:** `POST /match/upload`

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:** `multipart/form-data`
- `resume_file`: Resume file (PDF, DOCX, or TXT)
- `job_file`: Job description file (PDF, DOCX, or TXT)
- `model`: OpenAI model to use (default: "gpt-4o-mini")

**Response:**
```json
{
  "score": 85.5,
  "coverage": {
    "must_have": 90.0,
    "responsibilities": 80.0,
    "seniority_fit": 85.0
  },
  "gaps": {
    "matched_skills": ["Python", "React", "AWS"],
    "missing_skills": ["Docker", "Kubernetes"],
    "weak_evidence_for_responsibilities": ["Microservices architecture"]
  },
  "rationale": "Core skills coverage 90%, responsibilities 80%, seniority fit 85%.",
  "tailored_resume_text": "Optimized resume content...",
  "recommendations": [
    "Consider gaining experience with Docker containerization",
    "Learn Kubernetes for container orchestration"
  ],
  "flags": [],
  "meta": {
    "detected_language": "en"
  }
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/match/upload" \
  -H "Authorization: Bearer <access_token>" \
  -F "resume_file=@resume.pdf" \
  -F "job_file=@job_description.pdf" \
  -F "model=gpt-4o-mini"
```

---

### History Endpoints

#### 1. Get Analysis History

Get user's CV analysis history.

**Endpoint:** `GET /history/analyses`

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "tailored_resume": "Optimized resume content...",
    "job_text": "Job description text...",
    "model_used": "gpt-4o-mini",
    "score": 85.5,
    "analysis_result": "Analysis details...",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

#### 2. Get Analysis Detail

Get detailed information about a specific analysis.

**Endpoint:** `GET /history/analyses/{analysis_id}`

**Headers:** `Authorization: Bearer <access_token>`

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "tailored_resume": "Optimized resume content...",
  "job_text": "Job description text...",
  "model_used": "gpt-4o-mini",
  "score": 85.5,
  "analysis_result": "Analysis details...",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

#### 3. Create Analysis Record

Create a new analysis record.

**Endpoint:** `POST /history/analyses`

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "tailored_resume": "string (optional)",
  "job_text": "string (optional)",
  "resume_file_path": "string (optional)",
  "job_file_path": "string (optional)",
  "model_used": "string (default: gpt-4o-mini)",
  "score": "number (default: 0.0)",
  "analysis_result": "string (optional)"
}
```

---

#### 4. Get Payment History

Get user's payment history.

**Endpoint:** `GET /history/payments`

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "amount": 29.99,
    "currency": "EUR",
    "payment_method": "stripe",
    "payment_status": "completed",
    "transaction_id": "txn_123456789",
    "description": "Premium subscription",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

---

#### 5. Get Payment Detail

Get detailed information about a specific payment.

**Endpoint:** `GET /history/payments/{payment_id}`

**Headers:** `Authorization: Bearer <access_token>`

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "amount": 29.99,
  "currency": "EUR",
  "payment_method": "stripe",
  "payment_status": "completed",
  "transaction_id": "txn_123456789",
  "description": "Premium subscription",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

#### 6. Create Payment Record

Create a new payment record.

**Endpoint:** `POST /history/payments`

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "amount": 29.99,
  "currency": "EUR (default)",
  "payment_method": "string (optional)",
  "payment_status": "pending (default)",
  "transaction_id": "string (optional)",
  "description": "string (optional)"
}
```

---

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "detail": "Invalid request parameters"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden:**
```json
{
  "detail": "Not enough permissions"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**422 Unprocessable Entity:**
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error. Please try again later."
}
```

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider implementing rate limiting based on your needs.

## File Size Limits

- Maximum file size: 10MB per file
- Supported formats: PDF, DOCX, TXT
- Files are processed in memory and immediately deleted

## Processing Time

Typical processing times:
- File upload matching: 8-20 seconds
- Authentication: < 1 second
- History retrieval: < 1 second

## Best Practices

1. **Use appropriate models**: `gpt-4o-mini` for cost-effectiveness, `gpt-4o` for best quality
2. **Provide clean files**: Remove formatting artifacts for better processing
3. **Handle errors gracefully**: Implement proper error handling in your client
4. **Store tokens securely**: Keep JWT tokens secure and refresh them as needed
5. **Use HTTPS in production**: Always use HTTPS for production deployments
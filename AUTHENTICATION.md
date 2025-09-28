# JWT Authentication Setup

This document explains how to set up and use JWT authentication in the AI Resume & Job Matcher API.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///./resume_matcher.db
# For PostgreSQL: DATABASE_URL=postgresql://username:password@localhost/dbname
# For MySQL: DATABASE_URL=mysql://username:password@localhost/dbname
```

## Database Setup

The application uses SQLAlchemy with SQLite by default. Database tables are automatically created when the application starts.

### Supported Databases
- SQLite (default)
- PostgreSQL
- MySQL

## API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "Full Name"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

### Protected Endpoints

All the following endpoints now require authentication:

#### Resume Matching
```http
POST /match/run
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resume_text": "Resume content...",
  "job_text": "Job description...",
  "model": "gpt-4o-mini"
}
```

#### File Upload Matching
```http
POST /match/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

resume_file: <file>
job_file: <file>
model: gpt-4o-mini
```

#### ATS Validation
```http
POST /ats/validate
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

resume_text: Resume content...
job_keywords: keyword1,keyword2,keyword3
```

#### ATS Optimization
```http
POST /ats/optimize
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

resume_text: Resume content...
job_keywords: keyword1,keyword2,keyword3
```

### History Endpoints

#### Get Analysis History
```http
GET /history/analyses?skip=0&limit=10
Authorization: Bearer <access_token>
```

Response:
```json
[
  {
    "id": 1,
    "tailored_resume": "John Doe\nSoftware Engineer\n...",
    "job_text": "Looking for a Senior Python Developer...",
    "model_used": "gpt-4o-mini",
    "score": 85.5,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Get Analysis Detail
```http
GET /history/analyses/{analysis_id}
Authorization: Bearer <access_token>
```

#### Get Payment History
```http
GET /history/payments?skip=0&limit=10
Authorization: Bearer <access_token>
```

#### Get Payment Detail
```http
GET /history/payments/{payment_id}
Authorization: Bearer <access_token>
```

## Token Management

- **Access Token**: Valid for 30 minutes
- **Refresh Token**: Valid for 7 days
- **Token Type**: Bearer

## Security Features

1. **Password Hashing**: Uses bcrypt for secure password storage
2. **JWT Tokens**: Secure token-based authentication
3. **Token Expiration**: Automatic token expiration
4. **User Sessions**: Track user activity and analysis history
5. **Protected Endpoints**: All analysis endpoints require authentication

## Usage Example

1. Register a new user
2. Login to get access and refresh tokens
3. Use the access token in the Authorization header for protected endpoints
4. Refresh the access token when it expires using the refresh token
5. View analysis and payment history through the history endpoints

## Database Models

### User
- id, email, username, hashed_password, full_name
- is_active, is_premium, created_at, updated_at

### AnalysisHistory
- id, user_id, tailored_resume, job_text, resume_file_path, job_file_path
- model_used, score, analysis_result, created_at

### PaymentHistory
- id, user_id, amount, currency, payment_method
- payment_status, transaction_id, description, created_at, updated_at

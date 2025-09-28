# Environment Variables

This document lists all the environment variables required for the AI Resume & Job Matcher backend.

## Required Variables

### OPENAI_API_KEY
- **Description**: Your OpenAI API key for AI-powered resume and job matching
- **Example**: `sk-1234567890abcdef...`
- **How to get**: Sign up at [OpenAI](https://openai.com/) and generate an API key
- **Required for**: All AI matching and analysis features

### JWT_SECRET_KEY
- **Description**: Secret key for signing JWT tokens
- **Example**: `your-super-secure-secret-key-here`
- **Security**: Use a strong, random string (at least 32 characters)
- **Required for**: User authentication and protected endpoints

## Optional Variables

### DATABASE_URL
- **Description**: Database connection string
- **Default**: `sqlite:///./resume_matcher.db`
- **PostgreSQL Example**: `postgresql://username:password@host:port/database`
- **Usage**: For production, use PostgreSQL; for development, SQLite is fine

### PORT
- **Description**: Port number for the application
- **Default**: `8000`
- **Usage**: Railway will automatically set this; no need to configure manually

## Setting Environment Variables

### For Railway Deployment

1. **Via Railway Dashboard**:
   - Go to your Railway project
   - Navigate to "Variables" tab
   - Add each variable with its value

2. **Via Railway CLI**:
   ```bash
   railway variables set OPENAI_API_KEY=your_key_here
   railway variables set JWT_SECRET_KEY=your_secret_here
   ```

### For Local Development

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=your_secure_jwt_secret_key_here
DATABASE_URL=sqlite:///./resume_matcher.db
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use strong secrets** for JWT_SECRET_KEY
3. **Rotate secrets regularly** in production
4. **Use environment-specific values** (different keys for dev/staging/prod)
5. **Restrict API key permissions** where possible

## Validation

The application will:
- Check for OPENAI_API_KEY on startup and warn if missing
- Use default values for optional variables
- Validate JWT_SECRET_KEY strength (recommended: 32+ characters)

# Railway Deployment Guide

This guide explains how to deploy the AI Resume & Job Matcher backend to Railway.

## Prerequisites

1. A Railway account ([sign up here](https://railway.app/))
2. Railway CLI installed (`npm install -g @railway/cli`)
3. OpenAI API key

## Quick Deployment

### Method 1: GitHub Integration (Recommended)

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Connect to Railway**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the Python project

3. **Configure Environment Variables**:
   - In your Railway project dashboard, go to "Variables"
   - Add the following environment variables:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     JWT_SECRET_KEY=your_secure_jwt_secret_key_here
     DATABASE_URL=postgresql://username:password@host:port/database
     ```

4. **Deploy**:
   - Railway will automatically build and deploy your application
   - The deployment URL will be provided in the dashboard

### Method 2: Railway CLI

1. **Login to Railway**:
   ```bash
   railway login
   ```

2. **Initialize Railway project**:
   ```bash
   railway init
   ```

3. **Set environment variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_api_key_here
   railway variables set JWT_SECRET_KEY=your_secure_jwt_secret_key_here
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | `your-secure-secret-key` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./resume_matcher.db` |
| `PORT` | Port for the application | `8000` |

## Database Configuration

### Using SQLite (Default)
The application uses SQLite by default, which works well for development and small deployments.

### Using PostgreSQL (Recommended for Production)
1. Add PostgreSQL service in Railway:
   - In your Railway project, click "New Service"
   - Select "Database" → "PostgreSQL"
   - Railway will provide the connection string

2. Set the DATABASE_URL environment variable:
   ```
   DATABASE_URL=postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
   ```

## Deployment Files

The following files are included for Railway deployment:

- `railway.json` - Railway configuration
- `Procfile` - Process definition
- `Dockerfile` - Container configuration (alternative deployment method)

## Health Check

The application includes a health check endpoint at `/health` that Railway will use to monitor the service.

## Monitoring

Railway provides built-in monitoring:
- View logs in the Railway dashboard
- Monitor resource usage
- Set up alerts for failures

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

2. **Environment Variable Issues**:
   - Verify all required environment variables are set
   - Check variable names match exactly (case-sensitive)

3. **Database Connection Issues**:
   - Verify DATABASE_URL format
   - Ensure database service is running

4. **OpenAI API Issues**:
   - Verify OPENAI_API_KEY is valid
   - Check API quota and billing

### Viewing Logs

```bash
railway logs
```

### Accessing the Application

Once deployed, your application will be available at:
- Railway will provide a URL like: `https://your-app-name.up.railway.app`
- API documentation: `https://your-app-name.up.railway.app/docs`

## API Endpoints

After deployment, the following endpoints will be available:

- `GET /health` - Health check
- `POST /match/run` - Text-based matching
- `POST /match/upload` - File-based matching
- `POST /ats/validate` - ATS validation
- `POST /ats/optimize` - ATS optimization
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /history` - Analysis history

## Security Considerations

1. **JWT Secret**: Use a strong, random JWT secret key in production
2. **API Keys**: Never commit API keys to version control
3. **CORS**: The application allows all origins by default - restrict in production
4. **Rate Limiting**: Consider implementing rate limiting for production use

## Scaling

Railway automatically handles:
- Load balancing
- SSL certificates
- Auto-scaling based on traffic

For high-traffic applications, consider:
- Upgrading to a paid Railway plan
- Implementing caching
- Using a managed database service

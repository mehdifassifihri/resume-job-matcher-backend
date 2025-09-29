# Render Deployment Guide

This guide will help you deploy the Resume Job Matcher backend to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your OpenAI API key
3. Your GitHub repository connected to Render

## Environment Variables Required

You'll need to set these environment variables in Render:

### Required Variables:
- `OPENAI_API_KEY`: Your OpenAI API key (required for the application to work)
- `JWT_SECRET_KEY`: A secure secret key for JWT tokens (Render can generate this automatically)

### Optional Variables:
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `PORT`: Port number (defaults to 8000)

## Deployment Steps

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** (already done)
2. **Connect your repository to Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository: `resume-job-matcher-backend`

3. **Configure the service:**
   - **Name**: `resume-job-matcher-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m src.main`
   - **Health Check Path**: `/health`

4. **Set Environment Variables:**
   - Go to the "Environment" tab
   - Add the following variables:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `JWT_SECRET_KEY`: Generate a secure random string (or let Render generate it)
     - `DATABASE_URL`: `sqlite:///./resume_matcher.db` (or your preferred database)

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Method 2: Manual Configuration

If you prefer to configure manually without render.yaml:

1. **Create a new Web Service in Render**
2. **Connect your GitHub repository**
3. **Configure the following settings:**
   - **Root Directory**: `/` (leave empty)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m src.main`
   - **Health Check Path**: `/health`

4. **Set Environment Variables** (same as Method 1)

## Post-Deployment

### 1. Test Your Deployment

Once deployed, test your API:

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Test the API
curl -X POST https://your-app-name.onrender.com/match/run \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text here",
    "job_description": "Job description here"
  }'
```

### 2. Monitor Your Application

- Check the Render dashboard for logs and metrics
- Monitor the health check endpoint
- Set up alerts if needed

### 3. Custom Domain (Optional)

If you want a custom domain:
1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Configure DNS as instructed

## Troubleshooting

### Common Issues:

1. **Build Failures:**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

2. **Runtime Errors:**
   - Check environment variables are set correctly
   - Review application logs in Render dashboard

3. **Health Check Failures:**
   - Ensure `/health` endpoint is working
   - Check that the application starts successfully

4. **OpenAI API Issues:**
   - Verify your API key is correct and has sufficient credits
   - Check API rate limits

### Logs and Debugging:

- View logs in the Render dashboard
- Use the "Shell" feature to debug issues
- Check the health endpoint: `https://your-app.onrender.com/health`

## Performance Optimization

### For Production:

1. **Upgrade Plan:**
   - Consider upgrading from the free tier for better performance
   - Free tier has limitations on CPU and memory

2. **Database:**
   - Consider using PostgreSQL instead of SQLite for production
   - Set up a managed database service

3. **Caching:**
   - Implement Redis for caching (requires paid plan)
   - Use in-memory caching for free tier

## Security Considerations

1. **Environment Variables:**
   - Never commit API keys to your repository
   - Use Render's environment variable system

2. **JWT Secret:**
   - Use a strong, random JWT secret key
   - Rotate keys periodically

3. **CORS:**
   - Configure CORS settings for your frontend domain

## Cost Estimation

- **Free Tier**: $0/month (with limitations)
- **Starter Plan**: $7/month (recommended for production)
- **Standard Plan**: $25/month (for higher traffic)

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Application Logs: Available in Render dashboard

---

Your application should now be live at: `https://your-app-name.onrender.com`

# AI Resume & Job Matcher - Deployment Guide

## 🚀 Enterprise Deployment Guide

This comprehensive guide provides detailed instructions for deploying the AI Resume & Job Matcher application in various enterprise environments, from development to production. This premium system is designed for scalability, security, and high-performance commercial use.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [Security Configuration](#security-configuration)
7. [Scaling and Performance](#scaling-and-performance)

## Local Development

### Prerequisites

- Python 3.8+
- OpenAI API key
- Git (optional)

### Setup

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd resume-job-matcher
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Run Application**
   ```bash
   python main.py
   ```

4. **Test Installation**
   ```bash
   curl http://localhost:8000/health
   python samples/test_api.py
   ```

## Docker Deployment

### Single Container Deployment

1. **Build Image**
   ```bash
   docker build -t resume-matcher .
   ```

2. **Run Container**
   ```bash
   docker run -p 8000:8000 \
     -e OPENAI_API_KEY=your-api-key \
     -e DEFAULT_MODEL=gpt-4o-mini \
     resume-matcher
   ```

3. **Test Deployment**
   ```bash
   curl http://localhost:8000/health
   ```

### Docker Compose Deployment

1. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Check Status**
   ```bash
   docker-compose ps
   docker-compose logs resume-matcher
   ```

### Production Docker Compose

For production deployment with Nginx:

```yaml
version: '3.8'

services:
  resume-matcher:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEFAULT_MODEL=${DEFAULT_MODEL:-gpt-4o-mini}
      - DEBUG=false
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - resume-matcher
    restart: unless-stopped
```

## Cloud Deployment

### AWS Deployment

#### Using AWS ECS

1. **Create ECS Cluster**
   ```bash
   aws ecs create-cluster --cluster-name resume-matcher
   ```

2. **Create Task Definition**
   ```json
   {
     "family": "resume-matcher",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "512",
     "memory": "1024",
     "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "resume-matcher",
         "image": "your-account.dkr.ecr.region.amazonaws.com/resume-matcher:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "OPENAI_API_KEY",
             "value": "your-api-key"
           }
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/resume-matcher",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

3. **Create Service**
   ```bash
   aws ecs create-service \
     --cluster resume-matcher \
     --service-name resume-matcher-service \
     --task-definition resume-matcher:1 \
     --desired-count 2 \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
   ```

#### Using AWS Lambda (Serverless)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt -t .
   ```

2. **Create Lambda Function**
   ```python
   # lambda_handler.py
   from mangum import Mangum
   from api import app
   
   handler = Mangum(app)
   ```

3. **Deploy with Serverless Framework**
   ```yaml
   # serverless.yml
   service: resume-matcher
   
   provider:
     name: aws
     runtime: python3.9
     region: us-east-1
     environment:
       OPENAI_API_KEY: ${env:OPENAI_API_KEY}
   
   functions:
     api:
       handler: lambda_handler.handler
       events:
         - http:
             path: /{proxy+}
             method: ANY
             cors: true
   ```

### Google Cloud Platform

#### Using Cloud Run

1. **Build and Push Image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/resume-matcher
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy resume-matcher \
     --image gcr.io/PROJECT-ID/resume-matcher \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your-api-key
   ```

3. **Configure Custom Domain**
   ```bash
   gcloud run domain-mappings create \
     --service resume-matcher \
     --domain api.yourdomain.com \
     --region us-central1
   ```

### Azure Deployment

#### Using Azure Container Instances

1. **Create Resource Group**
   ```bash
   az group create --name resume-matcher-rg --location eastus
   ```

2. **Deploy Container**
   ```bash
   az container create \
     --resource-group resume-matcher-rg \
     --name resume-matcher \
     --image your-registry.azurecr.io/resume-matcher:latest \
     --dns-name-label resume-matcher-api \
     --ports 8000 \
     --environment-variables OPENAI_API_KEY=your-api-key
   ```

#### Using Azure App Service

1. **Create App Service Plan**
   ```bash
   az appservice plan create \
     --name resume-matcher-plan \
     --resource-group resume-matcher-rg \
     --sku B1 \
     --is-linux
   ```

2. **Create Web App**
   ```bash
   az webapp create \
     --resource-group resume-matcher-rg \
     --plan resume-matcher-plan \
     --name resume-matcher-app \
     --deployment-container-image-name your-registry.azurecr.io/resume-matcher:latest
   ```

3. **Configure Environment Variables**
   ```bash
   az webapp config appsettings set \
     --resource-group resume-matcher-rg \
     --name resume-matcher-app \
     --settings OPENAI_API_KEY=your-api-key
   ```

## Production Considerations

### Environment Configuration

1. **Production Environment Variables**
   ```env
   # Production settings
   OPENAI_API_KEY=your-production-api-key
   DEFAULT_MODEL=gpt-4o-mini
   DEBUG=false
   LOG_LEVEL=WARNING
   API_HOST=0.0.0.0
   API_PORT=8000
   
   # Security
   CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
   
   # Performance
   WORKERS=4
   MAX_REQUESTS=1000
   MAX_REQUESTS_JITTER=100
   ```

2. **SSL/TLS Configuration**
   ```nginx
   # nginx.conf
   server {
       listen 443 ssl http2;
       server_name api.yourdomain.com;
       
       ssl_certificate /etc/nginx/ssl/cert.pem;
       ssl_certificate_key /etc/nginx/ssl/key.pem;
       
       location / {
           proxy_pass http://resume-matcher:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

### Database Considerations

While the application is stateless, you might want to add:

1. **Redis for Caching**
   ```yaml
   # docker-compose.yml
   redis:
     image: redis:alpine
     ports:
       - "6379:6379"
     volumes:
       - redis_data:/data
   
   volumes:
     redis_data:
   ```

2. **PostgreSQL for Analytics**
   ```yaml
   # docker-compose.yml
   postgres:
     image: postgres:13
     environment:
       POSTGRES_DB: resume_matcher
       POSTGRES_USER: admin
       POSTGRES_PASSWORD: secure_password
     volumes:
       - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

## Monitoring and Logging

### Application Monitoring

1. **Health Checks**
   ```bash
   # Basic health check
   curl -f http://localhost:8000/health || exit 1
   
   # Detailed health check
   curl -s http://localhost:8000/health | jq '.openai_configured'
   ```

2. **Prometheus Metrics** (Optional)
   ```python
   # Add to api.py
   from prometheus_client import Counter, Histogram, generate_latest
   
   REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
   REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')
   
   @app.get("/metrics")
   def metrics():
       return Response(generate_latest(), media_type="text/plain")
   ```

### Logging Configuration

1. **Structured Logging**
   ```python
   # logging_config.py
   import logging
   import json
   from datetime import datetime
   
   class JSONFormatter(logging.Formatter):
       def format(self, record):
           log_entry = {
               "timestamp": datetime.utcnow().isoformat(),
               "level": record.levelname,
               "logger": record.name,
               "message": record.getMessage(),
               "module": record.module,
               "function": record.funcName,
               "line": record.lineno
           }
           
           if record.exc_info:
               log_entry["exception"] = self.formatException(record.exc_info)
           
           return json.dumps(log_entry)
   
   # Configure logging
   logging.basicConfig(
       level=logging.INFO,
       handlers=[
           logging.StreamHandler(),
           logging.FileHandler("app.log")
       ]
   )
   
   for handler in logging.root.handlers:
       handler.setFormatter(JSONFormatter())
   ```

2. **Log Rotation**
   ```bash
   # logrotate configuration
   /var/log/resume-matcher/*.log {
       daily
       missingok
       rotate 30
       compress
       delaycompress
       notifempty
       create 644 app app
       postrotate
           systemctl reload resume-matcher
       endscript
   }
   ```

## Security Configuration

### API Security

1. **Rate Limiting**
   ```python
   # Add to api.py
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
   
   @app.post("/match/run")
   @limiter.limit("10/minute")
   def match_run(request: Request, req: MatchRequest):
       # ... existing code
   ```

2. **API Key Authentication** (Optional)
   ```python
   # Add to api.py
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   
   security = HTTPBearer()
   
   def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
       if credentials.credentials != "your-api-key":
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid API key"
           )
       return credentials.credentials
   
   @app.post("/match/run")
   def match_run(req: MatchRequest, api_key: str = Depends(verify_api_key)):
       # ... existing code
   ```

### Network Security

1. **Firewall Configuration**
   ```bash
   # UFW (Ubuntu)
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw deny 8000/tcp  # Block direct access to app port
   ufw enable
   ```

2. **Docker Security**
   ```dockerfile
   # Use non-root user
   RUN useradd --create-home --shell /bin/bash app
   USER app
   
   # Remove unnecessary packages
   RUN apt-get update && apt-get install -y --no-install-recommends \
       gcc \
       && rm -rf /var/lib/apt/lists/*
   ```

## Scaling and Performance

### Horizontal Scaling

1. **Load Balancer Configuration**
   ```nginx
   # nginx.conf
   upstream resume_matcher {
       server resume-matcher-1:8000;
       server resume-matcher-2:8000;
       server resume-matcher-3:8000;
   }
   
   server {
       location / {
           proxy_pass http://resume_matcher;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

2. **Kubernetes Deployment**
   ```yaml
   # k8s-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: resume-matcher
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: resume-matcher
     template:
       metadata:
         labels:
           app: resume-matcher
       spec:
         containers:
         - name: resume-matcher
           image: resume-matcher:latest
           ports:
           - containerPort: 8000
           env:
           - name: OPENAI_API_KEY
             valueFrom:
               secretKeyRef:
                 name: openai-secret
                 key: api-key
           resources:
             requests:
               memory: "512Mi"
               cpu: "250m"
             limits:
               memory: "1Gi"
               cpu: "500m"
   ```

### Performance Optimization

1. **Gunicorn Configuration**
   ```python
   # gunicorn.conf.py
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "uvicorn.workers.UvicornWorker"
   worker_connections = 1000
   max_requests = 1000
   max_requests_jitter = 100
   preload_app = True
   ```

2. **Caching Strategy**
   ```python
   # Add to api.py
   from functools import lru_cache
   import hashlib
   
   @lru_cache(maxsize=1000)
   def cached_ats_validation(resume_hash: str, keywords_hash: str):
       # Cache ATS validation results
       pass
   
   def get_cache_key(text: str) -> str:
       return hashlib.md5(text.encode()).hexdigest()
   ```

### Monitoring Performance

1. **Application Metrics**
   ```python
   # metrics.py
   import time
   from functools import wraps
   
   def track_performance(func):
       @wraps(func)
       def wrapper(*args, **kwargs):
           start_time = time.time()
           result = func(*args, **kwargs)
           duration = time.time() - start_time
           
           logger.info(f"{func.__name__} completed in {duration:.2f}s")
           return result
       return wrapper
   ```

2. **System Monitoring**
   ```bash
   # Monitor system resources
   htop
   iotop
   netstat -tulpn
   
   # Monitor application logs
   tail -f /var/log/resume-matcher/app.log
   ```

## Backup and Recovery

### Data Backup

1. **Configuration Backup**
   ```bash
   # Backup configuration files
   tar -czf config-backup-$(date +%Y%m%d).tar.gz \
     .env docker-compose.yml nginx.conf ssl/
   ```

2. **Log Backup**
   ```bash
   # Backup logs
   tar -czf logs-backup-$(date +%Y%m%d).tar.gz /var/log/resume-matcher/
   ```

### Disaster Recovery

1. **Recovery Procedures**
   ```bash
   # Restore from backup
   tar -xzf config-backup-20240101.tar.gz
   docker-compose up -d
   ```

2. **Health Check After Recovery**
   ```bash
   # Verify service is running
   curl -f http://localhost:8000/health
   python samples/test_api.py
   ```

## Troubleshooting

### Common Issues

1. **Service Won't Start**
   ```bash
   # Check logs
   docker-compose logs resume-matcher
   
   # Check configuration
   docker-compose config
   ```

2. **High Memory Usage**
   ```bash
   # Monitor memory
   docker stats
   
   # Restart service
   docker-compose restart resume-matcher
   ```

3. **API Timeouts**
   ```bash
   # Check OpenAI API status
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

### Performance Issues

1. **Slow Response Times**
   - Check OpenAI API latency
   - Monitor system resources
   - Consider upgrading to faster models
   - Implement caching

2. **High Error Rates**
   - Check API key validity
   - Monitor rate limits
   - Review input validation
   - Check file size limits

## Maintenance

### Regular Maintenance Tasks

1. **Weekly Tasks**
   - Review logs for errors
   - Check system resources
   - Update dependencies
   - Backup configurations

2. **Monthly Tasks**
   - Security updates
   - Performance review
   - Capacity planning
   - Disaster recovery testing

3. **Quarterly Tasks**
   - Full system backup
   - Security audit
   - Performance optimization
   - Documentation updates

This deployment guide provides comprehensive instructions for deploying the AI Resume & Job Matcher application in various environments. Choose the deployment method that best fits your needs and infrastructure requirements.

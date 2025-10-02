# AI Resume & Job Matcher - Installation Guide

## 🚀 Premium Installation Guide

This comprehensive guide provides detailed step-by-step instructions for installing and setting up the AI Resume & Job Matcher application. This premium system is designed for enterprise use with production-ready deployment options.

## Prerequisites

Before installing the application, ensure you have the following:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **OpenAI API Key** - [Get API Key](https://platform.openai.com/api-keys)
- **Git** (optional) - [Download Git](https://git-scm.com/downloads)
- **Docker** (optional) - [Download Docker](https://www.docker.com/get-started)

## Installation Methods

### Method 1: Local Installation (Recommended for Development)

#### Step 1: Download the Application

**Option A: Direct Download**
1. Download the application files to your local machine
2. Extract the files to a directory of your choice (e.g., `~/resume-matcher`)

**Option B: Git Clone (if using Git)**
```bash
git clone <repository-url>
cd resume-job-matcher
```

#### Step 2: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   DEFAULT_MODEL=gpt-4o-mini
   ```

#### Step 5: Test the Installation

```bash
python main.py
```

The application should start and display:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Step 6: Verify Installation

Open a new terminal and test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"ok": true}
```

### Method 2: Docker Installation (Recommended for Production)

#### Step 1: Build Docker Image

```bash
docker build -t resume-matcher .
```

#### Step 2: Run Container

```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=your-api-key resume-matcher
```

#### Step 3: Verify Installation

```bash
curl http://localhost:8000/health
```

### Method 3: Docker Compose (Recommended for Production with Nginx)

#### Step 1: Configure Environment

Create a `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key-here
DEFAULT_MODEL=gpt-4o-mini
DEBUG=false
```

#### Step 2: Start Services

```bash
docker-compose up -d
```

#### Step 3: Verify Installation

```bash
curl http://localhost:8000/health
```

## Platform-Specific Instructions

### Windows Installation

1. **Install Python:**
   - Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation: `python --version`

2. **Install Git (optional):**
   - Download from [git-scm.com](https://git-scm.com/download/win)
   - Use default installation options

3. **Follow Method 1 steps above**

### macOS Installation

1. **Install Python:**
   ```bash
   # Using Homebrew (recommended)
   brew install python
   
   # Or download from python.org
   ```

2. **Install Git (optional):**
   ```bash
   brew install git
   ```

3. **Follow Method 1 steps above**

### Linux Installation

#### Ubuntu/Debian:

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install Git (optional)
sudo apt install git

# Follow Method 1 steps above
```

#### CentOS/RHEL:

```bash
# Install Python and pip
sudo yum install python3 python3-pip

# Install Git (optional)
sudo yum install git

# Follow Method 1 steps above
```

## Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Yes |
| `DEFAULT_MODEL` | Default OpenAI model | `gpt-4o-mini` | No |
| `API_HOST` | API host address | `0.0.0.0` | No |
| `API_PORT` | API port number | `8000` | No |
| `DEBUG` | Enable debug mode | `false` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Model Selection

Choose the appropriate OpenAI model based on your needs:

- **gpt-4o-mini** (default): Cost-effective, good quality
- **gpt-4o**: Best quality, higher cost
- **gpt-4-turbo**: Balanced quality and cost
- **gpt-3.5-turbo**: Fastest, lower cost

## Troubleshooting

### Common Issues

#### 1. Python Version Error
```
Error: Python 3.8+ is required
```
**Solution:** Install Python 3.8 or higher

#### 2. OpenAI API Key Error
```
Error: OpenAI API key not configured
```
**Solution:** Set the `OPENAI_API_KEY` environment variable

#### 3. Port Already in Use
```
Error: Port 8000 is already in use
```
**Solution:** 
- Change the port in `.env`: `API_PORT=8001`
- Or stop the process using port 8000

#### 4. Permission Denied (Linux/macOS)
```
Error: Permission denied
```
**Solution:** 
```bash
chmod +x main.py
# Or use sudo if necessary
```

#### 5. Module Not Found
```
Error: No module named 'fastapi'
```
**Solution:** 
```bash
pip install -r requirements.txt
```

#### 6. Docker Build Fails
```
Error: Docker build failed
```
**Solution:** 
- Ensure Docker is running
- Check internet connection
- Try: `docker system prune` to clean up

### Performance Issues

#### Slow Processing
- Use `gpt-4o-mini` model for faster processing
- Ensure stable internet connection
- Check OpenAI API status

#### Memory Issues
- Process smaller files
- Increase server memory
- Use Docker with memory limits

### Getting Help

1. **Check Logs:**
   ```bash
   # Local installation
   python main.py
   
   # Docker installation
   docker logs <container-id>
   ```

2. **Test API:**
   ```bash
   python samples/test_api.py
   ```

3. **Verify Configuration:**
   ```bash
   # Check environment variables
   echo $OPENAI_API_KEY
   
   # Test OpenAI connection
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

## Next Steps

After successful installation:

1. **Test the API** using the provided test script
2. **Read the API Documentation** in `docs/API.md`
3. **Explore sample files** in the `samples/` directory
4. **Configure for production** using Docker or reverse proxy

## Security Considerations

1. **API Key Security:**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **Network Security:**
   - Use HTTPS in production
   - Implement rate limiting
   - Configure firewall rules

3. **Data Privacy:**
   - Files are processed in memory only
   - No persistent storage of user data
   - Consider data residency requirements

## Production Deployment

For production deployment, see the [Deployment Guide](DEPLOYMENT.md) for detailed instructions on:

- Reverse proxy configuration
- SSL/TLS setup
- Monitoring and logging
- Scaling considerations
- Backup strategies

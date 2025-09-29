# Frequently Asked Questions (FAQ)

## General Questions

### What is the AI Resume & Job Matcher?

The AI Resume & Job Matcher is a powerful API service that uses artificial intelligence to analyze resume-job compatibility, generate tailored resumes, and provide user authentication with history tracking. It helps job seekers optimize their resumes and assists recruiters in candidate screening.

### How does it work?

The system uses OpenAI's GPT models to:
1. Parse and structure resume and job description content
2. Calculate compatibility scores based on skills, experience, and requirements
3. Generate optimized resumes tailored to specific job applications
4. Track user analysis history and provide personalized insights

### What file formats are supported?

The system supports:
- **PDF files** - Extracts text using PyPDF
- **DOCX files** - Processes Microsoft Word documents
- **TXT files** - Handles plain text files

### What languages are supported?

The system primarily supports English and French, with automatic language detection. It can process content in other languages but works best with English content.

## Technical Questions

### What are the system requirements?

**Minimum Requirements:**
- Python 3.8 or higher
- 2GB RAM
- 1GB disk space
- Internet connection for OpenAI API

**Recommended Requirements:**
- Python 3.11 or higher
- 4GB RAM
- 2GB disk space
- Stable internet connection

### How long does processing take?

Typical processing times:
- **File upload matching**: 8-20 seconds
- **Authentication**: < 1 second
- **History retrieval**: < 1 second

Processing time depends on:
- File size and complexity
- OpenAI API response time
- Server performance
- Network latency

### What OpenAI models are supported?

Supported models:
- **gpt-4o-mini** (default) - Cost-effective, good quality
- **gpt-4o** - Best quality, higher cost
- **gpt-4-turbo** - Balanced quality and cost
- **gpt-3.5-turbo** - Fastest, lower cost

### How much does it cost to run?

Costs depend on:
- **OpenAI API usage** - Based on model and token usage
- **Server hosting** - Varies by provider
- **Database storage** - Minimal for SQLite
- **Bandwidth** - File upload/download costs

Typical costs:
- **Development**: $5-20/month
- **Production**: $50-200/month
- **Enterprise**: $500+/month

### What authentication methods are supported?

The system supports:
- **JWT Tokens** - JSON Web Tokens for secure authentication
- **User Registration** - Create new user accounts
- **User Login** - Secure login with password hashing
- **Token Refresh** - Refresh access tokens for extended sessions

## API Questions

### What endpoints are available?

**Authentication Endpoints:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Get current user

**Analysis Endpoints:**
- `POST /match/upload` - File upload matching

**History Endpoints:**
- `GET /history/analyses` - Get analysis history
- `GET /history/analyses/{id}` - Get specific analysis
- `POST /history/analyses` - Create analysis record
- `GET /history/payments` - Get payment history
- `GET /history/payments/{id}` - Get specific payment
- `POST /history/payments` - Create payment record

### How do I authenticate with the API?

1. **Register a new user:**
   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "email": "john@example.com", "password": "secure_password"}'
   ```

2. **Login to get tokens:**
   ```bash
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "john@example.com", "password": "secure_password"}'
   ```

3. **Use the access token in requests:**
   ```bash
   curl -X POST "http://localhost:8000/match/upload" \
     -H "Authorization: Bearer <access_token>" \
     -F "resume_file=@resume.pdf" \
     -F "job_file=@job_description.pdf"
   ```

### How do I handle file uploads?

Use the `/match/upload` endpoint with multipart form data:

```python
import requests

url = "http://localhost:8000/match/upload"
headers = {"Authorization": f"Bearer {access_token}"}
files = {
    'resume_file': open('resume.pdf', 'rb'),
    'job_file': open('job_description.pdf', 'rb')
}
data = {'model': 'gpt-4o-mini'}

response = requests.post(url, files=files, data=data, headers=headers)
result = response.json()
```

### How do I get my analysis history?

Use the `/history/analyses` endpoint:

```python
import requests

url = "http://localhost:8000/history/analyses"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)
history = response.json()
```

## Security Questions

### Is my data secure?

Yes, the system implements multiple security measures:
- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - bcrypt encryption for passwords
- **Input Validation** - Comprehensive input sanitization
- **User Isolation** - Each user can only access their own data
- **Secure File Handling** - Temporary files are automatically deleted

### How are passwords stored?

Passwords are securely hashed using bcrypt before storage. The system never stores plain text passwords.

### Can I access other users' data?

No, the system implements strict user isolation. Each user can only access their own analysis history and payment records.

### Are files stored permanently?

No, uploaded files are processed in memory and immediately deleted after processing. Only analysis results are stored in the database.

## Usage Questions

### How do I get started?

1. **Install the application** (see Installation Guide)
2. **Set up environment variables** (OpenAI API key)
3. **Start the server** (`python src/main.py`)
4. **Register a user account**
5. **Upload files for analysis**

### What's the best way to use the API?

1. **Register and login** to get authentication tokens
2. **Upload resume and job description files** using `/match/upload`
3. **Store analysis results** using `/history/analyses`
4. **Retrieve history** when needed using `/history/analyses`

### Can I process multiple files at once?

Currently, the API processes one resume and one job description at a time. For bulk processing, you would need to make multiple API calls.

### How do I handle errors?

The API returns appropriate HTTP status codes:
- **200** - Success
- **400** - Bad Request (invalid input)
- **401** - Unauthorized (invalid token)
- **403** - Forbidden (insufficient permissions)
- **404** - Not Found
- **422** - Validation Error
- **500** - Internal Server Error

## Troubleshooting

### Common Issues

**"OpenAI API key not configured"**
- Set the `OPENAI_API_KEY` environment variable
- Ensure the API key is valid and has sufficient credits

**"Invalid file type"**
- Ensure files are PDF, DOCX, or TXT format
- Check file extensions are correct

**"File too large"**
- Maximum file size is 10MB
- Compress files or split content if needed

**"Authentication failed"**
- Check that the JWT token is valid
- Ensure the token hasn't expired
- Use the refresh token endpoint if needed

### Debug Mode

Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

**Slow processing:**
- Check OpenAI API status
- Verify network connectivity
- Consider using a faster model (gpt-3.5-turbo)

**Memory issues:**
- Reduce file sizes
- Process files individually
- Increase server memory

## Integration Questions

### Can I integrate this with my existing system?

Yes, the API is designed for easy integration:
- **RESTful API** - Standard HTTP methods
- **JSON format** - Standard request/response format
- **CORS support** - Cross-origin requests
- **Comprehensive documentation** - Auto-generated API docs

### What programming languages are supported?

The API can be used with any language that supports HTTP requests:
- **Python** - requests library
- **JavaScript** - fetch API or axios
- **cURL** - Command line
- **Postman** - API testing

### Can I use this in production?

Yes, but consider:
- **Security** - Use HTTPS in production
- **Rate limiting** - Implement rate limiting
- **Monitoring** - Set up logging and monitoring
- **Backup** - Regular database backups
- **Scaling** - Consider load balancing for high traffic

## Support Questions

### Where can I get help?

1. **Documentation** - Check the API documentation
2. **FAQ** - Review this FAQ for common issues
3. **GitHub Issues** - Report bugs and feature requests
4. **Community** - Join our community discussions

### How do I report bugs?

1. **Check existing issues** on GitHub
2. **Create a new issue** with detailed information
3. **Include logs** and error messages
4. **Provide steps to reproduce** the issue

### Can I contribute to the project?

Yes! We welcome contributions:
1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Submit a pull request**

### Is there a roadmap?

Yes, upcoming features include:
- Advanced analytics
- Bulk processing
- Enhanced AI models
- Mobile app support
- Advanced security features
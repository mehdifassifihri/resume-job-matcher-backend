# AI Resume & Job Matcher - Ultra-Light API

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)

A powerful AI-powered resume and job matching system that analyzes resumes against job descriptions, provides compatibility scores, and generates tailored resumes with user authentication and history tracking.

## 🚀 Features

### Core Functionality
- **Intelligent Resume-Job Matching**: Advanced AI analysis of resume compatibility with job requirements
- **Compatibility Scoring**: Detailed scoring system (0-100) with breakdown by skills, responsibilities, and seniority
- **Resume Tailoring**: AI-generated tailored resumes optimized for specific job applications
- **Multi-format Support**: Handles PDF, DOCX, and TXT files for both resumes and job descriptions

### Advanced Features
- **Smart Skill Matching**: Intelligent matching of technical skills with variants and aliases
- **Education Validation**: Validates education extraction against original resume content
- **Safety Checks**: Prevents AI hallucination and maintains factual accuracy
- **Multi-language Support**: Automatic language detection and processing
- **RESTful API**: Clean, well-documented API endpoints for easy integration

### Authentication & User Management
- **JWT Authentication**: Secure token-based authentication system
- **User Registration & Login**: Complete user management with secure password hashing
- **Analysis History**: Track and retrieve all CV analysis history per user
- **Payment History**: Manage and track payment records for premium features
- **Protected Endpoints**: All analysis endpoints require authentication

## 📋 API Endpoints

### Authentication (Public)
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT tokens
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user information

### Analysis (Protected - Requires JWT)
- `POST /match/upload` - Handle file uploads for resume and job description processing

### History (Protected - Requires JWT)
- `GET /history/analyses` - Get user's analysis history
- `GET /history/analyses/{id}` - Get specific analysis details
- `POST /history/analyses` - Create new analysis record
- `GET /history/payments` - Get user's payment history
- `GET /history/payments/{id}` - Get specific payment details
- `POST /history/payments` - Create new payment record

## 🛠️ Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-job-matcher-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file and add your OpenAI API key
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   echo "DEFAULT_MODEL=gpt-4o-mini" >> .env
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

The API will be available at `http://localhost:8000`

## 🔧 Configuration

### Environment Variables

The application uses the following environment variables:

```env
OPENAI_API_KEY=your-openai-api-key-here
DEFAULT_MODEL=gpt-4o-mini
```

You can set these as environment variables or create a `.env` file in the root directory.

### Supported Models
- `gpt-4o-mini` (default, cost-effective)
- `gpt-4o`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

## 📖 Usage

### API Usage

#### 1. User Registration

```python
import requests

url = "http://localhost:8000/auth/register"
data = {
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password"
}

response = requests.post(url, json=data)
result = response.json()
```

#### 2. User Login

```python
import requests

url = "http://localhost:8000/auth/login"
data = {
    "email": "your_email@example.com",
    "password": "your_password"
}

response = requests.post(url, json=data)
tokens = response.json()
access_token = tokens["access_token"]
```

#### 3. File Upload Matching

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

#### 4. Get Analysis History

```python
import requests

url = "http://localhost:8000/history/analyses"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)
history = response.json()
```

### Response Structure

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

## 🎯 Use Cases

### For Job Seekers
- **Resume Optimization**: Tailor your resume for specific job applications
- **Skill Gap Analysis**: Identify missing skills and areas for improvement
- **Compatibility Assessment**: Understand how well you match job requirements

### For Recruiters
- **Candidate Screening**: Quickly assess candidate-job fit
- **Resume Analysis**: Extract structured information from resumes
- **Skill Matching**: Identify candidates with required technical skills

### For HR Departments
- **Bulk Processing**: Process multiple resumes against job descriptions
- **Standardization**: Ensure consistent resume evaluation criteria
- **Integration**: Easy integration with existing HR systems via API

## 🔍 Technical Details

### Architecture
- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications with LLMs
- **OpenAI GPT**: Advanced language models for AI processing
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping
- **JWT**: JSON Web Tokens for secure authentication
- **SQLite**: Lightweight database for user data and history

### Security
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Secure password storage with bcrypt
- **Input Validation**: Comprehensive input validation and sanitization
- **Error Handling**: Secure error handling without information leakage

### Performance
- **Optimized Processing**: 5-15 second processing times
- **Memory Efficient**: Efficient file processing and cleanup
- **Concurrent Support**: Handle multiple requests simultaneously
- **Caching**: Intelligent caching for improved performance

## 📚 Documentation

- [API Documentation](docs/API.md) - Complete API reference
- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Features Overview](docs/FEATURES.md) - Comprehensive feature list
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [FAQ](docs/FAQ.md) - Frequently asked questions

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on how to get started.

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions, please:
1. Check the [FAQ](docs/FAQ.md)
2. Review the [API Documentation](docs/API.md)
3. Open an issue on GitHub

---

**Made with ❤️ for better job matching**
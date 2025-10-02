# AI Resume & Job Matcher - Premium API System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-Commercial-red.svg)](https://codecanyon.net)

## 🚀 Premium AI-Powered Resume & Job Matching System

Transform your recruitment process with our cutting-edge AI-powered resume and job matching API. This premium system analyzes resume-job compatibility with advanced AI, provides detailed compatibility scores, and generates tailored resumes optimized for specific positions.

**Perfect for:** HR departments, recruitment agencies, job boards, career coaching platforms, and SaaS applications.

## ✨ Key Features

### 🎯 Core AI Capabilities
- **Advanced Resume-Job Matching**: GPT-4 powered analysis with 95%+ accuracy
- **Smart Compatibility Scoring**: Detailed 0-100 scoring with skill, experience, and seniority breakdown
- **AI Resume Optimization**: Automatically tailors resumes for specific job applications
- **Multi-format Support**: PDF, DOCX, TXT file processing with intelligent text extraction

### 🔧 Enterprise Features
- **Smart Skill Recognition**: AI-powered skill matching with variants and aliases
- **Education Validation**: Prevents AI hallucination with factual accuracy checks
- **Multi-language Support**: English, French, and automatic language detection
- **RESTful API**: Production-ready API with comprehensive documentation

### 🔐 Security & Management
- **Enterprise Authentication**: JWT-based secure authentication system
- **User Management**: Complete user registration, login, and profile management
- **Analysis History**: Comprehensive tracking and retrieval of all user analyses
- **Payment Integration**: Built-in payment history tracking for premium features
- **API Security**: All endpoints protected with industry-standard security

## 📋 Complete API Reference

### 🔐 Authentication Endpoints
- `POST /auth/register` - User registration with secure password hashing
- `POST /auth/login` - JWT token authentication
- `POST /auth/refresh` - Token refresh for extended sessions
- `GET /auth/me` - Get authenticated user profile

### 🎯 Analysis Endpoints (Premium Features)
- `POST /match/upload` - AI-powered resume-job matching with file upload

### 📊 History & Analytics (Protected)
- `GET /history/analyses` - Retrieve user's complete analysis history
- `GET /history/analyses/{id}` - Get detailed analysis results
- `POST /history/analyses` - Save analysis results
- `GET /history/payments` - Payment transaction history
- `GET /history/payments/{id}` - Detailed payment information
- `POST /history/payments` - Record payment transactions

## 🛠️ Installation & Setup

### ⚡ Quick Start (5 Minutes)

1. **Download & Extract**
   ```bash
   # Extract the downloaded package
   unzip ai-resume-matcher.zip
   cd ai-resume-matcher
   ```

2. **Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   echo "DEFAULT_MODEL=gpt-4o-mini" >> .env
   ```

4. **Launch Application**
   ```bash
   python src/main.py
   ```

✅ **API Ready**: `http://localhost:8000` | 📚 **Documentation**: `http://localhost:8000/docs`

## ⚙️ Configuration

### 🔑 Required Environment Variables

```env
# OpenAI API Configuration (Required)
OPENAI_API_KEY=your-openai-api-key-here
DEFAULT_MODEL=gpt-4o-mini

# Optional Configuration
DEBUG=false
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

### 🤖 Supported AI Models

| Model | Use Case | Cost | Quality | Speed |
|-------|----------|------|---------|-------|
| `gpt-4o-mini` | **Default** | Low | High | Fast |
| `gpt-4o` | Premium | High | Excellent | Medium |
| `gpt-4-turbo` | Balanced | Medium | High | Medium |
| `gpt-3.5-turbo` | Budget | Very Low | Good | Very Fast |

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

## 🎯 Perfect For

### 🏢 **Enterprise HR Departments**
- **Automated Candidate Screening**: Process hundreds of resumes in minutes
- **Standardized Evaluation**: Consistent, unbiased resume assessment
- **Integration Ready**: Seamlessly integrate with existing HR systems
- **Cost Reduction**: Reduce manual screening time by 80%

### 🎯 **Recruitment Agencies**
- **Enhanced Candidate Matching**: AI-powered compatibility scoring
- **Client Presentations**: Professional analysis reports for clients
- **Scalable Operations**: Handle multiple clients simultaneously
- **Competitive Advantage**: Offer cutting-edge AI-powered services

### 💼 **Job Boards & Platforms**
- **Premium Features**: Add AI matching as a paid feature
- **User Engagement**: Increase platform usage with valuable tools
- **Revenue Generation**: Monetize through premium subscriptions
- **API Integration**: Easy integration with existing platforms

### 🎓 **Career Coaching Services**
- **Resume Optimization**: Help clients improve their resumes
- **Skill Gap Analysis**: Identify areas for professional development
- **Client Value**: Provide data-driven career advice
- **Service Differentiation**: Stand out with AI-powered insights

## 🔧 Technical Specifications

### 🏗️ **Architecture & Technology Stack**
- **FastAPI**: High-performance async web framework
- **OpenAI GPT-4**: State-of-the-art language models
- **LangChain**: Advanced LLM integration framework
- **SQLAlchemy**: Enterprise-grade ORM with SQLite
- **JWT Security**: Industry-standard authentication
- **Pydantic**: Robust data validation and serialization

### 🔒 **Enterprise Security**
- **JWT Authentication**: Secure token-based access control
- **bcrypt Password Hashing**: Military-grade password encryption
- **Input Validation**: Comprehensive sanitization and validation
- **CORS Protection**: Configurable cross-origin security
- **Error Handling**: Secure error responses without data leakage

### ⚡ **Performance & Scalability**
- **Lightning Fast**: 8-20 second processing times
- **Memory Optimized**: Efficient file processing with automatic cleanup
- **Concurrent Processing**: Handle multiple requests simultaneously
- **Production Ready**: Docker support with load balancing
- **Scalable Architecture**: Horizontal scaling capabilities

## 📚 Complete Documentation Package

### 📖 **Included Documentation**
- **[API Documentation](docs/API.md)** - Complete API reference with examples
- **[Installation Guide](docs/INSTALLATION.md)** - Step-by-step setup instructions
- **[Features Overview](docs/FEATURES.md)** - Comprehensive feature documentation
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment strategies
- **[FAQ](docs/FAQ.md)** - Frequently asked questions and troubleshooting

### 🚀 **What You Get**
- ✅ **Complete Source Code** - Fully documented and ready for customization
- ✅ **Production-Ready API** - Enterprise-grade FastAPI implementation
- ✅ **Comprehensive Documentation** - 5 detailed guides included
- ✅ **Docker Support** - Ready for containerized deployment
- ✅ **Security Best Practices** - JWT authentication and data protection
- ✅ **Scalable Architecture** - Built for enterprise-level usage

## 💼 Commercial License

This is a **premium commercial product** available on CodeCanyon. 

### 📋 **License Includes:**
- ✅ **Single Use License** - Use in one project
- ✅ **Commercial Use** - Use in commercial applications
- ✅ **Modification Rights** - Customize and extend the code
- ✅ **6 Months Support** - Direct support from the developer
- ✅ **Free Updates** - Receive updates for 6 months

### 🚫 **License Restrictions:**
- ❌ No redistribution of source code
- ❌ No resale of the product
- ❌ No use in competing products

## 🆘 Premium Support

### 📞 **Support Channels**
1. **Email Support** - Direct developer support via CodeCanyon
2. **Documentation** - Comprehensive guides and examples
3. **Code Comments** - Well-documented source code
4. **Community** - Access to user community (if available)

### 🛠️ **Support Includes**
- Installation assistance
- Configuration help
- API integration support
- Bug fixes and updates
- Customization guidance

---

## 🎯 **Ready to Transform Your Recruitment Process?**

This premium AI-powered resume and job matching system will revolutionize how you handle candidate screening and resume optimization. Get started today and experience the power of AI-driven recruitment!

**⭐ Purchase on CodeCanyon for instant access to this powerful system!**
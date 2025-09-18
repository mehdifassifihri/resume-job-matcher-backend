# AI Resume & Job Matcher - Ultra-Light API

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful AI-powered resume and job matching system that analyzes resumes against job descriptions, provides compatibility scores, generates tailored resumes, and validates ATS (Applicant Tracking System) compliance.

## 🚀 Features

### Core Functionality
- **Intelligent Resume-Job Matching**: Advanced AI analysis of resume compatibility with job requirements
- **Compatibility Scoring**: Detailed scoring system (0-100) with breakdown by skills, responsibilities, and seniority
- **Resume Tailoring**: AI-generated tailored resumes optimized for specific job applications
- **ATS Validation**: Comprehensive ATS compliance checking and optimization
- **Multi-format Support**: Handles PDF, DOCX, and TXT files for both resumes and job descriptions

### Advanced Features
- **Smart Skill Matching**: Intelligent matching of technical skills with variants and aliases
- **Education Validation**: Validates education extraction against original resume content
- **Safety Checks**: Prevents AI hallucination and maintains factual accuracy
- **Multi-language Support**: Automatic language detection and processing
- **RESTful API**: Clean, well-documented API endpoints for easy integration

### API Endpoints
- `POST /match/run` - Process text-based resume and job description matching
- `POST /match/upload` - Handle file uploads for resume and job description processing
- `POST /ats/validate` - Validate resume for ATS compatibility
- `POST /ats/optimize` - Optimize resume for ATS systems
- `GET /health` - Health check endpoint

## 📋 Requirements

- Python 3.8 or higher
- OpenAI API key
- Internet connection for AI processing

## 🛠️ Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-job-matcher
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r assets/requirements.txt
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

## 🚀 Deployment

### Render (Recommended)

1. **Fork this repository** to your GitHub account

2. **Create a Render account** at [render.com](https://render.com)

3. **Create a new Web Service**:
   - Connect your GitHub repository
   - Choose "Web Service"
   - Use the following settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python src/main.py`
     - **Environment**: `Python 3`
     - **Plan**: Free

4. **Set Environment Variables** in Render dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DEFAULT_MODEL`: `gpt-4o-mini`
   - `PORT`: `10000`

5. **Deploy**: Render will automatically deploy your app

Your API will be available at `https://your-app-name.onrender.com`

### Railway (Alternative)

Railway has timeout limitations for long-running requests. For APIs that take 1-2 minutes to process, consider using Render instead.

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

#### 1. Text-based Matching

```python
import requests

url = "http://localhost:8000/match/run"
data = {
    "resume_text": "Your resume text here...",
    "job_text": "Job description text here...",
    "model": "gpt-4o-mini"
}

response = requests.post(url, json=data)
result = response.json()

print(f"Compatibility Score: {result['score']}")
print(f"Tailored Resume: {result['tailored_resume_text']}")
```

#### 2. File Upload Matching

```python
import requests

url = "http://localhost:8000/match/upload"
files = {
    'resume_file': open('resume.pdf', 'rb'),
    'job_file': open('job_description.pdf', 'rb')
}
data = {'model': 'gpt-4o-mini'}

response = requests.post(url, files=files, data=data)
result = response.json()
```

#### 3. ATS Validation

```python
import requests

url = "http://localhost:8000/ats/validate"
data = {
    'resume_text': 'Your resume text...',
    'job_keywords': 'Python, React, AWS, Docker'
}

response = requests.post(url, data=data)
ats_result = response.json()

print(f"ATS Score: {ats_result['score']}")
print(f"Compliance Level: {ats_result['compliance_level']}")
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
- **ATS Compliance**: Ensure your resume passes through ATS systems
- **Compatibility Assessment**: Understand how well you match job requirements

### For Recruiters
- **Candidate Screening**: Quickly assess candidate-job fit
- **Resume Analysis**: Extract structured information from resumes
- **Skill Matching**: Identify candidates with required technical skills
- **ATS Validation**: Ensure candidate resumes are ATS-compliant

### For HR Departments
- **Bulk Processing**: Process multiple resumes against job descriptions
- **Standardization**: Ensure consistent resume evaluation criteria
- **Integration**: Easy integration with existing HR systems via API

## 🔍 Technical Details

### Architecture
- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications with LLMs
- **OpenAI GPT**: Advanced language model for text processing
- **Pydantic**: Data validation and settings management
- **PyPDF/DOCX**: Document parsing and text extraction

### Processing Pipeline
1. **Input Normalization**: Clean and standardize input text
2. **Document Parsing**: Extract text from PDF, DOCX, or TXT files
3. **Job Description Analysis**: Parse and structure job requirements
4. **Resume Analysis**: Extract candidate information and skills
5. **Matching Algorithm**: Calculate compatibility scores
6. **Resume Tailoring**: Generate optimized resume content
7. **ATS Validation**: Check and optimize for ATS compliance
8. **Safety Checks**: Validate output for accuracy and appropriateness

### Supported File Formats
- **Resumes**: PDF, DOCX, TXT
- **Job Descriptions**: PDF, DOCX, TXT
- **Languages**: English, French, and other languages (auto-detected)

## 🛡️ Security & Privacy

- **No Data Storage**: Files are processed in memory and immediately deleted
- **API Key Security**: Secure handling of OpenAI API keys
- **Input Validation**: Comprehensive validation of all inputs
- **Error Handling**: Graceful error handling with informative messages

## 📊 Performance

- **Processing Time**: Typically 5-15 seconds per resume-job pair
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Memory Usage**: Optimized for minimal memory footprint
- **Scalability**: Designed for horizontal scaling

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```
   Error: OpenAI API key not configured
   Solution: Set OPENAI_API_KEY environment variable
   ```

2. **File Upload Issues**
   ```
   Error: Unsupported file format
   Solution: Use PDF, DOCX, or TXT files only
   ```

3. **Memory Issues**
   ```
   Error: Out of memory
   Solution: Process smaller files or increase server memory
   ```

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export DEBUG=true
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the [FAQ](FAQ.md) for common questions
- Review the [API Documentation](docs/API.md)

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Core resume-job matching functionality
- ATS validation and optimization
- Multi-format file support
- RESTful API endpoints

## 🏆 Acknowledgments

- OpenAI for providing the GPT models
- FastAPI team for the excellent web framework
- LangChain for LLM application framework
- The open-source community for various dependencies

---

**Made with ❤️ for the job matching community**

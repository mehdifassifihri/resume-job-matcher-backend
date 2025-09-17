# API Documentation

## Overview

The AI Resume & Job Matcher API provides endpoints for analyzing resume-job compatibility, generating tailored resumes, and validating ATS compliance. All endpoints return JSON responses and support CORS for cross-origin requests.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. However, you need a valid OpenAI API key configured in your environment.

## Endpoints

### 1. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "ok": true
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/health"
```

---

### 2. Text-based Matching

Process resume and job description text for compatibility analysis.

**Endpoint:** `POST /match/run`

**Request Body:**
```json
{
  "resume_text": "string (optional)",
  "job_text": "string (optional)",
  "resume_file_path": "string (optional)",
  "job_file_path": "string (optional)",
  "model": "string (default: gpt-4o-mini)"
}
```

**Parameters:**
- `resume_text`: Raw resume text content
- `job_text`: Raw job description text content
- `resume_file_path`: Path to resume file (PDF, DOCX, TXT)
- `job_file_path`: Path to job description file (PDF, DOCX, TXT)
- `model`: OpenAI model to use (gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo)

**Response:**
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

**Example:**
```bash
curl -X POST "http://localhost:8000/match/run" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Smith\nSoftware Engineer...",
    "job_text": "Senior Full-Stack Developer...",
    "model": "gpt-4o-mini"
  }'
```

---

### 3. File Upload Matching

Process uploaded resume and job description files.

**Endpoint:** `POST /match/upload`

**Request:** Multipart form data

**Parameters:**
- `resume_file`: Resume file (PDF, DOCX, TXT) - required
- `job_file`: Job description file (PDF, DOCX, TXT) - required
- `model`: OpenAI model to use (default: gpt-4o-mini)

**Response:** Same as `/match/run`

**Example:**
```bash
curl -X POST "http://localhost:8000/match/upload" \
  -F "resume_file=@resume.pdf" \
  -F "job_file=@job_description.pdf" \
  -F "model=gpt-4o-mini"
```

**Python Example:**
```python
import requests

files = {
    'resume_file': open('resume.pdf', 'rb'),
    'job_file': open('job_description.pdf', 'rb')
}
data = {'model': 'gpt-4o-mini'}

response = requests.post('http://localhost:8000/match/upload', files=files, data=data)
result = response.json()
```

---

### 4. ATS Validation

Validate resume for ATS (Applicant Tracking System) compatibility.

**Endpoint:** `POST /ats/validate`

**Request:** Form data

**Parameters:**
- `resume_text`: Resume text to validate - required
- `job_keywords`: Comma-separated job keywords (optional)

**Response:**
```json
{
  "compliance_level": "good",
  "score": 78.5,
  "issues": [
    "No clear contact information found",
    "Few quantified achievements - add more metrics and numbers"
  ],
  "recommendations": [
    "Include specific numbers, percentages, and metrics in your achievements",
    "Start bullet points with strong action verbs"
  ],
  "keyword_density": {
    "Python": 2.1,
    "JavaScript": 1.8,
    "React": 1.5
  },
  "structure_score": 85.0,
  "formatting_score": 72.0
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/ats/validate" \
  -F "resume_text=John Smith\nSoftware Engineer..." \
  -F "job_keywords=Python,JavaScript,React,AWS"
```

---

### 5. ATS Optimization

Optimize resume for ATS compatibility.

**Endpoint:** `POST /ats/optimize`

**Request:** Form data

**Parameters:**
- `resume_text`: Resume text to optimize - required
- `job_keywords`: Comma-separated job keywords - required

**Response:**
```json
{
  "optimized_resume": "Optimized resume content...",
  "original_length": 2450,
  "optimized_length": 2380,
  "keywords_integrated": 8
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/ats/optimize" \
  -F "resume_text=John Smith\nSoftware Engineer..." \
  -F "job_keywords=Python,JavaScript,React,AWS,Docker"
```

## Response Fields

### Match Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `score` | float | Overall compatibility score (0-100) |
| `coverage` | object | Detailed coverage breakdown |
| `coverage.must_have` | float | Must-have skills coverage percentage |
| `coverage.responsibilities` | float | Responsibilities coverage percentage |
| `coverage.seniority_fit` | float | Seniority fit percentage |
| `gaps` | object | Analysis of gaps and matches |
| `gaps.matched_skills` | array | Skills that match job requirements |
| `gaps.missing_skills` | array | Skills missing from resume |
| `gaps.weak_evidence_for_responsibilities` | array | Responsibilities with weak evidence |
| `rationale` | string | Explanation of the score |
| `tailored_resume_text` | string | AI-generated tailored resume |
| `recommendations` | array | Actionable improvement suggestions |
| `flags` | array | Warning flags for potential issues |
| `meta` | object | Metadata about the processing |

### ATS Validation Fields

| Field | Type | Description |
|-------|------|-------------|
| `compliance_level` | string | ATS compliance level (excellent/good/fair/poor) |
| `score` | float | Overall ATS score (0-100) |
| `issues` | array | List of ATS compliance issues |
| `recommendations` | array | Suggestions for improvement |
| `keyword_density` | object | Keyword density analysis |
| `structure_score` | float | Resume structure score (0-100) |
| `formatting_score` | float | Resume formatting score (0-100) |

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "detail": "Invalid request parameters"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error processing request: OpenAI API key not configured"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider implementing rate limiting based on your needs.

## File Size Limits

- Maximum file size: 10MB per file
- Supported formats: PDF, DOCX, TXT
- Files are processed in memory and immediately deleted

## Processing Time

Typical processing times:
- Text-based matching: 5-15 seconds
- File upload matching: 8-20 seconds
- ATS validation: 2-5 seconds
- ATS optimization: 3-8 seconds

## Best Practices

1. **Use appropriate models**: `gpt-4o-mini` for cost-effectiveness, `gpt-4o` for best quality
2. **Provide clean text**: Remove formatting artifacts for better processing
3. **Include relevant keywords**: For ATS validation, provide job-specific keywords
4. **Handle errors gracefully**: Always check response status codes
5. **Respect rate limits**: Implement appropriate delays between requests

## SDK Examples

### Python SDK

```python
import requests
import json

class ResumeMatcherAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self):
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def match_text(self, resume_text, job_text, model="gpt-4o-mini"):
        data = {
            "resume_text": resume_text,
            "job_text": job_text,
            "model": model
        }
        response = requests.post(f"{self.base_url}/match/run", json=data)
        return response.json()
    
    def match_files(self, resume_file, job_file, model="gpt-4o-mini"):
        files = {
            'resume_file': open(resume_file, 'rb'),
            'job_file': open(job_file, 'rb')
        }
        data = {'model': model}
        response = requests.post(f"{self.base_url}/match/upload", files=files, data=data)
        files['resume_file'].close()
        files['job_file'].close()
        return response.json()
    
    def validate_ats(self, resume_text, job_keywords=""):
        data = {
            'resume_text': resume_text,
            'job_keywords': job_keywords
        }
        response = requests.post(f"{self.base_url}/ats/validate", data=data)
        return response.json()
    
    def optimize_ats(self, resume_text, job_keywords):
        data = {
            'resume_text': resume_text,
            'job_keywords': job_keywords
        }
        response = requests.post(f"{self.base_url}/ats/optimize", data=data)
        return response.json()

# Usage
api = ResumeMatcherAPI()
result = api.match_text("resume text...", "job description...")
print(f"Score: {result['score']}")
```

### JavaScript SDK

```javascript
class ResumeMatcherAPI {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async healthCheck() {
        const response = await fetch(`${this.baseUrl}/health`);
        return await response.json();
    }
    
    async matchText(resumeText, jobText, model = 'gpt-4o-mini') {
        const response = await fetch(`${this.baseUrl}/match/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_text: resumeText,
                job_text: jobText,
                model: model
            })
        });
        return await response.json();
    }
    
    async matchFiles(resumeFile, jobFile, model = 'gpt-4o-mini') {
        const formData = new FormData();
        formData.append('resume_file', resumeFile);
        formData.append('job_file', jobFile);
        formData.append('model', model);
        
        const response = await fetch(`${this.baseUrl}/match/upload`, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    }
    
    async validateATS(resumeText, jobKeywords = '') {
        const formData = new FormData();
        formData.append('resume_text', resumeText);
        formData.append('job_keywords', jobKeywords);
        
        const response = await fetch(`${this.baseUrl}/ats/validate`, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    }
    
    async optimizeATS(resumeText, jobKeywords) {
        const formData = new FormData();
        formData.append('resume_text', resumeText);
        formData.append('job_keywords', jobKeywords);
        
        const response = await fetch(`${this.baseUrl}/ats/optimize`, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    }
}

// Usage
const api = new ResumeMatcherAPI();
api.matchText('resume text...', 'job description...')
    .then(result => console.log(`Score: ${result.score}`))
    .catch(error => console.error('Error:', error));
```

## Testing

Use the provided test script to verify API functionality:

```bash
python samples/test_api.py
```

This will test all endpoints with sample data and provide detailed output about the results.

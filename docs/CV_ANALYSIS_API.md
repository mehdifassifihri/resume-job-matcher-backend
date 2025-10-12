# CV Analysis API Documentation

Complete guide for integrating CV analysis in your frontend application.

## Base URL
```
http://localhost:8000
```

---

## Analyze CV Endpoint

**Endpoint:** `POST /match/upload`

**Description:** Analyzes a resume against a job description using AI. Can be used with or without authentication.

### Request Parameters

**Form Data:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resume_file` | File | ✅ Yes | Resume file (PDF, DOCX, or TXT) |
| `job_description` | String | ✅ Yes | Job description text |
| `model` | String | ❌ No | OpenAI model to use (default: `gpt-4o-mini`) |
| `user_id` | Integer | ❌ No | User ID (if provided, analysis is saved to history) |

**File Constraints:**
- **Allowed formats:** PDF, DOCX, TXT
- **Maximum size:** 10 MB
- **Encoding:** UTF-8 recommended

### Two Usage Modes

#### 1. Anonymous Mode (No Authentication Required)

Use this mode for users who are not logged in. Analysis results are returned but **not saved**.

```javascript
const formData = new FormData();
formData.append('resume_file', resumeFile); // File object
formData.append('job_description', jobDescriptionText);
formData.append('model', 'gpt-4o-mini'); // optional

const response = await fetch('http://localhost:8000/match/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

#### 2. Authenticated Mode (With user_id)

Use this mode for logged-in users. Analysis results are **automatically saved** to user's history.

```javascript
const formData = new FormData();
formData.append('resume_file', resumeFile); // File object
formData.append('job_description', jobDescriptionText);
formData.append('model', 'gpt-4o-mini'); // optional
formData.append('user_id', userId); // ← Include user_id to save to history

const response = await fetch('http://localhost:8000/match/upload', {
  method: 'POST',
  body: formData
});

const result = await response.json();
// Analysis is automatically saved to user's history!
```

### Success Response (200)

```json
{
  "score": 73.0,
  "coverage": {
    "must_have": 90.0,
    "responsibilities": 0.0,
    "seniority_fit": 100.0
  },
  "gaps": {
    "matched_skills": ["python", "fastapi", "docker"],
    "missing_skills": ["kubernetes"],
    "weak_evidence_for_responsibilities": []
  },
  "rationale": "Core skills coverage 90%, responsibilities 0%, seniority fit 100%.",
  "tailored_resume_text": "John Doe\nSoftware Engineer\n\nEXPERIENCE...",
  "structured_resume": {
    "contact_info": {},
    "summary": "Results-driven Senior Python Developer...",
    "experience": [...],
    "education": [...],
    "skills": {...}
  },
  "recommendations": [
    "Consider obtaining a certification in Kubernetes",
    "Expand experience with container orchestration"
  ],
  "flags": [],
  "meta": {
    "detected_language": "en"
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `score` | Float | Overall compatibility score (0-100) |
| `coverage.must_have` | Float | Core skills match percentage |
| `coverage.responsibilities` | Float | Responsibilities match percentage |
| `coverage.seniority_fit` | Float | Seniority level match percentage |
| `gaps.matched_skills` | Array | Skills found in resume |
| `gaps.missing_skills` | Array | Skills missing from resume |
| `rationale` | String | Brief explanation of the score |
| `tailored_resume_text` | String | Optimized resume text |
| `structured_resume` | Object | Parsed and structured resume data |
| `recommendations` | Array | Suggestions for improvement |
| `flags` | Array | Any warning flags |
| `meta.detected_language` | String | Detected resume language |

### Error Responses

**400 Bad Request - Invalid file type:**
```json
{
  "detail": "Unsupported resume file type: .exe. Supported types: PDF, DOCX, TXT"
}
```

**400 Bad Request - File too large:**
```json
{
  "detail": "Resume file too large: 15000000 bytes. Maximum size: 10MB"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error processing files: [error message]"
}
```

---

## Get Analysis History

**Endpoint:** `GET /history/analyses/{user_id}`

**Description:** Retrieve all analysis history for a specific user.

**Authentication:** Required (Bearer token)

### Request

```javascript
const response = await fetch(`http://localhost:8000/history/analyses/${userId}`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const history = await response.json();
```

### Success Response (200)

```json
[
  {
    "id": 1,
    "tailored_resume": "Optimized resume text...",
    "job_text": "Job description text...",
    "score": 73.0,
    "created_at": "2025-10-11T10:30:00"
  },
  {
    "id": 2,
    "tailored_resume": "Another resume...",
    "job_text": "Another job...",
    "score": 85.5,
    "created_at": "2025-10-11T12:15:00"
  }
]
```

---

## Complete Frontend Integration Example

### React Component Example

```javascript
import React, { useState } from 'react';

function CVAnalyzer({ userId, isLoggedIn }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a PDF, DOCX, or TXT file');
      return;
    }
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }
    
    setResumeFile(file);
    setError('');
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('resume_file', resumeFile);
      formData.append('job_description', jobDescription);
      formData.append('model', 'gpt-4o-mini');
      
      // Include user_id if user is logged in
      if (isLoggedIn && userId) {
        formData.append('user_id', userId);
      }
      
      const response = await fetch('http://localhost:8000/match/upload', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }
      
      const data = await response.json();
      setResult(data);
      
      if (isLoggedIn && userId) {
        alert('Analysis saved to your history!');
      }
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="cv-analyzer">
      <h2>CV Analysis</h2>
      
      {!isLoggedIn && (
        <div className="warning">
          ⚠️ You're not logged in. Analysis results won't be saved.
        </div>
      )}
      
      <form onSubmit={handleAnalyze}>
        <div className="form-group">
          <label>Upload Resume (PDF, DOCX, or TXT)</label>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.docx,.txt"
            required
          />
        </div>
        
        <div className="form-group">
          <label>Job Description</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            rows="10"
            required
          />
        </div>
        
        {error && <div className="error">{error}</div>}
        
        <button type="submit" disabled={loading || !resumeFile}>
          {loading ? 'Analyzing...' : 'Analyze CV'}
        </button>
      </form>
      
      {result && (
        <div className="results">
          <h3>Analysis Results</h3>
          
          <div className="score">
            <h4>Compatibility Score: {result.score}%</h4>
            <div className="score-bar">
              <div 
                className="score-fill" 
                style={{width: `${result.score}%`}}
              />
            </div>
          </div>
          
          <div className="coverage">
            <h4>Coverage Breakdown:</h4>
            <ul>
              <li>Core Skills: {result.coverage.must_have}%</li>
              <li>Responsibilities: {result.coverage.responsibilities}%</li>
              <li>Seniority Fit: {result.coverage.seniority_fit}%</li>
            </ul>
          </div>
          
          <div className="skills">
            <h4>Matched Skills:</h4>
            <div className="skill-tags">
              {result.gaps.matched_skills.map((skill, i) => (
                <span key={i} className="skill-tag matched">{skill}</span>
              ))}
            </div>
            
            {result.gaps.missing_skills.length > 0 && (
              <>
                <h4>Missing Skills:</h4>
                <div className="skill-tags">
                  {result.gaps.missing_skills.map((skill, i) => (
                    <span key={i} className="skill-tag missing">{skill}</span>
                  ))}
                </div>
              </>
            )}
          </div>
          
          <div className="recommendations">
            <h4>Recommendations:</h4>
            <ul>
              {result.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </div>
          
          <div className="tailored-resume">
            <h4>Tailored Resume:</h4>
            <pre>{result.tailored_resume_text}</pre>
            <button onClick={() => {
              navigator.clipboard.writeText(result.tailored_resume_text);
              alert('Copied to clipboard!');
            }}>
              Copy to Clipboard
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default CVAnalyzer;
```

### History Component Example

```javascript
import React, { useState, useEffect } from 'react';

function AnalysisHistory({ userId, accessToken }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, [userId]);

  const fetchHistory = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/history/analyses/${userId}`,
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        }
      );
      
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }
      
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading history...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="analysis-history">
      <h2>Your Analysis History</h2>
      
      {history.length === 0 ? (
        <p>No analyses yet. Start by analyzing your first CV!</p>
      ) : (
        <div className="history-list">
          {history.map((analysis) => (
            <div key={analysis.id} className="history-item">
              <div className="history-header">
                <h3>Analysis #{analysis.id}</h3>
                <span className="date">
                  {new Date(analysis.created_at).toLocaleDateString()}
                </span>
              </div>
              
              <div className="history-details">
                <p><strong>Score:</strong> {analysis.score}%</p>
                <p><strong>Job Description:</strong></p>
                <p className="job-preview">{analysis.job_text.substring(0, 200)}...</p>
                <p><strong>Tailored Resume:</strong></p>
                <pre className="resume-preview">
                  {analysis.tailored_resume.substring(0, 300)}...
                </pre>
              </div>
              
              <button onClick={() => {
                // View full details or download
                console.log('View analysis', analysis.id);
              }}>
                View Full Analysis
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AnalysisHistory;
```

---

## Important Notes

### User Flow Recommendations

1. **For Anonymous Users:**
   - Allow CV analysis without login
   - Show notification: "Sign up to save your analyses"
   - Provide option to register after seeing results

2. **For Logged-In Users:**
   - Automatically include `user_id` in analysis requests
   - Show "Analysis saved!" confirmation
   - Provide easy access to history

### Best Practices

1. **File Validation:**
   - Validate file type and size on frontend before upload
   - Show clear error messages for invalid files

2. **User Experience:**
   - Show loading indicator during analysis (takes 5-15 seconds)
   - Display results in a clear, visually appealing format
   - Provide option to copy or download tailored resume

3. **History Management:**
   - Allow users to view, download, or delete past analyses
   - Implement pagination for users with many analyses
   - Show analysis date and score in list view

4. **Error Handling:**
   - Handle network errors gracefully
   - Show user-friendly error messages
   - Provide retry option for failed analyses

---

## API Endpoints Summary

| Endpoint | Method | Auth Required | Purpose |
|----------|--------|---------------|---------|
| `/match/upload` | POST | ❌ No | Analyze CV (saves if `user_id` provided) |
| `/history/analyses/{user_id}` | GET | ✅ Yes | Get user's analysis history |
| `/auth/register` | POST | ❌ No | Register new user |
| `/auth/login` | POST | ❌ No | Login user |

---

## Testing

Test the API using the provided test script:

```bash
python test_cv_analysis_with_userid.py
```

This will test both anonymous and authenticated analysis modes.

---

For more information:
- [Authentication API Documentation](./AUTH_API.md)
- [Quick Reference Guide](./API_QUICK_REFERENCE.md)
- [Interactive API Docs](http://localhost:8000/docs)



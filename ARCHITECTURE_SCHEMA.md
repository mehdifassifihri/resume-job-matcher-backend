# Resume-Job Matcher Architecture Schema

## System Overview
This is an AI-powered resume and job matching system that uses OpenAI's GPT models to analyze, match, and optimize resumes for specific job descriptions with ATS (Applicant Tracking System) compliance.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI APPLICATION LAYER                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  main.py                    │  api.py                                           │
│  ├─ Entry Point            │  ├─ /match/run (text input)                      │
│  ├─ Uvicorn Server         │  ├─ /match/upload (file upload)                   │
│  └─ Port 8000              │  ├─ /ats/validate                                │
│                            │  ├─ /ats/optimize                                │
│                            │  └─ /health                                      │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PIPELINE ORCHESTRATION                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│  pipeline.py                                                                     │
│  ├─ run_pipeline()                                                              │
│  ├─ Input Normalization                                                         │
│  ├─ Job Description Parsing                                                     │
│  ├─ CV Parsing                                                                  │
│  ├─ Matching & Scoring                                                          │
│  ├─ Resume Tailoring                                                            │
│  ├─ ATS Validation                                                              │
│  └─ Result Assembly                                                             │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATA PROCESSING LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│  parsers.py                    │  matcher.py                   │  tailor.py      │
│  ├─ parse_jd()                │  ├─ match_and_score()         │  ├─ tailor_resume() │
│  ├─ parse_cv()                │  ├─ seniority_fit_score()     │  ├─ LLM Prompting  │
│  ├─ LLM Integration           │  ├─ Skills Matching           │  └─ ATS Optimization │
│  ├─ Skills Extraction         │  ├─ Coverage Calculation      │                     │
│  └─ Normalization             │  └─ Gap Analysis              │                     │
│                                                                                     │
│  ats_validator.py              │  utils.py                                         │
│  ├─ validate_ats_compliance() │  ├─ normalize_inputs()                            │
│  ├─ optimize_resume_for_ats() │  ├─ load_text_auto()                              │
│  ├─ Keyword Analysis          │  ├─ clean_text()                                   │
│  ├─ Structure Validation      │  ├─ contains_skill()                              │
│  └─ Formatting Checks         │  ├─ safety_scan()                                 │
│                               │  └─ File Processing (PDF/DOCX/TXT)                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATA MODELS LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│  models.py                                                                       │
│  ├─ JDStruct (Job Description)                                                  │
│  ├─ CVStruct (Resume/CV)                                                        │
│  ├─ Coverage (Matching Metrics)                                                 │
│  ├─ SuperOutput (Main Result)                                                   │
│  ├─ MatchRequest (API Request)                                                  │
│  ├─ ATSValidationResult                                                         │
│  └─ EnhancedSuperOutput                                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CONFIGURATION LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  config.py                                                                       │
│  ├─ OpenAI API Configuration                                                    │
│  ├─ Skill Normalization Aliases                                                 │
│  ├─ Text Processing Patterns                                                    │
│  ├─ Skill Variants Mapping                                                      │
│  └─ Education Variants                                                          │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│  OpenAI API                    │  File Processing                               │
│  ├─ GPT-4o-mini               │  ├─ PDF Parsing (pypdf)                        │
│  ├─ Text Analysis             │  ├─ DOCX Parsing (python-docx)                 │
│  ├─ Resume Generation         │  ├─ TXT Processing                             │
│  └─ ATS Optimization          │  └─ Language Detection                         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Input Processing
```
User Input (Text/Files) → API Endpoints → Input Normalization → Text Cleaning
```

### 2. Document Parsing
```
Job Description → parse_jd() → JDStruct
Resume/CV → parse_cv() → CVStruct
```

### 3. Matching & Scoring
```
JDStruct + CVStruct → match_and_score() → Score + Coverage + Gaps
```

### 4. Resume Tailoring
```
Original Resume + Job Requirements → tailor_resume() → Optimized Resume
```

### 5. ATS Validation
```
Optimized Resume + Job Keywords → validate_ats_compliance() → ATS Score + Issues
```

### 6. Result Assembly
```
All Components → SuperOutput → JSON Response
```

## Key Components

### Core Modules
- **main.py**: Application entry point and server configuration
- **api.py**: FastAPI routes and HTTP endpoints
- **pipeline.py**: Main orchestration logic
- **models.py**: Pydantic data models and schemas

### Processing Modules
- **parsers.py**: LLM-based document parsing and extraction
- **matcher.py**: Skills matching and compatibility scoring
- **tailor.py**: Resume optimization and tailoring
- **ats_validator.py**: ATS compliance validation and optimization

### Utility Modules
- **utils.py**: Text processing, file handling, and utility functions
- **config.py**: Configuration, constants, and normalization mappings

## API Endpoints

### Matching Endpoints
- `POST /match/run`: Process resume and job description from text
- `POST /match/upload`: Process uploaded resume and job description files

### ATS Endpoints
- `POST /ats/validate`: Validate resume for ATS compliance
- `POST /ats/optimize`: Optimize resume for ATS compatibility

### Utility Endpoints
- `GET /health`: Health check endpoint

## Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications

### AI/ML Services
- **OpenAI API**: GPT models for text analysis and generation
- **LangChain**: Framework for LLM application development

### Data Processing
- **Pydantic**: Data validation and serialization
- **pypdf**: PDF text extraction
- **python-docx**: DOCX file processing
- **langdetect**: Language detection

### File Support
- **PDF**: Resume and job description files
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

## Security Features

### Input Validation
- File type validation
- Content length limits
- Safety scanning for hallucinations
- Education extraction validation

### API Security
- CORS configuration
- Error handling and sanitization
- Environment variable configuration

## Performance Optimizations

### Text Processing
- Efficient regex patterns for normalization
- Caching of skill variants
- Optimized file parsing

### LLM Usage
- Temperature=0 for consistent results
- Structured output parsing
- Minimal token usage through focused prompts

## Deployment Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client        │    │   FastAPI       │    │   OpenAI API    │
│   (Browser/App) │◄──►│   Server        │◄──►│   (GPT Models)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   File Storage  │
                       │   (Temporary)   │
                       └─────────────────┘
```

## Environment Configuration

### Required Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for LLM access

### Optional Configuration
- Model selection (default: gpt-4o-mini)
- Server host and port configuration
- CORS settings

## Error Handling

### Input Validation
- Missing or invalid files
- Unsupported file formats
- Empty or malformed content

### LLM Errors
- API key validation
- Rate limiting handling
- Model availability checks

### Processing Errors
- File parsing failures
- Text extraction issues
- ATS validation errors

This architecture provides a robust, scalable foundation for AI-powered resume and job matching with comprehensive ATS compliance features.

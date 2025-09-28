"""
Pydantic models for the resume-job matcher application.
"""
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field, validator


class JDStruct(BaseModel):
    """Job Description structure."""
    title: str = Field(..., description="Job title")
    seniority: str = Field(..., description="Seniority level (junior/mid/senior)")
    must_have_skills: List[str] = Field(default_factory=list, description="Required technical skills")
    nice_to_have_skills: List[str] = Field(default_factory=list, description="Optional technical skills")
    responsibilities: List[str] = Field(default_factory=list, description="Job responsibilities")
    keywords: List[str] = Field(default_factory=list, description="ATS keywords")
    
    @validator('seniority')
    def validate_seniority(cls, v: str) -> str:
        """Validate seniority level."""
        valid_levels = {'junior', 'mid', 'senior'}
        if v.lower() not in valid_levels:
            raise ValueError(f"Seniority must be one of {valid_levels}")
        return v.lower()


class CVStruct(BaseModel):
    """CV/Resume structure."""
    years_of_experience: float = Field(0.0, ge=0.0, le=50.0, description="Years of professional experience")
    tech_stack: List[str] = Field(default_factory=list, description="Technical skills and technologies")
    soft_skills: List[str] = Field(default_factory=list, description="Soft skills and competencies")
    achievements: List[str] = Field(default_factory=list, description="Professional achievements")
    education: List[str] = Field(default_factory=list, description="Educational qualifications")
    languages: List[str] = Field(default_factory=list, description="Programming and spoken languages")
    
    @validator('years_of_experience')
    def validate_experience(cls, v: float) -> float:
        """Validate years of experience."""
        if v < 0:
            raise ValueError("Years of experience cannot be negative")
        if v > 50:
            raise ValueError("Years of experience seems unrealistic")
        return v


class Coverage(BaseModel):
    """Coverage metrics for matching."""
    must_have: float = Field(0.0, ge=0.0, le=100.0, description="Must-have skills coverage percentage")
    responsibilities: float = Field(0.0, ge=0.0, le=100.0, description="Responsibilities coverage percentage")
    seniority_fit: float = Field(0.0, ge=0.0, le=100.0, description="Seniority fit percentage")


class TailoredResumeStruct(BaseModel):
    """Structured tailored resume for dynamic frontend rendering."""
    contact_info: Dict[str, str] = Field(default_factory=dict, description="Contact information (name, email, phone, location, linkedin)")
    summary: str = Field(default="", description="Professional summary/objective")
    experience: List[Dict[str, Any]] = Field(default_factory=list, description="Work experience with company, title, dates, achievements")
    education: List[Dict[str, str]] = Field(default_factory=list, description="Education with degree, institution, dates")
    skills: Dict[str, Any] = Field(default_factory=dict, description="Skills organized by category (technical, soft, languages)")
    certifications: List[Dict[str, str]] = Field(default_factory=list, description="Certifications with name, issuer, date")
    projects: List[Dict[str, Any]] = Field(default_factory=list, description="Relevant projects with name, description, technologies")
    achievements: List[str] = Field(default_factory=list, description="Key achievements and accomplishments")
    awards: List[Dict[str, str]] = Field(default_factory=list, description="Awards and honors with name, issuer, date")
    publications: List[Dict[str, str]] = Field(default_factory=list, description="Publications with title, journal, date")
    volunteer_work: List[Dict[str, Any]] = Field(default_factory=list, description="Volunteer work with organization, role, dates, description")
    interests: List[str] = Field(default_factory=list, description="Professional interests and hobbies")
    references: List[Dict[str, str]] = Field(default_factory=list, description="References with name, title, contact info")
    languages: List[Dict[str, str]] = Field(default_factory=list, description="Languages with name and proficiency level")
    additional_sections: Dict[str, Any] = Field(default_factory=dict, description="Any other sections present in the original resume")
    tailored_resume_text: str = Field(default="", description="Full formatted resume text for fallback")


class TailoredOutput(BaseModel):
    """Output structure for tailored resume generation."""
    tailored_resume_text: str = Field(default="", description="Full formatted resume text for fallback")
    structured_resume: Optional[TailoredResumeStruct] = None
    recommendations: List[str] = Field(default_factory=list, description="Actionable improvement suggestions")


class SuperOutput(BaseModel):
    """Main output structure for the matching pipeline."""
    score: float = Field(..., ge=0.0, le=100.0, description="Overall compatibility score (0-100)")
    coverage: Coverage = Field(..., description="Detailed coverage breakdown")
    gaps: Dict[str, List[str]] = Field(..., description="Analysis of gaps and matches")
    rationale: str = Field(..., description="Explanation of the compatibility score")
    tailored_resume_text: str = Field(..., description="AI-generated tailored resume")
    structured_resume: Optional[TailoredResumeStruct] = Field(None, description="Structured resume data for dynamic frontend rendering")
    recommendations: List[str] = Field(default_factory=list, description="Actionable improvement suggestions")
    flags: List[str] = Field(default_factory=list, description="Warning flags for potential issues")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Metadata about the processing")


class MatchRequest(BaseModel):
    """Request model for the matching API."""
    resume_text: Optional[str] = None
    job_text: Optional[str] = None
    resume_file_path: Optional[str] = None
    job_file_path: Optional[str] = None
    model: str = "gpt-4o-mini"


class ATSValidationResult(BaseModel):
    """ATS validation result structure."""
    compliance_level: str  # "excellent", "good", "fair", "poor"
    score: float  # 0-100
    issues: List[str]
    recommendations: List[str]
    keyword_density: Dict[str, float]
    structure_score: float
    formatting_score: float


class EnhancedSuperOutput(BaseModel):
    """Enhanced output structure with ATS validation."""
    score: float
    coverage: Coverage
    gaps: Dict[str, List[str]]
    rationale: str
    tailored_resume_text: str
    recommendations: List[str]
    flags: List[str]
    ats_validation: Optional[ATSValidationResult] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


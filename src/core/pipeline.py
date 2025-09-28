"""
Main pipeline orchestrating the resume-job matching process.
"""
from typing import Optional
from .models import SuperOutput, EnhancedSuperOutput, ATSValidationResult
from ..utils.utils import normalize_inputs, validate_education_extraction, safety_scan
from ..parsers.parsers import parse_jd, parse_cv
from .matcher import match_and_score
from .tailor import tailor_resume
from ..validators.ats_validator import validate_ats_compliance


def run_pipeline(
    resume_text: Optional[str],
    job_text: Optional[str],
    resume_file_path: Optional[str],
    job_file_path: Optional[str],
    model: str,
    include_ats_validation: bool = True
) -> SuperOutput:
    """
    Run the complete resume-job matching pipeline.
    
    Args:
        resume_text: Raw resume text
        job_text: Raw job description text
        resume_file_path: Path to resume file
        job_file_path: Path to job description file
        model: OpenAI model to use
        
    Returns:
        SuperOutput with matching results and tailored resume
    """
    # Step 1: Normalize inputs
    r_text, j_text, meta = normalize_inputs(
        resume_text, job_text, resume_file_path, job_file_path
    )
    
    # Step 2: Parse job description
    jd = parse_jd(j_text, model=model)
    
    # Step 3: Parse CV
    cv = parse_cv(r_text, model=model)
    
    # Step 4: Validate education extraction
    education_flags = validate_education_extraction(cv.education, r_text)
    
    # Step 5: Match and score
    score, cov, gaps, rationale = match_and_score(jd, cv, r_text)
    
    # Step 6: Generate tailored resume
    tailored = tailor_resume(r_text, jd, cv, score, cov.dict(), gaps, model=model)
    
    # Step 7: Safety checks
    flags = safety_scan(tailored.tailored_resume_text, r_text)
    
    # Step 8: Add education flags
    flags.extend(education_flags)
    
    # Step 9: ATS validation (optional)
    ats_validation = None
    if include_ats_validation:
        try:
            # Extract keywords from job description for ATS validation
            job_keywords = []
            if jd.must_have_skills:
                job_keywords.extend(jd.must_have_skills)
            if jd.nice_to_have_skills:
                job_keywords.extend(jd.nice_to_have_skills)
            if jd.keywords:
                job_keywords.extend(jd.keywords)
            
            ats_result = validate_ats_compliance(tailored.tailored_resume_text, job_keywords)
            ats_validation = ATSValidationResult(
                compliance_level=ats_result.compliance_level.value,
                score=ats_result.score,
                issues=ats_result.issues,
                recommendations=ats_result.recommendations,
                keyword_density=ats_result.keyword_density,
                structure_score=ats_result.structure_score,
                formatting_score=ats_result.formatting_score
            )
            
            # Add ATS issues to flags if compliance is poor
            if ats_result.compliance_level.value in ["fair", "poor"]:
                flags.extend([f"ats_issue: {issue}" for issue in ats_result.issues[:3]])  # Limit to top 3 issues
                
        except Exception as e:
            flags.append(f"ats_validation_error: {str(e)}")
    
    # Step 10: Return final result
    return SuperOutput(
        score=score,
        coverage=cov,
        gaps=gaps,
        rationale=rationale,
        tailored_resume_text=tailored.tailored_resume_text,
        structured_resume=tailored.structured_resume,
        recommendations=tailored.recommendations,
        flags=flags,
        meta=meta
    )


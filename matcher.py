"""
Matching and scoring logic for resume-job compatibility.
"""
from typing import Tuple, Dict, List
from models import JDStruct, CVStruct, Coverage
from utils import contains_skill


def seniority_fit_score(jd_seniority: str, years: float) -> float:
    """Calculate seniority fit score based on job requirements and candidate experience."""
    s, y = (jd_seniority or "").lower(), (years or 0.0)
    
    if s == "junior":
        return 100.0 if y < 2 else 60.0
    if s == "mid":
        if 2 <= y < 6:
            return 100.0
        if y >= 6:
            return 80.0
        return 40.0
    if s == "senior":
        if y >= 5:
            return 100.0
        if y >= 3:
            return 70.0
        return 30.0
    
    return 60.0


def match_and_score(
    jd: JDStruct, 
    cv: CVStruct, 
    resume_text: str
) -> Tuple[float, Coverage, Dict[str, List[str]], str]:
    """
    Match job description with CV and calculate compatibility score.
    
    Returns:
        - Overall score (0-100)
        - Coverage breakdown
        - Gaps analysis
        - Rationale explanation
    """
    # Create searchable text blob
    blob = (resume_text or "") + " " + " | ".join(cv.achievements or [])
    
    # Calculate must-have skills coverage
    must = jd.must_have_skills or []
    mh_hits, missing, matched = 0, [], []
    for s in must:
        if s in (cv.tech_stack or []) or contains_skill(blob, s):
            mh_hits += 1
            matched.append(s)
        else:
            missing.append(s)
    mh_cov = (mh_hits / max(1, len(must))) * 100.0

    # Calculate responsibilities coverage
    resp = jd.responsibilities or []
    resp_hits, weak = 0, []
    for r in resp:
        tokens = [t for t in r.lower().split() if len(t) > 3]
        hit = any(contains_skill(blob, t) for t in tokens)
        if hit:
            resp_hits += 1
        else:
            weak.append(r)
    resp_cov = (resp_hits / max(1, len(resp))) * 100.0

    # Calculate seniority fit
    sen_fit = seniority_fit_score(jd.seniority, cv.years_of_experience)
    
    # Calculate overall score (weighted average)
    score = 0.7 * mh_cov + 0.2 * resp_cov + 0.1 * sen_fit
    
    # Create coverage object
    cov = Coverage(must_have=mh_cov, responsibilities=resp_cov, seniority_fit=sen_fit)
    
    # Generate rationale
    rationale = f"Core skills coverage {mh_cov:.0f}%, responsibilities {resp_cov:.0f}%, seniority fit {sen_fit:.0f}%."
    
    # Compile gaps and matches
    gaps = {
        "matched_skills": matched,
        "missing_skills": missing,
        "weak_evidence_for_responsibilities": weak
    }
    
    return round(score, 2), cov, gaps, rationale


"""
Utility functions for text processing and normalization.
"""
import re
from typing import List, Dict, Optional, Tuple, Any
from pypdf import PdfReader
from docx import Document as DocxDocument
from langdetect import detect

from ..core.config import (
    BULLET_PATTERN, MULTISPACE, MULTINEWLINE, DASHES, DATE_RANGE,
    ALIASES, SKILL_VARIANTS, EDUCATION_VARIANTS
)


def norm_one(term: str, maps: Dict[str, str]) -> str:
    """Normalize a single term using the provided mapping."""
    if term is None:
        return ""
    t = term.strip().lower()
    return maps.get(t, t)


def normalize_list(items: List[str], maps: Dict[str, str]) -> List[str]:
    """Normalize a list of items using the provided mapping."""
    out, seen = [], set()
    for it in items or []:
        t = norm_one(it, maps)
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def load_text_from_pdf(path: str) -> str:
    """Load text content from a PDF file."""
    reader = PdfReader(path)
    return "\n".join((p.extract_text() or "") for p in reader.pages)


def load_text_from_docx(path: str) -> str:
    """Load text content from a DOCX file."""
    doc = DocxDocument(path)
    return "\n".join(p.text for p in doc.paragraphs)


def load_text_from_txt(path: str) -> str:
    """Load text content from a TXT file."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_text_auto(path: str) -> str:
    """Automatically detect file type and load text content."""
    p = path.lower()
    if p.endswith(".pdf"):
        return load_text_from_pdf(path)
    if p.endswith(".docx"):
        return load_text_from_docx(path)
    return load_text_from_txt(path)


def clean_text(raw: str) -> str:
    """Clean and normalize text content."""
    t = raw
    t = re.sub(BULLET_PATTERN, "-", t)
    t = re.sub(DASHES, "-", t)
    t = re.sub(MULTINEWLINE, "\n\n", t)
    t = re.sub(MULTISPACE, " ", t)
    t = re.sub(DATE_RANGE, lambda m: f"{m.group(1)} - {m.group(2)}", t, flags=re.IGNORECASE)
    return t.strip()


def normalize_inputs(
    resume_text: Optional[str], 
    job_text: Optional[str],
    resume_file_path: Optional[str], 
    job_file_path: Optional[str]
) -> Tuple[str, str, Dict[str, Any]]:
    """Normalize inputs from text or file paths."""
    if not resume_text and resume_file_path:
        resume_text = clean_text(load_text_auto(resume_file_path))
    if not job_text and job_file_path:
        job_text = clean_text(load_text_auto(job_file_path))
    
    resume_text = clean_text(resume_text or "")
    job_text = clean_text(job_text or "")
    
    lang = detect((resume_text or job_text)[:3000]) if (resume_text or job_text).strip() else "en"
    
    return resume_text, job_text, {"detected_language": lang}


def contains_skill(text: str, skill: str) -> bool:
    """Check if a skill is present in the text with improved logic."""
    if not text or not skill:
        return False
    
    text_lower = text.lower()
    skill_lower = skill.lower()
    
    # Direct check
    if skill_lower in text_lower:
        return True
    
    # Check variants
    for base_skill, variants in SKILL_VARIANTS.items():
        if base_skill in skill_lower:
            for variant in variants:
                if variant in text_lower:
                    return True
    
    return False


def validate_education_extraction(cv_education: List[str], original_resume_text: str) -> List[str]:
    """Validate that extracted education corresponds to the original resume."""
    flags = []
    if not cv_education:
        return flags
    
    original_lower = original_resume_text.lower()
    
    for edu in cv_education:
        edu_lower = edu.lower()
        # Check if the extracted degree is mentioned in the original CV
        if edu_lower not in original_lower:
            # Check common variants with stricter logic
            found_variant = False
            for full_name, variants in EDUCATION_VARIANTS.items():
                if full_name in edu_lower:
                    # Check that one of the exact variants is present
                    for variant in variants:
                        if variant in original_lower:
                            found_variant = True
                            break
                    if found_variant:
                        break
            
            if not found_variant:
                flags.append(f"education_hallucination: '{edu}' not found in original resume")
    
    return flags


def safety_scan(tailored_resume_text: str, original_resume_text: str) -> List[str]:
    """Perform safety checks on the tailored resume."""
    flags = []
    
    # Check for new years that weren't in the original
    years_new = set(re.findall(r"\b(19|20)\d{2}\b", tailored_resume_text)) - set(
        re.findall(r"\b(19|20)\d{2}\b", original_resume_text)
    )
    if years_new:
        flags.append("hallucination_suspected")
    
    # Check length limits
    if len(tailored_resume_text.splitlines()) > 200 or len(tailored_resume_text) > 12000:
        flags.append("length_exceeded")
    
    # Check for inappropriate tone
    low = tailored_resume_text.lower().strip()
    if low.startswith("je ") or " je " in low or low.startswith("i ") or " i " in low:
        flags.append("tone_issue")
    
    return flags


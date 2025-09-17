"""
Parsing logic for job descriptions and CVs using LLM.
"""
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from models import JDStruct, CVStruct
from config import ALIASES
from utils import normalize_list, norm_one


# Job Description Parser
JD_parser = PydanticOutputParser(pydantic_object=JDStruct)
JD_prompt = ChatPromptTemplate.from_template("""
You are an assistant that extracts structured information from a job description.
Return ONLY valid JSON according to the schema below. No commentary.

Job description:
---
{job_text}
---

Schema:
{format_instructions}

Rules:
- Seniority mapping: junior/entry-level → junior; confirmé/intermédiaire/mid-level → mid; senior/lead/principal/expert/staff → senior.
- Must-have skills: ONLY specific technical skills, programming languages, frameworks, tools (e.g., "Python", "React", "AWS", "Docker"). NO full sentences or requirements.
- Nice-to-have skills: ONLY specific technical skills, optional technologies (e.g., "GraphQL", "Kubernetes", "MongoDB"). NO full sentences.
- Responsibilities: action sentences, 3–10 items.
- Extract 6–12 specific technical keywords for ATS (e.g., "JavaScript", "Node.js", "PostgreSQL").
""").partial(format_instructions=JD_parser.get_format_instructions())


def clean_skills_list(skills_list: List[str]) -> List[str]:
    """Clean and filter skills list to keep only technical keywords."""
    if not skills_list:
        return []
    
    cleaned = []
    for skill in skills_list:
        if not skill or not skill.strip():
            continue
            
        skill = skill.strip()
        
        # Skip if it's a full sentence (more than 3 words)
        if len(skill.split()) > 3:
            continue
            
        # Skip if it contains common non-technical phrases
        skip_phrases = [
            "degree", "experience", "ability", "knowledge", "understanding",
            "familiarity", "proficiency", "expertise", "skills", "background",
            "bachelor", "master", "phd", "internship", "collaborative", "projects"
        ]
        
        if any(phrase in skill.lower() for phrase in skip_phrases):
            continue
            
        # Keep only technical terms
        cleaned.append(skill)
    
    return cleaned


def parse_jd(job_text: str, model: str) -> JDStruct:
    """Parse job description text into structured format."""
    llm = ChatOpenAI(model=model, temperature=0)
    chain = JD_prompt | llm | JD_parser
    jd = chain.invoke({"job_text": job_text})
    
    # Normalize the parsed data
    tech_map, skills_map = ALIASES["tech"], ALIASES["skills"]
    jd.title = norm_one(jd.title, ALIASES["roles"]) or jd.title
    jd.seniority = ALIASES["seniority"].get(jd.seniority.lower(), jd.seniority.lower())
    
    # Clean and normalize skills lists
    jd.must_have_skills = clean_skills_list(jd.must_have_skills)
    jd.must_have_skills = normalize_list(jd.must_have_skills, {**tech_map, **skills_map})
    
    jd.nice_to_have_skills = clean_skills_list(jd.nice_to_have_skills)
    jd.nice_to_have_skills = normalize_list(jd.nice_to_have_skills, {**tech_map, **skills_map})
    
    jd.keywords = clean_skills_list(jd.keywords)
    jd.keywords = normalize_list(jd.keywords, {**tech_map, **skills_map})
    
    jd.responsibilities = [s.strip() for s in jd.responsibilities if s and s.strip()]
    
    return jd


# CV Parser
CV_parser = PydanticOutputParser(pydantic_object=CVStruct)
CV_prompt = ChatPromptTemplate.from_template("""
Extract a structured candidate profile from the resume text. Use ONLY facts explicitly present in the resume. Return ONLY valid JSON.

Resume:
---
{resume_text}
---

Schema:
{format_instructions}

CRITICAL RULES:
- years_of_experience: infer from roles/dates if possible, else approximate conservatively.
- tech_stack: technologies, frameworks, tools, databases, clouds EXACTLY as mentioned.
- soft_skills: concise set if explicitly mentioned.
- achievements: keep only bullets already present; quantify if numbers exist.
- education: extract ONLY degrees, certifications, and educational qualifications EXPLICITLY mentioned. Include exact abbreviations like B.S., M.S., MBA, PhD, etc. DO NOT infer or suggest missing education.
- languages: as explicitly present.
- ABSOLUTELY NO INVENTION. If information is not explicitly stated, use empty list or 0.
- DO NOT suggest or recommend additional education that is not mentioned in the resume.
""").partial(format_instructions=CV_parser.get_format_instructions())


def parse_cv(resume_text: str, model: str) -> CVStruct:
    """Parse resume text into structured format."""
    llm = ChatOpenAI(model=model, temperature=0)
    chain = CV_prompt | llm | CV_parser
    cv = chain.invoke({"resume_text": resume_text})
    
    # Normalize the parsed data
    tech_map, skills_map, education_map = ALIASES["tech"], ALIASES["skills"], ALIASES["education"]
    cv.tech_stack = normalize_list(cv.tech_stack, {**tech_map, **skills_map})
    cv.soft_skills = normalize_list(cv.soft_skills, skills_map)
    
    # Normalize education with robust approach and avoid duplicates
    normalized_education = []
    seen_degrees = set()
    
    for edu in cv.education or []:
        if not edu or not edu.strip():
            continue
            
        edu_clean = edu.strip()
        edu_lower = edu_clean.lower()
        
        # Look for degree abbreviations in the text
        found_normalization = False
        for abbrev, full_name in education_map.items():
            if abbrev.lower() in edu_lower:
                # Check if we already have this normalized degree
                if full_name not in seen_degrees:
                    normalized_education.append(full_name)
                    seen_degrees.add(full_name)
                found_normalization = True
                break
        
        if not found_normalization:
            # If no abbreviation found, keep original if not already present
            if edu_clean not in seen_degrees:
                normalized_education.append(edu_clean)
                seen_degrees.add(edu_clean)
    
    cv.education = normalized_education
    cv.achievements = [a.strip() for a in cv.achievements if a and a.strip()]
    
    return cv


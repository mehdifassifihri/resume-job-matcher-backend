"""
Resume tailoring functionality using LLM.
"""
from typing import Dict, List
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from .models import JDStruct, CVStruct, TailoredOutput, TailoredResumeStruct


# Tailored Resume Parser
Tail_parser = PydanticOutputParser(pydantic_object=TailoredOutput)
Tail_prompt = ChatPromptTemplate.from_template("""
You are a professional resume tailor. Create a tailored resume using ONLY facts from the original resume, optimized for the job description. Return ONLY valid JSON according to the schema.

Original resume:
---
{resume_text}
---

Job requirements:
---
{jd_struct}
---

Candidate profile:
---
{cv_struct}
---

Match analysis:
- Score: {score}
- Coverage: {coverage}
- Gaps: {gaps}

Schema:
{format_instructions}

SUMMARY:
Create a professional summary that highlights the candidate's most relevant qualifications for this specific job. Focus on:
- Key skills that match job requirements
- Years of relevant experience
- Notable achievements or certifications
- Career objective aligned with the role

INSTRUCTIONS:
1. PRESERVE ALL SECTIONS: Include every section from the original resume
2. STRUCTURED RESUME: Fill all available fields with data from original resume
3. TAILORED TEXT: Create formatted resume text with all original sections
4. KEYWORDS: Naturally incorporate job description keywords
5. RECOMMENDATIONS: Suggest 3-5 actionable improvements
6. MISSING SKILLS: Add missing skills from job requirements to the skills section of structured_resume

SKILLS CATEGORIES:
- "programming_languages": Programming languages (Python, Java, C++, JavaScript, SQL, etc.)
- "tools": Development tools (Git, Docker, Kubernetes, Jenkins, etc.)
- "libraries": Frameworks and libraries (React, Django, TensorFlow, etc.)
- "databases": Database technologies (MySQL, PostgreSQL, MongoDB, etc.)
- "cloud_platforms": Cloud services (AWS, Azure, GCP, etc.)
- "methodologies": Development methodologies (Agile, Scrum, CI/CD, etc.)
- "other": Other technical skills (API Development, Microservices, etc.)

Return ONLY the JSON object, no additional text.
""").partial(format_instructions=Tail_parser.get_format_instructions())


def tailor_resume(
    resume_text: str,
    jd: JDStruct,
    cv: CVStruct,
    score: float,
    coverage: Dict,
    gaps: Dict,
    model: str
) -> TailoredOutput:
    """Generate a tailored resume based on job requirements."""
    llm = ChatOpenAI(model=model, temperature=0)
    chain = Tail_prompt | llm | Tail_parser
    
    return chain.invoke({
        "resume_text": resume_text,
        "jd_struct": jd.dict(),
        "cv_struct": cv.dict(),
        "score": score,
        "coverage": coverage,
        "gaps": gaps
    })


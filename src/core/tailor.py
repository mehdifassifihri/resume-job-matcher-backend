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
You rewrite the resume strictly using only facts from the original resume, tailored to the job description and optimized for ATS (Applicant Tracking Systems). Return ONLY valid JSON with both structured data and formatted text.

Original resume:
---
{resume_text}
---

Job (structured):
---
{jd_struct}
---

Candidate (structured):
---
{cv_struct}
---

Score and gaps:
---
score={score}
coverage={coverage}
gaps={gaps}
---

Schema:
{format_instructions}

CRITICAL RULES FOR STRUCTURED OUTPUT:
- structured_resume: Provide detailed structured data for dynamic frontend rendering
- tailored_resume_text: Provide full formatted resume text for fallback/ATS compatibility
- Keep ONLY factual content present in original resume
- Prioritize JD keywords naturally throughout all sections

STRUCTURED RESUME REQUIREMENTS:
- contact_info: Extract name, email, phone, location, linkedin from original resume
- summary: Create 2-3 sentence professional summary highlighting relevant experience for this job
- experience: List work experience with company, title, start_date, end_date, achievements (array of strings)
- education: List education with degree, institution, start_date, end_date
- skills: Organize into categories: technical (programming languages, frameworks, tools), soft (leadership, communication), languages (spoken languages). CRITICAL: Add ALL missing skills from job description to the skills section while avoiding duplicates with existing skills. This is mandatory - missing job skills must appear in the structured_resume skills field.
- certifications: List with name, issuer, date
- projects: Include relevant projects with name, description, technologies_used, achievements
- achievements: Key accomplishments and metrics

FORMATTED TEXT REQUIREMENTS:
- Use standard section headers: "EXPERIENCE", "EDUCATION", "SKILLS", "SUMMARY"
- Reorder experience with most relevant first
- Use simple formatting: standard bullets (- or •), no tables, no images
- Bullets ≤ 2 lines, start with strong action verbs, quantify with numbers
- Include contact information clearly at the top
- Total length target: 1–2 pages (400-800 words)
- Use consistent date formats (MM/YYYY or Month YYYY)
- Avoid first person pronouns ("I", "me", "my")
- Use industry-standard terminology and job titles

CONTENT OPTIMIZATION:
- Start bullet points with action verbs: "Developed", "Implemented", "Managed", "Led", "Improved", "Created"
- Include specific metrics and quantifiable results where possible
- Highlight technical skills and tools mentioned in the job description
- Emphasize relevant achievements and responsibilities
- Use keywords from the job description naturally in context

RECOMMENDATIONS:
- Provide 3–5 short, actionable items that DO NOT suggest education already present in the resume
- DO NOT recommend obtaining degrees or certifications that are already mentioned in the candidate's education
- Focus recommendations on skills, experience, or certifications that are actually missing and relevant to the job
- Include specific, measurable suggestions for skill development or experience gaps
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


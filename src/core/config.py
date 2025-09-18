"""
Configuration and constants for the resume-job matcher application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4o-mini"

# Validation
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY environment variable is not set!")
    print("Please set your OpenAI API key:")
    print("export OPENAI_API_KEY='your-api-key-here'")
    print("Or create a .env file with: OPENAI_API_KEY=your-api-key-here")

# Normalization aliases for different categories
ALIASES = {
    "seniority": {
        "stagiaire": "junior", "alternant": "junior", "junior": "junior", "entry-level": "junior",
        "confirmé": "mid", "expérimenté": "mid", "intermédiaire": "mid", "mid-level": "mid",
        "senior": "senior", "lead": "senior", "principal": "senior", "expert": "senior", "staff": "senior"
    },
    "roles": {
        "développeur": "software engineer", "développeuse": "software engineer",
        "ingénieur logiciel": "software engineer", "ingénieur études et développement": "software engineer",
        "développeur back-end": "backend engineer", "développeur front-end": "frontend engineer",
        "full-stack": "fullstack engineer", "référent technique": "tech lead", "tech lead": "tech lead"
    },
    "tech": {
        "js": "javascript", "javascript": "javascript", "ts": "typescript", "typescript": "typescript",
        "py": "python", "python": "python", "java ee": "java", "jee": "java", "j2ee": "java", "java": "java",
        ".net": ".net", "dotnet": ".net", "sql": "sql", "spring": "spring boot", "spring boot": "spring boot",
        "hibernate": "hibernate", "struts": "struts", "jpa": "jpa", "maven": "maven", "gradle": "gradle",
        "reactjs": "react", "react": "react", "vuejs": "vue", "vue": "vue", "angular": "angular", "jquery": "jquery",
        "postgres": "postgresql", "postgresql": "postgresql", "mysql": "mysql", "oracle": "oracle",
        "mongodb": "mongodb", "mongo": "mongodb", "elasticsearch": "elasticsearch", "elastic": "elasticsearch",
        "redis": "redis", "aws": "aws", "azure": "azure", "gcp": "gcp", "google cloud": "gcp",
        "docker": "docker", "k8s": "kubernetes", "kubernetes": "kubernetes", "ci/cd": "ci/cd",
        "intégration continue": "ci/cd", "déploiement continu": "ci/cd", "terraform": "terraform", "ansible": "ansible",
        "micro-services": "microservices", "microservices": "microservices", "rest": "rest", "restful": "rest",
        "soap": "soap", "event-driven": "event-driven", "événementiel": "event-driven",
        "message broker": "message queues", "queue": "message queues", "mq": "message queues"
    },
    "skills": {
        "cahier des charges": "functional specifications", "spécifications fonctionnelles": "functional specifications",
        "spécifications techniques": "technical specifications", "conception": "technical design", "design technique": "technical design",
        "développement back-end": "backend development", "développement front-end": "frontend development",
        "mise en production": "production deployment", "go-live": "production deployment", "release": "production deployment",
        "exploitation": "operations", "run": "operations", "recette": "user acceptance testing",
        "tests fonctionnels": "user acceptance testing", "tests unitaires": "unit testing", "revue de code": "code review",
        "pair programming": "pair programming", "montée en compétence": "upskilling", "veille technologique": "tech watch",
        "performance": "performance optimization", "optimisation": "performance optimization",
        "ergonomie": "ux/usability", "ux": "ux/usability", "accessibilité": "ux/usability",
        "sécurité applicative": "application security", "gestion d'incidents": "incident management",
        "sla": "sla management", "engagements de service": "sla management"
    },
    "education": {
        "b.s.": "bachelor of science", "bs": "bachelor of science", "bachelor of science": "bachelor of science",
        "b.a.": "bachelor of arts", "ba": "bachelor of arts", "bachelor of arts": "bachelor of arts",
        "b.eng.": "bachelor of engineering", "beng": "bachelor of engineering", "bachelor of engineering": "bachelor of engineering",
        "b.com.": "bachelor of commerce", "bcom": "bachelor of commerce", "bachelor of commerce": "bachelor of commerce",
        "m.s.": "master of science", "ms": "master of science", "master of science": "master of science",
        "m.a.": "master of arts", "ma": "master of arts", "master of arts": "master of arts",
        "m.eng.": "master of engineering", "meng": "master of engineering", "master of engineering": "master of engineering",
        "mba": "master of business administration", "master of business administration": "master of business administration",
        "phd": "doctor of philosophy", "ph.d.": "doctor of philosophy", "doctor of philosophy": "doctor of philosophy",
        "licence": "bachelor degree", "master": "master degree", "doctorat": "phd", "ingénieur": "engineer"
    }
}

# Text processing patterns
BULLET_PATTERN = r"[•·◦●∙\u2022\u25CF\u2219]"
MULTISPACE = r"[ \t]{2,}"
MULTINEWLINE = r"\n{3,}"
DASHES = r"[–—―]+"
DATE_RANGE = r"(\b\d{1,2}[\/\.-]\d{4}\b|\b\d{4}\b)\s*[-–—]\s*(\b\d{1,2}[\/\.-]\d{4}\b|\bPresent|Présent|Now\b)"

# Skill matching variants
SKILL_VARIANTS = {
    "ruby": ["ruby", "ruby on rails", "rails"],
    "javascript": ["javascript", "js", "node.js", "nodejs"],
    "java": ["java", "java ee", "jee", "j2ee"],
    "python": ["python", "py"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "nodejs", "node"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker", "dockerfile"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github", "gitlab"],
    "agile": ["agile", "scrum", "kanban"],
    "rest": ["rest", "restful", "rest api"],
    "graphql": ["graphql", "graph ql"],
    "typescript": ["typescript", "ts"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "swift": ["swift", "ios"],
    "c++": ["c++", "cpp", "c plus plus"],
    "c": ["c programming", "c language"],
    "latex": ["latex", "tex"],
    "figma": ["figma"],
    "firebase": ["firebase"],
    "heroku": ["heroku"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "jira": ["jira"],
    "xcode": ["xcode", "x-code"]
}

# Education validation variants
EDUCATION_VARIANTS = {
    "bachelor of science": ["b.s.", "bs", "bachelor of science"],
    "master of science": ["m.s.", "ms", "master of science"],
    "bachelor of arts": ["b.a.", "ba", "bachelor of arts"],
    "master of business administration": ["mba", "master of business administration"],
    "doctor of philosophy": ["phd", "ph.d.", "doctor of philosophy"]
}


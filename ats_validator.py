"""
ATS (Applicant Tracking System) validation and optimization module.
Ensures generated resumes are compliant with ATS requirements.
"""
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ATSComplianceLevel(Enum):
    """ATS compliance levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


@dataclass
class ATSValidationResult:
    """Result of ATS validation."""
    compliance_level: ATSComplianceLevel
    score: float  # 0-100
    issues: List[str]
    recommendations: List[str]
    keyword_density: Dict[str, float]
    structure_score: float
    formatting_score: float


class ATSValidator:
    """Validates and optimizes resumes for ATS compatibility."""
    
    def __init__(self):
        # ATS-friendly section headers (case-insensitive)
        self.standard_sections = {
            "contact", "personal information", "profile", "summary", "objective",
            "experience", "work experience", "employment", "professional experience",
            "education", "academic background", "qualifications",
            "skills", "technical skills", "core competencies", "expertise",
            "certifications", "licenses", "awards", "achievements",
            "projects", "publications", "languages", "interests", "hobbies"
        }
        
        # ATS-unfriendly elements
        self.problematic_elements = [
            r'<img[^>]*>',  # Images
            r'<table[^>]*>.*?</table>',  # Tables
            r'<div[^>]*>.*?</div>',  # Complex divs
            r'<span[^>]*>.*?</span>',  # Spans with styling
            r'background-color:',  # Background colors
            r'color:\s*[^;]+;',  # Text colors
            r'font-family:\s*[^;]+;',  # Custom fonts
            r'text-align:\s*center',  # Center alignment
            r'float:\s*(left|right)',  # Floating elements
        ]
        
        # Common ATS keywords for tech roles
        self.tech_keywords = {
            "programming": ["programming", "coding", "development", "software engineering"],
            "languages": ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "php", "ruby"],
            "frameworks": ["react", "angular", "vue", "spring", "django", "flask", "express", "laravel"],
            "databases": ["mysql", "postgresql", "mongodb", "redis", "elasticsearch", "oracle", "sqlite"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins"],
            "methodologies": ["agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "bdd"],
            "tools": ["git", "jira", "confluence", "slack", "figma", "postman", "swagger"]
        }
    
    def validate_resume(self, resume_text: str, job_keywords: List[str] = None) -> ATSValidationResult:
        """
        Validate a resume for ATS compatibility.
        
        Args:
            resume_text: The resume text to validate
            job_keywords: Keywords from the job description
            
        Returns:
            ATSValidationResult with validation details
        """
        issues = []
        recommendations = []
        
        # Check for problematic elements
        formatting_score = self._check_formatting(resume_text, issues, recommendations)
        
        # Check structure
        structure_score = self._check_structure(resume_text, issues, recommendations)
        
        # Check keyword optimization
        keyword_density = self._analyze_keywords(resume_text, job_keywords or [])
        
        # Check length and content
        self._check_content_quality(resume_text, issues, recommendations)
        
        # Calculate overall score
        overall_score = (formatting_score * 0.3 + structure_score * 0.4 + 
                        self._calculate_keyword_score(keyword_density) * 0.3)
        
        # Determine compliance level
        if overall_score >= 90:
            compliance_level = ATSComplianceLevel.EXCELLENT
        elif overall_score >= 75:
            compliance_level = ATSComplianceLevel.GOOD
        elif overall_score >= 60:
            compliance_level = ATSComplianceLevel.FAIR
        else:
            compliance_level = ATSComplianceLevel.POOR
        
        return ATSValidationResult(
            compliance_level=compliance_level,
            score=overall_score,
            issues=issues,
            recommendations=recommendations,
            keyword_density=keyword_density,
            structure_score=structure_score,
            formatting_score=formatting_score
        )
    
    def _check_formatting(self, text: str, issues: List[str], recommendations: List[str]) -> float:
        """Check formatting compliance."""
        score = 100.0
        
        # Check for problematic HTML/CSS elements
        for pattern in self.problematic_elements:
            if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                issues.append(f"Contains problematic formatting: {pattern}")
                score -= 15
        
        # Check for special characters that might confuse ATS
        special_chars = re.findall(r'[^\w\s\-\.\,\:\;\(\)\[\]\/\@\+]', text)
        if special_chars:
            unique_chars = set(special_chars)
            if len(unique_chars) > 5:
                issues.append(f"Contains many special characters: {unique_chars}")
                score -= 10
        
        # Check for proper bullet points
        bullet_patterns = [r'[•·◦●]', r'[-\*]', r'\d+\.']
        bullet_count = sum(len(re.findall(pattern, text)) for pattern in bullet_patterns)
        if bullet_count == 0:
            issues.append("No bullet points found - consider using bullet points for better readability")
            score -= 5
        elif bullet_count > 50:
            issues.append("Too many bullet points - consider consolidating")
            score -= 5
        
        # Check line length
        lines = text.split('\n')
        long_lines = [line for line in lines if len(line) > 100]
        if len(long_lines) > len(lines) * 0.3:
            issues.append("Many lines are too long - ATS prefers shorter lines")
            score -= 10
        
        if score < 70:
            recommendations.append("Simplify formatting - remove complex styling and use standard fonts")
        
        return max(0, score)
    
    def _check_structure(self, text: str, issues: List[str], recommendations: List[str]) -> float:
        """Check structural compliance."""
        score = 100.0
        text_lower = text.lower()
        
        # Check for standard sections
        found_sections = []
        for section in self.standard_sections:
            if section in text_lower:
                found_sections.append(section)
        
        # Essential sections
        essential_sections = ["experience", "education", "skills"]
        missing_essential = [s for s in essential_sections 
                           if not any(s in found for found in found_sections)]
        
        if missing_essential:
            issues.append(f"Missing essential sections: {missing_essential}")
            score -= 20 * len(missing_essential)
        
        # Check for proper section headers
        header_pattern = r'^[A-Z][A-Z\s]+$|^[A-Z][a-z\s]+:$'
        headers = re.findall(header_pattern, text, re.MULTILINE)
        if len(headers) < 3:
            issues.append("Insufficient section headers - use clear, standard headers")
            score -= 15
        
        # Check for contact information
        contact_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\+?[\d\s\-\(\)]{10,}',  # Phone
            r'\b[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+\b'  # Address
        ]
        
        contact_found = any(re.search(pattern, text) for pattern in contact_patterns)
        if not contact_found:
            issues.append("No clear contact information found")
            score -= 25
        
        if score < 70:
            recommendations.append("Improve structure - use standard section headers and ensure contact info is present")
        
        return max(0, score)
    
    def _analyze_keywords(self, text: str, job_keywords: List[str]) -> Dict[str, float]:
        """Analyze keyword density and relevance."""
        text_lower = text.lower()
        word_count = len(text.split())
        keyword_density = {}
        
        # Analyze job-specific keywords
        for keyword in job_keywords:
            keyword_lower = keyword.lower()
            count = text_lower.count(keyword_lower)
            density = (count / word_count) * 100 if word_count > 0 else 0
            keyword_density[keyword] = density
        
        # Analyze tech keywords
        for category, keywords in self.tech_keywords.items():
            category_count = 0
            for keyword in keywords:
                category_count += text_lower.count(keyword.lower())
            density = (category_count / word_count) * 100 if word_count > 0 else 0
            keyword_density[f"tech_{category}"] = density
        
        return keyword_density
    
    def _calculate_keyword_score(self, keyword_density: Dict[str, float]) -> float:
        """Calculate keyword optimization score."""
        if not keyword_density:
            return 50.0
        
        # Job-specific keywords should have reasonable density (1-3%)
        job_keywords = {k: v for k, v in keyword_density.items() 
                       if not k.startswith('tech_')}
        
        if not job_keywords:
            return 30.0
        
        # Check if keywords are present but not overused
        good_keywords = 0
        for keyword, density in job_keywords.items():
            if 0.5 <= density <= 3.0:  # Optimal range
                good_keywords += 1
            elif density > 5.0:  # Overused
                good_keywords -= 0.5
        
        return min(100, max(0, (good_keywords / len(job_keywords)) * 100))
    
    def _check_content_quality(self, text: str, issues: List[str], recommendations: List[str]):
        """Check content quality for ATS."""
        # Check length
        word_count = len(text.split())
        if word_count < 200:
            issues.append("Resume too short - may lack sufficient detail")
        elif word_count > 800:
            issues.append("Resume too long - ATS and recruiters prefer concise resumes")
        
        # Check for quantified achievements
        numbers = re.findall(r'\b\d+(?:\.\d+)?%?\b', text)
        if len(numbers) < 3:
            issues.append("Few quantified achievements - add more metrics and numbers")
            recommendations.append("Include specific numbers, percentages, and metrics in your achievements")
        
        # Check for action verbs
        action_verbs = [
            "developed", "created", "implemented", "managed", "led", "improved",
            "increased", "decreased", "optimized", "designed", "built", "delivered",
            "achieved", "accomplished", "executed", "coordinated", "collaborated"
        ]
        
        text_lower = text.lower()
        found_verbs = sum(1 for verb in action_verbs if verb in text_lower)
        if found_verbs < 5:
            issues.append("Insufficient action verbs - use more dynamic language")
            recommendations.append("Start bullet points with strong action verbs")
    
    def optimize_for_ats(self, resume_text: str, job_keywords: List[str]) -> str:
        """
        Optimize resume text for ATS compatibility.
        
        Args:
            resume_text: Original resume text
            job_keywords: Keywords from job description
            
        Returns:
            Optimized resume text
        """
        # Remove problematic formatting
        optimized = resume_text
        
        # Remove HTML tags and styling
        optimized = re.sub(r'<[^>]+>', '', optimized)
        optimized = re.sub(r'style="[^"]*"', '', optimized)
        
        # Normalize bullet points
        optimized = re.sub(r'[•·◦●]', '-', optimized)
        
        # Ensure proper line breaks
        optimized = re.sub(r'\n{3,}', '\n\n', optimized)
        
        # Add missing keywords naturally
        if job_keywords:
            optimized = self._integrate_keywords(optimized, job_keywords)
        
        return optimized
    
    def _integrate_keywords(self, text: str, keywords: List[str]) -> str:
        """Integrate job keywords naturally into the resume."""
        # This is a simplified version - in practice, you'd want more sophisticated
        # keyword integration that maintains natural language flow
        text_lower = text.lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower not in text_lower:
                # Find a good place to add the keyword (e.g., in skills section)
                if "skills" in text_lower:
                    skills_section = re.search(r'(?i)skills?[:\-]?\s*(.*?)(?=\n[A-Z]|\n\n|$)', 
                                             text, re.DOTALL)
                    if skills_section:
                        skills_text = skills_section.group(1)
                        if keyword not in skills_text:
                            # Add keyword to skills section
                            text = text.replace(skills_section.group(0), 
                                              skills_section.group(0) + f", {keyword}")
        
        return text


def validate_ats_compliance(resume_text: str, job_keywords: List[str] = None) -> ATSValidationResult:
    """
    Convenience function to validate ATS compliance.
    
    Args:
        resume_text: Resume text to validate
        job_keywords: Optional job description keywords
        
    Returns:
        ATSValidationResult
    """
    validator = ATSValidator()
    return validator.validate_resume(resume_text, job_keywords)


def optimize_resume_for_ats(resume_text: str, job_keywords: List[str]) -> str:
    """
    Convenience function to optimize resume for ATS.
    
    Args:
        resume_text: Original resume text
        job_keywords: Job description keywords
        
    Returns:
        Optimized resume text
    """
    validator = ATSValidator()
    return validator.optimize_for_ats(resume_text, job_keywords)


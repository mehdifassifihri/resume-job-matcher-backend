#!/usr/bin/env python3
"""
Demo script for the AI Resume & Job Matcher API
This script demonstrates the key features and capabilities of the system.
"""

import requests
import json
import time
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
SAMPLE_RESUME = """
John Smith
Software Engineer
Email: john.smith@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years of experience in full-stack development, specializing in Python, JavaScript, and cloud technologies.

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, TypeScript, Java
Frameworks: React, Node.js, Django, Flask
Databases: PostgreSQL, MongoDB, Redis
Cloud: AWS, Docker, Kubernetes
Tools: Git, Jira, VS Code

EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2021 - Present
• Led development of microservices architecture serving 1M+ users
• Implemented CI/CD pipelines reducing deployment time by 60%
• Built RESTful APIs using Python/Django and Node.js/Express
• Mentored 3 junior developers and conducted code reviews

Software Engineer | StartupXYZ | 2019 - 2021
• Developed full-stack web applications using React and Python
• Collaborated with cross-functional teams in Agile environment
• Implemented automated testing increasing code coverage to 85%

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2014 - 2018
GPA: 3.7/4.0

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2022)
• Certified Kubernetes Administrator (2021)
"""

SAMPLE_JOB = """
Senior Full-Stack Developer - Remote

Company: InnovateTech Solutions
Location: Remote
Employment Type: Full-time

About the Role:
We are seeking a highly skilled Senior Full-Stack Developer to join our dynamic team. You will be responsible for developing and maintaining our cutting-edge web applications.

Key Responsibilities:
• Design and develop scalable web applications using modern frameworks
• Build and maintain RESTful APIs and microservices architecture
• Collaborate with cross-functional teams including product managers and designers
• Implement automated testing and CI/CD pipelines for continuous deployment
• Optimize application performance and ensure high availability
• Mentor junior developers and conduct code reviews

Required Skills & Qualifications:
• 5+ years of professional software development experience
• Strong proficiency in Python and JavaScript/TypeScript
• Experience with React.js and Node.js frameworks
• Solid understanding of database design and optimization (PostgreSQL, MongoDB)
• Experience with cloud platforms (AWS, Azure, or GCP)
• Knowledge of containerization technologies (Docker, Kubernetes)
• Familiarity with version control systems (Git)
• Experience with Agile/Scrum development methodologies

Preferred Qualifications:
• Experience with microservices architecture
• Knowledge of DevOps practices and CI/CD pipelines
• Familiarity with testing frameworks (Jest, Pytest)
• Understanding of security best practices in web development

Keywords: Python, JavaScript, TypeScript, React, Node.js, AWS, Docker, Kubernetes, PostgreSQL, MongoDB, Microservices, CI/CD, Agile
"""


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n📋 {title}")
    print("-" * 40)


def check_api_health():
    """Check if the API is running and healthy."""
    print_header("API Health Check")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy and running!")
            print(f"   Status: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   OpenAI Configured: {data['openai_configured']}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Please make sure the server is running:")
        print("   python main.py")
        return False


def demo_text_matching():
    """Demonstrate text-based resume-job matching."""
    print_section("Text-based Resume-Job Matching")
    
    data = {
        "resume_text": SAMPLE_RESUME,
        "job_text": SAMPLE_JOB,
        "model": "gpt-4o-mini"
    }
    
    try:
        print("🔄 Processing resume and job description...")
        start_time = time.time()
        
        response = requests.post(f"{API_BASE_URL}/match/run", json=data)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            processing_time = end_time - start_time
            
            print(f"✅ Matching completed in {processing_time:.2f} seconds")
            print(f"📊 Overall Compatibility Score: {result['score']}/100")
            
            # Coverage breakdown
            coverage = result['coverage']
            print(f"   📈 Must-have Skills: {coverage['must_have']:.1f}%")
            print(f"   📈 Responsibilities: {coverage['responsibilities']:.1f}%")
            print(f"   📈 Seniority Fit: {coverage['seniority_fit']:.1f}%")
            
            # Gaps analysis
            gaps = result['gaps']
            print(f"\n🎯 Matched Skills: {', '.join(gaps['matched_skills'])}")
            print(f"❌ Missing Skills: {', '.join(gaps['missing_skills'])}")
            
            # Recommendations
            if result['recommendations']:
                print(f"\n💡 Recommendations:")
                for i, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
            
            # Flags
            if result['flags']:
                print(f"\n⚠️  Flags: {', '.join(result['flags'])}")
            else:
                print("\n✅ No issues detected")
                
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during matching: {e}")
        return None


def demo_ats_validation():
    """Demonstrate ATS validation."""
    print_section("ATS Validation")
    
    data = {
        'resume_text': SAMPLE_RESUME,
        'job_keywords': 'Python,JavaScript,React,AWS,Docker,Kubernetes,PostgreSQL,MongoDB'
    }
    
    try:
        print("🔄 Validating resume for ATS compliance...")
        start_time = time.time()
        
        response = requests.post(f"{API_BASE_URL}/ats/validate", data=data)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            processing_time = end_time - start_time
            
            print(f"✅ Validation completed in {processing_time:.2f} seconds")
            print(f"📊 ATS Score: {result['score']}/100")
            print(f"📈 Compliance Level: {result['compliance_level'].upper()}")
            print(f"   Structure Score: {result['structure_score']:.1f}/100")
            print(f"   Formatting Score: {result['formatting_score']:.1f}/100")
            
            # Issues
            if result['issues']:
                print(f"\n⚠️  Issues Found:")
                for i, issue in enumerate(result['issues'][:3], 1):
                    print(f"   {i}. {issue}")
            else:
                print("\n✅ No issues found")
            
            # Recommendations
            if result['recommendations']:
                print(f"\n💡 Recommendations:")
                for i, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
            
            # Keyword density
            if result['keyword_density']:
                print(f"\n🔍 Top Keywords:")
                sorted_keywords = sorted(
                    result['keyword_density'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5]
                for keyword, density in sorted_keywords:
                    print(f"   {keyword}: {density:.2f}%")
                    
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during ATS validation: {e}")
        return None


def demo_ats_optimization():
    """Demonstrate ATS optimization."""
    print_section("ATS Optimization")
    
    data = {
        'resume_text': SAMPLE_RESUME,
        'job_keywords': 'Python,JavaScript,React,AWS,Docker,Kubernetes,PostgreSQL,MongoDB,Microservices,CI/CD'
    }
    
    try:
        print("🔄 Optimizing resume for ATS...")
        start_time = time.time()
        
        response = requests.post(f"{API_BASE_URL}/ats/optimize", data=data)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            processing_time = end_time - start_time
            
            print(f"✅ Optimization completed in {processing_time:.2f} seconds")
            print(f"📊 Original Length: {result['original_length']} characters")
            print(f"📊 Optimized Length: {result['optimized_length']} characters")
            print(f"🔑 Keywords Integrated: {result['keywords_integrated']}")
            
            # Show a preview of the optimized resume
            optimized = result['optimized_resume']
            preview = optimized[:500] + "..." if len(optimized) > 500 else optimized
            print(f"\n📄 Optimized Resume Preview:")
            print(f"   {preview}")
            
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during ATS optimization: {e}")
        return None


def demo_file_upload():
    """Demonstrate file upload functionality."""
    print_section("File Upload Demo")
    
    # Create temporary files
    resume_file = "temp_resume.txt"
    job_file = "temp_job.txt"
    
    try:
        # Write sample data to files
        with open(resume_file, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_RESUME)
        
        with open(job_file, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_JOB)
        
        print("🔄 Uploading files for processing...")
        start_time = time.time()
        
        with open(resume_file, 'rb') as rf, open(job_file, 'rb') as jf:
            files = {
                'resume_file': rf,
                'job_file': jf
            }
            data = {'model': 'gpt-4o-mini'}
            
            response = requests.post(f"{API_BASE_URL}/match/upload", files=files, data=data)
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            processing_time = end_time - start_time
            
            print(f"✅ File processing completed in {processing_time:.2f} seconds")
            print(f"📊 Compatibility Score: {result['score']}/100")
            print(f"📈 Must-have Skills Coverage: {result['coverage']['must_have']:.1f}%")
            
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during file upload: {e}")
        return None
    finally:
        # Clean up temporary files
        for file in [resume_file, job_file]:
            try:
                Path(file).unlink(missing_ok=True)
            except:
                pass


def print_summary(results: dict):
    """Print a summary of all demo results."""
    print_header("Demo Summary")
    
    if not results:
        print("❌ No successful demos completed")
        return
    
    print("✅ Successfully completed demos:")
    
    if 'text_matching' in results:
        print(f"   📊 Text Matching: {results['text_matching']['score']}/100 score")
    
    if 'ats_validation' in results:
        print(f"   📋 ATS Validation: {results['ats_validation']['score']}/100 score")
    
    if 'ats_optimization' in results:
        print(f"   🔧 ATS Optimization: {results['ats_optimization']['keywords_integrated']} keywords integrated")
    
    if 'file_upload' in results:
        print(f"   📁 File Upload: {results['file_upload']['score']}/100 score")
    
    print(f"\n🎉 All {len(results)} demos completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Review the API documentation in docs/API.md")
    print("   2. Try the test script: python samples/test_api.py")
    print("   3. Explore the sample files in samples/")
    print("   4. Check out the deployment guide in docs/DEPLOYMENT.md")


def main():
    """Run the complete demo."""
    print_header("AI Resume & Job Matcher - Demo")
    print("This demo showcases the key features of the AI Resume & Job Matcher API.")
    print("Make sure the server is running: python main.py")
    
    # Check API health
    if not check_api_health():
        return
    
    results = {}
    
    # Run demos
    print("\n🚀 Starting demos...")
    
    # Text matching demo
    text_result = demo_text_matching()
    if text_result:
        results['text_matching'] = text_result
    
    # ATS validation demo
    ats_result = demo_ats_validation()
    if ats_result:
        results['ats_validation'] = ats_result
    
    # ATS optimization demo
    opt_result = demo_ats_optimization()
    if opt_result:
        results['ats_optimization'] = opt_result
    
    # File upload demo
    file_result = demo_file_upload()
    if file_result:
        results['file_upload'] = file_result
    
    # Print summary
    print_summary(results)


if __name__ == "__main__":
    main()

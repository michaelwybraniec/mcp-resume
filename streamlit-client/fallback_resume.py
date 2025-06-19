"""
Fallback Resume Service

Provides sample resume data when MCP server is not available (e.g., on Streamlit Cloud).
This allows the app to demonstrate functionality even without the full MCP setup.
"""

import json
from typing import Dict, Any

# Sample resume data for demonstration
SAMPLE_RESUME_DATA = {
    "personal": {
        "name": "Michael Wybraniec",
        "title": "Senior Full-Stack Developer & AI Specialist",
        "location": "Global Remote",
        "email": "contact@example.com",
        "summary": "Experienced full-stack developer with 10+ years across 5 countries, specializing in AI integration, MCP protocols, and enterprise solutions. Expert in TypeScript, Python, React, and modern AI frameworks."
    },
    "experience": [
        {
            "company": "AI Solutions Inc.",
            "position": "Senior AI Developer",
            "duration": "2022 - Present",
            "location": "Remote",
            "description": "Leading AI integration projects, developing MCP protocols, and building enterprise AI solutions. Specialized in LLM integration, prompt engineering, and AI-powered applications."
        },
        {
            "company": "Tech Innovations Ltd.",
            "position": "Full-Stack Developer",
            "duration": "2019 - 2022",
            "location": "London, UK",
            "description": "Developed scalable web applications using React, Node.js, and Python. Led team of 5 developers and implemented CI/CD pipelines."
        },
        {
            "company": "Global Software Corp.",
            "position": "Software Engineer",
            "duration": "2017 - 2019",
            "location": "Berlin, Germany",
            "description": "Built microservices architecture and RESTful APIs. Worked with cloud platforms and containerization technologies."
        }
    ],
    "skills": {
        "technical": [
            "TypeScript", "Python", "React", "Node.js", "AI/ML",
            "OpenAI API", "Streamlit", "MCP Protocol", "Docker",
            "AWS", "PostgreSQL", "MongoDB", "Git", "CI/CD"
        ],
        "languages": ["English (Native)", "German (Conversational)", "Polish (Native)"],
        "certifications": ["AWS Certified Developer", "AI/ML Specialization"]
    },
    "education": [
        {
            "degree": "Master of Computer Science",
            "institution": "Technical University",
            "year": "2016",
            "location": "Warsaw, Poland"
        }
    ],
    "projects": [
        {
            "name": "MCP Resume System",
            "description": "AI-powered resume screening system using Model Context Protocol",
            "technologies": ["TypeScript", "Python", "Streamlit", "OpenAI", "MCP"],
            "url": "https://github.com/michaelwybraniec/mcp-resume"
        },
        {
            "name": "Enterprise AI Dashboard",
            "description": "Real-time analytics dashboard with AI-powered insights",
            "technologies": ["React", "Python", "FastAPI", "PostgreSQL"],
            "url": "https://example.com/ai-dashboard"
        }
    ]
}

class FallbackResumeService:
    """Provides resume data when MCP server is not available"""
    
    def __init__(self):
        self.data = SAMPLE_RESUME_DATA
    
    def get_full_resume(self) -> Dict[str, Any]:
        """Get complete resume data"""
        return self.data
    
    def get_experience(self) -> Dict[str, Any]:
        """Get work experience"""
        return {"experience": self.data["experience"]}
    
    def get_skills(self) -> Dict[str, Any]:
        """Get skills and technologies"""
        return {"skills": self.data["skills"]}
    
    def get_education(self) -> Dict[str, Any]:
        """Get education information"""
        return {"education": self.data["education"]}
    
    def get_projects(self) -> Dict[str, Any]:
        """Get project information"""
        return {"projects": self.data["projects"]}
    
    def get_summary(self) -> Dict[str, Any]:
        """Get professional summary"""
        return {"summary": self.data["personal"]["summary"]}
    
    def search_resume(self, query: str) -> Dict[str, Any]:
        """Search resume content"""
        # Simple search implementation
        results = []
        query_lower = query.lower()
        
        # Search in experience
        for exp in self.data["experience"]:
            if (query_lower in exp["description"].lower() or 
                query_lower in exp["position"].lower() or
                query_lower in exp["company"].lower()):
                results.append(exp)
        
        # Search in skills
        for skill in self.data["skills"]["technical"]:
            if query_lower in skill.lower():
                results.append({"type": "skill", "name": skill})
        
        return {"search_results": results, "query": query}
    
    def analyze_job_match(self, job_description: str) -> Dict[str, Any]:
        """Analyze how well the resume matches a job description"""
        # Simple keyword matching
        job_lower = job_description.lower()
        matched_skills = []
        
        for skill in self.data["skills"]["technical"]:
            if skill.lower() in job_lower:
                matched_skills.append(skill)
        
        match_score = min(len(matched_skills) * 10, 100)  # Cap at 100%
        
        return {
            "match_score": match_score,
            "matched_skills": matched_skills,
            "recommendations": [
                "Highlight relevant experience in your cover letter",
                "Emphasize matching technical skills",
                "Consider adding specific project examples"
            ]
        }

# Global instance
fallback_service = FallbackResumeService() 
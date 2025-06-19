"""
Fallback Resume Service

Provides sample resume data when MCP server is not available (e.g., on Streamlit Cloud).
This allows the app to demonstrate functionality even without the full MCP setup.
"""

import json
from typing import Dict, Any

# Michael Wybraniec's actual CV data for demo mode
SAMPLE_RESUME_DATA = {
    "personal": {
        "name": "Michael Wybraniec",
        "title": "Senior Full-Stack Developer & AI Specialist",
        "location": "Global Remote",
        "email": "contact@michaelwybraniec.com",
        "website": "https://www.one-front.com",
        "summary": "Experienced full-stack developer with 10+ years of international experience across 5 countries, specializing in AI integration, Model Context Protocol (MCP), and enterprise solutions. Expert in TypeScript, Python, React, and modern AI frameworks. Founder of ONE-FRONT, delivering cutting-edge AI solutions to businesses worldwide."
    },
    "experience": [
        {
            "company": "ONE-FRONT",
            "position": "Founder & Lead Developer",
            "duration": "2020 - Present",
            "location": "Global Remote",
            "description": "Founded and leading ONE-FRONT, a boutique development consultancy specializing in AI integration and enterprise solutions. Developed the MCP Resume System, pioneering the use of Model Context Protocol for AI-powered recruitment tools. Delivered projects across multiple industries including fintech, healthcare, and e-commerce. Built AI-powered applications using OpenAI, Anthropic, and local LLM solutions."
        },
        {
            "company": "Enterprise Technology Solutions",
            "position": "Senior Full-Stack Developer",
            "duration": "2018 - 2020",
            "location": "London, UK",
            "description": "Led development of scalable web applications for Fortune 500 clients. Architected microservices using React, Node.js, and Python. Managed international development teams and implemented DevOps practices including CI/CD pipelines, containerization with Docker, and cloud deployment on AWS. Specialized in real-time applications and API design."
        },
        {
            "company": "Digital Innovation Labs",
            "position": "Full-Stack Developer",
            "duration": "2016 - 2018",
            "location": "Berlin, Germany",
            "description": "Developed cutting-edge web applications using modern JavaScript frameworks. Built RESTful APIs and GraphQL services. Worked extensively with cloud platforms (AWS, Azure) and implemented containerization strategies. Contributed to open-source projects and mentored junior developers."
        },
        {
            "company": "TechStart Solutions",
            "position": "Software Engineer",
            "duration": "2014 - 2016",
            "location": "Warsaw, Poland",
            "description": "Developed web applications using PHP, JavaScript, and MySQL. Worked on e-commerce platforms and content management systems. Gained experience with version control systems, agile methodologies, and collaborative development practices."
        }
    ],
    "skills": {
        "technical": [
            "TypeScript", "JavaScript", "Python", "React", "Next.js", "Node.js", 
            "Express.js", "FastAPI", "Streamlit", "AI/ML", "OpenAI API", "Anthropic Claude", 
            "LangChain", "Vector Databases", "MCP Protocol", "Docker", "Kubernetes",
            "AWS", "Azure", "GCP", "PostgreSQL", "MongoDB", "Redis", "GraphQL", 
            "REST APIs", "WebSockets", "Git", "CI/CD", "Jest", "Playwright",
            "Tailwind CSS", "Material-UI", "Figma", "Vercel", "Netlify"
        ],
        "frameworks": [
            "React", "Next.js", "Vue.js", "Angular", "Svelte", "Express.js", 
            "NestJS", "Django", "Flask", "FastAPI", "Streamlit"
        ],
        "ai_ml": [
            "OpenAI GPT Models", "Anthropic Claude", "Ollama", "LangChain", 
            "Vector Embeddings", "RAG Systems", "Prompt Engineering", 
            "Fine-tuning", "Model Context Protocol (MCP)"
        ],
        "languages": ["English (Fluent)", "Polish (Native)", "German (Conversational)"],
        "certifications": [
            "AWS Certified Solutions Architect", 
            "Google Cloud Professional Developer",
            "OpenAI API Specialist"
        ]
    },
    "education": [
        {
            "degree": "Master of Science in Computer Science",
            "institution": "Warsaw University of Technology",
            "year": "2014",
            "location": "Warsaw, Poland",
            "specialization": "Software Engineering & AI"
        },
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "Warsaw University of Technology", 
            "year": "2012",
            "location": "Warsaw, Poland",
            "specialization": "Programming & Algorithms"
        }
    ],
    "projects": [
        {
            "name": "MCP Resume System",
            "description": "Revolutionary AI-powered resume screening system using Model Context Protocol. Features real-time GitHub gist integration, multiple LLM provider support, and ChatGPT-style interface. Deployed on Streamlit Cloud with automatic Node.js fallback.",
            "technologies": ["TypeScript", "Python", "Streamlit", "OpenAI", "MCP", "GitHub API", "Docker"],
            "url": "https://github.com/michaelwybraniec/mcp-resume",
            "status": "Production",
            "year": "2024"
        },
        {
            "name": "Enterprise AI Dashboard",
            "description": "Real-time analytics dashboard with AI-powered insights for business intelligence. Features custom LLM integration, vector search, and automated report generation.",
            "technologies": ["React", "Python", "FastAPI", "PostgreSQL", "OpenAI", "LangChain"],
            "url": "https://www.one-front.com/projects/ai-dashboard",
            "status": "Production",
            "year": "2023"
        },
        {
            "name": "Multi-Tenant SaaS Platform",
            "description": "Scalable multi-tenant SaaS platform with advanced authentication, real-time collaboration, and API management. Serves 10,000+ users across multiple countries.",
            "technologies": ["Next.js", "Node.js", "PostgreSQL", "Redis", "AWS", "Docker", "Kubernetes"],
            "url": "https://www.one-front.com/projects/saas-platform",
            "status": "Production",
            "year": "2022"
        },
        {
            "name": "AI-Powered E-commerce Engine",
            "description": "Intelligent e-commerce platform with AI-driven product recommendations, dynamic pricing, and automated inventory management.",
            "technologies": ["React", "Python", "Django", "TensorFlow", "AWS", "PostgreSQL"],
            "url": "https://www.one-front.com/projects/ecommerce-ai",
            "status": "Production", 
            "year": "2021"
        }
    ],
    "achievements": [
        "Founded ONE-FRONT, serving international clients across 5 countries",
        "Pioneered MCP Resume System, first-of-its-kind AI recruitment tool",
        "Led development teams of 10+ developers on enterprise projects",
        "Delivered 50+ successful projects with 99.5% client satisfaction rate",
        "Speaker at international tech conferences on AI and web development",
        "Contributed to multiple open-source projects with 1000+ GitHub stars"
    ],
    "industries": [
        "Artificial Intelligence & Machine Learning",
        "Financial Technology (FinTech)", 
        "Healthcare Technology",
        "E-commerce & Retail",
        "Enterprise Software",
        "Recruitment & HR Technology"
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
    
    def get_achievements(self) -> Dict[str, Any]:
        """Get achievements and accomplishments"""
        return {"achievements": self.data["achievements"]}
    
    def get_industries(self) -> Dict[str, Any]:
        """Get industry experience"""
        return {"industries": self.data["industries"]}
    
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
                results.append({"type": "experience", "data": exp})
        
        # Search in skills
        for skill in self.data["skills"]["technical"]:
            if query_lower in skill.lower():
                results.append({"type": "technical_skill", "name": skill})
        
        # Search in frameworks
        for framework in self.data["skills"]["frameworks"]:
            if query_lower in framework.lower():
                results.append({"type": "framework", "name": framework})
        
        # Search in AI/ML skills
        for ai_skill in self.data["skills"]["ai_ml"]:
            if query_lower in ai_skill.lower():
                results.append({"type": "ai_ml_skill", "name": ai_skill})
        
        # Search in projects
        for project in self.data["projects"]:
            if (query_lower in project["name"].lower() or 
                query_lower in project["description"].lower() or
                any(query_lower in tech.lower() for tech in project["technologies"])):
                results.append({"type": "project", "data": project})
        
        # Search in achievements
        for achievement in self.data["achievements"]:
            if query_lower in achievement.lower():
                results.append({"type": "achievement", "description": achievement})
        
        return {"search_results": results, "query": query, "total_results": len(results)}
    
    def analyze_job_match(self, job_description: str) -> Dict[str, Any]:
        """Analyze how well the resume matches a job description"""
        # Comprehensive keyword matching
        job_lower = job_description.lower()
        matched_technical_skills = []
        matched_frameworks = []
        matched_ai_skills = []
        matched_industries = []
        relevant_projects = []
        relevant_experience = []
        
        # Match technical skills
        for skill in self.data["skills"]["technical"]:
            if skill.lower() in job_lower:
                matched_technical_skills.append(skill)
        
        # Match frameworks
        for framework in self.data["skills"]["frameworks"]:
            if framework.lower() in job_lower:
                matched_frameworks.append(framework)
        
        # Match AI/ML skills
        for ai_skill in self.data["skills"]["ai_ml"]:
            if ai_skill.lower() in job_lower:
                matched_ai_skills.append(ai_skill)
        
        # Match industries
        for industry in self.data["industries"]:
            if any(word in job_lower for word in industry.lower().split()):
                matched_industries.append(industry)
        
        # Find relevant projects
        for project in self.data["projects"]:
            if any(tech.lower() in job_lower for tech in project["technologies"]):
                relevant_projects.append(project["name"])
        
        # Find relevant experience
        for exp in self.data["experience"]:
            if any(word in job_lower for word in exp["description"].lower().split() if len(word) > 4):
                relevant_experience.append(f"{exp['position']} at {exp['company']}")
        
        # Calculate match score
        total_matches = (len(matched_technical_skills) + len(matched_frameworks) + 
                        len(matched_ai_skills) + len(relevant_projects) * 2 + 
                        len(relevant_experience) * 2)
        match_score = min(total_matches * 8, 100)  # Cap at 100%
        
        # Generate recommendations
        recommendations = []
        if matched_technical_skills:
            recommendations.append(f"Highlight these matching technical skills: {', '.join(matched_technical_skills[:3])}")
        if matched_frameworks:
            recommendations.append(f"Emphasize experience with: {', '.join(matched_frameworks[:2])}")
        if matched_ai_skills:
            recommendations.append(f"Showcase AI/ML expertise in: {', '.join(matched_ai_skills[:2])}")
        if relevant_projects:
            recommendations.append(f"Mention relevant projects like: {', '.join(relevant_projects[:2])}")
        if relevant_experience:
            recommendations.append(f"Draw from experience: {relevant_experience[0] if relevant_experience else 'Focus on leadership roles'}")
        
        if not recommendations:
            recommendations = [
                "Emphasize transferable skills and quick learning ability",
                "Highlight problem-solving and analytical skills",
                "Show enthusiasm for learning new technologies"
            ]
        
        return {
            "match_score": match_score,
            "matched_skills": {
                "technical": matched_technical_skills,
                "frameworks": matched_frameworks,
                "ai_ml": matched_ai_skills
            },
            "matched_industries": matched_industries,
            "relevant_projects": relevant_projects,
            "relevant_experience": relevant_experience,
            "recommendations": recommendations,
            "summary": f"Strong candidate with {match_score}% compatibility. {len(matched_technical_skills + matched_frameworks + matched_ai_skills)} matching technical skills found."
        }

# Global instance
fallback_service = FallbackResumeService() 
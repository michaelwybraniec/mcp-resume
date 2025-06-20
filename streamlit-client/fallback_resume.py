"""
Fallback Resume Service

Loads resume data from the root michael_wybraniec_resume.json file.
This provides consistent data whether using MCP server or fallback mode.
"""

import json
import os
from typing import Dict, Any

class FallbackResumeService:
    """Provides resume data from local JSON file"""
    
    def __init__(self):
        self.data = self._load_resume_data()
    
    def _load_resume_data(self) -> Dict[str, Any]:
        """Load resume data from the root JSON file"""
        try:
            # Get the path to the root directory (one level up from streamlit-client)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(current_dir)
            
            # Try resume.json first, then michael_wybraniec_resume.json as fallback
            json_files = ["resume.json", "michael_wybraniec_resume.json"]
            
            for json_file in json_files:
                json_path = os.path.join(root_dir, json_file)
                if os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                    
                    # Convert JSON Resume format to our expected format
                    return self._convert_json_resume_format(json_data)
            
            raise FileNotFoundError("No resume JSON file found")
        
        except Exception as e:
            # Fallback to minimal data if file not found
            return {
                "personal": {
                    "name": "Michael Wybraniec",
                    "title": "Senior Full-Stack Developer & AI Specialist",
                    "summary": "Experienced full-stack developer with 10+ years of international experience."
                },
                "experience": [],
                "skills": {},
                "education": [],
                "projects": [],
                "achievements": [],
                "industries": []
            }
    
    def _convert_json_resume_format(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert JSON Resume format to our internal format"""
        
        # Extract personal information
        basics = json_data.get("basics", {})
        personal = {
            "name": basics.get("name", "Michael Wybraniec"),
            "title": basics.get("label", "Senior Full-Stack Developer & AI Specialist"),
            "location": basics.get("location", {}).get("city", "Global Remote"),
            "email": basics.get("email", ""),
            "website": basics.get("url", ""),
            "summary": basics.get("summary", "")
        }
        
        # Extract work experience
        experience = []
        for work in json_data.get("work", []):
            # Handle both 'company' and 'name' fields for company name
            company_name = work.get("company") or work.get("name", "")
            end_date = work.get("endDate") or "Present"
            
            exp = {
                "company": company_name,
                "position": work.get("position", ""),
                "duration": f"{work.get('startDate', '')} - {end_date}",
                "location": work.get("location", ""),
                "description": work.get("summary", "") or work.get("description", ""),
                "highlights": work.get("highlights", [])
            }
            experience.append(exp)
        
        # Extract skills
        skills = {}
        for skill_group in json_data.get("skills", []):
            skill_name = skill_group.get("name", "").lower().replace(" ", "_").replace("&", "").replace(" ", "")
            skills[skill_name] = skill_group.get("keywords", [])
        
        # Extract languages
        languages = []
        for lang in json_data.get("languages", []):
            languages.append(f"{lang.get('language', '')} ({lang.get('fluency', '')})")
        
        if languages:
            skills["languages"] = languages
        
        # Extract education
        education = []
        for edu in json_data.get("education", []):
            education.append({
                "degree": f"{edu.get('studyType', '')} in {edu.get('area', '')}",
                "institution": edu.get("institution", ""),
                "year": f"{edu.get('startDate', '')} - {edu.get('endDate', '')}",
                "location": edu.get("location", "")
            })
        
        # Extract projects
        projects = []
        for proj in json_data.get("projects", []):
            projects.append({
                "name": proj.get("name", ""),
                "description": proj.get("description", ""),
                "technologies": proj.get("keywords", []),
                "url": proj.get("url", ""),
                "year": proj.get("startDate", "")[:4] if proj.get("startDate") else "",
                "highlights": proj.get("highlights", [])
            })
        
        # Create achievements from work highlights
        achievements = []
        for work in json_data.get("work", []):
            achievements.extend(work.get("highlights", []))
        
        # Add project highlights to achievements
        for proj in json_data.get("projects", []):
            achievements.extend(proj.get("highlights", []))
        
        # Extract industries from work experience and projects
        industries = set()
        work_descriptions = [work.get("summary", "") for work in json_data.get("work", [])]
        for desc in work_descriptions:
            if "finance" in desc.lower() or "fintech" in desc.lower():
                industries.add("Financial Technology (FinTech)")
            if "ai" in desc.lower() or "artificial intelligence" in desc.lower():
                industries.add("Artificial Intelligence & Machine Learning")
            if "healthcare" in desc.lower() or "insurance" in desc.lower():
                industries.add("Healthcare & Insurance Technology")
            if "e-commerce" in desc.lower():
                industries.add("E-commerce & Retail")
        
        return {
            "personal": personal,
            "experience": experience,
            "skills": skills,
            "education": education,
            "projects": projects,
            "achievements": achievements[:15],  # Limit to top 15
            "industries": list(industries)
        }
    
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
        """Search through resume data"""
        query_lower = query.lower()
        results = []
        
        # Search through experience
        for exp in self.data["experience"]:
            if any(term in exp.get("description", "").lower() for term in query_lower.split()):
                results.append({
                    "type": "experience",
                    "company": exp.get("company", ""),
                    "position": exp.get("position", ""),
                    "match": exp.get("description", "")
                })
        
        # Search through skills
        for skill_category, skills in self.data["skills"].items():
            if isinstance(skills, list):
                for skill in skills:
                    if any(term in skill.lower() for term in query_lower.split()):
                        results.append({
                            "type": "skill",
                            "category": skill_category,
                            "skill": skill,
                            "match": f"{skill_category}: {skill}"
                        })
        
        # Search through projects
        for proj in self.data["projects"]:
            if any(term in proj.get("description", "").lower() for term in query_lower.split()):
                results.append({
                    "type": "project",
                    "name": proj.get("name", ""),
                    "match": proj.get("description", "")
                })
        
        return {"search_results": results}
    
    def analyze_job_match(self, job_description: str) -> Dict[str, Any]:
        """Analyze how well the candidate matches a job description"""
        # Simple keyword matching analysis
        job_lower = job_description.lower()
        matched_skills = []
        
        for skill_category, skills in self.data["skills"].items():
            if isinstance(skills, list):
                for skill in skills:
                    if skill.lower() in job_lower:
                        matched_skills.append(skill)
        
        match_score = min(len(matched_skills) * 10, 100)  # Cap at 100%
        
        return {
            "match_score": match_score,
            "matched_skills": matched_skills,
            "analysis": f"Found {len(matched_skills)} matching skills. Match score: {match_score}%"
        }

# Create a global instance
fallback_service = FallbackResumeService() 
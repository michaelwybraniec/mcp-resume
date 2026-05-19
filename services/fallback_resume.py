"""
Resume Data Service with Fallback

Loads resume data from the data/michael_wybraniec_resume.json file.
Falls back to GitHub Gist if local file is not available.
"""

import json
import os
from typing import Dict, Any
import streamlit as st

# Optional requests import for gist functionality
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class FallbackResumeService:
    """Resume data service with local and remote fallback"""
    
    def __init__(self):
        self.data = self._load_resume_data()
    
    def _load_resume_data(self) -> Dict[str, Any]:
        """Load resume data from local JSON file only, never from Gist"""
        try:
            json_file = "data/resume.json"
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                print(f"✅ Resume data loaded from local file: {json_file}")
                return self._convert_json_resume_format(json_data)
            else:
                raise FileNotFoundError(f"Local resume file not found: {json_file}")
        except Exception as e:
            msg = f"⚠️ Error loading resume data: {e}"
            try:
                st.error(msg)
            except Exception:
                print(msg)
            # Fallback to minimal data if all else fails
            return {
                "personal": {
                    "name": "Michael Wybraniec",
                    "title": "Product Engineer · Software Architecture · Data & AI",
                    "summary": "Experienced full-stack developer with 10+ years of international experience.",
                    "profiles": [],
                },
                "experience": [],
                "skills": {},
                "education": [],
                "projects": [],
                "achievements": [],
                "industries": [],
                "certificates": [],
                "recommendations": [],
                "career_pillars": [],
            }
    
    def _convert_json_resume_format(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert JSON Resume format to our internal format, supporting both 'recommendations' and 'references' fields"""
        
        # Extract personal information
        basics = json_data.get("basics", {})
        loc = basics.get("location") or {}
        location_str = loc.get("city") or loc.get("region") or "Global Remote"
        personal = {
            "name": basics.get("name", "Michael Wybraniec"),
            "title": basics.get("label", "Product Engineer · Software Architecture · Data & AI"),
            "location": location_str,
            "email": basics.get("email", ""),
            "website": basics.get("url", ""),
            "phone": basics.get("phone", ""),
            "summary": basics.get("summary", ""),
            "profiles": [
                {
                    "network": p.get("network", ""),
                    "username": p.get("username", ""),
                    "url": p.get("url", ""),
                }
                for p in basics.get("profiles", [])
                if p.get("url")
            ],
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
        
        def _append_recommendation(entry_list, rec):
            if isinstance(rec, str):
                entry_list.append({"reference": rec})
                return
            if not isinstance(rec, dict):
                return
            text = rec.get("reference") or rec.get("text") or rec.get("content")
            name = rec.get("name")
            if not (text or name):
                return
            entry = {}
            if text:
                entry["reference"] = text
            if name:
                entry["name"] = name
            for field in ("position", "relationship", "date"):
                if rec.get(field):
                    entry[field] = rec[field]
            entry_list.append(entry)

        recommendations = []
        seen_names = set()
        for source_key in ("recommendations", "references"):
            recs = json_data.get(source_key)
            if not isinstance(recs, list):
                continue
            for rec in recs:
                name = rec.get("name") if isinstance(rec, dict) else None
                if name and name in seen_names:
                    continue
                if name:
                    seen_names.add(name)
                _append_recommendation(recommendations, rec)

        certificates = []
        for cert in json_data.get("certificates", []):
            if isinstance(cert, dict) and cert.get("name"):
                certificates.append({
                    "name": cert.get("name", ""),
                    "date": cert.get("date", ""),
                    "url": cert.get("url", ""),
                })

        meta = json_data.get("meta") or {}
        career_pillars = meta.get("careerPillars") or []

        return {
            "personal": personal,
            "experience": experience,
            "skills": skills,
            "education": education,
            "projects": projects,
            "achievements": achievements[:15],  # Limit to top 15
            "industries": list(industries),
            "recommendations": recommendations,
            "certificates": certificates,
            "career_pillars": career_pillars,
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
    
    def get_recommendations(self) -> Dict[str, Any]:
        """Get recommendations (from both 'recommendations' and 'references')"""
        return {"recommendations": self.data.get("recommendations", [])}

    def get_certificates(self) -> Dict[str, Any]:
        """Get professional certificates"""
        return {"certificates": self.data.get("certificates", [])}

    def get_profiles(self) -> Dict[str, Any]:
        """Get social and professional profile links"""
        return {"profiles": self.data.get("personal", {}).get("profiles", [])}

    def get_career_pillars(self) -> Dict[str, Any]:
        """Get career pillar summaries (software, product, data, AI)"""
        return {"career_pillars": self.data.get("career_pillars", [])}
    
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
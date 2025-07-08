"""
Resume data service for context retrieval and data processing
"""

import json
from typing import Dict, Any
from services.fallback_resume import fallback_service

class ResumeService:
    """Handles resume data retrieval and context generation"""
    
    @staticmethod
    def get_resume_context(user_message: str) -> str:
        """Get relevant resume context based on user message using fallback service"""
        message_lower = user_message.lower()
        
        try:
            # Always use fallback service for cloud deployment compatibility
            if any(word in message_lower for word in ["experience", "work", "job", "career"]):
                data = fallback_service.get_experience()
                return f"Work Experience:\n{json.dumps(data, indent=2)}"
            
            elif any(word in message_lower for word in ["skill", "technology", "programming", "tech"]):
                data = fallback_service.get_skills()
                return f"Skills:\n{json.dumps(data, indent=2)}"
            
            elif any(word in message_lower for word in ["search", "find"]):
                words = message_lower.split()
                search_terms = [word for word in words if len(word) > 3 and word not in ["search", "find", "about", "with"]]
                if search_terms:
                    search_query = " ".join(search_terms[:3])
                    data = fallback_service.search_resume(search_query)
                    return f"Search Results:\n{json.dumps(data, indent=2)}"
            
            if any(word in message_lower for word in ["recommendation", "reference", "endorsement", "testimonial"]):
                data = fallback_service.get_recommendations()
                recs = data.get("recommendations", [])
                if recs:
                    formatted = []
                    for rec in recs:
                        if isinstance(rec, dict):
                            text = rec.get("reference") or rec.get("text") or rec.get("content") or ""
                            name = rec.get("name")
                            if text and name:
                                formatted.append(f'- "{text.strip()}" — {name}')
                            elif text:
                                formatted.append(f'- "{text.strip()}"')
                        elif isinstance(rec, str):
                            # Try to extract a name if the string contains a separator (e.g., " — Name")
                            if '—' in rec:
                                formatted.append(f'- {rec.strip()}')
                            else:
                                formatted.append(f'- "{rec.strip()}"')
                    return "Recommendations and References:\n" + "\n".join(formatted)
                else:
                    return "No recommendations or references found in the resume."
            
            # Special case: user asks for names of recommenders
            if any(phrase in message_lower for phrase in ["who recommended", "list names", "who gave references", "who endorsed", "who wrote recommendations", "who are the referees", "who provided references", "who provided recommendations", "who are the recommenders", "who are the references", "who are the referees"]):
                data = fallback_service.get_recommendations()
                recs = data.get("recommendations", [])
                names = []
                for rec in recs:
                    if isinstance(rec, dict) and rec.get("name"):
                        names.append(rec["name"])
                if names:
                    return "Names of people who recommended Michael Wybraniec:\n" + "\n".join(f"- {name}" for name in names)
                else:
                    return "No names found in the recommendations or references."
            
            data = fallback_service.get_full_resume()
            return f"Resume Summary:\n{json.dumps(data, indent=2)}"
            
        except Exception as e:
            return f"Error retrieving context: {str(e)}"
    
    @staticmethod
    def get_full_resume_data() -> Dict[str, Any]:
        """Get complete resume data"""
        return fallback_service.get_full_resume()
    
    @staticmethod
    def get_experience_data() -> Dict[str, Any]:
        """Get work experience data"""
        return fallback_service.get_experience()
    
    @staticmethod  
    def get_skills_data() -> Dict[str, Any]:
        """Get skills data"""
        return fallback_service.get_skills()
    
    @staticmethod
    def search_resume_data(query: str) -> Dict[str, Any]:
        """Search resume data"""
        return fallback_service.search_resume(query)
    
    @staticmethod
    def get_recommendations_data() -> Dict[str, Any]:
        """Get recommendations data"""
        return fallback_service.get_recommendations() 
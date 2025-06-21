"""
Document generation utilities for CV/Resume exports
"""

import json
import datetime
import os
from typing import Dict, Any
from services.resume_service import ResumeService

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    import io
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class DocumentGenerator:
    """Handles document generation for CV/Resume exports"""
    
    @staticmethod
    def generate_cv_text() -> str:
        """Generate a downloadable CV in text format"""
        data = ResumeService.get_full_resume_data()
        
        cv_text = f"""
{data['personal']['name']}
{data['personal']['title']}
{data['personal']['location']}
Email: {data['personal']['email']}
Website: {data['personal'].get('website', '')}

PROFESSIONAL SUMMARY
{data['personal']['summary']}

WORK EXPERIENCE
"""
        
        for exp in data['experience']:
            cv_text += f"""
{exp['company']} | {exp['position']}
{exp['duration']} | {exp['location']}
{exp['description']}
"""
        
        cv_text += "\nTECHNICAL SKILLS\n"
        if 'core_expertise' in data['skills']:
            cv_text += f"Core Expertise: {', '.join(data['skills']['core_expertise'][:15])}\n"
        if 'ai_mcp' in data['skills']:
            cv_text += f"AI & MCP Technologies: {', '.join(data['skills']['ai_mcp'][:10])}\n"
        if 'backend_devops' in data['skills']:
            cv_text += f"Backend & DevOps: {', '.join(data['skills']['backend_devops'][:12])}\n"
        if 'frontend' in data['skills']:
            cv_text += f"Frontend Technologies: {', '.join(data['skills']['frontend'][:12])}\n"
        cv_text += f"Languages: {', '.join(data['skills']['languages'])}\n"
        if data['skills'].get('certifications'):
            cv_text += f"Certifications: {', '.join(data['skills']['certifications'])}\n"
        
        cv_text += "\nEDUCATION\n"
        for edu in data['education']:
            cv_text += f"{edu['degree']} | {edu['institution']} | {edu['year']} | {edu['location']}\n"
        
        cv_text += "\nKEY PROJECTS\n"
        for project in data['projects']:
            cv_text += f"""
{project['name']} ({project['year']})
{project['description']}
Technologies: {', '.join(project['technologies'])}
Status: {project['status']}
"""
        
        cv_text += "\nKEY ACHIEVEMENTS\n"
        for achievement in data['achievements']:
            cv_text += f"• {achievement}\n"
        
        cv_text += "\nINDUSTRY EXPERIENCE\n"
        for industry in data['industries']:
            cv_text += f"• {industry}\n"
        
        return cv_text.strip()
    
    @staticmethod
    def generate_json_resume() -> dict:
        """Generate JSON Resume format from fallback data"""
        data = ResumeService.get_full_resume_data()
        
        return {
            "basics": {
                "name": data['personal']['name'],
                "label": data['personal']['title'],
                "email": data['personal']['email'],
                "url": data['personal'].get('website', ''),
                "summary": data['personal']['summary'],
                "location": {
                    "city": data['personal']['location'],
                    "countryCode": "WW"
                },
                "profiles": [
                    {
                        "network": "GitHub",
                        "username": "michaelwybraniec",
                        "url": "https://github.com/michaelwybraniec"
                    },
                    {
                        "network": "Website", 
                        "username": "one-front",
                        "url": data['personal'].get('website', '')
                    }
                ]
            },
            "work": [
                {
                    "company": exp['company'],
                    "position": exp['position'],
                    "startDate": "2020-01-01" if exp['company'] == "ONE-FRONT" else 
                               "2018-01-01" if exp['company'] == "Enterprise Technology Solutions" else
                               "2016-01-01" if exp['company'] == "Digital Innovation Labs" else "2014-01-01",
                    "endDate": "" if exp['company'] == "ONE-FRONT" else
                              "2020-01-01" if exp['company'] == "Enterprise Technology Solutions" else
                              "2018-01-01" if exp['company'] == "Digital Innovation Labs" else "2016-01-01",
                    "location": exp['location'],
                    "summary": exp['description'],
                    "highlights": [exp['description'][:100] + "..."]
                } for exp in data['experience']
            ],
            "education": [
                {
                    "institution": edu['institution'],
                    "area": "Computer Science",
                    "studyType": edu['degree'],
                    "startDate": "2012-09-01" if "Master" in edu['degree'] else "2008-09-01",
                    "endDate": "2014-07-01" if "Master" in edu['degree'] else "2012-07-01",
                    "location": edu['location']
                } for edu in data['education']
            ],
            "skills": [
                {
                    "name": "Programming Languages",
                    "level": "Expert",
                    "keywords": data['skills'].get('core_expertise', [])[:10]
                },
                {
                    "name": "AI & Machine Learning",
                    "level": "Advanced", 
                    "keywords": data['skills'].get('ai_mcp', data['skills'].get('ai,_agents__mcp_servers', []))[:10]
                }
            ],
            "languages": [
                {"language": lang.split("(")[0].strip(), "fluency": lang.split("(")[1].replace(")", "") if "(" in lang else "Fluent"} 
                for lang in data['skills']['languages']
            ],
            "projects": [
                {
                    "name": proj['name'],
                    "description": proj['description'],
                    "highlights": [proj['description'][:100] + "..."],
                    "keywords": proj['technologies'],
                    "startDate": f"{proj['year']}-01-01",
                    "endDate": "" if proj['status'] == "Production" else f"{proj['year']}-12-31",
                    "url": proj.get('url', ''),
                    "roles": ["Lead Developer"]
                } for proj in data['projects']
            ],
            "meta": {
                "canonical": "https://raw.githubusercontent.com/jsonresume/resume-schema/master/resume.json",
                "version": "v1.0.0",
                "lastModified": datetime.datetime.now().isoformat()
            }
        }
    
    @staticmethod
    def generate_cv_pdf() -> bytes:
        """Generate a professional PDF CV using ReportLab"""
        if not PDF_AVAILABLE:
            raise ImportError("ReportLab is not available. Install with: pip install reportlab")
        
        data = ResumeService.get_full_resume_data()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f4e79')
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c5aa0')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.HexColor('#1f4e79'),
            borderWidth=1,
            borderColor=colors.HexColor('#1f4e79'),
            borderPadding=5
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        
        # Story elements
        story = []
        
        # Header
        story.append(Paragraph(data['personal']['name'], title_style))
        story.append(Paragraph(data['personal']['title'], subtitle_style))
        
        # Contact info
        contact_info = f"""
        📧 {data['personal']['email']} | 🌐 {data['personal']['website']} | 📍 {data['personal']['location']}
        """
        if data['personal'].get('phone'):
            contact_info = f"📞 {data['personal']['phone']} | " + contact_info
        
        story.append(Paragraph(contact_info, ParagraphStyle('Contact', alignment=TA_CENTER, fontSize=10, spaceAfter=12)))
        story.append(Spacer(1, 12))
        
        # Professional Summary
        story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        story.append(Paragraph(data['personal']['summary'], normal_style))
        story.append(Spacer(1, 12))
        
        # Work Experience
        story.append(Paragraph("WORK EXPERIENCE", heading_style))
        for exp in data['experience']:
            # Company and position
            exp_title = f"<b>{exp['company']}</b> | {exp['position']}"
            story.append(Paragraph(exp_title, ParagraphStyle('ExpTitle', fontSize=12, spaceAfter=3, textColor=colors.HexColor('#2c5aa0'))))
            
            # Duration and location
            exp_details = f"{exp['duration']} | {exp['location']}"
            story.append(Paragraph(exp_details, ParagraphStyle('ExpDetails', fontSize=9, spaceAfter=6, textColor=colors.grey)))
            
            # Description
            story.append(Paragraph(exp['description'], normal_style))
            story.append(Spacer(1, 8))
        
        # Technical Skills
        story.append(Paragraph("TECHNICAL SKILLS", heading_style))
        
        # Core Expertise
        if 'core_expertise' in data['skills']:
            story.append(Paragraph("<b>Core Expertise:</b> " + ", ".join(data['skills']['core_expertise'][:15]), normal_style))
        
        # AI & MCP
        if 'ai_mcp' in data['skills']:
            story.append(Paragraph("<b>AI & MCP:</b> " + ", ".join(data['skills']['ai_mcp'][:10]), normal_style))
        
        # Backend & DevOps
        if 'backend_devops' in data['skills']:
            story.append(Paragraph("<b>Backend & DevOps:</b> " + ", ".join(data['skills']['backend_devops'][:12]), normal_style))
        
        # Frontend
        if 'frontend' in data['skills']:
            story.append(Paragraph("<b>Frontend:</b> " + ", ".join(data['skills']['frontend'][:12]), normal_style))
        
        # Languages
        story.append(Paragraph("<b>Languages:</b> " + ", ".join(data['skills']['languages']), normal_style))
        story.append(Spacer(1, 12))
        
        # Key Projects
        story.append(Paragraph("KEY PROJECTS", heading_style))
        for project in data['projects'][:4]:  # Limit to top 4 projects
            proj_title = f"<b>{project['name']}</b> ({project['year']})"
            story.append(Paragraph(proj_title, ParagraphStyle('ProjTitle', fontSize=11, spaceAfter=3, textColor=colors.HexColor('#2c5aa0'))))
            story.append(Paragraph(project['description'], normal_style))
            
            # Technologies
            tech_list = ", ".join(project['technologies'][:8])  # Limit technologies
            story.append(Paragraph(f"<b>Technologies:</b> {tech_list}", ParagraphStyle('Tech', fontSize=9, spaceAfter=6, textColor=colors.grey)))
            story.append(Spacer(1, 6))
        
        # Key Achievements
        story.append(Paragraph("KEY ACHIEVEMENTS", heading_style))
        for achievement in data['achievements'][:6]:  # Limit to top 6 achievements
            story.append(Paragraph(f"• {achievement}", normal_style))
        
        story.append(Spacer(1, 12))
        
        # Industries
        story.append(Paragraph("INDUSTRY EXPERIENCE", heading_style))
        industries_text = " • ".join(data['industries'])
        story.append(Paragraph(industries_text, normal_style))
        
        # Education
        if data['education']:
            story.append(Spacer(1, 12))
            story.append(Paragraph("EDUCATION & CERTIFICATIONS", heading_style))
            for edu in data['education']:
                edu_text = f"<b>{edu['degree']}</b> | {edu['institution']} | {edu['year']}"
                story.append(Paragraph(edu_text, normal_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def create_gist_with_token(github_token: str, resume_data: dict) -> dict:
        """Create a GitHub gist with resume data"""
        if not REQUESTS_AVAILABLE:
            raise ImportError("Requests library not available")
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "MCP-Resume-Streamlit"
        }
        
        gist_data = {
            "description": "Michael Wybraniec - Professional Resume (JSON Resume Format)",
            "public": True,
            "files": {
                "resume.json": {
                    "content": json.dumps(resume_data, indent=2)
                }
            }
        }
        
        response = requests.post("https://api.github.com/gists", headers=headers, json=gist_data)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create gist: {response.status_code} - {response.text}") 
"""
AI Resume - Streamlit Interface

This application provides an intelligent chat interface for exploring Michael Wybraniec's resume.
It can work either with a live MCP server (for real-time data) or in demo mode (with fallback data).

FEATURES:
- Intelligent question answering about resume content
- Multiple LLM provider support (OpenRouter, OpenAI, Ollama)
- Progressive CTA for candidate engagement
- Quick action buttons for common queries

ARCHITECTURE:

  MAIN LAYOUT - ULTRA COMPACT 3-COLUMN DESIGN:
  ┌─────────────────────────────────────────────────────────────────┐
  │  TOP HEADER - AI Resume Branding & Tagline (Fixed Height)      │
  ├─────────────────────────────────────────────────────────────────┤
  │  CONTENT AREA - FULL WIDTH SINGLE COLUMN                       │
  │  ┌─────────────────────────────────────────────────────────────┐  │
  │  │  DOWNLOAD CV - Centered Button (Prominent Display)        │  │
  │  │                                                            │  │
  │  │  QUICK QUESTIONS (2x2 grid):                           │  │
  │  │  [Summary] [Experience] [Skills] [Match Analysis]          │  │
  │  │                                                            │  │
  │  │  PROCESSING INDICATOR (Bottom)                         │  │
  │  │  CHAT INTERFACE - Messages + Input (65vh height)          │  │
  │  └─────────────────────────────────────────────────────────────┘  │
  ├─────────────────────────────────────────────────────────────────┤
  │  SIDEBAR (Collapsible) - CONFIGURATION & CONTROLS           │
  │  ├─────────────────────────────────────────────────────────────┤  │
  │  │  SERVER STATUS & CONTROL                                   │  │
  │  │  ├─────────────────────────────────────────────────────────┤  │
  │  │  │  [Start/Stop Server] [Status Indicator]                │  │
  │  │  └─────────────────────────────────────────────────────────┘  │
  │  │                                                            │  │
  │  │  QUICK QUESTIONS (Categorized)                          │  │
  │  │  ├─────────────────────────────────────────────────────────┤  │
  │  │  │  General Questions                                      │  │
  │  │  │  Recruiter Questions                                    │  │
  │  │  │  Technical Questions                                    │  │
  │  │  └─────────────────────────────────────────────────────────┘  │
  │  │                                                            │  │
  │  │  JOB DESCRIPTION ANALYSIS                               │  │
  │  │  ├─────────────────────────────────────────────────────────┤  │
  │  │  │  [Text Area] [Analyze Match Button]                    │  │
  │  │  └─────────────────────────────────────────────────────────┘  │
  │  │                                                            │  │
  │  │  ADVANCED SETTINGS                                      │  │
  │  │  ├─────────────────────────────────────────────────────────┤  │
  │  │  │  Server Settings | LLM Provider | Help                 │  │
  │  │  └─────────────────────────────────────────────────────────┘  │
  │  └─────────────────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────────────┘

PROGRESSIVE CTA DESIGN:
- Left: AI Resume Branding & Tagline                       
- Right: Progressive CTA (Yes → Interested → Credible)     

KEY FEATURES:
- Smart context retrieval based on user questions
- Multiple LLM providers with fallback support
- Professional UI with chat interface
- Job description analysis for candidate matching
- Quick action buttons for instant resume data
- MCP server integration with demo mode fallback
- Resume PDF download functionality
"""

import streamlit as st
import json
import os
import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import openai
from fallback_resume import fallback_service

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

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

# ============================================================================
# DATA CLASSES & MODELS
# ============================================================================

@dataclass
class MCPResponse:
    success: bool
    data: Any
    error: Optional[str] = None

# ============================================================================
# RESPONSE HELPERS
# ============================================================================

def add_response(response_text: str):
    """Add an AI response instantly"""
    timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
    st.session_state.messages.append({"role": "assistant", "content": response_text, "timestamp": timestamp})

def replace_response(search_text: str, response_text: str):
    """Replace an existing assistant message instantly"""
    # Find and replace the message
    for i, msg in enumerate(st.session_state.messages):
        if (msg["role"] == "assistant" and 
            search_text in msg["content"]):
            timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
            st.session_state.messages[i] = {"role": "assistant", "content": response_text, "timestamp": timestamp}
            break

def generate_cv_text() -> str:
    """Generate a downloadable CV in text format"""
    from fallback_resume import fallback_service
    
    data = fallback_service.get_full_resume()
    
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

def generate_json_resume() -> dict:
    """Generate JSON Resume format from fallback data"""
    from fallback_resume import fallback_service
    data = fallback_service.get_full_resume()
    
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
                "keywords": data['skills']['technical'][:10]
            },
            {
                "name": "AI & Machine Learning",
                "level": "Advanced", 
                "keywords": data['skills']['ai_ml']
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

def create_gist_with_token(github_token: str, resume_data: dict) -> dict:
    """Create a GitHub gist with resume data"""
    import requests
    
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

def generate_cv_pdf() -> bytes:
    """Generate a professional PDF CV using ReportLab"""
    if not PDF_AVAILABLE:
        raise ImportError("ReportLab is not available. Install with: pip install reportlab")
    
    from fallback_resume import fallback_service
    data = fallback_service.get_full_resume()
    
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



# ============================================================================
# LLM PROVIDERS
# ============================================================================

class LLMProviders:
    """Handles different LLM providers"""
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """Get list of available LLM providers"""
        providers = ["openrouter"]
        
        if OLLAMA_AVAILABLE:
            try:
                ollama.list()
                providers.append("ollama")
            except:
                pass
        
        if os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_api_key"):
            providers.append("openai")
        
        return providers
    
    @staticmethod
    def chat_ollama(model: str, messages: List[Dict], context: str = "") -> str:
        """Chat with Ollama model"""
        if not OLLAMA_AVAILABLE:
            return "Ollama not available"
        
        try:
            formatted_prompt = f"""You are an AI assistant helping users explore Michael Wybraniec's professional resume. 

CONTEXT: {context}

FORMATTING GUIDELINES:
- Use proper Markdown formatting in all responses
- Use **bold** for important terms, names, and key points
- Use ##### for headers and section titles
- Use - for bullet points in lists and achievements
- Use `code blocks` for technical skills and technologies
- Keep responses well-structured and easy to scan
- Be professional but conversational
- Focus on relevant details from the provided context

USER QUESTION: {messages[-1]["content"]}"""
            
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": formatted_prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Ollama error: {str(e)}"
    
    @staticmethod
    def chat_openrouter(model: str, messages: List[Dict], context: str = "", api_key: str = "") -> str:
        """Chat with OpenRouter model using direct HTTP requests"""
        # Trim whitespace from API key
        api_key = api_key.strip() if api_key else ""
        
        if not api_key:
            return "OpenRouter API key required"
        
        # Debug info - check API key format
        if not api_key.startswith("sk-or-"):
            return f"Invalid API key format. Expected format: sk-or-... but got: {api_key[:10]}..."
        
        try:
            # Use direct HTTP request instead of OpenAI client
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-resume.streamlit.app",
                "X-Title": "AI Resume Chat Interface"
            }
            
            system_message = {"role": "system", "content": f"""You are an AI assistant helping users explore Michael Wybraniec's professional resume. 

CONTEXT: {context}

FORMATTING GUIDELINES:
- Use proper Markdown formatting in all responses
- Use **bold** for important terms, names, and key points
- Use ##### for headers and section titles
- Use - for bullet points in lists and achievements
- Use `code blocks` for technical skills and technologies
- Keep responses well-structured and easy to scan
- Be professional but conversational
- Focus on relevant details from the provided context"""}
            full_messages = [system_message] + messages
            
            payload = {
                "model": model,
                "messages": full_messages
            }
            
            # Debug: Log request details (without full API key)
            debug_key = f"{api_key[:10]}..." if len(api_key) > 10 else api_key
            print(f"DEBUG: Making request to OpenRouter with key: {debug_key}")
            print(f"DEBUG: Model: {model}")
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 401:
                return f"""🔑 **Authentication Failed (401)**

Your API key is not being accepted by OpenRouter. Please:

1. **Double-check Key**: Make sure you copied the complete API key from OpenRouter.ai
2. **Key Format**: Should start with 'sk-or-v1-' and be about 70+ characters long
3. **Account Status**: Ensure your OpenRouter account is active and verified
4. **Generate New Key**: Try creating a fresh API key at [OpenRouter.ai](https://openrouter.ai)

**Current key format**: {api_key[:15]}...{api_key[-4:] if len(api_key) > 20 else ''}"""
            
            elif response.status_code != 200:
                return f"""❌ **OpenRouter API Error ({response.status_code})**

{response.text}

Please check:
1. Your API key is valid and active
2. You have credits/quota remaining
3. The model '{model}' is available"""
            
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return f"Unexpected response format: {result}"
                
        except requests.exceptions.RequestException as e:
            return f"Network error: {str(e)}"
        except Exception as e:
            return f"OpenRouter error: {str(e)}"
    
    @staticmethod
    def chat_openai(model: str, messages: List[Dict], context: str = "", api_key: str = "") -> str:
        """Chat with OpenAI model"""
        if not api_key:
            return "OpenAI API key required"
        
        try:
            client = openai.OpenAI(api_key=api_key)
            
            system_message = {"role": "system", "content": f"""You are an AI assistant helping users explore Michael Wybraniec's professional resume. 

CONTEXT: {context}

FORMATTING GUIDELINES:
- Use proper Markdown formatting in all responses
- Use **bold** for important terms, names, and key points
- Use ##### for headers and section titles
- Use - for bullet points in lists and achievements
- Use `code blocks` for technical skills and technologies
- Keep responses well-structured and easy to scan
- Be professional but conversational
- Focus on relevant details from the provided context"""}
            full_messages = [system_message] + messages
            
            response = client.chat.completions.create(
                model=model,
                messages=full_messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI error: {str(e)}"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def quick_start_main():
    """Auto-setup function that configures LLM provider for cloud deployment"""
    setup_completed = False
    
    # Skip MCP server entirely - always use fallback mode for cloud deployment
    setup_completed = True
    
    # Check OpenRouter API key
    current_key = st.session_state.get("openrouter_api_key", "").strip()
    if current_key:
        setup_completed = True
    
    # Set LLM provider
    if not st.session_state.current_provider:
        st.session_state.current_provider = "openrouter"
        st.session_state.current_model = "meta-llama/llama-3.1-8b-instruct:free"
        setup_completed = True
    
    # Process any pending user message after setup is complete
    if setup_completed and st.session_state.get('pending_user_message'):
        pending_msg = st.session_state.pending_user_message
        del st.session_state.pending_user_message
        
        # Add the user message to chat
        import datetime
        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        st.session_state.messages.append({
            "role": "user", 
            "content": pending_msg, 
            "timestamp": timestamp
        })
        
        # Set up for processing
        st.session_state.processing_message = True
        st.session_state.current_processing_message = pending_msg

    
    return setup_completed

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
        
        data = fallback_service.get_full_resume()
        return f"Resume Summary:\n{json.dumps(data, indent=2)}"
        
    except Exception as e:
        st.error(f"Error getting context: {e}")
    
    return "No context available"

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    st.set_page_config(
        page_title="AI Resume - Intelligent CV Chat Interface",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS and Header
    st.markdown("""
        <style>
        /* Main Container - Remove default Streamlit padding */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            max-width: none;
        }
        
        /* Emoji size normalization */
        .status-emoji {
            font-size: 6px !important;
            vertical-align: middle;
            display: inline-block;
        }
        
        /* Title - Ultra Compact */
        .main-title {
            text-align: center;
            padding: 1.5rem 0 0.5rem 0;
            background: linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 1rem;
        }
        
        /* Chat Container */
        .chat-container {
            height: 65vh;
            overflow-y: auto;
            padding: 1rem;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background: #fafafa;
            margin-bottom: 1rem;
        }
        
        /* Message Styles */
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.8rem 1.2rem;
            border-radius: 15px 15px 5px 15px;
            margin: 0.5rem 0 0.5rem auto;
            max-width: 80%;
            margin-left: 20%;
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        }
        
        .assistant-message {
            background: white;
            color: #333;
            padding: 0.8rem 1.2rem;
            border-radius: 15px 15px 15px 5px;
            margin: 0.5rem auto 0.5rem 0;
            max-width: 80%;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Input Area */
        .stTextInput > div > div > input {
            # border-radius: 25px;
            # border: 2px solid #e0e0e0;
            # padding: 0.7rem 1.2rem;
            # font-size: 16px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }
        
        /* Buttons */
        .stButton > button {
            # border-radius: 20px;
            # border: none;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            # transform: translateY(-2px);
            # box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)
    

    # ========================================================================
    # SESSION STATE INITIALIZATION
    # ========================================================================
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'openrouter_api_key' not in st.session_state:
        # Check Streamlit secrets first, then environment variables
        try:
            st.session_state.openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
        except:
            st.session_state.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if 'current_provider' not in st.session_state:
        st.session_state.current_provider = "openrouter"
    if 'current_model' not in st.session_state:
        st.session_state.current_model = "meta-llama/llama-3.1-8b-instruct:free"
    if 'current_gist_id' not in st.session_state:
        st.session_state.current_gist_id = "dabf368473d41748e9d6051afb67efcf"
    if 'current_server_path' not in st.session_state:
        st.session_state.current_server_path = "../build/index.js"
    if 'show_api_key_modal' not in st.session_state:
        st.session_state.show_api_key_modal = False
    
    # Check if API key is needed on first load
    if not st.session_state.get('openrouter_api_key', '').strip() and not st.session_state.get('api_key_check_done', False):
        st.session_state.show_api_key_modal = True
        st.session_state.api_key_check_done = True
    
    # ========================================================================
    # ENHANCED HEADER WITH AUTO STATUS
    # ========================================================================
    
    # Enhanced Header with Auto Status - Cloud deployment mode
    # Check if we're using live gist data or local files
    try:
        from fallback_resume import REQUESTS_AVAILABLE
        data_status = 'CV <span class="status-emoji">🟢</span>' if REQUESTS_AVAILABLE else 'Local Data <span class="status-emoji">🟢</span>'
        requests_available = REQUESTS_AVAILABLE
    except:
        data_status = 'CV <span class="status-emoji">🟢</span>'
        requests_available = True
    
    ai_status = 'LLM <span class="status-emoji">🟢</span>' if st.session_state.current_provider else 'LLM required <span class="status-emoji">🔴</span>'
    api_key_status = 'API <span class="status-emoji">🟢</span>' if st.session_state.get('openrouter_api_key', '').strip() else 'API Key <span class="status-emoji">🔴</span>'
    
    # Initialize funnel step and path
    if 'quote_funnel_step' not in st.session_state:
        st.session_state.quote_funnel_step = "start"
    if 'quote_funnel_path' not in st.session_state:
        st.session_state.quote_funnel_path = []
    
    st.markdown(f"""
    <div style='text-align: center;'>
        <h1 style='margin: 0; font-size: 68px; font-weight: 800;'>🤖 AI Resume</h1>
        <p style='font-size: 18px; color: #666; margin: 0 0 0.5rem 0; font-weight: 500;'>
            Intelligent CV Chat Interface &nbsp;|&nbsp; Ask anything about Michael's experience 
        </p>
        <p style='font-size: 8px; color: #666; margin: 0;'>
            <span style='font-size: 12px;'>Systems:&nbsp;&nbsp;{data_status}&nbsp;{ai_status}&nbsp;{api_key_status}&nbsp;&nbsp;&nbsp;&nbsp;
            Need custom AI solutions?&nbsp;&nbsp;<a href="https://www.linkedin.com/in/michaelwybraniec/" target="_blank" style="color: #0077b5; text-decoration: none; font-weight: 600;">Let's connect on LinkedIn</a>
            </span> 
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    
    
    # Handle Pending Questions from action panel FIRST
    if hasattr(st.session_state, 'pending_question'):
        user_message = st.session_state.pending_question
        del st.session_state.pending_question
        
        # Add the question as a user message first
        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        st.session_state.messages.append({"role": "user", "content": user_message, "timestamp": timestamp})
        
        # Mark for processing
        st.session_state.processing_message = True
        st.session_state.current_processing_message = user_message
        
        st.rerun()
    
    # Chat Interface
    
    # ========================================================================
    # QUICK ACTIONS - RIGHT BEFORE CHAT INPUT
    # ========================================================================
    
    st.caption("Quick Actions:")
    quick_col1, quick_col2, quick_col3, quick_col4, quick_col5 = st.columns(5)
    
    with quick_col1:
        if st.button("👤 Summarize Profile", key="top_quick_summary", use_container_width=True, help="Get a comprehensive overview of this candidate"):
            # Clear any modal flags
            st.session_state.show_job_analysis_modal = False
            # Run quick start setup first
            quick_start_main()
            question = "Summarize this candidate's profile"
            timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
            st.session_state.messages.append({"role": "user", "content": question, "timestamp": timestamp})
            st.session_state.processing_message = True
            st.session_state.current_processing_message = question
            st.toast(f"Processing: {question[:50]}...")
            st.rerun()
    
    with quick_col2:
        if st.button("📅 Years Experience", key="top_quick_experience", use_container_width=True, help="Find out total years of experience"):
            # Clear any modal flags
            st.session_state.show_job_analysis_modal = False
            # Run quick start setup first
            quick_start_main()
            question = "How many years of experience does this candidate have?"
            timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
            st.session_state.messages.append({"role": "user", "content": question, "timestamp": timestamp})
            st.session_state.processing_message = True
            st.session_state.current_processing_message = question
            st.toast(f"Processing: {question[:50]}...")
            st.rerun()
    
    with quick_col3:
        if st.button("🛠️ Technical Skills", key="top_quick_tech_skills", use_container_width=True, help="Analyze technical competencies"):
            # Clear any modal flags
            st.session_state.show_job_analysis_modal = False
            # Run quick start setup first
            quick_start_main()
            question = "What are their strongest technical skills?"
            timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
            st.session_state.messages.append({"role": "user", "content": question, "timestamp": timestamp})
            st.session_state.processing_message = True
            st.session_state.current_processing_message = question
            st.toast(f"Processing: {question[:50]}...")
            st.rerun()
    
    with quick_col4:
        # Download CV functionality
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            pdf_path = os.path.join(current_dir, "CV_Michael_Wybraniec_15_Jun_2025.pdf")
            
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as pdf_file:
                    cv_pdf_data = pdf_file.read()
                
                st.download_button(
                    label="📄 Download CV",
                    data=cv_pdf_data,
                    file_name="CV_Michael_Wybraniec_15_Jun_2025.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    help="Download Michael's professional CV in PDF format"
                )
            else:
                st.button("📄 Download CV", disabled=True, use_container_width=True, help="CV PDF file not found")
        except Exception as e:
            st.button("📄 Download CV", disabled=True, use_container_width=True, help=f"Error loading CV: {str(e)}")
    
    with quick_col5:
        if st.button("🎯 Smart Match", key="top_quick_job_analysis", use_container_width=True, help="Analyze candidate fit for a specific job"):
            st.session_state.show_job_analysis_modal = True
            st.rerun()

    # Chat Input
    if user_input := st.chat_input("💬 Ask MikeGPT here..."):
        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})
        
        # Mark that we're processing a new message
        st.session_state.processing_message = True
        st.session_state.current_processing_message = user_input
        
        st.rerun()

    # Modal Management - Only show one modal at a time
    # Priority: API Key modal > Job Analysis modal
    if st.session_state.get('show_api_key_modal', False):
        # Close any other modals
        st.session_state.show_job_analysis_modal = False

        # Make modal bigger
        st.markdown("""
            <style>
            div[role="dialog"] { width: 30vw !important; }
            </style>
        """, unsafe_allow_html=True)
        
        @st.dialog("🔑 OpenRouter API Key is Required")
        def api_key_setup_modal():
            # Check if key exists in secrets
            secrets_key = ""
            try:
                secrets_key = st.secrets.get("OPENROUTER_API_KEY", "")
                if secrets_key:
                    st.success("API key found in Streamlit secrets!")
                    st.session_state.openrouter_api_key = secrets_key
                    st.session_state.show_api_key_modal = False
                    quick_start_main()
                    st.rerun()
            except:
                pass
            
            if not secrets_key:
                # Benefits section
               
                
                # API Key input
                api_key_input = st.text_input(
                    "**API Key:**",
                    type="password",
                    placeholder="sk-or-v1-...",
                    key="modal_api_key_input",
                    help="Must start with 'sk-or-'"
                )
                
                # Action buttons
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if st.button("Activate AI Chat", type="primary", use_container_width=True):
                        if api_key_input and api_key_input.startswith("sk-or-"):
                            st.session_state.openrouter_api_key = api_key_input
                            st.session_state.show_api_key_modal = False
                            st.toast("AI Chat activated! Try asking a question.")
                            quick_start_main()
                            st.rerun()
                        elif api_key_input:
                            st.error("Invalid key format. Must start with 'sk-or-'")
                        else:
                            st.error("Please paste your API key above")
                
                with col2:
                    if st.button("Skip for now", use_container_width=True):
                        st.session_state.show_api_key_modal = False
                        st.info("You can still use Quick Access buttons without AI chat!")
                        st.rerun()
                
                # Help section
                with st.expander("Need help getting an API key?"):
                    st.markdown("""
                    **Step-by-step guide:**
                    
                    1. **Visit** [OpenRouter.ai](https://openrouter.ai) and click "Sign Up"
                    2. **Verify** your email (check spam folder)
                    3. **Go to** "Keys" section in your dashboard
                    4. **Click** "Create Key" and give it a name
                    5. **Copy** the key (starts with 'sk-or-v1-')
                    6. **Paste** it in the field above
                    
                    **💰 Cost:** Free tier includes multiple models!
                    """)
                
              
                st.caption("🔒 **Privacy:** Your key stays in your browser session - never shared or stored.")
        
        api_key_setup_modal()

    # Smart Match Modal - Only show if API key modal is not active
    elif st.session_state.get('show_job_analysis_modal', False):
        # Make modal bigger
        st.markdown("""
            <style>
            div[role="dialog"] { width: 40vw !important; }
            </style>
        """, unsafe_allow_html=True)
        
        @st.dialog("🎯 Smart Match Analysis")
        def job_analysis_modal():
            st.markdown("**Analyze how well this candidate fits a specific job role**")
            
            job_description = st.text_area(
                "Paste Job Description",
                height=450,
                placeholder="""Example:
Senior Full-Stack Developer - Remote
Company: TechCorp

Requirements:
- 5+ years full-stack development
- React, Node.js, TypeScript
- AWS/Cloud experience
- Database design (PostgreSQL)
- API development (REST/GraphQL)
- Agile/Scrum experience

Responsibilities:
- Lead frontend architecture decisions
- Mentor junior developers
- Build scalable web applications
- Collaborate with product team

Nice to have:
- AI/ML integration experience
- DevOps knowledge
- Startup experience""",
                key="modal_job_desc"
            )
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("🔍 Analyze Fit", type="primary", use_container_width=True):
                    if job_description.strip():
                        analysis_prompt = f"""
                        Based on this job description:
                        
                        {job_description}
                        
                        Please provide a comprehensive analysis of this candidate including:
                        1. **Match Score** (1-10): How well does the candidate fit this role?
                        2. **Key Strengths**: What makes them a good fit?
                        3. **Potential Gaps**: What skills or experience might they be missing?
                        4. **Recommendations**: Should we proceed with this candidate?
                        5. **Interview Focus**: What areas should we focus on during interviews?
                        
                        Be specific and reference their actual experience and skills.
                        """
                        
                        # Add to messages and process
                        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
                        st.session_state.messages.append({"role": "user", "content": f"Smart Match Request", "timestamp": timestamp})
                        st.session_state.processing_message = True
                        st.session_state.current_processing_message = analysis_prompt
                        st.session_state.show_job_analysis_modal = False
                        st.toast("Analyzing candidate fit for this job...")
                        st.rerun()
                    else:
                        st.error("Please paste a job description first!")
            
            with col2:
                if st.button("❌ Close", use_container_width=True):
                    st.session_state.show_job_analysis_modal = False
                    st.rerun()
            
            st.markdown("---")
            st.caption("💡 **Tip**: Include requirements, responsibilities, and company details for best analysis results")
        
        job_analysis_modal()
    
    # st.markdown("---")

    # Chat Messages Display - NORMAL ORDER (newest last)

    
    # Display messages in NORMAL order (newest at bottom)
    for idx, message in enumerate(st.session_state.messages):
            
            # Custom names for chat messages
            display_name = "MikeGPT" if message["role"] == "assistant" else "User"
            with st.chat_message(message["role"]):
                # Display custom name and timestamp
                name_and_time = f"**{display_name}**"
                if "timestamp" in message:
                    name_and_time += f" • {message['timestamp']}"
                st.caption(name_and_time)
                st.markdown(message["content"])
                
                # API Key input for OpenRouter messages
                if (message["role"] == "assistant" and 
                    "OpenRouter API key required" in message["content"] and
                    not st.session_state.openrouter_api_key):
                    
                    st.markdown("**🔑 Add OpenRouter API Key:**")
                    key_col1, key_col2 = st.columns([4, 1])
                    
                    with key_col1:
                        new_api_key = st.text_input(
                            "API Key",
                            type="password",
                            placeholder="sk-or-...",
                            key=f"api_key_input_msg_{idx}_{hash(message['content'][:50])}",
                            label_visibility="collapsed"
                        )
                    
                    with key_col2:
                        if st.button("Add", key=f"add_key_msg_{idx}_{hash(message['content'][:50])}"):
                            if new_api_key:
                                st.session_state.openrouter_api_key = new_api_key
                                st.write("Added!")
                                
                                # Process the pending message
                                timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
                                st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})
                                st.session_state.processing_message = True
                                st.session_state.current_processing_message = user_input
                                st.toast(f"Now processing your message: {user_input[:50]}...")
                                
                                st.rerun()
                            else:
                                st.write("Configure your OpenRouter API key first")
                    
                    st.write("💡 Get your free API key at [OpenRouter.ai](https://openrouter.ai)")
                
                # LLM Provider configuration for provider messages
                if (message["role"] == "assistant" and 
                    "Please configure an LLM provider" in message["content"]):
                    
                    st.markdown("**🤖 Quick Setup:**")
                    setup_col1, setup_col2 = st.columns([1, 1])
                    
                    with setup_col1:
                        if st.button("🔧 Open Sidebar", key=f"open_sidebar_msg_{idx}"):
                            st.write("👈 Check the sidebar for LLM provider configuration")
                    
                    with setup_col2:
                        if st.button("📖 How to Setup", key=f"how_setup_msg_{idx}"):
                            st.write("💡 Go to sidebar → LLM Provider → Select OpenRouter (free) or Ollama (local)")
                    
                    st.write("💡 Configure your LLM provider in the sidebar to start chatting")
    
    # Welcome message appears when no messages exist
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown("""
            ##### Welcome to Michael's AI Resume!
                        
            ###### Language supported:
            🇺🇸 🇪🇸 🇫🇷 🇩🇪 🇮🇹 🇵🇹 🇳🇱 🇷🇺 🇨🇳 🇯🇵 🇰🇷
                        
            ###### Quick Actions:
            
            👤 **Summarize Profile** - Get a comprehensive overview  
            📅 **Years Experience** - View career timeline and progression  
            🛠️ **Technical Skills** - Explore technical expertise and specializations  
            🎯 **Smart Match** - Analyze job descriptions against candidate fit  
            📄 **Download CV** - Get professional PDF resume  
            
                  
            Just ask anything!
            """)

    # ========================================================================
    # PROCESSING INDICATOR AT BOTTOM
    # ========================================================================
    
    # Handle processing after user message is displayed - NOW AT BOTTOM
    if st.session_state.get('processing_message', False):
        # Show processing indicator AT THE BOTTOM
        st.toast(f"Processing: {st.session_state.current_processing_message[:50]}...")
        
        with st.spinner("Processing your question..."):
            user_input = st.session_state.current_processing_message
            
            # Get context using fallback service (cloud-compatible)
            context = get_resume_context(user_input)
            
            provider = st.session_state.get('current_provider')
            model = st.session_state.get('current_model')
            
            if provider and model:
                messages = [{"role": "user", "content": user_input}]
                
                if provider == "ollama":
                    response = LLMProviders.chat_ollama(model, messages, context)
                elif provider == "openrouter":
                    api_key = st.session_state.get('openrouter_api_key', '')
                    # Debug: Check what we're getting from session state
                    debug_key = f"{api_key[:10]}..." if api_key and len(api_key) > 10 else f"'{api_key}'"
                    print(f"DEBUG: Session state API key: {debug_key}")
                    
                    if api_key and api_key.strip():
                        response = LLMProviders.chat_openrouter(model, messages, context, api_key.strip())
                    else:
                        response = """🔑 **OpenRouter API Key Required**

To chat with AI, you need a free OpenRouter API key:

1. **Get Free Key**: Visit [OpenRouter.ai](https://openrouter.ai) and sign up
2. **Add Key**: Open sidebar (←) → System Setup → Enter your API key  
3. **Start Chatting**: Ask any questions about the resume!

💡 **Alternative**: Use the Quick Access buttons below - they work without any setup and provide instant resume insights!"""
                elif provider == "openai":
                    openai_key = st.session_state.get("openai_api_key", "")
                    if openai_key:
                        response = LLMProviders.chat_openai(model, messages, context, openai_key)
                    else:
                        response = "Please add your OpenAI API key in the sidebar first!"
                else:
                    response = "Please configure an LLM provider in the sidebar first!"
            else:
                # Store the user message for automatic processing after LLM is configured
                st.session_state.pending_user_message = user_input
                response = "⚠️ Please configure an LLM provider in the sidebar first!"
                st.toast(f"💾 Message saved! It will be processed automatically after configuring LLM.")
            
            add_response(response)
            
            # Clear processing flag and trigger scroll for Quick Actions
            st.session_state.processing_message = False
            if 'current_processing_message' in st.session_state:
                del st.session_state.current_processing_message
            

            
            st.rerun()
    
    # ========================================================================
    # RESPONSIVE CSS
    # ========================================================================
    
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100vw;
        width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .stApp {
        max-width: 100vw;
        overflow-x: hidden;
    }
    
    /* Header styling */
  
    
    /* Main chat area - full width */
    .main .block-container {
        max-width: 100%;
    }
    
    /* Chat container styling */
    .stChatMessage {
        margin-bottom: 1rem;
    }
    
    /* Button styling improvements */
    .stButton > button {
        transition: all 0.2s ease;
    }
    
    /* Green styling for secondary buttons */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #22c55e !important;
        color: white !important;
        border: 1px solid #16a34a !important;
    }
    
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #16a34a !important;
        border: 1px solid #15803d !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0 10px;
    }
    
    /* Compact spacing */
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    
    /* Chat input styling */
    .stChatInput {
        margin-top: 10px;
        padding: 10px 0;
    }
    
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: none !important;
            margin-bottom: 1rem;
            padding: 0 5px;
        }
        
        [data-testid="column"]:first-child {
            height: 500px; /* Smaller height for mobile */
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SIDEBAR CONFIGURATION
    # ========================================================================

    with st.sidebar:
        # Quick Setup - Show status or start button based on setup completion
        try:
            from fallback_resume import REQUESTS_AVAILABLE
            requests_available = REQUESTS_AVAILABLE
        except:
            requests_available = True
        
        # Check if all systems are active
        setup_complete = (
            requests_available and 
            st.session_state.current_provider and 
            st.session_state.get('openrouter_api_key', '').strip()
        )
        
        if setup_complete:
            st.info("✅ All Systems Ready!")
        else:
            if st.button("🚀 Start", type="primary", use_container_width=True, key="quick_start_main"):
                # Check if API key exists, if not show modal
                if not st.session_state.get('openrouter_api_key', '').strip():
                    st.session_state.show_api_key_modal = True
                    st.rerun()
                else:
                    quick_start_main()
        # Help & Tips - Main collapsible section at top
        with st.expander("Help & Tips", expanded=False):
            st.markdown("""
            **Quick Start:**
            1. Get a free API key from [OpenRouter.ai](https://openrouter.ai)
            2. Add your API key in "System Setup" below
            3. Start chatting or use Quick Action buttons
            
            **For Recruiters & HR:**
            - 👤 **Summarize Profile** - Get comprehensive candidate overview
            - 📅 **Years Experience** - View career progression timeline  
            - 🛠️ **Technical Skills** - Analyze technical competencies
            - 🎯 **Smart Match** - Job fit analysis with match scores
            - 📄 **Download CV** - Professional PDF resume
            
            **Sample Questions:**
            - "What are their strongest technical skills?"
            - "How many years of Python experience?"
            - "Have they worked with AI/ML technologies?"
            - "What industries have they worked in?"
            
            **Need Custom AI Resume Solutions?**
            - Contact [Michael](https://www.one-front.com/en/contact) for enterprise solutions
            """)
        
        # st.markdown("---")
        
        # System Configuration - Collapsible
        with st.expander("System Setup", expanded=True):
            # Cloud deployment mode - fetches from public gist
            st.info("🌟 **Live Data**: Resume fetched from public GitHub Gist. Always up-to-date, no setup required!")
            
            st.markdown("**OpenRouter API Key**")
            if st.session_state.openrouter_api_key:
                masked_key = st.session_state.openrouter_api_key[:8] + "..." + st.session_state.openrouter_api_key[-4:] if len(st.session_state.openrouter_api_key) > 12 else "***"
                st.write(f"✅ `{masked_key}`")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🔄 Change", use_container_width=True, key="sidebar_change_key"):
                        st.session_state.openrouter_api_key = ""
                        st.toast("🔑 API key cleared", icon="🔄")
                        st.rerun()
                with col2:
                    if st.button("🗑️ Remove", use_container_width=True, key="sidebar_remove_key"):
                        st.session_state.openrouter_api_key = ""
                        st.toast("🗑️ API key removed", icon="🗑️")
                        st.rerun()
            else:
                api_key_input = st.text_input("Enter API key", type="password", placeholder="sk-or-...", key="sidebar_openrouter_api_key_input", label_visibility="collapsed")
                if st.button("Add Key", use_container_width=True, key="sidebar_add_openrouter_api_key"):
                    if api_key_input:
                        st.session_state.openrouter_api_key = api_key_input
                        st.toast("✅ OpenRouter API key added!", icon="🔑")
                        st.rerun()
                    else:
                        st.toast("⚠️ Please enter an API key", icon="⚠️")
            
            st.caption("💡 Get free key at [OpenRouter.ai](https://openrouter.ai)")
        
        # ========================================================================
        # QUICK ACTIONS PANEL
        # ========================================================================
        

        with st.expander("Quick Actions", expanded=True):

            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                if st.button("🔄 Clear", key="sidebar_clear_chat", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()
            

if __name__ == "__main__":
    main() 
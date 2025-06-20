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
import subprocess
import time
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
# MCP CLIENT
# ============================================================================

class MCPClient:
    """Client to communicate with MCP Resume Server"""
    
    def __init__(self, server_path: str = "../build/index.js", gist_id: str = "dabf368473d41748e9d6051afb67efcf"):
        self.server_path = server_path
        self.gist_id = gist_id
        self.server_process = None
        
    def start_server(self):
        """Start the MCP server process"""
        try:
            # Check if Node.js is available
            subprocess.run(["node", "--version"], capture_output=True, check=True)
            
            env = os.environ.copy()
            env["GITHUB_GIST_ID"] = self.gist_id
            
            self.server_process = subprocess.Popen(
                ["node", self.server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            time.sleep(2)
            return True
        except FileNotFoundError:
            # Silently fall back to JSON mode - no warnings needed
            return False
        except Exception as e:
            # Silently fall back to JSON mode - no error messages needed
            return False
    
    def send_request(self, method: str, params: Dict = None) -> MCPResponse:
        """Send a request to the MCP server"""
        if not self.server_process:
            return MCPResponse(False, None, "Server not started")
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        try:
            self.server_process.stdin.write(json.dumps(request) + "\n")
            self.server_process.stdin.flush()
            
            response_line = self.server_process.stdout.readline()
            response = json.loads(response_line)
            
            if "error" in response:
                return MCPResponse(False, None, response["error"])
            
            return MCPResponse(True, response.get("result"))
            
        except Exception as e:
            return MCPResponse(False, None, str(e))
    
    def call_tool(self, tool_name: str, args: Dict = None) -> MCPResponse:
        """Call an MCP tool"""
        return self.send_request("tools/call", {
            "name": tool_name,
            "arguments": args or {}
        })
    
    def list_tools(self) -> MCPResponse:
        """List available MCP tools"""
        return self.send_request("tools/list")
    
    def stop_server(self):
        """Stop the MCP server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None

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
            prompt = f"Context: {context}\n\n" + messages[-1]["content"]
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}]
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
            
            system_message = {"role": "system", "content": f"Use this context about the user's resume: {context}"}
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
            
            system_message = {"role": "system", "content": f"Use this context about the user's resume: {context}"}
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
    """Auto-setup function that starts MCP server, adds demo API key, and configures LLM provider"""
    setup_completed = False
    
    # Try to start MCP server
    if not st.session_state.mcp_client:
        mcp_client = MCPClient()
        if mcp_client.start_server():
            st.session_state.mcp_client = mcp_client
            st.toast("✅ Step 1: MCP Server started!")
            setup_completed = True
        else:
            st.toast("⚠️ MCP Server unavailable - using demo mode")
    
    # Check OpenRouter API key
    current_key = st.session_state.get("openrouter_api_key", "").strip()
    if not current_key:
        st.toast("⚠️ Step 2: Please add your OpenRouter API key in the sidebar!")
        st.toast("💡 Get a free API key at OpenRouter.ai", icon="🔑")
    else:
        st.toast("✅ Step 2: OpenRouter API key configured!")
        setup_completed = True
    
    # Set LLM provider
    if not st.session_state.current_provider:
        st.session_state.current_provider = "openrouter"
        st.session_state.current_model = "meta-llama/llama-3.1-8b-instruct:free"
        st.toast("✅ Step 3: LLM provider configured!")
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
        st.toast("🚀 Setup complete! Processing your message...")
    
    return setup_completed

def get_resume_context(mcp_client: MCPClient, user_message: str) -> str:
    """Get relevant resume context based on user message"""
    message_lower = user_message.lower()
    
    try:
        # Check if MCP server is available and healthy
        if mcp_client and mcp_client.server_process:
            # Health check - if server is dead, restart it
            if mcp_client.server_process.poll() is not None:
                st.toast("🔄 Restarting MCP server...")
                mcp_client.start_server()
                st.session_state.mcp_client = mcp_client
            # Use MCP server
            if any(word in message_lower for word in ["experience", "work", "job", "career"]):
                response = mcp_client.call_tool("get_experience")
                if response.success:
                    return f"Work Experience:\n{json.dumps(response.data, indent=2)}"
            
            elif any(word in message_lower for word in ["skill", "technology", "programming", "tech"]):
                response = mcp_client.call_tool("get_skills")
                if response.success:
                    return f"Skills:\n{json.dumps(response.data, indent=2)}"
            
            elif any(word in message_lower for word in ["search", "find"]):
                words = message_lower.split()
                search_terms = [word for word in words if len(word) > 3 and word not in ["search", "find", "about", "with"]]
                if search_terms:
                    search_query = " ".join(search_terms[:3])
                    response = mcp_client.call_tool("search_resume", {"query": search_query})
                    if response.success:
                        return f"Search Results:\n{json.dumps(response.data, indent=2)}"
            
            response = mcp_client.call_tool("get_resume", {"format": "summary"})
            if response.success:
                return f"Resume Summary:\n{response.data}"
        else:
            # Use fallback service
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
        initial_sidebar_state="collapsed"
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
    if 'mcp_client' not in st.session_state:
        st.session_state.mcp_client = None
    if 'openrouter_api_key' not in st.session_state:
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
    
    # ========================================================================
    # ENHANCED HEADER WITH AUTO STATUS
    # ========================================================================
    
    # Enhanced Header with Auto Status
    server_status = 'Server <span class="status-emoji">🟢</span>' if st.session_state.mcp_client else 'Server<span class="status-emoji">🔴</span>'
    ai_status = 'Client <span class="status-emoji">🟢</span>' if st.session_state.current_provider else 'Setup Needed <span class="status-emoji">🔴</span>'
    api_key_status = 'API Key <span class="status-emoji">🟢</span>' if st.session_state.get('openrouter_api_key', '').strip() else 'API Key <span class="status-emoji">🔴</span>'
    
    st.markdown(f"""
    <div style='text-align: center;'>
        <h1 style='margin: 0; font-size: 68px; font-weight: 800;'>🤖 AI Resume</h1>
        <p style='font-size: 18px; color: #666; margin: 0 0 0.5rem 0; font-weight: 500;'>
            Intelligent CV Chat Interface &nbsp;|&nbsp; Ask anything about Michael's experience &nbsp;
        </p>
        <p style='font-size: 8px; color: #666; margin: 0;'>
            <span style='font-size: 12px;'>{server_status} &nbsp;&nbsp; {ai_status} &nbsp;&nbsp; {api_key_status}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # HEADER SECTION WITH CONVERSION FUNNEL
    # ========================================================================
    
    # header_placeholder = st.empty()
    
    # with header_placeholder.container():
    
        
    #     # Header columns
    #     header_col1, header_col2 = st.columns([3, 1])
        
    #     with header_col1:
    #         # Branding section
    #         st.markdown("""
    #         <div class="header-branding">
    #             <div class="flex-content" style='display: flex; align-items: center; justify-content: center; text-align: center;'>
    #                 <div>
    #                     <h1 style='margin: 0; font-size: 68px; font-weight: 800; text-align: center;'>🤖 AI Resume</h1>
    #                     <p style='margin: 0; font-size: 20px; font-style: italic; text-align: center;'>Redefining resumes beyond one page. Transforming hiring process with AI.</p>
    #                     <p style='margin: 0; font-size: 12px; text-align: center;'>Powered with #MCP. Made by <a href="https://www.one-front.com" target="_blank" style="color: #3b82f6; text-decoration: none;">ONE-FRONT</a></p>
    #                 </div>
    #             </div>
    #         </div>
    #         """, unsafe_allow_html=True)
        
    #     with header_col2:
    #         # Conversion funnel section
    #         st.markdown('<div class="header-funnel">', unsafe_allow_html=True)
            
    #         if 'cta_step' not in st.session_state:
    #             st.session_state.cta_step = 0
            
    #         with st.container():
    #             if st.session_state.cta_step > 0:
    #                 dots = "●" * st.session_state.cta_step + "○" * (4 - st.session_state.cta_step)
    #                 st.markdown(f"<div style='color:#888;font-size:12px;height:20px;line-height:20px;text-align:center'>{dots}</div>", unsafe_allow_html=True)
    #             else:
    #                 st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                
    #             content_container = st.container()
    #             with content_container:
    #                 if st.session_state.cta_step == 0:
    #                     st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>Spending hours screening resumes?</div><small style='color:#888'>Most HR teams waste 60% of their time on this</small></div>", unsafe_allow_html=True)
    #                     st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    #                     _, btn_col, _ = st.columns([1, 2, 1])
    #                     with btn_col:
    #                         if st.button("Yes!", type="primary", use_container_width=True, key="header_yes"):
    #                             st.session_state.cta_step = 1
    #                             st.rerun()
                    
    #                 elif st.session_state.cta_step == 1:
    #                     st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>What if AI did it in minutes?</div><small style='color:#888'>Smart screening • Perfect matches • Zero bias</small></div>", unsafe_allow_html=True)
    #                     st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    #                     _, btn_col, _ = st.columns([1, 2, 1])
    #                     with btn_col:
    #                         if st.button("Interested", type="primary", use_container_width=True, key="header_interested"):
    #                             st.session_state.cta_step = 2
    #                             st.rerun()
                    
    #                 elif st.session_state.cta_step == 2:
    #                     st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>Built by Enterprise Developer</div><small style='color:#888'>10+ years • 5 countries • MCP & AI specialist</small></div>", unsafe_allow_html=True)
    #                     st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    #                     _, btn_col, _ = st.columns([1, 2, 1])
    #                     with btn_col:
    #                         if st.button("Credible", type="primary", use_container_width=True, key="header_credible"):
    #                             st.session_state.cta_step = 3
    #                             st.rerun()
                    
    #                 elif st.session_state.cta_step == 3:
    #                     st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>Ready to transform hiring?</div><small style='color:#888'>Custom build • Full integration • 90-day delivery</small></div>", unsafe_allow_html=True)
    #                     st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    #                     _, btn_col, _ = st.columns([1, 2, 1])
    #                     with btn_col:
    #                         sub_col1, sub_col2 = st.columns([3, 1])
    #                         with sub_col1:
    #                             st.button("Get Quote", "https://www.one-front.com/en/contact", type="primary", use_container_width=True)
    #                         with sub_col2:
    #                             if st.button("↺", help="Start over", key="header_reset", use_container_width=True):
    #                                 st.session_state.cta_step = 0
    #                                 st.rerun()
            
    #         st.markdown('</div>', unsafe_allow_html=True)
        
    #     st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================================================
    # MAIN LAYOUT: FULL WIDTH CHAT
    # ========================================================================
    
    
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
    
    # Chat Interface - Input at top, newest messages at bottom
    
    # Chat Input at TOP
    if user_input := st.chat_input("Ask about the resume..."):
        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})
        
        # Mark that we're processing a new message
        st.session_state.processing_message = True
        st.session_state.current_processing_message = user_input
        
        st.rerun()

            # Smart Match Modal
    if st.session_state.get('show_job_analysis_modal', False):
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
    
    st.markdown("---")

    # Chat Messages Display - NORMAL ORDER (newest last)
    # Auto-scroll to bottom functionality
    st.markdown("""
        <script>
        function scrollToBottom() {
            window.scrollTo(0, document.body.scrollHeight);
        }
        setTimeout(scrollToBottom, 100);
        </script>
    """, unsafe_allow_html=True)
    
    # Display messages in NORMAL order (newest at bottom)
    for idx, message in enumerate(st.session_state.messages):
            
            with st.chat_message(message["role"]):
                # Display timestamp if available
                if "timestamp" in message:
                    st.caption(f"{message['timestamp']}")
                st.markdown(message["content"])
                
                # Start Server button for MCP server messages
                if (message["role"] == "assistant" and 
                    "Please start the MCP server first!" in message["content"] and
                    not st.session_state.mcp_client):
                    
                    st.markdown("**Quick Action:**")
                    if st.button("Start MCP Server", type="secondary", key=f"start_server_msg_{idx}"):
                        with st.spinner("Starting MCP server..."):
                            gist_id = st.session_state.get('current_gist_id', "dabf368473d41748e9d6051afb67efcf")
                            server_path = st.session_state.get('current_server_path', "../build/index.js")
                            mcp_client = MCPClient(server_path, gist_id)
                            if mcp_client.start_server():
                                st.session_state.mcp_client = mcp_client
                                st.toast("MCP Server started successfully!")
                                
                                # Process the pending user message
                                user_msg = user_input.strip()
                                timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
                                st.session_state.messages.append({"role": "user", "content": user_msg, "timestamp": timestamp})
                                st.session_state.processing_message = True
                                st.session_state.current_processing_message = user_msg
                                st.toast(f"Now processing your message: {user_msg[:50]}...")
                                st.rerun()
                                
                                if st.session_state.mcp_client and st.session_state.mcp_client.server_process:
                                    context = get_resume_context(st.session_state.mcp_client, user_msg)
                                    
                                    if st.session_state.current_provider == "openrouter":
                                        openrouter_key = st.session_state.get("openrouter_api_key", "")
                                        if openrouter_key:
                                            messages = [{"role": "user", "content": user_msg}]
                                            model = st.session_state.get("current_model", "meta-llama/llama-3.1-8b-instruct:free")
                                            response = LLMProviders.chat_openrouter(model, messages, context, openrouter_key)
                                        else:
                                            response = "Please add your OpenRouter API key in the sidebar first!"
                                    elif st.session_state.current_provider == "ollama":
                                        messages = [{"role": "user", "content": user_msg}]
                                        model = st.session_state.get("current_model", "llama3.2")
                                        response = LLMProviders.chat_ollama(model, messages, context)
                                    elif st.session_state.current_provider == "openai":
                                        openai_key = st.session_state.get("openai_api_key", "")
                                        if openai_key:
                                            messages = [{"role": "user", "content": user_msg}]
                                            model = st.session_state.get("current_model", "gpt-3.5-turbo")
                                            response = LLMProviders.chat_openai(model, messages, context, openai_key)
                                        else:
                                            response = "Please add your OpenAI API key in the sidebar first!"
                                    else:
                                        response = "Please configure an LLM provider in the sidebar first!"
                                    
                                    add_response(response)
                                    st.session_state.processing_message = False
                                    st.rerun()
                                else:
                                    st.write("Failed to start MCP server")
                
                # API Key input for OpenRouter messages
                elif (message["role"] == "assistant" and 
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
                elif (message["role"] == "assistant" and 
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
            **Welcome to Michael Wybraniec's AI Resume**
            
            Get instant access to professional insights and analysis:
            
            **Quick Setup** → 
            1. Click **🚀 Auto Start** in sidebar (←)
            2. Add your free OpenRouter API key ([Get one here](https://openrouter.ai))
            3. Start chatting with AI about the resume!
            
            **Quick Access Menu** (works without setup):
            - 👤 **Summarize Profile** - Get a comprehensive overview
            - 📅 **Years Experience** - View career timeline and progression  
            - 🛠️ **Technical Skills** - Explore technical expertise and specializations
            - 🎯 **Smart Match** - Analyze job descriptions against candidate fit
            - 📄 **Download CV** - Get professional PDF resume
            
            **Or just chat** → Ask anything about Michael's experience, projects, or skills!
            
            💡 **Tip**: The Quick Access buttons work immediately, but for AI chat you'll need a free OpenRouter API key.
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
            
            # Get context - works with both MCP server and fallback
            context = get_resume_context(st.session_state.mcp_client, user_input)
            
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
            
            # Clear processing flag
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
        # Quick Setup - Always visible for easy access at top of sidebar
        if st.button("🚀 Auto Start", type="primary", use_container_width=True, key="quick_start_main"):
            quick_start_main()
        # Help & Tips - Main collapsible section at top
        with st.expander("Help & Tips", expanded=False):
            st.markdown("""
            **About This Interface:**
            This is an AI-powered chat interface for exploring Michael Wybraniec's resume and experience.
            
            **How to Use:**
            1. **Auto Start**: Click "🚀 Auto Start" below for instant configuration
            2. **Chat**: Ask any questions about Michael's experience in the chat input
            3. **Instant Menu**: Use buttons at bottom for common questions (Profile, Experience, Skills, etc.)
            4. **Smart Match**: Paste job descriptions to analyze candidate fit
            5. **Download CV**: Get Michael's professional CV in PDF format
            
            **Key Features:**
            - **AI Chat**: Powered by multiple LLM providers (OpenRouter, OpenAI, Ollama)
            - **MCP Integration**: Uses Model Context Protocol for intelligent resume data retrieval
            - **Smart Analysis**: AI analyzes job descriptions against candidate profile
            - **Free Models**: Works with free AI models via OpenRouter
            
            **For Recruiters:**
            - Get instant candidate summaries and skill assessments
            - Analyze job fit with detailed match scores and recommendations
            - Access 10+ years of professional experience data
            
            **Technical Stack:**
            - Frontend: Streamlit
            - AI: Multiple LLM providers with free tier support
            - Data: MCP server with GitHub Gist integration
            - Resume: JSON format following industry standards
            
            **Useful Links:**
            - [OpenRouter.ai](https://openrouter.ai) - Free API keys for AI models
            - [One-Front.com](https://www.one-front.com/en/contact) - Get your own AI resume interface
            """)
        
        # st.markdown("---")
        
        # System Configuration - Collapsible
        with st.expander("System Setup", expanded=False):
            # MCP Server Control
            if not st.session_state.mcp_client:
                if st.button("Start MCP Server", use_container_width=True, key="sidebar_start_server"):
                    with st.spinner("Starting MCP server..."):
                        gist_id = st.session_state.get('current_gist_id', "dabf368473d41748e9d6051afb67efcf")
                        server_path = st.session_state.get('current_server_path', "../build/index.js")
                        mcp_client = MCPClient(server_path, gist_id)
                        if mcp_client.start_server():
                            st.session_state.mcp_client = mcp_client
                            st.toast("MCP Server started successfully!")
                            st.rerun()
                        else:
                            st.toast("❌ Failed to start MCP server", icon="🚨")
            else:
                if st.button("🛑 Stop MCP Server", use_container_width=True, key="sidebar_stop_server"):
                    st.session_state.mcp_client.stop_server()
                    st.session_state.mcp_client = None
                    st.toast("✅ MCP Server stopped", icon="🛑")
                    st.rerun()
            
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
        
        # st.markdown("### 🎯 Quick Actions")
        
        # action_col1, action_col2 = st.columns(2)
        
        # with action_col1:
        #     if st.button("🔄 Clear Chat", key="sidebar_clear_chat", use_container_width=True):
        #         st.session_state.messages = []
        #         st.rerun()
            
        #     if st.button("📄 Full Resume", key="sidebar_get_resume", use_container_width=True):
        #         if st.session_state.mcp_client:
        #             response = st.session_state.mcp_client.call_tool("get_resume", {"format": "text"})
        #             if response.success:
        #                 add_response(f"**Complete Resume:**\n\n{response.data}")
        #                 st.rerun()
        #             else:
        #                 st.error(f"Error: {response.error}")
        #         else:
        #             st.error("Start MCP server first!")
        
        # with action_col2:
        #     if st.button("💼 Experience", key="sidebar_get_experience", use_container_width=True):
        #         if st.session_state.mcp_client:
        #             response = st.session_state.mcp_client.call_tool("get_experience")
        #             if response.success:
        #                 add_response(f"**Work Experience:**\n\n```json\n{json.dumps(response.data, indent=2)}\n```")
        #                 st.rerun()
        #             else:
        #                 st.error(f"Error: {response.error}")
        #         else:
        #             st.error("Start MCP server first!")
            
        #     if st.button("🛠️ Skills", key="sidebar_get_skills", use_container_width=True):
        #         if st.session_state.mcp_client:
        #             response = st.session_state.mcp_client.call_tool("get_skills")
        #             if response.success:
        #                 add_response(f"**Skills:**\n\n```json\n{json.dumps(response.data, indent=2)}\n```")
        #                 st.rerun()
        #             else:
        #                 st.error(f"Error: {response.error}")
        #         else:
        #             st.error("Start MCP server first!")
        
        # Quick Questions Categories
        with st.expander("Questions for AI", expanded=False):
            
            # Main Questions
            st.markdown("**🎯 Essential Questions**")
            main_questions = [
                "Summarize this candidate's profile",
                "What are their strongest technical skills?", 
                "How many years of experience do they have?",
                "What industries have they worked in?"
            ]
            
            for i, question in enumerate(main_questions):
                if st.button(question, key=f"main_q_{i}", use_container_width=True):
                    st.session_state.pending_question = question
                    st.toast(f"🚀 Processing: {question}", icon="⚡")
                    st.rerun()
            
            # Recruiter Questions
            st.markdown("**💼 For Recruiters**")
            recruiter_questions = [
                "Is this candidate suitable for a senior role?",
                "What's their leadership experience?",
                "Do they have remote work experience?"
            ]
            
            for i, question in enumerate(recruiter_questions):
                if st.button(question, key=f"recruiter_q_{i}", use_container_width=True):
                    st.session_state.pending_question = question
                    st.toast(f"🚀 Processing: {question}", icon="⚡")
                    st.rerun()
            
            # Technical Questions
            st.markdown("**🔍 Technical Deep Dive**")
            technical_questions = [
                "What programming languages are they expert in?",
                "Do they have cloud platform experience?",
                "What's their experience with databases?"
            ]
            
            for i, question in enumerate(technical_questions):
                if st.button(question, key=f"tech_q_{i}", use_container_width=True):
                    st.session_state.pending_question = question
                    st.toast(f"🚀 Processing: {question}", icon="⚡")
                    st.rerun()
            
            # Role-Specific Questions
            st.markdown("**🎯 Role-Specific**")
            role_questions = [
                "Are they suitable for a frontend role?",
                "Do they have backend development skills?",
                "Can they work as a full-stack developer?"
            ]
            
            for i, question in enumerate(role_questions):
                if st.button(question, key=f"role_q_{i}", use_container_width=True):
                    st.session_state.pending_question = question
                    st.toast(f"🚀 Processing: {question}", icon="⚡")
                    st.rerun()
        
            # Resume Source Configuration
        with st.expander("Resume Source", expanded=False):
            gist_id = st.text_input(
                "GitHub Gist ID", 
                value="dabf368473d41748e9d6051afb67efcf",
                help="Enter your GitHub gist ID containing resume.json"
            )
            st.session_state.current_gist_id = gist_id
            
            if st.button("📋 Copy Example Gist URL"):
                st.code("https://gist.github.com/michaelwybraniec/dabf368473d41748e9d6051afb67efcf")
                st.caption("👆 This is an example gist. Create your own with resume.json!")
            
            # Gist Creation Section
            st.markdown("---")
            st.markdown("**🚀 Create New Gist with Real Data**")
            
            if REQUESTS_AVAILABLE:
                github_token = st.text_input(
                    "GitHub Personal Access Token",
                    type="password",
                    help="Get one at: https://github.com/settings/tokens (requires 'gist' scope)",
                    key="github_token"
                )
                
                if github_token and st.button("📤 Create Gist with Resume Data", use_container_width=True):
                    try:
                        with st.spinner("Creating GitHub gist..."):
                            resume_data = generate_json_resume()
                            result = create_gist_with_token(github_token, resume_data)
                            
                            st.success("✅ Gist created successfully!")
                            st.info(f"🔗 **Gist ID:** `{result['id']}`")
                            st.info(f"📄 **URL:** {result['html_url']}")
                            
                            # Auto-update the gist ID field
                            st.session_state.current_gist_id = result['id']
                            st.success(f"🔄 Gist ID updated in configuration!")
                            
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"❌ Failed to create gist: {str(e)}")
                        if "401" in str(e):
                            st.error("🔑 Invalid GitHub token. Make sure it has 'gist' scope.")
                
                if not github_token:
                    st.info("💡 Add your GitHub token above to create a gist with your real resume data")
            else:
                st.warning("⚠️ `requests` library not available. Cannot create gists.")
                st.caption("💡 Use the command line script: `python create_gist.py`")
                
        # Job Description Analysis
        # with st.expander("📋 Job Description Analysis", expanded=False):
        #     job_description = st.text_area(
        #         "Paste Job Description",
        #         height=120,
        #         placeholder="Paste job description for candidate analysis...",
        #         key="sidebar_job_desc"
        #     )
            
        #     if st.button("🔍 Analyze Candidate Fit", key="sidebar_analyze", use_container_width=True):
        #         if job_description.strip():
        #             analysis_prompt = f"""
        #             Based on this job description:
                    
        #             {job_description}
                    
        #             Please provide a comprehensive analysis of this candidate including:
        #             1. **Match Score** (1-10): How well does the candidate fit this role?
        #             2. **Key Strengths**: What makes them a good fit?
        #             3. **Potential Gaps**: What skills or experience might they be missing?
        #             4. **Recommendations**: Should we proceed with this candidate?
        #             5. **Interview Focus**: What areas should we focus on during interviews?
                    
        #             Be specific and reference their actual experience and skills.
        #             """
                    
        #             st.session_state.pending_question = analysis_prompt
        #             st.toast("Analyzing candidate fit...")
        #             st.rerun()
        #         else:
        #             st.toast("Please paste a job description first!")
            
        #     if not job_description.strip():
        #         st.caption("💡 Paste a job description above, then click the button to analyze candidate fit")
        
        # Advanced Settings
        with st.expander("Advanced Settings", expanded=False):
            
            # Server Settings
            st.markdown("**Server Settings**")
            server_path = st.text_input(
                "Server Path", 
                value=st.session_state.current_server_path,
                help="Path to the MCP server build file"
            )
            st.session_state.current_server_path = server_path
            st.caption("Default path should work for most setups")
            
            st.markdown("---")
            
            # LLM Provider Configuration
            st.markdown("**LLM Provider**")
            available_providers = LLMProviders.get_available_providers()
            
            if not available_providers:
                st.write("No LLM providers available. Install Ollama or add API keys.")
                provider = None
            else:
                provider_index = 0
                if st.session_state.current_provider in available_providers:
                    provider_index = available_providers.index(st.session_state.current_provider)
                
                provider = st.selectbox(
                    "Provider", 
                    available_providers,
                    index=provider_index,
                    key="provider_select"
                )
            
            st.session_state.current_provider = provider
            
            model = None
            
            if provider == "ollama":
                if OLLAMA_AVAILABLE:
                    try:
                        models = ollama.list()
                        model_names = [model['name'] for model in models['models']]
                        if model_names:
                            model_index = 0
                            if st.session_state.current_model in model_names:
                                model_index = model_names.index(st.session_state.current_model)
                            model = st.selectbox("Model", model_names, index=model_index)
                        else:
                            st.caption("No Ollama models found. Run: `ollama pull llama3.2`")
                    except:
                        st.caption("Ollama not running. Start with: `ollama serve`")
            
            elif provider == "openrouter":
                openrouter_models = [
                    "meta-llama/llama-3.1-8b-instruct:free",
                    "meta-llama/llama-3.2-3b-instruct:free",
                    "microsoft/phi-3-mini-128k-instruct:free",
                    "huggingfaceh4/zephyr-7b-beta:free"
                ]
                model_index = 0
                if st.session_state.current_model in openrouter_models:
                    model_index = openrouter_models.index(st.session_state.current_model)
                model = st.selectbox("Model", openrouter_models, index=model_index)
                st.caption("Free models available with OpenRouter API key")
            
            elif provider == "openai":
                openai_models = [
                    "gpt-3.5-turbo",
                    "gpt-4",
                    "gpt-4-turbo-preview"
                ]
                model_index = 0
                if st.session_state.current_model in openai_models:
                    model_index = openai_models.index(st.session_state.current_model)
                model = st.selectbox("Model", openai_models, index=model_index)
                st.caption("Requires OpenAI API key (paid service)")
            
            st.session_state.current_model = model
    
    # ========================================================================
    # INSTANT MENU - BOTTOM OF PAGE
    # ========================================================================
    
  
   
    st.caption("Quick access to common questions and actions")
    
    quick_col1, quick_col2, quick_col3, quick_col4, quick_col5 = st.columns(5)
    
    with quick_col1:
        if st.button("👤 Summarize Profile", key="bottom_quick_summary", use_container_width=True, help="Get a comprehensive overview of this candidate"):
            # Clear any modal flags
            st.session_state.show_job_analysis_modal = False
            # Run quick start setup first
            quick_start_main()
            question = "Please provide a comprehensive summary of this candidate's profile, including their experience, key skills, and what makes them a strong hire for a senior developer role."
            timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
            st.session_state.messages.append({"role": "user", "content": question, "timestamp": timestamp})
            st.session_state.processing_message = True
            st.session_state.current_processing_message = question
            st.toast(f"Processing: {question[:50]}...")
            st.rerun()
    
    with quick_col2:
        if st.button("📅 Years Experience", key="bottom_quick_experience", use_container_width=True, help="Find out total years of experience"):
            # Clear any modal flags
            st.session_state.show_job_analysis_modal = False
            # Run quick start setup first
            quick_start_main()
            question = "How many years of total professional experience does this candidate have? Break it down by different roles and highlight their progression."
            timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
            st.session_state.messages.append({"role": "user", "content": question, "timestamp": timestamp})
            st.session_state.processing_message = True
            st.session_state.current_processing_message = question
            st.toast(f"Processing: {question[:50]}...")
            st.rerun()
    
    with quick_col3:
        if st.button("🛠️ Technical Skills", key="bottom_quick_tech_skills", use_container_width=True, help="Analyze technical competencies"):
            # Clear any modal flags
            st.session_state.show_job_analysis_modal = False
            # Run quick start setup first
            quick_start_main()
            question = "What are this candidate's strongest technical skills? List their expertise in programming languages, frameworks, AI/ML technologies, and cloud platforms. Rate their proficiency level."
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
            root_dir = os.path.dirname(current_dir)
            pdf_path = os.path.join(root_dir, "CV_Michael_Wybraniec_15_Jun_2025.pdf")
            
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
        if st.button("🎯 Smart Match", key="bottom_quick_job_analysis", use_container_width=True, help="Analyze candidate fit for a specific job"):
            st.session_state.show_job_analysis_modal = True
            st.rerun()


if __name__ == "__main__":
    main() 
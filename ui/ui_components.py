"""
UI Components and styling for the Streamlit application
"""

import streamlit as st
import datetime
from typing import List, Dict, Any
from core.models import ChatMessage

class UIComponents:
    """Handles UI components and styling"""
    
    @staticmethod
    def apply_custom_css():
        """Apply custom CSS styling to the application"""
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
            
            /* Responsive Design */
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
    
    @staticmethod
    def render_header(data_status: str, ai_status: str, api_key_status: str):
        """Render the application header with system status"""
        st.markdown(f"""
        <div style='text-align: center;'>
            <h1 style='margin: 0; font-size: 68px; font-weight: 800;'>🤖 AI Resume</h1>
            <p style='font-size: 18px; color: #666; margin: 0 0 0.5rem 0; font-weight: 500;'>
                Intelligent CV Chat Interface &nbsp;|&nbsp; Ask anything about Michael's experience &nbsp;|&nbsp; 
                <span style='background: linear-gradient(135deg, #00C851, #00A041); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin: 0 5px; display: inline-block;'>
                    🛡️ AWP Compliant
                </span>
                <span style='background: linear-gradient(135deg, #0077b5, #005885); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin: 0 5px; display: inline-block;'>
                    ⚖️ EU AI Act Ready
                </span>
            </p>
            <p style='font-size: 8px; color: #666; margin: 0;'>
                <span style='font-size: 12px;'>Systems:&nbsp;&nbsp;{data_status}&nbsp;{ai_status}&nbsp;{api_key_status}&nbsp;&nbsp;&nbsp;&nbsp;
                Need custom AI solutions?&nbsp;&nbsp;<a href="https://www.linkedin.com/in/michaelwybraniec/" target="_blank" style="color: #0077b5; text-decoration: none; font-weight: 600;">Let's connect on LinkedIn</a>
                </span> 
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    
    @staticmethod
    def render_quick_actions():
        """Render quick action buttons"""
        st.caption("Quick Actions:")
        quick_col1, quick_col2, quick_col3, quick_col4, quick_col5 = st.columns(5)
        
        actions = {}
        
        with quick_col1:
            actions["summary"] = st.button("👤 Summarize Profile", key="top_quick_summary", use_container_width=True, help="Get a comprehensive overview of this candidate")
        
        with quick_col2:
            actions["experience"] = st.button("📅 Years Experience", key="top_quick_experience", use_container_width=True, help="Find out total years of experience")
        
        with quick_col3:
            actions["skills"] = st.button("🛠️ Technical Skills", key="top_quick_tech_skills", use_container_width=True, help="Analyze technical competencies")
        
        with quick_col4:
            actions["download"] = UIComponents.render_download_button()
        
        with quick_col5:
            actions["match"] = st.button("🎯 Smart Match", key="top_quick_job_analysis", use_container_width=True, help="Analyze candidate fit for a specific job")
        
        return actions
    
    @staticmethod
    def render_download_button():
        """Render the CV download button"""
        try:
            import os
            from core.config import CV_PDF_FILENAME
            
            # CV_PDF_FILENAME already includes 'data/' prefix
            pdf_path = CV_PDF_FILENAME
            
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as pdf_file:
                    cv_pdf_data = pdf_file.read()
                
                return st.download_button(
                    label="📄 Download CV",
                    data=cv_pdf_data,
                    file_name="Awesome CV - Michael Wybraniec.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    help="Download Michael's professional CV in PDF format"
                )
            else:
                st.button("📄 Download CV", disabled=True, use_container_width=True, help="CV PDF file not found")
                return False
        except Exception as e:
            st.button("📄 Download CV", disabled=True, use_container_width=True, help=f"Error loading CV: {str(e)}")
            return False
    
    @staticmethod
    def render_chat_messages(messages: List[Dict[str, Any]]):
        """Render chat messages"""
        for idx, message in enumerate(messages):
            display_name = "MikeGPT" if message["role"] == "assistant" else "User"
            with st.chat_message(message["role"]):
                # Display custom name and timestamp
                name_and_time = f"**{display_name}**"
                if "timestamp" in message:
                    name_and_time += f" • {message['timestamp']}"
                st.caption(name_and_time)
                st.markdown(message["content"])
                
                # AI Act Compliance: Human Oversight Mechanism (Article 14)
                if message["role"] == "assistant":
                    col1, col2, col3 = st.columns([1, 1, 4])
                    with col1:
                        if st.button("👍", key=f"thumbs_up_{idx}", help="Response is accurate"):
                            st.toast("✅ Response marked as accurate", icon="👍")
                    with col2:
                        if st.button("👎", key=f"thumbs_down_{idx}", help="Flag response for review"):
                            st.toast("🚩 Response flagged for human review", icon="👎")
                            # Store flagged response for review
                            if 'flagged_responses' not in st.session_state:
                                st.session_state.flagged_responses = []
                            st.session_state.flagged_responses.append({
                                'message': message["content"],
                                'timestamp': message.get("timestamp", "Unknown"),
                                'index': idx
                            })
    
    @staticmethod
    def render_welcome_message():
        """Render the welcome message when no messages exist"""
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
            
        # AI Act Compliance: Detailed AI System Information (Article 13)
        with st.expander("ℹ️ AI System Information & User Rights", expanded=False):
            st.markdown("""
            **🤖 AI System Details:**
            - **System Type**: High-risk AI system under EU AI Act
            - **Purpose**: Resume analysis and career information presentation
            - **AI Models**: Multiple LLM providers (OpenRouter, OpenAI, Ollama)
            - **Data Processing**: Personal and professional information analysis
            - **Decision Influence**: Advisory only - no automated decision making
            - **Compliance Status**: ✅ **AWP Verified** - Scanned and verified for EU AI Act compliance using Agentic Workflow Protocol (Context Engineering & Migration Strategy Backlog Generation)
            
            **📋 Your Rights:**
            - Right to human oversight and review
            - Right to request explanation of AI decisions
            - Right to contest AI-generated information
            - Right to data protection and privacy
            
            **⚠️ Important Notice:**
            All AI-generated responses should be verified for accuracy. 
            This system provides information for informational purposes only.
            """)
    
    @staticmethod 
    def render_api_key_modal():
        """Render the API key setup modal"""
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
                    st.rerun()
            except:
                pass
            
            if not secrets_key:
                # API Key input
                api_key_input = st.text_input(
                    "**API Key:**",
                    type="password",
                    placeholder="sk-or-v1-...",
                    key="modal_api_key_input",
                    help="Must start with 'sk-or-"
                )
                
                # Action buttons
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if st.button("Activate AI Chat", type="primary", use_container_width=True):
                        if api_key_input and api_key_input.startswith("sk-or-"):
                            st.session_state.openrouter_api_key = api_key_input
                            st.session_state.show_api_key_modal = False
                            st.toast("AI Chat activated! Try asking a question.")
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
    
    @staticmethod
    def render_job_analysis_modal():
        """Render the job analysis modal""" 
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
            
            action_taken = False
            
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
                        action_taken = True
                    else:
                        st.error("Please paste a job description first!")
            
            with col2:
                if st.button("❌ Close", use_container_width=True):
                    st.session_state.show_job_analysis_modal = False
                    action_taken = True
            
            if action_taken:
                st.rerun()
            
            st.markdown("---")
            st.caption("💡 **Tip**: Include requirements, responsibilities, and company details for best analysis results")
        
        job_analysis_modal() 
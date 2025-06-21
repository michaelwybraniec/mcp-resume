"""
AI Resume - Streamlit Interface

This application provides an intelligent chat interface for exploring Michael Wybraniec's resume.
Built with a modular architecture for maintainability and scalability.

MODULAR ARCHITECTURE:
- config.py: Configuration and constants
- models.py: Data models and types
- llm_providers.py: LLM provider implementations
- resume_service.py: Resume data handling
- document_generator.py: PDF/document generation
- ui_components.py: UI components and styling
- session_manager.py: Session state management
- app.py: Main application (this file)
"""

import streamlit as st
from typing import Dict, Any

# Import our modules
from core.config import APP_TITLE, APP_ICON
from ui.session_manager import SessionManager
from ui.ui_components import UIComponents
from services.llm_providers import LLMProviders
from services.resume_service import ResumeService
from services.document_generator import DocumentGenerator

def process_user_message(user_message: str) -> str:
    """Process a user message and return AI response"""
    # Get context from resume service
    context = ResumeService.get_resume_context(user_message)
    
    provider = st.session_state.get('current_provider')
    model = st.session_state.get('current_model')
    
    if not provider or not model:
        return "⚠️ Please configure an LLM provider in the sidebar first!"
    
    messages = [{"role": "user", "content": user_message}]
    
    # Get API key based on provider
    api_key = ""
    if provider == "openrouter":
        api_key = st.session_state.get('openrouter_api_key', '').strip()
        if not api_key:
            return """🔑 **OpenRouter API Key Required**

To chat with AI, you need a free OpenRouter API key:

1. **Get Free Key**: Visit [OpenRouter.ai](https://openrouter.ai) and sign up
2. **Add Key**: Open sidebar (←) → System Setup → Enter your API key  
3. **Start Chatting**: Ask any questions about the resume!

💡 **Alternative**: Use the Quick Access buttons below - they work without any setup and provide instant resume insights!"""
    elif provider == "openai":
        api_key = st.session_state.get("openai_api_key", "")
        if not api_key:
            return "Please add your OpenAI API key in the sidebar first!"
    
    # Use the unified chat interface
    return LLMProviders.chat(provider, model, messages, context, api_key)

def handle_quick_actions(actions: Dict[str, bool]):
    """Handle quick action button clicks"""
    if actions.get("summary"):
        question = "Summarize this candidate's profile"
        SessionManager.add_message("user", question)
        SessionManager.set_processing_state(question)
        st.toast(f"Processing: {question[:50]}...")
        st.rerun()
    
    elif actions.get("experience"):
        question = "How many years of experience does this candidate have?"
        SessionManager.add_message("user", question)
        SessionManager.set_processing_state(question)
        st.toast(f"Processing: {question[:50]}...")
        st.rerun()
    
    elif actions.get("skills"):
        question = "What are their strongest technical skills?"
        SessionManager.add_message("user", question)
        SessionManager.set_processing_state(question)
        st.toast(f"Processing: {question[:50]}...")
        st.rerun()
    
    elif actions.get("match"):
        st.session_state.show_job_analysis_modal = True
        st.rerun()

def render_sidebar():
    """Render the sidebar with configuration options"""
    with st.sidebar:
        # Quick Setup Status
        if SessionManager.is_setup_complete():
            st.info("✅ All Systems Ready!")
        else:
            if st.button("🚀 Start", type="primary", use_container_width=True, key="quick_start_main"):
                if not st.session_state.get('openrouter_api_key', '').strip():
                    st.session_state.show_api_key_modal = True
                    st.rerun()
                else:
                    SessionManager.quick_start_setup()
        
        # Help & Tips
        with st.expander("Help & Tips", expanded=False):
            st.markdown("""
            **Quick Start:**
                        
            If you hit the limits:
            1. Get free API key at [OpenRouter.ai](https://openrouter.ai)
            2. Add key in "System Setup" below
            3. Ask questions or try quick actions
            
            **Sample Questions:**
            - "What are their strongest technical skills?"
            - "How many years of Python experience?"
            - "Have they worked with AI/ML technologies?"
            - "What industries have they worked in?"
            
            **Need Custom AI Resume Solutions?**
            - Contact [Michael](https://www.one-front.com/en/contact) for enterprise solutions
            """)
        
        # System Configuration
        with st.expander("System Setup", expanded=True):
            st.info("🌟 **Live Data**: Resume fetched from public GitHub Gist. Always up-to-date, no setup required!")
            
            st.markdown("**OpenRouter API Key**")
            if st.session_state.openrouter_api_key:
                masked_key = st.session_state.openrouter_api_key[:8] + "..." + st.session_state.openrouter_api_key[-4:] if len(st.session_state.openrouter_api_key) > 12 else "***"
                st.write(f"✅ `{masked_key}`")
                
                if st.button("🔄 Change", use_container_width=True, key="sidebar_change_key"):
                    st.session_state.openrouter_api_key = ""
                    st.toast("🔑 API key cleared", icon="🔄")
                    st.rerun()
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
        
        # Quick Actions Panel
        with st.expander("Quick Actions", expanded=True):
            if st.button("🔄 Clear", key="sidebar_clear_chat", use_container_width=True):
                SessionManager.clear_chat()
                st.rerun()

def main():
    """Main application function"""
    # Configure page
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    SessionManager.initialize_session_state()
    
    # Check API key modal trigger
    SessionManager.check_api_key_modal_trigger()
    
    # Apply custom CSS
    UIComponents.apply_custom_css()
    
    # Render header with system status
    system_status = SessionManager.get_system_status()
    UIComponents.render_header(
        system_status['data'],
        system_status['ai'], 
        system_status['api_key']
    )
    
    # Handle pending questions from previous interactions
    SessionManager.handle_pending_question()
    
    # Render quick actions and handle clicks
    actions = UIComponents.render_quick_actions()
    if any(actions.values()):
        # Clear any modal flags when action buttons are clicked
        st.session_state.show_job_analysis_modal = False
        SessionManager.quick_start_setup()
        handle_quick_actions(actions)
    
    # Chat input
    if user_input := st.chat_input("💬 Ask MikeGPT here..."):
        SessionManager.add_message("user", user_input)
        SessionManager.set_processing_state(user_input)
        st.rerun()
    
    # Modal Management
    if st.session_state.get('show_api_key_modal', False):
        st.session_state.show_job_analysis_modal = False
        UIComponents.render_api_key_modal()
    elif st.session_state.get('show_job_analysis_modal', False):
        UIComponents.render_job_analysis_modal()
    
    # Display chat messages
    if st.session_state.messages:
        UIComponents.render_chat_messages(st.session_state.messages)
    else:
        UIComponents.render_welcome_message()
    
    # Handle message processing
    if st.session_state.get('processing_message', False):
        st.toast(f"Processing: {st.session_state.current_processing_message[:50]}...")
        
        with st.spinner("Processing your question..."):
            user_input = st.session_state.current_processing_message
            response = process_user_message(user_input)
            
            SessionManager.add_message("assistant", response)
            SessionManager.clear_processing_state()
            
            st.rerun()
    
    # Render sidebar
    render_sidebar()

if __name__ == "__main__":
    main() 
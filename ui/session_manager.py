"""
Session state management for the Streamlit application
"""

import streamlit as st
from typing import Dict, Any, List
from core.config import get_openrouter_api_key, get_openai_api_key, DEFAULT_OPENROUTER_MODEL, DEFAULT_GIST_ID, DEFAULT_SERVER_PATH

class SessionManager:
    """Handles session state management and initialization"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables"""
        # Chat messages
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # API Keys
        if 'openrouter_api_key' not in st.session_state:
            st.session_state.openrouter_api_key = get_openrouter_api_key()
        
        if 'openai_api_key' not in st.session_state:
            st.session_state.openai_api_key = get_openai_api_key()
        
        # LLM Configuration
        if 'current_provider' not in st.session_state:
            st.session_state.current_provider = "openrouter"
        
        if 'current_model' not in st.session_state:
            st.session_state.current_model = DEFAULT_OPENROUTER_MODEL
        
        # Server Configuration
        if 'current_gist_id' not in st.session_state:
            st.session_state.current_gist_id = DEFAULT_GIST_ID
        
        if 'current_server_path' not in st.session_state:
            st.session_state.current_server_path = DEFAULT_SERVER_PATH
        
        # UI State
        if 'show_api_key_modal' not in st.session_state:
            st.session_state.show_api_key_modal = False
        
        if 'show_job_analysis_modal' not in st.session_state:
            st.session_state.show_job_analysis_modal = False
        
        # Processing state
        if 'processing_message' not in st.session_state:
            st.session_state.processing_message = False
        
        if 'current_processing_message' not in st.session_state:
            st.session_state.current_processing_message = ""
        
        # API key check
        if 'api_key_check_done' not in st.session_state:
            st.session_state.api_key_check_done = False
        
        # Funnel state
        if 'quote_funnel_step' not in st.session_state:
            st.session_state.quote_funnel_step = "start"
        
        if 'quote_funnel_path' not in st.session_state:
            st.session_state.quote_funnel_path = []
    
    @staticmethod
    def check_api_key_modal_trigger():
        """Check if API key modal should be shown"""
        if not st.session_state.get('openrouter_api_key', '').strip() and not st.session_state.get('api_key_check_done', False):
            st.session_state.show_api_key_modal = True
            st.session_state.api_key_check_done = True
    
    @staticmethod
    def add_message(role: str, content: str):
        """Add a message to the chat history"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        st.session_state.messages.append({
            "role": role,
            "content": content,
            "timestamp": timestamp
        })
    
    @staticmethod
    def clear_chat():
        """Clear all chat messages"""
        st.session_state.messages = []
    
    @staticmethod
    def set_processing_state(message: str = ""):
        """Set the processing state for a message"""
        st.session_state.processing_message = True
        st.session_state.current_processing_message = message
    
    @staticmethod
    def clear_processing_state():
        """Clear the processing state"""
        st.session_state.processing_message = False
        if 'current_processing_message' in st.session_state:
            del st.session_state.current_processing_message
    
    @staticmethod
    def is_setup_complete() -> bool:
        """Check if the application setup is complete"""
        try:
            from fallback_resume import REQUESTS_AVAILABLE
            requests_available = REQUESTS_AVAILABLE
        except:
            requests_available = True
        
        return (
            requests_available and 
            st.session_state.current_provider and 
            st.session_state.get('openrouter_api_key', '').strip()
        )
    
    @staticmethod
    def get_system_status() -> Dict[str, str]:
        """Get system status indicators"""
        try:
            from fallback_resume import REQUESTS_AVAILABLE
            data_status = 'CV <span class="status-emoji">🟢</span>' if REQUESTS_AVAILABLE else 'Local Data <span class="status-emoji">🟢</span>'
        except:
            data_status = 'CV <span class="status-emoji">🟢</span>'
        
        ai_status = 'LLM <span class="status-emoji">🟢</span>' if st.session_state.current_provider else 'LLM required <span class="status-emoji">🔴</span>'
        api_key_status = 'API <span class="status-emoji">🟢</span>' if st.session_state.get('openrouter_api_key', '').strip() else 'API Key <span class="status-emoji">🔴</span>'
        
        return {
            'data': data_status,
            'ai': ai_status,
            'api_key': api_key_status
        }
    
    @staticmethod
    def handle_pending_question():
        """Handle any pending question from action buttons"""
        if hasattr(st.session_state, 'pending_question'):
            user_message = st.session_state.pending_question
            del st.session_state.pending_question
            
            # Add the question as a user message
            SessionManager.add_message("user", user_message)
            
            # Mark for processing
            SessionManager.set_processing_state(user_message)
            
            st.rerun()
    
    @staticmethod
    def quick_start_setup():
        """Quick setup for cloud deployment"""
        setup_completed = True
        
        # Check OpenRouter API key
        current_key = st.session_state.get("openrouter_api_key", "").strip()
        if current_key:
            setup_completed = True
        
        # Set LLM provider
        if not st.session_state.current_provider:
            st.session_state.current_provider = "openrouter"
            st.session_state.current_model = DEFAULT_OPENROUTER_MODEL
            setup_completed = True
        
        # Process any pending user message after setup
        if setup_completed and st.session_state.get('pending_user_message'):
            pending_msg = st.session_state.pending_user_message
            del st.session_state.pending_user_message
            
            # Add the user message to chat
            SessionManager.add_message("user", pending_msg)
            
            # Set up for processing
            SessionManager.set_processing_state(pending_msg)
        
        return setup_completed 
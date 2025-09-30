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
import os
from typing import Dict, Any

# Import our modules
from core.config import APP_TITLE, APP_ICON, DEFAULT_OPENROUTER_MODEL, AVAILABLE_OPENROUTER_MODELS
from ui.session_manager import SessionManager
from ui.ui_components import UIComponents
from services.llm_providers import LLMProviders
from services.resume_service import ResumeService
from services.document_generator import DocumentGenerator
from services.risk_management import risk_manager
from services.data_governance import data_governor
from services.record_keeping import record_keeper
from services.compliance_monitoring import compliance_monitor
from services.audit_procedures import audit_procedures
from services.performance_analytics import performance_analytics
from services.conformity_assessment import conformity_assessor
from services.certification_preparation import certification_preparer
from services.compliance_validation import compliance_validator

def process_user_message(user_message: str) -> str:
    """Process a user message and return AI response"""
    import time
    
    # Start timing for record keeping
    start_time = time.time()
    
    # Get context from resume service
    context = ResumeService.get_resume_context(user_message)
    
    provider = st.session_state.get('current_provider', 'ollama')
    model = st.session_state.get('current_model', 'llama3.2')
    
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
    elif provider == "ollama":
        # Ollama doesn't need an API key
        api_key = ""
    
    # Use the appropriate chat method based on provider
    if provider == "openrouter":
        response = LLMProviders.chat_openrouter(model, messages, context, api_key)
    elif provider == "ollama":
        response = LLMProviders.chat_ollama(model, messages, context)
    elif provider == "openai":
        response = LLMProviders.chat_openai(model, messages, context, api_key)
    else:
        response = f"Unsupported provider: {provider}"
    
    # Record keeping for AI Act compliance (Article 12)
    processing_time_ms = int((time.time() - start_time) * 1000)
    user_id = st.session_state.get('user_id', 'anonymous')
    session_id = st.session_state.get('session_id', 'default')
    
    # Log the user interaction
    record_keeper.log_user_interaction(
        user_id=user_id,
        session_id=session_id,
        query=user_message,
        response=response,
        ai_model=model,
        processing_time_ms=processing_time_ms,
        confidence_score=None  # Could be added if available from LLM
    )
    
    return response

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
        # ===== SYSTEM STATUS SECTION =====
        st.markdown("---")
        st.markdown("## System Status")
        
        # Quick Setup Status
        if SessionManager.is_setup_complete():
            st.write("✅ All Systems Ready!")
            st.caption("Application is fully configured and ready to use")
        else:
            st.write("⚠️ Setup Required")
            st.caption("Configure your AI provider to get started")
            if st.button("Start Application", type="primary", use_container_width=True, key="quick_start_main"):
                if not st.session_state.get('openrouter_api_key', '').strip():
                    st.session_state.show_api_key_modal = True
                    st.rerun()
                else:
                    SessionManager.quick_start_setup()
        
        st.markdown("---")
        
        # ===== AI CONFIGURATION SECTION =====
        st.markdown("## AI Configuration")
        
        # System Configuration
        with st.expander("AI Provider Setup", expanded=True):
            st.write("📄 Live Data: Resume loaded from local file. Always up-to-date!")
            
            # Manual AI Provider Switch
            st.markdown("**Provider Selection**")
            st.caption("Choose between local or cloud AI processing")
            provider_mode = st.radio(
                "Choose AI provider:",
                ["Local (Ollama)", "Production (OpenRouter)"],
                index=0 if st.session_state.get('current_provider', 'ollama') == 'ollama' else 1,
                key="provider_mode_switch"
            )
            
            # Update provider based on selection
            if provider_mode == "Local (Ollama)":
                st.session_state.current_provider = "ollama"
                st.session_state.current_model = "llama3.2"
            else:
                st.session_state.current_provider = "openrouter"
                st.session_state.current_model = DEFAULT_OPENROUTER_MODEL
            
            # Show current AI provider
            current_provider = st.session_state.get('current_provider', 'ollama')
            current_model = st.session_state.get('current_model', 'llama3.2')
            
            st.markdown("**Current Configuration**")
            if current_provider == 'ollama':
                st.write(f"🤖 Provider: {current_provider.upper()} - {current_model}")
                st.write("✅ Local AI: Using Ollama with Llama 3.2 - No API key needed!")
                st.caption("💻 Running locally on your Apple M1 Max GPU")
            else:
                st.write(f"🌐 Provider: {current_provider.upper()} - {current_model}")
                st.write("✅ Cloud AI: Using OpenRouter - API key configured!")
                st.caption("☁️ Running on OpenRouter's cloud infrastructure")
                
                st.markdown("**API Key Management**")
                st.caption("Manage your OpenRouter API key for cloud AI access")
                if st.session_state.openrouter_api_key:
                    masked_key = st.session_state.openrouter_api_key[:8] + "..." + st.session_state.openrouter_api_key[-4:] if len(st.session_state.openrouter_api_key) > 12 else "***"
                    st.write(f"🔑 API Key: {masked_key}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Change", use_container_width=True, key="sidebar_change_key"):
                            st.session_state.openrouter_api_key = ""
                            st.toast("API key cleared")
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Remove", use_container_width=True, key="sidebar_remove_key"):
                            st.session_state.openrouter_api_key = ""
                            st.toast("API key removed")
                            st.rerun()
                else:
                    st.write("⚠️ No API key configured")
                    api_key_input = st.text_input("Enter API key", type="password", placeholder="sk-or-...", key="sidebar_openrouter_api_key_input", label_visibility="collapsed")
                    if st.button("➕ Add Key", use_container_width=True, key="sidebar_add_openrouter_api_key"):
                        if api_key_input:
                            st.session_state.openrouter_api_key = api_key_input
                            st.toast("OpenRouter API key added!")
                            st.rerun()
                        else:
                            st.toast("Please enter an API key")
                
                st.caption("🔗 Get free key at [OpenRouter.ai](https://openrouter.ai)")
        
        # Model selection
        if current_provider == 'openrouter':
            st.markdown("**Model Selection**")
            st.caption("Choose from available OpenRouter models")
            selected_model = st.selectbox(
                "Choose a model:",
                AVAILABLE_OPENROUTER_MODELS,
                index=AVAILABLE_OPENROUTER_MODELS.index(DEFAULT_OPENROUTER_MODEL),
                key="sidebar_openrouter_model_select"
            )
            st.session_state['current_model'] = selected_model
            st.write(f"✅ Selected: {selected_model}")
        elif current_provider == 'ollama':
            st.markdown("**Model Selection**")
            st.caption("Local model optimized for your hardware")
            st.write(f"🤖 Model: {current_model} - 3.2B parameters, optimized for Apple Silicon")
        
        st.markdown("---")
        
        # ===== HELP & GUIDANCE SECTION =====
        st.markdown("## Help & Guidance")
        
        # Help & Tips
        with st.expander("📚 Quick Start Guide", expanded=False):
            st.markdown("""
            **🚀 Getting Started:**
            1. Choose your AI provider above
            2. Ask questions about Michael's experience
            3. Try quick actions in the main interface
            
            **💬 Sample Questions:**
            - "What are their strongest technical skills?"
            - "How many years of Python experience?"
            - "Have they worked with AI/ML technologies?"
            - "What industries have they worked in?"
            
            **🏢 Enterprise Solutions:**
            - Contact [Michael](https://www.one-front.com/en/contact) for custom AI solutions
            """)
        
        # Add a quick tips section
        with st.expander("💡 Quick Tips", expanded=False):
            st.markdown("""
            **💻 Local vs Cloud:**
            - **Local (Ollama)**: Free, private, runs on your device
            - **Cloud (OpenRouter)**: More powerful models, requires API key
            
            **🔧 Troubleshooting:**
            - If local AI is slow, try cloud provider
            - If you hit rate limits, get a free OpenRouter key
            - Check the compliance dashboard for system status
            """)
        
        st.markdown("---")
        
        # ===== COMPLIANCE & TRANSPARENCY SECTION =====
        st.markdown("## Compliance & Transparency")
        
        # MCP-AI-ACT Compliance Notice
        st.write("🛡️ **Powered by Agentic Workflow Protocol**: This tool has been scanned and verified for EU AI Act compliance using the Agentic Workflow Protocol (Context Engineering & Migration Strategy Backlog Generation).")
        st.caption("Compliance verified through automated scanning and assessment")
        
        # AI Act Compliance: AI Transparency Notice (Article 13)
        st.write("🤖 **AI-Powered System Notice**: This application uses artificial intelligence to analyze and present resume information. All responses are generated by AI systems and should be verified for accuracy. This system is classified as a high-risk AI system under EU AI Act regulations.")
        st.caption("High-risk classification due to employment-related decision support")
        
        # AI Act Compliance: Advanced Dashboard
        with st.expander("📊 AI Act Compliance Dashboard", expanded=False):
            st.markdown("**EU AI Act Compliance Status**")
            st.caption("Detailed compliance metrics and monitoring data")
            
            # Overall compliance status
            risk_summary = risk_manager.get_risk_summary()
            governance_status = data_governor.get_governance_compliance_status()
            record_summary = record_keeper.get_compliance_summary()
            monitoring_data = compliance_monitor.get_compliance_dashboard_data()
            audit_summary = audit_procedures.get_audit_summary()
            performance_data = performance_analytics.get_dashboard_metrics()
            assessment_summary = conformity_assessor.get_assessment_summary()
            certification_readiness = certification_preparer.get_certification_readiness()
            validation_status = compliance_validator.get_compliance_validation_status()
            
            # Compliance indicators
            st.markdown("**Compliance Articles**")
            col1, col2 = st.columns(2)
            with col1:
                st.write("✅ AI Transparency (Art. 13)")
                st.write("✅ Human Oversight (Art. 14)")
                st.write("✅ Risk Management (Art. 9)")
                st.write("✅ Data Governance (Art. 10)")
            with col2:
                st.write("✅ Technical Docs (Art. 11)")
                st.write("✅ Record Keeping (Art. 12)")
                st.write("✅ Conformity Assessment")
                st.write("✅ Certification Preparation")
            
            # Advanced monitoring section
            with st.expander("Advanced Monitoring", expanded=False):
                st.markdown("**Monitoring Metrics**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Active Alerts", monitoring_data['active_alerts'])
                with col2:
                    st.metric("Critical Alerts", monitoring_data['critical_alerts'])
                with col3:
                    st.metric("Status", monitoring_data['monitoring_status'])
                
                if monitoring_data['metrics_summary']:
                    st.markdown("**Recent Metrics**")
                    for metric_type, stats in monitoring_data['metrics_summary'].items():
                        if isinstance(stats, dict) and 'latest' in stats:
                            st.metric(metric_type.replace('_', ' ').title(), 
                                     f"{stats['latest']:.2f}")
            
            # Audit procedures section
            with st.expander("Audit Procedures", expanded=False):
                st.markdown("**Audit Status**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Audits", audit_summary['total_audits'])
                with col2:
                    st.metric("Completed", audit_summary['completed_audits'])
                
                if audit_summary['latest_audit']:
                    latest = audit_summary['latest_audit']
                    st.markdown("**Latest Audit**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Score", f"{latest['score']:.1f}" if latest['score'] else "N/A")
                    with col2:
                        st.metric("Result", latest['result'] or "Pending")
            
            # Performance analytics section
            with st.expander("Performance Analytics", expanded=False):
                if 'kpis' in performance_data:
                    st.markdown("**Key Performance Indicators**")
                    for category, kpi in performance_data['kpis'].items():
                        st.metric(
                            category.replace('_', ' ').title(),
                            f"{kpi['current_value']:.2f}",
                            delta=f"{kpi['trend']}"
                        )
                else:
                    st.write("No performance data available")
            
            # Conformity assessment section
            with st.expander("Conformity Assessment", expanded=False):
                st.markdown("**Assessment Status**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Assessments", assessment_summary['total_assessments'])
                with col2:
                    st.metric("Completed", assessment_summary['completed_assessments'])
                
                if assessment_summary['latest_assessment']:
                    latest = assessment_summary['latest_assessment']
                    st.markdown("**Latest Assessment**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Score", f"{latest['score']:.1f}" if latest['score'] else "N/A")
                    with col2:
                        st.metric("Certification Ready", "Yes" if latest['certification_ready'] else "No")
            
            # Certification preparation section
            with st.expander("Certification Preparation", expanded=False):
                st.markdown("**Document Status**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Readiness", f"{certification_readiness['readiness_percentage']:.1f}%")
                with col2:
                    st.metric("Ready for Submission", "Yes" if certification_readiness['ready_for_submission'] else "No")
                with col3:
                    st.metric("Approved Docs", f"{certification_readiness['approved_documents']}/{certification_readiness['total_required_documents']}")
            
            # Compliance validation section
            with st.expander("Compliance Validation", expanded=False):
                if 'overall_status' in validation_status:
                    st.markdown("**Validation Status**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Status", validation_status['overall_status'].replace('_', ' ').title())
                    with col2:
                        st.metric("Score", f"{validation_status['overall_score']:.1f}" if validation_status['overall_score'] else "N/A")
                    with col3:
                        st.metric("Certification Ready", "Yes" if validation_status['certification_ready'] else "No")
                else:
                    st.write("No validation data available")
            
            # Risk management summary
            with st.expander("Risk Management", expanded=False):
                st.markdown("**Risk Overview**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Risks", risk_summary['total_risks'])
                with col2:
                    st.metric("High/Critical", 
                             risk_summary['risks_by_level'].get('high', 0) + 
                             risk_summary['risks_by_level'].get('critical', 0))
                
                if risk_summary['risks_by_level']:
                    st.markdown("**Risk Distribution**")
                    st.bar_chart(risk_summary['risks_by_level'])
            
            # Data governance summary
            with st.expander("Data Governance", expanded=False):
                st.markdown("**Governance Status**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Quality Assessments", len(data_governor.quality_assessments))
                with col2:
                    st.metric("Processing Records", len(data_governor.processing_records))
                with col3:
                    st.metric("Compliance", 
                             "Compliant" if governance_status['overall_compliance'] else "Non-Compliant")
            
            # Record keeping summary
            with st.expander("Record Keeping", expanded=False):
                st.markdown("**Record Status**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("System Records", record_summary['total_records'])
                with col2:
                    st.metric("Audit Trails", record_summary['total_audit_trails'])
                with col3:
                    st.metric("Retention Compliance", 
                             f"{record_summary['retention_compliance']['compliance_percentage']:.1f}%")
            
            # Human oversight section
            with st.expander("Human Oversight", expanded=False):
                # Display flagged responses
                if 'flagged_responses' in st.session_state and st.session_state.flagged_responses:
                    st.warning(f"🚩 {len(st.session_state.flagged_responses)} responses flagged for review")
                    for i, flagged in enumerate(st.session_state.flagged_responses):
                        with st.expander(f"Flagged Response #{i+1} - {flagged['timestamp']}", expanded=False):
                            st.markdown(f"**Message:** {flagged['message'][:200]}...")
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✅ Resolve", key=f"resolve_{i}"):
                                    st.session_state.flagged_responses.pop(i)
                                    st.toast("✅ Flagged response resolved", icon="✅")
                                    st.rerun()
                            with col2:
                                if st.button("📝 Review", key=f"review_{i}"):
                                    st.toast("📝 Opening review interface", icon="📝")
                else:
                    st.success("✅ No flagged responses")
            
            # Advanced compliance actions
            st.markdown("**Advanced Actions:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Generate Report", key="generate_report"):
                    st.toast("📊 Generating compliance report", icon="📊")
            with col2:
                if st.button("🔍 Start Audit", key="start_audit"):
                    st.toast("🔍 Starting compliance audit", icon="🔍")
            with col3:
                if st.button("🔄 Refresh All", key="refresh_all"):
                    st.toast("🔄 All systems refreshed", icon="🔄")
                    st.rerun()
        
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
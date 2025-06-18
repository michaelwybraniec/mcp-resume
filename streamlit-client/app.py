"""
🤖 AI Resume - Streamlit Interface

A Streamlit web application for AI-powered resume screening and analysis.
Integrates with GitHub gists through MCP (Model Context Protocol) Resume Server.

CURRENT LAYOUT STRUCTURE:
┌─────────────────────────────────────────────────────────────────┐
│                    🎯 CONVERSION FUNNEL HEADER                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  4-Step Business Psychology Funnel [3:1 columns]          │  │
│  │  Left: AI Resume Branding & Tagline                       │  │
│  │  Right: Progressive CTA (Yes → Interested → Credible)     │  │
│  └─────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  MAIN CONTENT (FULL WIDTH CHAT)                                │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    💬 CHAT INTERFACE                       │  │
│  │  • Chat Input (top)                                       │  │
│  │  • Messages (chronological order - newest last)           │  │
│  │  • Interactive buttons in messages                        │  │
│  │  • Human-readable timestamps                              │  │
│  │  • Welcome message when empty (at bottom)                 │  │
│  │  ─────────────────────────────────────────────────────────  │  │
│  │  🎯 QUICK ACTIONS (Near Chat Input):                      │  │
│  │    [Clear Chat] [Full Resume] [Experience] [Skills]       │  │
│  │  ❓ QUICK QUESTIONS (2x2 grid):                           │  │
│  │    [Summarize Profile] [Years Experience]                 │  │
│  │    [Technical Skills] [Industries]                        │  │
│  │  🤖 PROCESSING INDICATOR (Bottom)                         │  │
│  └─────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️ SIDEBAR (Collapsible) - CONFIGURATION & CONTROLS           │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  🚦 SYSTEM STATUS                                          │  │
│  │    • Server Status (Ready/Offline)                        │  │
│  │    • LLM Provider Status                                  │  │
│  │  ⚡ QUICK START                                            │  │
│  │    • Start/Stop MCP Server                                │  │
│  │    • API Key Setup (with masked display)                  │  │
│  │  ❓ QUICK QUESTIONS (Categorized)                          │  │
│  │    • Essential Questions                                  │  │
│  │    • For Recruiters                                       │  │
│  │    • Technical Deep Dive                                  │  │
│  │    • Role-Specific                                        │  │
│  │  📄 RESUME SOURCE                                          │  │
│  │    • GitHub Gist ID configuration                         │  │
│  │  📋 JOB DESCRIPTION ANALYSIS                               │  │
│  │    • Text area + Analyze button                           │  │
│  │  ⚙️ ADVANCED SETTINGS                                      │  │
│  │    • Server Settings                                      │  │
│  │    • LLM Provider Configuration                           │  │
│  │    • Help & Tips                                          │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

KEY FEATURES:
- 🎯 Quick Actions positioned near chat input for immediate access
- 💬 Clean chat interface: input at top, processing at bottom
- 🚦 Real-time system status in sidebar
- 🔄 Auto-processing: pending messages handled after setup
- 🔑 Smart API key management with masked display
- ⚡ Toast notifications for all user actions
- 🕒 Human-readable timestamps on all messages
- 📊 Progressive conversion funnel header
- 📋 Job description analysis for candidate matching

TECHNICAL IMPLEMENTATION:
- Native Streamlit components with minimal custom CSS
- Multi-provider LLM support (OpenRouter, Ollama, OpenAI)
- Real-time MCP server integration via subprocess
- Session state management for persistent conversations
- Automatic API key handling and message processing
- Responsive layout with proper column structures
- Error handling and user guidance throughout
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

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

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
        except Exception as e:
            st.error(f"Failed to start MCP server: {e}")
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
        """Chat with OpenRouter model"""
        if not api_key:
            return "OpenRouter API key required"
        
        try:
            client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
            
            system_message = {"role": "system", "content": f"Use this context about the user's resume: {context}"}
            full_messages = [system_message] + messages
            
            response = client.chat.completions.create(
                model=model,
                messages=full_messages
            )
            return response.choices[0].message.content
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

def get_resume_context(mcp_client: MCPClient, user_message: str) -> str:
    """Get relevant resume context based on user message"""
    message_lower = user_message.lower()
    
    try:
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
        
    except Exception as e:
        st.error(f"Error getting context: {e}")
    
    return "No context available"

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    st.set_page_config(
        page_title="AI Resume",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
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
    
    # ========================================================================
    # HEADER SECTION WITH CONVERSION FUNNEL
    # ========================================================================
    
    header_placeholder = st.empty()
    
    with header_placeholder.container():
    
        
        # Header columns
        header_col1, header_col2 = st.columns([3, 1])
        
        with header_col1:
            # Branding section
            st.markdown("""
            <div class="header-branding">
                <div class="flex-content" style='display: flex; align-items: center; justify-content: center; text-align: center;'>
                    <div>
                        <h1 style='margin: 0; font-size: 68px; font-weight: 800; text-align: center;'>🤖 AI Resume</h1>
                        <p style='margin: 0; font-size: 20px; font-style: italic; text-align: center;'>Redefining resumes beyond one page. Transforming hiring process with AI.</p>
                        <p style='margin: 0; font-size: 12px; text-align: center;'>Powered with #MCP. Made by <a href="https://www.one-front.com" target="_blank" style="color: #3b82f6; text-decoration: none;">ONE-FRONT</a></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with header_col2:
            # Conversion funnel section
            st.markdown('<div class="header-funnel">', unsafe_allow_html=True)
            
            if 'cta_step' not in st.session_state:
                st.session_state.cta_step = 0
            
            with st.container():
                if st.session_state.cta_step > 0:
                    dots = "●" * st.session_state.cta_step + "○" * (4 - st.session_state.cta_step)
                    st.markdown(f"<div style='color:#888;font-size:12px;height:20px;line-height:20px;text-align:center'>{dots}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                
                content_container = st.container()
                with content_container:
                    if st.session_state.cta_step == 0:
                        st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>Spending hours screening resumes?</div><small style='color:#888'>Most HR teams waste 60% of their time on this</small></div>", unsafe_allow_html=True)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                        _, btn_col, _ = st.columns([1, 2, 1])
                        with btn_col:
                            if st.button("Yes", type="primary", use_container_width=True, key="header_yes"):
                                st.session_state.cta_step = 1
                                st.rerun()
                    
                    elif st.session_state.cta_step == 1:
                        st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>What if AI did it in minutes?</div><small style='color:#888'>Smart screening • Perfect matches • Zero bias</small></div>", unsafe_allow_html=True)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                        _, btn_col, _ = st.columns([1, 2, 1])
                        with btn_col:
                            if st.button("Interested", type="primary", use_container_width=True, key="header_interested"):
                                st.session_state.cta_step = 2
                                st.rerun()
                    
                    elif st.session_state.cta_step == 2:
                        st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>Built by Enterprise Developer</div><small style='color:#888'>10+ years • 5 countries • MCP & AI specialist</small></div>", unsafe_allow_html=True)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                        _, btn_col, _ = st.columns([1, 2, 1])
                        with btn_col:
                            if st.button("Credible", type="primary", use_container_width=True, key="header_credible"):
                                st.session_state.cta_step = 3
                                st.rerun()
                    
                    elif st.session_state.cta_step == 3:
                        st.markdown("<div style='height:40px;display:flex;align-items:center;flex-direction:column;justify-content:center;text-align:center'><div>Ready to transform hiring?</div><small style='color:#888'>Custom build • Full integration • 90-day delivery</small></div>", unsafe_allow_html=True)
                        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                        _, btn_col, _ = st.columns([1, 2, 1])
                        with btn_col:
                            sub_col1, sub_col2 = st.columns([3, 1])
                            with sub_col1:
                                st.link_button("Get Quote", "https://www.one-front.com/en/contact", type="primary", use_container_width=True)
                            with sub_col2:
                                if st.button("↺", help="Start over", key="header_reset"):
                                    st.session_state.cta_step = 0
                                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
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

    # Chat Messages Display - NORMAL ORDER (newest last)
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
                    
                    st.markdown("**🚀 Quick Action:**")
                    if st.button("🚀 Start MCP Server", type="secondary", key=f"start_server_msg_{idx}"):
                        with st.spinner("Starting MCP server..."):
                            gist_id = st.session_state.get('current_gist_id', "dabf368473d41748e9d6051afb67efcf")
                            server_path = st.session_state.get('current_server_path', "../build/index.js")
                            mcp_client = MCPClient(server_path, gist_id)
                            if mcp_client.start_server():
                                st.session_state.mcp_client = mcp_client
                                st.write("✅ MCP Server started successfully!")
                                
                                # Check if there's a pending user message to process
                                if hasattr(st.session_state, 'pending_user_message'):
                                    user_msg = st.session_state.pending_user_message
                                    del st.session_state.pending_user_message
                                    
                                    # Process the pending message automatically
                                    st.toast(f"🚀 Now processing your message: {user_msg[:50]}...", icon="⚡")
                                    context = get_resume_context(mcp_client, user_msg)
                                    
                                    provider = st.session_state.get('current_provider')
                                    model = st.session_state.get('current_model')
                                    
                                    if provider and model:
                                        messages = [{"role": "user", "content": user_msg}]
                                        
                                        if provider == "ollama":
                                            response = LLMProviders.chat_ollama(model, messages, context)
                                        elif provider == "openrouter":
                                            response = LLMProviders.chat_openrouter(model, messages, context, st.session_state.openrouter_api_key)
                                        elif provider == "openai":
                                            response = LLMProviders.chat_openai(model, messages, context, st.session_state.openai_api_key)
                                        else:
                                            response = "Unknown provider"
                                    else:
                                        response = "⚠️ Please configure an LLM provider in the sidebar first!"
                                    
                                    # Replace the "Please start the MCP server first!" message with the actual response
                                    replace_response("Please start the MCP server first!", response)
                                
                                st.rerun()
                            else:
                                st.write("❌ Failed to start MCP server")
                
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
                                st.write("✅ Added!")
                                
                                # Find the most recent user message to process
                                user_msg = None
                                for msg in reversed(st.session_state.messages):
                                    if msg["role"] == "user":
                                        user_msg = msg["content"]
                                        break
                                
                                if user_msg:
                                    # Process the user message automatically
                                    st.toast(f"🚀 Now processing your message: {user_msg[:50]}...", icon="⚡")
                                    
                                    if st.session_state.mcp_client:
                                        context = get_resume_context(st.session_state.mcp_client, user_msg)
                                        
                                        provider = st.session_state.get('current_provider')
                                        model = st.session_state.get('current_model')
                                        
                                        if provider and model:
                                            messages = [{"role": "user", "content": user_msg}]
                                            
                                            if provider == "ollama":
                                                response = LLMProviders.chat_ollama(model, messages, context)
                                            elif provider == "openrouter":
                                                response = LLMProviders.chat_openrouter(model, messages, context, new_api_key)
                                            elif provider == "openai":
                                                response = LLMProviders.chat_openai(model, messages, context, new_api_key)
                                            else:
                                                response = "Unknown provider"
                                            
                                            # Replace the API key message with the actual response
                                            if any("OpenRouter API key required" in msg.get("content", "") for msg in st.session_state.messages if msg["role"] == "assistant"):
                                                replace_response("OpenRouter API key required", response)
                                            elif any("Please configure an LLM provider" in msg.get("content", "") for msg in st.session_state.messages if msg["role"] == "assistant"):
                                                replace_response("Please configure an LLM provider", response)
                                        else:
                                            # If MCP server not started, store for later processing
                                            st.session_state.pending_user_message = user_msg
                                
                                st.rerun()
                            else:
                                st.write("Invalid key")
                    
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
    
    # Welcome message appears at the bottom when no messages exist
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown("""
            👋 **Welcome to AI Resume!**
            
            I'm here to help you analyze resumes with AI-powered insights. Here's how to get started:
            
            1. **Configure MCP Server** → Use the sidebar to start the server
            2. **Select LLM Provider** → Choose OpenRouter (free), Ollama (local), or OpenAI
            3. **Start Chatting** → Ask me anything about the resume!
            
            **Quick Questions to Try:**
            - "Summarize this candidate's profile"
            - "What are their strongest technical skills?"
            - "How many years of experience do they have?"
            
            💡 **Tip:** Use the quick action buttons below for instant resume data!
            """)

    # ========================================================================
    # PROCESSING INDICATOR AT BOTTOM
    # ========================================================================
    
    # Handle processing after user message is displayed - NOW AT BOTTOM
    if st.session_state.get('processing_message', False):
        # Show processing indicator AT THE BOTTOM
        st.toast(f"🚀 Processing: {st.session_state.current_processing_message[:50]}...", icon="⚡")
        
        with st.spinner("🤖 Processing your question..."):
            user_input = st.session_state.current_processing_message
            
            if st.session_state.mcp_client:
                context = get_resume_context(st.session_state.mcp_client, user_input)
                
                provider = st.session_state.get('current_provider')
                model = st.session_state.get('current_model')
                
                if provider and model:
                    messages = [{"role": "user", "content": user_input}]
                    
                    if provider == "ollama":
                        response = LLMProviders.chat_ollama(model, messages, context)
                    elif provider == "openrouter":
                        response = LLMProviders.chat_openrouter(model, messages, context, st.session_state.openrouter_api_key)
                    elif provider == "openai":
                        response = LLMProviders.chat_openai(model, messages, context, st.session_state.openai_api_key)
                    else:
                        response = "Unknown provider"
                else:
                    # Store the user message for automatic processing after LLM is configured
                    st.session_state.pending_user_message = user_input
                    response = "⚠️ Please configure an LLM provider in the sidebar first!"
                    st.toast(f"💾 Message saved! It will be processed automatically after configuring LLM.", icon="📝")
                
                add_response(response)
            else:
                # Store the user message for automatic processing after server starts
                st.session_state.pending_user_message = user_input
                add_response("Please start the MCP server first!")
                st.toast(f"💾 Message saved! It will be processed automatically after starting the server.", icon="📝")
            
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
        st.header("Control Panel")
        
        # ========================================================================
        # SYSTEM STATUS & QUICK START
        # ========================================================================
        
      
        
        # Status indicators
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.mcp_client:
                st.markdown("🟢 **Server**: Ready")
            else:
                st.markdown("🔴 **Server**: Offline")
        
        with col2:
            provider = st.session_state.get('current_provider')
            model = st.session_state.get('current_model')
            if provider and model:
                st.markdown(f"**LLM**: {provider}")
            else:
                st.markdown("⚠️ **LLM**: Not set")
        
        # Quick Start Actions
       
        
        if not st.session_state.mcp_client:
            if st.button("🚀 Start MCP Server", use_container_width=True, key="sidebar_start_server"):
                with st.spinner("🔄 Starting MCP server..."):
                    gist_id = st.session_state.get('current_gist_id', "dabf368473d41748e9d6051afb67efcf")
                    server_path = st.session_state.get('current_server_path', "../build/index.js")
                    mcp_client = MCPClient(server_path, gist_id)
                    if mcp_client.start_server():
                        st.session_state.mcp_client = mcp_client
                        st.toast("✅ MCP Server started successfully!", icon="🚀")
                        
                        # Check if there's a pending user message to process
                        if hasattr(st.session_state, 'pending_user_message'):
                            user_msg = st.session_state.pending_user_message
                            del st.session_state.pending_user_message
                            
                            # Process the pending message automatically
                            st.toast(f"🚀 Now processing your message: {user_msg[:50]}...", icon="⚡")
                            context = get_resume_context(mcp_client, user_msg)
                            
                            provider = st.session_state.get('current_provider')
                            model = st.session_state.get('current_model')
                            
                            if provider and model:
                                messages = [{"role": "user", "content": user_msg}]
                                
                                if provider == "ollama":
                                    response = LLMProviders.chat_ollama(model, messages, context)
                                elif provider == "openrouter":
                                    response = LLMProviders.chat_openrouter(model, messages, context, st.session_state.openrouter_api_key)
                                elif provider == "openai":
                                    response = LLMProviders.chat_openai(model, messages, context, st.session_state.openai_api_key)
                                else:
                                    response = "Unknown provider"
                            else:
                                response = "⚠️ Please configure an LLM provider in the sidebar first!"
                            
                            # Replace the "Please start the MCP server first!" message with the actual response
                            replace_response("Please start the MCP server first!", response)
                        
                        st.rerun()
                    else:
                        st.toast("❌ Failed to start MCP server", icon="🚨")
        else:
            if st.button("🛑 Stop MCP Server", use_container_width=True, key="sidebar_stop_server"):
                st.session_state.mcp_client.stop_server()
                st.session_state.mcp_client = None
                st.toast("✅ MCP Server stopped", icon="🛑")
                st.rerun()
        
        # OpenRouter API Key Setup
        st.write("🔑 API Key for **OpenRouter** (Free models available)")
        
        if st.session_state.openrouter_api_key:
            # Show current API key status
            masked_key = st.session_state.openrouter_api_key[:8] + "..." + st.session_state.openrouter_api_key[-4:] if len(st.session_state.openrouter_api_key) > 12 else "***"
            st.write(f"✅ **Current Key**: `{masked_key}`")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔄 Change Key", use_container_width=True, key="sidebar_change_key"):
                    st.session_state.openrouter_api_key = ""
                    st.toast("🔑 API key cleared. Please enter a new one.", icon="🔄")
                    st.rerun()
            with col2:
                if st.button("🗑️ Remove Key", use_container_width=True, key="sidebar_remove_key"):
                    st.session_state.openrouter_api_key = ""
                    st.toast("🗑️ API key removed.", icon="🗑️")
                    st.rerun()
        else:
            # Show input for new API key
            api_key_input = st.text_input("Enter API key", type="password", placeholder="sk-or-...", key="sidebar_openrouter_api_key_input", label_visibility="collapsed")
            
            if st.button("Add Key", use_container_width=True, key="sidebar_add_openrouter_api_key"):
                if api_key_input:
                    st.session_state.openrouter_api_key = api_key_input
                    st.toast("✅ OpenRouter API key added successfully!", icon="🔑")
                    
                    # Check if there's a pending user message to process
                    if hasattr(st.session_state, 'pending_user_message'):
                        user_msg = st.session_state.pending_user_message
                        del st.session_state.pending_user_message
                        
                        # Process the pending message automatically
                        if st.session_state.mcp_client:
                            st.toast(f"🚀 Now processing your message: {user_msg[:50]}...", icon="⚡")
                            context = get_resume_context(st.session_state.mcp_client, user_msg)
                            
                            provider = st.session_state.get('current_provider')
                            model = st.session_state.get('current_model')
                            
                            if provider == "openrouter" and model:
                                messages = [{"role": "user", "content": user_msg}]
                                response = LLMProviders.chat_openrouter(model, messages, context, api_key_input)
                                
                                # Replace the API key requirement message with the actual response
                                replace_response("Please add your OpenRouter API key", response)
                            else:
                                response = "⚠️ Please configure OpenRouter as your LLM provider in the sidebar first!"
                                replace_response("Please add your OpenRouter API key", response)
                    
                    st.rerun()
                else:
                    st.toast("⚠️ Please enter an API key", icon="⚠️")
        
        st.caption("💡 Get free API key at [OpenRouter.ai](https://openrouter.ai)")
        
        st.markdown("---")
        
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
        with st.expander("❓ Quick Questions", expanded=False):
            
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
        with st.expander("📄 Resume Source", expanded=False):
            gist_id = st.text_input(
                "GitHub Gist ID", 
                value="dabf368473d41748e9d6051afb67efcf",
                help="Enter your GitHub gist ID containing resume.json"
            )
            st.session_state.current_gist_id = gist_id
            
            if st.button("📋 Copy Example Gist URL"):
                st.code("https://gist.github.com/michaelwybraniec/dabf368473d41748e9d6051afb67efcf")
                st.caption("👆 This is an example gist. Create your own with resume.json!")
                
        # Job Description Analysis
        with st.expander("📋 Job Description Analysis", expanded=False):
            job_description = st.text_area(
                "Paste Job Description",
                height=120,
                placeholder="Paste job description for candidate analysis...",
                key="sidebar_job_desc"
            )
            
            if job_description and st.button("🔍 Analyze Candidate Fit", key="sidebar_analyze", use_container_width=True):
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
                
                st.session_state.pending_question = analysis_prompt
                st.toast("🎯 Analyzing candidate fit...", icon="⚡")
                st.rerun()
        

        
        # ========================================================================
        # ADVANCED CONFIGURATION
        # ========================================================================
        
        st.markdown("### ⚙️ Advanced Settings")
        
        # Server Configuration
        with st.expander("📡 Server Settings", expanded=False):
            server_path = st.text_input("Server Path", value="../build/index.js")
            st.session_state.current_server_path = server_path
            st.caption("💡 Default path should work for most setups")
        
        # LLM Provider Configuration
        with st.expander("🤖 LLM Provider", expanded=False):
            available_providers = LLMProviders.get_available_providers()
            
            if not available_providers:
                st.write("No LLM providers available. Install Ollama or add API keys.")
                provider = None
            else:
                provider = st.selectbox("Provider", available_providers)
            
            st.session_state.current_provider = provider
            
            model = None
            
            if provider == "ollama":
                if OLLAMA_AVAILABLE:
                    try:
                        models = ollama.list()
                        model_names = [model['name'] for model in models['models']]
                        if model_names:
                            model = st.selectbox("Model", model_names)
                        else:
                            st.caption("No Ollama models found. Run: `ollama pull llama3.2`")
                    except:
                        st.caption("Ollama not running. Start with: `ollama serve`")
            
            elif provider == "openrouter":
                model = st.selectbox("Model", [
                    "meta-llama/llama-3.1-8b-instruct:free",
                    "meta-llama/llama-3.2-3b-instruct:free",
                    "microsoft/phi-3-mini-128k-instruct:free",
                    "huggingfaceh4/zephyr-7b-beta:free"
                ])
                st.caption("💡 Free models available with OpenRouter API key")
            
            elif provider == "openai":
                model = st.selectbox("Model", [
                    "gpt-3.5-turbo",
                    "gpt-4",
                    "gpt-4-turbo-preview"
                ])
                st.caption("💡 Requires OpenAI API key (paid service)")
            
            st.session_state.current_model = model
        
        # Help Section
        with st.expander("❓ Help & Tips", expanded=False):
            st.markdown("""
            **🚀 Quick Start:**
            1. Start MCP Server (if not already running)
            2. Add OpenRouter API key (free models available)
            3. Start chatting with AI about the resume!
            
            **💡 Tips:**
            - Use Quick Questions for common queries
            - Try the Quick Actions for instant resume data
            - Paste job descriptions for candidate analysis
            
            **🔗 Links:**
            - [OpenRouter.ai](https://openrouter.ai) - Free API key
            - [JSON Resume](https://jsonresume.org) - Resume format
            - [Example Gist](https://gist.github.com/michaelwybraniec/dabf368473d41748e9d6051afb67efcf) - Sample resume
            """)
        


if __name__ == "__main__":
    main() 
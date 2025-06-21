"""
Data models and types for AI Resume application
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import datetime

@dataclass
class MCPResponse:
    """Response from MCP server"""
    success: bool
    data: Any
    error: Optional[str] = None

@dataclass
class ChatMessage:
    """Chat message structure"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str

    @classmethod
    def create_user_message(cls, content: str) -> 'ChatMessage':
        """Create a user message with current timestamp"""
        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        return cls(role="user", content=content, timestamp=timestamp)
    
    @classmethod
    def create_assistant_message(cls, content: str) -> 'ChatMessage':
        """Create an assistant message with current timestamp"""
        timestamp = datetime.datetime.now().strftime("%b %d, %I:%M %p")
        return cls(role="assistant", content=content, timestamp=timestamp)

@dataclass
class LLMProvider:
    """LLM Provider configuration"""
    name: str
    models: List[str]
    requires_api_key: bool
    api_key_env_var: Optional[str] = None

# Available LLM Providers
LLM_PROVIDERS = {
    "openrouter": LLMProvider(
        name="OpenRouter",
        models=[
            "meta-llama/llama-3.1-8b-instruct:free",
            "microsoft/phi-3-mini-128k-instruct:free",
            "google/gemma-2-9b-it:free"
        ],
        requires_api_key=True,
        api_key_env_var="OPENROUTER_API_KEY"
    ),
    "openai": LLMProvider(
        name="OpenAI",
        models=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        requires_api_key=True,
        api_key_env_var="OPENAI_API_KEY"
    ),
    "ollama": LLMProvider(
        name="Ollama (Local)",
        models=["llama2", "codellama", "mistral"],
        requires_api_key=False
    )
} 
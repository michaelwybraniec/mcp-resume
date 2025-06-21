"""
LLM Provider implementations for different AI services
"""

import os
from typing import List, Dict, Optional
import openai

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
        
        if os.getenv("OPENAI_API_KEY"):
            providers.append("openai")
        
        return providers
    
    @staticmethod
    def create_system_message(context: str) -> str:
        """Create system message with context"""
        return f"""You are an AI assistant helping users explore Michael Wybraniec's professional resume. 

CONTEXT: {context}

FORMATTING GUIDELINES:
- Use proper Markdown formatting in all responses
- Use **bold** for important terms, names, and key points
- Use ##### for headers and section titles
- Use - for bullet points in lists and achievements
- Use `code blocks` for technical skills and technologies
- Keep responses well-structured and easy to scan
- Be professional but conversational
- Focus on relevant details from the provided context"""
    
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
        api_key = api_key.strip() if api_key else ""
        
        if not api_key:
            return "OpenRouter API key required"
        
        if not api_key.startswith("sk-or-"):
            return f"Invalid API key format. Expected format: sk-or-... but got: {api_key[:10]}..."
        
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-resume.streamlit.app",
                "X-Title": "AI Resume Chat Interface"
            }
            
            system_message = {
                "role": "system", 
                "content": LLMProviders.create_system_message(context)
            }
            full_messages = [system_message] + messages
            
            payload = {
                "model": model,
                "messages": full_messages
            }
            
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
            
            system_message = {
                "role": "system", 
                "content": LLMProviders.create_system_message(context)
            }
            full_messages = [system_message] + messages
            
            response = client.chat.completions.create(
                model=model,
                messages=full_messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI error: {str(e)}"
    
    @staticmethod
    def chat(provider: str, model: str, messages: List[Dict], context: str = "", api_key: str = "") -> str:
        """Unified chat interface for all providers"""
        if provider == "ollama":
            return LLMProviders.chat_ollama(model, messages, context)
        elif provider == "openrouter":
            return LLMProviders.chat_openrouter(model, messages, context, api_key)
        elif provider == "openai":
            return LLMProviders.chat_openai(model, messages, context, api_key)
        else:
            return f"Unknown provider: {provider}" 
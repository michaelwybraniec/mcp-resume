"""
LLM Provider implementations for different AI services
"""

import os
from typing import List, Dict
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
        return f"""You are MikeGPT, an AI assistant that answers questions ONLY about Michael Wybraniec's professional resume.

RESUME CONTEXT (sole source of truth):
{context}

CRITICAL — ACCURACY (no improvisation):
- Use ONLY facts present in RESUME CONTEXT above. You have no other knowledge about Michael.
- NEVER invent or infer: employers, job titles, dates, technologies, certifications, projects, or recommendation quotes.
- NEVER add common stack items (e.g. Hadoop, Spark, Tableau, Databricks, Snowflake, TensorFlow) unless they appear verbatim in RESUME CONTEXT.
- If the user asks about something not in context, reply: "That is not listed in Michael's resume data" — do not guess.
- Do not use general industry knowledge to fill gaps. Do not embellish or assume seniority beyond what is stated.
- Michael's profile may span software engineering, product, data/analytics, and AI/agentic work — but mention only pillars and tools explicitly listed above.

STYLE:
- Use **bold** for important terms; bullet points (-) for lists; `code blocks` for technical terms
- Be professional and concise
- When the context contains quoted recommendation or reference text and the user asks to see them, reproduce the actual quotes verbatim — do NOT paraphrase or summarise them.
- If context is insufficient, ask the user to narrow the question

Every claim about Michael must be traceable to RESUME CONTEXT."""
    
    @staticmethod
    def _openrouter_models_to_try(requested_model: str) -> List[str]:
        """Build ordered model list: preferred first, then failover chain."""
        from resume_core.config import AUTO_OPENROUTER_MODEL, OPENROUTER_FALLBACK_MODELS

        if requested_model in (AUTO_OPENROUTER_MODEL, "openrouter/free"):
            return list(OPENROUTER_FALLBACK_MODELS)

        chain = [requested_model]
        for model in OPENROUTER_FALLBACK_MODELS:
            if model not in chain:
                chain.append(model)
        return chain

    @staticmethod
    def _extract_openrouter_content(result: dict) -> str:
        if not result.get("choices"):
            return ""
        message = result["choices"][0].get("message") or {}
        content = message.get("content") or ""
        return content.strip() if isinstance(content, str) else ""

    @staticmethod
    def _should_try_next_openrouter_model(status_code: int, content: str) -> bool:
        if status_code in (404, 429, 502, 503):
            return True
        if status_code == 200 and not content:
            return True
        return False

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
        """Chat with OpenRouter; auto-failover across free models on rate limits."""
        api_key = api_key.strip() if api_key else ""
        
        if not api_key:
            return "OpenRouter API key required"
        
        if not api_key.startswith("sk-or-"):
            return f"Invalid API key format. Expected format: sk-or-... but got: {api_key[:10]}..."
        
        if not REQUESTS_AVAILABLE:
            return "HTTP client (requests) not available"

        from resume_core.config import OPENROUTER_CONNECT_TIMEOUT, OPENROUTER_READ_TIMEOUT

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-resume.streamlit.app",
            "X-Title": "AI Resume Chat Interface",
        }
        system_message = {
            "role": "system",
            "content": LLMProviders.create_system_message(context),
        }
        full_messages = [system_message] + messages
        models_to_try = LLMProviders._openrouter_models_to_try(model)
        failures: List[str] = []

        try:
            for attempt_model in models_to_try:
                payload = {
                    "model": attempt_model,
                    "messages": full_messages,
                    "max_tokens": 2500,
                    "temperature": 0.7,
                }
                try:
                    response = requests.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=(OPENROUTER_CONNECT_TIMEOUT, OPENROUTER_READ_TIMEOUT),
                    )
                except requests.exceptions.Timeout:
                    failures.append(f"`{attempt_model}`: timed out")
                    continue
                except requests.exceptions.RequestException as exc:
                    failures.append(f"`{attempt_model}`: {exc}")
                    continue

                content = ""
                if response.status_code == 200:
                    try:
                        content = LLMProviders._extract_openrouter_content(response.json())
                    except Exception:
                        content = ""

                if response.status_code == 401:
                    return f"""🔑 **Authentication Failed (401)**

Your API key is not being accepted by OpenRouter. Please:

1. **Double-check Key**: Make sure you copied the complete API key from OpenRouter.ai
2. **Key Format**: Should start with 'sk-or-v1-' and be about 70+ characters long
3. **Account Status**: Ensure your OpenRouter account is active and verified
4. **Generate New Key**: Try creating a fresh API key at [OpenRouter.ai](https://openrouter.ai)

**Current key format**: {api_key[:15]}...{api_key[-4:] if len(api_key) > 20 else ''}"""

                if LLMProviders._should_try_next_openrouter_model(response.status_code, content):
                    failures.append(f"`{attempt_model}`: HTTP {response.status_code}")
                    continue

                if response.status_code != 200:
                    failures.append(f"`{attempt_model}`: HTTP {response.status_code} — {response.text[:120]}")
                    continue

                return content

            tried = ", ".join(failures) if failures else "none"
            return f"""❌ **All free models are temporarily unavailable**

Tried: {', '.join(f'`{m}`' for m in models_to_try)}

Details:
{chr(10).join(f'- {f}' for f in failures)}

**What to do:**
1. Wait a minute and send your message again (rate limits reset quickly)
2. Sidebar → keep **Auto (best available free)** selected
3. Add provider API keys at [OpenRouter integrations](https://openrouter.ai/settings/integrations) for higher limits"""

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

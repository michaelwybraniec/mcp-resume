"""
Configuration settings for AI Resume application
"""

import os
import streamlit as st

# API Keys and Secrets
def get_openrouter_api_key():
    """Get OpenRouter API key from secrets or environment"""
    try:
        return st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
    except:
        return os.getenv("OPENROUTER_API_KEY", "")

def get_openai_api_key():
    """Get OpenAI API key from environment"""
    return os.getenv("OPENAI_API_KEY", "")

# Default Models
DEFAULT_OPENROUTER_MODEL = "mistralai/mistral-7b-instruct:free"
AVAILABLE_OPENROUTER_MODELS = [
    "mistralai/mistral-7b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "google/gemma-2-9b-it:free"
]
DEFAULT_GIST_ID = "dabf368473d41748e9d6051afb67efcf"
DEFAULT_SERVER_PATH = "../build/index.js"

# UI Configuration
APP_TITLE = "AI Resume - Intelligent CV Chat Interface"
APP_ICON = "📄"
CHAT_HEIGHT = "65vh"

# File Paths
CV_PDF_FILENAME = "data/CV_Michael_Wybraniec_15_Jun_2025.pdf"

# Quick Questions
QUICK_QUESTIONS = {
    "general": [
        "👤 Summarize Profile",
        "📅 Years Experience", 
        "🛠️ Technical Skills",
        "🎯 Smart Match"
    ],
    "detailed": [
        "What are their strongest technical skills?",
        "How many years of Python experience?",
        "Have they worked with AI/ML technologies?",
        "What industries have they worked in?"
    ]
} 
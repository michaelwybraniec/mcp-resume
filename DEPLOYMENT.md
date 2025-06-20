# 🚀 AI Resume - Deployment Guide

This guide covers how to deploy the AI Resume application both locally and on Streamlit Cloud.

## 🏠 Local Development

### Prerequisites
- Python 3.11+

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/michaelwybraniec/mcp-resume.git
   cd mcp-resume
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Configure your setup:**
   - Add an OpenRouter API key (free models available)
   - Use the Auto Start button for quick setup
   - Start chatting!

## ☁️ Streamlit Cloud Deployment

### Automatic Deployment

The app is optimized for Streamlit Cloud with a pure Python stack:

1. **Fork the repository** on GitHub
2. **Connect to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Deploy from `app.py` (in the root directory)

3. **The deployment will automatically:**
   - Install Python dependencies via `requirements.txt`
   - Use the fallback resume service with demo/live data
   - Work immediately without any additional setup

## 🎯 Features Available

### ✅ Core Features
- **AI Chat Interface** - ChatGPT-style conversation
- **Resume Data** - Professional developer profile
- **Multiple LLM Providers** - OpenRouter, Ollama, OpenAI
- **Quick Access Menu** - Pre-built resume queries
- **Smart Match** - Job description analysis and candidate matching
- **Auto Start** - One-click setup and configuration
- **GitHub Gist Integration** - Live resume data from public gists
- **PDF Download** - Professional resume download

## 🔑 API Keys & Configuration

### OpenRouter (Recommended - Free Models)
1. Get free API key at [OpenRouter.ai](https://openrouter.ai)
2. Add key in sidebar
3. Select from free models:
   - `meta-llama/llama-3.1-8b-instruct:free`
   - `meta-llama/llama-3.2-3b-instruct:free`
   - `microsoft/phi-3-mini-128k-instruct:free`

### Ollama (Local)
1. Install [Ollama](https://ollama.ai)
2. Pull a model: `ollama pull llama3.2`
3. Start service: `ollama serve`

### OpenAI (Paid)
1. Get API key from [OpenAI](https://platform.openai.com)
2. Add key in sidebar
3. Select model (gpt-3.5-turbo, gpt-4, etc.)

## 📁 Resume Data Format

### GitHub Gist Setup
1. Create a new GitHub gist
2. Add a file named `resume.json`
3. Use this format:

```json
{
  "personal": {
    "name": "Your Name",
    "title": "Your Title",
    "location": "Your Location",
    "email": "your.email@example.com",
    "summary": "Professional summary..."
  },
  "experience": [
    {
      "company": "Company Name",
      "position": "Your Position",
      "duration": "2020 - Present",
      "location": "Location",
      "description": "What you did..."
    }
  ],
  "skills": {
    "technical": ["JavaScript", "Python", "React"],
    "languages": ["English", "Spanish"],
    "certifications": ["AWS Certified"]
  },
  "education": [
    {
      "degree": "Your Degree",
      "institution": "University Name",
      "year": "2020",
      "location": "Location"
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "description": "What it does...",
      "technologies": ["React", "Node.js"],
      "url": "https://github.com/..."
    }
  ]
}
```

4. Copy the gist ID from the URL
5. Add it in the app's sidebar under "Resume Source"

## 🔧 Troubleshooting

### Common Issues

**"Please configure LLM provider":**
- Add an API key in the sidebar
- OpenRouter offers free models
- Ollama works for local development

**API Key not working:**
- Ensure you copied the full key including prefixes (sk-or-...)
- Check that you have credits/usage available
- Verify the key is valid at the provider's website

**App loading slowly:**
- First load may take time as dependencies install
- Subsequent loads will be faster
- Use Auto Start for quicker setup

### Performance Tips

- **Use free OpenRouter models** for cost-effective AI
- **Local Ollama** for privacy and offline use
- **Demo mode** works great for testing and demos

## 🌟 Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit Cloud               │
│  ┌─────────────────────────────────────┐ │
│  │        Python App (app.py)         │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │     Fallback Resume Service    │ │ │
│  │  │   • Local JSON Resume Data     │ │ │
│  │  │   • GitHub Gist Integration    │ │ │
│  │  │   • PDF Generation             │ │ │
│  │  └─────────────────────────────────┘ │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│            LLM Providers                │
│  • OpenRouter (Free Models)            │
│  • Ollama (Local)                      │
│  • OpenAI (Paid)                       │
└─────────────────────────────────────────┘
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/michaelwybraniec/mcp-resume/issues)
- **Discussions**: [GitHub Discussions](https://github.com/michaelwybraniec/mcp-resume/discussions)
- **Professional Services**: [ONE-FRONT.com](https://www.one-front.com/en/contact)

---

Made with ❤️ using Model Context Protocol (MCP) and Streamlit 
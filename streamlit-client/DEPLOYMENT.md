# 🚀 AI Resume - Deployment Guide

This guide covers how to deploy the AI Resume application both locally and on Streamlit Cloud.

## 🏠 Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/michaelwybraniec/mcp-resume.git
   cd mcp-resume
   ```

2. **Build the MCP Server:**
   ```bash
   npm install
   npm run build
   ```

3. **Set up Python environment:**
   ```bash
   cd streamlit-client
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Configure your setup:**
   - Add an OpenRouter API key (free models available)
   - Start the MCP server from the sidebar
   - Start chatting!

## ☁️ Streamlit Cloud Deployment

### Automatic Deployment

The app is configured to work on Streamlit Cloud with automatic Node.js setup:

1. **Fork the repository** on GitHub
2. **Connect to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Deploy from `streamlit-client/app.py`

3. **The deployment will automatically:**
   - Install Node.js via `packages.txt`
   - Install Python dependencies via `requirements.txt`
   - Use fallback demo data if MCP server fails to start

### Manual Build (if needed)

If you need to manually build the server:

```bash
cd streamlit-client
./build_server.sh
```

## 🎯 Features Available

### ✅ Always Available (Demo Mode)
- **AI Chat Interface** - ChatGPT-style conversation
- **Sample Resume Data** - Professional developer profile
- **Multiple LLM Providers** - OpenRouter, Ollama, OpenAI
- **Quick Questions** - Pre-built resume queries
- **Job Analysis** - Candidate-job matching
- **Conversion Funnel** - Business development flow

### 🔧 Full Features (with MCP Server)
- **Live GitHub Gist Integration** - Your actual resume data
- **Real-time Updates** - Changes reflect immediately
- **Custom Resume Sources** - Any GitHub gist
- **Advanced Search** - Semantic resume search

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

**"Node.js not found" on Streamlit Cloud:**
- The app automatically falls back to demo mode
- All features work except live gist integration
- This is normal and expected

**"Please configure LLM provider":**
- Add an API key in the sidebar
- OpenRouter offers free models
- Ollama works for local development

**"Failed to start MCP server" locally:**
- Run `npm run build` in the project root
- Check that Node.js is installed: `node --version`
- Verify the build folder exists: `ls build/`

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
│  │  │     Fallback Service           │ │ │
│  │  │   (Demo Resume Data)           │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │      MCP Client                │ │ │
│  │  │   (Node.js Server Bridge)     │ │ │
│  │  └─────────────────────────────────┘ │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │       Node.js MCP Server            │ │
│  │    (GitHub Gist Integration)       │ │
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
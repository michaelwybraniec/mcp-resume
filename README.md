# 🤖 AI Resume - Interactive Chat Interface

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy%20on-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io)

> **Chat with Michael Wybraniec's AI-powered resume using open-source LLMs - Deploy for FREE!**

*✨ Built with a clean, modular architecture for maximum maintainability and scalability.*

## 📋 Table of Contents

- [🚀 Features](#-features)
- [🎯 Quick Start](#-quick-start)
- [🌟 Deploy to Streamlit Cloud](#-deploy-to-streamlit-cloud-free)
- [🤖 LLM Provider Setup](#-llm-provider-setup)
- [🏗️ Architecture](#️-architecture)
- [💡 Usage Examples](#-usage-examples)
- [🔧 Features & Functionality](#-features--functionality)
- [🌐 Deployment Options](#-deployment-options)
- [📁 Project Structure](#-project-structure)
- [🎨 Customization](#-customization)
- [🛠️ Development](#️-development)
- [❓ Troubleshooting](#-troubleshooting)
- [📞 Contact & Support](#-contact--support)
- [📄 License](#-license)

## 🚀 Features

### 🎯 **Core Functionality**

- **📄 Interactive Resume Chat** - Ask any question about Michael's background and experience
- **🎯 Smart Context Retrieval** - Intelligent context selection based on user questions
- **📄 PDF Download** - Generate and download professional CV on demand
- **🎯 Smart Matching** - Job description analysis for recruiter insights

### 🤖 **AI & LLM Integration**

- **🤖 Multiple LLM Providers** - OpenRouter (free models), OpenAI, Ollama (local)
- **⚡ Real-time Responses** - Instant responses with intelligent context retrieval
- **🆓 Free Models Available** - Use powerful open-source models at no cost
- **🔧 Flexible Configuration** - Easy switching between different AI providers

### 🎨 **User Experience**

- **💬 Modern Chat UI** - Beautiful Streamlit interface with quick action buttons
- **📱 Mobile Responsive** - Works perfectly on all devices and screen sizes
- **✅ System Status** - Real-time status indicator shows when all systems are ready
- **🔧 Auto-Configuration** - Smart setup flow with contextual help
- **⚡ Quick Actions** - One-click access to common tasks and insights

### 🏗️ **Technical Excellence**

- **🏗️ Purpose-Based Architecture** - Professional project organization with logical file grouping
- **🆓 Free Deployment** - Deploy on Streamlit Cloud for free
- **📦 Modular Design** - Clean separation of concerns for maintainability
- **🔧 Easy Customization** - Simple to adapt for your own resume and branding

## 🎬 Live Demo

> **🚀 Try it now!** [Deploy your own instance on Streamlit Cloud](https://share.streamlit.io) or run locally.

### 📱 **Screenshots**

*Coming soon: Interactive screenshots and demo GIFs*

### 🎯 **What You Can Do**

- **💬 Chat with the AI** - Ask questions about experience, skills, and projects
- **📄 Download CV** - Generate professional PDF resumes
- **🎯 Smart Matching** - Analyze job descriptions for fit
- **⚡ Quick Actions** - Get instant insights with one-click buttons

## 🎯 Quick Start (Local)

### Prerequisites

- Python 3.11 or higher
- Git

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/michaelwybraniec/mcp-resume.git
cd mcp-resume

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

### 🚀 **First Run**

1. **Open your browser** to `http://localhost:8501`
2. **Get a free API key** from [OpenRouter.ai](https://openrouter.ai)
3. **Add your API key** in the sidebar
4. **Look for "✅ All Systems Ready!"** status
5. **Start chatting!** 🎉

> **💡 Pro Tip:** Use the free model `meta-llama/llama-3.1-8b-instruct:free` for testing!

## 🌟 Deploy to Streamlit Cloud (FREE!)

### 1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy AI Resume to Streamlit Cloud"
git push origin main
```

### 2. **Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `app.py`
5. Click "Deploy"!

### 3. **Configure Secrets (Optional)**
For enhanced LLM providers, add secrets in Streamlit Cloud dashboard:

```toml
[secrets]
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
```

### 4. **Your app is live!** 🎉
You'll get a URL like: `https://your-username-mcp-resume-app-xyz.streamlit.app`

## 🤖 LLM Provider Setup

### Option 1: OpenRouter (Recommended)
- **Free models available!**
- Sign up at [OpenRouter](https://openrouter.ai)
- Get API key and add via the sidebar or Streamlit secrets
- Use free models like `meta-llama/llama-3.1-8b-instruct:free`

### Option 2: Ollama (Local Development)
```bash
# Install Ollama
brew install ollama  # macOS
# or visit https://ollama.ai for other platforms

# Start Ollama
ollama serve

# Install models
ollama pull llama3.2
ollama pull llama3.1
```

### Option 3: OpenAI (Paid)
- Get API key from [OpenAI](https://platform.openai.com)
- Add to Streamlit secrets or enter in the app

## 🏗️ Architecture

### **Purpose-Based Organization:**
```
mcp-resume/
├── 🏠 app.py                     # Main entry point (Streamlit-ready)
├── 📋 requirements.txt           # Dependencies
│
├── 🔧 core/                      # Foundation & Configuration
│   ├── config.py                # Settings & constants
│   └── models.py                # Data models & types
│
├── ⚙️ services/                  # Business Logic & Integrations
│   ├── resume_service.py        # Resume data handling
│   ├── llm_providers.py         # AI/LLM integrations
│   ├── document_generator.py    # PDF generation
│   └── fallback_resume.py       # Data fallback service
│
├── 🎨 ui/                        # User Interface Layer
│   ├── ui_components.py         # UI components & styling
│   └── session_manager.py       # Session state management
│
├── 📊 data/                      # Data Files
│   ├── resume.json
│   ├── michael_wybraniec_resume.json
│   └── CV_Michael_Wybraniec_15_Jun_2025.pdf
│
└── 🔨 utils/                     # Utility Scripts
    └── create_gist.py           # GitHub Gist utilities
```

### **System Architecture Diagram:**
```
┌─────────────────────────────────────────────────────────────────┐
│                        🌐 Streamlit App                        │
├─────────────────────────────────────────────────────────────────┤
│  🎨 UI Layer (ui/)                                              │
│  ├── ui_components.py    # Chat interface, modals, styling     │
│  └── session_manager.py  # State management & initialization   │
├─────────────────────────────────────────────────────────────────┤
│  ⚙️ Services Layer (services/)                                  │
│  ├── resume_service.py      # Data retrieval & context         │
│  ├── llm_providers.py       # AI/LLM integrations              │
│  ├── document_generator.py  # PDF generation                   │
│  └── fallback_resume.py     # Data fallback service            │
├─────────────────────────────────────────────────────────────────┤
│  🔧 Core Layer (core/)                                         │
│  ├── config.py           # Settings & constants                │
│  └── models.py           # Data models & types                 │
├─────────────────────────────────────────────────────────────────┤
│  📊 Data Layer (data/)                                         │
│  ├── resume.json              # Primary resume data            │
│  ├── michael_wybraniec_resume.json  # Backup data             │
│  └── CV_Michael_Wybraniec_15_Jun_2025.pdf  # Professional CV  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🤖 External LLM Providers                   │
├─────────────────────────────────────────────────────────────────┤
│  🌐 OpenRouter API    │  🏠 Ollama Local    │  🔑 OpenAI API    │
│  • Free models        │  • llama3.2         │  • GPT models     │
│  • Paid models        │  • llama3.1         │  • Advanced AI    │
│  • Rate limiting      │  • Local processing │  • High quality   │
└─────────────────────────────────────────────────────────────────┘
```

### **Data Flow:**
```
User Input → UI Components → Session Manager → Resume Service
     ↓              ↓              ↓              ↓
LLM Providers ← Message Processing ← Context Generation ← JSON Data
     ↓
AI Response → UI Components → User Interface
```

### **Module Responsibilities:**

#### **🔧 Core Layer**
- **`core/config.py`** - Configuration, constants, and settings
- **`core/models.py`** - Data models and type definitions

#### **🎨 UI Layer**
- **`ui/ui_components.py`** - UI components, styling, and modals
- **`ui/session_manager.py`** - Session state management and initialization

#### **⚙️ Services Layer**
- **`services/resume_service.py`** - Resume data retrieval and context generation
- **`services/llm_providers.py`** - LLM provider implementations and unified chat interface
- **`services/document_generator.py`** - PDF generation and export functionality
- **`services/fallback_resume.py`** - Resume data service and context management

#### **📊 Data Layer**
- **`data/`** - Resume JSON files and PDF assets
- **`utils/`** - Utility scripts and helper functions

## 💡 Usage Examples

### 💬 Chat Examples:
- **"Tell me about Michael's work experience"**
- **"What are his technical skills?"**
- **"Summarize his background for a recruiter"**
- **"Find projects involving JavaScript"**
- **"What's his experience with AI and machine learning?"**
- **"How many years of Python experience does he have?"**
- **"Has he worked with AI/ML technologies?"**
- **"What industries has he worked in?"**

### ⚡ Quick Actions:
- **👤 Summarize Profile** - Get comprehensive candidate overview
- **📅 Years Experience** - View career progression timeline  
- **🛠️ Technical Skills** - Analyze technical competencies
- **🎯 Smart Match** - Job fit analysis with match scores
- **📄 Download CV** - Professional PDF resume

### 🎯 For Recruiters & HR:
- **"Is this candidate suitable for a senior developer role?"**
- **"What's their leadership experience?"**
- **"Do they have experience with cloud platforms?"**
- **"Rate their frontend vs backend skills"**
- **"Analyze fit for this job description..."** (paste job description)

## 🔧 Features & Functionality

### 📱 **Modern Chat Interface**
- Clean, professional design with expanded sidebar
- Quick action buttons for instant insights
- Real-time system status indicator
- Message timestamps and processing indicators
- Mobile-responsive design

### 🎯 **Smart Context Retrieval**
- Intelligent context selection based on user questions
- Focused responses with relevant resume sections
- Experience, skills, projects, and achievements matching
- Job description analysis capabilities

### 📄 **Professional CV Generation**
- Generate PDF CV on demand
- Clean, professional formatting
- Download directly from the interface

### 🔧 **Enhanced User Experience**
- **System Status**: Real-time indicator showing "All Systems Ready!" when configured
- **Help & Tips**: Comprehensive setup guide and sample questions
- **Quick Actions**: Organized, expandable panel for common tasks
- **Auto-Setup**: Smart configuration flow with contextual guidance

## 🌐 Deployment Options

### 1. **Streamlit Cloud (Recommended - Free)** ⭐
- Free hosting for public repositories
- Automatic deployments from GitHub
- Built-in secrets management
- Perfect for demos and portfolios

### 2. **Local Development**
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 3. **Other Cloud Platforms**
- Railway, Render, Heroku
- Use provided `requirements.txt` and `runtime.txt`
- Set startup command: `streamlit run app.py --server.port $PORT`

## 📁 Project Structure

```
mcp-resume/
├── 🏠 app.py                           # Main entry point (Streamlit-ready)
├── 📋 requirements.txt                 # Python dependencies
├── 🐍 runtime.txt                      # Python version for deployment
├── 📖 README.md                        # Documentation
├── 🚀 DEPLOYMENT.md                    # Deployment guide
├── 🔧 secrets.toml.example             # Example secrets configuration
│
├── 🔧 core/                            # Foundation & Configuration
│   ├── __init__.py
│   ├── config.py                       # Settings & constants
│   └── models.py                       # Data models & types
│
├── ⚙️ services/                        # Business Logic & Integrations
│   ├── __init__.py
│   ├── resume_service.py               # Resume data handling
│   ├── llm_providers.py                # AI/LLM integrations
│   ├── document_generator.py           # PDF generation
│   └── fallback_resume.py              # Data fallback service
│
├── 🎨 ui/                              # User Interface Layer
│   ├── __init__.py
│   ├── ui_components.py                # UI components & styling
│   └── session_manager.py              # Session state management
│
├── 📊 data/                            # Data Files
│   ├── resume.json                     # Primary resume data
│   ├── michael_wybraniec_resume.json   # Backup resume data
│   └── CV_Michael_Wybraniec_15_Jun_2025.pdf # Professional CV
│
├── 🔨 utils/                           # Utility Scripts
│   ├── __init__.py
│   └── create_gist.py                  # GitHub Gist utilities
│
└── 🐍 venv/                            # Virtual environment
```

## 🏗️ Purpose-Based Architecture Benefits

### **🔧 For Developers:**
- **Easy Navigation**: Find files by purpose (UI, services, data, etc.)
- **Maintainable**: Clear separation of concerns across directories
- **Scalable**: Add new features without touching existing modules
- **Testable**: Each layer can be tested independently
- **Professional**: Industry-standard project organization

### **🚀 For Features:**
- **New LLM Providers**: Extend `services/llm_providers.py`
- **UI Changes**: Modify `ui/ui_components.py`
- **Export Formats**: Add to `services/document_generator.py`
- **Data Sources**: Extend `services/resume_service.py`
- **Configuration**: Update `core/config.py`

### **📁 Organization Highlights:**
- **Streamlit Compatible**: `app.py` stays in root for deployment
- **Logical Grouping**: Files organized by functionality, not arbitrarily
- **Clean Root**: No clutter - only essential files visible
- **Python Packages**: Proper `__init__.py` files for clean imports

### **Architecture Highlights:**
- **88% reduction** in main file complexity (1,500 → 180 lines)
- **8 focused modules** instead of monolithic structure
- **Clear dependencies** and import relationships
- **Single responsibility** principle throughout

## 🚀 Getting Started

1. **Clone and Install**
   ```bash
   git clone <your-repo>
   cd mcp-resume
   pip install -r requirements.txt
   ```

2. **Run Locally**
   ```bash
   streamlit run app.py
   ```

3. **Configure & Chat**
   - Navigate to `http://localhost:8501`
   - Get a free API key from [OpenRouter.ai](https://openrouter.ai)
   - Add your API key in the sidebar
   - When you see "✅ All Systems Ready!" you're good to go!
   - Start chatting with the AI resume!

## 🎨 Customization

### **🏠 Adding Your Own Resume**

#### **Step 1: Prepare Your Resume Data**
```json
{
  "personal_info": {
    "name": "Your Name",
    "title": "Your Professional Title",
    "email": "your.email@example.com",
    "phone": "+1-234-567-8900",
    "location": "Your City, Country",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "github": "https://github.com/yourusername",
    "website": "https://yourwebsite.com"
  },
  "summary": "Your professional summary...",
  "experience": [
    {
      "company": "Company Name",
      "position": "Your Position",
      "duration": "2020 - Present",
      "description": "Your role description...",
      "achievements": ["Achievement 1", "Achievement 2"]
    }
  ],
  "skills": {
    "technical": ["Python", "JavaScript", "React"],
    "soft": ["Leadership", "Communication", "Problem Solving"]
  },
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor of Science",
      "field": "Computer Science",
      "year": "2020"
    }
  ]
}
```

#### **Step 2: Update Files**
1. **Replace resume data**: Update `data/michael_wybraniec_resume.json` with your data
2. **Update branding**: Modify header in `ui/ui_components.py`
3. **Replace CV**: Add your PDF to `data/` folder
4. **Update config**: Modify constants in `core/config.py`

### **🤖 LLM Configuration**

#### **Adding New Providers**
```python
# In services/llm_providers.py
class CustomProvider(LLMProvider):
    def __init__(self):
        super().__init__("custom_provider")
    
    def chat_completion(self, messages, model, api_key):
        # Your custom implementation
        response = your_api_call(messages, model, api_key)
        return response.choices[0].message.content
```

#### **Customizing System Prompts**
```python
# In services/llm_providers.py
SYSTEM_PROMPT = """
You are an AI assistant helping with resume analysis.
Customize this prompt for your specific needs.
"""
```

### **🎨 UI Customization**

#### **Branding & Colors**
```python
# In ui/ui_components.py
def render_header():
    st.markdown("""
    <div style="background: linear-gradient(90deg, #your-color-1, #your-color-2);">
        <h1>Your Name - AI Resume</h1>
    </div>
    """, unsafe_allow_html=True)
```

#### **Custom Quick Actions**
```python
# In ui/ui_components.py
def render_quick_actions():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Your Custom Action"):
            # Your custom logic
            pass
```

#### **Custom Styling**
```python
# In ui/ui_components.py
def apply_custom_css():
    st.markdown("""
    <style>
    .custom-chat-message {
        background-color: #your-color;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
```

### **📄 Export Customization**

#### **Custom PDF Templates**
```python
# In services/document_generator.py
def generate_custom_cv(resume_data):
    # Custom PDF generation logic
    # Add your company logo, custom fonts, etc.
    pass
```

#### **Multiple Export Formats**
```python
# Add new export methods
def export_to_docx(resume_data):
    # DOCX export implementation
    pass

def export_to_html(resume_data):
    # HTML export implementation
    pass
```

### **🔧 Advanced Customization**

#### **Custom Data Sources**
```python
# In services/resume_service.py
def get_custom_context(query):
    # Add integration with external APIs
    # LinkedIn API, GitHub API, etc.
    pass
```

#### **Analytics Integration**
```python
# Add usage tracking
def track_interaction(user_query, response_time):
    # Google Analytics, Mixpanel, etc.
    pass
```

#### **Multi-language Support**
```python
# In core/config.py
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch'
}
```

### **🚀 Deployment Customization**

#### **Environment Variables**
```bash
# .env file
RESUME_OWNER_NAME="Your Name"
RESUME_OWNER_TITLE="Your Title"
CUSTOM_BRAND_COLOR="#your-color"
ENABLE_ANALYTICS=true
```

#### **Streamlit Configuration**
```toml
# .streamlit/config.toml
[theme]
primaryColor = "#your-color"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### **📚 Customization Examples**

#### **Example 1: Software Developer Resume**
- Technical skills emphasis
- GitHub integration
- Project portfolio showcase
- Code snippet examples

#### **Example 2: Marketing Professional Resume**
- Campaign metrics focus
- Social media integration
- Brand awareness metrics
- Creative portfolio links

#### **Example 3: Data Scientist Resume**
- ML model showcase
- Research publications
- Data visualization examples
- Technical blog integration

### **🔧 Adding New Features**

#### **Feature Development Checklist**
- [ ] **Plan the feature** - Define requirements and scope
- [ ] **Choose the right layer** - UI, Services, Core, or Data
- [ ] **Implement incrementally** - Start with core functionality
- [ ] **Add configuration** - Make it customizable
- [ ] **Update documentation** - Document new features
- [ ] **Test thoroughly** - Ensure it works with existing features
- [ ] **Consider deployment** - Update deployment configs if needed

#### **Common Extension Points**
- **New Export Format**: Extend `document_generator.py`
- **Additional Data Sources**: Modify `resume_service.py`
- **New UI Components**: Add to `ui_components.py`
- **Custom Session Logic**: Extend `session_manager.py`
- **New LLM Providers**: Add to `llm_providers.py`
- **Configuration Options**: Update `core/config.py`

## 🛠️ Development

### **Development Setup**

```bash
# Clone and setup
git clone https://github.com/michaelwybraniec/mcp-resume.git
cd mcp-resume

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py --server.runOnSave true
```

### **Project Structure Overview**

```
mcp-resume/
├── 🏠 app.py                    # Main Streamlit application
├── 🔧 core/                     # Configuration and data models
├── ⚙️ services/                 # Business logic and integrations
├── 🎨 ui/                       # User interface components
├── 📊 data/                     # Resume data files
└── 🔨 utils/                    # Utility scripts
```

### **Key Development Files**

| File | Purpose | Key Functions |
|------|---------|---------------|
| `app.py` | Main entry point | Application initialization, message processing |
| `core/config.py` | Configuration | App settings, constants, model configurations |
| `services/llm_providers.py` | AI Integration | LLM provider implementations |
| `services/resume_service.py` | Data handling | Resume context generation |
| `ui/ui_components.py` | UI Components | Chat interface, modals, styling |
| `ui/session_manager.py` | State management | Session initialization and management |

### **Adding New LLM Providers**

1. **Extend the provider class** in `services/llm_providers.py`:
```python
class NewProvider(LLMProvider):
    def __init__(self):
        super().__init__("new_provider")
    
    def chat_completion(self, messages, model, api_key):
        # Implementation here
        pass
```

2. **Add to provider registry** in the same file
3. **Update configuration** in `core/config.py`

### **Testing**

```bash
# Run the application
streamlit run app.py

# Test different providers
# - OpenRouter: Use free models
# - Ollama: Run locally with `ollama serve`
# - OpenAI: Use your API key
```

### **Code Style**

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings for functions and classes
- Keep functions focused and single-purpose

## ❓ Troubleshooting

### **Common Issues**

#### 🔑 **API Key Problems**
```bash
# Issue: "API Key Required" error
# Solution: 
1. Get free API key from https://openrouter.ai
2. Add key in sidebar or Streamlit secrets
3. Ensure no extra spaces in the key
```

#### 🐍 **Python Version Issues**
```bash
# Issue: Import errors or compatibility issues
# Solution:
python --version  # Should be 3.11+
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 🌐 **Streamlit Connection Issues**
```bash
# Issue: App won't start or connection refused
# Solution:
streamlit run app.py --server.port 8501
# Check if port 8501 is available
# Try different port: --server.port 8502
```

#### 🤖 **LLM Provider Issues**

**OpenRouter:**
- Ensure API key is valid and has credits
- Try different free models
- Check rate limits

**Ollama:**
```bash
# Ensure Ollama is running
ollama serve

# Install required models
ollama pull llama3.2
ollama pull llama3.1
```

**OpenAI:**
- Verify API key is valid
- Check billing and usage limits
- Ensure model is available

#### 📱 **UI Issues**
- Clear browser cache
- Try different browser
- Check console for JavaScript errors
- Ensure stable internet connection

### **Getting Help**

1. **Check the logs** in Streamlit for error messages
2. **Verify configuration** in the sidebar
3. **Test with different providers** to isolate issues
4. **Check system status** indicator in the app

## 📞 Contact & Support

- **Developer**: Michael Wybraniec
- **Website**: [One-Front.com](https://www.one-front.com/en/contact)
- **LinkedIn**: [Connect with Michael](https://www.linkedin.com/in/michaelwybraniec/)
- **Custom AI Solutions**: Contact through One-Front for enterprise implementations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### **What this means:**
- ✅ **Free to use** for personal and commercial projects
- ✅ **Modify and distribute** as needed
- ✅ **Private use** allowed
- ✅ **Attribution** appreciated but not required

### **Usage Guidelines:**
- Feel free to fork and customize for your own resume
- Commercial use is permitted
- Please consider giving credit if you find it helpful
- Report issues or contribute improvements via GitHub

## 🛠️ Recent Updates

- ✅ **Modular Architecture**: Refactored into 8 focused modules for better maintainability
- 🎯 **88% Code Reduction**: Main app now just 180 lines vs original 1,500
- 📚 **Improved Documentation**: Clear module responsibilities and architecture overview
- 🔧 **Enhanced Testability**: Each module can be tested independently
- 🚀 **Better Scalability**: Easy to add features without touching existing code
- 📱 **Maintained All Features**: Full functionality preserved in cleaner structure
- 🆕 **Enhanced README**: Modern documentation with comprehensive guides

## 🎯 Roadmap

### **Planned Features**
- [ ] **Multi-language Support** - Support for different languages
- [ ] **Advanced Analytics** - Usage statistics and insights
- [ ] **Custom Themes** - Multiple UI themes and branding options
- [ ] **API Endpoints** - REST API for programmatic access
- [ ] **Enhanced Export** - Multiple document formats (DOCX, HTML, etc.)
- [ ] **Voice Interface** - Speech-to-text and text-to-speech capabilities

### **Contributing**
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

---

## 🚀 **Ready to revolutionize resume interactions?**

**Deploy your AI-powered resume today with professional-grade architecture!**

[![Deploy to Streamlit Cloud](https://img.shields.io/badge/Deploy%20to-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io)

*Built with ❤️ by [Michael Wybraniec](https://www.linkedin.com/in/michaelwybraniec/)*
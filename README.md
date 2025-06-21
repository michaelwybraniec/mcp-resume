# 🤖 AI Resume - Interactive Chat Interface

**Chat with Michael Wybraniec's AI-powered resume using open-source LLMs - Deploy for FREE!**

*✨ Now built with a clean, modular architecture for maximum maintainability and scalability.*

## 🚀 Features

- **📄 Interactive Resume Chat** - Ask any question about Michael's background and experience
- **🆓 Free Deployment** - Deploy on Streamlit Cloud for free
- **🤖 Multiple LLM Providers** - OpenRouter (free models), OpenAI, Ollama (local)
- **💬 Modern Chat UI** - Beautiful Streamlit interface with quick action buttons
- **📱 Mobile Responsive** - Works perfectly on all devices
- **⚡ Real-time** - Instant responses with intelligent context retrieval
- **📄 PDF Download** - Generate and download professional CV
- **🎯 Smart Matching** - Job description analysis for recruiter insights
- **✅ System Status** - Real-time status indicator shows when all systems are ready
- **🔧 Auto-Configuration** - Smart setup flow with contextual help
- **🏗️ Purpose-Based Architecture** - Professional project organization with logical file grouping

## 🎯 Quick Start (Local)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd mcp-resume

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py

# 4. Open http://localhost:8501
# 5. Get a free API key from OpenRouter.ai
# 6. Add your API key in the sidebar and start chatting!
```

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

### **Data Flow:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ UI Components   │◄──►│ Resume Service   │◄──►│ JSON Resume     │
│ (Chat Interface)│    │ (Data Processing)│    │ Data            │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│ LLM Providers   │
│ • OpenRouter    │
│ • Ollama        │
│ • OpenAI        │
└─────────────────┘
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

### **Adding Your Own Resume**
1. Replace `michael_wybraniec_resume.json` with your resume data
2. Update the `resume_service.py` if needed
3. Modify branding in `ui_components.py` header section
4. Replace the CV PDF file with your own

### **LLM Configuration**
- Add your preferred LLM providers in `llm_providers.py`
- Configure API keys via sidebar or Streamlit secrets
- Customize system prompts in the provider implementations

### **UI Customization**
- Modify the header branding and colors in `ui_components.py`
- Update Quick Action buttons and modal content
- Customize the Help & Tips content in the sidebar
- Adjust the responsive CSS styling

### **Adding New Features**
- **New Export Format**: Extend `document_generator.py`
- **Additional Data Sources**: Modify `resume_service.py`
- **New UI Components**: Add to `ui_components.py`
- **Custom Session Logic**: Extend `session_manager.py`

## 📞 Contact & Support

- **Developer**: Michael Wybraniec
- **Website**: [One-Front.com](https://www.one-front.com/en/contact)
- **LinkedIn**: [Connect with Michael](https://www.linkedin.com/in/michaelwybraniec/)
- **Custom AI Solutions**: Contact through One-Front for enterprise implementations

## 🛠️ Recent Updates

- ✅ **Modular Architecture**: Refactored into 8 focused modules for better maintainability
- 🎯 **88% Code Reduction**: Main app now just 180 lines vs original 1,500
- 📚 **Improved Documentation**: Clear module responsibilities and architecture overview
- 🔧 **Enhanced Testability**: Each module can be tested independently
- 🚀 **Better Scalability**: Easy to add features without touching existing code
- 📱 **Maintained All Features**: Full functionality preserved in cleaner structure

---

**Ready to revolutionize resume interactions with a maintainable, scalable architecture?** 🚀 

*Deploy your AI-powered resume today - now with professional-grade code organization!* 
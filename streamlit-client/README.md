# 🤖 AI Resume - Streamlit Edition

**Chat about ANY resume using open-source LLMs - Deploy for FREE on Streamlit Cloud!**

## 🚀 Features

- **📄 Any Resume** - Use ANY GitHub gist with resume.json (custom gist ID input)
- **🆓 Free Deployment** - Deploy on Streamlit Cloud for free
- **🤖 Multiple LLM Providers** - Ollama (local), OpenRouter (free models), OpenAI
- **💬 Modern Chat UI** - Beautiful Streamlit chat interface with built-in help
- **🔧 MCP Integration** - Direct connection to MCP Resume Server
- **📱 Mobile Responsive** - Works on all devices
- **⚡ Real-time** - Instant responses and live status updates
- **💼 Enterprise Ready** - Contact for company integration

## 🎯 Quick Start (Local)

```bash
# 1. Install dependencies
cd streamlit-client
pip install -r requirements.txt

# 2. Start your MCP Resume Server (in another terminal)
cd ..
npm run dev

# 3. Run the Streamlit app
streamlit run app.py

# 4. Open http://localhost:8501
```

## 🌟 Deploy to Streamlit Cloud (FREE!)

### 1. **Push to GitHub**
```bash
git add .
git commit -m "Add Streamlit MCP Resume Client"
git push origin main
```

### 2. **Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `streamlit-client/app.py`
5. Click "Deploy"!

### 3. **Configure Secrets**
In Streamlit Cloud dashboard:
1. Go to your app settings
2. Add secrets for LLM providers:

```toml
[llm_providers]
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
```

### 4. **Your app is live!** 🎉
You'll get a URL like: `https://your-username-mcp-resume-streamlit-client-app-xyz.streamlit.app`

## 🤖 LLM Provider Setup

### Option 1: OpenRouter (Recommended for Cloud)
- **Free models available!**
- Sign up at [OpenRouter](https://openrouter.ai)
- Get API key and add to Streamlit secrets
- Use free models like `meta-llama/llama-3.1-8b-instruct:free`

### Option 2: Ollama (Local only)
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
- Add to Streamlit secrets

## 🏗️ Architecture & Layout

### **System Architecture:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Streamlit App   │◄──►│ MCP Resume       │◄──►│ GitHub Gist     │
│ (Python)        │    │ Server (Node.js) │    │ (JSON Resume)   │
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

### **App Layout Structure:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    🎯 CONVERSION FUNNEL HEADER                   │
│  Step 1: "Spending hours screening?"  →  [Yes]                 │
│  Step 2: "What if AI did it in minutes?"  →  [Interested]      │
│  Step 3: "Built by Enterprise Developer"  →  [Credible]        │
│  Step 4: "Ready to transform hiring?"  →  [Get Quote]          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌─────────────────────────────────────────┐
│    SIDEBAR       │  │              MAIN CHAT AREA             │
│                  │  │                                         │
│ ⚡ ACTION PANEL   │  │  🎛️ System Controls                     │
│  🎯 Quick Actions │  │   • MCP Server Status & Control        │
│  ❓ Quick Questions│  │   • LLM Provider Status                │
│  📋 Job Analysis  │  │   • OpenRouter API Key Input           │
│                  │  │                                         │
│ ⚙️ CONFIGURATION  │  │  💬 Chat Interface (700px height)      │
│  📖 How to Use    │  │   • Chat Input (at top)               │
│  📄 Resume Source │  │   • Messages (newest first)           │
│  📡 MCP Server    │  │   • Timestamps on all messages        │
│  🤖 LLM Provider  │  │   • Interactive buttons in messages   │
│  🛠️ MCP Tools     │  │                                        │
│                  │  │                                         │
└──────────────────┘  └─────────────────────────────────────────┘
```

## 💡 Usage Examples

### 🎯 Conversion Funnel Flow:
1. **"Spending hours screening resumes?"** → [Yes]
2. **"What if AI did it in minutes?"** → [Interested]  
3. **"Built by Enterprise Developer"** → [Credible]
4. **"Ready to transform hiring?"** → [Get Quote]

### 💬 Chat Examples:
- "Tell me about Michael's work experience"
- "What are his technical skills?"
- "Summarize his background for a recruiter"
- "Find projects involving JavaScript"

### ⚡ Action Panel (Sidebar):
**🎯 Quick Actions:**
- **🔄 Clear Chat** - Reset conversation
- **📄 Full Resume** - Complete resume data
- **💼 Experience** - Work history only
- **🛠️ Skills** - Technical skills breakdown

**❓ Quick Questions Categories:**
- **🎯 Essential Questions**: "Summarize this candidate's profile", "What are their strongest technical skills?"
- **💼 For Recruiters**: "Is this candidate suitable for a senior role?", "What's their leadership experience?"
- **🔍 Technical Deep Dive**: "What programming languages are they expert in?", "Do they have cloud platform experience?"
- **🎯 Role-Specific**: "Are they suitable for a frontend role?", "Do they have backend development skills?"

**📋 Job Description Analysis:**
- Paste job description for AI-powered candidate fit analysis
- Get match score, strengths, gaps, and interview recommendations

### 🎛️ System Controls (Main Area):
- **🚀 Start MCP Server** - One-click server startup with status display
- **🔑 Add OpenRouter API Key** - Direct API key input with validation
- **Smart Status Display** - Real-time MCP server and LLM provider status

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# The app will open at http://localhost:8501
```

## 🌐 Deployment Options

### 1. **Streamlit Cloud (Free)** ⭐
- Free hosting for public repos
- Automatic updates from GitHub
- Built-in secrets management
- Perfect for demos and personal use

### 2. **Heroku (Free tier discontinued)**
- More complex setup
- Requires Procfile and additional config

### 3. **Railway, Render, etc.**
- Alternative cloud platforms
- Similar setup to Heroku

## 🎨 Features

### 🎯 Conversion Funnel Header
- **Business Psychology Funnel** - 4-step conversion process for hiring managers
- **Progressive Engagement** - Step-by-step value proposition
- **Call-to-Action** - Direct contact for enterprise solutions

### 💬 Modern Chat Interface
- **Reversed Chat Order** - Newest messages first (like modern messaging apps)
- **Chat Input at Top** - Easy access to message input
- **Real-time Processing** - Sequential message display with typing animations
- **Timestamped Messages** - Human-readable timestamps (Dec 19, 2:30 PM)

### ⚡ Sidebar Action Panel
- **Prominent Placement** - Action Panel at top of sidebar for immediate access
- **Quick Actions Grid** - 2x2 layout: Clear Chat, Full Resume, Experience, Skills
- **Categorized Questions** - Essential, Recruiter, Technical, and Role-Specific questions
- **Job Description Analysis** - Integrated candidate fit analysis tool
- **One-Click Access** - All most-used features immediately visible

### 🎛️ System Controls Panel (Main Area)
- **Clean Status Display** - Clear MCP server and LLM provider status
- **One-Click Server Control** - Start/stop MCP server with feedback
- **API Key Management** - Direct OpenRouter API key input with validation
- **Smart Help Text** - Contextual setup guidance

### 🔧 Enhanced Workflow
- **Auto-Processing** - Pending messages processed after server/API setup
- **Toast Notifications** - Real-time feedback for all actions
- **Sequential Processing** - Messages appear one after another naturally

### 🎨 Color-Neutral Design
- **Professional Appearance** - Neutral colors suitable for business use
- **Accessibility Focus** - High contrast, readable interface
- **Clean Typography** - Streamlined section headers and spacing
- **Responsive Layout** - 2-column layout optimized for all screen sizes

### Smart Context Fetching
The app automatically determines what resume data to fetch:
- Questions about "work/experience" → work history
- Questions about "skills/tech" → technical skills
- Questions with "search/find" → search functionality
- General questions → full resume summary

### Multi-Provider Support
Switch between LLM providers easily:
- **OpenRouter** - Free tier with open-source models
- **Ollama** - 100% local, unlimited (local only)
- **OpenAI** - High quality (paid)

### Streamlined Configuration
- **Collapsed Expanders** - Clean sidebar with organized sections
- **Focused Setup** - Essential configuration options only
- **Context-Aware Help** - Setup guidance when needed

## 🚀 Action Panel Workflow

### **Quick Start with Action Panel:**
1. **Open Sidebar** - Action Panel is at the top for immediate access
2. **Quick Actions** - Use 2x2 grid for instant resume data:
   - 🔄 Clear Chat | 💼 Experience
   - 📄 Full Resume | 🛠️ Skills
3. **Quick Questions** - Click to expand categories:
   - **🎯 Essential** - Core candidate questions
   - **💼 Recruiters** - Hiring manager focused
   - **🔍 Technical** - Deep technical assessment
   - **🎯 Role-Specific** - Position-specific queries
4. **Job Analysis** - Paste job description for candidate fit analysis

### **Professional Workflow:**
- **Recruiters**: Use "For Recruiters" questions + Job Description Analysis
- **Technical Leads**: Focus on "Technical Deep Dive" + "Role-Specific" questions
- **HR Teams**: Start with "Essential Questions" then use Job Analysis tool
- **All Users**: Quick Actions provide instant access to raw resume data

## 🆓 Free Usage Options

### Completely Free:
1. **Streamlit Cloud** - Free hosting
2. **OpenRouter** - Free models available
3. **GitHub** - Free repository hosting

### Total Cost: $0/month! 💰

## 🚨 Troubleshooting

### **App won't start locally?**
- Check if MCP Resume Server is running: `npm run dev`
- Verify Python dependencies: `pip install -r requirements.txt`
- Ensure you're in the correct directory: `cd streamlit-client`

### **"🔴 MCP Server: Disconnected" showing?**
- Click **🚀 Start MCP Server** in the System Controls panel
- Make sure the server path is correct in sidebar configuration
- Check if Node.js and npm are installed
- Verify the MCP server is built: `npm run build`

### **"⚠️ LLM Provider: Not configured" showing?**
- **OpenRouter**: Use **🔑 Add OpenRouter API Key** in System Controls
- **Ollama**: Only works locally, run `ollama serve` first
- **OpenAI**: Add API key in sidebar configuration

### **Messages not processing?**
- Check that both MCP server is connected (🟢) AND LLM provider is configured
- Try using Quick Questions in the sidebar Action Panel
- Use Quick Actions (📄 Full Resume, 💼 Experience, 🛠️ Skills) to test MCP connection
- Look for toast notifications showing processing status

### **Deployment issues on Streamlit Cloud?**
- Check Streamlit Cloud logs for errors
- Verify secrets are configured correctly in app settings
- Ensure repository is public (for free tier)
- Make sure main file path is set to: `streamlit-client/app.py`

## 📊 Comparison: Streamlit vs Node.js Client

| Feature | Streamlit Client | Node.js Client |
|---------|------------------|----------------|
| **Deployment** | Free on Streamlit Cloud | Requires hosting |
| **Setup** | 1 Python file | Multiple JS files |
| **UI** | Built-in chat interface | Custom React UI |
| **Local LLMs** | Ollama support | Full Ollama support |
| **Development Speed** | Very fast | Slower |
| **Customization** | Limited but sufficient | Full control |

## 🎯 Perfect For:

- **🎓 Students** - Free portfolio projects
- **💼 Job Seekers** - Demo to recruiters
- **🏢 Small Companies** - Internal resume search
- **🔬 Developers** - Learning MCP and LLMs
- **📊 Demos** - Quick proof of concepts

## 📄 License

MIT License - Open source and free to use!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test locally with `streamlit run app.py`
4. Submit a pull request

## 🎉 Get Started Now!

```bash
cd streamlit-client
pip install -r requirements.txt
streamlit run app.py
```

Then deploy to Streamlit Cloud for free hosting! 🚀 
# MCP Resume Client - Open Source LLM Chat

A modern web client for the MCP Resume Server that lets you chat about resume data using **any open-source LLM** - no vendor lock-in, no API limits!

## 🚀 Features

- **🤖 Multiple LLM Providers**: Ollama, OpenRouter, Hugging Face, LocalAI
- **🆓 100% Open Source**: No vendor lock-in, use any local or free models  
- **🎯 MCP Integration**: Direct connection to your MCP Resume Server
- **💬 Smart Context**: Automatically fetches relevant resume data for queries
- **🌐 Modern Web UI**: Beautiful, responsive chat interface
- **⚡ Real-time**: WebSocket-based for instant responses

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Client    │◄──►│  MCP Client      │◄──►│ MCP Resume      │
│   (Browser)     │    │  (Node.js)       │    │ Server          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   LLM Providers  │
                       │ • Ollama         │
                       │ • OpenRouter     │
                       │ • Hugging Face   │
                       │ • LocalAI        │
                       └──────────────────┘
```

## 📋 Prerequisites

1. **MCP Resume Server** - Must be running (from parent directory)
2. **Node.js 18+** - For the client server
3. **At least one LLM provider** configured (see below)

## 🛠️ Installation

```bash
cd client
npm install
```

## ⚙️ Configuration

Create a `.env` file in the `client` directory:

```env
# Server Configuration
PORT=3000
MCP_SERVER_PATH=../build/index.js

# Ollama (Local LLMs)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.2

# OpenRouter (Free Open-Source Models)
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_DEFAULT_MODEL=meta-llama/llama-3.1-8b-instruct:free

# Hugging Face
HUGGINGFACE_API_KEY=your_huggingface_key_here
HUGGINGFACE_DEFAULT_MODEL=microsoft/DialoGPT-medium

# LocalAI
LOCALAI_BASE_URL=http://localhost:8080
LOCALAI_DEFAULT_MODEL=gpt-3.5-turbo
```

## 🤖 LLM Provider Setup

### 1. Ollama (Recommended - 100% Local)

**Install Ollama:**
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

**Install models:**
```bash
ollama pull llama3.2        # Fast, good quality
ollama pull llama3.1        # Larger, better quality  
ollama pull mistral         # Alternative option
ollama pull codellama       # For code-related questions
```

**Start Ollama:**
```bash
ollama serve
```

### 2. OpenRouter (Free Tier Available)

1. Sign up at [OpenRouter](https://openrouter.ai)
2. Get your API key
3. Add to `.env` file
4. **Free models available**: `meta-llama/llama-3.1-8b-instruct:free`

### 3. Hugging Face (Free Tier)

1. Sign up at [Hugging Face](https://huggingface.co)
2. Get your API token
3. Add to `.env` file
4. **Note**: Inference API has rate limits on free tier

### 4. LocalAI (Self-hosted)

Follow [LocalAI installation guide](https://localai.io/basics/getting_started/)

## 🚀 Usage

### Start the Client

```bash
cd client
npm run dev
```

### Access the Interface

Open your browser and go to: **http://localhost:3000**

### Chat Examples

1. **Select a provider and model** from the sidebar
2. **Ask questions about the resume:**
   - "What is Michael's work experience?"
   - "Tell me about his technical skills"
   - "Summarize his background"
   - "Find experience with JavaScript"

### Direct MCP Tools

Use the sidebar buttons to call MCP tools directly:
- **Get Full Resume** - Complete resume data
- **Get Experience** - Work history only  
- **Get Skills** - Technical skills
- **Search Resume** - Find specific content

## 🎯 Quick Start with Ollama

**Fastest way to get started:**

```bash
# 1. Install and start Ollama
brew install ollama
ollama serve

# 2. Install a model
ollama pull llama3.2

# 3. Start the MCP Resume Server (in parent directory)
npm run dev

# 4. Start the client (in client directory)
cd client
npm install
npm run dev

# 5. Open http://localhost:3000
# 6. Select "Ollama" → "llama3.2" 
# 7. Start chatting!
```

## 🆓 Free Options

### Completely Free (No API Keys)
- **Ollama** - Run models locally, unlimited usage
- **LocalAI** - Self-hosted, unlimited usage

### Free Tier Available
- **OpenRouter** - Free models: `meta-llama/llama-3.1-8b-instruct:free`
- **Hugging Face** - Free inference API with rate limits

## 🔧 Development

```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🌐 API Endpoints

The client also exposes REST API endpoints:

```bash
# Get available providers
GET /api/providers

# Chat with an LLM
POST /api/chat
{
  "message": "Tell me about the work experience",
  "provider": "ollama", 
  "model": "llama3.2"
}

# Call MCP tools directly
POST /api/mcp/get_resume
POST /api/mcp/get_experience
POST /api/mcp/get_skills
POST /api/mcp/search_resume
```

## 🎨 Features

### Smart Context Fetching
The client automatically determines what resume data to fetch based on your question:
- Questions about "work" → fetches work experience
- Questions about "skills" → fetches technical skills  
- Questions about "search" → performs resume search
- General questions → fetches summary

### Multi-Provider Support
Switch between LLM providers seamlessly:
- **Ollama** - Local models, fast, private
- **OpenRouter** - Access to many models, some free
- **Hugging Face** - Research models, free tier
- **LocalAI** - Self-hosted OpenAI-compatible API

### Real-time Communication
- WebSocket connection for instant responses
- Automatic reconnection on disconnection
- Live status updates

## 🚨 Troubleshooting

**Can't connect to MCP server?**
- Make sure the MCP Resume Server is running
- Check the `MCP_SERVER_PATH` in `.env`

**Ollama not working?**
- Run `ollama serve` first
- Make sure models are downloaded: `ollama list`

**No providers available?**
- Check your `.env` configuration
- Verify API keys if using cloud providers
- Make sure local services (Ollama/LocalAI) are running

## 📄 License

MIT License - same as the MCP Resume Server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🎯 Use Cases

- **Job Applications** - Demo your resume to recruiters with AI assistance
- **Interview Prep** - Practice talking about your experience
- **Resume Analysis** - Get insights about your background
- **Professional Networking** - Quickly share your experience in conversations
- **Career Development** - Explore your background with AI guidance 
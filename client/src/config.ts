import dotenv from 'dotenv';

dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || '3000'),
  mcpServerPath: process.env.MCP_SERVER_PATH || '../build/index.js',
  
  // LLM Provider configurations
  ollama: {
    baseUrl: process.env.OLLAMA_BASE_URL || 'http://localhost:11434',
    defaultModel: process.env.OLLAMA_DEFAULT_MODEL || 'llama3.2',
  },
  
  openRouter: {
    apiKey: process.env.OPENROUTER_API_KEY,
    baseUrl: process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1',
    defaultModel: process.env.OPENROUTER_DEFAULT_MODEL || 'meta-llama/llama-3.1-8b-instruct:free',
  },
  
  huggingFace: {
    apiKey: process.env.HUGGINGFACE_API_KEY,
    baseUrl: process.env.HUGGINGFACE_BASE_URL || 'https://api-inference.huggingface.co/models',
    defaultModel: process.env.HUGGINGFACE_DEFAULT_MODEL || 'microsoft/DialoGPT-medium',
  },
  
  localAI: {
    baseUrl: process.env.LOCALAI_BASE_URL || 'http://localhost:8080',
    defaultModel: process.env.LOCALAI_DEFAULT_MODEL || 'gpt-3.5-turbo',
  }
}; 
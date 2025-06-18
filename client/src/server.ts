import express from 'express';
import cors from 'cors';
import { WebSocketServer } from 'ws';
import { createServer } from 'http';
import { MCPClient } from './mcp-client.js';
import { LLMProviders } from './llm-providers.js';
import { config } from './config.js';

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// MCP Client instance
const mcpClient = new MCPClient();
const llmProviders = new LLMProviders();

// WebSocket connection for real-time chat
wss.on('connection', (ws) => {
  console.log('Client connected');

  ws.on('message', async (message) => {
    try {
      const data = JSON.parse(message.toString());
      
      switch (data.type) {
        case 'chat':
          await handleChatMessage(ws, data);
          break;
        case 'mcp_tool':
          await handleMCPTool(ws, data);
          break;
        case 'get_providers':
          ws.send(JSON.stringify({
            type: 'providers',
            providers: llmProviders.getAvailableProviders()
          }));
          break;
      }
    } catch (error) {
      ws.send(JSON.stringify({
        type: 'error',
        error: `Error processing message: ${error instanceof Error ? error.message : 'Unknown error'}`
      }));
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

async function handleChatMessage(ws: any, data: any) {
  const { message, provider, model } = data;
  
  try {
    // First, get relevant resume data based on the message
    const resumeContext = await getResumeContext(message);
    
    // Send the context and message to the LLM
    const response = await llmProviders.chat(provider, model, message, resumeContext);
    
    ws.send(JSON.stringify({
      type: 'chat_response',
      response,
      context: resumeContext
    }));
  } catch (error) {
    ws.send(JSON.stringify({
      type: 'error',
      error: `Chat error: ${error instanceof Error ? error.message : 'Unknown error'}`
    }));
  }
}

async function handleMCPTool(ws: any, data: any) {
  const { tool, args } = data;
  
  try {
    const result = await mcpClient.callTool(tool, args);
    
    ws.send(JSON.stringify({
      type: 'mcp_response',
      tool,
      result
    }));
  } catch (error) {
    ws.send(JSON.stringify({
      type: 'error',
      error: `MCP tool error: ${error instanceof Error ? error.message : 'Unknown error'}`
    }));
  }
}

async function getResumeContext(message: string): Promise<string> {
  try {
    // Analyze the message to determine what resume data to fetch
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('experience') || lowerMessage.includes('work') || lowerMessage.includes('job')) {
      const experience = await mcpClient.callTool('get_experience', {});
      return `Work Experience:\n${JSON.stringify(experience, null, 2)}`;
    }
    
    if (lowerMessage.includes('skill') || lowerMessage.includes('technology') || lowerMessage.includes('programming')) {
      const skills = await mcpClient.callTool('get_skills', {});
      return `Skills:\n${JSON.stringify(skills, null, 2)}`;
    }
    
    if (lowerMessage.includes('search') || lowerMessage.includes('find')) {
      // Extract search terms from the message
      const searchTerms = extractSearchTerms(message);
      if (searchTerms.length > 0) {
        const searchResults = await mcpClient.callTool('search_resume', { query: searchTerms.join(' ') });
        return `Search Results:\n${JSON.stringify(searchResults, null, 2)}`;
      }
    }
    
    // Default: get the summary for general questions
    const resume = await mcpClient.callTool('get_resume', { format: 'text' });
    return `Resume Summary:\n${resume}`;
    
  } catch (error) {
    console.error('Error getting resume context:', error);
    return 'Resume data is currently unavailable.';
  }
}

function extractSearchTerms(message: string): string[] {
  // Simple extraction - could be improved with NLP
  const words = message.toLowerCase().split(' ');
  const skipWords = ['search', 'find', 'look', 'for', 'about', 'what', 'when', 'where', 'how', 'the', 'a', 'an', 'is', 'are', 'was', 'were'];
  return words.filter(word => word.length > 2 && !skipWords.includes(word));
}

// REST API endpoints
app.get('/api/providers', (req, res) => {
  res.json(llmProviders.getAvailableProviders());
});

app.post('/api/chat', async (req, res) => {
  try {
    const { message, provider, model } = req.body;
    const resumeContext = await getResumeContext(message);
    const response = await llmProviders.chat(provider, model, message, resumeContext);
    
    res.json({ response, context: resumeContext });
  } catch (error) {
    res.status(500).json({ error: error instanceof Error ? error.message : 'Unknown error' });
  }
});

app.post('/api/mcp/:tool', async (req, res) => {
  try {
    const { tool } = req.params;
    const args = req.body;
    const result = await mcpClient.callTool(tool, args);
    
    res.json({ result });
  } catch (error) {
    res.status(500).json({ error: error instanceof Error ? error.message : 'Unknown error' });
  }
});

// Initialize and start server
async function startServer() {
  try {
    await mcpClient.connect();
    console.log('✅ Connected to MCP Resume Server');
    
    const port = config.port || 3000;
    server.listen(port, () => {
      console.log(`🚀 MCP Resume Client running on http://localhost:${port}`);
      console.log(`📡 WebSocket server ready for connections`);
      console.log(`🤖 Supported LLM providers: ${llmProviders.getAvailableProviders().join(', ')}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer(); 
import fetch from 'node-fetch';
import { config } from './config.js';

export interface LLMProvider {
  name: string;
  models: string[];
  isAvailable: () => Promise<boolean>;
  chat: (model: string, message: string, context: string) => Promise<string>;
}

export class LLMProviders {
  private providers: Map<string, LLMProvider> = new Map();

  constructor() {
    this.initializeProviders();
  }

  private initializeProviders() {
    // Ollama Provider
    this.providers.set('ollama', {
      name: 'Ollama',
      models: ['llama3.2', 'llama3.1', 'llama2', 'codellama', 'mistral', 'mixtral'],
      isAvailable: async () => {
        try {
          const response = await fetch(`${config.ollama.baseUrl}/api/tags`);
          return response.ok;
        } catch {
          return false;
        }
      },
      chat: async (model: string, message: string, context: string) => {
        const prompt = `Context: ${context}\n\nUser: ${message}\n\nAssistant: `;
        
        const response = await fetch(`${config.ollama.baseUrl}/api/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model,
            prompt,
            stream: false,
          }),
        });

        if (!response.ok) {
          throw new Error(`Ollama API error: ${response.statusText}`);
        }

        const data = await response.json() as any;
        return data.response;
      },
    });

    // OpenRouter Provider (for free open-source models)
    this.providers.set('openrouter', {
      name: 'OpenRouter',
      models: [
        'meta-llama/llama-3.1-8b-instruct:free',
        'meta-llama/llama-3.2-3b-instruct:free',
        'microsoft/phi-3-mini-128k-instruct:free',
        'huggingfaceh4/zephyr-7b-beta:free',
      ],
      isAvailable: async () => {
        return !!config.openRouter.apiKey;
      },
      chat: async (model: string, message: string, context: string) => {
        if (!config.openRouter.apiKey) {
          throw new Error('OpenRouter API key not configured');
        }

        const response = await fetch(`${config.openRouter.baseUrl}/chat/completions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${config.openRouter.apiKey}`,
          },
          body: JSON.stringify({
            model,
            messages: [
              { role: 'system', content: `You are a helpful assistant. Use this context about the user's resume: ${context}` },
              { role: 'user', content: message },
            ],
          }),
        });

        if (!response.ok) {
          throw new Error(`OpenRouter API error: ${response.statusText}`);
        }

        const data = await response.json() as any;
        return data.choices[0].message.content;
      },
    });

    // Hugging Face Provider
    this.providers.set('huggingface', {
      name: 'Hugging Face',
      models: [
        'microsoft/DialoGPT-medium',
        'google/flan-t5-large',
        'microsoft/DialoGPT-large',
      ],
      isAvailable: async () => {
        return !!config.huggingFace.apiKey;
      },
      chat: async (model: string, message: string, context: string) => {
        if (!config.huggingFace.apiKey) {
          throw new Error('Hugging Face API key not configured');
        }

        const prompt = `Context: ${context}\n\nUser: ${message}\n\nAssistant:`;
        
        const response = await fetch(`${config.huggingFace.baseUrl}/${model}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${config.huggingFace.apiKey}`,
          },
          body: JSON.stringify({
            inputs: prompt,
            parameters: {
              max_new_tokens: 500,
              temperature: 0.7,
            },
          }),
        });

        if (!response.ok) {
          throw new Error(`Hugging Face API error: ${response.statusText}`);
        }

        const data = await response.json() as any;
        return Array.isArray(data) ? data[0]?.generated_text?.replace(prompt, '') || 'No response' : 'No response';
      },
    });

    // LocalAI Provider
    this.providers.set('localai', {
      name: 'LocalAI',
      models: ['gpt-3.5-turbo', 'gpt-4', 'llama-2-7b', 'codellama'],
      isAvailable: async () => {
        try {
          const response = await fetch(`${config.localAI.baseUrl}/v1/models`);
          return response.ok;
        } catch {
          return false;
        }
      },
      chat: async (model: string, message: string, context: string) => {
        const response = await fetch(`${config.localAI.baseUrl}/v1/chat/completions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model,
            messages: [
              { role: 'system', content: `You are a helpful assistant. Use this context about the user's resume: ${context}` },
              { role: 'user', content: message },
            ],
          }),
        });

        if (!response.ok) {
          throw new Error(`LocalAI API error: ${response.statusText}`);
        }

        const data = await response.json() as any;
        return data.choices[0].message.content;
      },
    });
  }

  async getAvailableProviders(): Promise<string[]> {
    const available: string[] = [];
    
    for (const [name, provider] of this.providers) {
      try {
        if (await provider.isAvailable()) {
          available.push(name);
        }
      } catch {
        // Provider not available
      }
    }
    
    return available;
  }

  getProvider(name: string): LLMProvider | undefined {
    return this.providers.get(name);
  }

  async chat(providerName: string, model: string, message: string, context: string): Promise<string> {
    const provider = this.providers.get(providerName);
    
    if (!provider) {
      throw new Error(`Provider ${providerName} not found`);
    }

    if (!(await provider.isAvailable())) {
      throw new Error(`Provider ${providerName} is not available`);
    }

    return provider.chat(model, message, context);
  }

  getModelsForProvider(providerName: string): string[] {
    const provider = this.providers.get(providerName);
    return provider ? provider.models : [];
  }
} 
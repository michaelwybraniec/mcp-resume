import { spawn } from 'child_process';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { config } from './config.js';

export class MCPClient {
  private client: Client;
  private transport: StdioClientTransport | null = null;
  private serverProcess: any = null;

  constructor() {
    this.client = new Client(
      {
        name: 'mcp-resume-client',
        version: '0.1.0',
      },
      {
        capabilities: {},
      }
    );
  }

  async connect(): Promise<void> {
    try {
      // Start the MCP server process
      this.serverProcess = spawn('node', [config.mcpServerPath], {
        stdio: ['pipe', 'pipe', 'pipe'],
      });

      if (!this.serverProcess.stdout || !this.serverProcess.stdin) {
        throw new Error('Failed to create server process stdio');
      }

      // Create transport
      this.transport = new StdioClientTransport({
        reader: this.serverProcess.stdout,
        writer: this.serverProcess.stdin,
      });

      // Connect to server
      await this.client.connect(this.transport);

      console.log('✅ MCP Client connected to resume server');
    } catch (error) {
      throw new Error(`Failed to connect to MCP server: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async disconnect(): Promise<void> {
    if (this.transport) {
      await this.client.close();
      this.transport = null;
    }

    if (this.serverProcess) {
      this.serverProcess.kill();
      this.serverProcess = null;
    }
  }

  async listTools(): Promise<any> {
    try {
      const response = await this.client.request(
        { method: 'tools/list', params: {} },
        'ListToolsResult'
      );
      return response.tools;
    } catch (error) {
      throw new Error(`Failed to list tools: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async listResources(): Promise<any> {
    try {
      const response = await this.client.request(
        { method: 'resources/list', params: {} },
        'ListResourcesResult'
      );
      return response.resources;
    } catch (error) {
      throw new Error(`Failed to list resources: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async callTool(name: string, args: any = {}): Promise<any> {
    try {
      const response = await this.client.request(
        {
          method: 'tools/call',
          params: {
            name,
            arguments: args,
          },
        },
        'CallToolResult'
      );
      return response.content;
    } catch (error) {
      throw new Error(`Failed to call tool ${name}: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async readResource(uri: string): Promise<any> {
    try {
      const response = await this.client.request(
        {
          method: 'resources/read',
          params: { uri },
        },
        'ReadResourceResult'
      );
      return response.contents;
    } catch (error) {
      throw new Error(`Failed to read resource ${uri}: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }
} 
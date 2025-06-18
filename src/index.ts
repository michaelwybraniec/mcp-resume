#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { ResumeService } from './services/resumeService.js';
import { config } from './config.js';

class ResumeServer {
  private server: Server;
  private resumeService: ResumeService;

  constructor() {
    this.server = new Server(
      {
        name: 'mcp-resume',
        version: '0.1.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.resumeService = new ResumeService(config.gistId, config.githubToken);
    this.setupHandlers();
  }

  private setupHandlers() {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: 'resume://cv',
            name: 'Michael Wybraniec - CV',
            description: 'Complete CV/Resume data from GitHub gist',
            mimeType: 'application/json',
          },
          {
            uri: 'resume://summary',
            name: 'Michael Wybraniec - Professional Summary',
            description: 'Professional summary from CV',
            mimeType: 'text/plain',
          },
          {
            uri: 'resume://experience',
            name: 'Michael Wybraniec - Work Experience',
            description: 'Work experience details from CV',
            mimeType: 'application/json',
          },
          {
            uri: 'resume://skills',
            name: 'Michael Wybraniec - Skills',
            description: 'Technical and professional skills',
            mimeType: 'application/json',
          },
        ],
      };
    });

    // Read specific resources
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      
      try {
        const resumeData = await this.resumeService.getResume();
        
        switch (uri) {
          case 'resume://cv':
            return {
              contents: [
                {
                  uri,
                  mimeType: 'application/json',
                  text: JSON.stringify(resumeData, null, 2),
                },
              ],
            };
            
          case 'resume://summary':
            return {
              contents: [
                {
                  uri,
                  mimeType: 'text/plain',
                  text: resumeData.basics?.summary || 'No summary available',
                },
              ],
            };
            
          case 'resume://experience':
            return {
              contents: [
                {
                  uri,
                  mimeType: 'application/json',
                  text: JSON.stringify(resumeData.work || [], null, 2),
                },
              ],
            };
            
          case 'resume://skills':
            return {
              contents: [
                {
                  uri,
                  mimeType: 'application/json',
                  text: JSON.stringify(resumeData.skills || [], null, 2),
                },
              ],
            };
            
          default:
            throw new Error(`Unknown resource: ${uri}`);
        }
      } catch (error) {
        throw new Error(`Failed to fetch resume data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    });

    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'get_resume',
            description: 'Get the complete CV/Resume data',
            inputSchema: {
              type: 'object',
              properties: {
                format: {
                  type: 'string',
                  enum: ['json', 'text'],
                  description: 'Output format (json or text)',
                  default: 'json',
                },
              },
            },
          },
          {
            name: 'get_experience',
            description: 'Get work experience details',
            inputSchema: {
              type: 'object',
              properties: {
                company: {
                  type: 'string',
                  description: 'Filter by company name (optional)',
                },
              },
            },
          },
          {
            name: 'get_skills',
            description: 'Get technical and professional skills',
            inputSchema: {
              type: 'object',
              properties: {
                category: {
                  type: 'string',
                  description: 'Filter by skill category (optional)',
                },
              },
            },
          },
          {
            name: 'search_resume',
            description: 'Search for specific content in the resume',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Search query',
                },
              },
              required: ['query'],
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      try {
        const resumeData = await this.resumeService.getResume();
        
        switch (name) {
          case 'get_resume':
            const format = args?.format || 'json';
            if (format === 'text') {
              return {
                content: [
                  {
                    type: 'text',
                    text: this.resumeService.formatAsText(resumeData),
                  },
                ],
              };
            }
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(resumeData, null, 2),
                },
              ],
            };
            
          case 'get_experience':
            const experience = resumeData.work || [];
            const filteredExperience = (args as any)?.company 
              ? experience.filter(job => 
                  job.company?.toLowerCase().includes((args as any).company.toLowerCase())
                )
              : experience;
            
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(filteredExperience, null, 2),
                },
              ],
            };
            
          case 'get_skills':
            const skills = resumeData.skills || [];
            const filteredSkills = (args as any)?.category
              ? skills.filter(skill => 
                  skill.name?.toLowerCase().includes((args as any).category.toLowerCase())
                )
              : skills;
            
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(filteredSkills, null, 2),
                },
              ],
            };
            
          case 'search_resume':
            const query = ((args as any)?.query as string)?.toLowerCase() || '';
            const results = this.resumeService.searchResume(resumeData, query);
            
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(results, null, 2),
                },
              ],
            };
            
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        throw new Error(`Tool execution failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('MCP Resume Server running on stdio');
  }
}

const server = new ResumeServer();
server.run().catch(console.error); 
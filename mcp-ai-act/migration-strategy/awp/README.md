# AI Act Compliance Migration - AWP Integration

This directory contains AWP-compatible files for generating a detailed migration backlog using MCP-Agentic-SDLC's Agentic Workflow Protocol.

## Files in this Directory

- **`base.md`** - Contains the questions that the `base` tool would ask (placeholder)
- **`README.md`** - This file with installation and usage instructions

## Getting Started

1. **First, run a compliance analysis** using the `check_compliance` tool
2. **Then, prepare the migration backlog** using the `prepare_migration_backlog` tool
3. **This will populate the `base.md` file** with your specific compliance requirements
4. **Follow the instructions below** to use AWP for automated backlog generation

## What is AWP?

The Agentic Workflow Protocol (AWP) is a framework for creating structured, actionable project backlogs from high-level project descriptions. It's part of the MCP-Agentic-SDLC server.

## Installation Instructions

### Option 1: Install MCP-Agentic-SDLC

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/mcp-agentic-sdlc.git
   cd mcp-agentic-sdlc
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Build the project:**
   ```bash
   npm run build
   ```

4. **Add to your Cursor MCP configuration:**
   
   Edit `~/.cursor/mcp.json` and add:
   ```json
   {
     "mcpServers": {
       "sdlc": {
         "command": "node",
         "args": ["/path/to/mcp-agentic-sdlc/dist/index.js"]
       }
     }
   }
   ```

5. **Restart Cursor** to load the new MCP server

### Option 2: Use the base.md Manually

If you prefer not to install MCP-Agentic-SDLC, you can:

1. **Review the `base.md` file** - it contains all the questions you need to answer
2. **Answer the questions** based on your specific AI system and compliance needs
3. **Create your own migration plan** using the structured questions as a guide

## Usage with AWP

Once MCP-Agentic-SDLC is installed:

1. **Open Cursor** and ensure the `sdlc` MCP server is connected
2. **Use the `base` tool** to start the project setup process
3. **Answer the questions** from the `base.md` file
4. **Generate the migration backlog** using the `init` tool
5. **Review and customize** the generated backlog items

## Benefits of Using AWP

- **Structured Approach:** Systematic breakdown of complex compliance requirements
- **Actionable Items:** Concrete tasks with clear priorities and dependencies
- **Context Engineering:** Proper project context and stakeholder alignment
- **Scalable:** Can handle complex multi-phase compliance projects
- **Traceable:** Clear audit trail from requirements to implementation

---
*This is a placeholder README. Run the migration backlog preparation to get specific instructions for your compliance requirements.*

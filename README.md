# MCP Resume Server

A Model Context Protocol (MCP) server that fetches your CV/Resume from a GitHub gist and provides it to LLMs for enhanced conversations about your professional background.

## Features

- ✅ Fetches CV data from GitHub gist automatically
- ✅ Provides multiple tools for querying resume data
- ✅ Supports both JSON and text output formats
- ✅ Includes search functionality across all resume sections
- ✅ Caches data to reduce API calls
- ✅ Supports both public and private gists (with token)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd mcp-resume
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your GitHub gist ID and token (if needed)
```

4. Build the project:
```bash
npm run build
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# GitHub Gist Configuration
GITHUB_GIST_ID=dabf368473d41748e9d6051afb67efcf
GITHUB_TOKEN=your_github_token_here_optional
CACHE_TIMEOUT=300000
```

- `GITHUB_GIST_ID`: Your gist ID (defaults to Michael's public gist)
- `GITHUB_TOKEN`: Optional GitHub token for private gists or higher rate limits
- `CACHE_TIMEOUT`: Cache timeout in milliseconds (default: 5 minutes)

### Gist Structure

Your gist should contain a file named `resume.json` following the [JSON Resume](https://jsonresume.org/) schema format.

## Usage

### Running the Server

```bash
npm run dev
```

Or for production:

```bash
npm start
```

### MCP Tools

The server provides the following tools:

1. **get_resume** - Get the complete CV/Resume data
   - Parameters: `format` (json|text)

2. **get_experience** - Get work experience details
   - Parameters: `company` (optional filter)

3. **get_skills** - Get technical and professional skills
   - Parameters: `category` (optional filter)

4. **search_resume** - Search for specific content in the resume
   - Parameters: `query` (required)

### MCP Resources

The server provides these resources:

- `resume://cv` - Complete CV data (JSON)
- `resume://summary` - Professional summary (text)
- `resume://experience` - Work experience (JSON)
- `resume://skills` - Skills list (JSON)

## Integration with LLM Clients

### Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "mcp-resume": {
      "command": "node",
      "args": ["/path/to/mcp-resume/build/index.js"],
      "env": {
        "GITHUB_GIST_ID": "your-gist-id-here"
      }
    }
  }
}
```

### Other MCP Clients

The server communicates via stdio and follows the MCP specification, making it compatible with any MCP-compliant client.

## Development

```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## GitHub Gist Setup

1. Create a new gist on GitHub
2. Add a file named `resume.json`
3. Use the JSON Resume schema format
4. Get the gist ID from the URL (e.g., `dabf368473d41748e9d6051afb67efcf`)

## Example Resume Data

Your `resume.json` should follow this structure:

```json
{
  "basics": {
    "name": "Your Name",
    "label": "Your Professional Title",
    "email": "your.email@example.com",
    "phone": "Your Phone Number",
    "url": "https://your-website.com",
    "summary": "Your professional summary here..."
  },
  "work": [
    {
      "company": "Company Name",
      "position": "Your Position",
      "startDate": "2020-01-01",
      "endDate": "2023-12-31",
      "summary": "Job description...",
      "highlights": ["Achievement 1", "Achievement 2"]
    }
  ],
  "education": [...],
  "skills": [...],
  "languages": [...],
  "interests": [...],
  "references": [...]
}
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

If you encounter any issues or have questions, please open an issue on GitHub. 